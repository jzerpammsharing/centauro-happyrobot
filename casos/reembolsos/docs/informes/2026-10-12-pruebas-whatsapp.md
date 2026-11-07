# Informe de pruebas · Datos por WhatsApp durante la llamada (12/10/2026)

Resumen de lo que se ha probado de «Centauro Reembolsos WhatsApp» (W1, voz) y «Centauro Reembolsos
· Datos por WhatsApp» (W2, texto), cómo y con qué resultado, y de lo que **no** se ha probado. Spec
en `docs/specs/2026-10-12-datos-por-whatsapp.md`; evals en `pruebas/evals-whatsapp.md`.

Ninguna prueba se hizo con clientes ni con datos reales: reserva `ER00000000` / `ER12345678`,
nombre «Prueba Prueba» y el móvil del equipo, que va en una variable del workflow y no en el repo.

## 1. Resumen

| Bloque | Qué cubre | Resultado |
|---|---|---|
| T3 · publicar la señal (4 intentos, llamada web) | Que la señal de W2 llega a la llamada de W1 con su payload | Tras 4 intentos, OK con Webhook POST a la API de signals |
| Evals de HappyRobot (10) | Lógica de conversación del prompt de W1 v2 | 10/10 PASS en la ronda 2 (8/10 en la 1) |
| E2E por WhatsApp (W1 v2 + W2 v4) | Oferta, envío, respuesta del cliente, señal y consulta | Caso principal OK |
| Casos 5.b–5.f, comillas, plantillas por idioma | Normalización, imágenes, audio, límites | **Sin probar** (apartado 5) |

## 2. Señal de W2 a W1 (T3, paso 8): 4 intentos

Se probó con llamadas web (`from_number = web`) y un teléfono de prueba fijado en la variable
`TELEFONO_PRUEBA` de W1. W2 estaba en modo prueba: publicaba un payload fijo sin enviar WhatsApp.

| # | W1 / W2 | Versión de W2 | Qué se hizo | Resultado |
|---|---|---|---|---|
| 1 | `617b2b8e-fc18-4519-a259-4e900fa86171` / `4bb78986-a2b0-4773-905f-771dba3c2149` | v1 | Nodo Send Signal con el payload en `body.raw` | El webhook funciona, W2 arranca y la señal llega a la sesión correcta y despierta al agente, pero el **payload llega vacío** (`{}`) |
| 2 | `b27d47d0-7086-405f-b56c-ec46c6a67394` / `1a60e390-f559-4d7f-8518-78bdaffd281e` | v2 | El mismo nodo, con el JSON también en el campo `message` | Igual: señal recibida con el **payload vacío**. El nodo Send Signal no entrega el payload ni con `body` ni con `message` |
| 3 | — / `8abcacb8-7dea-4436-a5b8-91c2882c8246` | v3 | Se sustituye Send Signal por un Webhook POST a `https://platform.eu.happyrobot.ai/api/v2/signals` (`key`, `env`, `payload`) con la API key de la organización | La API responde **403** («API key cannot perform action workflow.trigger»): la URL y la autenticación valen, falta permiso con el rol Viewer |
| 4 | `3ee5633a-a9bd-4577-8c58-e46d3f5e50bd` / `d60f57b3-88da-4c93-9c84-1a00bfd64948` | v3 | Rol de la API key subido a uno con `workflow.trigger` | La API devuelve `published` y la señal llega con el **payload completo**. El agente (aún sin reglas de WhatsApp) usa reserva y nombre del payload, pide la fecha por voz y consulta. **OK** |

Lecciones (también en `prompts/reembolsos-whatsapp-datos/v3/README.md`):
- El nodo Send Signal no sirve para este caso: el payload llega vacío. Se publica con Webhook POST
  a la API de signals.
- El nodo POST se marca «succeeded» aunque la API devuelva un 4xx: el error va en `data`. Hay que
  comprobar `status == "published"`.
- En la transcripción la señal aparece como turno `user` con `<Signal Received>{…}</Signal Received>`.
- Los outputs del trigger de W2 guardan las cabeceras (incluida la API key) y el teléfono: no
  copiarlos al repo.

## 3. Evals de HappyRobot sobre el prompt de W1 v2

Diez evals personalizados sobre el nodo de prompt de W1 v2, con la señal simulada como mensaje
`user` con `<Signal Received>…`. Detalle, ids y cómo repetirlos en `pruebas/evals-whatsapp.md`.

| Eval | Qué comprueba | Ronda 1 | Ronda 2 |
|---|---|---|---|
| 4a1 oferta inicial | Ofrece WhatsApp al mirar la reserva, sin herramientas | PASS | PASS |
| 4a2 acepta → envía | Ejecuta `enviar_whatsapp` con `idioma: es` | PASS | PASS |
| 4a3 señal con fecha ya dada | «Me ha llegado, gracias» sin repetir datos y consulta | **FAIL** | PASS |
| 4b rechaza | Pide la reserva por voz, sin enviar | PASS | PASS |
| 4c señal pegada sin fecha | Acusa recibo y pide la fecha, sin consultar | PASS | PASS |
| 4d segunda oferta | Tras «no encontrada», dice que no aparece y ofrece WhatsApp | **FAIL** | PASS |
| 4e no reenviar | No reenvía; ofrece dictar | PASS | PASS |
| 4f sin WhatsApp | No lo menciona si `whatsapp_posible` es false | PASS | PASS |
| 4g inglés | `enviar_whatsapp` con `idioma: en` | PASS | PASS |
| 4h señal tardía | Ignora la señal tras verificar | PASS | PASS |

- **Ronda 1: 8/10.** 4a3 repetía nombre y fecha en voz alta al llegar la señal y 4d no hacía la
  segunda oferta (tres pasadas). Ambos eran del prompt.
- **Ronda 2: 10/10.** Se ajustó el prompt en el sitio (sin publicar): acuse corto sin repetir datos y
  consulta en el mismo turno, y la segunda oferta como lo primero de la rama «No encontrada» (con la
  frase de que no aparece con esos datos).
- **Límite:** los evals cubren la lógica del prompt, no lo asíncrono (señal real en mitad de la
  llamada), que se probó con las llamadas del apartado 2 y 4. Con el resultado de la herramienta
  simulado, 4a2 y 4g solo valoran la llamada a la herramienta.
- Se pueden repetir contra cualquier versión nueva de W1 con `manage_custom_evals`.

## 4. Prueba de extremo a extremo por WhatsApp

Una llamada web de W1 v2 con W2 v4 (agente de WhatsApp real, plantilla mock `info_minibus`):

- W1 v2: run `3891a3f4-76b7-412d-bc9a-ce21edf5273a`
- W2 v4: run `a54d5b89-59ce-4780-9a06-ee52905a30d7`

Paso a paso:

1. El agente de voz saluda, el cliente dice que no le ha llegado la devolución y el agente ofrece
   enviar un WhatsApp para no dictar los datos.
2. El cliente acepta. El agente ejecuta `enviar_whatsapp` con `idioma: es`, que hace el POST a W2.
3. En el mismo turno el agente dice que ya se lo ha enviado y pide la fecha de nacimiento por voz.
4. W2 arranca y envía la plantilla mock `info_minibus` desde el número de empresa
   +44 20 4621 5219; llega al móvil del equipo. (Desde el 12/10/2026 a las 10:08 también probado con el número español +34 914 83 13 55, run de W2 `eeaf365c`.)
5. El cliente responde por WhatsApp con la reserva (`ER12345678`) y el nombre («Prueba Prueba»).
6. El agente de texto ejecuta `pasar_a_llamada`; el POST a la API de signals devuelve
   `published`.
7. En la llamada llega la señal; el agente dice «Me ha llegado, gracias.» y ejecuta
   `consultar_reembolso` con el payload y la fecha dada por voz.
8. La reserva no existe (datos de prueba), el resultado es «no encontrada» y el agente pide repetir
   los datos despacio sin ofrecer otro WhatsApp, porque ya se envió uno. Es el comportamiento
   esperado.

Observación: tras «no encontrada» con datos llegados por WhatsApp, quizá sea mejor pedir que revise
lo que escribió en el WhatsApp que pedir un dictado carácter a carácter (en pendientes).

## 5. Lo que no se ha probado

Por decisión del usuario del 12/10/2026 se da por cubierta la tarea de pruebas con el E2E del
apartado 4 y los 10 evals. Queda sin probar:

| Caso | Qué falta |
|---|---|
| 5.b | Reserva con minúsculas o espacios: el agente de texto normaliza antes de enviar |
| 5.c | Captura del correo de la reserva (OCR) |
| 5.d | Nota de voz con los datos (transcripción) |
| 5.e | El cliente pregunta por la fianza o el reembolso por WhatsApp: «Eso se lo cuento por teléfono» |
| 5.f | El cliente reescribe datos después de enviarlos: el agente repite el mensaje de cierre |
| Comillas | Valores con `"`, `\` o saltos de línea en la reserva o el nombre: se añadieron instrucciones de limpieza al prompt y a la herramienta, pero no se ha comprobado cómo escapa la plataforma `{{$var}}` dentro de `body.raw` |
| Plantillas | Plantillas aprobadas por Meta `datos_llamada_es/en/it/pt` y selección por idioma: el mock es una sola plantilla (habla del minibús) |
| Otros casos del spec | Sin prueba real: teléfono fijo u oculto (solo el eval 4f), error del webhook y cierre por inactividad de 15 minutos |

Antes de publicar a clientes, como mínimo hay que cerrar las plantillas por idioma, quitar el mock
y repetir el E2E con la plantilla real.
