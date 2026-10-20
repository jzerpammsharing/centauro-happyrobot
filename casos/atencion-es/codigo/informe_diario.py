"""Documento diario del artefacto «Calidad Atención España» (colección `informes`, doc_id = AAAA-MM-DD).

Uso: python3 -I casos/atencion-es/codigo/informe_diario.py <llamadas.json> --fecha AAAA-MM-DD [--fin ISO] [--fase N]
     [--contexto a.json,b.json] [--pruebas llamadas_pruebas.json] -o <informe.json>
- llamadas.json: el de scripts/normalizar_llamadas.py (los tres workflows del día); lee <llamadas>.avisos.json si existe.
- --contexto: llamadas.json de los días de alrededor (separados por comas), solo para buscar rellamadas.
- --pruebas: llamadas de prueba del bot único (normalizar_llamadas.py --pruebas); se miden aparte (`pruebas` del
  documento) y alimentan la puerta 0 (créditos de prolongación y medición con los runs de prueba).
- --fin: instante de referencia de la resolución real (por defecto, ahora); --fase: 0, 1 o 2 (spec §8.2; por defecto 0).
- Escribe el documento listo para `ArtifactData set`. La rutina rellena después `resumen`, `alerta`, `incidencias` y,
  los lunes, `auditoria`, y conserva los campos que escriben las personas.

Los indicadores son los de scripts/medir_bots.py (importado por ruta). Las puertas de §8.4 se evalúan con las cifras
del día: son orientativas, porque las puertas 1 y 2 se deciden con dos semanas completas (§8.3).
"""
import importlib.util
import json
import os
import sys
from datetime import datetime, timezone

UTC = timezone.utc
AQUI = os.path.dirname(os.path.abspath(__file__))
RUTA_MEDIR = os.path.join(AQUI, "..", "..", "..", "scripts", "medir_bots.py")


def _cargar_medir():
    especificacion = importlib.util.spec_from_file_location("medir_bots", RUTA_MEDIR)
    modulo = importlib.util.module_from_spec(especificacion)
    especificacion.loader.exec_module(modulo)
    return modulo


medir = _cargar_medir()

PARADAS_R43 = ("gestion_cerrada", "modo_virtual")
LIMITE_CREDITOS_PROLONGACION = 80
LIMITE_CREDITOS_MINIBUS = 64
RESOLUCION_MINIBUS = 47.0
MARGEN_RESOLUCION = 2.0
MARGEN_TRANSFERIDAS = 2.0
FACTOR_CREDITOS_RESUELTA = 0.7
MAX_PCT_3_SALTOS = 2.0


def transferencias_prohibidas(llamadas):
    """Por workflow: transferencias ejecutadas a Gestión fuera de su horario, las paradas por «Preparar
    transferencia» (R43, no se ejecutan) y las enviadas a un menú automático (2114, 2115, 2119)."""
    resultado = {}
    for ll in llamadas:
        cuenta = resultado.setdefault(ll["workflow"], {"gestion_cerrada": 0, "gestion_cerrada_paradas": 0, "menus": 0})
        for t in ll.get("transferencias") or []:
            if t["cola"] == "menu_automatico":
                cuenta["menus"] += 1
            elif t["cola"] == "gestion" and medir.franja(medir._a_fecha(t["ts"])) != "gestion_abierta":
                if t.get("error") in PARADAS_R43:
                    cuenta["gestion_cerrada_paradas"] += 1
                else:
                    cuenta["gestion_cerrada"] += 1
    return resultado


def _filas(resultado):
    filas = []
    for clave, valores in resultado["por_opcion"].items():
        workflow, opcion = clave.split("/")
        filas.append(dict(workflow=workflow, opcion=opcion, franja="todas", **valores))
    for clave, valores in resultado["por_opcion_franja"].items():
        workflow, opcion, franja = clave.split("/")
        filas.append(dict(workflow=workflow, opcion=opcion, franja=franja, **valores))
    return filas


def _fila(filas, workflow, opcion):
    for f in filas:
        if f["workflow"] == workflow and f["opcion"] == opcion and f["franja"] == "todas":
            return f
    return None


def _tasa(fila, campo):
    if not fila or not fila["llamadas"]:
        return None
    return round(100.0 * fila[campo] / fila["llamadas"], 1)


def _item(id_, texto, valor, control=None, objetivo="", cumple=None, orientativo=False):
    if valor is None:
        estado = "sin_datos"
    else:
        estado = "cumple" if cumple else "no_cumple"
    return {"id": id_, "texto": texto, "estado": estado, "valor": valor, "control": control, "objetivo": objetivo,
            "orientativo": orientativo}


def _manual(id_, texto):
    return {"id": id_, "texto": texto, "estado": "manual", "valor": None, "control": None, "objetivo": "",
            "orientativo": False}


def _comparar(prefijo, nuevo, control, prohibidas):
    """Items comunes a las puertas 1 y 2: el bot único frente al bot actual de la misma opción."""
    items = []

    def par(campo):
        return (nuevo or {}).get(campo), (control or {}).get(campo)

    v, c = par("pct_transferidas")
    items.append(_item(prefijo + "_transferidas", "% de transferencias ≤ control + 2 puntos", v if c is not None else None,
                       c, "≤ control + 2", v is not None and c is not None and v <= c + MARGEN_TRANSFERIDAS, True))
    v, c = par("pct_llegan_agente")
    items.append(_item(prefijo + "_llegan_agente", "% que llega a un agente ≥ control", v if c is not None else None, c,
                       "≥ control", v is not None and c is not None and v >= c, True))
    n = prohibidas.get("atencion", {"gestion_cerrada": 0, "menus": 0})
    total = n["gestion_cerrada"] + n["menus"]
    items.append(_item(prefijo + "_prohibidas", "0 transferencias ejecutadas a Gestión cerrada y 0 a 2114, 2115 o 2119",
                       total if nuevo else None, None, "0", total == 0))
    v, c = _tasa(nuevo, "rellamadas_48h"), _tasa(control, "rellamadas_48h")
    items.append(_item(prefijo + "_rellamadas", "Rellamadas en 48 h no peores (% de llamadas)", v if c is not None else None,
                       c, "≤ control", v is not None and c is not None and v <= c, True))
    v, c = _tasa(nuevo, "cortes_600"), _tasa(control, "cortes_600")
    items.append(_item(prefijo + "_cortes", "Cortes a 600 s no peores (% de llamadas)", v if c is not None else None, c,
                       "≤ control", v is not None and c is not None and v <= c, True))
    v = (nuevo or {}).get("pct_3_saltos")
    items.append(_item(prefijo + "_saltos", "≤ 2 % de llamadas con 3 o más saltos", v, None, "≤ 2 %",
                       v is not None and v <= MAX_PCT_3_SALTOS, True))
    return items


def puertas(filas, prohibidas, fase, filas_pruebas=None):
    """Estado de las puertas de §8.4 con las cifras del día: cumple | no_cumple | sin_datos | manual.
    En la fase 0, `filas_pruebas` (las llamadas de prueba del bot único) alimentan créditos y medición."""
    if fase == 0:
        prol = _fila(filas_pruebas or filas, "atencion", "prolongacion")
        creditos = (prol or {}).get("creditos_llamada")
        hay_bot = any(f["workflow"] == "atencion" for f in list(filas) + list(filas_pruebas or []))
        return [
            _manual("p0_evals", "Evals: críticas 3 de 3 y resto ≥ 90 %"),
            _manual("p0_voz", "25 llamadas de prueba por voz con guion, sin fallos críticos"),
            _manual("p0_correo", "Caso «coincide» del correo probado con una reserva real"),
            _item("p0_creditos", "Créditos por llamada de prolongación en las pruebas ≤ 80", creditos, None, "≤ 80",
                  creditos is not None and creditos <= LIMITE_CREDITOS_PROLONGACION),
            _item("p0_medicion", "Medición, rutina y artefacto funcionando con los runs de prueba",
                  1 if hay_bot else None, None, "runs del bot medidos", hay_bot),
            _manual("p0_vuelta_atras", "Movimiento de líneas y vuelta atrás escritos y ensayados"),
        ]
    if fase == 1:
        nuevo, control = _fila(filas, "atencion", "prolongacion"), _fila(filas, "prolongaciones", "prolongacion")
        v, c = (nuevo or {}).get("resolucion_real"), (control or {}).get("resolucion_real")
        items = [_item("p1_resolucion", "Resolución real no peor que la V11 (≥ −2 puntos; objetivo ≥ 50 %)",
                       v if c is not None else None, c, "≥ V11 − 2",
                       v is not None and c is not None and v >= c - MARGEN_RESOLUCION, True)]
        v = (nuevo or {}).get("creditos_llamada")
        items.append(_item("p1_creditos", "Créditos por llamada ≤ 80", v, None, "≤ 80",
                           v is not None and v <= LIMITE_CREDITOS_PROLONGACION, True))
        v, c = (nuevo or {}).get("creditos_resuelta"), (control or {}).get("creditos_resuelta")
        items.append(_item("p1_creditos_resuelta", "Créditos por llamada resuelta ≤ 70 % de los de la V11",
                           v if c is not None else None, c, "≤ 70 % de la V11",
                           v is not None and c is not None and v <= FACTOR_CREDITOS_RESUELTA * c, True))
        items += _comparar("p1", nuevo, control, prohibidas)
        items.append(_manual("p1_auditoria", "Auditoría: fallos del bot no peores que en la V11 y ningún fallo crítico"))
        return items
    nuevo, control = _fila(filas, "atencion", "minibus"), _fila(filas, "minibus", "minibus")
    v, c = (nuevo or {}).get("resolucion_real"), (control or {}).get("resolucion_real")
    minimo = RESOLUCION_MINIBUS if c is None else max(RESOLUCION_MINIBUS, c - MARGEN_RESOLUCION)
    items = [_item("p2_resolucion", "Resolución real ≥ 47 % y no peor que la v25 (≥ −2 puntos)", v, c, "≥ 47 %",
                   v is not None and v >= minimo, True)]
    v = (nuevo or {}).get("creditos_llamada")
    items.append(_item("p2_creditos", "Créditos por llamada ≤ 64", v, None, "≤ 64",
                       v is not None and v <= LIMITE_CREDITOS_MINIBUS, True))
    items += _comparar("p2", nuevo, control, prohibidas)
    items.append(_manual("p2_punto", "Punto de encuentro entregado y WhatsApp enviados no peores que en la v25"))
    return items


def documento(llamadas, avisos, fecha, fin, fase=0, generado=None, contexto=None, pruebas=None):
    """`contexto`: llamadas de los días de alrededor, solo para buscar rellamadas. `pruebas`: llamadas de prueba del
    bot único (normalizadas con --pruebas), que se miden aparte y alimentan la puerta 0."""
    fin_dt = medir._a_fecha(fin) if isinstance(fin, str) else fin
    resultado = medir.indicadores(llamadas, fin_dt, contexto)
    filas = _filas(resultado)
    prohibidas = transferencias_prohibidas(llamadas)
    filas_pruebas = _filas(medir.indicadores(pruebas, fin_dt)) if pruebas else None
    versiones = {}
    for ll in llamadas:
        cuenta = versiones.setdefault(ll["workflow"], {})
        cuenta[ll.get("version") or "?"] = cuenta.get(ll.get("version") or "?", 0) + 1
    doc = {
        "fecha": fecha,
        "generado": generado or datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "fin_resolucion": resultado["fin"],
        "fase": fase,
        "llamadas": len(llamadas),
        "versiones": versiones,
        "avisos": dict(avisos or {}),
        "filas": filas,
        "prohibidas": prohibidas,
        "puertas": puertas(filas, prohibidas, fase, filas_pruebas),
        "muestra": "",
        "resumen": "",
        "alerta": "",
        "incidencias": [],
    }
    if pruebas:
        doc["pruebas"] = {"llamadas": len(pruebas), "filas": filas_pruebas}
    return doc


def main(argv):
    args = list(argv)
    opciones = {}
    for nombre in ("--fecha", "--fin", "--fase", "--contexto", "--pruebas", "-o"):
        if nombre in args:
            i = args.index(nombre)
            opciones[nombre] = args[i + 1]
            del args[i:i + 2]
    if len(args) != 1 or "--fecha" not in opciones or "-o" not in opciones:
        print("Uso: python3 -I informe_diario.py <llamadas.json> --fecha AAAA-MM-DD [--fin ISO] [--fase N] "
              "[--contexto a.json,b.json] [--pruebas llamadas_pruebas.json] -o <informe.json>")
        return 2
    with open(args[0]) as f:
        llamadas = json.load(f)
    ruta_avisos = os.path.splitext(args[0])[0] + ".avisos.json"
    avisos = json.load(open(ruta_avisos)) if os.path.exists(ruta_avisos) else {}
    contexto = []
    for ruta in filter(None, opciones.get("--contexto", "").split(",")):
        if os.path.exists(ruta):
            with open(ruta) as f:
                contexto += json.load(f)
    pruebas = []
    if opciones.get("--pruebas") and os.path.exists(opciones["--pruebas"]):
        with open(opciones["--pruebas"]) as f:
            pruebas = json.load(f)
    fin = opciones.get("--fin") or datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    doc = documento(llamadas, avisos, opciones["--fecha"], fin, int(opciones.get("--fase", "0")), contexto=contexto,
                    pruebas=pruebas)
    with open(opciones["-o"], "w") as f:
        json.dump(doc, f, indent=1, ensure_ascii=False)
    estados = ", ".join("%s=%s" % (p["id"], p["estado"]) for p in doc["puertas"])
    print("%d llamadas, %d filas. Puertas: %s" % (doc["llamadas"], len(doc["filas"]), estados))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
