"""Medición común de los bots de Centauro: resolución real y créditos por llamada resuelta.

Uso: python3 -I scripts/medir_bots.py <llamadas.json> [--fin AAAA-MM-DDTHH:MM:SSZ] [--contexto otras.json]
- llamadas.json: lista de llamadas ya normalizadas (las arma la rutina de medición), con "run_id",
  "workflow" (atencion | prolongaciones | minibus), "version", "inicio" (ISO UTC), "from_hash" (10 caracteres o ""),
  "opcion_menu", "turnos_cliente", "transferencias": [{"cola", "ts", "error"}], "llego_agente" (bool o null),
  "creditos" (número o null), "saltos", "duracion_s" y "motivo".
- --fin: instante de referencia (por defecto, ahora). Las llamadas de las 48 h anteriores a `fin` no entran en
  la resolución real, porque todavía pueden recibir una rellamada. `con_margen` cuenta las llamadas que sí entran:
  si es menor que `llamadas`, la resolución del grupo está medida solo con una parte.
- --contexto: uno o varios ficheros separados por comas con llamadas de otros días (mismo formato) que solo sirven para buscar rellamadas; no se miden.
- Imprime una tabla y escribe <llamadas>.indicadores.json junto al fichero de entrada.

Solo lectura y sin dependencias externas. Ningún indicador depende del nombre de las colas: solo se cuenta si hubo
transferencias (la normalización de `gestion` / `gestion_reserva` es cosa de la rutina).
"""
import importlib.util
import json
import os
import sys
from datetime import datetime, timedelta, timezone

UTC = timezone.utc
VENTANA_RELLAMADA = timedelta(hours=48)
CORTE_S = 600
MIN_TURNOS_CLIENTE = 2
SALTOS_ALTOS = 3

RUTA_CONTEXTO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "casos", "atencion-es", "codigo",
                             "contexto_llamada.py")


def _cargar_contexto():
    especificacion = importlib.util.spec_from_file_location("contexto_llamada", RUTA_CONTEXTO)
    modulo = importlib.util.module_from_spec(especificacion)
    especificacion.loader.exec_module(modulo)
    return modulo


_contexto = _cargar_contexto()
gestion_abierta_en = _contexto.gestion_abierta_en
modo_virtual_en = _contexto.modo_virtual_en


def _a_fecha(texto):
    return datetime.fromisoformat(texto.replace("Z", "+00:00"))


def _en_utc(t):
    return t.replace(tzinfo=UTC) if t.tzinfo is None else t.astimezone(UTC)


def franja(inicio_utc):
    """gestion_abierta | gestion_cerrada | modo_virtual según el horario del bot único."""
    inicio_utc = _en_utc(inicio_utc)
    if gestion_abierta_en(inicio_utc):
        return "gestion_abierta"
    if modo_virtual_en(inicio_utc):
        return "modo_virtual"
    return "gestion_cerrada"


def rellamadas(llamadas):
    """run_id de las llamadas con otra llamada del mismo from_hash en las 48 h siguientes (cualquier workflow)."""
    por_numero = {}
    for ll in llamadas:
        if ll.get("from_hash"):
            por_numero.setdefault(ll["from_hash"], []).append((_a_fecha(ll["inicio"]), ll["run_id"]))
    resultado = set()
    for lista in por_numero.values():
        for inicio, run_id in lista:
            if any(inicio < otro <= inicio + VENTANA_RELLAMADA for otro, rid in lista if rid != run_id):
                resultado.add(run_id)
    return resultado


def resuelta(llamada, con_rellamada):
    """Sin transferencias, con al menos 2 turnos del cliente y sin rellamada."""
    return (not llamada.get("transferencias")
            and (llamada.get("turnos_cliente") or 0) >= MIN_TURNOS_CLIENTE
            and llamada["run_id"] not in con_rellamada)


def _pct(parte, total):
    return round(100.0 * parte / total, 1) if total else None


def _grupo(llamadas, con_rellamada, fin):
    """Indicadores de un conjunto de llamadas. Resolución y créditos por resuelta usan solo las llamadas con 48 h de
    margen antes de `fin`; el resto usa todas."""
    elegibles = [ll for ll in llamadas if _a_fecha(ll["inicio"]) <= fin - VENTANA_RELLAMADA]
    resueltas = [ll for ll in elegibles if resuelta(ll, con_rellamada)]
    transferidas = [ll for ll in llamadas if ll.get("transferencias")]
    con_dato_agente = [ll for ll in transferidas if ll.get("llego_agente") is not None]
    con_saltos = [ll for ll in llamadas if ll.get("saltos") is not None]
    duraciones = [ll["duracion_s"] for ll in llamadas if ll.get("duracion_s") is not None]

    def creditos_totales(lista):
        # Si falta el dato en alguna llamada, la cifra no es fiable: null
        if not lista or any(ll.get("creditos") is None for ll in lista):
            return None
        return sum(ll["creditos"] for ll in lista)

    total_todas = creditos_totales(llamadas)
    total_elegibles = creditos_totales(elegibles)
    return {
        "llamadas": len(llamadas),
        "con_margen": len(elegibles),
        "resolucion_real": _pct(len(resueltas), len(elegibles)),
        "pct_transferidas": _pct(len(transferidas), len(llamadas)),
        "pct_llegan_agente": _pct(sum(1 for ll in con_dato_agente if ll["llego_agente"]), len(con_dato_agente)),
        "rellamadas_48h": sum(1 for ll in llamadas if ll["run_id"] in con_rellamada),
        "creditos_llamada": round(total_todas / len(llamadas), 1) if total_todas is not None else None,
        "creditos_resuelta": (round(total_elegibles / len(resueltas), 1)
                              if total_elegibles is not None and resueltas else None),
        "pct_3_saltos": _pct(sum(1 for ll in con_saltos if ll["saltos"] >= SALTOS_ALTOS), len(con_saltos)),
        "cortes_600": sum(1 for ll in llamadas if (ll.get("duracion_s") or 0) >= CORTE_S),
        "duracion_media": round(sum(duraciones) / len(duraciones), 1) if duraciones else None,
    }


def indicadores(llamadas, fin, contexto=None):
    """Indicadores por (workflow, opción), por franja y por (workflow, opción, franja). `contexto`: llamadas de otros
    días que solo cuentan para buscar rellamadas (no se miden)."""
    fin = _en_utc(fin)
    con_rellamada = rellamadas(list(llamadas) + list(contexto or []))
    claves = {
        "por_opcion": lambda ll: "%s/%s" % (ll["workflow"], ll["opcion_menu"]),
        "por_franja": lambda ll: franja(_a_fecha(ll["inicio"])),
        "por_opcion_franja": lambda ll: "%s/%s/%s" % (ll["workflow"], ll["opcion_menu"], franja(_a_fecha(ll["inicio"]))),
    }
    resultado = {"fin": fin.isoformat().replace("+00:00", "Z")}
    for nombre, clave in claves.items():
        grupos = {}
        for ll in llamadas:
            grupos.setdefault(clave(ll), []).append(ll)
        resultado[nombre] = {k: _grupo(v, con_rellamada, fin) for k, v in sorted(grupos.items())}
    return resultado


def tabla(resultado):
    columnas = ["llamadas", "resolucion_real", "pct_transferidas", "pct_llegan_agente", "rellamadas_48h",
                "creditos_llamada", "creditos_resuelta", "pct_3_saltos", "cortes_600", "duracion_media"]
    lineas = []
    for seccion in ("por_opcion", "por_franja", "por_opcion_franja"):
        lineas.append("== %s ==" % seccion)
        lineas.append("%-44s" % "grupo" + "".join("%18s" % c for c in columnas))
        for grupo, valores in resultado[seccion].items():
            lineas.append("%-44s" % grupo + "".join("%18s" % ("-" if valores[c] is None else valores[c])
                                                   for c in columnas))
    return "\n".join(lineas)


def main(argv):
    args = list(argv)
    fin = datetime.now(UTC)
    if "--fin" in args:
        i = args.index("--fin")
        fin = _a_fecha(args[i + 1])
        del args[i:i + 2]
    contexto = []
    if "--contexto" in args:
        i = args.index("--contexto")
        for ruta_contexto in filter(None, args[i + 1].split(",")):
            with open(ruta_contexto) as f:
                contexto += json.load(f)
        del args[i:i + 2]
    if len(args) != 1:
        print("Uso: python3 -I medir_bots.py <llamadas.json> [--fin AAAA-MM-DDTHH:MM:SSZ] [--contexto otras.json]")
        return 2
    ruta = args[0]
    with open(ruta) as f:
        llamadas = json.load(f)
    resultado = indicadores(llamadas, fin, contexto)
    print(tabla(resultado))
    salida = os.path.splitext(ruta)[0] + ".indicadores.json"
    with open(salida, "w") as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)
    print("Escrito %s" % salida)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
