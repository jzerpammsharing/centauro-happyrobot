# casos/atencion-es/codigo/test_pista_correo.py
# Ejecutar: python3 -I casos/atencion-es/codigo/test_pista_correo.py
import ast
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pista_correo import pista  # noqa: E402

RUTA_NODO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pista_correo.py")

# Textos fijos que ve el agente (copiados a mano: si cambian en el nodo, esta prueba avisa)
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

CLAVES = {"verificado", "dominio", "resultado", "detalle"}

# Datos inventados de una reserva verificada: nada de esto puede llegar al agente
RESERVA = {
    "encontrada": True,
    "verificado": True,
    "estado": "ESTADO-FICTICIO",
    "fecha_hora_recogida": "2031-01-02T09:15:00",
    "fecha_hora_devolucion": "2031-01-09T18:45:00",
    "oficina_recogida": "OFICINA-RECOGIDA-FICTICIA",
    "oficina_devolucion": "OFICINA-DEVOLUCION-FICTICIA",
    "duracion_dias": 987,
    "canal": "CANAL-FICTICIO",
    "email_hint": "gmail.com",
}
OTROS_VALORES = [
    "ESTADO-FICTICIO", "2031-01-02", "2031-01-09", "09:15", "18:45", "OFICINA-RECOGIDA-FICTICIA",
    "OFICINA-DEVOLUCION-FICTICIA", "987", "CANAL-FICTICIO",
]
NO_VERIFICADO = {"encontrada": True, "verificado": False, "motivo_no_verificado": "MOTIVO-FICTICIO"}
MCP_TEXTO = json.dumps([{"type": "text", "text": json.dumps(RESERVA)}])


def reserva(**cambios):
    return {**RESERVA, **cambios}


CASOS = [
    # (nombre, entrada, verificado, dominio, resultado, detalle)
    ("verificado (dict)", {"result": RESERVA, "is_error": False}, True, "gmail.com", "verificado",
     DETALLE_VERIFICADO),
    ("verificado (texto MCP)", {"result": MCP_TEXTO, "is_error": "false"}, True, "gmail.com", "verificado",
     DETALLE_VERIFICADO),
    ("verificado (JSON suelto)", {"result": json.dumps(RESERVA)}, True, "gmail.com", "verificado",
     DETALLE_VERIFICADO),
    ("verificado, textos 'true' como cadena",
     {"result": reserva(encontrada="true", verificado="True")}, True, "gmail.com", "verificado", DETALLE_VERIFICADO),
    # Normalización del dominio
    ("hint con correo completo", {"result": reserva(email_hint="ana@gmail.com")}, True, "gmail.com", "verificado",
     DETALLE_VERIFICADO),
    ("hint con dos arrobas", {"result": reserva(email_hint="ana@pepe@Hotmail.com")}, True, "hotmail.com",
     "verificado", DETALLE_VERIFICADO),
    ("hint en mayúsculas y con espacios", {"result": reserva(email_hint="  Gmail.COM ")}, True, "gmail.com",
     "verificado", DETALLE_VERIFICADO),
    ("hint con espacios dentro", {"result": reserva(email_hint="gma il. com")}, True, "gmail.com", "verificado",
     DETALLE_VERIFICADO),
    ("hint con correo completo y espacios", {"result": reserva(email_hint=" Ana@Outlook.es ")}, True,
     "outlook.es", "verificado", DETALLE_VERIFICADO),
    # Verificado pero sin dominio útil
    ("hint vacío", {"result": reserva(email_hint="")}, True, "", "verificado", DETALLE_SIN_DOMINIO),
    ("hint solo espacios", {"result": reserva(email_hint="   ")}, True, "", "verificado", DETALLE_SIN_DOMINIO),
    ("hint nulo", {"result": reserva(email_hint=None)}, True, "", "verificado", DETALLE_SIN_DOMINIO),
    ("hint ausente",
     {"result": {k: v for k, v in RESERVA.items() if k != "email_hint"}}, True, "", "verificado",
     DETALLE_SIN_DOMINIO),
    ("hint que acaba en arroba", {"result": reserva(email_hint="ana@")}, True, "", "verificado",
     DETALLE_SIN_DOMINIO),
    ("hint no es texto (dict)", {"result": reserva(email_hint={"dominio": "gmail.com"})}, True, "", "verificado",
     DETALLE_SIN_DOMINIO),
    ("hint no es texto (lista)", {"result": reserva(email_hint=["gmail.com"])}, True, "", "verificado",
     DETALLE_SIN_DOMINIO),
    # No verifica: nunca hay dominio, aunque llegue email_hint
    ("encontrada sin verificar", {"result": NO_VERIFICADO}, False, "", "no_verificado", DETALLE_NO_VERIFICADO),
    ("sin verificar pero con hint", {"result": {**NO_VERIFICADO, "email_hint": "gmail.com"}}, False, "",
     "no_verificado", DETALLE_NO_VERIFICADO),
    ("sin verificar con la reserva entera", {"result": reserva(verificado=False)}, False, "", "no_verificado",
     DETALLE_NO_VERIFICADO),
    ("no encontrada", {"result": {"encontrada": False, "verificado": False}}, False, "", "no_verificado",
     DETALLE_NO_VERIFICADO),
    ("verificado sin encontrada", {"result": reserva(encontrada=False)}, False, "", "no_verificado",
     DETALLE_NO_VERIFICADO),
    ("sin encontrada ni verificado", {"result": {"estado": "ESTADO-FICTICIO", "email_hint": "gmail.com"}}, False,
     "", "no_verificado", DETALLE_NO_VERIFICADO),
    ("no verificado (texto MCP)",
     {"result": json.dumps([{"type": "text", "text": json.dumps(NO_VERIFICADO)}]), "is_error": "false"}, False, "",
     "no_verificado", DETALLE_NO_VERIFICADO),
    # Errores del MCP
    ("timeout", {"result": "timeout", "is_error": True}, False, "", "no_disponible", DETALLE_NO_DISPONIBLE),
    ("timed out (texto MCP)",
     {"result": json.dumps([{"type": "text", "text": "Request timed out"}]), "is_error": True}, False, "",
     "no_disponible", DETALLE_NO_DISPONIBLE),
    ("error en el JSON", {"result": {"error": "servicio_no_disponible"}}, False, "", "no_disponible",
     DETALLE_NO_DISPONIBLE),
    ("error en el JSON con reserva dentro", {"result": reserva(error="servicio_no_disponible")}, False, "",
     "no_disponible", DETALLE_NO_DISPONIBLE),
    ("validación pydantic", {"result": "1 validation error ... Field required", "is_error": True}, False, "",
     "no_disponible", DETALLE_NO_DISPONIBLE),
    ("respuesta vacía", {"result": "", "is_error": False}, False, "", "no_disponible", DETALLE_NO_DISPONIBLE),
    ("sin result", {}, False, "", "no_disponible", DETALLE_NO_DISPONIBLE),
    ("result nulo", {"result": None, "is_error": None}, False, "", "no_disponible", DETALLE_NO_DISPONIBLE),
    ("texto que no es JSON", {"result": "Internal Server Error", "is_error": False}, False, "", "no_disponible",
     DETALLE_NO_DISPONIBLE),
    ("is_error con un JSON que parece verificado", {"result": RESERVA, "is_error": True}, False, "",
     "no_disponible", DETALLE_NO_DISPONIBLE),
    # Datos que el MCP no ha podido interpretar
    ("fecha ilegible", {"result": "No se ha podido interpretar la fecha de nacimiento", "is_error": True}, False,
     "", "dato_no_interpretado", DETALLE_FECHA),
    ("fecha ilegible (texto MCP)",
     {"result": json.dumps([{"type": "text", "text": "No se ha podido interpretar la fecha. Pide día, mes y año."}]),
      "is_error": "true"}, False, "", "dato_no_interpretado", DETALLE_FECHA),
    ("reserva ilegible", {"result": "No se ha podido interpretar el número de reserva", "is_error": True}, False,
     "", "dato_no_interpretado", DETALLE_RESERVA),
    ("nombre ilegible", {"result": "No se ha podido interpretar el nombre completo", "is_error": True}, False, "",
     "dato_no_interpretado", DETALLE_NOMBRE),
    ("dato ilegible sin identificar", {"result": "No se ha podido interpretar la entrada", "is_error": True}, False,
     "", "dato_no_interpretado", DETALLE_OTRO),
    ("falta un dato", {"result": "Falta un dato obligatorio", "is_error": True}, False, "",
     "dato_no_interpretado", DETALLE_OTRO),
]

fallos = 0
for nombre, entrada, verificado, dominio, res, detalle in CASOS:
    out = pista(entrada)
    if (
        set(out) != CLAVES
        or out["verificado"] is not verificado
        or out["dominio"] != dominio
        or out["resultado"] != res
        or out["detalle"] != detalle
    ):
        fallos += 1
        print("FALLO [%s]: %r" % (nombre, out))

# Lo ÚNICO que ve el agente: exactamente cuatro claves y ningún otro dato de la reserva en ningún sitio
total = len(CASOS)
for nombre, entrada in (
    ("reserva verificada (dict)", {"result": RESERVA}),
    ("reserva verificada (texto MCP)", {"result": MCP_TEXTO, "is_error": False}),
    ("reserva sin verificar", {"result": reserva(verificado=False)}),
    ("reserva con error", {"result": reserva(error="x")}),
    ("reserva con is_error", {"result": RESERVA, "is_error": True}),
):
    total += 1
    out = pista(entrada)
    volcado = json.dumps(out, ensure_ascii=False)
    filtrados = [v for v in OTROS_VALORES if v in volcado]
    if set(out) != CLAVES or filtrados:
        fallos += 1
        print("FALLO fuga [%s]: claves %r, se cuelan %r" % (nombre, sorted(out), filtrados))

# Cuando no verifica, ni el motivo ni el dominio llegan al agente; el detalle no dice qué dato falla
for nombre, entrada, prohibidos in (
    ("motivo ficticio", {"result": NO_VERIFICADO}, ["MOTIVO-FICTICIO"]),
    ("motivo fecha", {"result": {**NO_VERIFICADO, "motivo_no_verificado": "fecha", "email_hint": "gmail.com"}},
     ["fecha", "nombre", "gmail", "motivo"]),
    ("motivo nombre", {"result": {**NO_VERIFICADO, "motivo_no_verificado": "nombre", "email_hint": "gmail.com"}},
     ["fecha", "nombre", "gmail", "motivo"]),
):
    total += 1
    volcado = json.dumps(pista(entrada), ensure_ascii=False).lower()
    filtrados = [p for p in prohibidos if p.lower() in volcado]
    if filtrados:
        fallos += 1
        print("FALLO no verificado [%s]: se cuela %r" % (nombre, filtrados))

# La entrada no se modifica
total += 1
entrada = {"result": dict(RESERVA), "is_error": False}
copia = json.loads(json.dumps(entrada))
pista(entrada)
if entrada != copia:
    fallos += 1
    print("FALLO: la función ha modificado la entrada")

# El nodo de HappyRobot no puede importar otros ficheros: solo biblioteca estándar y nada de decidir_envio
total += 1
with open(RUTA_NODO, encoding="utf-8") as f:
    codigo = f.read()
importados = set()
for nodo in ast.walk(ast.parse(codigo)):
    if isinstance(nodo, ast.Import):
        importados |= {a.name.split(".")[0] for a in nodo.names}
    elif isinstance(nodo, ast.ImportFrom):
        importados.add((nodo.module or "").split(".")[0])
if importados - {"json"}:
    fallos += 1
    print("FALLO imports: el nodo importa %r, solo puede usar json" % sorted(importados))

# Como lo ejecuta el nodo: input_data ya definido y el resultado en `output`
total += 1
espacio = {"input_data": {"result": MCP_TEXTO, "is_error": False}}
exec(compile(codigo, RUTA_NODO, "exec"), espacio)
salida = espacio.get("output")
if (
    not isinstance(salida, dict)
    or set(salida) != CLAVES
    or salida["verificado"] is not True
    or salida["dominio"] != "gmail.com"
    or salida["resultado"] != "verificado"
):
    fallos += 1
    print("FALLO ejecución como nodo: %r" % salida)

print("%d/%d casos correctos" % (total - fallos, total))
sys.exit(1 if fallos else 0)
