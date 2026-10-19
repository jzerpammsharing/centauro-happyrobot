"""Normaliza los registros por run de la rutina diaria al formato de llamadas.json de medir_bots.py.

Uso: python3 -I scripts/normalizar_llamadas.py <registros.json> [--creditos creditos.json] [--pruebas] -o <llamadas.json>
- registros.json: lista de registros por run (los escriben los subagentes de la rutina; ver
  casos/atencion-es/rutinas/informe-atencion-es.md): "run_id", "workflow" (atencion | prolongaciones | minibus),
  "version", "inicio", "from_hash", "opcion_menu", "turnos_cliente", "duracion_s", "es_prueba",
  "intentos": [{"ext" o "cola", "ts", "error"}] (outputs de «Initiate customer connection»),
  "paradas": [{"resultado", "cola", "ts"}] (resultado de «Preparar transferencia», solo el bot único),
  "intento_gestion_cerrada" ("si" | "no", del extract), "saltos", "motivo" y "llego_agente" (bool o null).
- creditos.json: {run_id: créditos o null} de creditos_runs.py. Si falta, `creditos` = null.
- --pruebas: deja las llamadas de prueba (web o «prueba» en el resumen); sin él se quitan.
- Escribe <llamadas.json> y, al lado, <llamadas>.avisos.json con lo que falta (para el aviso del informe).

Reglas (Tarea 15, R43):
- `inicio` siempre en ISO UTC con Z, sin milisegundos.
- `opcion_menu` nunca vacía: en los bots antiguos, la de su línea (prolongaciones → prolongacion, minibus → minibus);
  en el bot único, si viene vacía, minibus (línea desconocida, Tarea 1).
- Colas con un solo nombre: `gestion_reserva` (bots antiguos) = `gestion` (bot único); las extensiones se traducen.
- Un intento parado por «Preparar transferencia» con `gestion_cerrada` o `modo_virtual` (o, si no hay dato del nodo,
  `intento_gestion_cerrada` = si del extract) entra en `transferencias` con `error` igual a ese resultado: así la
  llamada no cuenta como resuelta.
- `llego_agente`: el dato de RingCentral si lo hay; si no, true si algún intento conectó (error vacío o
  `transfer_result_timeout`), false si todos fallaron por una causa conocida, null en otro caso.
- Solo llamadas reales: fuera las de prueba (salvo --pruebas) y las que no tienen ningún turno del cliente.
"""
import json
import os
import re
import sys
from datetime import datetime, timezone

UTC = timezone.utc
OPCION_DE_LINEA = {"prolongaciones": "prolongacion", "minibus": "minibus"}
OPCION_POR_DEFECTO_ATENCION = "minibus"
EXTENSIONES = {
    "18057": "gestion", "18061": "gestion",
    "18034": "asistencia", "18035": "asistencia",
    "18001": "nueva_reserva", "18006": "nueva_reserva",
    "18056": "minibus", "18059": "minibus",
    "2114": "menu_automatico", "2115": "menu_automatico", "2119": "menu_automatico",
}
NOMBRES = {"gestion_reserva": "gestion", "gestion": "gestion", "asistencia": "asistencia",
           "nueva_reserva": "nueva_reserva", "minibus": "minibus"}
PARADAS_R43 = ("gestion_cerrada", "modo_virtual")
CONECTADO = ("", "transfer_result_timeout")
FALLOS_CONOCIDOS = ("whisper_transfer_no_bridge", "whisper_transfer_timeout", "disconnected before rep",
                    "invalid phone number", "no disponible") + PARADAS_R43


def cola_comun(valor):
    """Nombre común de la cola a partir de un nombre (gestion_reserva ↔ gestion) o de una extensión."""
    texto = (valor or "").strip()
    if not texto:
        return "desconocida"
    if texto.lower() in NOMBRES:
        return NOMBRES[texto.lower()]
    if "NO DISPONIBLE" in texto.upper():
        return "gestion"  # aviso de Gestión cerrada copiado como extensión (fallo conocido de los bots antiguos)
    m = re.search(r"(\d{4,5})", texto)
    return EXTENSIONES.get(m.group(1), "desconocida") if m else "desconocida"


def inicio_utc(texto):
    t = datetime.fromisoformat(texto.replace("Z", "+00:00"))
    t = t.replace(tzinfo=UTC) if t.tzinfo is None else t.astimezone(UTC)
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def _llego_agente(transferencias, dato):
    if dato is not None or not transferencias:
        return dato if transferencias else None
    errores = [(t["error"] or "").lower() for t in transferencias]
    if any(e in CONECTADO for e in errores):
        return True
    if all(any(f in e for f in FALLOS_CONOCIDOS) for e in errores):
        return False
    return None


def _transferencias(reg):
    resultado = []
    for i in reg.get("intentos") or []:
        resultado.append({"cola": cola_comun(i.get("cola") or i.get("ext")), "ts": inicio_utc(i["ts"]),
                          "error": i.get("error") or ""})
    paradas = [p for p in reg.get("paradas") or [] if p.get("resultado") in PARADAS_R43]
    for p in paradas:
        resultado.append({"cola": cola_comun(p.get("cola")) if p.get("cola") else "gestion",
                          "ts": inicio_utc(p.get("ts") or reg["inicio"]), "error": p["resultado"]})
    if reg.get("intento_gestion_cerrada") == "si" and not any(p["resultado"] == "gestion_cerrada" for p in paradas):
        resultado.append({"cola": "gestion", "ts": inicio_utc(reg["inicio"]), "error": "gestion_cerrada"})
    resultado.sort(key=lambda t: t["ts"])
    return resultado


def normalizar(registros, creditos=None, incluir_pruebas=False):
    """(llamadas, avisos). llamadas sigue la interfaz de medir_bots.py; avisos cuenta lo que falta o se quitó."""
    creditos = creditos or {}
    avisos = {"registros": len(registros), "pruebas_excluidas": 0, "sin_turno_cliente": 0, "sin_creditos": 0,
              "transferidas_sin_llego_agente": 0, "opcion_por_defecto": 0}  # opcion_por_defecto: solo el bot único
    llamadas = []
    for reg in registros:
        if reg.get("es_prueba") and not incluir_pruebas:
            avisos["pruebas_excluidas"] += 1
            continue
        if not reg.get("turnos_cliente"):
            avisos["sin_turno_cliente"] += 1
            continue
        workflow = reg["workflow"]
        if workflow in OPCION_DE_LINEA:
            opcion = OPCION_DE_LINEA[workflow]
        else:
            opcion = reg.get("opcion_menu") or OPCION_POR_DEFECTO_ATENCION
            if not reg.get("opcion_menu"):
                avisos["opcion_por_defecto"] += 1
        transferencias = _transferencias(reg)
        llamada = {
            "run_id": reg["run_id"], "workflow": workflow, "version": reg.get("version") or "",
            "inicio": inicio_utc(reg["inicio"]), "from_hash": (reg.get("from_hash") or "")[:10],
            "opcion_menu": opcion, "turnos_cliente": reg["turnos_cliente"], "transferencias": transferencias,
            "llego_agente": _llego_agente(transferencias, reg.get("llego_agente")),
            "creditos": creditos.get(reg["run_id"]), "saltos": reg.get("saltos"),
            "duracion_s": reg.get("duracion_s"), "motivo": reg.get("motivo") or "",
        }
        if reg.get("es_prueba"):
            llamada["es_prueba"] = True
        if llamada["creditos"] is None:
            avisos["sin_creditos"] += 1
        if transferencias and llamada["llego_agente"] is None:
            avisos["transferidas_sin_llego_agente"] += 1
        llamadas.append(llamada)
    avisos["llamadas"] = len(llamadas)
    return llamadas, avisos


def main(argv):
    args = list(argv)
    incluir_pruebas = "--pruebas" in args
    if incluir_pruebas:
        args.remove("--pruebas")
    opciones = {}
    for nombre in ("--creditos", "-o"):
        if nombre in args:
            i = args.index(nombre)
            opciones[nombre] = args[i + 1]
            del args[i:i + 2]
    if len(args) != 1 or "-o" not in opciones:
        print("Uso: python3 -I normalizar_llamadas.py <registros.json> [--creditos creditos.json] [--pruebas] "
              "-o <llamadas.json>")
        return 2
    with open(args[0]) as f:
        registros = json.load(f)
    creditos = {}
    if "--creditos" in opciones and os.path.exists(opciones["--creditos"]):
        with open(opciones["--creditos"]) as f:
            texto = f.read().strip()
        creditos = json.loads(texto) if texto else {}  # vacío: creditos_runs.py salió sin clave
    llamadas, avisos = normalizar(registros, creditos, incluir_pruebas)
    salida = opciones["-o"]
    with open(salida, "w") as f:
        json.dump(llamadas, f, indent=1, ensure_ascii=False)
    with open(os.path.splitext(salida)[0] + ".avisos.json", "w") as f:
        json.dump(avisos, f, indent=1, ensure_ascii=False)
    print("%d llamadas en %s. Avisos: %s" % (len(llamadas), salida, json.dumps(avisos, ensure_ascii=False)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
