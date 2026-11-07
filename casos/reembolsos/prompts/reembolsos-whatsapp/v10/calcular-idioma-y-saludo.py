from datetime import datetime, timedelta, timezone

# ===============================================================
# IDIOMA, SALUDO, FECHA Y AVISO LEGAL - CENTAURO REEMBOLSOS SPAIN
# ---------------------------------------------------------------
# La IVR solo redirige a este agente de 08:00 a 22:00, asi que no
# hay logica de horario para las transferencias.
#
# Para anadir un idioma:
#   1. Anade su numero de linea en NUMEROS_IDIOMA.
#   2. Anade su bloque en IDIOMAS (nombre, saludos, mensaje, grabacion).
#   3. Anade sus colas en el nodo "Resolver colas por idioma".
# ===============================================================

# Numero marcado (solo digitos, con prefijo de pais) -> idioma
# PENDIENTE: anadir los numeros de la linea de reembolsos.
# Ejemplo: "349112003003": "en",
NUMEROS_IDIOMA = {
}

IDIOMA_RESPALDO = "es"

MESES_ES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
            "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
DIAS_ES = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]

IDIOMAS = {
    "es": {
        "nombre": "espanol",
        "manana": "buenos días",
        "tarde": "buenas tardes",
        "noche": "buenas noches",
        # Daniel se presenta como asistente de IA (decision de negocio) y abre con pregunta abierta
        "mensaje": "Centauro Rent a Car, {saludo}, le atiende Daniel, el asistente de IA de Centauro. Cuénteme, ¿en qué puedo ayudarle?",
        # greetinminibus-es (misma grabacion que minibus)
        "recording_id": "019fd44b-56a4-7a06-b240-1ede829ccceb",
    },
}

# ---------------------------------------------------------------
# Hora local de Espana peninsular (CET/CEST, reglas UE)
# ---------------------------------------------------------------
ahora_utc = datetime.now(timezone.utc)


def ultimo_domingo(anio, mes):
    if mes == 12:
        d = datetime(anio + 1, 1, 1, tzinfo=timezone.utc)
    else:
        d = datetime(anio, mes + 1, 1, tzinfo=timezone.utc)
    d = d - timedelta(days=1)
    while d.weekday() != 6:
        d = d - timedelta(days=1)
    return d


inicio_verano = ultimo_domingo(ahora_utc.year, 3).replace(hour=1)
fin_verano = ultimo_domingo(ahora_utc.year, 10).replace(hour=1)
verano = inicio_verano <= ahora_utc < fin_verano
ahora_local = ahora_utc + timedelta(hours=2 if verano else 1)
hora_cet = ahora_local.hour

# ---------------------------------------------------------------
# Idioma segun el numero marcado
# ---------------------------------------------------------------
to_number_raw = input_data.get("to_number") or ""
digitos = "".join(c for c in str(to_number_raw) if c.isdigit())

idioma = IDIOMA_RESPALDO
for numero, codigo in NUMEROS_IDIOMA.items():
    if digitos and digitos.endswith(numero):
        idioma = codigo
        break
if idioma not in IDIOMAS:
    idioma = IDIOMA_RESPALDO

datos = IDIOMAS[idioma]

# Tres franjas: buenos dias (06:00-14:00), buenas tardes (14:00-21:00), buenas noches el resto
if 6 <= hora_cet < 14:
    saludo = datos["manana"]
elif 14 <= hora_cet < 21:
    saludo = datos["tarde"]
else:
    saludo = datos["noche"]

# Fecha de hoy (hora de Espana peninsular)
fecha_hoy_iso = ahora_local.strftime("%Y-%m-%d")
fecha_hoy = "%s %d de %s de %d (%s)" % (
    DIAS_ES[ahora_local.weekday()], ahora_local.day,
    MESES_ES[ahora_local.month - 1], ahora_local.year, fecha_hoy_iso)

# Numero desde el que llama el cliente, tal como llega al trigger
numero_cliente = str(input_data.get("from_number") or "")


def normalizar_telefono(numero):
    """Devuelve el número en E.164 (+ y dígitos) o "" si no es un teléfono."""
    texto = str(numero or "").strip()
    digitos = "".join(c for c in texto if c.isdigit())
    if not digitos:
        return ""
    if texto.startswith("+"):
        return "+" + digitos
    if digitos.startswith("00"):
        return "+" + digitos[2:]
    if len(digitos) == 9:
        return "+34" + digitos
    return "+" + digitos


def whatsapp_posible(e164):
    """True si tiene sentido ofrecer WhatsApp a ese número."""
    if not e164 or not e164.startswith("+"):
        return False
    if e164.startswith("+34"):
        return len(e164) == 12 and e164[3] in "67"
    return len(e164) >= 9


def telefono_para_consulta(numero_cliente, telefono_prueba=""):
    """Teléfono (E.164) que va al MCP para buscar la reserva sin pedir datos, o "" si no hay.

    Es el número desde el que llama el cliente. En las llamadas web del editor (from_number =
    "web") es TELEFONO_PRUEBA, para poder probar la búsqueda por teléfono con una reserva
    propia. Con menos de 9 cifras (extensión interna, oculto) no se puede buscar: "".
    """
    numero = telefono_prueba if str(numero_cliente or "").strip() == "web" else numero_cliente
    e164 = normalizar_telefono(numero)
    return e164 if len(e164) - 1 >= 9 else ""


# WhatsApp: numero de destino y si tiene sentido ofrecerlo.
# TELEFONO_PRUEBA solo se usa en llamadas web del editor (from_number = "web").
telefono_prueba = str(input_data.get("telefono_prueba") or "")
if numero_cliente == "web" and telefono_prueba:
    telefono_e164 = normalizar_telefono(telefono_prueba)
else:
    telefono_e164 = normalizar_telefono(numero_cliente)
puede_whatsapp = whatsapp_posible(telefono_e164)

# Unico destino posible del WhatsApp: el numero desde el que llama (o TELEFONO_PRUEBA en
# llamadas web), y solo si es un movil. Nunca un numero dictado en la llamada (D-004).
telefono_whatsapp = telefono_e164 if puede_whatsapp else ""

# Telefono para buscar la reserva sin pedir datos: va al parametro telefono del MCP Call
# «Check Reimbursement Status». Lo pone el sistema, nunca el modelo (D-006).
telefono_consulta = telefono_para_consulta(numero_cliente, telefono_prueba)

output = {
    "idioma": idioma,
    "idioma_nombre": datos["nombre"],
    "numero_marcado": digitos,
    "numero_cliente": numero_cliente,
    "hora_cet": "%02d:%02d" % (hora_cet, ahora_local.minute),
    "saludo": saludo,
    "fecha_hoy": fecha_hoy,
    "fecha_hoy_iso": fecha_hoy_iso,
    "mensaje_inicial": datos["mensaje"].format(saludo=saludo),
    "recording_id": datos["recording_id"],
    "telefono_e164": telefono_e164,
    "telefono_whatsapp": telefono_whatsapp,
    "whatsapp_posible": puede_whatsapp,
    "telefono_consulta": telefono_consulta,
    "telefono_consultable": bool(telefono_consulta),
}
