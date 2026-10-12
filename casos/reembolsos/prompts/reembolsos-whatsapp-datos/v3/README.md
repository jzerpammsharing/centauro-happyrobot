<!-- workflow: Centauro Reembolsos · Datos por WhatsApp · versión: v3 (j0utp12shz0v) · copiado: 2026-10-12 -->
# W2 · v2 y v3 (modo prueba)

## v2 · «v1 + payload en message» (xc8n9t2rbods)

Igual que la v1, pero el JSON del payload va también en el campo `message` del nodo Send Signal.
Resultado: la señal llegaba a la llamada con el payload vacío (`{}`).

## v3 · «señal por API de signals» (j0utp12shz0v, publicada)

El nodo Send Signal se sustituye por un Webhook POST, «Señal de prueba (API)»:

- URL: `https://platform.eu.happyrobot.ai/api/v2/signals`
- Cuerpo JSON: `{"key": "<trigger.session_key>", "env": "<trigger.entorno>", "payload": {payload fijo de prueba}}`
  con `numero_reserva` = `ER00000000` y `nombre_completo` = `Prueba Prueba` (email y matrícula vacíos).
- Cabecera `Authorization: Bearer {{use_case_variables.HR_SIGNALS_API_KEY}}`. La clave es una
  variable oculta del workflow W2; no se guarda en el repo.

Resultado: la API devuelve `published` y el payload llega completo a la llamada (probado desde W1).

## Lecciones

- El nodo Send Signal exige `apiKeyId` en el editor y, aun así, entrega el payload vacío tanto desde
  el body como desde `message`.
- La API key necesita un rol con el permiso `workflow.trigger`: con el rol Viewer devuelve 403.
- El nodo POST muestra «succeeded» aunque la API devuelva un 4xx; el error está en `data`. Hay que
  mirar la respuesta, no solo el estado del nodo.
