import json
import re

# ===============================================================
# FILTRAR RESPUESTA VERIFICADA - consultar_reembolso
# (copia exacta del nodo de W1 desde la v10; si se cambia aquí, se pega allí)
# ---------------------------------------------------------------
# Lo UNICO que ve el agente es la salida de este nodo.
# - verificado false / no encontrada: solo flags y motivo_no_verificado.
# - verificado true: solo los campos del contrato (lista blanca), mas
#   numero_reserva, tiene_cuenta y otras_reservas (busqueda v2 del MCP).
# - error: error normalizado, sin datos.
# - Se eliminan las fechas futuras (fecha_limite) a cualquier nivel:
#   el agente no da fechas futuras concretas, solo plazos en dias.
# - Identificacion: numero de reserva, email o DNI/NIE (prioridad en ese
#   orden) y, si no hay ninguno, el telefono desde el que llama (lo pone el
#   sistema en el MCP Call, nunca el modelo).
# ===============================================================

CAMPOS_VERIFICADOS = [
    "hoy", "estado_alquiler", "fecha_cierre", "dias_desde_cierre",
    "oficina_devolucion", "pais", "pago", "combustible", "fianza",
    "via_verde", "cancelacion", "cargos_posteriores",
    "reclamacion_abierta", "factura_disponible",
    # campos de plazo a nivel raiz, si el servidor los envia
    "dentro_de_plazo", "emision_retrasada",
    # busqueda v2: reserva elegida, acceso al area de cliente y otras reservas del cliente
    "numero_reserva", "tiene_cuenta", "otras_reservas",
]

# De cada reserva de otras_reservas solo pasan estos campos (sin datos personales)
CAMPOS_OTRA_RESERVA = (
    "numero_reserva", "estado", "oficina_recogida", "oficina_devolucion",
    "fecha_recogida", "fecha_devolucion",
)

CAMPOS_EXCLUIDOS = ("fecha_limite",)

DETALLE_FALTA = (
    "Falta el identificador: pide el numero de reserva; si no lo tiene, el email con el que "
    "hizo la reserva; y si tampoco, su DNI o NIE."
)
DETALLE_FECHA = "No se ha podido interpretar la fecha de nacimiento: pide dia, mes y año."
DETALLE_RESERVA = "No se ha podido interpretar el numero de reserva: pide que lo repita."
DETALLE_EMAIL = "No se ha podido interpretar el email: pide al cliente que lo deletree despacio."
DETALLE_DNI = (
    "No se ha podido interpretar el DNI o NIE, o su letra no es valida: pide al cliente que "
    "lo repita cifra a cifra, con la letra al final."
)
DETALLE_NO_DISPONIBLE = (
    "Esa busqueda no esta disponible ahora: pide el numero de reserva, que aparece en el "
    "correo de confirmacion."
)
DETALLE_OTRO = "No se ha podido interpretar uno de los datos: pide que lo repita."


def es_verdadero(v):
    return v is True or str(v).strip().lower() in ("true", "1", "si", "yes")


def sin_fechas_futuras(v):
    if isinstance(v, dict):
        return {k: sin_fechas_futuras(x) for k, x in v.items() if k not in CAMPOS_EXCLUIDOS}
    if isinstance(v, list):
        return [sin_fechas_futuras(x) for x in v]
    return v


def limpiar_otras_reservas(v):
    if not isinstance(v, list):
        return []
    return [{k: o[k] for k in CAMPOS_OTRA_RESERVA if k in o} for o in v if isinstance(o, dict)]


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


def clasificar_error_texto(texto):
    """Devuelve (error, detalle) a partir del texto de un isError del MCP."""
    if "timeout" in texto or "timed out" in texto:
        return "timeout", ""
    if "no esta disponible" in texto or "no está disponible" in texto:
        return "dato_no_interpretado", DETALLE_NO_DISPONIBLE
    if "falta" in texto or "por email no" in texto:
        return "dato_no_interpretado", DETALLE_FALTA
    if "interpretar" in texto:
        # Mira que dato dice el mensaje justo despues de "interpretar".
        dato = texto.split("interpretar", 1)[1][:40]
        if "fecha" in dato:
            return "dato_no_interpretado", DETALLE_FECHA
        if "email" in dato or "correo" in dato:
            return "dato_no_interpretado", DETALLE_EMAIL
        if re.search(r"\b(dni|nie)\b", dato):
            return "dato_no_interpretado", DETALLE_DNI
        if "mero" in dato or "reserva" in dato:
            return "dato_no_interpretado", DETALLE_RESERVA
        return "dato_no_interpretado", DETALLE_OTRO
    return "servicio_no_disponible", ""


def filtrar(input_data):
    raw = input_data.get("result")
    is_error = es_verdadero(input_data.get("is_error"))
    datos = a_dict(raw)

    # Consulta sin numero de reserva, email ni DNI: el MCP busca por el telefono desde el que llama
    por_telefono = not any(
        str(input_data.get(k) or "").strip()
        for k in ("numero_reserva_solicitado", "email_solicitado", "dni_solicitado")
    )

    encontrada = False
    verificado = False
    motivo = ""
    error = ""
    detalle = ""
    datos_reserva = {}

    if is_error or datos is None:
        texto = str(raw or "")
        try:
            d = json.loads(texto)
            if isinstance(d, list) and d and isinstance(d[0], dict):
                texto = str(d[0].get("text") or texto)
        except Exception:
            pass
        error, detalle = clasificar_error_texto(texto.lower())
    else:
        err = str(datos.get("error") or "")
        if err:
            error = err if err in ("timeout", "servicio_no_disponible") else "servicio_no_disponible"
        encontrada = es_verdadero(datos.get("encontrada"))
        verificado = encontrada and es_verdadero(datos.get("verificado"))
        if encontrada and not verificado:
            m = str(datos.get("motivo_no_verificado") or "")
            motivo = m if m in ("nombre", "fecha", "ambos") else "ambos"
        if verificado and not error:
            for k in CAMPOS_VERIFICADOS:
                if k in datos:
                    datos_reserva[k] = sin_fechas_futuras(datos[k])
            if "otras_reservas" in datos_reserva:
                datos_reserva["otras_reservas"] = limpiar_otras_reservas(datos_reserva["otras_reservas"])

    numero_verificado = ""
    if datos_reserva:
        numero_verificado = str(datos.get("numero_reserva") or input_data.get("numero_reserva_solicitado") or "").strip()

    # El primer intento por telefono que no se ha podido hacer (llamada web, numero oculto) no cuenta
    cuenta_en_limite = not (por_telefono and detalle == DETALLE_FALTA)

    return {
        "encontrada": encontrada,
        "verificado": verificado,
        "motivo_no_verificado": motivo,
        "error": error,
        "detalle_error": detalle,
        # Solo tiene contenido si verificado es true
        "datos_reserva": json.dumps(datos_reserva, ensure_ascii=False) if datos_reserva else "",
        "numero_reserva_verificado": numero_verificado,
        "consulta_por_telefono": por_telefono,
        "cuenta_en_limite": cuenta_en_limite,
    }


try:
    _entrada = input_data  # noqa: F821 (lo inyecta el nodo Python de HappyRobot)
except NameError:  # importado desde las pruebas locales
    _entrada = None
if _entrada is not None:
    output = filtrar(_entrada)
