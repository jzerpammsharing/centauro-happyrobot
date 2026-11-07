"""Business case: coste de los bots de HappyRobot frente a atender las mismas llamadas con personas (salario mínimo).

Uso: python3 -I scripts/coste_bots_vs_humanos.py <dir_datos> [--json salida.json]
- <dir_datos>: carpeta con un JSON por bot ({"meta": {...}, "llamadas": [...]}); cada llamada con `created` (ISO UTC),
  `duration_s`, `transferida`, `seg_bot` y `seg_tras_transferencia` (null si no se pudo partir). Las de
  `tipo` = "prueba" no cuentan.
- Imprime las tablas del informe y, con --json, guarda los números.

Solo lectura y sin dependencias externas. Todos los supuestos están en las constantes de abajo.
"""
import importlib.util
import json
import math
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone

RUTA_CONTEXTO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "casos", "atencion-es", "codigo",
                             "contexto_llamada.py")
_especificacion = importlib.util.spec_from_file_location("contexto_llamada", RUTA_CONTEXTO)
_contexto = importlib.util.module_from_spec(_especificacion)
_especificacion.loader.exec_module(_contexto)
gestion_abierta_en = _contexto.gestion_abierta_en

# --- HappyRobot (Order Form #2, 01/09/2026) ---
EUR_CREDITO = 0.004  # tarifa del crédito (incluido en la cuota y para el exceso)
CUOTA_ANUAL = 450_000
CREDITOS_ANUALES = 50_000_000  # 25 M pagados + 25 M gratis el primer año
EUR_CREDITO_CARGADO = CUOTA_ANUAL / CREDITOS_ANUALES  # 0,009 €: toda la cuota repartida entre todos los créditos
CREDITOS_MIN_INDICATIVO = 24  # Schedule A: LLM 6 + Voice Orchestration 16 + telefonía 2 por minuto
# Créditos por llamada facturados (pantalla de uso de HappyRobot, sin evals):
# - Prolongación: 323,94 en 521 runs del 18 al 25/10 (UTC), todo voz y run.
# - Minibús ES: 307,26 del 18 al 25/10 (8 días UTC), prorrateado a 7 días sobre las 1.068 llamadas medidas; la media
#   de 30 días es menor ((831,15 − 31,26 de evals) / 4.890 runs = 0,16 €) porque el coste ha subido en octubre.
# - Atención España: la pantalla da 4,26 de voz y run en 67 llamadas de producción (16 créditos por llamada, 7,6 por
#   minuto), muy por debajo de lo esperable; seguramente falta facturar la voz del 25/10. Se usa la estimación del spec
#   (§9: 60–75 créditos) para no abaratar el bot. Los otros 276,39 son evals: construcción.
CREDITOS_LLAMADA = {'prolongacion_es': 323.94 / 521 / EUR_CREDITO,
                    'minibus_es': 307.26 * 7 / 8 / 1068 / EUR_CREDITO,
                    'atencion_es': 70}
EVALS_SEMANA_EUR = 276.39  # evals de Atención España del 18 al 25/10: coste de construcción, no de atender

# --- Personas (salario mínimo 2026) ---
SMI_ANUAL = 1_221 * 14  # 17.094 €, Real Decreto 126/2026
CUOTAS_EMPRESA = 0.32
COSTE_FTE = SMI_ANUAL * (1 + CUOTAS_EMPRESA)  # ~22.564 €
HORAS_ANUALES = 40 * 52 - 22 * 8 - 14 * 8  # 1.792 h: 40 h/semana menos vacaciones y festivos
MERMA = 0.16  # pausas de pantalla (8 %), absentismo (5 %), formación y reuniones (3 %)
OCUPACION = 0.70  # parte del tiempo disponible que se pasa atendiendo (escenario 1)
ACW_S = 30  # trabajo posterior por llamada atendida
MIN_CONVERSACION_S = 15  # por debajo, cuelgue: una persona no tendría trabajo posterior
NIVEL_SERVICIO, SEGUNDOS_OBJETIVO = 0.80, 30

DIAS_ANIO = 365
MADRID_CAMBIO = datetime(2026, 10, 25, 1, tzinfo=timezone.utc)  # UTC+2 antes, UTC+1 después


def a_madrid(iso):
    t = datetime.fromisoformat(iso.replace('Z', '+00:00')).astimezone(timezone.utc)
    return t + (timedelta(hours=2) if t < MADRID_CAMBIO else timedelta(hours=1))


def eur_minuto_persona():
    minutos_utiles = HORAS_ANUALES * 60 * (1 - MERMA) * OCUPACION
    return COSTE_FTE / minutos_utiles


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


def agentes(a, aht_s, sl=NIVEL_SERVICIO, t=SEGUNDOS_OBJETIVO):
    """Agentes conectados para cumplir el nivel de servicio; al menos 1 en cada hora que el bot atiende."""
    if a <= 0:
        return 1
    n = max(1, math.ceil(a))
    while 1 - erlang_c(n, a) * math.exp(-(n - a) * t / aht_s) < sl:
        n += 1
    return n


def seg_bot(ll):
    """Segundos del bot antes de transferir: el exacto, o el estimado por la transcripción, o toda la llamada."""
    for campo in ('seg_bot', 'seg_bot_aprox'):
        if ll.get(campo) is not None:
            return ll[campo]
    return ll['duration_s']


def seg_persona(ll):
    """Lo que tardaría una persona en la parte que hace el bot: la misma conversación más el trabajo posterior."""
    bot = seg_bot(ll)
    return bot + (ACW_S if ll['duration_s'] >= MIN_CONVERSACION_S and not ll.get('transferida') else 0)


def leer(directorio):
    bots = {}
    for nombre in sorted(os.listdir(directorio)):
        if nombre.endswith('.json'):
            datos = json.load(open(os.path.join(directorio, nombre)))
            bots[nombre[:-5]] = [dict(ll, created=ll.get('created') or ll['created_utc']) for ll in datos['llamadas']
                                 if ll.get('tipo', 'produccion') != 'prueba']
    return bots


def resumen_bot(bot, llamadas):
    n = len(llamadas)
    seg_total = sum(ll['duration_s'] for ll in llamadas)
    segundos_bot = sum(seg_bot(ll) for ll in llamadas)
    transferidas = sum(1 for ll in llamadas if ll.get('transferida'))
    sin_transferir = sum(1 for ll in llamadas if not ll.get('transferida') and ll['duration_s'] >= MIN_CONVERSACION_S)
    creditos = n * CREDITOS_LLAMADA[bot]
    return {
        'llamadas': n, 'min_total': seg_total / 60, 'min_bot': segundos_bot / 60,
        'min_tras_transferencia': (seg_total - segundos_bot) / 60, 'transferidas': transferidas,
        'sin_transferir': sin_transferir, 'creditos': creditos,
        'creditos_indicativos': seg_total / 60 * CREDITOS_MIN_INDICATIVO,
        'min_persona': sum(seg_persona(ll) for ll in llamadas) / 60,
        # conservador: en las transferidas el agente vuelve a preguntar, así que el bot no le ahorra nada
        'min_persona_sin_transferir': sum(seg_persona(ll) for ll in llamadas if not ll.get('transferida')) / 60,
    }


def cobertura(llamadas, dias, solo_cerrada=False):
    """Horas de agente por semana para atender a 80/30, hora a hora del periodo, lo que hoy atiende el bot.

    solo_cerrada: solo las horas con Gestión cerrada (en las abiertas lo absorbe el equipo actual)."""
    por_hora = defaultdict(list)
    for ll in llamadas:
        t = datetime.fromisoformat(ll['created'].replace('Z', '+00:00')).astimezone(timezone.utc)
        por_hora[t.replace(minute=0, second=0, microsecond=0)].append(seg_persona(ll))
    inicio = min(por_hora)
    inicio = inicio - timedelta(hours=a_madrid(inicio.isoformat()).hour)  # medianoche de Madrid del primer día
    horas_agente = 0
    for i in range(dias * 24):
        h = inicio + timedelta(hours=i)
        if solo_cerrada and gestion_abierta_en(h + timedelta(minutes=30)):
            continue
        v = por_hora.get(h, [])
        aht = sum(v) / len(v) if v else 180
        horas_agente += agentes(len(v) * aht / 3600, aht)
    return horas_agente * 7 / dias


def calcular(bots):
    todas = [ll for v in bots.values() for ll in v]
    dias = (max(a_madrid(ll['created']).date() for ll in todas) - min(a_madrid(ll['created']).date() for ll in todas)).days + 1
    anual = DIAS_ANIO / dias
    r = {'dias': dias, 'bots': {b: resumen_bot(b, v) for b, v in bots.items()}}
    tot = {k: sum(x[k] for x in r['bots'].values()) for k in next(iter(r['bots'].values()))}
    r['total'] = tot
    eur_min = eur_minuto_persona()
    horas_semana = cobertura(todas, dias)
    horas_fte_semana = HORAS_ANUALES / 52 * (1 - MERMA)
    fte = horas_semana / horas_fte_semana
    abiertas = [ll for ll in todas if gestion_abierta_en(datetime.fromisoformat(ll['created'].replace('Z', '+00:00')))]
    horas_cerrada = cobertura(todas, dias, solo_cerrada=True)
    min_abierta = sum(seg_persona(ll) for ll in abiertas) / 60
    r['hr'] = {
        'semana_eur_credito': tot['creditos'] * EUR_CREDITO,
        'semana_eur_cargado': tot['creditos'] * EUR_CREDITO_CARGADO,
        'semana_eur_indicativo': tot['creditos_indicativos'] * EUR_CREDITO,
        'anual_creditos': tot['creditos'] * anual,
        'pct_bolsa': tot['creditos'] * anual / CREDITOS_ANUALES,
        'evals_semana': EVALS_SEMANA_EUR,
    }
    r['personas'] = {
        'eur_minuto': eur_min, 'coste_fte': COSTE_FTE,
        'semana_minuto': tot['min_persona'] * eur_min,
        'semana_minuto_conservador': tot['min_persona_sin_transferir'] * eur_min,
        'horas_agente_semana': horas_semana, 'fte_cobertura': fte,
        'semana_cobertura': fte * COSTE_FTE / 52,
        'fte_minuto': tot['min_persona'] * anual / (HORAS_ANUALES * 60 * (1 - MERMA) * OCUPACION),
        'llamadas_gestion_abierta': len(abiertas),
        'horas_agente_semana_cerrada': horas_cerrada, 'fte_cerrada': horas_cerrada / horas_fte_semana,
        'semana_mixto': min_abierta * eur_min + horas_cerrada / horas_fte_semana * COSTE_FTE / 52,
    }
    r['anual'] = anual
    return r


def eur(x):
    return f'{x:,.0f} €'.replace(',', '.')


def imprimir(r):
    a = r['anual']
    print(f"Días medidos: {r['dias']} (anualizado ×{a:.1f})\n")
    print('bot llamadas min_total min_bot min_tras sin_transferir transferidas créditos')
    for b, x in list(r['bots'].items()) + [('TOTAL', r['total'])]:
        print(f"{b} {x['llamadas']} {x['min_total']:.0f} {x['min_bot']:.0f} {x['min_tras_transferencia']:.0f} "
              f"{x['sin_transferir']} {x['transferidas']} {x['creditos']:.0f}")
    hr, p = r['hr'], r['personas']
    print(f"\nHappyRobot semana: {eur(hr['semana_eur_credito'])} a 0,004 €/crédito; {eur(hr['semana_eur_cargado'])} "
          f"con la cuota repartida (0,009 €); {eur(hr['semana_eur_indicativo'])} con la tabla indicativa (24 cr/min)")
    print(f"  al año: {hr['anual_creditos'] / 1e6:.2f} M créditos = {hr['pct_bolsa']:.1%} de la bolsa de 50 M; "
          f"{eur(hr['semana_eur_credito'] * a)} – {eur(hr['semana_eur_cargado'] * a)}")
    print(f"  más evals de construcción (Atención España): {eur(hr['evals_semana'])} esta semana")
    print(f"\nPersonas: {p['eur_minuto']:.3f} €/min atendido; FTE {eur(p['coste_fte'])}")
    print(f"  escenario 1 (minutos absorbidos por el equipo): {eur(p['semana_minuto'])}/semana, "
          f"{eur(p['semana_minuto'] * a)}/año, {p['fte_minuto']:.1f} FTE")
    print(f"  escenario 1 conservador (solo las no transferidas): {eur(p['semana_minuto_conservador'])}/semana, "
          f"{eur(p['semana_minuto_conservador'] * a)}/año")
    print(f"  escenario 2 (cobertura 24/7 a 80/30): {p['horas_agente_semana']} h de agente/semana, "
          f"{p['fte_cobertura']:.1f} FTE, {eur(p['semana_cobertura'])}/semana, {eur(p['semana_cobertura'] * a)}/año")
    print(f"  escenario 3 (de día el equipo; con Gestión cerrada, cobertura a 80/30): "
          f"{p['llamadas_gestion_abierta']} llamadas con Gestión abierta; {p['horas_agente_semana_cerrada']:.0f} h/semana "
          f"cerrada = {p['fte_cerrada']:.1f} FTE; {eur(p['semana_mixto'])}/semana, {eur(p['semana_mixto'] * a)}/año")


if __name__ == '__main__':
    resultado = calcular(leer(sys.argv[1]))
    imprimir(resultado)
    if '--json' in sys.argv:
        json.dump(resultado, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1, ensure_ascii=False)
