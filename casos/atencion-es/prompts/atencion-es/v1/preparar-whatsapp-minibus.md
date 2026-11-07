<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v1 (veavliy3k6jx) · nodo: Preparar WhatsApp minibús · copiado: 2026-10-18 -->

# Preparar WhatsApp minibús (código Python)

- Tipo: action (Python), event_id `019dde7b-3500-7a3c-8f5e-1c2d4e6a8b9c`
- persistent_id: `4bd059bb-837c-4242-845f-7fc802c0f937`
- Nodo padre: «Registrar consultas del alquiler»
- Hijo: Paths «¿Enviar WhatsApp?»
- execution_profile: `standard`

## Código

```python
# ===============================================================
# PREPARAR WHATSAPP DEL PUNTO DE ENCUENTRO (v24)
# ---------------------------------------------------------------
# Se ejecuta al terminar la llamada, despues del Extract. Decide si
# se envia la plantilla "minibus_punto_texto_boton" (espanol) y
# prepara sus variables:
#   {{aeropuerto}}          -> var_aeropuerto  (aeropuerto y terminal)
#   {{indicaciones}}        -> var_indicaciones (texto escrito)
#   {{descripcion_minibus}} -> var_descripcion
#   {{frecuencia}}          -> var_frecuencia
# El boton "Ver minibus en directo" no tiene parte variable.
#
# Solo se envia si: el cliente acepto el WhatsApp en la llamada, el
# punto de encuentro es de un aeropuerto CON SEGUIMIENTO EN DIRECTO
# en buscentauro.com (TRACKING), la llamada fue en espanol y el
# numero parece un movil valido.
#
# Para dar de alta un aeropuerto nuevo con seguimiento:
#   1) anadir su codigo IATA a TRACKING;
#   2) anadir sus puntos a PUNTOS (misma estructura);
#   3) anadir el codigo del punto a los valores permitidos de
#      "punto_whatsapp" en el Extract y al prompt de Punto de
#      encuentro (lista de aeropuertos con WhatsApp).
# ===============================================================

# Aeropuertos con seguimiento en directo en buscentauro.com
TRACKING = {"MAD", "SVQ", "AGP"}

DESCRIPCION_MINIBUS = "amarillo, con el logo de Centauro"
FRECUENCIA = "15 o 20 minutos"

# codigo de punto -> (aeropuerto y terminal, indicaciones, IATA)
PUNTOS = {
    "MAD-T1": ("Madrid, Terminal 1", "Salga de la terminal, gire a la derecha y camine unos 150 m hasta el cartel verde \"Hotel Bus\", justo enfrente de la Consigna de Equipaje. Ahí espera el minibús.", "MAD"),
    "MAD-T2": ("Madrid, Terminal 2", "En llegadas, siga a mano izquierda las señales \"Bus Connecting\" hasta la señal \"P Exprés\". Salga en ese punto y cruce la calzada; a mano derecha verá las señales \"Bus Stop, EMT Hotels, Agencies\". Sígalas hasta el minibús.", "MAD"),
    "MAD-T4": ("Madrid, Terminal 4", "Siga el cartel \"Bus y Shuttle\", que verá a su izquierda, hasta la salida. Una vez fuera, cruce la calzada y siga las indicaciones \"Bus Hotel\" a la izquierda. Ahí espera el minibús.", "MAD"),
    "AGP": ("Málaga", "Salga por la puerta principal de la terminal (salida hacia la Estación de Tren). Cruce la carretera por el paso de cebra y siga unos 100 m: tras la estación \"Renfe Aeropuerto\" está la parada de minibuses.", "AGP"),
    "SVQ": ("Sevilla", "Salga de llegadas por la puerta más próxima, cruce la calle y vaya a la izquierda. A unos 250 m, pasado el parking público P1, está el parking P2 de larga estancia: en la señal \"Meeting Point\" está la zona de espera del minibús.", "SVQ"),
}


def limpio(v):
    return str(v or "").strip()


def telefono_movil(raw):
    """Devuelve el numero en formato +E.164 si parece un movil al que se puede enviar WhatsApp; si no, ''."""
    raw = limpio(raw)
    d = "".join(c for c in raw if c.isdigit())
    if raw.startswith("00"):
        d = d[2:]
    elif not raw.startswith("+") and len(d) == 9:
        d = "34" + d  # numero espanol sin prefijo
    if d.startswith("34"):
        # Espana: solo moviles (6xx o 7xx), 9 cifras tras el prefijo
        return "+" + d if len(d) == 11 and d[2] in "67" else ""
    # Extranjero: no sabemos si es movil; si no tiene WhatsApp, Meta no lo entrega
    return "+" + d if 8 <= len(d) <= 15 else ""


aceptado = limpio(input_data.get("whatsapp_aceptado")).lower()
punto = limpio(input_data.get("punto_whatsapp")).upper()
idioma = limpio(input_data.get("idioma_cliente")).lower()
telefono = telefono_movil(input_data.get("from_number"))
iata = PUNTOS[punto][2] if punto in PUNTOS else ""

motivo = ""
if aceptado != "si":
    motivo = "no_aceptado"
elif not punto or punto == "NINGUNO":
    motivo = "sin_punto"
elif iata not in TRACKING:
    motivo = "sin_geolocalizacion"
elif idioma != "es":
    motivo = "idioma_no_es"
elif not telefono:
    motivo = "telefono_no_valido"

output = {"enviar": motivo == "", "motivo_no_envio": motivo or "ninguno", "telefono": telefono, "punto": punto}
if punto in PUNTOS:
    aeropuerto, indicaciones, _ = PUNTOS[punto]
    output.update({
        "var_aeropuerto": aeropuerto,
        "var_indicaciones": indicaciones,
        "var_descripcion": DESCRIPCION_MINIBUS,
        "var_frecuencia": FRECUENCIA,
    })
```

## Entradas (input_data)

```json
[
  {"key": "from_number", "value": "{{33c2681a-9160-413c-8010-e455bd4023c6.from_number}}"},
  {"key": "whatsapp_aceptado", "value": "{{15bf240b-4db7-47cc-86c5-963eaf6955b3.response.whatsapp_aceptado}}"},
  {"key": "punto_whatsapp", "value": "{{15bf240b-4db7-47cc-86c5-963eaf6955b3.response.punto_whatsapp}}"},
  {"key": "idioma_cliente", "value": "{{15bf240b-4db7-47cc-86c5-963eaf6955b3.response.idioma_cliente}}"}
]
```
