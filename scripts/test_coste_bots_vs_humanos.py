# scripts/test_coste_bots_vs_humanos.py
# Ejecutar: python3 -I scripts/test_coste_bots_vs_humanos.py
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from coste_bots_vs_humanos import (ACW_S, a_madrid, agentes, calcular, cobertura, eur_minuto_persona,  # noqa: E402
                                   seg_bot, seg_persona)

fallos = 0
total = 0


def comprobar(nombre, obtenido, esperado):
    global fallos, total
    total += 1
    if obtenido != esperado:
        fallos += 1
        print("FALLO %s: obtenido %r, esperado %r" % (nombre, obtenido, esperado))


def llamada(created, duracion=120, transferida=False, seg=None, aprox=None):
    return {'created': created, 'duration_s': duracion, 'transferida': transferida, 'seg_bot': seg,
            'seg_bot_aprox': aprox}


# Hora de Madrid: UTC+2 hasta el cambio del 25/10 a las 01:00 UTC, UTC+1 después
comprobar("madrid verano", a_madrid("2026-10-24T22:30:00Z").hour, 0)
comprobar("madrid invierno", a_madrid("2026-10-25T23:30:00Z").hour, 0)

# Segundos del bot: exacto, si no el estimado, si no toda la llamada
comprobar("seg_bot exacto", seg_bot(llamada("2026-10-20T10:00:00Z", seg=40, aprox=30)), 40)
comprobar("seg_bot aprox", seg_bot(llamada("2026-10-20T10:00:00Z", transferida=True, aprox=30)), 30)
comprobar("seg_bot sin dato", seg_bot(llamada("2026-10-20T10:00:00Z", duracion=90)), 90)

# Una persona: la misma conversación más el trabajo posterior, salvo cuelgues y transferidas
comprobar("persona resuelta", seg_persona(llamada("2026-10-20T10:00:00Z", duracion=100)), 100 + ACW_S)
comprobar("persona cuelgue", seg_persona(llamada("2026-10-20T10:00:00Z", duracion=10)), 10)
comprobar("persona transferida", seg_persona(llamada("2026-10-20T10:00:00Z", 300, True, aprox=60)), 60)

# Coste del minuto atendido: entre 0,30 y 0,40 € con el salario mínimo
comprobar("euro minuto", 0.30 < eur_minuto_persona() < 0.40, True)

# Erlang C: al menos 1 agente en cada hora; con más carga, más agentes
comprobar("agentes sin carga", agentes(0, 180), 1)
comprobar("agentes poca carga", agentes(0.05, 180), 1)
comprobar("agentes crecen", agentes(5, 180) > agentes(1, 180), True)

# Cobertura de un día sin apenas llamadas: 24 h de agente al día = 168 h a la semana
un_dia = [llamada("2026-10-20T10:00:00Z")]
comprobar("cobertura mínima", cobertura(un_dia, 1), 168)
# Solo con Gestión cerrada: menos horas que la cobertura completa
comprobar("cobertura cerrada", cobertura(un_dia, 1, solo_cerrada=True) < 168, True)

# Cálculo completo con dos bots: suma las llamadas y no cuenta las de prueba
bots = {'minibus_es': [llamada("2026-10-20T10:00:00Z"), llamada("2026-10-21T10:00:00Z", 200, True, aprox=50)],
        'atencion_es': [llamada("2026-10-21T12:00:00Z")]}
r = calcular(bots)
comprobar("total llamadas", r['total']['llamadas'], 3)
comprobar("días", r['dias'], 2)
comprobar("transferidas", r['total']['transferidas'], 1)

print("%d/%d pruebas correctas" % (total - fallos, total))
sys.exit(1 if fallos else 0)
