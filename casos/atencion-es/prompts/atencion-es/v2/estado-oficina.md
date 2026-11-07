<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v2 (x8xd0llbdp3j) · nodo: Estado de la oficina (Punto de encuentro) · copiado: 2026-10-20 (Tarea 15b, R39; Tarea 16, R45) -->

# Estado de la oficina (código Python) · Punto de encuentro

- Herramienta `estado_oficina` (tool): ID = persistent_id en la v2 `01a1575e-923d-7deb-8a35-da450582d445`; padre, el
  prompt «Punto de encuentro» (`01a14f1d-0397-7c91-b2bc-a12efeed5595`, persistent_id
  `a80fca22-b295-41e3-a735-a3c878af4eee`). `message`: `{"type": "none"}`. Descripción y parámetro (`aeropuerto`):
  `herramientas-punto-de-encuentro.md` (§3).
- Hijo: action (Python Sandbox) «Estado de la oficina», event_id `019dde7b-3500-7a3c-8f5e-1c2d4e6a8b9c`,
  execution_profile `standard`; ID = persistent_id en la v2 `01a1575e-9248-71bc-ac3d-1dc0666e3a92`. No tiene hijos:
  el agente recibe su salida como resultado de la herramienta.
- Código: `casos/atencion-es/codigo/estado_oficina.py` tal cual (pruebas: `test_estado_oficina.py`). Creado el
  20/10/2026 a las 05:32 (Tarea 15b). Tarea 16 (R45, D-014): calcula con la hora del momento y el horario concreto de
  cada oficina, y la variable `HORA_PRUEBA` manda sobre el reloj; subido a las 06:18 y comprobado con
  `get_node_details` (variables como nodos de Plate).

## Entradas (input_data)

```json
[
  {"key": "aeropuerto", "value": "{{01a1575e-923d-7deb-8a35-da450582d445.aeropuerto}}"},
  {"key": "hora_prueba", "value": "{{use_case_variables.HORA_PRUEBA}}"}
]
```

Desde la Tarea 16 ya no lee las `nocturno_*` de «Contexto de la llamada» (eran la hora del principio de la llamada).

**Variable del workflow `HORA_PRUEBA`** (id `01a15787-36ac-782d-9f54-1353c934de58`): `ninguna` en los tres entornos
(HappyRobot no admite valores vacíos). Con `ninguna` (o cualquier cosa que no sea una hora) manda el reloj. En una
eval se pone `use_case_variables.HORA_PRUEBA` = `HH:MM` (hora peninsular, del día de la ejecución) y la herramienta
calcula como si fuera esa hora: así la eval no depende de la hora a la que se ejecuta.

## Salida

`aeropuerto` (nombre de la tabla, o el que llegó si no se reconoce), `reconocido`, `oficina_cerrada`,
`hora_apertura` («siete de la mañana, hora local» u «ocho…» en Murcia, Bari, Florencia, Nápoles y Venecia),
`instruccion` (frase para el agente) y `fuente` (`reloj`, o `prueba` si mandó `HORA_PRUEBA`).

Horario (hora local del aeropuerto, el mismo que dice el prompt en HORARIO Y DEVOLUCIÓN EN AEROPUERTOS): de 7:00 a
23:00; Murcia de 8:00 a 22:00; Alicante de 7:00 a 23:30; Bari, Florencia, Nápoles y Venecia de 8:00 a 23:00. Un
aeropuerto que no se reconoce usa el horario general en hora peninsular (la antigua LISTA 1).

## Pruebas con `test_node`

- 20/10/2026, 05:33–05:39 (Tarea 15b): el nodo acepta `re` y `unicodedata` y las variables se resuelven.
- 20/10/2026, 06:18 (Tarea 16): `aeropuerto` vacío, `fuente` reloj, `oficina_cerrada` true (eran las 06:18 en
  Madrid): con `HORA_PRUEBA` = `ninguna` manda el reloj.

Lo demás lo cubren las pruebas locales (`test_estado_oficina.py`) y las evals: con `HORA_PRUEBA` = 10:00,
SALTO-ENTRADA-PE dio el punto de Málaga a las 06:28 (por el reloj la oficina estaba cerrada).
