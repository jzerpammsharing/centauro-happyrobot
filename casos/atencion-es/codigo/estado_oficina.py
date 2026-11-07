# ===============================================================
# ESTADO DE LA OFICINA - bot único de Atención España (R39, Tarea 15b; hora del momento, Tarea 16, R45)
# ---------------------------------------------------------------
# Se pega tal cual en el nodo Python «Estado de la oficina», hijo de la herramienta estado_oficina de Punto de
# encuentro. Sustituye a las LISTAS 1 a 4 del prompt: el modelo ya no cruza el aeropuerto con las listas, recibe el
# dato resuelto.
#
# Entradas (input_data):
#   aeropuerto    el nombre que dice el modelo (argumento de la herramienta), en cualquier idioma
#   hora_prueba   la variable del workflow HORA_PRUEBA: «ninguna» en producción; en las evals, una hora peninsular
#                 «HH:MM» que manda sobre el reloj (así la eval no depende de la hora a la que se ejecuta)
#
# Salidas: aeropuerto (nombre de la tabla o, si no se reconoce, el que llegó), reconocido (bool), oficina_cerrada
# (bool), hora_apertura (en palabras), instruccion (para el agente) y fuente (reloj | prueba).
#
# - La hora es la del momento en que se ejecuta la herramienta (mismo criterio que «Preparar transferencia»), no la
#   del principio de la llamada: una llamada que empieza a las 22:55 y pregunta a las 23:05 ya oye que ha cerrado.
# - Horario de cada oficina en hora local del aeropuerto, el mismo que dice el prompt (HORARIO Y DEVOLUCIÓN EN
#   AEROPUERTOS): de 7:00 a 23:00, salvo Murcia (8:00–22:00), Alicante (7:00–23:30) y Bari, Florencia, Nápoles y
#   Venecia (8:00–23:00). Hora local: cet (España peninsular, Baleares e Italia; también Murcia), wet (Portugal y
#   Canarias) y eet (Grecia).
# - Aeropuerto desconocido: horario general en hora peninsular (la regla «si no está en ninguna lista, usa la LISTA 1»).
# - Las funciones de hora son copia de contexto_llamada.py (un nodo no puede importar otro fichero): si cambian allí,
#   cambian aquí. La prueba comprueba que, con el horario general, dan lo mismo que las nocturno_* de allí.
# ===============================================================
import re
import unicodedata
from datetime import datetime, timedelta, timezone

# Aeropuerto (nombre del prompt) -> (zona, hora de apertura). Cierre: CIERRE o, si no está, CIERRE_GENERAL
AEROPUERTOS = {
    # LISTA 1 (cet)
    "Madrid": ("cet", 7), "Barcelona": ("cet", 7), "Bilbao": ("cet", 7), "Ibiza": ("cet", 7),
    "Málaga": ("cet", 7), "Palma de Mallorca": ("cet", 7), "Santiago de Compostela": ("cet", 7),
    "Sevilla": ("cet", 7), "Valencia": ("cet", 7), "Alicante": ("cet", 7), "Almería": ("cet", 7),
    "Menorca": ("cet", 7), "Bari": ("cet", 8), "Bolonia": ("cet", 7), "Cagliari": ("cet", 7),
    "Florencia": ("cet", 8), "Milán-Bérgamo": ("cet", 7), "Milán-Malpensa": ("cet", 7), "Nápoles": ("cet", 8),
    "Olbia": ("cet", 7), "Palermo": ("cet", 7), "Pisa": ("cet", 7), "Roma-Ciampino": ("cet", 7),
    "Roma-Fiumicino": ("cet", 7), "Catania": ("cet", 7), "Venecia": ("cet", 8),
    # LISTA 2 (wet)
    "Faro": ("wet", 7), "Lisboa": ("wet", 7), "Madeira": ("wet", 7), "Oporto": ("wet", 7),
    "Gran Canaria": ("wet", 7), "Tenerife Sur": ("wet", 7),
    # LISTA 3 (eet)
    "Atenas": ("eet", 7), "Cefalonia": ("eet", 7), "Corfú": ("eet", 7), "Chania": ("eet", 7),
    "Heraclión": ("eet", 7), "Rodas": ("eet", 7), "Santorini": ("eet", 7), "Tesalónica": ("eet", 7),
    # LISTA 4
    "Murcia": ("murcia", 8),
}

# Otras formas de decir cada aeropuerto (sin tildes y en minúsculas; el nombre de la tabla ya cuenta)
ALIAS = {
    "Madrid": ["barajas", "adolfo suarez"],
    "Barcelona": ["el prat"],
    "Málaga": ["costa del sol"],
    "Palma de Mallorca": ["palma", "mallorca", "son sant joan"],
    "Santiago de Compostela": ["santiago", "rosalia de castro"],
    "Sevilla": ["seville", "san pablo"],
    "Alicante": ["elche"],
    "Menorca": ["mahon", "mao"],
    "Bolonia": ["bologna"],
    "Florencia": ["florence", "firenze"],
    "Milán-Bérgamo": ["bergamo", "orio al serio"],
    "Milán-Malpensa": ["malpensa"],
    "Nápoles": ["naples", "napoli"],
    "Roma-Ciampino": ["ciampino"],
    "Roma-Fiumicino": ["fiumicino"],
    "Venecia": ["venice", "venezia", "marco polo"],
    "Lisboa": ["lisbon"],
    "Madeira": ["funchal"],
    "Oporto": ["porto"],
    "Gran Canaria": ["las palmas"],
    "Tenerife Sur": ["tenerife"],
    "Atenas": ["athens", "athina"],
    "Cefalonia": ["kefalonia", "cephalonia"],
    "Corfú": ["corfu", "kerkyra"],
    "Chania": ["hania", "la canea", "canea"],
    "Heraclión": ["heraklion", "iraklion", "iraklio"],
    "Rodas": ["rhodes", "rodos"],
    "Santorini": ["thira", "fira"],
    "Tesalónica": ["thessaloniki", "salonica"],
    "Murcia": ["corvera"],
}

# Nombres de una ciudad o una isla con varios aeropuertos, todos de la misma zona y con la misma apertura
GENERICOS = {
    "milan": ("Milán", "cet", 7), "roma": ("Roma", "cet", 7), "rome": ("Roma", "cet", 7),
    "creta": ("Creta", "eet", 7), "crete": ("Creta", "eet", 7),
    "cerdena": ("Cerdeña", "cet", 7), "sardinia": ("Cerdeña", "cet", 7), "sardegna": ("Cerdeña", "cet", 7),
    "sicilia": ("Sicilia", "cet", 7), "sicily": ("Sicilia", "cet", 7),
    "canarias": ("Canarias", "wet", 7), "canary": ("Canarias", "wet", 7),
}

# Hora de cierre en minutos desde medianoche (hora local del aeropuerto)
CIERRE_GENERAL = 23 * 60
CIERRE = {"Murcia": 22 * 60, "Alicante": 23 * 60 + 30}

APERTURA_TEXTO = {7: "siete de la mañana, hora local", 8: "ocho de la mañana, hora local"}

INSTRUCCION_CERRADA = (
    "La oficina de este aeropuerto ya ha cerrado por hoy y abre a las {apertura}. Sigue PRIMERO: da solo el aviso "
    "de cierre con esa hora; no des el punto de encuentro ni ninguna indicación, no preguntes la terminal ni la "
    "puerta y no transfieras."
)
INSTRUCCION_ABIERTA = (
    "La oficina de este aeropuerto está abierta: sigue con QUÉ HACER AHORA y dale el punto de encuentro; si se queja "
    "de que el minibús no pasa o se ha ido, sigue SI «EL BUS TARDA DEMASIADO» y ESCALADO."
)

# ---------------------------------------------------------------
# Copia de contexto_llamada.py (mantener igual)
# ---------------------------------------------------------------
# Desfase base respecto a UTC en horario de invierno
BASE = {
    "wet": 0,  # Portugal y Madeira
    "cet": 1,  # España peninsular, Baleares e Italia
    "eet": 2,  # Grecia
}


def _en_utc(t):
    if t.tzinfo is None:
        return t.replace(tzinfo=timezone.utc)
    return t.astimezone(timezone.utc)


def ultimo_domingo(anio, mes):
    # Primer día del mes siguiente, retrocediendo al domingo anterior
    if mes == 12:
        d = datetime(anio + 1, 1, 1, tzinfo=timezone.utc)
    else:
        d = datetime(anio, mes + 1, 1, tzinfo=timezone.utc)
    d = d - timedelta(days=1)
    while d.weekday() != 6:  # 6 = domingo
        d = d - timedelta(days=1)
    return d


def en_horario_verano_ue(t):
    # Reglas UE: empieza el último domingo de marzo a las 01:00 UTC
    # y termina el último domingo de octubre a las 01:00 UTC
    t = _en_utc(t)
    inicio = ultimo_domingo(t.year, 3).replace(hour=1)
    fin = ultimo_domingo(t.year, 10).replace(hour=1)
    return inicio <= t < fin


def hora_local(ahora_utc, base):
    """Hora local de una zona con `base` horas de desfase en invierno (una más en horario de verano)."""
    t = _en_utc(ahora_utc)
    desfase = base + (1 if en_horario_verano_ue(t) else 0)
    return t.astimezone(timezone(timedelta(hours=desfase)))


# ---------------------------------------------------------------
# Aeropuerto y estado
# ---------------------------------------------------------------
def _normalizar(texto):
    sin_tildes = unicodedata.normalize("NFKD", str(texto or "")).encode("ascii", "ignore").decode("ascii")
    return " " + " ".join(re.sub(r"[^a-z0-9]+", " ", sin_tildes.lower()).split()) + " "


# (forma normalizada, nombre, zona, apertura), de la más larga a la más corta: gana la coincidencia más larga
_FORMAS = []
for _nombre, (_zona, _apertura) in AEROPUERTOS.items():
    for _forma in [_nombre] + ALIAS.get(_nombre, []):
        _FORMAS.append((_normalizar(_forma), _nombre, _zona, _apertura))
for _forma, (_nombre, _zona, _apertura) in GENERICOS.items():
    _FORMAS.append((_normalizar(_forma), _nombre, _zona, _apertura))
_FORMAS.sort(key=lambda f: -len(f[0]))


def identificar(aeropuerto):
    """(nombre, zona, hora de apertura) del aeropuerto dicho, o (None, None, None) si no se reconoce."""
    texto = _normalizar(aeropuerto)
    for forma, nombre, zona, apertura in _FORMAS:
        if forma in texto:
            return nombre, zona, apertura
    return None, None, None


def _hora_prueba(valor):
    """(horas, minutos) si el valor es una hora «HH:MM» válida; None si no (vacío, «ninguna» o sin resolver)."""
    m = re.fullmatch(r"\s*(\d{1,2}):(\d{2})\s*", str(valor if valor is not None else ""))
    if not m:
        return None
    horas, minutos = int(m.group(1)), int(m.group(2))
    if horas > 23 or minutos > 59:
        return None
    return horas, minutos


def momento_prueba(hora, ahora_utc):
    """El instante UTC de la hora peninsular `hora` (horas, minutos) en el día peninsular de `ahora_utc`."""
    madrid = hora_local(ahora_utc, BASE["cet"])
    local = madrid.replace(hour=hora[0], minute=hora[1], second=0, microsecond=0)
    return local.astimezone(timezone.utc)


def cerrada_en(nombre, zona, apertura, ahora_utc):
    local = hora_local(ahora_utc, BASE["cet" if zona == "murcia" else zona])
    minuto = local.hour * 60 + local.minute
    return not (apertura * 60 <= minuto < CIERRE.get(nombre, CIERRE_GENERAL))


def estado(input_data, ahora_utc=None):
    dicho = str(input_data.get("aeropuerto") or "").strip()
    nombre, zona, apertura = identificar(dicho)
    reconocido = nombre is not None
    if not reconocido:
        nombre, zona, apertura = dicho, "cet", 7

    ahora = _en_utc(ahora_utc or datetime.now(timezone.utc))
    prueba = _hora_prueba(input_data.get("hora_prueba"))
    fuente = "reloj"
    if prueba is not None:
        ahora = momento_prueba(prueba, ahora)
        fuente = "prueba"
    cerrada = cerrada_en(nombre, zona, apertura, ahora)

    texto_apertura = APERTURA_TEXTO[apertura]
    return {
        "aeropuerto": nombre,
        "reconocido": reconocido,
        "oficina_cerrada": cerrada,
        "hora_apertura": texto_apertura,
        "instruccion": INSTRUCCION_CERRADA.format(apertura=texto_apertura) if cerrada else INSTRUCCION_ABIERTA,
        "fuente": fuente,
    }


try:
    _entrada = input_data  # noqa: F821 (lo inyecta el nodo Python de HappyRobot)
except NameError:  # importado desde las pruebas locales
    _entrada = None
if _entrada is not None:
    output = estado(_entrada)
