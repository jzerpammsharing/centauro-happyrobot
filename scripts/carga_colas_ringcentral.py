"""Carga de trabajo por cola y agentes necesarios (Erlang C) a partir del registro de llamadas de RingCentral.

Uso: python3 -I carga_colas_ringcentral.py <dir_csv> [nivel_servicio=0.8] [segundos=30]

Entrada: CSV en <dir_csv> (uno o varios), una línea por registro del call log de una cola, con las columnas
`cola,dia,inicio_utc,tipo_interno,accion,resultado,duracion_s,origen` (origen = bot si viene de la
extensión 19236 de HappyRobot, externo o interno). Sin teléfonos ni nombres.

Reglas:
- Atendida por un agente: resultado Accepted y duración > 5 s (los Accepted de 0-5 s son anuncios de cerrado).
- Colgada en la bienvenida: Missed directa de menos de 40 s (en la 18057 los agentes empiezan a sonar a los
  ~37 s). No cuenta como demanda para el cálculo de agentes.
- Tiempo por llamada (AHT) = conversación media de la muestra del 15/10/2026 + 30 s de trabajo posterior.
- Erlang C por hora, dentro del horario de cada grupo; los agentes de un grupo se reparten entre sus colas.
"""
import csv
import glob
import math
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta

CAMPOS = ['cola', 'dia', 'inicio_utc', 'tipo_interno', 'accion', 'resultado', 'duracion_s', 'origen']
GRUPO = {
    '18057': 'ES atención', '18061': 'ES atención', '18001': 'ES atención', '18006': 'ES atención',
    '18056': 'ES atención', '18059': 'ES atención',
    '18034': 'ES asistencia', '18035': 'ES asistencia', '18076': 'ES asistencia', '18078': 'ES asistencia',
    '18063': 'PT', '18064': 'PT', '18067': 'PT',
    '18069': 'IT', '18071': 'IT', '18073': 'IT', '18074': 'IT', '18024': 'IT', '19042': 'IT',
}
HORARIO = {'ES atención': (8, 22), 'IT': (8, 22), 'PT': (8, 22), 'ES asistencia': (0, 24)}
CONV = {'18057': 178, '18061': 283, '18001': 277, '18006': 277,
        '18034': 603, '18035': 603, '18076': 603, '18078': 603}
CONV_DEF, ACW = 230, 30
MADRID = timedelta(hours=2)  # UTC+2 hasta el 25/10/2026


def aht(cola):
    return CONV.get(cola, CONV_DEF) + ACW


def leer(directorio):
    filas, vistos = [], set()
    for f in sorted(glob.glob(os.path.join(directorio, '*.csv'))):
        for v in csv.reader(open(f)):
            if len(v) != 8 or v[0] == 'cola':
                continue
            r = dict(zip(CAMPOS, v))
            clave = (r['cola'], r['inicio_utc'], r['duracion_s'], r['resultado'])
            if clave in vistos:
                continue
            vistos.add(clave)
            t = datetime.fromisoformat(r['inicio_utc'].replace('Z', '+00:00')) + MADRID
            r['dia'], r['h'] = t.strftime('%Y-%m-%d'), t.hour
            r['dur'] = int(float(r['duracion_s'] or 0))
            r['atendida'] = r['resultado'] == 'Accepted' and r['dur'] > 5
            r['cerrado'] = r['resultado'] == 'Accepted' and not r['atendida']
            r['bienvenida'] = r['resultado'] == 'Missed' and r['dur'] < 40 and r['origen'] != 'bot'
            filas.append(r)
    return filas


def erlang_c(n, a):
    if n <= a:
        return 1.0
    s = term = 1.0
    for k in range(1, n):
        term *= a / k
        s += term
    term *= a / n
    top = term * n / (n - a)
    return top / (s + top)


def agentes(a, aht_s, sl, t):
    if a <= 0:
        return 0
    n = max(1, math.ceil(a))
    while 1 - erlang_c(n, a) * math.exp(-(n - a) * t / aht_s) < sl:
        n += 1
    return n


def por_hora(filas, dia, grupo, sl, t, delta=0):
    """delta: llamadas que se suman (+) o se quitan (−) al día, repartidas como la demanda."""
    demanda = [r for r in filas if r['dia'] == dia and GRUPO.get(r['cola']) == grupo
               and not r['cerrado'] and not r['bienvenida']]
    a0, a1 = HORARIO[grupo]
    horas = defaultdict(list)
    for r in demanda:
        if a0 <= r['h'] < a1:
            horas[r['h']].append(r)
    total = sum(len(v) for v in horas.values())
    out = []
    for h in range(a0, a1):
        v = horas.get(h, [])
        n = max(0.0, len(v) + (delta * len(v) / total if total else 0))
        aht_h = sum(aht(r['cola']) for r in v) / len(v) if v else CONV_DEF + ACW
        a = n * aht_h / 3600
        out.append({'h': h, 'llamadas': n, 'erlang': a, 'agentes': agentes(a, aht_h, sl, t)})
    return out


if __name__ == '__main__':
    d = sys.argv[1]
    sl = float(sys.argv[2]) if len(sys.argv) > 2 else 0.8
    t = float(sys.argv[3]) if len(sys.argv) > 3 else 30
    F = leer(d)
    print(f'{len(F)} registros')
    cuenta = defaultdict(lambda: defaultdict(int))
    for r in F:
        c = cuenta[(r['dia'], r['cola'])]
        c['registros'] += 1
        c['del_bot'] += r['origen'] == 'bot'
        c['atendidas'] += r['atendida']
        c['perdidas'] += r['resultado'] in ('Missed', 'Voicemail')
        c['en_bienvenida'] += r['bienvenida']
    print('\ndía cola registros del_bot atendidas perdidas en_bienvenida')
    for (dia, cola), c in sorted(cuenta.items()):
        print(dia, cola, c['registros'], c['del_bot'], c['atendidas'], c['perdidas'], c['en_bienvenida'])
    print(f'\nAgentes necesarios ({sl:.0%} en {t:.0f} s)')
    for dia in sorted({r['dia'] for r in F}):
        for g in HORARIO:
            ph = por_hora(F, dia, g, sl, t)
            if not any(x['llamadas'] for x in ph):
                continue
            pico = max(ph, key=lambda x: x['agentes'])
            print(f"{dia} {g}: {sum(x['llamadas'] for x in ph):.0f} llamadas, {sum(x['erlang'] for x in ph):.1f} h de "
                  f"trabajo, {sum(x['agentes'] for x in ph)} horas-agente, pico {pico['agentes']} a las {pico['h']} h")
