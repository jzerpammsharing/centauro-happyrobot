<!-- workflow: 01a0d9de-b1cd-7bc9-bafc-f5117bd57249 · versión: Version 11 (2g1bxzyzazpp) · nodo: Resolver colas por idioma · copiado: 2026-10-11 -->

Python Sandbox (Code). Persistent ID `01a0da07-411e-71c5-84ce-499952b43d8e`. No es un prompt: se guarda
porque aquí están las colas de transferencia y lo que pasa cuando la cola de Gestión está cerrada.
Es igual que en la V10.

- **Entradas:** `idioma` y `gestion_abierta` de «Calcular idioma y saludo» (`01a0da06-917d-7e9c-9b1c-153df5946a48`).
- **Salidas:** `idioma_colas`, `gestion_abierta` y, para cada cola, `cola_<clave>` (URI SIP),
  `cola_<clave>_ext` y `cola_<clave>_nombre` (claves: `nueva_reserva`, `horario_minibus`,
  `gestion_reserva` y `asistencia`).
- **Execution profile:** standard.

```python
# ===============================================================
# COLAS DE TRANSFERENCIA POR IDIOMA (copiado de Centauro Minibus SPAIN)
# ---------------------------------------------------------------
# Para cambiar una extension, edita solo este bloque.
#
#   nueva_reserva   -> reservas nuevas
#   horario_minibus -> minibus / punto de encuentro / idioma no soportado
#   gestion_reserva -> cambios, cancelaciones, facturacion (cola por defecto en este flujo)
#   asistencia      -> averias, accidentes, opciones RA
#
# Este flujo no tiene cola de fuera de horario: hay un unico horario.
# Los nodos Transfer aceptan la URI SIP completa.
# ===============================================================

PBX = "hrpbx.buscentauro.com"

COLAS = {
    "es": {
        "nueva_reserva":   {"ext": "18001", "nombre": "CC ES-ES Nueva Reserva"},
        "horario_minibus": {"ext": "18056", "nombre": "CC ES-ES Hor.MiniBus"},
        "gestion_reserva": {"ext": "18057", "nombre": "CC ES-ES Hor.Gestion"},
        "asistencia":      {"ext": "18034",  "nombre": "RA ES-ES-Opciones"},
    },
    "en": {
        "nueva_reserva":   {"ext": "18006", "nombre": "CC ES-EN Nueva Reserva"},
        "horario_minibus": {"ext": "18059", "nombre": "CC ES-EN Hor.MiniBus"},
        "gestion_reserva": {"ext": "18061", "nombre": "CC ES-EN Hor. Manage Reserv."},
        "asistencia":      {"ext": "18035",  "nombre": "RA ES-EN-OPCIONES"},
    },
}

IDIOMA_RESPALDO = "es"

idioma = str(input_data.get("idioma") or "").strip().lower()
if idioma not in COLAS:
    idioma = IDIOMA_RESPALDO

seleccion = COLAS[idioma]

output = {"idioma_colas": idioma}

for clave, datos in seleccion.items():
    output["cola_" + clave] = "sip:" + datos["ext"] + "@" + PBX
    output["cola_" + clave + "_ext"] = datos["ext"]
    output["cola_" + clave + "_nombre"] = datos["nombre"]

# Cola de GESTION DE RESERVA cerrada (fuera de L-V 08:00-21:00): se quita la
# extension para que el agente no pueda transferir a una locucion de cerrado.
ga_raw = input_data.get("gestion_abierta")
if isinstance(ga_raw, bool):
    gestion_abierta = ga_raw
else:
    gestion_abierta = str(ga_raw).strip().lower() not in ("false", "0", "no")
output["gestion_abierta"] = gestion_abierta
if not gestion_abierta:
    output["cola_gestion_reserva"] = (
        "NO DISPONIBLE AHORA: la cola de gestion de reserva esta cerrada "
        "(atiende de lunes a viernes de 8:00 a 21:00). No transfieras a gestion: "
        "sigue la seccion COLA DE GESTION CERRADA de tus instrucciones"
    )
```
