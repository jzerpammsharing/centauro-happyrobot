<!-- workflow: 01a03a65-3700-74c1-9c7b-e9c708833c4b · versión: v3 (jgkjecsoaxp4) · nodo: Resolver colas por idioma · copiado: 2026-10-12 -->

# Resolver colas por idioma (código Python)

- Tipo: action (Python), event_id `019dde7b-3500-7a3c-8f5e-1c2d4e6a8b9c`
- persistent_id: `4e0b9531-326f-4c5f-8f49-bbe460868570`
- Nodo padre: «Calcular horario nocturno»

## Código

```python
# ===============================================================
# COLAS DE TRANSFERENCIA POR IDIOMA
# ---------------------------------------------------------------
# Para cambiar una extension, edita solo este bloque.
# La logica de abajo no necesita tocarse.
#
#   nueva_reserva   -> reservas nuevas
#   horario_minibus -> horarios de minibus / shuttle
#   gestion_reserva -> cambios, cancelaciones, facturacion
#                      (solo L-V 08:00-21:00 hora peninsular espanola; fuera de ese horario se
#                      sustituye por un aviso y el agente no puede transferir)
#   asistencia      -> averias, accidentes
#                      (19048 / 19049, colas con agentes equivalentes a las
#                      18034 / 18035 de Espana; antes 2118 / 2119, que son
#                      un menu automatico sin agente)
#   fuera_horario   -> cola especial del IVR que reproduce la
#                      grabacion de oficina cerrada y cuelga.
#                      La llamada se reencamina a esta cola SIN que
#                      el agente de IA entre en la conversacion.
#
# ---------------------------------------------------------------
# FORMATO DE LOS DESTINOS: OJO, NO ES EL MISMO PARA TODO
# ---------------------------------------------------------------
# Los nodos Transfer ("Initiate customer connection", los que usa
# la herramienta transfer_to_human_agent) SI aceptan la URI SIP
# completa: "sip:18056@hrpbx.buscentauro.com". Verificado en
# produccion con transfer_succeeded = true.
#
# Los nodos Forward call ("Reenviar a cola de fuera de horario")
# NO la aceptan y fallan con:
#   "SipCallTo should be a phone number or SIP user,
#    not a full SIP URI"
# Por eso esos nodos llevan la extension pelada (2129 / 2130)
# configurada directamente en el nodo, no desde aqui. Desde la v3 este
# workflow no tiene nodos Forward call (modo virtual, como ES v22).
#
# Este bloque alimenta solo a los nodos Transfer, asi que devuelve
# la URI completa en cola_*. Si algun dia se conecta a un Forward
# call, usa cola_*_ext en su lugar.
# ===============================================================

PBX = "hrpbx.buscentauro.com"

COLAS = {
    "it": {
        "nueva_reserva":   {"ext": "18024", "nombre": "00. CC IT-IT-1 Nuova Prenotazione"},
        "horario_minibus": {"ext": "18069", "nombre": "00. CC IT-IT-Hor.MiniBus"},
        "gestion_reserva": {"ext": "18071", "nombre": "00. CC IT-IT-Hor.Mod.Reserva"},
        "asistencia":      {"ext": "19048", "nombre": "00. RA IT-IT RA Guasti"},
        "fuera_horario":   {"ext": "2133",  "nombre": "Fuera de horario IT"},
    },
    "en": {
        "nueva_reserva":   {"ext": "19042", "nombre": "00. CC IT-EN-1 Nuova Prenotazione"},
        "horario_minibus": {"ext": "18073", "nombre": "00. CC IT-EN-Hor.MiniBus"},
        "gestion_reserva": {"ext": "18074", "nombre": "00. CC IT-EN-Hor.Mod.Reserva."},
        "asistencia":      {"ext": "19049", "nombre": "00. RA IT-EN Breakdowns"},
        "fuera_horario":   {"ext": "2134",  "nombre": "Fuera de horario EN"},
    },
}

# Idioma por defecto si llega vacio o no reconocido
IDIOMA_RESPALDO = "it"

# Texto que sustituye a la cola de gestion cuando esta cerrada. El agente
# lo ve en la descripcion de transfer_to_human_agent en lugar de la extension.
GESTION_CERRADA = (
    "NO DISPONIBLE AHORA: la cola de gestion de reserva esta cerrada "
    "(atiende de lunes a viernes de 8:00 a 21:00, hora peninsular espanola). No transfieras a gestion: "
    "sigue la seccion COLA DE GESTION CERRADA de tus instrucciones"
)

# ---------------------------------------------------------------
# Resolucion
# ---------------------------------------------------------------
idioma_raw = input_data.get("idioma") or ""
idioma = str(idioma_raw).strip().lower()

if idioma not in COLAS:
    idioma = IDIOMA_RESPALDO

seleccion = COLAS[idioma]

# gestion_abierta puede llegar como booleano o como texto; si no llega, se
# asume abierta para no bloquear transferencias por un fallo de datos.
ga_raw = input_data.get("gestion_abierta")
if isinstance(ga_raw, bool):
    gestion_abierta = ga_raw
else:
    gestion_abierta = str(ga_raw).strip().lower() not in ("false", "0", "no")

output = {
    "idioma_colas": idioma,
    "gestion_abierta": gestion_abierta,
}

# Una URI SIP lista para usar por cada cola, mas su nombre legible
for clave, datos in seleccion.items():
    output["cola_" + clave] = "sip:" + datos["ext"] + "@" + PBX
    output["cola_" + clave + "_ext"] = datos["ext"]
    output["cola_" + clave + "_nombre"] = datos["nombre"]

if not gestion_abierta:
    output["cola_gestion_reserva"] = GESTION_CERRADA
```

## Entradas (input_data)

```json
[
  {"key": "idioma", "value": "{{3b1e91ac-f471-47a9-b175-8408c58d826f.idioma}}"},
  {"key": "gestion_abierta", "value": "{{3b1e91ac-f471-47a9-b175-8408c58d826f.gestion_abierta}}"}
]
```
