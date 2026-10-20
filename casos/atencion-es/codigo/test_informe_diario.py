# casos/atencion-es/codigo/test_informe_diario.py
# Ejecutar: python3 -I casos/atencion-es/codigo/test_informe_diario.py
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from informe_diario import documento, main, puertas, transferencias_prohibidas  # noqa: E402

fallos = 0
total = 0


def comprobar(nombre, obtenido, esperado):
    global fallos, total
    total += 1
    if obtenido != esperado:
        fallos += 1
        print("FALLO %s: obtenido %r, esperado %r" % (nombre, obtenido, esperado))


def llamada(run_id, workflow="atencion", opcion="prolongacion", inicio="2026-10-06T08:00:00Z", transferencias=None,
            creditos=60, turnos=3, hash_=None, version="v2"):
    return {"run_id": run_id, "workflow": workflow, "version": version, "inicio": inicio,
            "from_hash": hash_ if hash_ is not None else run_id[:10], "opcion_menu": opcion, "turnos_cliente": turnos,
            "transferencias": transferencias or [], "llego_agente": True if transferencias else None,
            "creditos": creditos, "saltos": 0, "duracion_s": 100, "motivo": ""}


FIN = "2026-10-20T08:00:00Z"
T_GESTION = [{"cola": "gestion", "ts": "2026-10-06T08:01:00Z", "error": ""}]

# --- transferencias prohibidas: a Gestión cerrada o a un menú automático ---
sabado = "2026-10-10T08:01:00Z"  # sábado 10:01 en Madrid: Gestión cerrada
ll = [llamada("a", transferencias=[{"cola": "gestion", "ts": sabado, "error": ""}]),
      llamada("b", transferencias=[{"cola": "gestion", "ts": sabado, "error": "gestion_cerrada"}]),
      llamada("c", transferencias=[{"cola": "menu_automatico", "ts": "2026-10-06T08:01:00Z", "error": "x"}]),
      llamada("d", transferencias=T_GESTION),
      llamada("e", workflow="prolongaciones", transferencias=[{"cola": "gestion", "ts": sabado, "error": ""}])]
r = transferencias_prohibidas(ll)
comprobar("ejecutada a Gestión cerrada", r["atencion"]["gestion_cerrada"], 1)
comprobar("parada por R43 no cuenta", r["atencion"]["gestion_cerrada_paradas"], 1)
comprobar("menú automático", r["atencion"]["menus"], 1)
comprobar("por workflow", r["prolongaciones"]["gestion_cerrada"], 1)

# --- documento ---
ll = [llamada("p1"), llamada("p2", transferencias=T_GESTION),
      llamada("v1", workflow="prolongaciones", version="V11"),
      llamada("v2", workflow="prolongaciones", version="V11", transferencias=T_GESTION),
      llamada("m1", workflow="minibus", opcion="minibus", version="v25")]
avisos = {"sin_creditos": 0, "transferidas_sin_llego_agente": 0, "opcion_por_defecto": 0, "pruebas_excluidas": 2}
doc = documento(ll, avisos, fecha="2026-10-06", fin=FIN, fase=0, generado="2026-10-20T08:00:00Z")
comprobar("fecha", doc["fecha"], "2026-10-06")
comprobar("fase", doc["fase"], 0)
comprobar("avisos copiados", doc["avisos"]["pruebas_excluidas"], 2)
comprobar("versiones por workflow", doc["versiones"], {"atencion": {"v2": 2}, "minibus": {"v25": 1},
                                                    "prolongaciones": {"V11": 2}})
filas = {(f["workflow"], f["opcion"], f["franja"]): f for f in doc["filas"]}
comprobar("fila total por opción", filas[("atencion", "prolongacion", "todas")]["llamadas"], 2)
comprobar("fila por franja", filas[("atencion", "prolongacion", "gestion_abierta")]["llamadas"], 2)
comprobar("resolución en la fila", filas[("prolongaciones", "prolongacion", "todas")]["resolucion_real"], 50.0)
comprobar("fila de minibús", ("minibus", "minibus", "todas") in filas, True)
comprobar("llamadas totales", doc["llamadas"], 5)
comprobar("campos de texto para la rutina", (doc["resumen"], doc["alerta"], doc["incidencias"]), ("", "", []))

# --- puertas ---
p = {x["id"]: x for x in puertas(doc["filas"], doc["prohibidas"], fase=0)}
comprobar("puerta 0: créditos de prolongación ≤ 80", p["p0_creditos"]["estado"], "cumple")
comprobar("puerta 0: valor", p["p0_creditos"]["valor"], 60.0)
comprobar("puerta 0: medición con runs del bot", p["p0_medicion"]["estado"], "cumple")
comprobar("puerta 0: evals a mano", p["p0_evals"]["estado"], "manual")

caras = [llamada("x%d" % i, creditos=95) for i in range(3)]
d2 = documento(caras, avisos, fecha="2026-10-06", fin=FIN, fase=0, generado="x")
comprobar("créditos > 80 no cumple", {x["id"]: x for x in d2["puertas"]}["p0_creditos"]["estado"], "no_cumple")
d3 = documento([llamada("y", creditos=None)], avisos, fecha="2026-10-06", fin=FIN, fase=0, generado="x")
comprobar("sin créditos: sin datos", {x["id"]: x for x in d3["puertas"]}["p0_creditos"]["estado"], "sin_datos")
d4 = documento([llamada("v", workflow="prolongaciones")], avisos, fecha="2026-10-06", fin=FIN, fase=0, generado="x")
comprobar("sin runs del bot: medición pendiente", {x["id"]: x for x in d4["puertas"]}["p0_medicion"]["estado"],
          "sin_datos")

# Fix 2: la puerta 0 se mide con las llamadas de prueba del bot único (§8.4)
pruebas = [llamada("t%d" % i, creditos=70) for i in range(2)] + [llamada("tm", opcion="minibus", creditos=40)]
d8 = documento([llamada("v", workflow="prolongaciones")], avisos, fecha="2026-10-06", fin=FIN, fase=0,
               generado="x", pruebas=pruebas)
p = {x["id"]: x for x in d8["puertas"]}
comprobar("pruebas: créditos de prolongación de las pruebas", (p["p0_creditos"]["estado"], p["p0_creditos"]["valor"]),
          ("cumple", 70.0))
comprobar("pruebas: medición con runs de prueba", p["p0_medicion"]["estado"], "cumple")
comprobar("pruebas: resumen en el documento", d8["pruebas"]["llamadas"], 3)
comprobar("pruebas: no se mezclan con las reales", d8["llamadas"], 1)
caras_p = [llamada("tc", creditos=95)]
d9 = documento([], avisos, fecha="2026-10-06", fin=FIN, fase=0, generado="x", pruebas=caras_p)
comprobar("pruebas caras: no cumple", {x["id"]: x for x in d9["puertas"]}["p0_creditos"]["estado"], "no_cumple")
comprobar("sin pruebas: campo vacío", d2.get("pruebas"), None)

# Puerta 1: el bot único frente a la V11 en la opción de prolongación
nuevo = [llamada("n%d" % i, creditos=60) for i in range(4)]  # 4 resueltas
v11 = [llamada("o%d" % i, workflow="prolongaciones", version="V11", creditos=118,
               transferencias=T_GESTION if i < 2 else None) for i in range(4)]  # 2 de 4 resueltas
d5 = documento(nuevo + v11, avisos, fecha="2026-10-06", fin=FIN, fase=1, generado="x")
p = {x["id"]: x for x in d5["puertas"]}
comprobar("puerta 1: resolución no peor", p["p1_resolucion"]["estado"], "cumple")
comprobar("puerta 1: valor y control", (p["p1_resolucion"]["valor"], p["p1_resolucion"]["control"]), (100.0, 50.0))
comprobar("puerta 1: créditos por llamada ≤ 80", p["p1_creditos"]["estado"], "cumple")
comprobar("puerta 1: créditos por resuelta ≤ 70 % de la V11", p["p1_creditos_resuelta"]["estado"], "cumple")
comprobar("puerta 1: 0 transferencias prohibidas", p["p1_prohibidas"]["estado"], "cumple")
comprobar("puerta 1: saltos", p["p1_saltos"]["estado"], "cumple")
comprobar("puerta 1 es orientativa a diario", p["p1_resolucion"]["orientativo"], True)
comprobar("fase 1 no evalúa la puerta 0", "p0_creditos" in p, False)

peor = [llamada("n%d" % i, transferencias=T_GESTION) for i in range(4)]
d6 = documento(peor + v11, avisos, fecha="2026-10-06", fin=FIN, fase=1, generado="x")
p = {x["id"]: x for x in d6["puertas"]}
comprobar("puerta 1: resolución peor", p["p1_resolucion"]["estado"], "no_cumple")
comprobar("puerta 1: más transferencias", p["p1_transferidas"]["estado"], "no_cumple")

d7 = documento(nuevo, avisos, fecha="2026-10-06", fin=FIN, fase=1, generado="x")
comprobar("sin control: sin datos", {x["id"]: x for x in d7["puertas"]}["p1_resolucion"]["estado"], "sin_datos")

# Puerta 2: minibús frente a Minibús ES
mb = [llamada("q%d" % i, opcion="minibus", creditos=50) for i in range(2)]
mbv = [llamada("r%d" % i, workflow="minibus", opcion="minibus", version="v25", creditos=64) for i in range(2)]
p = {x["id"]: x for x in documento(mb + mbv, avisos, fecha="2026-10-06", fin=FIN, fase=2, generado="x")["puertas"]}
comprobar("puerta 2: créditos ≤ 64", p["p2_creditos"]["estado"], "cumple")
comprobar("puerta 2: resolución ≥ 47", p["p2_resolucion"]["estado"], "cumple")

# --- main ---
with tempfile.TemporaryDirectory() as d:
    ruta = os.path.join(d, "llamadas.json")
    json.dump(ll, open(ruta, "w"))
    json.dump(avisos, open(os.path.join(d, "llamadas.avisos.json"), "w"))
    salida = os.path.join(d, "informe.json")
    rc = main([ruta, "--fecha", "2026-10-06", "--fin", FIN, "--fase", "0", "-o", salida])
    comprobar("main sale con 0", rc, 0)
    comprobar("main escribe el documento", json.load(open(salida))["llamadas"], 5)
    comprobar("main sin argumentos", main([]), 2)
    otro = os.path.join(d, "dia_siguiente.json")
    json.dump([llamada("v1b", workflow="prolongaciones", inicio="2026-10-07T08:00:00Z", hash_="v1")], open(otro, "w"))
    main([ruta, "--fecha", "2026-10-06", "--fin", FIN, "--contexto", otro, "-o", salida])
    filas = {(f["workflow"], f["franja"]): f for f in json.load(open(salida))["filas"]}
    comprobar("contexto: rellamada del día siguiente", filas[("prolongaciones", "todas")]["rellamadas_48h"], 1)
    comprobar("contexto: no se mide", filas[("prolongaciones", "todas")]["llamadas"], 2)
    ruta_pruebas = os.path.join(d, "llamadas_pruebas.json")
    json.dump([llamada("tp", creditos=50)], open(ruta_pruebas, "w"))
    main([ruta, "--fecha", "2026-10-06", "--fin", FIN, "--pruebas", ruta_pruebas, "-o", salida])
    p = {x["id"]: x for x in json.load(open(salida))["puertas"]}
    comprobar("main --pruebas: créditos de la prueba", p["p0_creditos"]["valor"], 50.0)

print("%d/%d casos correctos" % (total - fallos, total))
sys.exit(1 if fallos else 0)
