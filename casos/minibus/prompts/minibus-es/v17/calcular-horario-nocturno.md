<!-- workflow: 019f7594-2cce-7eed-b995-dd9ea64a1062 · versión: v17 (i0syf61bujsz) · nodo: Calcular horario nocturno · copiado: 2026-10-11 -->

# Calcular horario nocturno (código Python)

- Tipo: action (Python), event_id `019dde7b-3500-7a3c-8f5e-1c2d4e6a8b9c`
- persistent_id: `019fd418-5a5d-7bd4-93f8-eae309f8dc7a`
- execution_profile: `standard`
- Redacción: los números de teléfono completos de las líneas ES/EN se sustituyen por [REDACTADO].

## Código

```python
from datetime import datetime, timedelta, timezone

# Oficina de aeropuerto cerrada: de 23:00 a 07:00 (hora local del aeropuerto).
# Los flags nocturno_* indican si la oficina (y su minibus) ya ha cerrado.
NOCHE_INICIO = 23
NOCHE_FIN = 7

# Murcia cierra antes: de 22:00 a 08:00 (hora peninsular)
MURCIA_INICIO = 22
MURCIA_FIN = 8

# Centro de atencion con operadores: de 08:00 a 22:00 (hora peninsular).
# Fuera de esa franja el agente atiende en modo virtual, sin transferencias.
CALLCENTER_INICIO = 8
CALLCENTER_FIN = 22

ahora_utc = datetime.now(timezone.utc)


def ultimo_domingo(anio, mes):
    # Primer dia del mes siguiente, retrocediendo al domingo anterior
    if mes == 12:
        d = datetime(anio + 1, 1, 1, tzinfo=timezone.utc)
    else:
        d = datetime(anio, mes + 1, 1, tzinfo=timezone.utc)
    d = d - timedelta(days=1)
    while d.weekday() != 6:  # 6 = domingo
        d = d - timedelta(days=1)
    return d


def en_horario_verano_ue(t):
    # Reglas UE: empieza el ultimo domingo de marzo a las 01:00 UTC
    # y termina el ultimo domingo de octubre a las 01:00 UTC
    inicio = ultimo_domingo(t.year, 3).replace(hour=1)
    fin = ultimo_domingo(t.year, 10).replace(hour=1)
    return inicio <= t < fin


verano = en_horario_verano_ue(ahora_utc)

# Desfase base respecto a UTC en horario de invierno
BASE = {
    "wet": 0,  # Portugal y Madeira
    "cet": 1,  # Espana peninsular, Baleares e Italia
    "eet": 2,  # Grecia
}


def es_nocturno(hora):
    # Ventana que cruza medianoche
    return hora >= NOCHE_INICIO or hora < NOCHE_FIN


output = {"horario_verano": verano}

for clave, base in BASE.items():
    desfase = base + (1 if verano else 0)
    local = ahora_utc + timedelta(hours=desfase)
    output["nocturno_" + clave] = es_nocturno(local.hour)
    output["hora_" + clave] = local.strftime("%H:%M")

# Franja del dia para el saludo, referida a CET
hora_cet = (ahora_utc + timedelta(hours=BASE["cet"] + (1 if verano else 0))).hour

output["nocturno_murcia"] = hora_cet >= MURCIA_INICIO or hora_cet < MURCIA_FIN
output["callcenter_abierto"] = CALLCENTER_INICIO <= hora_cet < CALLCENTER_FIN
output["modo_virtual"] = not output["callcenter_abierto"]
if 6 <= hora_cet < 13:
    output["saludo"] = "buenos dias"
elif 13 <= hora_cet < 21:
    output["saludo"] = "buenas tardes"
else:
    output["saludo"] = "buenas noches"

# ---------------------------------------------------------------
# Idioma de atencion segun el numero marcado por el cliente
# ---------------------------------------------------------------
# Linea en espanol: [REDACTADO]
# Linea en ingles:  [REDACTADO]
NUMERO_INGLES = "[REDACTADO]"

to_number_raw = input_data.get("to_number") or ""
# Nos quedamos solo con los digitos para que el formato no afecte
digitos = "".join(c for c in str(to_number_raw) if c.isdigit())

# Por defecto espanol: si el numero llega vacio o irreconocible,
# preferimos caer en el idioma de la linea principal
if digitos.endswith(NUMERO_INGLES):
    idioma = "en"
else:
    idioma = "es"

output["idioma"] = idioma
output["idioma_nombre"] = "English" if idioma == "en" else "espanol"
output["numero_marcado"] = digitos

# Saludo equivalente en ingles, con la misma franja horaria CET
if 6 <= hora_cet < 13:
    output["saludo_en"] = "good morning"
elif 13 <= hora_cet < 21:
    output["saludo_en"] = "good afternoon"
else:
    output["saludo_en"] = "good evening"

# Saludo ya resuelto en el idioma que toca
output["saludo_localizado"] = output["saludo_en"] if idioma == "en" else output["saludo"]

# Mensaje inicial completo, listo para el campo de saludo del agente.
# En modo virtual avisa desde el principio de que no hay operadores.
if output["modo_virtual"]:
    if idioma == "en":
        output["mensaje_inicial"] = (
            "Hello, Centauro, " + output["saludo_en"] + ". "
            "I'm Daniel, Centauro's virtual assistant. Our customer service team is closed at this time, "
            "so I can't transfer you to a colleague, but I can help you find the shuttle bus "
            "and give you information about our offices. How can I help you?"
        )
    else:
        output["mensaje_inicial"] = (
            "Hola, Centauro, " + output["saludo"] + ". "
            "Soy Daniel, el asistente virtual de Centauro. A esta hora nuestro centro de atención está cerrado "
            "y no puedo pasarle con un compañero, pero sí puedo ayudarle a encontrar el minibús "
            "y con la información de nuestras oficinas. ¿En qué puedo ayudarle?"
        )
elif idioma == "en":
    output["mensaje_inicial"] = (
        "Hello, Centauro, " + output["saludo_en"] + ". "
        "My name is Daniel, your AI assistant. How can I help you?"
    )
else:
    output["mensaje_inicial"] = (
        "Hola, Centauro, " + output["saludo"] + ". "
        "Mi nombre es Daniel, su asistente de IA. En que puedo ayudarle?"
    )

# ---------------------------------------------------------------
# Grabacion de aviso legal (disclaimer) segun el idioma resuelto
# ---------------------------------------------------------------
# greeting-minibus-en -> linea en ingles
# greetinminibus-es   -> linea en espanol (tambien respaldo)
DISCLAIMER_EN = "019feaea-eea1-7139-a9ae-07e639c52456"
DISCLAIMER_ES = "019fd44b-56a4-7a06-b240-1ede829ccceb"

# Comparte la misma decision que el saludo, de modo que aviso legal
# y agente no puedan quedar en idiomas distintos
output["recording_id"] = DISCLAIMER_EN if idioma == "en" else DISCLAIMER_ES
```

## Entradas (input_data)

```json
[
  {"key": "to_number", "value": "{{019f7594-d64b-778e-bc23-1d0b6d94d240.to_number}}"}
]
```
