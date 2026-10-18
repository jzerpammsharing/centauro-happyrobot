# casos/atencion-es/codigo/test_comprobar_prompts.py
# Ejecutar: python3 -I casos/atencion-es/codigo/test_comprobar_prompts.py
#
# Prueba comprobar_prompts.py como se usa (por línea de órdenes, con carpetas temporales) y el propio bloque de
# reglas comunes (comun/bloques/reglas-comunes.md). Los prompts de prueba llevan el bloque real.
import os
import re
import subprocess
import sys
import tempfile

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
import comprobar_prompts  # noqa: E402

SCRIPT = os.path.join(DIR, "comprobar_prompts.py")
RUTA_BLOQUE = os.path.join(DIR, "..", "..", "..", "comun", "bloques", "reglas-comunes.md")
MODULOS = ["triaje.md", "punto-de-encuentro.md", "informacion-de-oficina.md", "prolongacion.md",
           "consultas-del-alquiler.md"]
ID_CONTEXTO = "e51cd732-f403-4ef7-95d4-490347960a93"  # lleva «490347960»: nueve cifras seguidas
MARCADORES = ["idioma_nombre", "modo_virtual", "gestion_abierta"]
SECCIONES = [
    "IDENTIDAD Y ESTILO",
    "REGLAS DE VOZ",
    "IDIOMA DE ATENCIÓN",
    "MODO DE ATENCIÓN",
    "GESTIÓN CERRADA: REGLA DE MÁXIMA PRIORIDAD",
    "COLA DE GESTIÓN CERRADA",
    "TELÉFONOS QUE PUEDES DAR",
    "CÓMO TRANSFERIR",
    "SI LA TRANSFERENCIA FALLA",
    "CAMBIOS DE MÓDULO",
]

BLOQUE = comprobar_prompts.texto_del_bloque()

total = 0
fallos = 0


def caso(nombre, ok, detalle=""):
    global total, fallos
    total += 1
    if not ok:
        fallos += 1
        print("FALLO %s%s" % (nombre, (":\n" + detalle) if detalle else ""))


def ejecutar(carpeta, *opciones):
    r = subprocess.run([sys.executable, "-I", SCRIPT, str(carpeta), *opciones], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def escribir(carpeta, nombre, texto):
    with open(os.path.join(carpeta, nombre), "w", encoding="utf-8") as f:
        f.write(texto)


def con_bloque(tamano=None, extra="Reglas propias del módulo.", bloque=BLOQUE):
    """Un prompt con el bloque y un texto propio; con `tamano`, el texto se rellena hasta medir eso exactamente."""
    texto = bloque + "\n\n" + extra
    if tamano is not None:
        texto += "x" * (tamano - len(texto))
        assert len(texto) == tamano
    return texto


def lineas_de_fallo(salida):
    return [linea for linea in salida.splitlines() if linea.startswith("  - ")]


# --- El bloque ---------------------------------------------------------------------------------------------

caso("bloque: mide como mucho 4.500 caracteres (mide %d)" % len(BLOQUE), 0 < len(BLOQUE) <= 4500)

titulos = [linea[2:-2] for linea in BLOQUE.split("\n") if re.fullmatch(r"\*\*[^*]+\*\*", linea)]
caso("bloque: secciones en el orden de la ficha",
     len(titulos) == len(SECCIONES) and all(t.startswith(s) for t, s in zip(titulos, SECCIONES)),
     "  encontradas: %r" % titulos)

caso("bloque: sin notas «>» dentro del texto que se copia",
     not any(linea.lstrip().startswith(">") for linea in BLOQUE.split("\n")))

caso("bloque: lleva los marcadores {{idioma_nombre}}, {{modo_virtual}} y {{gestion_abierta}}",
     all(BLOQUE.count("{{%s}}" % m) == 1 for m in MARCADORES))

caso("bloque: nombra las cuatro colas y los resultados gestion_cerrada y cola_no_valida",
     all(p in BLOQUE for p in ("gestion", "asistencia", "nueva_reserva", "minibus", "gestion_cerrada",
                               "cola_no_valida", "transfer_to_human_agent", "motivo_transferencia",
                               "resumen_para_agente")))

caso("bloque: dice los cuatro idiomas que atiende y, en francés, que se ofrecen nombrándolos",
     "Atiendes en español, inglés, italiano y portugués" in BLOQUE and "nombrándolos" in BLOQUE)

caso("bloque: en modo virtual, un caso de gestión sigue COLA DE GESTIÓN CERRADA",
     "si es un caso de gestión, sigue COLA DE GESTIÓN CERRADA" in BLOQUE)

caso("bloque: el límite de cambios se cuenta por tema y al tercero se transfiere",
     "por tema" in BLOQUE and "al tercero transfiere" in BLOQUE)

caso("bloque: los cuatro teléfonos de la V11 en palabras",
     all(t in BLOQUE for t in ("nueve seis seis, tres seis cinco, tres seis cinco",
                               "nueve seis seis, tres seis cero, tres seis cero",
                               "nueve seis, seis ocho tres, cero siete, cero siete",
                               "nueve seis, seis siete cero, tres cinco, tres cuatro")))

with open(RUTA_BLOQUE, encoding="utf-8") as f:
    fichero_bloque = f.read()
caso("bloque: el fichero tiene las dos líneas que delimitan el texto que se copia",
     fichero_bloque.count(comprobar_prompts.INICIO_BLOQUE) == 1
     and fichero_bloque.count(comprobar_prompts.FIN_BLOQUE) == 1)

# --- Paso 1 de la ficha: un prompt de 9.001 caracteres y otro sin el bloque ----------------------------------

with tempfile.TemporaryDirectory() as d:
    escribir(d, "triaje.md", con_bloque(9001))
    escribir(d, "consultas-del-alquiler.md", "Prompt de Consultas sin el bloque de reglas comunes.\n")
    codigo, salida = ejecutar(d)
    lf = lineas_de_fallo(salida)
    caso("paso 1: sale con 1 y lista los dos fallos",
         codigo == 1 and len(lf) == 2
         and any("triaje.md" in x and "9.001" in x and "9.000" in x for x in lf)
         and any("consultas-del-alquiler.md" in x and "bloque" in x for x in lf),
         salida)

with tempfile.TemporaryDirectory() as d:
    escribir(d, "triaje.md", con_bloque(9000))
    codigo, salida = ejecutar(d)
    caso("triaje de 9.000 caracteres exactos: pasa", codigo == 0, salida)

with tempfile.TemporaryDirectory() as d:
    escribir(d, "punto-de-encuentro.md", con_bloque(40000))
    escribir(d, "prolongacion.md", con_bloque(22001))
    codigo, salida = ejecutar(d)
    lf = lineas_de_fallo(salida)
    caso("punto de encuentro sin máximo; prolongación de 22.001 falla",
         codigo == 1 and len(lf) == 1 and "prolongacion.md" in lf[0] and "22.000" in lf[0], salida)

with tempfile.TemporaryDirectory() as d:
    escribir(d, "consultas-del-alquiler.md", con_bloque(8001))
    codigo, salida = ejecutar(d)
    caso("consultas de 8.001 falla", codigo == 1 and "8.000" in salida, salida)

# --- El bloque tal cual --------------------------------------------------------------------------------------

lineas = BLOQUE.split("\n")
medio = next(i for i in range(len(lineas) // 2, len(lineas)) if lineas[i].strip())
cambiado = "\n".join(lineas[:medio] + [lineas[medio] + " Cambiado."] + lineas[medio + 1:])
with tempfile.TemporaryDirectory() as d:
    escribir(d, "triaje.md", con_bloque(bloque=cambiado))
    codigo, salida = ejecutar(d)
    caso("bloque con una línea cambiada: falla y cita la línea", codigo == 1 and "Cambiado." in salida, salida)

with tempfile.TemporaryDirectory() as d:
    escribir(d, "triaje.md", "Texto del módulo antes.\n\n" + BLOQUE + "\n\nY después.\n")
    codigo, salida = ejecutar(d)
    caso("el bloque puede ir detrás de una frase propia del módulo", codigo == 0, salida)

# --- Sintaxis de HappyRobot, cabecera y configuración --------------------------------------------------------

assert all("{{%s}}" % m in BLOQUE for m in MARCADORES)
happyrobot = BLOQUE
for m in MARCADORES:
    happyrobot = happyrobot.replace("{{%s}}" % m, '{{ index . "%s.%s" }}' % (ID_CONTEXTO, m))
with tempfile.TemporaryDirectory() as d:
    escribir(d, "prolongacion.md", con_bloque(bloque=happyrobot))
    codigo, salida = ejecutar(d)
    caso("fichero copiado de HappyRobot ({{ index . \"<id>.<variable>\" }}): pasa", codigo == 0, salida)

por_api = BLOQUE
for m in MARCADORES:
    por_api = por_api.replace("{{%s}}" % m, "{{%s.%s}}" % (ID_CONTEXTO, m))
with tempfile.TemporaryDirectory() as d:
    escribir(d, "prolongacion.md", con_bloque(bloque=por_api))
    codigo, salida = ejecutar(d)
    caso("fichero con {{<persistent_id>.<variable>}}: pasa", codigo == 0, salida)

cabecera = "<!-- workflow: prueba · versión: v2 (prueba) · nodo: Triaje · copiado: 2026-10-18 -->\n\n"
configuracion = ("\n\n## Configuración\n\n```json\n{\"node_id\": \"%s\", \"persistent_id\": \"%s\"}\n```\n"
                 % (ID_CONTEXTO, ID_CONTEXTO))
with tempfile.TemporaryDirectory() as d:
    escribir(d, "triaje.md", cabecera + con_bloque(9000) + configuracion)
    codigo, salida = ejecutar(d)
    caso("cabecera y «## Configuración» no cuentan ni se revisan (prompt de 9.000 exactos)",
         codigo == 0 and "triaje.md: 9.000 caracteres" in salida, salida)

# --- Textos prohibidos ---------------------------------------------------------------------------------------

with tempfile.TemporaryDirectory() as d:
    escribir(d, "prolongacion.md", con_bloque(extra="Si la cola dice NO DISPONIBLE AHORA, no transfieras."))
    codigo, salida = ejecutar(d)
    caso("«NO DISPONIBLE»: falla", codigo == 1 and "NO DISPONIBLE" in salida, salida)

with tempfile.TemporaryDirectory() as d:
    escribir(d, "prolongacion.md", con_bloque(extra="Rellena extension_destino.\n\nO pasa a la 2114."))
    codigo, salida = ejecutar(d)
    lf = lineas_de_fallo(salida)
    caso("«extension_destino» y la extensión 2114: dos fallos",
         codigo == 1 and len(lf) == 2 and any("extension_destino" in x for x in lf)
         and any("2114" in x for x in lf), salida)

with tempfile.TemporaryDirectory() as d:
    escribir(d, "prolongacion.md", con_bloque(extra="Llame al 900000111."))
    codigo, salida = ejecutar(d)
    caso("número de 9 cifras seguidas: falla", codigo == 1 and "900000111" in salida, salida)

with tempfile.TemporaryDirectory() as d:
    escribir(d, "prolongacion.md", con_bloque(extra="Llame al +34 900 000 111."))
    codigo, salida = ejecutar(d)
    caso("número de 9 o más cifras con espacios: falla", codigo == 1 and "900 000 111" in salida, salida)

with tempfile.TemporaryDirectory() as d:
    escribir(d, "prolongacion.md", con_bloque(extra="Las colas son 18057/18061 y el código 1234 5678."))
    codigo, salida = ejecutar(d)
    caso("8 cifras o cifras separadas por una barra: pasa", codigo == 0, salida)

# --- Textos prohibidos en los demás ficheros (herramientas, saltos…), salvo las copias de código ----------

with tempfile.TemporaryDirectory() as d:
    escribir(d, "herramientas-triaje.md", "Rellena extension_destino con la extensión.\n")
    escribir(d, "saltos.md", "Si la cola dice NO DISPONIBLE, no saltes.\n")
    escribir(d, "registrar-resultado.md", "La cola de asistencia era la 2115.\n")
    codigo, salida = ejecutar(d)
    lf = lineas_de_fallo(salida)
    caso("herramientas-*.md, saltos.md y otros ficheros: se revisan los textos prohibidos",
         codigo == 1 and len(lf) == 3 and any("herramientas-triaje.md" in x and "extension_destino" in x for x in lf)
         and any("saltos.md" in x and "NO DISPONIBLE" in x for x in lf)
         and any("registrar-resultado.md" in x and "2115" in x for x in lf), salida)

with tempfile.TemporaryDirectory() as d:
    for nombre in comprobar_prompts.EXCLUIDOS:
        escribir(d, nombre, "# NO DISPONIBLE AHORA, extension_destino, menú 2114, prueba 900000111\n")
    codigo, salida = ejecutar(d)
    caso("copias de código o configuración (EXCLUIDOS): no se revisan",
         codigo == 0 and "resolver-colas.md" in salida and "No se revisan" in salida, salida)

with tempfile.TemporaryDirectory() as d:
    escribir(d, "herramientas-triaje.md",
             cabecera + "- persistent_id: `%s`\n\nDescripción: transfiere con la cola que corresponda.%s"
             % (ID_CONTEXTO, configuracion))
    codigo, salida = ejecutar(d)
    caso("un UUID con nueve cifras seguidas no cuenta como teléfono", codigo == 0, salida)

# --- Módulos que faltan: sin y con --completo ----------------------------------------------------------------

with tempfile.TemporaryDirectory() as d:
    escribir(d, "triaje.md", con_bloque())
    escribir(d, "herramientas-triaje.md", "Descripción de una herramienta, sin textos prohibidos.\n")
    codigo, salida = ejecutar(d)
    pendientes = [m for m in MODULOS[1:] if m in salida]
    caso("sin --completo: los módulos que faltan son pendientes y no fallan",
         codigo == 0 and len(pendientes) == 4 and "pendiente" in salida.lower(), salida)

    codigo, salida = ejecutar(d, "--completo")
    lf = lineas_de_fallo(salida)
    caso("con --completo: cada módulo que falta es un fallo",
         codigo == 1 and len(lf) == 4 and all(any(m in x for x in lf) for m in MODULOS[1:]), salida)

with tempfile.TemporaryDirectory() as d:
    for m in MODULOS:
        escribir(d, m, con_bloque())
    codigo, salida = ejecutar(d, "--completo")
    caso("con --completo y los cinco módulos bien: pasa", codigo == 0, salida)

with tempfile.TemporaryDirectory() as d:
    codigo, salida = ejecutar(os.path.join(d, "no-existe"))
    caso("carpeta que no existe: sale con 2", codigo == 2, salida)

print("%d/%d casos correctos" % (total - fallos, total))
sys.exit(1 if fallos else 0)
