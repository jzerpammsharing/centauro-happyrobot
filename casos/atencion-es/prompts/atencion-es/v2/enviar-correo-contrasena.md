<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v2 (x8xd0llbdp3j) · nodo: enviar_correo_contrasena (Prolongación) · copiado: 2026-10-18 (Tarea 10) -->

# enviar_correo_contrasena (Prolongación, v2)

Herramienta del prompt «Prolongación». Es la cadena de Prolongaciones v12 copiada tal cual
(`casos/prolongaciones/prompts/prolongacion-es/v12/enviar-correo-contrasena.md`): mismo texto de herramienta, misma
credencial «Centauro MCP» (`01a0e1d8-9c92-7e58-8e25-caf109f1fadb`), mismo event de MCP Call
(`019d4a7a-f3e9-7748-b002-efb988800cd3`) y el mismo código, sin cambios. Descripción y parámetros:
`herramientas-prolongacion.md` §1.

| # | Nodo | Tipo | ID = persistent_id | Qué hace |
|---|---|---|---|---|
| 0 | enviar_correo_contrasena | tool, `message` ai | `01a150c7-08df-73fd-abac-19c873b9533d` | La función que ve el agente |
| 1 | Comprobar correo (consultar_reserva) | MCP Call | `01a150c7-08ea-725d-a22c-f6dd3d5161d4` | `consultar_reserva` con `email`, `nombre_completo` y `fecha_nacimiento` de la herramienta |
| 2 | Decidir envío | Python Sandbox (`standard`) | `01a150c7-08fd-7f91-9dc8-5b5d5290896e` | `casos/prolongaciones/codigo/decidir_envio.py` tal cual. Entradas: `email` de la herramienta, `result` e `is_error` del nodo 1 |
| 3 | Enviar correo (enviar_reset_contrasena) | MCP Call | `01a150c7-090c-7f7b-b5f7-38aa1b1614d9` | `enviar_reset_contrasena` con `email` = `{{01a150c7-08fd-….email_envio}}` (vacío si no coincide: el MCP lo rechaza y no sale ningún correo) |
| 4 | Resultado para el agente | Python Sandbox (`standard`) | `01a150c7-091b-7abf-a101-539b1b7ec049` | `casos/prolongaciones/codigo/resultado_envio.py` tal cual. Entradas: `estado` y `detalle` del nodo 2; `reset_result` y `reset_is_error` del nodo 3 |

## Mejora de la spec §5.7 (que «Enviar correo» no se ejecute si no coincide): no se hace en la Tarea 10

Por API sí se puede: un Paths nuevo bajo «Decidir envío» (`estado` = `coincide` o no) con un «Resultado para el agente» en
cada rama (en la de envío, detrás de «Enviar correo»). No hace falta enganchar un nodo a dos padres. Lo que no está
comprobado es si el agente recibe como resultado de la herramienta la salida del «Resultado» de la rama que se ejecuta, y
`test_node` no ejecuta un Paths, así que solo se vería con evals o una llamada de prueba. La cadena sigue como en la v12
y la mejora queda en `docs/pendientes.md`.

## Paso 3: `test_node` con datos inventados (18/10/2026, 22:54, Madrid)

Para la prueba, los `tool_args` del nodo 1 se pusieron como texto fijo (`prueba.prueba@example.com`, `Prueba Prueba`,
`03/03/1990`) y después se volvieron a dejar las variables de la herramienta (comprobado con `get_node_details`).

| Nodo | Salida |
|---|---|
| 1 Comprobar correo | `{"is_error": false, "result": {"encontrada": false, "motivo_no_verificado": null, "verificado": false}}` |
| 2 Decidir envío | `{"coincide": false, "detalle": "", "email_envio": "", "estado": "no_coincide"}` (con `test_node` el `email` de la herramienta llega con su ejemplo) |
| 4 Resultado para el agente | `{"resultado": "no_coincide", "enviado": false, "detalle": "No coincide: no se ha enviado nada. Sigue ENVÍO DEL CORREO DE CONTRASEÑA, caso «No coincide»."}` |

El nodo 3 (envío) **no** se ejecutó con `test_node`. Forma real de la respuesta de `consultar_reserva`: un objeto JSON
(`dict`) en `result`, no envuelto en `{"content": [...]}`; `decidir_envio.py` y `pista_correo.py` la leen bien.
