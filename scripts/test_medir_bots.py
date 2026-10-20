# scripts/test_medir_bots.py
# Ejecutar: python3 -I scripts/test_medir_bots.py
import io
import json
import os
import sys
import tempfile
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medir_bots import franja, indicadores, main, rellamadas, resuelta  # noqa: E402

UTC = timezone.utc
BASE = datetime(2026, 10, 5, 10, 0, tzinfo=UTC)  # lunes
FIN = datetime(2026, 10, 20, 0, 0, tzinfo=UTC)

fallos = 0
total = 0


def comprobar(nombre, obtenido, esperado):
    global fallos, total
    total += 1
    if obtenido != esperado:
        fallos += 1
        print("FALLO %s: obtenido %r, esperado %r" % (nombre, obtenido, esperado))


def llamada(run_id, inicio=BASE, hash_="h000000001", workflow="atencion", opcion="prolongacion", turnos=3,
            transferencias=None, llego=None, creditos=50, saltos=1, duracion=120):
    return {
        "run_id": run_id, "workflow": workflow, "version": "v1", "inicio": inicio.isoformat().replace("+00:00", "Z"),
        "from_hash": hash_, "opcion_menu": opcion, "turnos_cliente": turnos,
        "transferencias": transferencias or [], "llego_agente": llego, "creditos": creditos, "saltos": saltos,
        "duracion_s": duracion, "motivo": "otro",
    }


FALLIDA = [{"cola": "gestion", "ts": "2026-10-05T10:01:00Z", "error": "whisper_transfer_no_bridge"}]

# --- franja (martes 20/10/2026; en octubre Madrid es UTC+2 hasta el 25) ---
comprobar("franja martes 21:30 Madrid", franja(datetime(2026, 10, 20, 19, 30, tzinfo=UTC)), "gestion_cerrada")
comprobar("franja martes 22:30 Madrid", franja(datetime(2026, 10, 20, 20, 30, tzinfo=UTC)), "modo_virtual")
comprobar("franja martes 10:00 Madrid", franja(datetime(2026, 10, 20, 8, 0, tzinfo=UTC)), "gestion_abierta")
comprobar("franja 8/12/2026 10:00 (festivo)", franja(datetime(2026, 12, 8, 9, 0, tzinfo=UTC)), "gestion_cerrada")
comprobar("franja sábado 10:00", franja(datetime(2026, 10, 17, 8, 0, tzinfo=UTC)), "gestion_cerrada")
comprobar("franja con hora sin zona", franja(datetime(2026, 10, 20, 8, 0)), "gestion_abierta")

# --- rellamadas ---
a = llamada("run-a")
comprobar("rellamada a las 47 h", rellamadas([a, llamada("run-b", BASE + timedelta(hours=47))]), {"run-a"})
comprobar("rellamada a las 49 h", rellamadas([a, llamada("run-b", BASE + timedelta(hours=49))]), set())
comprobar("rellamada en otro workflow",
          rellamadas([a, llamada("run-b", BASE + timedelta(hours=2), workflow="minibus")]), {"run-a"})
comprobar("otro número no es rellamada", rellamadas([a, llamada("run-b", BASE + timedelta(hours=2), hash_="h000000002")]), set())
comprobar("from_hash vacío nunca es rellamada",
          rellamadas([llamada("run-a", hash_=""), llamada("run-b", BASE + timedelta(hours=1), hash_="")]), set())
comprobar("la última llamada no es rellamada de la primera",
          rellamadas([a, llamada("run-b", BASE + timedelta(hours=1))]), {"run-a"})

# --- resuelta ---
comprobar("resuelta simple", resuelta(a, set()), True)
comprobar("transferencia fallida no resuelta", resuelta(llamada("r", transferencias=FALLIDA), set()), False)
comprobar("1 turno no resuelta", resuelta(llamada("r", turnos=1), set()), False)
comprobar("2 turnos resuelta", resuelta(llamada("r", turnos=2), set()), True)
comprobar("con rellamada no resuelta", resuelta(a, {"run-a"}), False)

# --- indicadores ---
reciente = FIN - timedelta(hours=10)
ls = [
    llamada("r1", creditos=40, duracion=100, saltos=1),
    llamada("r2", BASE + timedelta(days=1), hash_="h000000002", creditos=60, duracion=700, saltos=3),
    llamada("r3", BASE + timedelta(days=2), hash_="h000000003", transferencias=FALLIDA, llego=False, creditos=30),
    llamada("r4", BASE + timedelta(days=3), hash_="h000000004", transferencias=[{"cola": "g", "ts": "x", "error": ""}],
            llego=True, creditos=30),
    llamada("rec", reciente, hash_="h000000009", creditos=999, duracion=800),
]
ind = indicadores(ls, FIN)["por_opcion"]["atencion/prolongacion"]
comprobar("llamadas incluye recientes", ind["llamadas"], 5)
# elegibles: r1..r4 (la reciente queda fuera); resueltas: r1 y r2
comprobar("resolucion_real sin recientes", ind["resolucion_real"], 50.0)
comprobar("pct_transferidas", ind["pct_transferidas"], 40.0)
comprobar("pct_llegan_agente", ind["pct_llegan_agente"], 50.0)
comprobar("creditos_llamada", ind["creditos_llamada"], round((40 + 60 + 30 + 30 + 999) / 5, 1))
comprobar("creditos_resuelta", ind["creditos_resuelta"], (40 + 60 + 30 + 30) / 2)
comprobar("cortes_600", ind["cortes_600"], 2)
comprobar("pct_3_saltos", ind["pct_3_saltos"], 20.0)
comprobar("rellamadas_48h", ind["rellamadas_48h"], 0)

sin_dato = ls[:4] + [llamada("rx", BASE + timedelta(days=4), hash_="h000000005", creditos=None)]
ind2 = indicadores(sin_dato, FIN)["por_opcion"]["atencion/prolongacion"]
comprobar("creditos_resuelta null si falta un dato", ind2["creditos_resuelta"], None)
comprobar("creditos_llamada null si falta un dato", ind2["creditos_llamada"], None)

solo_recientes = indicadores([llamada("rec", reciente)], FIN)["por_opcion"]["atencion/prolongacion"]
comprobar("sin llamadas elegibles resolución null", solo_recientes["resolucion_real"], None)
comprobar("sin resueltas creditos_resuelta null", solo_recientes["creditos_resuelta"], None)

# Rellamada en el grupo y por franja
dos = [llamada("p1"), llamada("p2", BASE + timedelta(hours=3), opcion="minibus", workflow="minibus")]
res = indicadores(dos, FIN)
comprobar("rellamadas_48h cuenta la primera", res["por_opcion"]["atencion/prolongacion"]["rellamadas_48h"], 1)
comprobar("rellamada no resuelta", res["por_opcion"]["atencion/prolongacion"]["resolucion_real"], 0.0)
comprobar("grupos por opción", sorted(res["por_opcion"]), ["atencion/prolongacion", "minibus/minibus"])
comprobar("franja de lunes 10:00 UTC (12:00 Madrid)", sorted(res["por_franja"]), ["gestion_abierta"])
comprobar("por opción y franja", sorted(res["por_opcion_franja"]),
          ["atencion/prolongacion/gestion_abierta", "minibus/minibus/gestion_abierta"])

# La rellamada se busca en todas las llamadas, no solo en el grupo
comprobar("rellamada entre grupos cuenta en la fuente", resuelta(dos[0], rellamadas(dos)), False)

# Rellamadas con llamadas de otros días (contexto) que no se miden
dia = [llamada("d1", BASE)]
despues = [llamada("d2", BASE + timedelta(hours=20))]
res = indicadores(dia, FIN, contexto=despues)["por_opcion"]["atencion/prolongacion"]
comprobar("contexto: la rellamada del día siguiente cuenta", res["rellamadas_48h"], 1)
comprobar("contexto: no se mide", res["llamadas"], 1)
comprobar("contexto: la llamada ya no es resuelta", res["resolucion_real"], 0.0)

# --contexto con varios ficheros separados por comas
with tempfile.TemporaryDirectory() as d:
    rutas = [os.path.join(d, n) for n in ("dia.json", "antes.json", "despues.json")]
    json.dump([llamada("d1", BASE)], open(rutas[0], "w"))
    json.dump([llamada("d0", BASE - timedelta(hours=30), hash_="h000000009")], open(rutas[1], "w"))
    json.dump([llamada("d2", BASE + timedelta(hours=20))], open(rutas[2], "w"))
    with redirect_stdout(io.StringIO()):
        rc = main([rutas[0], "--fin", "2026-10-20T00:00:00Z", "--contexto", rutas[1] + "," + rutas[2]])
    res = json.load(open(os.path.join(d, "dia.indicadores.json")))["por_opcion"]["atencion/prolongacion"]
    comprobar("--contexto con varios ficheros: sale con 0", rc, 0)
    comprobar("--contexto con varios ficheros: rellamada del segundo", res["rellamadas_48h"], 1)
    comprobar("--contexto con varios ficheros: solo mide el día", res["llamadas"], 1)

# Margen de 48 h: la rutina corre a las 07:30 de Madrid (05:30 UTC). El día D-2 solo tiene margen hasta las 07:30
# (D-2 00:00-07:30 UTC), el día D-3 lo tiene entero: la rutina rehace D-3, no D-2.
AHORA = datetime(2026, 10, 20, 5, 30, tzinfo=UTC)
dia_d2 = [llamada("a%d" % h, datetime(2026, 10, 18, h, 0, tzinfo=UTC), hash_="h0000000%02d" % h) for h in (3, 10, 20)]
dia_d3 = [llamada("b%d" % h, datetime(2026, 10, 17, h, 0, tzinfo=UTC), hash_="h0000001%02d" % h) for h in (3, 10, 20)]
g2 = indicadores(dia_d2, AHORA)["por_opcion"]["atencion/prolongacion"]
g3 = indicadores(dia_d3, AHORA)["por_opcion"]["atencion/prolongacion"]
comprobar("margen: D-2 solo tiene margen para una parte", (g2["llamadas"], g2["con_margen"]), (3, 1))
comprobar("margen: D-3 tiene margen para todo el día", (g3["llamadas"], g3["con_margen"]), (3, 3))

print("%d/%d casos correctos" % (total - fallos, total))
sys.exit(1 if fallos else 0)
