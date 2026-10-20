# casos/atencion-es/codigo/test_estado_oficina.py
# Ejecutar: python3 -I casos/atencion-es/codigo/test_estado_oficina.py
import ast
import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import contexto_llamada  # noqa: E402
from estado_oficina import AEROPUERTOS, estado, identificar  # noqa: E402

UTC = timezone.utc
RUTA_NODO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "estado_oficina.py")
RUTA_PROMPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "prompts", "atencion-es", "v2",
                           "punto-de-encuentro.md")

# Las cuatro listas de la v2 antes de R39 (prompt de Punto de encuentro, sección PRIMERO): la tabla del código tiene
# que dar la misma zona a cada aeropuerto.
LISTAS_V2 = {
    "cet": ["Madrid", "Barcelona", "Bilbao", "Ibiza", "Málaga", "Palma de Mallorca", "Santiago de Compostela",
            "Sevilla", "Valencia", "Alicante", "Almería", "Menorca", "Bari", "Bolonia", "Cagliari", "Florencia",
            "Milán-Bérgamo", "Milán-Malpensa", "Nápoles", "Olbia", "Palermo", "Pisa", "Roma-Ciampino",
            "Roma-Fiumicino", "Catania", "Venecia"],
    "wet": ["Faro", "Lisboa", "Madeira", "Oporto", "Gran Canaria", "Tenerife Sur"],
    "eet": ["Atenas", "Cefalonia", "Corfú", "Chania", "Heraclión", "Rodas", "Santorini", "Tesalónica"],
    "murcia": ["Murcia"],
}
# Abren a las ocho (prompt, PRIMERO y HORARIO Y DEVOLUCIÓN EN AEROPUERTOS); el resto, a las siete.
ABREN_A_LAS_OCHO = {"Murcia", "Bari", "Florencia", "Nápoles", "Venecia"}

NOCHE = {"nocturno_cet": "true", "nocturno_wet": "true", "nocturno_eet": "true", "nocturno_murcia": "true"}
DIA = {"nocturno_cet": "false", "nocturno_wet": "false", "nocturno_eet": "false", "nocturno_murcia": "false"}

# Martes 20/10/2026 (UTC+2 en Madrid)
MARTES_05_30 = datetime(2026, 10, 20, 3, 30, tzinfo=UTC)   # Madrid 05:30, Lisboa 04:30, Atenas 06:30
MARTES_06_30 = datetime(2026, 10, 20, 4, 30, tzinfo=UTC)   # Madrid 06:30, Atenas 07:30 (abierta)
MARTES_07_30 = datetime(2026, 10, 20, 5, 30, tzinfo=UTC)   # Madrid 07:30: Murcia sigue cerrada hasta las 8
MARTES_10_00 = datetime(2026, 10, 20, 8, 0, tzinfo=UTC)
MARTES_22_30 = datetime(2026, 10, 20, 20, 30, tzinfo=UTC)  # Murcia cerrada, Madrid abierta, Atenas 23:30 cerrada
MARTES_23_30 = datetime(2026, 10, 20, 21, 30, tzinfo=UTC)  # Madrid cerrada, Lisboa 22:30 abierta


def entrada(aeropuerto, **extra):
    return {"aeropuerto": aeropuerto, **extra}


total = 0
fallos = 0


def comprobar(nombre, obtenido, esperado):
    global total, fallos
    total += 1
    if obtenido != esperado:
        fallos += 1
        print("FALLO %s: obtenido %r, esperado %r" % (nombre, obtenido, esperado))


# 1. La tabla cubre exactamente los aeropuertos de las cuatro listas, con la misma zona y la hora de apertura del prompt
for zona, nombres in LISTAS_V2.items():
    for nombre in nombres:
        comprobar("tabla %s" % nombre, AEROPUERTOS.get(nombre, (None, None))[0], zona)
        comprobar("apertura %s" % nombre, AEROPUERTOS.get(nombre, (None, None))[1],
                  8 if nombre in ABREN_A_LAS_OCHO else 7)
comprobar("tabla sin aeropuertos de más", sorted(AEROPUERTOS), sorted(n for ns in LISTAS_V2.values() for n in ns))

# 2. Identificación del nombre que dice el modelo (sin tildes, mayúsculas, otros idiomas, con «aeropuerto de»)
NOMBRES = [
    ("Valencia", "Valencia"), ("valencia", "Valencia"), ("Aeropuerto de Valencia", "Valencia"),
    ("VALENCIA AIRPORT", "Valencia"), ("Malaga", "Málaga"), ("Málaga-Costa del Sol", "Málaga"),
    ("Madrid Barajas", "Madrid"), ("Barajas T4", "Madrid"), ("Barcelona El Prat", "Barcelona"),
    ("Palma", "Palma de Mallorca"), ("Mallorca", "Palma de Mallorca"), ("Palma de Mallorca", "Palma de Mallorca"),
    ("Las Palmas de Gran Canaria", "Gran Canaria"), ("Gran Canaria", "Gran Canaria"),
    ("Tenerife", "Tenerife Sur"), ("Tenerife Sur", "Tenerife Sur"), ("Santiago", "Santiago de Compostela"),
    ("Seville", "Sevilla"), ("Alicante-Elche", "Alicante"), ("Mahón", "Menorca"), ("Almeria", "Almería"),
    ("Murcia", "Murcia"), ("Región de Murcia (Corvera)", "Murcia"), ("Lisbon", "Lisboa"), ("Porto", "Oporto"),
    ("Funchal", "Madeira"), ("Bergamo", "Milán-Bérgamo"), ("Milán Bérgamo", "Milán-Bérgamo"),
    ("Malpensa", "Milán-Malpensa"), ("Milan Malpensa", "Milán-Malpensa"), ("Fiumicino", "Roma-Fiumicino"),
    ("Roma Ciampino", "Roma-Ciampino"), ("Naples", "Nápoles"), ("Napoli", "Nápoles"), ("Florence", "Florencia"),
    ("Firenze", "Florencia"), ("Venice", "Venecia"), ("Venezia", "Venecia"), ("Bologna", "Bolonia"),
    ("Athens", "Atenas"), ("Atenas", "Atenas"), ("Corfu", "Corfú"), ("Kerkyra", "Corfú"), ("Heraklion", "Heraclión"),
    ("Iraklion", "Heraclión"), ("Chania", "Chania"), ("La Canea", "Chania"), ("Rhodes", "Rodas"),
    ("Thessaloniki", "Tesalónica"), ("Kefalonia", "Cefalonia"), ("Santorini", "Santorini"), ("Thira", "Santorini"),
    ("Catania", "Catania"), ("Olbia", "Olbia"), ("Cagliari", "Cagliari"), ("Palermo", "Palermo"), ("Pisa", "Pisa"),
    ("Bari", "Bari"), ("Bilbao", "Bilbao"), ("Ibiza", "Ibiza"), ("Faro", "Faro"),
]
for dicho, esperado in NOMBRES:
    comprobar("identificar %r" % dicho, identificar(dicho)[0], esperado)

# Nombres que no son de un aeropuerto concreto pero sí de una zona (todas sus oficinas cierran igual)
for dicho, zona in (("Milán", "cet"), ("Roma", "cet"), ("Creta", "eet"), ("Cerdeña", "cet"), ("Sicilia", "cet"),
                    ("Canarias", "wet")):
    nombre, zona_obtenida, apertura = identificar(dicho)
    comprobar("zona genérica %r" % dicho, (zona_obtenida, apertura), (zona, 7))

for dicho in ("", None, "Zaragoza", "Ámsterdam", "la estación de tren"):
    comprobar("desconocido %r" % dicho, identificar(dicho), (None, None, None))

# 3. Con los valores de «Contexto de la llamada» (lo normal en una llamada y en las evals)
caso = estado(entrada("Valencia", **NOCHE), MARTES_10_00)
comprobar("Valencia de noche", (caso["oficina_cerrada"], caso["aeropuerto"], caso["reconocido"]),
          (True, "Valencia", True))
comprobar("Valencia de noche: apertura", caso["hora_apertura"], "siete de la mañana, hora local")
comprobar("Valencia de noche: instrucción de cierre", "no des el punto de encuentro" in caso["instruccion"], True)
# El vuelo retrasado lo lleva el prompt (PRIMERO): nombrarlo aquí hacía que el bot preguntara por retrasos (ronda A2)
comprobar("Valencia de noche: sin hablar de retrasos", "retras" in caso["instruccion"], False)
caso = estado(entrada("Valencia", **DIA), MARTES_05_30)  # el reloj dice noche, pero manda el contexto
comprobar("Valencia de día", caso["oficina_cerrada"], False)
comprobar("Valencia de día: instrucción", "QUÉ HACER AHORA" in caso["instruccion"], True)
comprobar("Valencia de día: fuente", caso["fuente"], "contexto")
comprobar("Valencia de día: queja", "EL BUS TARDA DEMASIADO" in caso["instruccion"], True)

# Cada aeropuerto lee solo el valor de su lista
SOLO = {
    "cet": dict(DIA, nocturno_cet="true"), "wet": dict(DIA, nocturno_wet="true"),
    "eet": dict(DIA, nocturno_eet="true"), "murcia": dict(DIA, nocturno_murcia="true"),
}
for zona_activa, valores in SOLO.items():
    for zona, nombres in LISTAS_V2.items():
        for nombre in nombres:
            comprobar("%s con solo %s cerrado" % (nombre, zona_activa),
                      estado(entrada(nombre, **valores), MARTES_10_00)["oficina_cerrada"], zona == zona_activa)

comprobar("Murcia abre a las ocho", estado(entrada("Murcia", **NOCHE))["hora_apertura"],
          "ocho de la mañana, hora local")
comprobar("Nápoles abre a las ocho", estado(entrada("Naples", **NOCHE))["hora_apertura"],
          "ocho de la mañana, hora local")
comprobar("Atenas abre a las siete", estado(entrada("Athens", **NOCHE))["hora_apertura"],
          "siete de la mañana, hora local")

# Formatos en que pueden llegar los booleanos desde las variables
for valor, cerrado in (("true", True), ("True", True), (True, True), ("1", True), (" TRUE ", True),
                       ("false", False), ("False", False), (False, False), ("0", False)):
    comprobar("valor %r" % (valor,), estado(entrada("Sevilla", nocturno_cet=valor), MARTES_10_00)["oficina_cerrada"],
              cerrado)

# 4. Aeropuerto desconocido: el valor de la LISTA 1 (regla del prompt), sin inventar la hora de apertura
caso = estado(entrada("Zaragoza", **dict(DIA, nocturno_cet="true")), MARTES_10_00)
comprobar("desconocido: LISTA 1", (caso["oficina_cerrada"], caso["reconocido"], caso["aeropuerto"]),
          (True, False, "Zaragoza"))
comprobar("desconocido: apertura genérica", caso["hora_apertura"], "siete de la mañana, hora local")
caso = estado(entrada("Zaragoza", **DIA), MARTES_10_00)
comprobar("desconocido de día", caso["oficina_cerrada"], False)
comprobar("sin aeropuerto", estado(entrada("", **NOCHE), MARTES_10_00)["oficina_cerrada"], True)

# 5. Sin valor del contexto (variable sin resolver o vacía): el reloj, con las mismas franjas que contexto_llamada.py
SIN_VALOR = {"nocturno_cet": "", "nocturno_wet": "{{e51cd732.nocturno_wet}}", "nocturno_eet": None}
for ahora, nombre, cerrado in (
        (MARTES_05_30, "Valencia", True), (MARTES_05_30, "Lisboa", True), (MARTES_05_30, "Atenas", True),
        (MARTES_06_30, "Atenas", False), (MARTES_07_30, "Murcia", True), (MARTES_07_30, "Valencia", False),
        (MARTES_10_00, "Murcia", False), (MARTES_22_30, "Murcia", True), (MARTES_22_30, "Madrid", False),
        (MARTES_22_30, "Atenas", True), (MARTES_23_30, "Madrid", True), (MARTES_23_30, "Lisboa", False)):
    caso = estado(entrada(nombre, **SIN_VALOR), ahora)
    comprobar("reloj %s %s" % (nombre, ahora.strftime("%H:%M UTC")), (caso["oficina_cerrada"], caso["fuente"]),
              (cerrado, "reloj"))

# El reloj da lo mismo que contexto_llamada.py en cada cuarto de hora de una semana con cambio de hora
t = datetime(2026, 10, 22, 0, 0, tzinfo=UTC)
distintos = []
for _ in range(7 * 96):
    ctx = contexto_llamada.contexto({}, t)
    for zona, nombre in (("cet", "Valencia"), ("wet", "Lisboa"), ("eet", "Atenas"), ("murcia", "Murcia")):
        if estado(entrada(nombre), t)["oficina_cerrada"] != ctx["nocturno_" + zona]:
            distintos.append((nombre, t.isoformat()))
    t += timedelta(minutes=15)
comprobar("reloj igual que contexto_llamada.py", distintos[:3], [])

# 6. El prompt de Punto de encuentro ya no lleva las listas ni las variables nocturno_* (R39)
with open(RUTA_PROMPT, encoding="utf-8") as f:
    prompt = f.read().split("## Configuración")[0]
comprobar("prompt sin LISTA 1", "LISTA 1" in prompt, False)
comprobar("prompt sin nocturno_*", "nocturno_" in prompt, False)
comprobar("prompt con estado_oficina", "estado_oficina" in prompt, True)

# 7. El nodo solo usa la biblioteca estándar y deja el resultado en `output`
with open(RUTA_NODO, encoding="utf-8") as f:
    codigo = f.read()
importados = set()
for nodo in ast.walk(ast.parse(codigo)):
    if isinstance(nodo, ast.Import):
        importados |= {a.name.split(".")[0] for a in nodo.names}
    elif isinstance(nodo, ast.ImportFrom):
        importados.add((nodo.module or "").split(".")[0])
comprobar("imports", sorted(importados - {"datetime", "unicodedata", "re"}), [])
espacio = {"input_data": entrada("Valencia", **NOCHE)}
exec(compile(codigo, RUTA_NODO, "exec"), espacio)
comprobar("ejecución como nodo", espacio.get("output", {}).get("oficina_cerrada"), True)

print("%d/%d casos correctos" % (total - fallos, total))
sys.exit(1 if fallos else 0)
