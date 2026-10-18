# casos/atencion-es/codigo/test_preparar_transferencia.py
# Ejecutar: python3 -I casos/atencion-es/codigo/test_preparar_transferencia.py
import ast
import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import contexto_llamada  # noqa: E402
from preparar_transferencia import (  # noqa: E402
    FESTIVOS_NACIONALES,
    GESTION_FIN,
    GESTION_INICIO,
    gestion_abierta_en,
    hora_madrid,
    preparar,
)

UTC = timezone.utc
RUTA_NODO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "preparar_transferencia.py")

# Las salidas de «Resolver colas» llegan como entradas del nodo
COLAS_PRUEBA = {
    "cola_gestion_reserva": "sip:1@x",
    "cola_asistencia": "sip:2@x",
    "cola_nueva_reserva": "sip:3@x",
    "cola_horario_minibus": "sip:4@x",
}

# Textos fijos que ve el agente (copiados a mano: si cambian en el nodo, esta prueba avisa)
DETALLE_GESTION_CERRADA = (
    "No se ha transferido: el equipo de gestión de reservas atiende de lunes a viernes de ocho de la mañana a "
    "nueve de la noche, salvo festivos. Díselo al cliente con calma, no digas que le pasas con nadie y sigue con "
    "COLA DE GESTIÓN CERRADA."
)
DETALLE_COLA_NO_VALIDA = (
    "No se ha transferido: la cola no es válida. Usa gestion, asistencia, nueva_reserva o minibus."
)

# Todas las horas son de Madrid; entre paréntesis, el desfase respecto a UTC de ese día
SABADO_03 = datetime(2026, 10, 24, 1, 0, tzinfo=UTC)  # sábado 24/10 03:00 (UTC+2)
SABADO_10 = datetime(2026, 10, 24, 8, 0, tzinfo=UTC)  # sábado 24/10 10:00
DOMINGO_10 = datetime(2026, 10, 18, 8, 0, tzinfo=UTC)  # domingo 18/10 10:00
MARTES_10 = datetime(2026, 10, 20, 8, 0, tzinfo=UTC)  # martes 20/10 10:00
MARTES_07_59 = datetime(2026, 10, 20, 5, 59, tzinfo=UTC)
MARTES_08_00 = datetime(2026, 10, 20, 6, 0, tzinfo=UTC)
MARTES_20_59 = datetime(2026, 10, 20, 18, 59, tzinfo=UTC)
MARTES_21_00 = datetime(2026, 10, 20, 19, 0, tzinfo=UTC)
MARTES_21_02 = datetime(2026, 10, 20, 19, 2, tzinfo=UTC)  # la llamada empezó a las 20:55 con Gestión abierta
MARTES_23_00 = datetime(2026, 10, 20, 21, 0, tzinfo=UTC)
FESTIVO_12_OCT = datetime(2026, 10, 12, 8, 0, tzinfo=UTC)  # lunes, Fiesta Nacional, 10:00
FESTIVO_8_DIC = datetime(2026, 12, 8, 9, 0, tzinfo=UTC)  # martes, Inmaculada, 10:00 (UTC+1)
VIERNES_23_OCT_20_30 = datetime(2026, 10, 23, 18, 30, tzinfo=UTC)  # viernes 20:30 (UTC+2)
LUNES_26_OCT_20_30 = datetime(2026, 10, 26, 19, 30, tzinfo=UTC)  # lunes 20:30, ya con UTC+1 (cambio de hora el 25/10)
LUNES_26_OCT_21_30 = datetime(2026, 10, 26, 20, 30, tzinfo=UTC)  # lunes 21:30 (UTC+1)


def entrada(cola, **extra):
    return {"cola": cola, **COLAS_PRUEBA, **extra}


CASOS = [
    # (nombre, input_data, ahora_utc, comprobaciones)
    ("asistencia, sábado 03:00", entrada("asistencia"), SABADO_03,
     {"transferir": True, "numero": "sip:2@x", "resultado": "transferir"}),
    ("gestión, martes 10:00", entrada("gestion"), MARTES_10,
     {"transferir": True, "numero": "sip:1@x", "resultado": "transferir"}),
    # Gestión cierra durante la llamada: manda la hora de ahora, no gestion_abierta del principio
    ("gestión 21:02 aunque gestion_abierta venga true", entrada("gestion", gestion_abierta=True), MARTES_21_02,
     {"transferir": False, "numero": "", "resultado": "gestion_cerrada", "detalle": DETALLE_GESTION_CERRADA}),
    ("gestión 21:02 sin gestion_abierta en la entrada", entrada("gestion"), MARTES_21_02,
     {"transferir": False, "numero": "", "resultado": "gestion_cerrada"}),
    ("gestion_abierta false no bloquea si ahora está abierta", entrada("gestion", gestion_abierta=False), MARTES_10,
     {"transferir": True, "numero": "sip:1@x", "resultado": "transferir"}),
    ("gestion_abierta 'false' (texto) tampoco bloquea", entrada("gestion", gestion_abierta="false"), MARTES_10,
     {"transferir": True, "numero": "sip:1@x"}),
    ("gestión, festivo 8/12/2026 10:00", entrada("gestion"), FESTIVO_8_DIC,
     {"transferir": False, "numero": "", "resultado": "gestion_cerrada"}),
    ("gestión, festivo 12/10/2026 (lunes) 10:00", entrada("gestion"), FESTIVO_12_OCT,
     {"transferir": False, "numero": "", "resultado": "gestion_cerrada"}),
    ("gestión, domingo 10:00", entrada("gestion"), DOMINGO_10,
     {"transferir": False, "numero": "", "resultado": "gestion_cerrada"}),
    ("gestión, sábado 10:00", entrada("gestion"), SABADO_10,
     {"transferir": False, "numero": "", "resultado": "gestion_cerrada"}),
    # Límites del horario
    ("gestión 07:59 cerrada", entrada("gestion"), MARTES_07_59, {"transferir": False, "resultado": "gestion_cerrada"}),
    ("gestión 08:00 abierta", entrada("gestion"), MARTES_08_00, {"transferir": True, "numero": "sip:1@x"}),
    ("gestión 20:59 abierta", entrada("gestion"), MARTES_20_59, {"transferir": True, "numero": "sip:1@x"}),
    ("gestión 21:00 cerrada", entrada("gestion"), MARTES_21_00, {"transferir": False, "resultado": "gestion_cerrada"}),
    ("gestión viernes 20:30 (UTC+2) abierta", entrada("gestion"), VIERNES_23_OCT_20_30,
     {"transferir": True, "numero": "sip:1@x"}),
    ("gestión lunes 20:30 tras el cambio de hora (UTC+1) abierta", entrada("gestion"), LUNES_26_OCT_20_30,
     {"transferir": True, "numero": "sip:1@x"}),
    ("gestión lunes 21:30 tras el cambio de hora cerrada", entrada("gestion"), LUNES_26_OCT_21_30,
     {"transferir": False, "resultado": "gestion_cerrada"}),
    # El resto de colas no dependen del horario: el modo virtual lo controla el prompt
    ("minibús a las 23:00", entrada("minibus"), MARTES_23_00,
     {"transferir": True, "numero": "sip:4@x", "resultado": "transferir"}),
    ("nueva reserva a las 23:00", entrada("nueva_reserva"), MARTES_23_00,
     {"transferir": True, "numero": "sip:3@x", "resultado": "transferir"}),
    ("minibús en domingo", entrada("minibus"), DOMINGO_10, {"transferir": True, "numero": "sip:4@x"}),
    ("nueva reserva en festivo", entrada("nueva_reserva"), FESTIVO_8_DIC, {"transferir": True, "numero": "sip:3@x"}),
    ("asistencia en festivo a las 23:00", entrada("asistencia"), MARTES_23_00,
     {"transferir": True, "numero": "sip:2@x"}),
    # Normalización de la cola
    ("«GESTION » con mayúsculas y espacios", entrada("GESTION "), MARTES_10,
     {"transferir": True, "numero": "sip:1@x", "resultado": "transferir"}),
    ("«GESTION » cerrada también se normaliza", entrada("GESTION "), MARTES_21_02,
     {"transferir": False, "resultado": "gestion_cerrada"}),
    ("« Nueva_Reserva »", entrada(" Nueva_Reserva "), MARTES_10, {"transferir": True, "numero": "sip:3@x"}),
    ("«MINIBUS»", entrada("MINIBUS"), MARTES_10, {"transferir": True, "numero": "sip:4@x"}),
    # Cola no válida
    ("cola vacía", entrada(""), MARTES_10,
     {"transferir": False, "numero": "", "resultado": "cola_no_valida", "detalle": DETALLE_COLA_NO_VALIDA}),
    ("cola «18057» (una extensión)", entrada("18057"), MARTES_10,
     {"transferir": False, "numero": "", "resultado": "cola_no_valida", "detalle": DETALLE_COLA_NO_VALIDA}),
    ("cola numérica 18057 (entero)", entrada(18057), MARTES_10,
     {"transferir": False, "numero": "", "resultado": "cola_no_valida"}),
    ("cola None", entrada(None), MARTES_10, {"transferir": False, "resultado": "cola_no_valida"}),
    ("cola ausente", COLAS_PRUEBA, MARTES_10, {"transferir": False, "numero": "", "resultado": "cola_no_valida"}),
    ("cola «sip:1@x»", entrada("sip:1@x"), MARTES_10, {"transferir": False, "resultado": "cola_no_valida"}),
    ("cola «horario_minibus» (la clave de Resolver colas, no la cola del modelo)", entrada("horario_minibus"),
     MARTES_10, {"transferir": False, "resultado": "cola_no_valida"}),
    ("cola no válida en fin de semana sigue siendo no válida", entrada("otra"), DOMINGO_10,
     {"transferir": False, "resultado": "cola_no_valida"}),
    # Si Resolver colas no dio la URI de la cola pedida, nunca se transfiere a un número vacío
    ("falta la URI de asistencia", {"cola": "asistencia", "cola_gestion_reserva": "sip:1@x"}, MARTES_10,
     {"transferir": False, "numero": "", "resultado": "cola_no_valida"}),
    ("URI de minibús vacía", entrada("minibus", cola_horario_minibus="  "), MARTES_10,
     {"transferir": False, "numero": "", "resultado": "cola_no_valida"}),
    ("URI de Gestión vacía con Gestión abierta", entrada("gestion", cola_gestion_reserva=""), MARTES_10,
     {"transferir": False, "numero": "", "resultado": "cola_no_valida"}),
    ("Gestión cerrada y sin URI: manda gestion_cerrada", entrada("gestion", cola_gestion_reserva=""), MARTES_21_02,
     {"transferir": False, "numero": "", "resultado": "gestion_cerrada"}),
    ("la URI se devuelve sin espacios", entrada("asistencia", cola_asistencia=" sip:2@x "), MARTES_10,
     {"transferir": True, "numero": "sip:2@x"}),
    # Una hora sin zona se toma como UTC
    ("hora sin zona (UTC) a las 19:02", entrada("gestion"), datetime(2026, 10, 20, 19, 2),
     {"transferir": False, "resultado": "gestion_cerrada"}),
]

SALIDAS = {"transferir", "numero", "resultado", "detalle"}

# (nombre, inicio UTC, días): se recorren con paso de 15 minutos
RANGOS_EQUIVALENCIA = [
    ("octubre, semana del festivo del 12", datetime(2026, 10, 12, 0, 0, tzinfo=UTC), 7),
    ("octubre, semana del cambio de hora del 25", datetime(2026, 10, 22, 0, 0, tzinfo=UTC), 8),
    ("diciembre, semana del festivo del 8", datetime(2026, 12, 5, 0, 0, tzinfo=UTC), 8),
    ("diciembre, semana de Navidad", datetime(2026, 12, 21, 0, 0, tzinfo=UTC), 7),
    ("marzo, semana del cambio de hora del 29", datetime(2026, 3, 26, 0, 0, tzinfo=UTC), 7),
    ("enero de 2027, semana de Reyes", datetime(2027, 1, 3, 0, 0, tzinfo=UTC), 7),
]

fallos = 0
total = 0

for nombre, datos, ahora, esperado in CASOS:
    total += 1
    out = preparar(datos, ahora)
    malos = {k: (out.get(k), v) for k, v in esperado.items() if out.get(k) != v}
    if malos:
        fallos += 1
        print("FALLO preparar [%s]: (obtenido, esperado) %r" % (nombre, malos))

# Las cuatro salidas, con sus tipos, en todos los resultados
total += 1
formas = [preparar(entrada("gestion"), MARTES_10), preparar(entrada("gestion"), MARTES_21_02),
          preparar(entrada(""), MARTES_10)]
if any(set(o) != SALIDAS or not isinstance(o["transferir"], bool) or not isinstance(o["numero"], str)
       or not isinstance(o["detalle"], str) for o in formas):
    fallos += 1
    print("FALLO salidas: %r" % [sorted(o) for o in formas])

# Cuando transfiere no hay nada que decirle al agente; cuando no transfiere, siempre hay detalle
total += 1
if preparar(entrada("gestion"), MARTES_10)["detalle"] != "" \
        or not preparar(entrada(""), MARTES_10)["detalle"] \
        or not preparar(entrada("gestion"), MARTES_21_02)["detalle"]:
    fallos += 1
    print("FALLO detalle: debe ir vacío al transferir y lleno si no")

# Sin hora explícita usa la de ahora: asistencia no depende del horario, así que el resultado es estable
total += 1
if preparar(entrada("asistencia"))["numero"] != "sip:2@x":
    fallos += 1
    print("FALLO preparar sin hora: %r" % preparar(entrada("asistencia")))

# La copia de las funciones de hora da lo mismo que la de «Contexto de la llamada» (el nodo no puede importarla)
total += 1
if FESTIVOS_NACIONALES != contexto_llamada.FESTIVOS_NACIONALES:
    fallos += 1
    print("FALLO festivos: la copia difiere de contexto_llamada.py en %r"
          % sorted(FESTIVOS_NACIONALES ^ contexto_llamada.FESTIVOS_NACIONALES))

total += 1
if (GESTION_INICIO, GESTION_FIN) != (contexto_llamada.GESTION_INICIO, contexto_llamada.GESTION_FIN):
    fallos += 1
    print("FALLO horario de Gestión: copia %r, original %r"
          % ((GESTION_INICIO, GESTION_FIN), (contexto_llamada.GESTION_INICIO, contexto_llamada.GESTION_FIN)))

for nombre, inicio, dias in RANGOS_EQUIVALENCIA:
    total += 1
    t = inicio
    fin = inicio + timedelta(days=dias)
    distintos = []
    revisados = 0
    while t < fin:
        revisados += 1
        original = contexto_llamada.gestion_abierta_en(t)
        copia = gestion_abierta_en(t)
        # La copia de hora_madrid: mismo instante y mismo desfase
        misma_hora = (hora_madrid(t) == contexto_llamada.hora_madrid(t)
                      and hora_madrid(t).utcoffset() == contexto_llamada.hora_madrid(t).utcoffset())
        # Y el nodo entero: Gestión se transfiere justo cuando el original dice que está abierta
        out = preparar(entrada("gestion"), t)
        resultado_esperado = "transferir" if original else "gestion_cerrada"
        coherente = out["transferir"] == original and out["resultado"] == resultado_esperado
        if copia != original or not misma_hora or not coherente:
            distintos.append(t.strftime("%Y-%m-%d %H:%M UTC"))
        t += timedelta(minutes=15)
    if distintos or revisados != dias * 96:
        fallos += 1
        print("FALLO equivalencia [%s]: %d de %d instantes distintos, el primero %s"
              % (nombre, len(distintos), revisados, distintos[:1]))

# El nodo de HappyRobot no puede importar otros ficheros: solo biblioteca estándar y nada de contexto_llamada
total += 1
with open(RUTA_NODO, encoding="utf-8") as f:
    codigo = f.read()
importados = set()
for nodo in ast.walk(ast.parse(codigo)):
    if isinstance(nodo, ast.Import):
        importados |= {a.name.split(".")[0] for a in nodo.names}
    elif isinstance(nodo, ast.ImportFrom):
        importados.add((nodo.module or "").split(".")[0])
if importados - {"datetime"}:
    fallos += 1
    print("FALLO imports: el nodo importa %r, solo puede usar datetime" % sorted(importados))

# Como lo ejecuta el nodo: input_data ya definido y el resultado en `output`
total += 1
espacio = {"input_data": entrada("asistencia")}
exec(compile(codigo, RUTA_NODO, "exec"), espacio)
if espacio.get("output", {}).get("numero") != "sip:2@x" or espacio["output"].get("transferir") is not True:
    fallos += 1
    print("FALLO ejecución como nodo: %r" % espacio.get("output"))

print("%d/%d casos correctos" % (total - fallos, total))
sys.exit(1 if fallos else 0)
