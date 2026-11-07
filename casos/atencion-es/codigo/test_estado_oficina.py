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

# 3. Producción: manda el reloj del momento en que se ejecuta la herramienta, nunca las nocturno_* del principio de
#    la llamada (R45). Las nocturno_* ya no son entradas: si llegan, no cuentan.
caso = estado(entrada("Valencia", **NOCHE), MARTES_10_00)
comprobar("Valencia 10:00 con nocturno_* true: manda el reloj", (caso["oficina_cerrada"], caso["fuente"]),
          (False, "reloj"))
caso = estado(entrada("Valencia", **DIA), MARTES_05_30)
comprobar("Valencia 05:30 con nocturno_* false: manda el reloj", (caso["oficina_cerrada"], caso["fuente"]),
          (True, "reloj"))
comprobar("Valencia de noche: apertura", caso["hora_apertura"], "siete de la mañana, hora local")
comprobar("Valencia de noche: instrucción de cierre", "no des el punto de encuentro" in caso["instruccion"], True)
# El vuelo retrasado lo lleva el prompt (PRIMERO): nombrarlo aquí hacía que el bot preguntara por retrasos (ronda A2)
comprobar("Valencia de noche: sin hablar de retrasos", "retras" in caso["instruccion"], False)
caso = estado(entrada("Valencia"), MARTES_10_00)
comprobar("Valencia de día", caso["oficina_cerrada"], False)
comprobar("Valencia de día: instrucción", "QUÉ HACER AHORA" in caso["instruccion"], True)
comprobar("Valencia de día: queja", "EL BUS TARDA DEMASIADO" in caso["instruccion"], True)

# Valores de hora_prueba que no son una hora (producción: la variable del workflow vale «ninguna»): el reloj
for valor in (None, "", "ninguna", "{{use_case_variables.HORA_PRUEBA}}", "25:00", "23", "mañana"):
    caso = estado(entrada("Valencia", hora_prueba=valor), MARTES_05_30)
    comprobar("hora_prueba %r → reloj" % (valor,), (caso["oficina_cerrada"], caso["fuente"]), (True, "reloj"))

# 4. Horario concreto de cada oficina (hora local del aeropuerto), el mismo que dice el prompt en HORARIO Y
#    DEVOLUCIÓN EN AEROPUERTOS: de 7:00 a 23:00, salvo Murcia (8:00–22:00), Alicante (7:00–23:30) y Bari, Florencia,
#    Nápoles y Venecia (8:00–23:00). Martes 20/10/2026, horario de verano.
def a_utc_madrid(hh, mm):
    return datetime(2026, 10, 20, hh, mm, tzinfo=UTC) - timedelta(hours=2)

for hh, mm, nombre, cerrado in (
        (6, 59, "Valencia", True), (7, 0, "Valencia", False), (22, 59, "Valencia", False), (23, 0, "Valencia", True),
        (23, 15, "Alicante", False), (23, 29, "Alicante", False), (23, 30, "Alicante", True), (6, 59, "Alicante", True),
        (7, 30, "Bari", True), (7, 30, "Florencia", True), (7, 30, "Nápoles", True), (7, 30, "Venecia", True),
        (8, 0, "Bari", False), (22, 59, "Venecia", False), (23, 0, "Nápoles", True),
        (7, 30, "Murcia", True), (8, 0, "Murcia", False), (21, 59, "Murcia", False), (22, 0, "Murcia", True),
        (23, 30, "Lisboa", False),    # 22:30 en Lisboa
        (0, 30, "Lisboa", True),      # 23:30 en Lisboa
        (7, 30, "Lisboa", True),      # 06:30 en Lisboa
        (8, 0, "Lisboa", False),      # 07:00 en Lisboa
        (22, 30, "Atenas", True),     # 23:30 en Atenas
        (6, 30, "Atenas", False),     # 07:30 en Atenas
        (5, 59, "Atenas", True),      # 06:59 en Atenas
        (23, 15, "Zaragoza", True),   # desconocido: horario general de la LISTA 1
        (10, 0, "Zaragoza", False)):
    caso = estado(entrada(nombre), a_utc_madrid(hh, mm))
    comprobar("reloj %s %02d:%02d Madrid" % (nombre, hh, mm), (caso["oficina_cerrada"], caso["fuente"]),
              (cerrado, "reloj"))

# La herramienta no se contradice: si dice que está cerrada con hora_apertura «ocho», a las 7:30 no puede estar abierta
for nombre in ABREN_A_LAS_OCHO:
    caso = estado(entrada(nombre), a_utc_madrid(7, 30))
    comprobar("%s 07:30: cerrada y abre a las ocho" % nombre, (caso["oficina_cerrada"], caso["hora_apertura"]),
              (True, "ocho de la mañana, hora local"))

comprobar("Nápoles abre a las ocho", estado(entrada("Naples"), MARTES_05_30)["hora_apertura"],
          "ocho de la mañana, hora local")
comprobar("Atenas abre a las siete", estado(entrada("Athens"), MARTES_05_30)["hora_apertura"],
          "siete de la mañana, hora local")
caso = estado(entrada("Zaragoza"), MARTES_05_30)
comprobar("desconocido: LISTA 1", (caso["oficina_cerrada"], caso["reconocido"], caso["aeropuerto"]),
          (True, False, "Zaragoza"))
comprobar("desconocido: apertura genérica", caso["hora_apertura"], "siete de la mañana, hora local")
comprobar("sin aeropuerto de noche", estado(entrada(""), MARTES_05_30)["oficina_cerrada"], True)

# 5. Variable de prueba hora_prueba (HH:MM, hora peninsular; la variable del workflow HORA_PRUEBA): manda sobre el
#    reloj, para que las evals no dependan de la hora a la que se ejecutan.
for hora, nombre, cerrado in (
        ("23:15", "Valencia", True), ("23:15", "Alicante", False), ("23:45", "Alicante", True),
        ("10:00", "Valencia", False), ("7:30", "Bari", True), ("08:30", "Venecia", False),
        ("22:30", "Atenas", True), ("23:30", "Lisboa", False), ("21:30", "Murcia", False), ("22:15", "Murcia", True),
        ("02:00", "Madrid", True), (" 23:15 ", "Valencia", True)):
    for ahora in (MARTES_10_00, MARTES_23_30):
        caso = estado(entrada(nombre, hora_prueba=hora), ahora)
        comprobar("hora_prueba %s %s (reloj %s)" % (hora, nombre, ahora.strftime("%H:%M UTC")),
                  (caso["oficina_cerrada"], caso["fuente"]), (cerrado, "prueba"))
# hora_prueba también manda sobre las nocturno_* si alguien las pasa
comprobar("hora_prueba sobre nocturno_*",
          estado(entrada("Valencia", hora_prueba="10:00", **NOCHE), MARTES_05_30)["oficina_cerrada"], False)

# El reloj da lo mismo que contexto_llamada.py en los aeropuertos con el horario general (y Murcia) en cada cuarto de
# hora de una semana con cambio de hora
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
espacio = {"input_data": entrada("Valencia", hora_prueba="23:15")}
exec(compile(codigo, RUTA_NODO, "exec"), espacio)
comprobar("ejecución como nodo", espacio.get("output", {}).get("oficina_cerrada"), True)

print("%d/%d casos correctos" % (total - fallos, total))
sys.exit(1 if fallos else 0)
