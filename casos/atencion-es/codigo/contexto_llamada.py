# ===============================================================
# CONTEXTO DE LA LLAMADA - bot único de Atención España
# ---------------------------------------------------------------
# Se pega tal cual en el nodo Python «Contexto de la llamada» (antes «Calcular horario nocturno» de Minibús ES
# v25), el primer nodo tras el trigger. Entradas (input_data): to_number, from_number y opcion_prueba (la variable de
# workflow OPCION_PRUEBA, vacía en producción).
#
# - opcion_menu (minibus | prolongacion) e idioma salen de la línea marcada (to_number), con la tabla LINEAS. Una
#   línea desconocida, un número oculto o una llamada web dan minibús en español, salvo que opcion_prueba diga
#   otra cosa (solo se mira si la línea no está en LINEAS).
# - Horarios en hora peninsular (el horario de verano se calcula a mano): modo virtual de 22:00 a 08:00; Gestión
#   abierta de lunes a viernes de 08:00 a 21:00, salvo festivos nacionales.
# - Las demás salidas son las de «Calcular horario nocturno» de la v25 (spec §5.2).
# - En el repo las líneas van como marcadores. Al pegar el código en HappyRobot, las claves de LINEAS se sustituyen
#   por los números reales, solo dígitos y sin «+» (la clave se compara con el final de los dígitos de to_number).
# - Las funciones de hora (hora_madrid, gestion_abierta_en, FESTIVOS_NACIONALES) se copian en «Preparar
#   transferencia», que no puede importar este fichero: si cambian aquí, cambian allí.
# ===============================================================
from datetime import date, datetime, timedelta, timezone

LINEAS = {
    "<LINEA_PROLONGACION_ES>": ("prolongacion", "es"),
    "<LINEA_PROLONGACION_EN>": ("prolongacion", "en"),
    "<LINEA_MINIBUS_ES>": ("minibus", "es"),
    "<LINEA_MINIBUS_EN>": ("minibus", "en"),
}

OPCIONES = ("minibus", "prolongacion")

# Festivos de ámbito nacional (resolución de la Dirección General de Trabajo publicada en el BOE). Los
# autonómicos y locales no cuentan. Hay que añadir el año siguiente antes de que acabe 2027.
FESTIVOS_NACIONALES = {
    # 2026
    date(2026, 1, 1),    # Año Nuevo
    date(2026, 1, 6),    # Epifanía
    date(2026, 4, 3),    # Viernes Santo
    date(2026, 5, 1),    # Fiesta del Trabajo
    date(2026, 8, 15),   # Asunción
    date(2026, 10, 12),  # Fiesta Nacional de España
    date(2026, 12, 8),   # Inmaculada Concepción
    date(2026, 12, 25),  # Navidad
    # 2027
    date(2027, 1, 1),    # Año Nuevo
    date(2027, 1, 6),    # Epifanía
    date(2027, 3, 26),   # Viernes Santo
    date(2027, 5, 1),    # Fiesta del Trabajo
    date(2027, 8, 15),   # Asunción (domingo)
    date(2027, 10, 12),  # Fiesta Nacional de España
    date(2027, 11, 1),   # Todos los Santos
    date(2027, 12, 6),   # Día de la Constitución
    date(2027, 12, 8),   # Inmaculada Concepción
    date(2027, 12, 25),  # Navidad
}

# Oficina de aeropuerto cerrada: de 23:00 a 07:00 (hora local del aeropuerto).
# Los flags nocturno_* indican si la oficina (y su minibus) ya ha cerrado.
NOCHE_INICIO = 23
NOCHE_FIN = 7

# Murcia cierra antes: de 22:00 a 08:00 (hora peninsular)
MURCIA_INICIO = 22
MURCIA_FIN = 8

# Centro de atención con operadores: de 08:00 a 22:00 (hora peninsular).
# Fuera de esa franja el agente atiende en modo virtual, sin transferencias (salvo Asistencia).
CALLCENTER_INICIO = 8
CALLCENTER_FIN = 22

# Cola de GESTION DE RESERVA: solo de lunes a viernes de 08:00 a 21:00 (hora peninsular) y no en festivos
# nacionales. Fuera de ese horario la cola reproduce una locución de cerrado y nadie atiende.
GESTION_INICIO = 8
GESTION_FIN = 21

# Desfase base respecto a UTC en horario de invierno
BASE = {
    "wet": 0,  # Portugal y Madeira
    "cet": 1,  # España peninsular, Baleares e Italia
    "eet": 2,  # Grecia
}

# Grabación de aviso legal (disclaimer) según el idioma resuelto.
# greeting-minibus-en -> línea en inglés; greetinminibus-es -> línea en español (también respaldo)
DISCLAIMER_EN = "019feaea-eea1-7139-a9ae-07e639c52456"
DISCLAIMER_ES = "019fd44b-56a4-7a06-b240-1ede829ccceb"

# Mensaje inicial por (opción, idioma, modo virtual); {saludo} se sustituye por el saludo de la franja.
# Minibús: textos de la v25; en modo virtual avisa desde el principio de que no hay operadores.
# Prolongación: el mismo en modo virtual; allí se avisa cuando el cliente pide una persona (spec §5.2).
MENSAJES = {
    ("minibus", "es", False): (
        "Hola, Centauro, {saludo}. "
        "Mi nombre es Daniel, su asistente de IA. En que puedo ayudarle?"
    ),
    ("minibus", "es", True): (
        "Hola, Centauro, {saludo}. "
        "Soy Daniel, el asistente virtual de Centauro. A esta hora nuestro centro de atención está cerrado "
        "y no puedo pasarle con un compañero, pero sí puedo ayudarle a encontrar el minibús "
        "y con la información de nuestras oficinas. ¿En qué puedo ayudarle?"
    ),
    ("minibus", "en", False): (
        "Hello, Centauro, {saludo}. "
        "My name is Daniel, your AI assistant. How can I help you?"
    ),
    ("minibus", "en", True): (
        "Hello, Centauro, {saludo}. "
        "I'm Daniel, Centauro's virtual assistant. Our customer service team is closed at this time, "
        "so I can't transfer you to a colleague, but I can help you find the shuttle bus "
        "and give you information about our offices. How can I help you?"
    ),
    ("prolongacion", "es", False): (
        "Centauro Rent a Car, {saludo}, le atiende Daniel, su asistente de IA. "
        "¿Quiere prolongar un alquiler que tiene en curso?"
    ),
    ("prolongacion", "en", False): (
        "Centauro Rent a Car, {saludo}, this is Daniel, your AI assistant. "
        "Would you like to extend a rental you currently have?"
    ),
}

# El saludo del mensaje de Prolongación en español lleva tilde; `saludo` conserva el valor de la v25
CON_TILDE = {"buenos dias": "buenos días"}

PALABRAS = {"0": "cero", "1": "uno", "2": "dos", "3": "tres", "4": "cuatro",
            "5": "cinco", "6": "seis", "7": "siete", "8": "ocho", "9": "nueve"}


# ---------------------------------------------------------------
# Hora peninsular y horarios
# ---------------------------------------------------------------
def _en_utc(t):
    if t.tzinfo is None:
        return t.replace(tzinfo=timezone.utc)
    return t.astimezone(timezone.utc)


def ultimo_domingo(anio, mes):
    # Primer día del mes siguiente, retrocediendo al domingo anterior
    if mes == 12:
        d = datetime(anio + 1, 1, 1, tzinfo=timezone.utc)
    else:
        d = datetime(anio, mes + 1, 1, tzinfo=timezone.utc)
    d = d - timedelta(days=1)
    while d.weekday() != 6:  # 6 = domingo
        d = d - timedelta(days=1)
    return d


def en_horario_verano_ue(t):
    # Reglas UE: empieza el último domingo de marzo a las 01:00 UTC
    # y termina el último domingo de octubre a las 01:00 UTC
    t = _en_utc(t)
    inicio = ultimo_domingo(t.year, 3).replace(hour=1)
    fin = ultimo_domingo(t.year, 10).replace(hour=1)
    return inicio <= t < fin


def hora_local(ahora_utc, base):
    """Hora local de una zona con `base` horas de desfase en invierno (una más en horario de verano)."""
    t = _en_utc(ahora_utc)
    desfase = base + (1 if en_horario_verano_ue(t) else 0)
    return t.astimezone(timezone(timedelta(hours=desfase)))


def hora_madrid(ahora_utc):
    return hora_local(ahora_utc, BASE["cet"])


def es_nocturno(hora):
    # Ventana que cruza medianoche
    return hora >= NOCHE_INICIO or hora < NOCHE_FIN


def callcenter_abierto_en(ahora_utc):
    return CALLCENTER_INICIO <= hora_madrid(ahora_utc).hour < CALLCENTER_FIN


def modo_virtual_en(ahora_utc):
    return not callcenter_abierto_en(ahora_utc)


def festivo_nacional_en(ahora_utc):
    return hora_madrid(ahora_utc).date() in FESTIVOS_NACIONALES


def gestion_abierta_en(ahora_utc):
    local = hora_madrid(ahora_utc)
    return (local.weekday() < 5
            and local.date() not in FESTIVOS_NACIONALES
            and GESTION_INICIO <= local.hour < GESTION_FIN)


def saludos(hora):
    """(español, inglés) según la franja del día, referida a la hora peninsular."""
    if 6 <= hora < 13:
        return "buenos dias", "good morning"
    if 13 <= hora < 21:
        return "buenas tardes", "good afternoon"
    return "buenas noches", "good evening"


# ---------------------------------------------------------------
# Línea marcada, idioma y mensaje inicial
# ---------------------------------------------------------------
def identificar_linea(digitos, opcion_prueba, lineas):
    """(opción del menú, idioma) a partir de los dígitos del número marcado."""
    for clave, (opcion, idioma) in lineas.items():
        if clave and digitos.endswith(clave):
            return opcion, idioma
    # Línea desconocida, número oculto o llamada web: minibús en español, salvo opcion_prueba
    prueba = str(opcion_prueba or "").strip().lower()
    return (prueba if prueba in OPCIONES else "minibus"), "es"


def mensaje_inicial(opcion, idioma, modo_virtual, saludo, saludo_en):
    if idioma == "en":
        saludo_texto = saludo_en
    elif opcion == "prolongacion":
        saludo_texto = CON_TILDE.get(saludo, saludo)
    else:
        saludo_texto = saludo
    # Solo Minibús avisa del modo virtual en el saludo
    virtual = modo_virtual and opcion == "minibus"
    return MENSAJES[(opcion, idioma, virtual)].format(saludo=saludo_texto)


# ---------------------------------------------------------------
# Teléfono del cliente
# ---------------------------------------------------------------
def dictar(d):
    grupos = [d[i:i + 3] for i in range(0, len(d), 3)]
    return ", ".join(" ".join(PALABRAS[c] for c in g) for g in grupos)


def telefono_dictado(from_raw):
    """Teléfono del cliente dictado dígito a dígito (para el whisper)."""
    tel = "".join(c for c in from_raw if c.isdigit())
    if from_raw.startswith("00"):
        tel = tel[2:]
        internacional = True
    else:
        internacional = from_raw.startswith("+")

    if len(tel) < 6:
        return "número oculto"
    if internacional and tel.startswith("34") and len(tel) == 11:
        return dictar(tel[2:])
    if internacional:
        return "internacional, más " + dictar(tel)
    return dictar(tel)


def whatsapp_disponible(from_raw, idioma):
    """Se puede ofrecer el punto de encuentro por WhatsApp si la llamada es de la línea en español (la plantilla
    «minibus_punto_texto_boton» está en español) y el número del cliente parece un móvil. Que el aeropuerto tenga
    seguimiento en directo lo decide el prompt de Punto de encuentro y lo vuelve a comprobar «Preparar WhatsApp
    minibus» antes de enviar."""
    wa_tel = "".join(c for c in from_raw if c.isdigit())
    if from_raw.startswith("00"):
        wa_tel = wa_tel[2:]
    elif not from_raw.startswith("+") and len(wa_tel) == 9:
        wa_tel = "34" + wa_tel
    if wa_tel.startswith("34"):
        wa_movil = len(wa_tel) == 11 and wa_tel[2] in "67"
    else:
        wa_movil = 8 <= len(wa_tel) <= 15
    return bool(wa_movil and idioma == "es")


# ---------------------------------------------------------------
# Salida del nodo
# ---------------------------------------------------------------
def contexto(input_data, ahora_utc=None, lineas=LINEAS):
    ahora = _en_utc(ahora_utc or datetime.now(timezone.utc))
    verano = en_horario_verano_ue(ahora)
    output = {"horario_verano": verano}

    for clave, base in BASE.items():
        local = hora_local(ahora, base)
        output["nocturno_" + clave] = es_nocturno(local.hour)
        output["hora_" + clave] = local.strftime("%H:%M")

    hora_cet = hora_madrid(ahora).hour
    output["nocturno_murcia"] = hora_cet >= MURCIA_INICIO or hora_cet < MURCIA_FIN
    output["callcenter_abierto"] = callcenter_abierto_en(ahora)
    output["modo_virtual"] = modo_virtual_en(ahora)
    saludo, saludo_en = saludos(hora_cet)
    output["saludo"] = saludo
    output["saludo_en"] = saludo_en

    # Idioma de atención y opción del menú según el número marcado por el cliente. Nos quedamos solo con los
    # dígitos para que el formato no afecte.
    digitos = "".join(c for c in str(input_data.get("to_number") or "") if c.isdigit())
    opcion, idioma = identificar_linea(digitos, input_data.get("opcion_prueba"), lineas)
    output["opcion_menu"] = opcion
    output["idioma"] = idioma
    output["idioma_nombre"] = "English" if idioma == "en" else "espanol"
    output["numero_marcado"] = digitos

    # Saludo ya resuelto en el idioma que toca y mensaje inicial completo, listo para el campo de saludo del agente
    output["saludo_localizado"] = saludo_en if idioma == "en" else saludo
    output["mensaje_inicial"] = mensaje_inicial(opcion, idioma, output["modo_virtual"], saludo, saludo_en)

    # Comparte la misma decisión que el saludo, de modo que aviso legal y agente no puedan quedar en idiomas distintos
    output["recording_id"] = DISCLAIMER_EN if idioma == "en" else DISCLAIMER_ES

    from_raw = str(input_data.get("from_number") or "").strip()
    output["telefono_dictado"] = telefono_dictado(from_raw)
    output["festivo_nacional"] = festivo_nacional_en(ahora)
    output["gestion_abierta"] = gestion_abierta_en(ahora)
    output["whatsapp_disponible"] = whatsapp_disponible(from_raw, idioma)
    return output


try:
    _entrada = input_data  # noqa: F821 (lo inyecta el nodo Python de HappyRobot)
except NameError:  # importado desde las pruebas locales
    _entrada = None
if _entrada is not None:
    output = contexto(_entrada)
