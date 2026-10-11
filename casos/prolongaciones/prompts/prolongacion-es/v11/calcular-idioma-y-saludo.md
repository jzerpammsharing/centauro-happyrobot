<!-- workflow: 01a0d9de-b1cd-7bc9-bafc-f5117bd57249 · versión: Version 11 (2g1bxzyzazpp) · nodo: Calcular idioma y saludo · copiado: 2026-10-11 -->

Python Sandbox (Code). Persistent ID `01a0da06-917d-7e9c-9b1c-153df5946a48`. No es un prompt: se guarda
porque decide el idioma, el saludo y el horario de la cola de Gestión.

- **Entradas:** `to_number` y `from_number` de Inbound Call (`01a0da06-7f3b-7b5a-9af0-e424300d057c`).
- **Salidas:** `idioma`, `idioma_nombre`, `numero_marcado`, `hora_cet`, `saludo`, `mensaje_inicial`,
  `recording_id`, `telefono_dictado` y `gestion_abierta`.
- **Execution profile:** standard.

> Copia literal salvo una línea: el número de la línea en inglés de `NUMEROS_IDIOMA` se sustituye por
> `<LINEA_EN>`, porque el repo no guarda teléfonos.

```python
from datetime import datetime, timedelta, timezone

# ===============================================================
# IDIOMA, SALUDO Y AVISO LEGAL - CENTAURO PROLONGACION SPAIN
# ---------------------------------------------------------------
# Este flujo tiene un unico horario: el agente atiende siempre.
# No hay logica nocturna.
#
# Para anadir un idioma:
#   1. Anade su numero de linea en NUMEROS_IDIOMA.
#   2. Anade su bloque en IDIOMAS (nombre, saludos, mensaje, grabacion).
#   3. Anade sus colas en el nodo "Resolver colas por idioma".
# ===============================================================

# Numero marcado (solo digitos, con prefijo de pais) -> idioma
# Formato: "NUMERO": "codigo_idioma"
NUMEROS_IDIOMA = {
    "<LINEA_EN>": "en",
}

IDIOMA_RESPALDO = "es"

IDIOMAS = {
    "es": {
        "nombre": "espanol",
        "manana": "buenos días",
        "tarde": "buenas tardes",
        "mensaje": "Centauro Rent a Car, {saludo}, le atiende Daniel. Cuénteme, ¿quiere prolongar un alquiler que tiene en curso?",
        # greetinminibus-es (misma grabacion que minibus)
        "recording_id": "019fd44b-56a4-7a06-b240-1ede829ccceb",
    },
    "en": {
        "nombre": "ingles (English)",
        "manana": "good morning",
        "tarde": "good afternoon",
        "mensaje": "Centauro Rent a Car, {saludo}, this is Daniel speaking. Would you like to extend a rental you currently have?",
        # PENDIENTE: sustituir por el ID de la grabacion de aviso legal en ingles.
        # De momento usa la grabacion en espanol.
        "recording_id": "019fd44b-56a4-7a06-b240-1ede829ccceb",
    },
}

# ---------------------------------------------------------------
# Hora local de Espana peninsular (CET/CEST, reglas UE)
# ---------------------------------------------------------------
ahora_utc = datetime.now(timezone.utc)


def ultimo_domingo(anio, mes):
    if mes == 12:
        d = datetime(anio + 1, 1, 1, tzinfo=timezone.utc)
    else:
        d = datetime(anio, mes + 1, 1, tzinfo=timezone.utc)
    d = d - timedelta(days=1)
    while d.weekday() != 6:
        d = d - timedelta(days=1)
    return d


inicio_verano = ultimo_domingo(ahora_utc.year, 3).replace(hour=1)
fin_verano = ultimo_domingo(ahora_utc.year, 10).replace(hour=1)
verano = inicio_verano <= ahora_utc < fin_verano
hora_cet = (ahora_utc + timedelta(hours=2 if verano else 1)).hour

# ---------------------------------------------------------------
# Idioma segun el numero marcado
# ---------------------------------------------------------------
to_number_raw = input_data.get("to_number") or ""
digitos = "".join(c for c in str(to_number_raw) if c.isdigit())

idioma = IDIOMA_RESPALDO
for clave, valor in NUMEROS_IDIOMA.items():
    # Acepta los dos ordenes: "numero": "idioma" o "idioma": "numero"
    if clave in IDIOMAS:
        numero, codigo = valor, clave
    else:
        numero, codigo = clave, valor
    numero = "".join(c for c in str(numero) if c.isdigit())
    if digitos and numero and digitos.endswith(numero):
        idioma = codigo
        break
if idioma not in IDIOMAS:
    idioma = IDIOMA_RESPALDO

datos = IDIOMAS[idioma]

# Solo dos franjas: buenos dias (06:00-13:00) y buenas tardes el resto
saludo = datos["manana"] if 6 <= hora_cet < 13 else datos["tarde"]

# ---------------------------------------------------------------
# Telefono del cliente dictado digito a digito (para el whisper)
# ---------------------------------------------------------------
PALABRAS = {"0": "cero", "1": "uno", "2": "dos", "3": "tres", "4": "cuatro",
            "5": "cinco", "6": "seis", "7": "siete", "8": "ocho", "9": "nueve"}


def dictar(d):
    grupos = [d[i:i + 3] for i in range(0, len(d), 3)]
    return ", ".join(" ".join(PALABRAS[c] for c in g) for g in grupos)


from_raw = str(input_data.get("from_number") or "").strip()
tel = "".join(c for c in from_raw if c.isdigit())
if from_raw.startswith("00"):
    tel = tel[2:]
    internacional = True
else:
    internacional = from_raw.startswith("+")

if len(tel) < 6:
    telefono_dictado = "número oculto"
elif internacional and tel.startswith("34") and len(tel) == 11:
    telefono_dictado = dictar(tel[2:])
elif internacional:
    # Prefijo de pais extranjero: se dicta completo con aviso
    telefono_dictado = "internacional, más " + dictar(tel)
else:
    telefono_dictado = dictar(tel)

output = {
    "idioma": idioma,
    "idioma_nombre": datos["nombre"],
    "numero_marcado": digitos,
    "hora_cet": "%02d:00" % hora_cet,
    "saludo": saludo,
    "mensaje_inicial": datos["mensaje"].format(saludo=saludo),
    "recording_id": datos["recording_id"],
    "telefono_dictado": telefono_dictado,
}

# Cola de GESTION DE RESERVA: solo L-V de 08:00 a 21:00 (hora peninsular).
# Fuera de ese horario suena una locucion de cerrado: no transferir alli.
local_cet = ahora_utc + timedelta(hours=2 if verano else 1)
output["gestion_abierta"] = local_cet.weekday() < 5 and 8 <= local_cet.hour < 21
```
