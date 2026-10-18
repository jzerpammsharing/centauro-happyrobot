#!/usr/bin/env python3
# casos/atencion-es/codigo/comprobar_prompts.py
# Ejecutar: python3 -I casos/atencion-es/codigo/comprobar_prompts.py <versión> [--completo]
# Pruebas:  python3 -I casos/atencion-es/codigo/test_comprobar_prompts.py
"""Comprueba los prompts de módulo de una versión del bot único de Atención España.

<versión> es el nombre de una carpeta de casos/atencion-es/prompts/atencion-es/ (por ejemplo, v2). Si lleva una
barra, se toma como la ruta de una carpeta (así lo usan las pruebas, con carpetas temporales).

En cada prompt de módulo que existe en la carpeta comprueba:
- el tamaño máximo (restricciones globales del plan): Triaje 9.000, Prolongación 22.000 y Consultas 8.000
  caracteres; Punto de encuentro e Información de oficina no tienen máximo;
- que lleva el texto del bloque de reglas comunes (comun/bloques/reglas-comunes.md, entre sus dos líneas de
  INICIO y FIN) tal cual, empezando en una línea;
- que no contiene «NO DISPONIBLE», «extension_destino», las extensiones de los menús automáticos 2114, 2115 y
  2119 ni nueve o más cifras seguidas, con o sin espacios (los teléfonos se escriben en palabras).
Al propio bloque le comprueba el tamaño (4.500 como mucho) y los mismos textos prohibidos. Los demás ficheros de
la carpeta (herramientas, código, configuración) no se revisan.

Qué cuenta como prompt: el fichero sin la cabecera «<!-- … -->» del principio ni la sección «## Configuración»
del final, si las lleva, y sin espacios al final de las líneas. Los marcadores de variables se comparan y se
miden normalizados: {{ index . "<id>.<variable>" }} (como lo copia HappyRobot) y {{<persistent_id>.<variable>}}
(como se escribe por API) cuentan como {{<variable>}}, así que vale tanto el fichero fuente del repo como uno
copiado de HappyRobot, y los dos miden lo mismo.

Un módulo que falta se lista como pendiente y no es un fallo; con --completo, sí lo es.
Sale con 0 si todo cumple; con 1 y la lista de fallos si algo no cumple; con 2 si no encuentra la carpeta o el
bloque.
"""
import argparse
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(DIR, "..", "..", ".."))
PROMPTS = os.path.join(RAIZ, "casos", "atencion-es", "prompts", "atencion-es")
RUTA_BLOQUE = os.path.join(RAIZ, "comun", "bloques", "reglas-comunes.md")

# Prompt de módulo -> tamaño máximo en caracteres (None: sin máximo)
MODULOS = {
    "triaje.md": 9000,
    "punto-de-encuentro.md": None,
    "informacion-de-oficina.md": None,
    "prolongacion.md": 22000,
    "consultas-del-alquiler.md": 8000,
}
MAX_BLOQUE = 4500

# Las dos líneas de reglas-comunes.md entre las que está el texto que se copia en cada módulo
INICIO_BLOQUE = "----- INICIO DEL TEXTO QUE SE COPIA EN CADA MÓDULO -----"
FIN_BLOQUE = "----- FIN DEL TEXTO QUE SE COPIA -----"

UUID = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
RE_INDEX = re.compile(r'\{\{-?\s*index\s+\.\s+"[^".]+\.([^"]+)"\s*-?\}\}')  # {{ index . "<id>.<variable>" }}
RE_PERSISTENT = re.compile(r"\{\{\s*" + UUID + r"\.([^{}\s]+)\s*\}\}")  # {{<persistent_id>.<variable>}}
RE_MARCADOR = re.compile(r"\{\{\s*([A-Za-z0-9_.]+)\s*\}\}")  # {{ variable }} -> {{variable}}
RE_CONFIGURACION = re.compile(r"^##\s+Configuración\s*$")

# Patrón -> qué se dice en el fallo ({} es el texto encontrado)
PROHIBIDOS = [
    (re.compile(r"NO DISPONIBLE"), "«{}»"),
    (re.compile(r"extension_destino"), "«{}»"),
    (re.compile(r"(?<![0-9])(?:2114|2115|2119)(?![0-9])"), "la extensión {} de un menú automático"),
]
# Nueve o más cifras seguidas, con o sin espacios entre ellas (no cuentan los saltos de línea)
RE_CIFRAS = re.compile(r"[0-9](?:[ \t\u00a0\u202f]*[0-9]){8,}")


class ErrorUso(Exception):
    """No se puede comprobar: falta la carpeta o el bloque no está bien delimitado."""


def miles(n):
    return "{:,}".format(n).replace(",", ".")


def normalizar_linea(linea):
    linea = RE_INDEX.sub(r"{{\1}}", linea)
    linea = RE_PERSISTENT.sub(r"{{\1}}", linea)
    linea = RE_MARCADOR.sub(r"{{\1}}", linea)
    return linea.rstrip()


def partir(texto):
    return texto.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n").split("\n")


def recortar_blancos(lineas):
    """Quita las líneas en blanco del principio y del final de una lista de (número, línea)."""
    while lineas and not lineas[0][1].strip():
        lineas.pop(0)
    while lineas and not lineas[-1][1].strip():
        lineas.pop()
    return lineas


def lineas_del_prompt(texto):
    """(número de línea en el fichero, línea normalizada) de la parte que es prompt."""
    lineas = partir(texto)
    inicio = 0
    if lineas and lineas[0].lstrip().startswith("<!--"):
        for i, linea in enumerate(lineas):
            if "-->" in linea:
                inicio = i + 1
                break
    resultado = []
    for i in range(inicio, len(lineas)):
        if RE_CONFIGURACION.match(lineas[i]):
            break
        resultado.append((i + 1, normalizar_linea(lineas[i])))
    return recortar_blancos(resultado)


def lineas_del_bloque(ruta=RUTA_BLOQUE):
    """(número de línea en el fichero, línea normalizada) del texto que se copia, entre INICIO y FIN."""
    if not os.path.isfile(ruta):
        raise ErrorUso("no existe el bloque de reglas comunes: %s" % ruta)
    with open(ruta, encoding="utf-8") as f:
        lineas = partir(f.read())
    inicios = [i for i, linea in enumerate(lineas) if linea.strip() == INICIO_BLOQUE]
    fines = [i for i, linea in enumerate(lineas) if linea.strip() == FIN_BLOQUE]
    if len(inicios) != 1 or len(fines) != 1 or fines[0] < inicios[0]:
        raise ErrorUso("el bloque %s tiene que llevar una vez la línea «%s» y, después, una vez «%s»"
                       % (ruta, INICIO_BLOQUE, FIN_BLOQUE))
    resultado = [(i + 1, normalizar_linea(lineas[i])) for i in range(inicios[0] + 1, fines[0])]
    return recortar_blancos(resultado)


def texto_del_bloque(ruta=RUTA_BLOQUE):
    """El texto del bloque que se copia en cada módulo, normalizado (es el que se mide y se busca)."""
    return "\n".join(linea for _, linea in lineas_del_bloque(ruta))


def textos_prohibidos(nombre, lineas):
    fallos = []
    for numero, linea in lineas:
        for patron, descripcion in PROHIBIDOS:
            m = patron.search(linea)
            if m:
                fallos.append("%s, línea %d: contiene %s" % (nombre, numero, descripcion.format(m.group(0))))
        for m in RE_CIFRAS.finditer(linea):
            cifras = sum(c.isdigit() for c in m.group(0))
            fallos.append("%s, línea %d: tiene %d cifras seguidas («%s»); los teléfonos se escriben en palabras"
                          % (nombre, numero, cifras, m.group(0)))
    return fallos


def recorte(linea, n=90):
    linea = linea.strip()
    return linea if len(linea) <= n else linea[:n] + "…"


def alrededor(linea, pos, antes=40, despues=50):
    """El trozo de `linea` alrededor de la posición `pos`."""
    ini, fin = max(0, pos - antes), min(len(linea), pos + despues)
    return ("…" if ini else "") + linea[ini:fin] + ("…" if fin < len(linea) else "")


def falta_el_bloque(nombre, bloque, texto):
    """Mensaje de fallo si el prompt no lleva el bloque tal cual (empezando en una línea), o None."""
    if ("\n" + bloque + "\n") in ("\n" + texto + "\n"):
        return None
    lineas_prompt = texto.split("\n")
    presentes = set(lineas_prompt)
    for linea in bloque.split("\n"):
        if not linea.strip() or linea in presentes:
            continue
        # La línea del prompt que empieza igual durante más caracteres: si comparten un buen trozo, es la misma
        # línea cambiada y se enseña dónde cambia
        parecida = max(lineas_prompt, key=lambda p: len(os.path.commonprefix([linea, p])))
        comun = len(os.path.commonprefix([linea, parecida]))
        if comun >= 20:
            return ("%s: no lleva el bloque de reglas comunes tal cual; una línea cambia en el carácter %d: "
                    "el bloque dice «%s» y el prompt «%s»"
                    % (nombre, comun + 1, alrededor(linea, comun), alrededor(parecida, comun)))
        return "%s: no lleva el bloque de reglas comunes tal cual; falta la línea «%s»" % (nombre, recorte(linea))
    return ("%s: no lleva el bloque de reglas comunes tal cual; están todas sus líneas, pero no seguidas o en otro "
            "orden" % nombre)


def mostrar_ruta(ruta):
    ruta = os.path.abspath(ruta)
    return os.path.relpath(ruta, RAIZ) if ruta.startswith(RAIZ + os.sep) else ruta


def comprobar(carpeta, completo=False, ruta_bloque=RUTA_BLOQUE):
    """Devuelve (informe, fallos): las líneas que se imprimen y la lista de fallos."""
    if not os.path.isdir(carpeta):
        raise ErrorUso("no existe la carpeta %s" % carpeta)
    informe = ["Prompts de %s%s" % (mostrar_ruta(carpeta), " (--completo)" if completo else "")]
    fallos = []

    lineas_bloque = lineas_del_bloque(ruta_bloque)
    bloque = "\n".join(linea for _, linea in lineas_bloque)
    nombre_bloque = os.path.basename(ruta_bloque)
    informe.append("  %s: %s caracteres (máximo %s)" % (nombre_bloque, miles(len(bloque)), miles(MAX_BLOQUE)))
    if not bloque:
        fallos.append("%s: el texto que se copia está vacío" % nombre_bloque)
    if len(bloque) > MAX_BLOQUE:
        fallos.append("%s: mide %s caracteres; el máximo es %s" % (nombre_bloque, miles(len(bloque)),
                                                                   miles(MAX_BLOQUE)))
    fallos += textos_prohibidos(nombre_bloque, lineas_bloque)

    pendientes = []
    for nombre, maximo in MODULOS.items():
        ruta = os.path.join(carpeta, nombre)
        if not os.path.isfile(ruta):
            pendientes.append(nombre)
            informe.append("  %s: no existe%s" % (nombre, " (fallo)" if completo else " (pendiente)"))
            if completo:
                fallos.append("%s: falta el fichero" % nombre)
            continue
        with open(ruta, encoding="utf-8") as f:
            lineas = lineas_del_prompt(f.read())
        texto = "\n".join(linea for _, linea in lineas)
        informe.append("  %s: %s caracteres (%s)" % (nombre, miles(len(texto)),
                                                     "máximo %s" % miles(maximo) if maximo else "sin máximo"))
        if maximo and len(texto) > maximo:
            fallos.append("%s: mide %s caracteres; el máximo es %s" % (nombre, miles(len(texto)), miles(maximo)))
        mensaje = falta_el_bloque(nombre, bloque, texto)
        if mensaje:
            fallos.append(mensaje)
        fallos += textos_prohibidos(nombre, lineas)

    if pendientes and not completo:
        informe.append("Pendientes, no cuentan como fallo sin --completo: %s" % ", ".join(pendientes))
    return informe, fallos


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Comprueba los prompts de módulo de una versión del bot único de Atención España.")
    parser.add_argument("version", help="carpeta de casos/atencion-es/prompts/atencion-es/ (p. ej. v2) o ruta de "
                                        "una carpeta (si lleva una barra)")
    parser.add_argument("--completo", action="store_true",
                        help="un módulo que falta es un fallo (para la versión terminada)")
    args = parser.parse_args(argv)

    es_ruta = "/" in args.version or os.sep in args.version
    carpeta = args.version if es_ruta else os.path.join(PROMPTS, args.version)
    try:
        informe, fallos = comprobar(carpeta, completo=args.completo)
    except ErrorUso as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 2
    print("\n".join(informe))
    if fallos:
        print("%d %s:" % (len(fallos), "fallo" if len(fallos) == 1 else "fallos"))
        for fallo in fallos:
            print("  - %s" % fallo)
        return 1
    print("Sin fallos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
