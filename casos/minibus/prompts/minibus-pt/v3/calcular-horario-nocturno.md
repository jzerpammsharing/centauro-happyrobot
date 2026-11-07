<!-- workflow: 01a05977-3a33-76da-acb2-a757f3947cf9 · versión: v3 (2139o3pf25qm) · nodo: Calcular horario nocturno · copiado: 2026-10-12 -->

# Calcular horario nocturno (código Python)

- Tipo: action (Python), event_id `019dde7b-3500-7a3c-8f5e-1c2d4e6a8b9c`
- persistent_id: `0f85067a-078e-4a21-9b45-0d5bfb92dd8e`
- Redacción: los números de teléfono de las líneas se sustituyen por [REDACTADO].

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

# Hora peninsular (CET/CEST): la usan el centro de atencion y la cola de Gestion,
# que estan en Espana
hora_cet = (ahora_utc + timedelta(hours=BASE["cet"] + (1 if verano else 0))).hour

output["nocturno_murcia"] = hora_cet >= MURCIA_INICIO or hora_cet < MURCIA_FIN
output["callcenter_abierto"] = CALLCENTER_INICIO <= hora_cet < CALLCENTER_FIN
output["modo_virtual"] = not output["callcenter_abierto"]
# Franja del dia para el saludo, referida a la hora local (WET)
hora_saludo = (ahora_utc + timedelta(hours=BASE["wet"] + (1 if verano else 0))).hour
if 6 <= hora_saludo < 13:
    output["saludo"] = "bom dia"
elif 13 <= hora_saludo < 21:
    output["saludo"] = "boa tarde"
else:
    output["saludo"] = "boa noite"

# ---------------------------------------------------------------
# Idioma de atencion segun el numero marcado por el cliente
# ---------------------------------------------------------------
# Linea en ingles: [REDACTADO] (valor heredado de PT v1)
NUMERO_INGLES = "[REDACTADO]"

to_number_raw = input_data.get("to_number") or ""
# Nos quedamos solo con los digitos para que el formato no afecte
digitos = "".join(c for c in str(to_number_raw) if c.isdigit())

# Por defecto el idioma local (portugues): si el numero llega vacio o irreconocible,
# preferimos caer en el idioma de la linea principal
if digitos.endswith(NUMERO_INGLES):
    idioma = "en"
else:
    idioma = "pt"

output["idioma"] = idioma
output["idioma_nombre"] = "English" if idioma == "en" else "portugues"
output["numero_marcado"] = digitos

# Saludo equivalente en ingles, con la misma franja horaria
if 6 <= hora_saludo < 13:
    output["saludo_en"] = "good morning"
elif 13 <= hora_saludo < 21:
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
            "so I can't transfer you to a colleague, but I can help you find the shuttle bus. How can I help you?"
        )
    else:
        output["mensaje_inicial"] = (
            "Olá, Centauro, " + output["saludo"] + ". "
            "Sou o Daniel, o assistente virtual da Centauro. A esta hora o nosso apoio ao cliente está fechado "
            "e não posso passar a chamada a um colega, mas posso ajudá-lo a encontrar o minibus. Como posso ajudá-lo?"
        )
elif idioma == "en":
    output["mensaje_inicial"] = (
        "Hello, Centauro, " + output["saludo_en"] + ". "
        "My name is Daniel, your AI assistant. How can I help you?"
    )
else:
    output["mensaje_inicial"] = (
        "Olá, Centauro, " + output["saludo"] + ". "
        "Chamo-me Daniel, sou o seu assistente de IA. Como posso ajudá-lo?"
    )

# ---------------------------------------------------------------
# Grabacion de aviso legal (disclaimer) segun el idioma resuelto
# ---------------------------------------------------------------
# greeting-minibus-en -> linea en ingles
# disclaimer PT       -> linea en portugues (tambien respaldo)
DISCLAIMER_EN = "019feaea-eea1-7139-a9ae-07e639c52456"
DISCLAIMER_LOCAL = "01a061be-b6d1-72cf-bb3b-968a1491d031"

# Comparte la misma decision que el saludo, de modo que aviso legal
# y agente no puedan quedar en idiomas distintos
output["recording_id"] = DISCLAIMER_EN if idioma == "en" else DISCLAIMER_LOCAL

# ---------------------------------------------------------------
# Telefono del cliente dictado digito a digito (para el whisper)
# ---------------------------------------------------------------
PALABRAS = {"0": "zero", "1": "um", "2": "dois", "3": "três", "4": "quatro",
            "5": "cinco", "6": "seis", "7": "sete", "8": "oito", "9": "nove"}


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
elif internacional and tel.startswith("351"):
    telefono_dictado = dictar(tel[3:])
elif internacional:
    telefono_dictado = "internacional, mais " + dictar(tel)
else:
    telefono_dictado = dictar(tel)

output["telefono_dictado"] = telefono_dictado

# ---------------------------------------------------------------
# Horario de la cola de GESTION DE RESERVA (L-V 08:00-21:00 peninsular)
# ---------------------------------------------------------------
local_cet = ahora_utc + timedelta(hours=BASE["cet"] + (1 if verano else 0))
output["gestion_abierta"] = local_cet.weekday() < 5 and GESTION_INICIO <= local_cet.hour < GESTION_FIN
```

## Entradas (input_data)

```json
[
  {"key": "to_number", "value": "{{efcc08a0-2b5b-407a-871d-656194b896ba.to_number}}"},
  {"key": "from_number", "value": "{{efcc08a0-2b5b-407a-871d-656194b896ba.from_number}}"}
]
```
