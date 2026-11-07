# casos/reembolsos/codigo/test_filtrar_respuesta_verificada.py
# Ejecutar: python3 -I casos/reembolsos/codigo/test_filtrar_respuesta_verificada.py
# Datos inventados. Los textos de error son los del MCP (centauro-mcp, tools/_pipeline.py, 21/10/2026).
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from filtrar_respuesta_verificada import (  # noqa: E402
    DETALLE_DNI, DETALLE_EMAIL, DETALLE_FALTA, DETALLE_FECHA, DETALLE_NO_DISPONIBLE, DETALLE_RESERVA, filtrar,
)

MSG_FALTA = ("Falta numero_reserva, email o dni: se necesita al menos uno. Pide al cliente el número de reserva "
             "(bono) y, si no lo tiene, el email con el que hizo la reserva o su DNI/NIE.")
MSG_RESERVA = "No se ha podido interpretar el número de reserva. Pide al cliente que lo repita despacio, carácter a carácter."
MSG_EMAIL = "No se ha podido interpretar el email. Pide al cliente que lo deletree despacio."
MSG_DNI = ("No se ha podido interpretar el DNI/NIE o su letra no es válida. Pide al cliente que lo repita cifra a "
           "cifra, con la letra al final.")
MSG_FECHA = "No se ha podido interpretar fecha_nacimiento. Pide al cliente día, mes y año de nacimiento."
MSG_DNI_NO_DISPONIBLE = ("La búsqueda por DNI no está disponible. Pide al cliente el número de reserva (bono): aparece "
                         "en el email de confirmación de la reserva.")

VERIFICADA = {
    "encontrada": True, "verificado": True, "hoy": "2026-10-21", "estado_alquiler": "cerrado",
    "fecha_cierre": "2026-10-14", "dias_desde_cierre": 7, "oficina_devolucion": "Alicante Aeropuerto",
    "pais": "ES", "pago": {"metodo": "tarjeta"},
    "combustible": {"deposito_cobrado": 80.0, "reembolso": {"emitido": True, "fecha_limite": "2026-10-26"}},
    "fianza": None, "via_verde": {"aplica": False}, "cargos_posteriores": [],
    "reclamacion_abierta": {"existe": False}, "factura_disponible": True,
    "numero_reserva": "ER00000001", "tiene_cuenta": False,
    "otras_reservas": [
        {"numero_reserva": "ER00000002", "estado": "cerrado", "oficina_recogida": "Madrid Aeropuerto",
         "oficina_devolucion": "Madrid Aeropuerto", "fecha_recogida": "2026-09-01",
         "fecha_devolucion": "2026-09-05", "titular": "Prueba Prueba"},
    ],
    # Campos que no deben llegar nunca al agente
    "nombre_titular": "Prueba Prueba", "email": "prueba.prueba@example.com", "dni": "00000000T",
    "fecha_nacimiento": "03/03/1990",
}

fallos = 0


def comprobar(nombre, entrada, esperado, extra=None):
    global fallos
    salida = filtrar(entrada)
    malos = {k: (salida.get(k), v) for k, v in esperado.items() if salida.get(k) != v}
    if extra:
        error_extra = extra(salida)
        if error_extra:
            malos["extra"] = error_extra
    if malos:
        fallos += 1
        print("FALLO %s: %r" % (nombre, malos))


def error_mcp(texto, **solicitado):
    entrada = {"result": json.dumps([{"type": "text", "text": texto}]), "is_error": "true"}
    entrada.update(solicitado)
    return entrada


# Errores del MCP: un caso por cada mensaje
comprobar("falta, primer intento por teléfono (web u oculto)", error_mcp(MSG_FALTA),
          {"error": "dato_no_interpretado", "detalle_error": DETALLE_FALTA,
           "consulta_por_telefono": True, "cuenta_en_limite": False})
comprobar("número ilegible", error_mcp(MSG_RESERVA, numero_reserva_solicitado="ER1"),
          {"error": "dato_no_interpretado", "detalle_error": DETALLE_RESERVA,
           "consulta_por_telefono": False, "cuenta_en_limite": True})
comprobar("email ilegible", error_mcp(MSG_EMAIL, email_solicitado="prueba arroba"),
          {"error": "dato_no_interpretado", "detalle_error": DETALLE_EMAIL, "consulta_por_telefono": False})
comprobar("DNI ilegible", error_mcp(MSG_DNI, dni_solicitado="0000000"),
          {"error": "dato_no_interpretado", "detalle_error": DETALLE_DNI, "consulta_por_telefono": False})
comprobar("fecha ilegible", error_mcp(MSG_FECHA),
          {"error": "dato_no_interpretado", "detalle_error": DETALLE_FECHA, "cuenta_en_limite": True})
comprobar("DNI no disponible", error_mcp(MSG_DNI_NO_DISPONIBLE, dni_solicitado="00000000T"),
          {"error": "dato_no_interpretado", "detalle_error": DETALLE_NO_DISPONIBLE})
comprobar("timeout", {"result": json.dumps({"encontrada": False, "error": "timeout"}), "is_error": "false"},
          {"error": "timeout", "verificado": False, "datos_reserva": ""})
comprobar("texto sin formato", {"result": "timed out", "is_error": True}, {"error": "timeout"})

# No encontrada y no verificada
comprobar("no encontrada por teléfono", {"result": json.dumps({"encontrada": False}), "is_error": "false"},
          {"encontrada": False, "verificado": False, "error": "", "consulta_por_telefono": True,
           "cuenta_en_limite": True, "datos_reserva": ""})
comprobar("verificado false",
          {"result": json.dumps({"encontrada": True, "verificado": False, "motivo_no_verificado": "nombre",
                                 "oficina_devolucion": "Alicante"}),
           "is_error": "false", "numero_reserva_solicitado": "ER00000000"},
          {"encontrada": True, "verificado": False, "motivo_no_verificado": "nombre", "datos_reserva": "",
           "numero_reserva_verificado": "", "consulta_por_telefono": False})


# Verificada: lista blanca, campos nuevos y nada personal
def sin_datos_personales(salida):
    texto = json.dumps(salida, ensure_ascii=False)
    for prohibido in ("Prueba Prueba", "prueba.prueba@example.com", "00000000T", "03/03/1990", "fecha_limite",
                      "titular"):
        if prohibido in texto:
            return "aparece %r" % prohibido
    datos = json.loads(salida["datos_reserva"])
    if datos.get("tiene_cuenta") is not False:
        return "falta tiene_cuenta"
    if datos.get("numero_reserva") != "ER00000001":
        return "falta numero_reserva"
    otras = datos.get("otras_reservas") or []
    if len(otras) != 1 or set(otras[0]) != {"numero_reserva", "estado", "oficina_recogida", "oficina_devolucion",
                                            "fecha_recogida", "fecha_devolucion"}:
        return "otras_reservas mal: %r" % otras
    return ""


comprobar("verificada por teléfono", {"result": json.dumps(VERIFICADA), "is_error": "false"},
          {"verificado": True, "error": "", "numero_reserva_verificado": "ER00000001",
           "consulta_por_telefono": True, "cuenta_en_limite": True}, extra=sin_datos_personales)
comprobar("verificada, formato de contenido MCP",
          {"result": json.dumps([{"type": "text", "text": json.dumps(VERIFICADA)}]), "is_error": "false",
           "email_solicitado": "prueba.prueba@example.com"},
          {"verificado": True, "consulta_por_telefono": False}, extra=sin_datos_personales)
comprobar("otras_reservas que no es una lista",
          {"result": json.dumps(dict(VERIFICADA, otras_reservas="x")), "is_error": "false"},
          {"verificado": True},
          extra=lambda s: "" if json.loads(s["datos_reserva"])["otras_reservas"] == [] else "no se vacía")

print("OK" if fallos == 0 else "%d fallos" % fallos)
sys.exit(1 if fallos else 0)
