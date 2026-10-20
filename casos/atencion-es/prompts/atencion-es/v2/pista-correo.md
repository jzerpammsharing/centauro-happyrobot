<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v2 (x8xd0llbdp3j) · nodo: pista_correo (Prolongación) · copiado: 2026-10-18 (Tarea 10) -->

# pista_correo (Prolongación, v2)

Herramienta nueva del prompt «Prolongación» (spec §5.7): identifica al cliente por número de reserva, nombre y fecha de
nacimiento y devuelve al agente solo `verificado`, el **dominio** del correo del alquiler, `resultado` y `detalle`.
Descripción y parámetros: `herramientas-prolongacion.md` §2. «Como mucho dos llamadas por conversación» va en la
descripción de la herramienta (como en `enviar_correo_contrasena`).

| # | Nodo | Tipo | ID = persistent_id | Qué hace |
|---|---|---|---|---|
| 0 | pista_correo | tool, `message` ai («Un momento, lo compruebo.») | `01a150c7-0928-79dc-a21c-4d9348ca038d` | La función que ve el agente |
| 1 | Identificar al cliente (consultar_reserva) | MCP Call, «Centauro MCP» (`01a0e1d8-9c92-7e58-8e25-caf109f1fadb`), event `019d4a7a-f3e9-7748-b002-efb988800cd3` | `01a150c7-0930-723c-89d9-eaeb76a0599e` | `consultar_reserva` con `numero_reserva`, `nombre_completo` y `fecha_nacimiento` de la herramienta |
| 2 | Pista del correo | Python Sandbox (`standard`) | `01a150c7-0940-76a7-8129-f132e4373895` | `casos/atencion-es/codigo/pista_correo.py` tal cual (Tarea 5). Entradas: `result` e `is_error` del nodo 1 |

## Paso 3: `test_node` con datos inventados (18/10/2026, 22:54, Madrid)

`tool_args` del nodo 1 como texto fijo (`ER00000000`, `Prueba Prueba`, `03/03/1990`) y después otra vez las variables
de la herramienta (comprobado con `get_node_details`).

| Nodo | Salida |
|---|---|
| 1 Identificar al cliente | `{"is_error": false, "result": {"encontrada": false, "motivo_no_verificado": null, "verificado": false}}` |
| 2 Pista del correo | `{"verificado": false, "dominio": "", "resultado": "no_verificado", "detalle": "Con esos datos no se puede verificar. No digas qué dato falla. …"}` |

**Comparación con lo que espera `pista_correo.py` (nota de la Tarea 5):**

- Forma: `result` llega como un objeto JSON (`dict`), no como texto ni envuelto en `{"content": [...]}`. `a_dict` lo
  acepta tal cual (también aceptaría el formato de contenido MCP).
- Con una reserva que no existe, el MCP **no** da error: devuelve `encontrada: false, verificado: false` con
  `motivo_no_verificado: null`. Es la rama `no_verificado` del código, la que se esperaba.
- No se vio el texto que devuelve el MCP cuando no interpreta el número de reserva o el nombre (la ficha solo permite
  esta prueba): las ramas `DETALLE_RESERVA` y `DETALLE_NOMBRE` de `clasificar_error` siguen sin confirmar. Si el texto real
  no lleva «reserva», «número» o «nombre» a menos de 40 caracteres de «interpretar», saldrá el detalle genérico, que sigue
  siendo correcto. Apuntado en `docs/pendientes.md`.
- El caso «verificado» (devuelve `email_hint`) solo se puede ver con una reserva real: puerta 0 (`pendientes.md`).
