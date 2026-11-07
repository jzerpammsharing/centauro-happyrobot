# ===============================================================
# PISTA DEL CORREO - bot único de Atención España, módulo Prolongación
# ---------------------------------------------------------------
# Se pega tal cual en el nodo Python «Pista del correo», hijo del MCP Call «Identificar al cliente
# (consultar_reserva)» de la herramienta pista_correo (cuando el cliente no sabe con qué correo está su alquiler).
#
# Entradas (input_data), las del MCP Call:
#   result     lo que devuelve consultar_reserva (dict, JSON en texto o formato de contenido MCP
#              [{type: text, text: "{...}"}])
#   is_error   si el MCP Call ha fallado
#
# Salidas: SOLO estas cuatro claves, y es lo único que ve el agente:
#   verificado   true si consultar_reserva ha encontrado la reserva y ha verificado la identidad
#   dominio      solo el dominio del correo del alquiler (p. ej. gmail.com); vacío si no verifica o si no consta
#   resultado    verificado | no_verificado | dato_no_interpretado | no_disponible
#   detalle      instrucción corta para el agente (sin datos personales)
#
# - Nunca se devuelve ningún otro dato de la reserva (estado, fechas, oficinas, duración, canal, motivo de por qué
#   no verifica...): el nodo construye la salida desde cero con textos fijos y el dominio normalizado. Si no se
#   verifica, el dominio va vacío aunque llegue email_hint.
# - El dominio se normaliza: sin espacios, en minúsculas y, si trae «@», lo que va después de la última «@».
#   Si email_hint no es un texto, no hay dominio.
# - a_dict, texto_error y clasificar_error son una copia de decidir_envio.py de Prolongaciones (un nodo de
#   HappyRobot no puede importar otro fichero). Cambia el dato que se pide repetir según el error: aquí el
#   cliente da número de reserva, nombre y fecha de nacimiento, no el correo.
# ===============================================================
import json

DETALLE_VERIFICADO = (
    'Identidad verificada. Puedes decirle solo el dominio del correo de su alquiler (por ejemplo, "es una '
    'dirección de gmail") y pedirle que te diga el correo completo para enviarle el enlace con '
    "enviar_correo_contrasena. No digas ningún otro dato de la reserva."
)
DETALLE_SIN_DOMINIO = (
    "Identidad verificada, pero no consta el dominio del correo. Pídele el correo que dio en la oficina y usa "
    "enviar_correo_contrasena."
)
DETALLE_NO_VERIFICADO = (
    'Con esos datos no se puede verificar. No digas qué dato falla. Ofrece repetirlos una vez o da las '
    'instrucciones de "¿Has olvidado tu contraseña?" (plan B).'
)
DETALLE_NO_DISPONIBLE = (
    'No se ha podido consultar la reserva ahora: da las instrucciones de "¿Has olvidado tu contraseña?" (plan B).'
)
DETALLE_FECHA = "No se ha podido interpretar la fecha de nacimiento: pide día, mes y año."
DETALLE_RESERVA = "No se ha podido interpretar el número de reserva: pide que lo dicte despacio, cifra a cifra."
DETALLE_NOMBRE = "No se ha podido interpretar el nombre: pide nombre y apellidos completos."
DETALLE_OTRO = "No se ha podido interpretar uno de los datos: pide que lo repita."


def es_verdadero(v):
    return v is True or str(v).strip().lower() in ("true", "1", "si", "yes")


def a_dict(raw):
    if isinstance(raw, dict):
        return raw
    try:
        d = json.loads(str(raw or ""))
    except Exception:
        return None
    if isinstance(d, list) and d and isinstance(d[0], dict):
        # formato de contenido MCP [{type: text, text: "{...}"}]
        try:
            d = json.loads(d[0].get("text") or "")
        except Exception:
            return None
    return d if isinstance(d, dict) else None


def texto_error(raw):
    texto = str(raw or "")
    try:
        d = json.loads(texto)
        if isinstance(d, list) and d and isinstance(d[0], dict):
            texto = str(d[0].get("text") or texto)
    except Exception:
        pass
    return texto.lower()


def clasificar_error(texto):
    """Devuelve (resultado, detalle) a partir del texto de un isError del MCP."""
    if "timeout" in texto or "timed out" in texto:
        return "no_disponible", DETALLE_NO_DISPONIBLE
    if "interpretar" in texto:
        dato = texto.split("interpretar", 1)[1][:40]
        if "fecha" in dato:
            return "dato_no_interpretado", DETALLE_FECHA
        if "reserva" in dato or "número" in dato or "numero" in dato:
            return "dato_no_interpretado", DETALLE_RESERVA
        if "nombre" in dato:
            return "dato_no_interpretado", DETALLE_NOMBRE
        return "dato_no_interpretado", DETALLE_OTRO
    if "falta" in texto:
        # Falta uno de los datos obligatorios: que el cliente lo repita
        return "dato_no_interpretado", DETALLE_OTRO
    return "no_disponible", DETALLE_NO_DISPONIBLE


def normalizar_dominio(hint):
    """Solo el dominio, en minúsculas y sin espacios. Si el hint no es un texto, vacío."""
    if not isinstance(hint, str):
        return ""
    texto = "".join(hint.split()).lower()
    return texto.rsplit("@", 1)[-1]


def salida(verificado, dominio, resultado, detalle):
    return {"verificado": verificado, "dominio": dominio, "resultado": resultado, "detalle": detalle}


def pista(input_data):
    raw = input_data.get("result")
    is_error = es_verdadero(input_data.get("is_error"))
    datos = a_dict(raw)

    if is_error or datos is None:
        resultado, detalle = clasificar_error(texto_error(raw))
        return salida(False, "", resultado, detalle)
    if datos.get("error"):
        return salida(False, "", "no_disponible", DETALLE_NO_DISPONIBLE)
    if not (es_verdadero(datos.get("encontrada")) and es_verdadero(datos.get("verificado"))):
        return salida(False, "", "no_verificado", DETALLE_NO_VERIFICADO)

    dominio = normalizar_dominio(datos.get("email_hint"))
    if not dominio:
        return salida(True, "", "verificado", DETALLE_SIN_DOMINIO)
    return salida(True, dominio, "verificado", DETALLE_VERIFICADO)


try:
    _entrada = input_data  # noqa: F821 (lo inyecta el nodo Python de HappyRobot)
except NameError:  # importado desde las pruebas locales
    _entrada = None
if _entrada is not None:
    output = pista(_entrada)
