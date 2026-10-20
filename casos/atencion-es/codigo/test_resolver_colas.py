# casos/atencion-es/codigo/test_resolver_colas.py
# Ejecutar: python3 -I casos/atencion-es/codigo/test_resolver_colas.py
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from resolver_colas import COLAS, resolver  # noqa: E402

PBX = "hrpbx.buscentauro.com"
CLAVES = ("nueva_reserva", "horario_minibus", "gestion_reserva", "asistencia")

# Extensiones por idioma (docs/extensiones.md): ningún valor es un menú automático (2114, 2115, 2119)
EXT_ES = {"nueva_reserva": "18001", "horario_minibus": "18056", "gestion_reserva": "18057", "asistencia": "18034"}
EXT_EN = {"nueva_reserva": "18006", "horario_minibus": "18059", "gestion_reserva": "18061", "asistencia": "18035"}
PROHIBIDAS = ("2114", "2115", "2119")


def sip(ext):
    return "sip:%s@%s" % (ext, PBX)


# Todas las salidas del nodo: idioma_colas, gestion_abierta y tres por cola
SALIDAS = {"idioma_colas", "gestion_abierta"}
for _clave in CLAVES:
    SALIDAS |= {"cola_" + _clave, "cola_" + _clave + "_ext", "cola_" + _clave + "_nombre"}

CASOS = [
    # (nombre, input_data, comprobaciones)
    ("inglés: Gestión es la 18061", {"idioma": "en", "gestion_abierta": True},
     {"idioma_colas": "en", "cola_gestion_reserva": sip("18061"), "cola_gestion_reserva_ext": "18061"}),
    ("español: Gestión es la 18057", {"idioma": "es", "gestion_abierta": True},
     {"idioma_colas": "es", "cola_gestion_reserva": sip("18057"), "cola_gestion_reserva_ext": "18057"}),
    ("italiano cae en español y Asistencia es la 18034", {"idioma": "it", "gestion_abierta": True},
     {"idioma_colas": "es", "cola_asistencia_ext": "18034", "cola_asistencia": sip("18034")}),
    ("portugués cae en español", {"idioma": "pt"}, {"idioma_colas": "es"}),
    ("francés cae en español", {"idioma": "fr"}, {"idioma_colas": "es"}),
    ("idioma vacío cae en español", {"idioma": "", "gestion_abierta": True}, {"idioma_colas": "es"}),
    ("idioma ausente cae en español", {"gestion_abierta": True}, {"idioma_colas": "es"}),
    ("idioma None cae en español", {"idioma": None, "gestion_abierta": True}, {"idioma_colas": "es"}),
    ("idioma que no es texto cae en español", {"idioma": 5, "gestion_abierta": True}, {"idioma_colas": "es"}),
    ("idioma con mayúsculas y espacios", {"idioma": " EN ", "gestion_abierta": True},
     {"idioma_colas": "en", "cola_nueva_reserva_ext": "18006"}),
    # Gestión cerrada: la extensión sale igual, el texto nunca sustituye a la extensión
    ("Gestión cerrada en español: la extensión sale igual", {"idioma": "es", "gestion_abierta": False},
     {"gestion_abierta": False, "cola_gestion_reserva": sip("18057"), "cola_gestion_reserva_ext": "18057"}),
    ("Gestión cerrada en inglés: la extensión sale igual", {"idioma": "en", "gestion_abierta": False},
     {"gestion_abierta": False, "cola_gestion_reserva": sip("18061"), "cola_gestion_reserva_ext": "18061"}),
    ("Gestión cerrada no toca las demás colas", {"idioma": "es", "gestion_abierta": False},
     {"cola_nueva_reserva": sip("18001"), "cola_horario_minibus": sip("18056"), "cola_asistencia": sip("18034")}),
    # Nombres de Asistencia: los de 18034 y 18035, no los de los menús 2114 y 2115
    ("nombre de Asistencia en español", {"idioma": "es"}, {"cola_asistencia_nombre": "RA ES-ES AVERÍAS"}),
    ("nombre de Asistencia en inglés", {"idioma": "en"}, {"cola_asistencia_nombre": "RA ES-EN Breakdowns"}),
    # gestion_abierta puede llegar como booleano o texto; si no llega, abierta (como la v25)
    ("gestion_abierta ausente se da por abierta", {"idioma": "es"}, {"gestion_abierta": True}),
    ("gestion_abierta None se da por abierta", {"idioma": "es", "gestion_abierta": None}, {"gestion_abierta": True}),
    ("gestion_abierta vacía se da por abierta", {"idioma": "es", "gestion_abierta": ""}, {"gestion_abierta": True}),
    ("gestion_abierta True", {"idioma": "es", "gestion_abierta": True}, {"gestion_abierta": True}),
    ("gestion_abierta False", {"idioma": "es", "gestion_abierta": False}, {"gestion_abierta": False}),
    ("gestion_abierta «false»", {"idioma": "es", "gestion_abierta": "false"}, {"gestion_abierta": False}),
    ("gestion_abierta «False» con espacios", {"idioma": "es", "gestion_abierta": " False "},
     {"gestion_abierta": False}),
    ("gestion_abierta «0»", {"idioma": "es", "gestion_abierta": "0"}, {"gestion_abierta": False}),
    ("gestion_abierta «no»", {"idioma": "es", "gestion_abierta": "no"}, {"gestion_abierta": False}),
    ("gestion_abierta «true»", {"idioma": "es", "gestion_abierta": "true"}, {"gestion_abierta": True}),
    ("gestion_abierta «1»", {"idioma": "es", "gestion_abierta": "1"}, {"gestion_abierta": True}),
]

fallos = 0
total = 0

for nombre, entrada, esperado in CASOS:
    total += 1
    out = resolver(entrada)
    malos = {k: (out.get(k), v) for k, v in esperado.items() if out.get(k) != v}
    if malos:
        fallos += 1
        print("FALLO resolver [%s]: (obtenido, esperado) %r" % (nombre, malos))

# Las cuatro colas de cada idioma con la extensión, la URI SIP y el nombre
for idioma, exts in (("es", EXT_ES), ("en", EXT_EN)):
    total += 1
    out = resolver({"idioma": idioma, "gestion_abierta": True})
    malos = {}
    for clave in CLAVES:
        esperado = {"cola_" + clave: sip(exts[clave]), "cola_" + clave + "_ext": exts[clave]}
        for k, v in esperado.items():
            if out.get(k) != v:
                malos[k] = (out.get(k), v)
        if not out.get("cola_" + clave + "_nombre"):
            malos["cola_" + clave + "_nombre"] = (out.get("cola_" + clave + "_nombre"), "no vacío")
    if malos:
        fallos += 1
        print("FALLO colas [%s]: (obtenido, esperado) %r" % (idioma, malos))

# Solo estas salidas: ni cola_fuera_horario* ni nada más
for idioma in ("es", "en", "it"):
    for abierta in (True, False, None):
        total += 1
        out = resolver({"idioma": idioma, "gestion_abierta": abierta})
        if set(out) != SALIDAS:
            fallos += 1
            print("FALLO salidas [%s, %r]: sobran %r, faltan %r"
                  % (idioma, abierta, sorted(set(out) - SALIDAS), sorted(SALIDAS - set(out))))

total += 1
if any("fuera_horario" in k for k in COLAS) or any("fuera_horario" in k for i in COLAS.values() for k in i) \
        or any("fuera_horario" in k for k in resolver({"idioma": "es"})):
    fallos += 1
    print("FALLO: sigue habiendo una cola de fuera de horario")

# Ninguna salida es un texto «NO DISPONIBLE…» ni lleva otra cosa que una extensión SIP donde va una extensión
for idioma in ("es", "en"):
    total += 1
    out = resolver({"idioma": idioma, "gestion_abierta": False})
    texto = json.dumps(out, ensure_ascii=False)
    malos = []
    if "NO DISPONIBLE" in texto or "no disponible" in texto.lower():
        malos.append("lleva un texto «NO DISPONIBLE»")
    for clave in CLAVES:
        if not re.fullmatch(r"sip:\d{5}@" + re.escape(PBX), out["cola_" + clave]):
            malos.append("cola_%s no es una URI SIP: %r" % (clave, out["cola_" + clave]))
        if not re.fullmatch(r"\d{5}", out["cola_" + clave + "_ext"]):
            malos.append("cola_%s_ext no es una extensión: %r" % (clave, out["cola_" + clave + "_ext"]))
    if malos:
        fallos += 1
        print("FALLO sin textos en lugar de extensiones [%s]: %r" % (idioma, malos))

# Con Gestión cerrada solo cambia gestion_abierta: quien decide no transferir es «Preparar transferencia»
for idioma in ("es", "en"):
    total += 1
    abierta = resolver({"idioma": idioma, "gestion_abierta": True})
    cerrada = resolver({"idioma": idioma, "gestion_abierta": False})
    distintas = sorted(k for k in SALIDAS if abierta[k] != cerrada[k])
    if distintas != ["gestion_abierta"]:
        fallos += 1
        print("FALLO cerrada frente a abierta [%s]: difieren %r" % (idioma, distintas))

# Ninguna extensión es un menú automático (2114, 2115, 2119) ni la cola de fuera de horario (2129, 2130)
total += 1
exts = [e for i in COLAS.values() for e in i.values()]
exts_salida = [resolver({"idioma": i, "gestion_abierta": True})["cola_" + c + "_ext"]
               for i in ("es", "en") for c in CLAVES]
prohibidas = [e for e in exts + exts_salida if e in PROHIBIDAS + ("2129", "2130")]
if prohibidas:
    fallos += 1
    print("FALLO extensiones prohibidas: %r" % prohibidas)

# COLAS: clave → {"es": ext, "en": ext}, solo las cuatro claves y solo extensiones de cinco cifras
total += 1
esperado_colas = {c: {"es": EXT_ES[c], "en": EXT_EN[c]} for c in CLAVES}
if COLAS != esperado_colas:
    fallos += 1
    print("FALLO COLAS: %r, esperado %r" % (COLAS, esperado_colas))

# Pegado en HappyRobot: el nodo inyecta input_data y espera que el código deje la variable output
total += 1
codigo = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "resolver_colas.py"), encoding="utf-8").read()
entorno = {"input_data": {"idioma": "en", "gestion_abierta": "false"}}
exec(compile(codigo, "resolver_colas.py", "exec"), entorno)
if entorno.get("output") != resolver({"idioma": "en", "gestion_abierta": "false"}) \
        or entorno["output"]["cola_gestion_reserva"] != sip("18061"):
    fallos += 1
    print("FALLO pegado en el nodo: output = %r" % entorno.get("output"))

# Importado desde las pruebas (sin input_data) no se ejecuta nada ni se define output
total += 1
entorno = {}
exec(compile(codigo, "resolver_colas.py", "exec"), entorno)
if "output" in entorno:
    fallos += 1
    print("FALLO: sin input_data el código no debe definir output")

# El repo no lleva textos «NO DISPONIBLE» como valor ni números de teléfono
total += 1
sin_comentarios = "\n".join(linea.split("#", 1)[0] for linea in codigo.splitlines())
if "NO DISPONIBLE" in sin_comentarios or re.search(r"\+\d{6,}|\b\d{9,}\b", codigo):
    fallos += 1
    print("FALLO: el código lleva un texto «NO DISPONIBLE» o un número de teléfono")

print("%d/%d casos correctos" % (total - fallos, total))
sys.exit(1 if fallos else 0)
