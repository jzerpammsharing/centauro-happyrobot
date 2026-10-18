# casos/prolongaciones/codigo/test_correo_contrasena.py
# Ejecutar: python3 -I casos/prolongaciones/codigo/test_correo_contrasena.py
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decidir_envio import decidir  # noqa: E402
from resultado_envio import resultado  # noqa: E402

EMAIL = "prueba.prueba@example.com"
VERIFICADO = {"encontrada": True, "verificado": True, "estado_alquiler": "en_curso"}
MCP_TEXTO = json.dumps([{"type": "text", "text": json.dumps(VERIFICADO)}])
INTERPRETAR_EMAIL = "No se ha podido interpretar el email. Pide al cliente que lo deletree."

CASOS_DECIDIR = [
    # (nombre, entrada, estado, email_envio)
    ("verificado (dict)", {"email": EMAIL, "result": VERIFICADO, "is_error": False}, "coincide", EMAIL),
    ("verificado (texto MCP)", {"email": EMAIL, "result": MCP_TEXTO, "is_error": "false"}, "coincide", EMAIL),
    ("email con espacios", {"email": "  " + EMAIL + " ", "result": VERIFICADO}, "coincide", EMAIL),
    ("no encontrada", {"email": EMAIL, "result": {"encontrada": False, "verificado": False}}, "no_coincide", ""),
    ("encontrada sin verificar", {"email": EMAIL, "result": {"encontrada": True, "verificado": False,
                                                             "motivo_no_verificado": "fecha"}}, "no_coincide", ""),
    ("verificado sin encontrada", {"email": EMAIL, "result": {"encontrada": False, "verificado": True}}, "no_coincide", ""),
    ("email ilegible", {"email": EMAIL, "result": INTERPRETAR_EMAIL, "is_error": True}, "dato_no_interpretado", ""),
    ("fecha ilegible", {"email": EMAIL, "result": "No se ha podido interpretar la fecha de nacimiento",
                        "is_error": True}, "dato_no_interpretado", ""),
    ("timeout", {"email": EMAIL, "result": "timeout", "is_error": True}, "no_disponible", ""),
    ("error en el JSON", {"email": EMAIL, "result": {"error": "servicio_no_disponible"}}, "no_disponible", ""),
    ("validación pydantic", {"email": EMAIL, "result": "1 validation error ... Field required", "is_error": True},
     "no_disponible", ""),
    ("respuesta vacía", {"email": EMAIL, "result": "", "is_error": False}, "no_disponible", ""),
    ("sin email", {"email": "", "result": VERIFICADO}, "dato_no_interpretado", ""),
]

CASOS_RESULTADO = [
    # (nombre, entrada, resultado, enviado)
    ("enviado", {"estado": "coincide", "reset_result": {"ok": True}, "reset_is_error": False}, "enviado", True),
    ("enviado (texto MCP)", {"estado": "coincide", "reset_result": json.dumps([{"type": "text", "text": "{\"ok\": true}"}]),
                             "reset_is_error": "false"}, "enviado", True),
    ("coincide pero el reset falla", {"estado": "coincide", "reset_result": "timeout", "reset_is_error": True},
     "no_disponible", False),
    ("coincide pero ok false", {"estado": "coincide", "reset_result": {"ok": False}}, "no_disponible", False),
    ("no coincide", {"estado": "no_coincide", "reset_result": "email Field required", "reset_is_error": True},
     "no_coincide", False),
    ("dato no interpretado", {"estado": "dato_no_interpretado", "detalle": "pide que lo deletree"},
     "dato_no_interpretado", False),
    ("no disponible", {"estado": "no_disponible"}, "no_disponible", False),
    ("sin estado", {}, "no_disponible", False),
]

fallos = 0
for nombre, entrada, estado, email_envio in CASOS_DECIDIR:
    out = decidir(entrada)
    if out["estado"] != estado or out["email_envio"] != email_envio or out["coincide"] != (estado == "coincide"):
        fallos += 1
        print("FALLO decidir [%s]: %r" % (nombre, out))
for nombre, entrada, res, enviado in CASOS_RESULTADO:
    out = resultado(entrada)
    if out["resultado"] != res or out["enviado"] != enviado or EMAIL in json.dumps(out):
        fallos += 1
        print("FALLO resultado [%s]: %r" % (nombre, out))

total = len(CASOS_DECIDIR) + len(CASOS_RESULTADO)
print("%d/%d casos correctos" % (total - fallos, total))
sys.exit(1 if fallos else 0)
