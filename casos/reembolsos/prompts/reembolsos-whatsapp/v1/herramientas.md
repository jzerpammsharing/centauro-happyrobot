<!-- workflow: Centauro Reembolsos WhatsApp · versión: v1 (1g52kgh7y4pn) · nodo: enviar_whatsapp y POST petición de datos · copiado: 2026-10-12 -->

Herramienta nueva, hija del prompt «Reembolsos». Su única acción es el webhook POST a W2
(«Centauro Reembolsos · Datos por WhatsApp»).

## Herramienta `enviar_whatsapp`

- Descripción: Envía al móvil del cliente un WhatsApp para que escriba ahí su número de reserva, su
  nombre completo, su email y la matrícula. Úsala solo si el cliente ha aceptado y solo una vez por llamada.
- Parámetro `idioma` (obligatorio): Idioma en que estás hablando con el cliente ahora mismo.
  Exactamente uno de: es, en, it, pt.
- Mensaje (tipo `ai`): ejemplo «Un momento, se lo envío.»; descripción: «Di en pocas palabras, en el
  idioma del cliente, que le envías el WhatsApp.»

## Nodo «POST petición de datos» (hijo de la herramienta)

Evento POST (`01926f2b-2973-7ebf-ada1-e984251e27ec`), esquema v2 (`body.raw`, no `rawBody`).

- URL: `{{use_case_variables.WA_DATOS_URL}}`
- Cabecera `x-api-key`: `{{use_case_variables.WA_DATOS_API_KEY}}`
  (la cabecera `x-api-key` funcionó en las llamadas de la tarea 3 y en la prueba de extremo a extremo)
- `authType`: `none`; `contentType`: `application/json`; `ignore5XX`: `false`; `webhookSchemaVersion`: 2
- Cuerpo (`body.raw`; los tokens `$var` apuntan, por persistent_id, a «Calcular idioma y saludo»,
  «Receive Customer Call» y la herramienta `enviar_whatsapp`):

```json
{"telefono": "{{$var:<PID_IDIOMA>.telefono_e164}}",
 "session_key": "session.{{$var:<PID_AGENTE>.session_id}}",
 "idioma": "{{$var:<PID_HERRAMIENTA>.idioma}}",
 "entorno": "{{$var:current.execution_environment}}"}
```

Variables del workflow que crea la persona en HappyRobot (no van al repo): `WA_DATOS_URL`,
`WA_DATOS_API_KEY`, `TELEFONO_PRUEBA`.

## Receive Customer Call

Se añade a la configuración de la V4: `"agentSignalsConfig": {"enabled": true, "shouldRespondOnSignal": true, "customTopics": []}`.
