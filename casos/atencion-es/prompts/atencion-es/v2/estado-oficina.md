<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v2 (x8xd0llbdp3j) · nodo: Estado de la oficina (Punto de encuentro) · copiado: 2026-10-20 (Tarea 15b, R39) -->

# Estado de la oficina (código Python) · Punto de encuentro

- Herramienta `estado_oficina` (tool): ID = persistent_id en la v2 `01a1575e-923d-7deb-8a35-da450582d445`; padre, el
  prompt «Punto de encuentro» (`01a14f1d-0397-7c91-b2bc-a12efeed5595`, persistent_id
  `a80fca22-b295-41e3-a735-a3c878af4eee`). `message`: `{"type": "none"}`. Descripción y parámetro (`aeropuerto`):
  `herramientas-punto-de-encuentro.md` (§3).
- Hijo: action (Python Sandbox) «Estado de la oficina», event_id `019dde7b-3500-7a3c-8f5e-1c2d4e6a8b9c`,
  execution_profile `standard`; ID = persistent_id en la v2 `01a1575e-9248-71bc-ac3d-1dc0666e3a92`. No tiene hijos:
  el agente recibe su salida como resultado de la herramienta.
- Código: `casos/atencion-es/codigo/estado_oficina.py` tal cual (pruebas: `test_estado_oficina.py`). Creado el
  20/10/2026 a las 05:32; la versión del repo se subió por última vez a las 05:50 (ronda A3).

## Entradas (input_data)

```json
[
  {"key": "aeropuerto", "value": "{{01a1575e-923d-7deb-8a35-da450582d445.aeropuerto}}"},
  {"key": "nocturno_cet", "value": "{{e51cd732-f403-4ef7-95d4-490347960a93.nocturno_cet}}"},
  {"key": "nocturno_wet", "value": "{{e51cd732-f403-4ef7-95d4-490347960a93.nocturno_wet}}"},
  {"key": "nocturno_eet", "value": "{{e51cd732-f403-4ef7-95d4-490347960a93.nocturno_eet}}"},
  {"key": "nocturno_murcia", "value": "{{e51cd732-f403-4ef7-95d4-490347960a93.nocturno_murcia}}"}
]
```

## Salida

`aeropuerto` (nombre de la tabla, o el que llegó si no se reconoce), `reconocido`, `oficina_cerrada`,
`hora_apertura` («siete de la mañana, hora local» u «ocho…» en Murcia, Bari, Florencia, Nápoles y Venecia),
`instruccion` (frase para el agente) y `fuente` (`contexto` si leyó la `nocturno_*` de su zona; `reloj` si llegó vacía
o sin resolver y la calculó con las franjas de `contexto_llamada.py`).

## Pruebas con `test_node` (20/10/2026, 05:33–05:39)

`test_node` no usa el argumento de la herramienta (llega vacío) y toma las `nocturno_*` de la salida guardada de
«Contexto de la llamada» (de día): devuelve `aeropuerto` vacío, `reconocido` false, `oficina_cerrada` false y
`fuente` contexto. Comprueba que el nodo acepta `re` y `unicodedata` y que las variables se resuelven. Lo demás lo
cubren las pruebas locales (361 casos) y las evals PE-EST-1 a 3, en las que la herramienta se ejecuta de verdad con las
variables de la eval.
