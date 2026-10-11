<!-- workflow: 019f7594-2cce-7eed-b995-dd9ea64a1062 · versión: v17 (i0syf61bujsz) · nodo: Resolver colas por idioma · copiado: 2026-10-11 -->

# Resolver colas por idioma (código Python)

- Tipo: action (Python), event_id `019dde7b-3500-7a3c-8f5e-1c2d4e6a8b9c`
- persistent_id: `019feb2c-0554-7b99-a980-42f896779230`
- Nodo padre: «Calcular horario nocturno»
- execution_profile: `standard`

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
#   asistencia      -> averias, accidentes, opciones RA
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
# configurada directamente en el nodo, no desde aqui.
#
# Este bloque alimenta solo a los nodos Transfer, asi que devuelve
# la URI completa en cola_*. Si algun dia se conecta a un Forward
# call, usa cola_*_ext en su lugar.
# ===============================================================

PBX = "hrpbx.buscentauro.com"

COLAS = {
    "es": {
        "nueva_reserva":   {"ext": "18001", "nombre": "CC ES-ES Nueva Reserva"},
        "horario_minibus": {"ext": "18056", "nombre": "CC ES-ES Hor.MiniBus"},
        "gestion_reserva": {"ext": "18057", "nombre": "CC ES-ES Hor.Gestion"},
        "asistencia":      {"ext": "2114",  "nombre": "RA ES-ES-Opciones"},
        "fuera_horario":   {"ext": "2129",  "nombre": "Fuera de horario ES"},
    },
    "en": {
        "nueva_reserva":   {"ext": "18006", "nombre": "CC ES-EN Nueva Reserva"},
        "horario_minibus": {"ext": "18059", "nombre": "CC ES-EN Hor.MiniBus"},
        "gestion_reserva": {"ext": "18061", "nombre": "CC ES-EN Hor. Manage Reserv."},
        "asistencia":      {"ext": "2115",  "nombre": "RA ES-EN-OPCIONES"},
        "fuera_horario":   {"ext": "2130",  "nombre": "Fuera de horario EN"},
    },
}

# Idioma por defecto si llega vacio o no reconocido
IDIOMA_RESPALDO = "es"

# ---------------------------------------------------------------
# Resolucion
# ---------------------------------------------------------------
idioma_raw = input_data.get("idioma") or ""
idioma = str(idioma_raw).strip().lower()

if idioma not in COLAS:
    idioma = IDIOMA_RESPALDO

seleccion = COLAS[idioma]

output = {
    "idioma_colas": idioma,
}

# Una URI SIP lista para usar por cada cola, mas su nombre legible
for clave, datos in seleccion.items():
    output["cola_" + clave] = "sip:" + datos["ext"] + "@" + PBX
    output["cola_" + clave + "_ext"] = datos["ext"]
    output["cola_" + clave + "_nombre"] = datos["nombre"]
```

## Entradas (input_data)

```json
[
  {"key": "idioma", "value": "{{019fd418-5a5d-7bd4-93f8-eae309f8dc7a.idioma}}"}
]
```
