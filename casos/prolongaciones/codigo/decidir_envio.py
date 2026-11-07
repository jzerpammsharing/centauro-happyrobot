# ===============================================================
# DECIDIR ENVÍO - herramienta enviar_correo_contrasena (Prolongaciones v12)
# ---------------------------------------------------------------
# Se pega tal cual en el nodo Python «Decidir envío», hijo del MCP Call
# «Comprobar correo (consultar_reserva)».
#
# - El correo «coincide» si consultar_reserva, buscando por el email que dictó
#   el cliente, encuentra una reserva y verifica nombre y fecha de nacimiento.
# - Solo entonces email_envio lleva el email. Si no coincide, email_envio va
#   vacío: HappyRobot no manda el argumento y el MCP rechaza el envío
#   («email Field required»), así que no sale ningún correo.
# - Nunca se devuelve ningún dato de la reserva.
# ===============================================================
import json

DETALLE_EMAIL = "No se ha podido interpretar el email: pide al cliente que lo deletree despacio."
DETALLE_FECHA = "No se ha podido interpretar la fecha de nacimiento: pide día, mes y año."
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
    """Devuelve (estado, detalle) a partir del texto de un isError del MCP."""
    if "timeout" in texto or "timed out" in texto:
        return "no_disponible", ""
    if "interpretar" in texto:
        dato = texto.split("interpretar", 1)[1][:40]
        if "fecha" in dato:
            return "dato_no_interpretado", DETALLE_FECHA
        if "email" in dato or "correo" in dato:
            return "dato_no_interpretado", DETALLE_EMAIL
        return "dato_no_interpretado", DETALLE_OTRO
    if "falta" in texto:
        # Con el email relleno no debería pasar: lo tratamos como email ilegible.
        return "dato_no_interpretado", DETALLE_EMAIL
    return "no_disponible", ""


def decidir(input_data):
    email = str(input_data.get("email") or "").strip()
    raw = input_data.get("result")
    is_error = es_verdadero(input_data.get("is_error"))
    datos = a_dict(raw)

    estado = "no_coincide"
    detalle = ""
    if not email:
        estado, detalle = "dato_no_interpretado", DETALLE_EMAIL
    elif is_error or datos is None:
        estado, detalle = clasificar_error(texto_error(raw))
    elif datos.get("error"):
        estado = "no_disponible"
    elif es_verdadero(datos.get("encontrada")) and es_verdadero(datos.get("verificado")):
        estado = "coincide"

    coincide = estado == "coincide"
    return {
        "coincide": coincide,
        "email_envio": email if coincide else "",
        "estado": estado,
        "detalle": detalle,
    }


try:
    _entrada = input_data  # noqa: F821 (lo inyecta el nodo Python de HappyRobot)
except NameError:  # importado desde las pruebas locales
    _entrada = None
if _entrada is not None:
    output = decidir(_entrada)
