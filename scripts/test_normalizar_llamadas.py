# scripts/test_normalizar_llamadas.py
# Ejecutar: python3 -I scripts/test_normalizar_llamadas.py
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from normalizar_llamadas import cola_comun, inicio_utc, main, normalizar  # noqa: E402

fallos = 0
total = 0


def comprobar(nombre, obtenido, esperado):
    global fallos, total
    total += 1
    if obtenido != esperado:
        fallos += 1
        print("FALLO %s: obtenido %r, esperado %r" % (nombre, obtenido, esperado))


def registro(run_id="r1", workflow="atencion", **extra):
    base = {"run_id": run_id, "workflow": workflow, "version": "v2", "inicio": "2026-10-16T09:32:42.969Z",
            "from_hash": "abcdef0123", "opcion_menu": "prolongacion", "turnos_cliente": 3, "duracion_s": 120,
            "intentos": [], "paradas": [], "intento_gestion_cerrada": "no", "saltos": 0, "motivo": "prolongar",
            "llego_agente": None, "es_prueba": False}
    base.update(extra)
    return base


def una(reg, **kw):
    llamadas, avisos = normalizar([reg], **kw)
    return llamadas[0] if llamadas else None


# --- cola_comun: gestion_reserva ↔ gestion y extensiones ---
comprobar("gestion_reserva es gestion", cola_comun("gestion_reserva"), "gestion")
comprobar("gestion se queda", cola_comun("gestion"), "gestion")
comprobar("extensión 18057", cola_comun("18057"), "gestion")
comprobar("sip de 18061", cola_comun("sip:18061@hrpbx.buscentauro.com"), "gestion")
comprobar("18035 asistencia", cola_comun("18035"), "asistencia")
comprobar("18006 nueva_reserva", cola_comun("18006"), "nueva_reserva")
comprobar("18059 minibus", cola_comun("18059"), "minibus")
comprobar("2114 menú automático", cola_comun("sip:2114@hrpbx.buscentauro.com"), "menu_automatico")
comprobar("aviso NO DISPONIBLE es gestión", cola_comun("NO DISPONIBLE AHORA: la cola..."), "gestion")
comprobar("vacía", cola_comun(""), "desconocida")
comprobar("rara", cola_comun("sip:9999@x"), "desconocida")

# --- inicio siempre en ISO UTC con Z ---
comprobar("Z con milisegundos", inicio_utc("2026-10-16T09:32:42.969Z"), "2026-10-16T09:32:42Z")
comprobar("con zona +02:00", inicio_utc("2026-10-16T11:32:42+02:00"), "2026-10-16T09:32:42Z")
comprobar("sin zona = UTC", inicio_utc("2026-10-16T09:32:42"), "2026-10-16T09:32:42Z")
comprobar("registro normalizado", una(registro(inicio="2026-10-16T11:00:00+02:00"))["inicio"], "2026-10-16T09:00:00Z")

# --- opcion_menu nunca vacía ---
comprobar("prolongaciones sin opción", una(registro(workflow="prolongaciones", opcion_menu=""))["opcion_menu"],
          "prolongacion")
comprobar("minibus sin opción", una(registro(workflow="minibus", opcion_menu=None))["opcion_menu"], "minibus")
comprobar("atención sin opción = minibus", una(registro(opcion_menu=""))["opcion_menu"], "minibus")
comprobar("atención con opción", una(registro(opcion_menu="prolongacion"))["opcion_menu"], "prolongacion")
comprobar("bot antiguo usa la de su línea aunque diga otra",
          una(registro(workflow="prolongaciones", opcion_menu="minibus"))["opcion_menu"], "prolongacion")

# --- transferencias: intentos reales ---
ll = una(registro(intentos=[{"ext": "sip:18057@hrpbx.buscentauro.com", "ts": "2026-10-16T09:35:00.5Z", "error": ""}]))
comprobar("intento real", ll["transferencias"], [{"cola": "gestion", "ts": "2026-10-16T09:35:00Z", "error": ""}])
comprobar("conectado → llegó al agente", ll["llego_agente"], True)
ll = una(registro(intentos=[{"cola": "gestion_reserva", "ts": "2026-10-16T09:35:00Z", "error": None}]))
comprobar("gestion_reserva se traduce", ll["transferencias"][0]["cola"], "gestion")
comprobar("error None pasa a vacío", ll["transferencias"][0]["error"], "")
ll = una(registro(intentos=[{"ext": "18057", "ts": "2026-10-16T09:35:00Z", "error": "whisper_transfer_no_bridge"}]))
comprobar("fallido → no llegó", ll["llego_agente"], False)
ll = una(registro(intentos=[{"ext": "18057", "ts": "2026-10-16T09:35:00Z", "error": "whisper_transfer_no_bridge"},
                            {"ext": "18057", "ts": "2026-10-16T09:37:00Z", "error": "transfer_result_timeout"}]))
comprobar("salvada por reintento → llegó", ll["llego_agente"], True)
ll = una(registro(intentos=[{"ext": "18057", "ts": "2026-10-16T09:35:00Z", "error": ""}], llego_agente=False))
comprobar("el dato de RingCentral manda", ll["llego_agente"], False)
comprobar("sin transferencias, llego_agente null", una(registro())["llego_agente"], None)

# --- R43: paradas por gestion_cerrada o modo_virtual cuentan como intento con error ---
ll = una(registro(paradas=[{"resultado": "gestion_cerrada", "cola": "gestion", "ts": "2026-10-16T19:10:00Z"}]))
comprobar("parada gestion_cerrada entra", ll["transferencias"],
          [{"cola": "gestion", "ts": "2026-10-16T19:10:00Z", "error": "gestion_cerrada"}])
comprobar("parada → no llegó al agente", ll["llego_agente"], False)
ll = una(registro(paradas=[{"resultado": "modo_virtual", "cola": "minibus", "ts": "2026-10-16T21:10:00Z"}]))
comprobar("parada modo_virtual entra", ll["transferencias"][0]["error"], "modo_virtual")
ll = una(registro(paradas=[{"resultado": "transferir", "cola": "asistencia", "ts": "2026-10-16T09:35:00Z"}]))
comprobar("«transferir» no es parada", ll["transferencias"], [])
ll = una(registro(paradas=[{"resultado": "cola_no_valida", "cola": "x", "ts": "2026-10-16T09:35:00Z"}]))
comprobar("cola_no_valida no es parada de R43", ll["transferencias"], [])
ll = una(registro(intento_gestion_cerrada="si"))
comprobar("solo el extract dice gestion_cerrada", ll["transferencias"],
          [{"cola": "gestion", "ts": "2026-10-16T09:32:42Z", "error": "gestion_cerrada"}])
ll = una(registro(intento_gestion_cerrada="si",
                  paradas=[{"resultado": "gestion_cerrada", "cola": "gestion", "ts": "2026-10-16T19:10:00Z"}]))
comprobar("extract y parada no se duplican", len(ll["transferencias"]), 1)

# --- créditos ---
comprobar("créditos del fichero", una(registro(), creditos={"r1": 61.5})["creditos"], 61.5)
comprobar("sin créditos, null", una(registro(), creditos={})["creditos"], None)
comprobar("sin fichero de créditos, null", una(registro())["creditos"], None)

# --- llamadas reales: pruebas y sin cliente ---
llamadas, avisos = normalizar([registro("a"), registro("b", es_prueba=True), registro("c", turnos_cliente=0)])
comprobar("sin pruebas ni llamadas sin cliente", [x["run_id"] for x in llamadas], ["a"])
comprobar("aviso pruebas", avisos["pruebas_excluidas"], 1)
comprobar("aviso sin cliente", avisos["sin_turno_cliente"], 1)
llamadas, avisos = normalizar([registro("a"), registro("b", es_prueba=True)], incluir_pruebas=True)
comprobar("con --pruebas entran", [x["run_id"] for x in llamadas], ["a", "b"])

# --- avisos para el informe ---
regs = [registro("a"), registro("b", intentos=[{"ext": "18057", "ts": "2026-10-16T09:35:00Z", "error": "raro"}]),
        registro("c", workflow="minibus", opcion_menu=""), registro("d", opcion_menu="")]
llamadas, avisos = normalizar(regs, creditos={"a": 10})
comprobar("aviso sin créditos", avisos["sin_creditos"], 3)
comprobar("aviso transferidas sin llego_agente", avisos["transferidas_sin_llego_agente"], 1)
comprobar("aviso opción por defecto solo en el bot único", avisos["opcion_por_defecto"], 1)
comprobar("error desconocido → llego_agente null", llamadas[1]["llego_agente"], None)

# --- campos de salida (interfaz de medir_bots.py) ---
claves = {"run_id", "workflow", "version", "inicio", "from_hash", "opcion_menu", "turnos_cliente", "transferencias",
          "llego_agente", "creditos", "saltos", "duracion_s", "motivo"}
comprobar("claves de medir_bots", claves - set(una(registro()).keys()), set())
comprobar("from_hash None pasa a vacío", una(registro(from_hash=None))["from_hash"], "")
comprobar("from_hash largo se recorta a 10", una(registro(from_hash="0123456789abcdef"))["from_hash"], "0123456789")

# --- main ---
with tempfile.TemporaryDirectory() as d:
    entrada, cred, salida = (os.path.join(d, n) for n in ("registros.json", "creditos.json", "llamadas.json"))
    json.dump([registro("a"), registro("b", es_prueba=True)], open(entrada, "w"))
    json.dump({"a": 5}, open(cred, "w"))
    rc = main([entrada, "--creditos", cred, "-o", salida])
    comprobar("main sale con 0", rc, 0)
    datos = json.load(open(salida))
    comprobar("main escribe las llamadas", [(x["run_id"], x["creditos"]) for x in datos], [("a", 5)])
    comprobar("main escribe los avisos", json.load(open(salida.replace(".json", ".avisos.json")))["pruebas_excluidas"], 1)
    comprobar("main sin argumentos", main([]), 2)
    open(cred, "w").close()  # creditos_runs.py sin clave deja el fichero vacío
    comprobar("créditos vacío no rompe", main([entrada, "--creditos", cred, "-o", salida]), 0)
    comprobar("créditos vacío → null", json.load(open(salida))[0]["creditos"], None)

print("%d/%d casos correctos" % (total - fallos, total))
sys.exit(1 if fallos else 0)
