# ===============================================================
# RESOLVER COLAS - bot único de Atención España
# ---------------------------------------------------------------
# Se pega tal cual en el nodo Python «Resolver colas» (antes «Resolver colas por idioma» de Minibús ES v25).
# Entradas (input_data): idioma (es | en) y gestion_abierta, las dos salidas de «Contexto de la llamada».
#
# Da, según el idioma, las extensiones de las cuatro colas a las que transfiere el bot. Para cambiar una extensión,
# edita solo el bloque COLAS (y NOMBRES si cambia el nombre en RingCentral); la lógica de abajo no necesita tocarse.
#
#   nueva_reserva   -> reservas nuevas
#   horario_minibus -> horarios de minibús / shuttle
#   gestion_reserva -> cambios, cancelaciones, facturación (solo L-V 08:00-21:00, salvo festivos nacionales)
#   asistencia      -> averías, accidentes (18034 / 18035; los menús automáticos 2114 / 2115 / 2119 no atienden
#                      nadie y la transferencia falla siempre)
#
# - Con Gestión cerrada la extensión de Gestión sale igual que con Gestión abierta: nunca se pone un texto en el
#   lugar de una extensión (con la v25, «NO DISPONIBLE AHORA…» acababa en una transferencia con un número
#   inválido). Quien decide no transferir a Gestión es «Preparar transferencia», que calcula la hora por su cuenta
#   (la del momento en que se ejecuta) y no usa gestion_abierta.
# - No hay cola de fuera de horario: el bot único no reencamina llamadas a un IVR sin agente.
# - Un idioma vacío o no atendido (it, pt, fr…) da las colas en español.
# - Si gestion_abierta no llega, se da por abierta (como la v25), para no bloquear transferencias por un fallo de
#   datos.
# - Los nodos Transfer aceptan la URI SIP completa («sip:18056@hrpbx.buscentauro.com»); los nodos Forward call NO,
#   y piden la extensión pelada. Por eso cada cola sale de las dos formas: cola_<clave> (URI) y cola_<clave>_ext.
# ===============================================================

PBX = "hrpbx.buscentauro.com"

# clave -> {idioma: extensión}
COLAS = {
    "nueva_reserva":   {"es": "18001", "en": "18006"},
    "horario_minibus": {"es": "18056", "en": "18059"},
    "gestion_reserva": {"es": "18057", "en": "18061"},
    "asistencia":      {"es": "18034", "en": "18035"},
}

# clave -> {idioma: nombre legible}. Los de Asistencia son los de 18034 y 18035 en RingCentral
# (docs/extensiones.md), no los de los menús 2114 y 2115.
NOMBRES = {
    "nueva_reserva":   {"es": "CC ES-ES Nueva Reserva", "en": "CC ES-EN Nueva Reserva"},
    "horario_minibus": {"es": "CC ES-ES Hor.MiniBus", "en": "CC ES-EN Hor.MiniBus"},
    "gestion_reserva": {"es": "CC ES-ES Hor.Gestion", "en": "CC ES-EN Hor. Manage Reserv."},
    "asistencia":      {"es": "RA ES-ES AVERÍAS", "en": "RA ES-EN Breakdowns"},
}

# Idioma por defecto si llega vacío o no reconocido
IDIOMA_RESPALDO = "es"


def idioma_de(valor):
    idioma = str(valor or "").strip().lower()
    if any(idioma not in por_idioma for por_idioma in COLAS.values()):
        return IDIOMA_RESPALDO
    return idioma


def es_abierta(valor):
    """gestion_abierta puede llegar como booleano o como texto; si no llega, se da por abierta."""
    if isinstance(valor, bool):
        return valor
    return str(valor).strip().lower() not in ("false", "0", "no")


def resolver(input_data):
    idioma = idioma_de(input_data.get("idioma"))
    output = {
        "idioma_colas": idioma,
        "gestion_abierta": es_abierta(input_data.get("gestion_abierta")),
    }
    # Una URI SIP lista para usar por cada cola, más la extensión pelada y su nombre legible. La extensión de
    # Gestión sale siempre, esté abierta o cerrada.
    for clave, por_idioma in COLAS.items():
        ext = por_idioma[idioma]
        output["cola_" + clave] = "sip:" + ext + "@" + PBX
        output["cola_" + clave + "_ext"] = ext
        output["cola_" + clave + "_nombre"] = NOMBRES[clave][idioma]
    return output


try:
    _entrada = input_data  # noqa: F821 (lo inyecta el nodo Python de HappyRobot)
except NameError:  # importado desde las pruebas locales
    _entrada = None
if _entrada is not None:
    output = resolver(_entrada)
