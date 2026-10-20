# casos/atencion-es/codigo/test_consultas_alquiler.py
# Ejecutar: python3 -I casos/atencion-es/codigo/test_consultas_alquiler.py
#
# Prueba el generador (generar_consultas.py) y el nodo generado (consultas_alquiler.py) que sale de
# comun/bloques/consultas-alquiler.md.
import os
import subprocess
import sys
import tempfile

CARPETA = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CARPETA)
from consultas_alquiler import SECCIONES, buscar  # noqa: E402
from generar_consultas import leer_secciones  # noqa: E402

GENERADOR = os.path.join(CARPETA, "generar_consultas.py")
VERSIONADO = os.path.join(CARPETA, "consultas_alquiler.py")

TEMAS = [
    "devolver_tarde", "aseguradora_empresa", "detalles_prolongacion", "la_web_no_le_deja",
    "reserva_no_iniciada", "recoger_tarde", "devolucion", "cargos_y_reembolsos", "requisitos",
    "durante_el_alquiler", "otras", "telefonos",
]
# Temas que salen de un subapartado «####» de CONSULTAS FRECUENTES: llevan delante su introducción
CON_INTRODUCCION = TEMAS[4:]
INTRODUCCION = "Son preguntas que no son de prolongación, pero que puedes responder tú."
# Fragmentos que solo aparecen en las notas del bloque y no pueden llegar al prompt
PROHIBIDOS = ("DECIDIR", "Solo en Minibús", "Nuevo.", "Equipo (")

fallos = 0
total = 0


def comprobar(nombre, cumple, detalle=""):
    global fallos, total
    total += 1
    if not cumple:
        fallos += 1
        print("FALLO [%s] %s" % (nombre, detalle))


# ---------------------------------------------------------------
# Las secciones del bloque
# ---------------------------------------------------------------
comprobar("están los 12 temas, en el orden de la ficha", list(SECCIONES) == TEMAS,
          "obtenido %r" % (list(SECCIONES),))

for tema, texto in SECCIONES.items():
    comprobar("%s: sin líneas de nota" % tema,
              not any(linea.lstrip().startswith(">") for linea in texto.splitlines()))
    for prohibido in PROHIBIDOS:
        comprobar("%s: sin «%s»" % (tema, prohibido), prohibido not in texto)
    comprobar("%s: de 1.000 a 6.000 caracteres" % tema, 1000 <= len(texto) <= 6000, "mide %d" % len(texto))
    comprobar("%s: sin títulos ni líneas en blanco de más" % tema,
              not any(linea.startswith("#") for linea in texto.splitlines())
              and "\n\n\n" not in texto and texto == texto.strip())

for tema in TEMAS:
    texto = SECCIONES[tema]
    # Los cinco primeros temas salen de un «###» y no llevan la introducción de CONSULTAS FRECUENTES
    comprobar("%s: introducción de CONSULTAS FRECUENTES" % tema,
              texto.startswith(INTRODUCCION) == (tema in CON_INTRODUCCION),
              "empieza por %r" % texto[:60])

comprobar("reserva_no_iniciada empieza con el párrafo de introducción",
          SECCIONES["reserva_no_iniciada"].startswith(
              "Son preguntas que no son de prolongación, pero que puedes responder tú. "
              "Responde solo con lo que pone aquí, en una o dos frases por turno, y no añadas nada que no esté escrito. "
              "Si el cliente necesita después que alguien mire o cambie su reserva, transfiere a GESTIÓN DE RESERVA.\n\n"
              "REGLA: cambiar o cancelar una reserva que aún no ha empezado"))
comprobar("la introducción aparece una sola vez por tema",
          all(SECCIONES[tema].count(INTRODUCCION) == 1 for tema in CON_INTRODUCCION))
comprobar("CONSULTAS FRECUENTES no es un tema", not any("consultas" in tema for tema in SECCIONES))

# Contenido que tiene que sobrevivir (y el de las notas, no), tema a tema
CONTENIDO = [
    ("devolver_tarde", "no hay periodo de cortesía"),
    ("devolver_tarde", "Después sigue con EXPLICACIÓN."),
    ("aseguradora_empresa", "motivo_transferencia aseguradora"),
    ("detalles_prolongacion", "la penalización es de cincuenta euros por día de demora"),
    ("la_web_no_le_deja", "Usuario bloqueado:"),
    ("reserva_no_iniciada", "Smart Key: en las oficinas sin personal"),
    ("recoger_tarde", "NO PUDO RECOGER A SU HORA:"),
    ("devolucion", "Con la oficina cerrada: algunas tienen buzón de llaves; depende de la oficina"),
    ("cargos_y_reembolsos", "hasta diez días hábiles"),
    ("requisitos", "Conductor adicional: todos los conductores tienen que figurar en el contrato."),
    ("durante_el_alquiler", "Testigo de presión de los neumáticos"),
    ("otras", "Está hablando con un agente de IA"),
    ("telefonos", "más treinta y cuatro, nueve seis seis, tres seis cinco, tres seis cinco"),
]
for tema, fragmento in CONTENIDO:
    comprobar("%s contiene «%s»" % (tema, fragmento[:40]), fragmento in SECCIONES[tema])

# Las notas de cada apartado no se cuelan en el texto del vecino
comprobar("no pasa texto de una nota al tema siguiente",
          "Resuelto por el equipo" not in SECCIONES["aseguradora_empresa"]
          and "Se queda en cada bot" not in SECCIONES["la_web_no_le_deja"]
          and "Enganche por bot" not in SECCIONES["recoger_tarde"])

# ---------------------------------------------------------------
# buscar()
# ---------------------------------------------------------------
out = buscar({"tema": "fianza", "pregunta": "¿cuándo me devuelven la fianza?"})
comprobar("tema desconocido → otras y encontrado False",
          out == {"tema": "otras", "texto": SECCIONES["otras"], "encontrado": False}, "obtenido %r" % (out["tema"],))

out = buscar({"tema": " Requisitos ", "pregunta": "¿qué carnet necesito?"})
comprobar("tema con mayúsculas y espacios → requisitos y encontrado True",
          out == {"tema": "requisitos", "texto": SECCIONES["requisitos"], "encontrado": True},
          "obtenido %r" % (out["tema"],))

for tema in TEMAS:
    out = buscar({"tema": tema, "pregunta": "x"})
    comprobar("buscar(%s)" % tema,
              out == {"tema": tema, "texto": SECCIONES[tema], "encontrado": True})

comprobar("sin pregunta funciona igual", buscar({"tema": "telefonos"}) == buscar({"tema": "telefonos", "pregunta": "?"}))
for vacio in ({}, {"tema": None}, {"tema": ""}, {"tema": "   "}, {"tema": 42}):
    out = buscar(vacio)
    comprobar("tema ausente o vacío (%r) → otras" % (vacio,),
              out["tema"] == "otras" and out["encontrado"] is False and out["texto"] == SECCIONES["otras"])
comprobar("salidas exactas", set(buscar({"tema": "otras"})) == {"tema", "texto", "encontrado"})

# ---------------------------------------------------------------
# El fichero generado
# ---------------------------------------------------------------
with open(VERSIONADO, encoding="utf-8") as f:
    versionado = f.read()

comprobar("pesa menos de 45.000 caracteres", len(versionado) < 45000, "mide %d" % len(versionado))

cabecera = versionado[:1500]
comprobar("la cabecera dice que está generado, de qué fichero, con qué comando y que no se edita a mano",
          "GENERADO" in cabecera
          and "comun/bloques/consultas-alquiler.md" in cabecera
          and "python3 -I casos/atencion-es/codigo/generar_consultas.py" in cabecera
          and "no se edita a mano" in cabecera.lower())

# Se genera en un directorio temporal y tiene que salir idéntico al versionado
with tempfile.TemporaryDirectory() as tmp:
    salida = os.path.join(tmp, "consultas_alquiler.py")
    proc = subprocess.run([sys.executable, "-I", GENERADOR, "--salida", salida],
                          capture_output=True, text=True)
    comprobar("el generador termina bien", proc.returncode == 0, "código %d, %s" % (proc.returncode, proc.stderr))
    if os.path.exists(salida):
        with open(salida, encoding="utf-8") as f:
            generado = f.read()
        comprobar("lo generado es idéntico al consultas_alquiler.py versionado", generado == versionado,
                  "difieren; vuelve a generar con python3 -I casos/atencion-es/codigo/generar_consultas.py")
    else:
        comprobar("el generador escribe el fichero de salida", False, "no existe %s" % salida)

# El nodo, tal como lo ejecuta HappyRobot: input_data inyectado y `output` al final
espacio = {"input_data": {"tema": "cargos_y_reembolsos", "pregunta": "¿cuándo me devuelven la fianza?"}}
exec(compile(versionado, VERSIONADO, "exec"), espacio)
comprobar("como nodo: asigna output",
          espacio.get("output") == {"tema": "cargos_y_reembolsos", "texto": SECCIONES["cargos_y_reembolsos"],
                                    "encontrado": True})
espacio = {}
exec(compile(versionado, VERSIONADO, "exec"), espacio)
comprobar("importado sin input_data: no asigna output", "output" not in espacio)

# ---------------------------------------------------------------
# El generador con bloques mal formados
# ---------------------------------------------------------------
TITULOS = [
    ("###", "DEVOLVER TARDE (aviso)"), ("###", "COCHE DE ASEGURADORA O DE EMPRESA"),
    ("###", "DETALLES QUE PUEDES DAR (uno por turno)"), ("###", "LA WEB NO LE DEJA"),
    ("###", "CONSULTAS FRECUENTES"),
    ("####", "RESERVA QUE AÚN NO HA EMPEZADO"), ("####", "RECOGER TARDE (VUELO)"),
    ("####", "DEVOLVER ANTES, EN OTRA OFICINA O CON LA OFICINA CERRADA"),
    ("####", "COMBUSTIBLE, FIANZA, CARGOS Y REEMBOLSOS"), ("####", "REQUISITOS Y CONDUCTORES"),
    ("####", "DURANTE EL ALQUILER"), ("####", "OTRAS PREGUNTAS"), ("####", "TELÉFONOS QUE PUEDES DAR (solo estos)"),
]


def bloque(titulos=TITULOS, antes="# Bloque\n\n> nota de la cabecera\n\n## Bloque\n\n"):
    partes = [antes]
    for nivel, titulo in titulos:
        partes.append("%s %s\n\n" % (nivel, titulo))
        if titulo == "CONSULTAS FRECUENTES":
            partes.append("Introducción común.\n\n> Nota que no va.\n\n")
        else:
            partes.append("Texto de %s.\n\n> Nota que no va.\n\nSegundo párrafo.\n\n> Otra nota\n> en dos líneas.\n\n" % titulo)
    return "".join(partes)


def falla(texto, *fragmentos):
    """True si leer_secciones falla con un ValueError cuyo mensaje contiene todos los fragmentos."""
    try:
        leer_secciones(texto)
    except ValueError as error:
        return all(fragmento in str(error) for fragmento in fragmentos)
    return False


minimo = leer_secciones(bloque())
comprobar("bloque mínimo: 12 temas", list(minimo) == TEMAS, "obtenido %r" % (list(minimo),))
comprobar("bloque mínimo: sin notas, párrafos separados por una línea en blanco",
          minimo["devolver_tarde"] == "Texto de DEVOLVER TARDE (aviso).\n\nSegundo párrafo."
          and minimo["otras"] == "Introducción común.\n\nTexto de OTRAS PREGUNTAS.\n\nSegundo párrafo.", repr(minimo["otras"]))
comprobar("título sin tema → falla y nombra el título",
          falla(bloque(TITULOS + [("###", "SEGUROS NUEVOS")]), "SEGUROS NUEVOS"))
comprobar("subapartado sin tema → falla y nombra el título",
          falla(bloque(TITULOS[:-1] + [("####", "SEGUROS NUEVOS")] + TITULOS[-1:]), "SEGUROS NUEVOS"))
comprobar("tema que no aparece → falla y dice cuál",
          falla(bloque([t for t in TITULOS if not t[1].startswith("TELÉFONOS")]), "telefonos")
          and falla(bloque([t for t in TITULOS if not t[1].startswith("LA WEB")]), "la_web_no_le_deja"))
comprobar("tema repetido → falla",
          falla(bloque(TITULOS + [("####", "OTRAS PREGUNTAS")]), "otras"))
comprobar("CONSULTAS FRECUENTES en sí no es un tema (sin subapartados faltan los demás)",
          falla(bloque(TITULOS[:5]), "reserva_no_iniciada"))
comprobar("subapartado fuera de CONSULTAS FRECUENTES → falla",
          falla(bloque([TITULOS[0], ("####", "RECOGER TARDE (VUELO)")] + TITULOS[1:4] + TITULOS[4:]), "RECOGER TARDE"))
comprobar("apartado vacío → falla",
          falla(bloque().replace("Texto de LA WEB NO LE DEJA.\n\n> Nota que no va.\n\nSegundo párrafo.\n\n> Otra nota\n> en dos líneas.\n\n", ""),
                "la_web_no_le_deja"))
comprobar("sin «## Bloque» → falla", falla("### DEVOLVER TARDE\n\nTexto.\n", "## Bloque"))
comprobar("texto suelto antes del primer título → falla",
          falla(bloque(antes="## Bloque\n\nTexto suelto.\n\n"), "Texto suelto"))

print("%d/%d casos correctos" % (total - fallos, total))
sys.exit(1 if fallos else 0)
