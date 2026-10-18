# casos/atencion-es/codigo/generar_consultas.py
# Ejecutar: python3 -I casos/atencion-es/codigo/generar_consultas.py [--salida RUTA]
#
# Genera consultas_alquiler.py, el nodo Python de la herramienta «buscar_respuesta», a partir de
# comun/bloques/consultas-alquiler.md. Así las respuestas del alquiler tienen una sola fuente: el bloque.
#
# Del bloque solo se lee la parte «## Bloque» (el texto que va al bot) y se descartan las notas, que son las
# líneas que empiezan por «>». Se corta por los títulos «###» y «####»:
# - Cada título corresponde a un tema de TEMAS, emparejado por el principio del título (los paréntesis del final
#   se pueden cambiar sin tocar nada).
# - CONSULTAS FRECUENTES no es un tema: su introducción va delante del texto de cada subapartado «####».
# - Si un título no corresponde a ningún tema, o un tema no aparece, el generador falla con un mensaje claro.
import argparse
import os
import re
import sys

CARPETA = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(CARPETA, "..", "..", ".."))
BLOQUE_RELATIVO = "comun/bloques/consultas-alquiler.md"
BLOQUE = os.path.join(RAIZ, *BLOQUE_RELATIVO.split("/"))
SALIDA = os.path.join(CARPETA, "consultas_alquiler.py")
COMANDO = "python3 -I casos/atencion-es/codigo/generar_consultas.py"

# (principio del título del bloque, tema). El orden es el de SECCIONES en el fichero generado.
TEMAS = [
    ("DEVOLVER TARDE", "devolver_tarde"),
    ("COCHE DE ASEGURADORA O DE EMPRESA", "aseguradora_empresa"),
    ("DETALLES QUE PUEDES DAR", "detalles_prolongacion"),
    ("LA WEB NO LE DEJA", "la_web_no_le_deja"),
    ("RESERVA QUE AÚN NO HA EMPEZADO", "reserva_no_iniciada"),
    ("RECOGER TARDE", "recoger_tarde"),
    ("DEVOLVER ANTES", "devolucion"),
    ("COMBUSTIBLE, FIANZA, CARGOS Y REEMBOLSOS", "cargos_y_reembolsos"),
    ("REQUISITOS Y CONDUCTORES", "requisitos"),
    ("DURANTE EL ALQUILER", "durante_el_alquiler"),
    ("OTRAS PREGUNTAS", "otras"),
    ("TELÉFONOS QUE PUEDES DAR", "telefonos"),
]

# Sección del bloque que solo aporta su introducción a los subapartados «####»
TITULO_CONSULTAS = "CONSULTAS FRECUENTES"

ENCABEZADO = re.compile(r"^(#{3,4})\s+(\S.*?)\s*$")
FIN_DEL_BLOQUE = re.compile(r"^#{1,2}\s")

CABECERA = """\
# ===============================================================
# CONSULTAS DEL ALQUILER - bot único de Atención España
# ---------------------------------------------------------------
# GENERADO: este fichero no se edita a mano. Sale de %(bloque)s (solo la parte «## Bloque»,
# sin las notas, que son las líneas que empiezan por «>») con:
#
#     %(comando)s
#
# Para cambiar una respuesta se edita el bloque, se vuelve a generar y se pega el fichero entero en HappyRobot.
#
# Se pega tal cual en el nodo Python de la herramienta «buscar_respuesta». Entradas (input_data): tema (una de las
# claves de SECCIONES) y pregunta (la duda del cliente; el nodo no la usa). Salidas: tema (el usado), texto (la
# sección de ese tema) y encontrado (False si el tema no existía y se ha devuelto la sección «otras»).
# ===============================================================

# Una sección por tema, en el orden del bloque. Cada texto va troceado por párrafos para que los cambios del
# bloque se vean párrafo a párrafo en git.
"""

PIE = '''

def buscar(input_data):
    """Sección del tema pedido; si el tema no existe, la de «otras» con encontrado False."""
    tema = str(input_data.get("tema") or "").strip().lower()
    if tema in SECCIONES:
        return {"tema": tema, "texto": SECCIONES[tema], "encontrado": True}
    return {"tema": "otras", "texto": SECCIONES["otras"], "encontrado": False}


try:
    _entrada = input_data  # noqa: F821 (lo inyecta el nodo Python de HappyRobot)
except NameError:  # importado desde las pruebas locales
    _entrada = None
if _entrada is not None:
    output = buscar(_entrada)
'''


def _tema_de(titulo, numero_linea):
    """Tema que corresponde al título del bloque, emparejado por el principio del título."""
    temas = [tema for prefijo, tema in TEMAS if titulo.startswith(prefijo)]
    if not temas:
        raise ValueError(
            "El título «%s» (línea %d del bloque) no corresponde a ningún tema. Añade el tema a TEMAS en "
            "generar_consultas.py o corrige el título." % (titulo, numero_linea))
    if len(temas) > 1:
        raise ValueError(
            "El título «%s» (línea %d del bloque) corresponde a varios temas a la vez: %s."
            % (titulo, numero_linea, ", ".join(temas)))
    return temas[0]


def _limpiar(lineas):
    """Texto de un apartado: sin notas (ya filtradas), con una sola línea en blanco entre párrafos y sin
    líneas en blanco al principio ni al final."""
    texto = "\n".join(linea.rstrip() for linea in lineas)
    return re.sub(r"\n{3,}", "\n\n", texto).strip()


def _apartados(texto):
    """Apartados «###» y «####» de la parte «## Bloque»: lista de (nivel, título, número de línea, líneas)."""
    lineas = texto.replace("\r\n", "\n").split("\n")
    try:
        inicio = [linea.rstrip() for linea in lineas].index("## Bloque")
    except ValueError:
        raise ValueError("No encuentro la línea «## Bloque»: sin ella no sé dónde empieza el texto del bot.")

    apartados = []
    for numero, linea in enumerate(lineas[inicio + 1:], start=inicio + 2):
        if linea.lstrip().startswith(">"):
            continue  # nota: no va al prompt
        if FIN_DEL_BLOQUE.match(linea):
            break  # otro «#» o «##»: se acaba el bloque
        if linea.startswith("#"):
            encabezado = ENCABEZADO.match(linea)
            if not encabezado:
                raise ValueError("Título no reconocido en la línea %d del bloque: «%s». Solo hay títulos «###» y "
                                 "«####»." % (numero, linea))
            apartados.append((len(encabezado.group(1)), encabezado.group(2), numero, []))
        elif apartados:
            apartados[-1][3].append(linea)
        elif linea.strip():
            raise ValueError("Hay texto antes del primer título «###» (línea %d del bloque): «%s»."
                             % (numero, linea.strip()[:60]))
    return apartados


def leer_secciones(texto):
    """dict tema -> texto del bot, en el orden de TEMAS, a partir del contenido de consultas-alquiler.md. Lanza
    ValueError, con un mensaje que dice qué arreglar, si el bloque no cuadra con TEMAS."""
    secciones = {}
    introduccion = None  # la de CONSULTAS FRECUENTES, mientras estemos dentro de esa sección

    def guardar(tema, titulo, numero, contenido):
        if not contenido:
            raise ValueError("El apartado «%s» (línea %d del bloque, tema %s) está vacío." % (titulo, numero, tema))
        if tema in secciones:
            raise ValueError("El tema %s sale dos veces en el bloque (último título: «%s», línea %d)."
                             % (tema, titulo, numero))
        secciones[tema] = contenido

    for nivel, titulo, numero, lineas in _apartados(texto):
        cuerpo = _limpiar(lineas)
        if nivel == 3 and titulo.startswith(TITULO_CONSULTAS):
            if not cuerpo:
                raise ValueError("«%s» (línea %d del bloque) no tiene introducción: va delante de cada subapartado."
                                 % (titulo, numero))
            introduccion = cuerpo
        elif nivel == 3:
            introduccion = None
            guardar(_tema_de(titulo, numero), titulo, numero, cuerpo)
        else:
            if introduccion is None:
                raise ValueError("El subapartado «%s» (línea %d del bloque) está fuera de «%s»: los «####» solo "
                                 "valen dentro de esa sección." % (titulo, numero, TITULO_CONSULTAS))
            tema = _tema_de(titulo, numero)
            guardar(tema, titulo, numero, (introduccion + "\n\n" + cuerpo) if cuerpo else "")

    faltan = [tema for _, tema in TEMAS if tema not in secciones]
    if faltan:
        raise ValueError("Faltan temas en el bloque: %s. Cada uno necesita un título «###» o «####» que empiece "
                         "como se indica en TEMAS (generar_consultas.py)." % ", ".join(faltan))
    return {tema: secciones[tema] for _, tema in TEMAS}


def _literal(texto):
    """El texto como literal de Python, troceado por párrafos (repr de cada uno, unidos por concatenación)."""
    parrafos = texto.split("\n\n")
    trozos = [repr(parrafo + "\n\n") for parrafo in parrafos[:-1]] + [repr(parrafos[-1])]
    return "(\n" + "\n".join("        " + trozo for trozo in trozos) + "\n    )"


def generar(secciones):
    """Contenido completo de consultas_alquiler.py."""
    cabecera = CABECERA % {"bloque": BLOQUE_RELATIVO, "comando": COMANDO}
    entradas = "".join("    %r: %s,\n" % (tema, _literal(texto)) for tema, texto in secciones.items())
    return cabecera + "SECCIONES = {\n" + entradas + "}\n" + PIE


def main(argv=None):
    parser = argparse.ArgumentParser(description="Genera consultas_alquiler.py desde %s." % BLOQUE_RELATIVO)
    parser.add_argument("--salida", default=SALIDA, help="fichero que se escribe (por defecto, %s)" % SALIDA)
    args = parser.parse_args(argv)

    try:
        with open(BLOQUE, encoding="utf-8") as f:
            secciones = leer_secciones(f.read())
    except (OSError, ValueError) as error:
        print("ERROR: %s" % error, file=sys.stderr)
        return 1

    with open(args.salida, "w", encoding="utf-8", newline="\n") as f:
        f.write(generar(secciones))
    print("Escrito %s" % args.salida)
    for tema, texto in secciones.items():
        print("  %-22s %5d caracteres" % (tema, len(texto)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
