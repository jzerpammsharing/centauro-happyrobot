<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v1 (veavliy3k6jx) · nodo: Calcular horario nocturno · copiado: 2026-10-18 -->

# Calcular horario nocturno (código Python)

- Tipo: action (Python), event_id `019dde7b-3500-7a3c-8f5e-1c2d4e6a8b9c`
- persistent_id: `e51cd732-f403-4ef7-95d4-490347960a93`
- Nodo padre: «Inbound Call»
- execution_profile: `standard`
- Redacción: los números de las líneas de Minibús ES/EN se sustituyen por `<LINEA_MINIBUS_ES>` y
  `<LINEA_MINIBUS_EN>`; los reales se ponen al pegar el código en HappyRobot.

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

# Cola de GESTION DE RESERVA: solo de lunes a viernes de 08:00 a 21:00
# (hora peninsular). Fuera de ese horario la cola reproduce una locucion
# de cerrado y nadie atiende: el agente no debe transferir alli.
GESTION_INICIO = 8
GESTION_FIN = 21

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
# Linea en espanol: <LINEA_MINIBUS_ES>
# Linea en ingles:  <LINEA_MINIBUS_EN>
NUMERO_INGLES = "<LINEA_MINIBUS_EN>"

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
    telefono_dictado = "internacional, más " + dictar(tel)
else:
    telefono_dictado = dictar(tel)

output["telefono_dictado"] = telefono_dictado

# ---------------------------------------------------------------
# Horario de la cola de GESTION DE RESERVA (L-V 08:00-21:00 peninsular)
# ---------------------------------------------------------------
local_cet = ahora_utc + timedelta(hours=BASE["cet"] + (1 if verano else 0))
output["gestion_abierta"] = local_cet.weekday() < 5 and GESTION_INICIO <= local_cet.hour < GESTION_FIN

# ---------------------------------------------------------------
# WhatsApp (v24): se puede ofrecer enviar el punto de encuentro por
# WhatsApp si la llamada es de la linea en espanol (la plantilla
# "minibus_punto_texto_boton" esta en espanol) y el numero del
# cliente parece un movil. Que el aeropuerto tenga seguimiento en
# directo (MAD, SVQ, AGP) lo decide el prompt de Punto de encuentro
# y lo vuelve a comprobar "Preparar WhatsApp minibus" antes de enviar.
# ---------------------------------------------------------------
wa_tel = "".join(c for c in from_raw if c.isdigit())
if from_raw.startswith("00"):
    wa_tel = wa_tel[2:]
elif not from_raw.startswith("+") and len(wa_tel) == 9:
    wa_tel = "34" + wa_tel
if wa_tel.startswith("34"):
    wa_movil = len(wa_tel) == 11 and wa_tel[2] in "67"
else:
    wa_movil = 8 <= len(wa_tel) <= 15
output["whatsapp_disponible"] = bool(wa_movil and idioma == "es")
```

## Entradas (input_data)

```json
[
  {"key": "to_number", "value": "{{33c2681a-9160-413c-8010-e455bd4023c6.to_number}}"},
  {"key": "from_number", "value": "{{33c2681a-9160-413c-8010-e455bd4023c6.from_number}}"}
]
```
