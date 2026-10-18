<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v2 (x8xd0llbdp3j) · nodo: ¿Transferir? + Initiate customer connection (Triaje) · copiado: 2026-10-18 -->

# Transferencia del Triaje: «¿Transferir?» → «Initiate customer connection»

Patrón de transferencia del bot único (spec §5.8). Las Tareas 9 a 11 lo copian en la herramienta de transferencia de
cada módulo.

```
transfer_to_human_agent (cola, motivo_transferencia, resumen_para_agente; message ai; música holdacent)
 └ Python «Preparar transferencia»            (preparar-transferencia.md)
   └ Paths «¿Transferir?»
       ├ «Transferir»  (transferir es true) → Transfer «Initiate customer connection»
       └ «Fallback»    (sin hijos: no se transfiere y la herramienta devuelve la salida del Python)
```

## Forma elegida para no transferir (spec §11.4): Paths después del Python

Se probaron las dos formas del Paso 4 de la Tarea 8 con `test_node` (no hay llamada web: la v2 no está publicada):

1. **Transfer con `numero` vacío** (Transfer colgado directamente del Python, con `number` = `{{<preparar>.numero}}`):
   con `resultado = gestion_cerrada` y `numero = ""`, el `test_node` del Transfer devuelve `transfer_succeeded: true`
   y `error: ""` (en pruebas el Transfer se simula). Es decir, el nodo **se ejecuta** aunque no haya número: no hay
   nada que impida que en una llamada real intente transferir o deje al cliente en espera. Descartada.
2. **Paths después del Python** (la elegida): con `transferir = false` el Transfer no se ejecuta. `test_node` no
   puede ejecutar un Paths por separado («unable to find activityType=PathsExecutor»), pero las evals del Triaje,
   que sí ejecutan la cadena de la herramienta, lo muestran: con `cola = gestion` en domingo, «Preparar
   transferencia» devuelve `gestion_cerrada`, la rama «Fallback» no tiene hijos y **el agente recibe `resultado` y
   `detalle` del Python** y le dice al cliente el horario de Gestión (LINEA-06 y «GESTIÓN ABIERTA · cargo no
   reconocido», 18/10/2026). Con `cola_no_valida` el agente reintenta una vez, como dice el bloque común.

**Pendiente (Tarea 17):** comprobarlo en una llamada de prueba por web con `OPCION_PRUEBA = prolongacion` y Gestión
cerrada: que el agente recibe `resultado: gestion_cerrada`, que no se marca ninguna llamada saliente en RingCentral y
que el bot sigue hablando. Si el agente no recibiera la salida del Python con el «Fallback» vacío, la alternativa es
colgar de «Fallback» un Python de una línea que devuelva `resultado` y `detalle` del «Preparar transferencia».

## «¿Transferir?» (Paths) y sus ramas

- Paths: ID = persistent_id `01a14f66-5245-7cb6-9718-59dd25ecc3f5`, configuración `{"policy": null}` (creado por API
  con `type: "path"`, que crea solo la rama «Fallback»).
- Condición «Transferir»: ID = persistent_id `01a14f66-524e-78a8-a01b-fd9c184bbe1d`, orden 0:

```json
[{"id": "transferir", "ors": [{"ands": [{"field": {"group_id": "01a14f64-277b-7226-8e39-a8ef0274949f",
  "variable_id": "transferir"}, "condition": "boolean_true"}]}]}]
```

- «Fallback»: `01a14f66-5245-7cb6-9718-59de12c52f87`, sin hijos.

## Transfer «Initiate customer connection»

- Event `01926f25-dacb-710e-a823-4254189111dd` (Transfer, Phone calls). ID = persistent_id
  `01a14f66-5252-70a4-81ad-fa8d1cc6b438`. Sustituye al de la v1 (`b4439401-…`), que se borró (era una hoja) para poder
  colgar el nuevo de la rama «Transferir».
- **Al crear un Transfer por API, poner `outside_agent_transfer: false`**: por defecto es `true` y entonces el
  `test_node` falla con «whisper transfer not supported for outside agent transfers» (los Transfer de la v25, creados
  en el editor, no llevan el campo).
- `number` y `fallback_number` = la salida `numero` del Python: la misma cola, nunca Gestión de respaldo.
- `test_node` con la salida de Asistencia: `number` = URI SIP de Asistencia, whisper «Llamada del asistente de
  atención.  Teléfono del cliente: número oculto.» (el resumen sale vacío porque en `test_node` la herramienta no
  tiene argumentos), `transfer_succeeded: true` (simulado).

```json
{
  "agent": {"type": "static", "static": {"id": "300ae88d-ccb2-466c-a914-9f9090363a74", "name": "Receive Customer Call"}},
  "number": "{{01a14f64-277b-7226-8e39-a8ef0274949f.numero}}",
  "fallback_number": "{{01a14f64-277b-7226-8e39-a8ef0274949f.numero}}",
  "extension": "",
  "from_number": "",
  "headers": [],
  "whisper_transfer": true,
  "whisper_message": "Llamada del asistente de atención. {{17c682a0-82d2-42f6-88fa-817d8cba0783.resumen_para_agente}} Teléfono del cliente: {{e51cd732-f403-4ef7-95d4-490347960a93.telefono_dictado}}.",
  "skip_digit_press": false,
  "record_transfer_conversation": true,
  "stop_recording_on_transfer": false,
  "skip_handoff_message": true,
  "warm_handoff": false,
  "warm_handoff_intro_mode": "default",
  "enableSpokenDigit": false,
  "uui_encoding": "ascii",
  "uui_data_format": "text",
  "transfer_timeout": "300",
  "outside_agent_transfer": false
}
```

## Para las Tareas 9 a 11 (copiar el patrón)

1. Cambiar los parámetros de la herramienta a `cola`, `motivo_transferencia` y `resumen_para_agente` (todos
   obligatorios), con la variable `{{e51cd732-….gestion_abierta}}` como nodo de variable de Plate en la descripción
   de `cola` (un `{{…}}` dentro de un texto plano de herramienta se queda como texto literal); música «holdacent»
   (`hold_music` estático con la URL firmada del asset `01a0fc02-a13d-77a2-8de3-82459eb2a2a6` y
   `hold_music_asset_id`). El campo `execution` no se guarda por API (se queda el de por defecto).
2. Añadir el Python «Preparar transferencia» con `parent_node_id` = la herramienta (el Transfer existente pasa a
   colgar del Python).
3. Borrar ese Transfer (es una hoja) y añadir en un lote el Paths (`type: "path"`), la condición «Transferir» y el
   Transfer nuevo con la configuración de arriba (cambiando el persistent_id del Python y de la herramienta).
4. Ojo: el extract «Registrar resultado de la llamada» lee `extension_destino` y `transfer_succeeded` de los
   Transfer antiguos; lo rehace la Tarea 13.
