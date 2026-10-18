# casos/atencion-es/codigo/test_contexto_llamada.py
# Ejecutar: python3 -I casos/atencion-es/codigo/test_contexto_llamada.py
import os
import sys
from datetime import date, datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from contexto_llamada import (  # noqa: E402
    FESTIVOS_NACIONALES,
    LINEAS,
    contexto,
    gestion_abierta_en,
    hora_madrid,
    modo_virtual_en,
)

UTC = timezone.utc
LINEAS_PRUEBA = {
    "111": ("prolongacion", "es"),
    "222": ("prolongacion", "en"),
    "333": ("minibus", "es"),
    "444": ("minibus", "en"),
}

# Martes 20/10/2026 10:00 en Madrid (UTC+2)
MARTES_10 = datetime(2026, 10, 20, 8, 0, tzinfo=UTC)
MARTES_22_30 = datetime(2026, 10, 20, 20, 30, tzinfo=UTC)  # 22:30 en Madrid: modo virtual
PROLONGACION_ES = {"to_number": "+34900000111", "from_number": "+34600000000"}
PROLONGACION_EN = {"to_number": "+34900000222", "from_number": "+34600000000"}
MINIBUS_ES = {"to_number": "+34900000333", "from_number": "+34600000000"}
MINIBUS_EN = {"to_number": "+34900000444", "from_number": "+34600000000"}

# Textos exactos de «Calcular horario nocturno» de la v25 de Minibús España (martes 10:00, saludo de mañana)
V25_MINIBUS_ES = "Hola, Centauro, buenos dias. Mi nombre es Daniel, su asistente de IA. En que puedo ayudarle?"
V25_MINIBUS_EN = "Hello, Centauro, good morning. My name is Daniel, your AI assistant. How can I help you?"
V25_MINIBUS_ES_VIRTUAL = (
    "Hola, Centauro, buenas noches. "
    "Soy Daniel, el asistente virtual de Centauro. A esta hora nuestro centro de atención está cerrado "
    "y no puedo pasarle con un compañero, pero sí puedo ayudarle a encontrar el minibús "
    "y con la información de nuestras oficinas. ¿En qué puedo ayudarle?"
)
V25_MINIBUS_EN_VIRTUAL = (
    "Hello, Centauro, good evening. "
    "I'm Daniel, Centauro's virtual assistant. Our customer service team is closed at this time, "
    "so I can't transfer you to a colleague, but I can help you find the shuttle bus "
    "and give you information about our offices. How can I help you?"
)
PROLONGACION_MENSAJE_ES = (
    "Centauro Rent a Car, buenos días, le atiende Daniel, su asistente de IA. "
    "¿Quiere prolongar un alquiler que tiene en curso?"
)
PROLONGACION_MENSAJE_EN = (
    "Centauro Rent a Car, good morning, this is Daniel, your AI assistant. "
    "Would you like to extend a rental you currently have?"
)

CASOS = [
    # (nombre, input_data, ahora_utc, comprobaciones)
    ("prolongación ES, martes 10:00", PROLONGACION_ES, MARTES_10,
     {"opcion_menu": "prolongacion", "idioma": "es", "gestion_abierta": True, "modo_virtual": False}),
    ("mensaje de Prolongación ES", PROLONGACION_ES, MARTES_10,
     {"mensaje_inicial": PROLONGACION_MENSAJE_ES}),
    ("mensaje de Prolongación EN", PROLONGACION_EN, MARTES_10,
     {"idioma": "en", "mensaje_inicial": PROLONGACION_MENSAJE_EN}),
    ("minibús ES conserva el saludo de la v25", MINIBUS_ES, MARTES_10,
     {"opcion_menu": "minibus", "mensaje_inicial": V25_MINIBUS_ES}),
    ("minibús EN conserva el saludo de la v25", MINIBUS_EN, MARTES_10,
     {"opcion_menu": "minibus", "idioma": "en", "mensaje_inicial": V25_MINIBUS_EN}),
    ("línea desconocida → minibús es", {"to_number": "+34900000999", "from_number": "+34600000000"}, MARTES_10,
     {"opcion_menu": "minibus", "idioma": "es"}),
    ("web con OPCION_PRUEBA", {"to_number": "web", "from_number": "web", "opcion_prueba": "prolongacion"}, MARTES_10,
     {"opcion_menu": "prolongacion", "idioma": "es", "whatsapp_disponible": False}),
    ("OPCION_PRUEBA no pisa una línea conocida", {**MINIBUS_ES, "opcion_prueba": "prolongacion"}, MARTES_10,
     {"opcion_menu": "minibus", "idioma": "es"}),
    ("OPCION_PRUEBA vacía en la web → minibús es", {"to_number": "web", "from_number": "web", "opcion_prueba": ""},
     MARTES_10, {"opcion_menu": "minibus", "idioma": "es"}),
    ("21:00 en punto cierra Gestión", PROLONGACION_ES, datetime(2026, 10, 20, 19, 0, tzinfo=UTC),
     {"gestion_abierta": False, "modo_virtual": False}),
    ("20:59 sigue abierta", PROLONGACION_ES, datetime(2026, 10, 20, 18, 59, tzinfo=UTC),
     {"gestion_abierta": True}),
    ("22:00 entra el modo virtual", PROLONGACION_ES, datetime(2026, 10, 20, 20, 0, tzinfo=UTC),
     {"modo_virtual": True}),
    ("sábado 10:00 cerrada", PROLONGACION_ES, datetime(2026, 10, 24, 8, 0, tzinfo=UTC),
     {"gestion_abierta": False}),
    ("festivo 8/12/2026 10:00", PROLONGACION_ES, datetime(2026, 12, 8, 9, 0, tzinfo=UTC),
     {"gestion_abierta": False, "festivo_nacional": True}),
    ("cambio de hora: lunes 26/10 08:30 (UTC+1)", PROLONGACION_ES, datetime(2026, 10, 26, 7, 30, tzinfo=UTC),
     {"gestion_abierta": True}),
    ("viernes 23/10 08:30 (UTC+2)", PROLONGACION_ES, datetime(2026, 10, 23, 6, 30, tzinfo=UTC),
     {"gestion_abierta": True}),
    ("nocturno CET a las 23:30", PROLONGACION_ES, datetime(2026, 10, 20, 21, 30, tzinfo=UTC),
     {"nocturno_cet": True}),
    # Modo virtual: los mensajes de Minibús de la v25 y el mismo de Prolongación
    ("minibús ES en modo virtual conserva el mensaje de la v25", MINIBUS_ES, MARTES_22_30,
     {"modo_virtual": True, "mensaje_inicial": V25_MINIBUS_ES_VIRTUAL}),
    ("minibús EN en modo virtual conserva el mensaje de la v25", MINIBUS_EN, MARTES_22_30,
     {"modo_virtual": True, "mensaje_inicial": V25_MINIBUS_EN_VIRTUAL}),
    ("Prolongación ES en modo virtual no avisa en el saludo", PROLONGACION_ES, MARTES_22_30,
     {"modo_virtual": True,
      "mensaje_inicial": PROLONGACION_MENSAJE_ES.replace("buenos días", "buenas noches")}),
    # Salidas de la v25 que se conservan
    ("grabación del aviso legal por idioma (es)", PROLONGACION_ES, MARTES_10,
     {"recording_id": "019fd44b-56a4-7a06-b240-1ede829ccceb"}),
    ("grabación del aviso legal por idioma (en)", PROLONGACION_EN, MARTES_10,
     {"recording_id": "019feaea-eea1-7139-a9ae-07e639c52456"}),
    ("teléfono dictado y WhatsApp de un móvil español", MINIBUS_ES, MARTES_10,
     {"telefono_dictado": "seis cero cero, cero cero cero, cero cero cero", "whatsapp_disponible": True,
      "numero_marcado": "34900000333"}),
    ("número oculto", {"to_number": "+34900000333", "from_number": ""}, MARTES_10,
     {"telefono_dictado": "número oculto", "whatsapp_disponible": False}),
    ("WhatsApp no se ofrece en la línea inglesa", {**MINIBUS_EN, "from_number": "+34600000000"}, MARTES_10,
     {"whatsapp_disponible": False}),
    ("horas locales y horario de verano en octubre", MINIBUS_ES, MARTES_10,
     {"hora_wet": "09:00", "hora_cet": "10:00", "hora_eet": "11:00", "horario_verano": True,
      "nocturno_wet": False, "nocturno_cet": False, "nocturno_eet": False, "nocturno_murcia": False,
      "callcenter_abierto": True, "saludo": "buenos dias", "saludo_en": "good morning",
      "saludo_localizado": "buenos dias", "idioma_nombre": "espanol", "festivo_nacional": False}),
]

# Todas las salidas de la v25 más opcion_menu y festivo_nacional
SALIDAS = {
    "nocturno_wet", "nocturno_cet", "nocturno_eet", "nocturno_murcia",
    "hora_wet", "hora_cet", "hora_eet", "callcenter_abierto", "modo_virtual",
    "saludo", "saludo_en", "saludo_localizado", "idioma", "idioma_nombre", "numero_marcado",
    "mensaje_inicial", "recording_id", "telefono_dictado", "gestion_abierta", "whatsapp_disponible",
    "horario_verano", "opcion_menu", "festivo_nacional",
}

# (nombre, instante UTC, hora de Madrid esperada «AAAA-MM-DD HH:MM»)
CASOS_HORA = [
    ("invierno", datetime(2026, 1, 15, 12, 0, tzinfo=UTC), "2026-01-15 13:00"),
    ("verano", datetime(2026, 7, 15, 12, 0, tzinfo=UTC), "2026-07-15 14:00"),
    ("un minuto antes del cambio de marzo", datetime(2026, 3, 29, 0, 59, tzinfo=UTC), "2026-03-29 01:59"),
    ("cambio de marzo a la 01:00 UTC", datetime(2026, 3, 29, 1, 0, tzinfo=UTC), "2026-03-29 03:00"),
    ("un minuto antes del cambio de octubre", datetime(2026, 10, 25, 0, 59, tzinfo=UTC), "2026-10-25 02:59"),
    ("cambio de octubre a la 01:00 UTC", datetime(2026, 10, 25, 1, 0, tzinfo=UTC), "2026-10-25 02:00"),
    ("2027: último domingo de octubre es el 31", datetime(2027, 10, 31, 1, 0, tzinfo=UTC), "2027-10-31 02:00"),
]

# (nombre, instante UTC, gestion_abierta_en, modo_virtual_en)
CASOS_HORARIOS = [
    ("domingo 10:00", datetime(2026, 10, 25, 9, 0, tzinfo=UTC), False, False),
    ("07:59 de un martes", datetime(2026, 10, 20, 5, 59, tzinfo=UTC), False, True),
    ("08:00 de un martes", datetime(2026, 10, 20, 6, 0, tzinfo=UTC), True, False),
    ("festivo 12/10/2026 (lunes) 10:00", datetime(2026, 10, 12, 8, 0, tzinfo=UTC), False, False),
    ("festivo 6/1/2027 (miércoles) en invierno, 10:00", datetime(2027, 1, 6, 9, 0, tzinfo=UTC), False, False),
    ("víspera del festivo, tarde de invierno", datetime(2027, 1, 5, 16, 0, tzinfo=UTC), True, False),
]

FESTIVOS_2026 = [(1, 1), (6, 1), (3, 4), (1, 5), (15, 8), (12, 10), (8, 12), (25, 12)]
FESTIVOS_2027 = [(1, 1), (6, 1), (26, 3), (1, 5), (15, 8), (12, 10), (1, 11), (6, 12), (8, 12), (25, 12)]

fallos = 0
total = 0

for nombre, entrada, ahora, esperado in CASOS:
    total += 1
    out = contexto(entrada, ahora, LINEAS_PRUEBA)
    malos = {k: (out.get(k), v) for k, v in esperado.items() if out.get(k) != v}
    if malos:
        fallos += 1
        print("FALLO contexto [%s]: (obtenido, esperado) %r" % (nombre, malos))

total += 1
out = contexto(MINIBUS_ES, MARTES_10, LINEAS_PRUEBA)
if set(out) != SALIDAS:
    fallos += 1
    print("FALLO salidas: sobran %r, faltan %r" % (sorted(set(out) - SALIDAS), sorted(SALIDAS - set(out))))

# Con las líneas del repo (marcadores, sin números reales) ninguna llamada reconoce la línea: minibús en español
total += 1
out = contexto({"to_number": "+34900000222", "from_number": "+34600000000"}, MARTES_10)
if out["opcion_menu"] != "minibus" or out["idioma"] != "es" or len(LINEAS) != 4 \
        or any(clave.isdigit() for clave in LINEAS):
    fallos += 1
    print("FALLO LINEAS del repo: %r %r" % (LINEAS, out["opcion_menu"]))

for nombre, ahora, esperado in CASOS_HORA:
    total += 1
    local = hora_madrid(ahora)
    if local.strftime("%Y-%m-%d %H:%M") != esperado:
        fallos += 1
        print("FALLO hora_madrid [%s]: %s, esperado %s" % (nombre, local.strftime("%Y-%m-%d %H:%M"), esperado))

for nombre, ahora, abierta, virtual in CASOS_HORARIOS:
    total += 1
    if gestion_abierta_en(ahora) != abierta or modo_virtual_en(ahora) != virtual:
        fallos += 1
        print("FALLO horarios [%s]: gestion=%r virtual=%r, esperado %r %r"
              % (nombre, gestion_abierta_en(ahora), modo_virtual_en(ahora), abierta, virtual))

total += 1
fuera = sorted(d for d in FESTIVOS_NACIONALES if d.year not in (2026, 2027))
faltan = sorted([date(2026, m, d) for d, m in FESTIVOS_2026] + [date(2027, m, d) for d, m in FESTIVOS_2027])
faltan = [d for d in faltan if d not in FESTIVOS_NACIONALES]
if fuera or faltan:
    fallos += 1
    print("FALLO festivos: fuera de 2026-2027 %r, faltan %r" % (fuera, faltan))

print("%d/%d casos correctos" % (total - fallos, total))
sys.exit(1 if fallos else 0)
