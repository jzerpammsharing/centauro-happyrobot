"""Empareja los intentos de transferencia de HappyRobot con las patas salientes de RingCentral.

Uso: python3 -I emparejar_ringcentral.py <llamadas.json> <ringcentral.json>
- llamadas.json: lista de runs con "run_id", "pais" y "transfers": [{"ext", "ts" (ISO UTC), "error"}]
- ringcentral.json: lista de patas con "id", "start" (ISO UTC), "duration", "to_ext"
Una pata casa con un intento si va a la misma extensión y empieza a ±15 s.
"""
import json, sys
from datetime import datetime

P = lambda s: datetime.fromisoformat(s.replace('Z', '+00:00'))
D = json.load(open(sys.argv[1]))
R = json.load(open(sys.argv[2]))
usadas, sin_pata = set(), []
for d in D:
    for t in d['transfers']:
        mejor = None
        for r in R:
            if r['id'] in usadas or r['to_ext'] != t['ext']:
                continue
            dt = (P(r['start']) - P(t['ts'])).total_seconds()
            if abs(dt) <= 15 and (mejor is None or abs(dt) < abs(mejor[1])):
                mejor = (r, dt)
        if mejor:
            usadas.add(mejor[0]['id'])
            if t.get('error'):
                print('CON ERROR', d['run_id'], t['ext'], t['error'], f"{mejor[0]['duration']} s")
        else:
            sin_pata.append((d['run_id'], t['ext'], t.get('error'), t['ts']))
for x in sin_pata:
    print('SIN PATA', *x)
print('Patas sin intento:', [(r['to_ext'], r['start']) for r in R if r['id'] not in usadas])
