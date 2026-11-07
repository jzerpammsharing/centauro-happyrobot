# ===============================================================
# RESULTADO PARA EL AGENTE - herramienta enviar_correo_contrasena (Prolongaciones v12)
# ---------------------------------------------------------------
# Se pega tal cual en el nodo Python «Resultado para el agente», el último de
# la herramienta. Lo ÚNICO que ve el agente es la salida de este nodo:
#   resultado = enviado | no_coincide | dato_no_interpretado | no_disponible
#   enviado   = true solo si el MCP ha cursado el envío
#   detalle   = instrucción corta para el agente (sin datos personales)
# ===============================================================
import json

DETALLE_ENVIADO = (
    "Correo enviado. Di que ya se lo has enviado, que el correo dice «restablecer contraseña» "
    "pero sirve para crearla, y pregunta si le ha llegado."
)
DETALLE_NO_COINCIDE = (
    "No coincide: no se ha enviado nada. Sigue ENVÍO DEL CORREO DE CONTRASEÑA, caso «No coincide»."
)
DETALLE_NO_DISPONIBLE = (
    "No se ha podido enviar ahora: da las instrucciones de «¿Has olvidado tu contraseña?» (plan B)."
)


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
        try:
            d = json.loads(d[0].get("text") or "")
        except Exception:
            return None
    return d if isinstance(d, dict) else None


def resultado(input_data):
    estado = str(input_data.get("estado") or "").strip()
    if estado != "coincide":
        if estado == "dato_no_interpretado":
            detalle = str(input_data.get("detalle") or "") or "No se ha podido interpretar un dato: pide que lo repita."
            return {"resultado": "dato_no_interpretado", "enviado": False, "detalle": detalle}
        if estado == "no_coincide":
            return {"resultado": "no_coincide", "enviado": False, "detalle": DETALLE_NO_COINCIDE}
        return {"resultado": "no_disponible", "enviado": False, "detalle": DETALLE_NO_DISPONIBLE}

    datos = a_dict(input_data.get("reset_result"))
    ok = (
        not es_verdadero(input_data.get("reset_is_error"))
        and datos is not None
        and es_verdadero(datos.get("ok"))
    )
    if ok:
        return {"resultado": "enviado", "enviado": True, "detalle": DETALLE_ENVIADO}
    return {"resultado": "no_disponible", "enviado": False, "detalle": DETALLE_NO_DISPONIBLE}


try:
    _entrada = input_data  # noqa: F821 (lo inyecta el nodo Python de HappyRobot)
except NameError:  # importado desde las pruebas locales
    _entrada = None
if _entrada is not None:
    output = resultado(_entrada)
