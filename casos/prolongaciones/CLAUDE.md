# CLAUDE.md — Caso Prolongaciones

Contexto propio del caso Prolongaciones. Las reglas comunes (forma de trabajar, transferencias,
RingCentral, convenciones) están en el `CLAUDE.md` de la raíz.

## 1. Qué es

Un voicebot de HappyRobot con el agente «Daniel Prolongaciones». Atiende la opción **PROLONGACIÓN**
del menú telefónico de Centauro España.

- **A quién atiende.** Sobre todo a clientes con un alquiler en curso que quieren quedarse el coche
  más tiempo, a menudo con la devolución en pocas horas. Como el menú se marca mal, también le llegan
  otras consultas: reservas que no han empezado, recogidas tarde, fianza, combustible, cargos,
  averías, minibús.
- **Qué resuelve sin transferir:**
  - explica que la prolongación la hace el cliente desde su área de cliente en centauro.net o en la app;
  - le dice cómo crear la contraseña si no la tiene y le da los pasos;
  - responde una lista cerrada de consultas frecuentes.
- **Qué no puede hacer:** no tiene acceso a ninguna reserva, así que no prolonga, no cobra y no
  comprueba nada. Lo que exige mirar o cambiar una reserva se transfiere a una persona.

| Workflow | País | workflow_id | slug | Producción (11/10/2026) |
|---|---|---|---|---|
| Centauro Prolongacion Spain | ES | `01a0d9de-b1cd-7bc9-bafc-f5117bd57249` | `tiz1bci7y0dh` | Version 11 (`2g1bxzyzazpp`) |

- **Ficha del workflow** (flujo, comportamiento esperado, campos del extract, versiones):
  `docs/workflows.md`.
- **Colas:** `../../docs/extensiones.md`. Prolongaciones comparte colas con Minibús:
  - con todos los bots de Minibús, 18056 y 18059;
  - con Minibús España desde su v19, 18057, 18061, 18001, 18006 y 18034.

## 2. Carpetas del caso

| Ruta | Qué contiene |
|---|---|
| `docs/decisiones.md` | Decisiones de Prolongaciones (D-NNN) |
| `docs/workflows.md` | Ficha del workflow y tabla de versiones |
| `docs/pendientes.md` | Incidencias abiertas y mejoras propuestas |
| `prompts/prolongacion-es/<versión>/` | Copias de los prompts y de la configuración de los nodos |
| `rutinas/informe-prolongaciones.md` | Prompt de la rutina diaria de calidad |

## 3. Reglas propias de Prolongaciones

### Workflow
- **Estructura.** Un solo módulo de prompt («Prolongacion») y una sola herramienta
  (`transfer_to_human_agent`). No hay herramientas de consulta ni herramientas que devuelvan vacío a
  propósito, al contrario que en Minibús. Si un análisis ve una herramienta distinta, es un error.
- **Horario.** El bot atiende siempre: no tiene horario nocturno ni derivación. Solo la cola de
  Gestión tiene horario: lunes a viernes de 08:00 a 21:00, hora peninsular. Lo calcula
  `gestion_abierta` en «Calcular idioma y saludo».
- **Gestión cerrada.** Con Gestión cerrada, «Resolver colas» pone en `cola_gestion_reserva` el texto
  «NO DISPONIBLE AHORA…» en vez de una extensión. Si ese texto aparece en `extension_destino` o en el
  error de una transferencia («invalid phone number for Number: +1NO DISPONIBLE…»), es el fallo
  conocido de `docs/pendientes.md`.
- **Idiomas:**
  - el idioma sale del número marcado: la línea inglesa da inglés y el resto, español;
  - el agente atiende en español, inglés, italiano y portugués, pero solo hay colas en español e
    inglés;
  - en francés no hay atención;
  - un idioma no atendido se transfiere a la cola de Minibús.
- **Variables.** En el prompt aparecen como `{{ index . "<persistent_id>.<variable>" }}`. Son dos,
  `idioma_nombre` y `gestion_abierta`, y no están rotas.
- **Teléfonos.** Los únicos que puede dar el bot son los que están en «TELÉFONOS QUE PUEDES DAR»:
  asistencia en carretera, reservas nuevas y las oficinas de Benidorm y Torrevieja (solo para el
  servicio de entrega). Si da cualquier otro, es un fallo.
- **Whisper.** El susurro al agente incluye el teléfono del cliente dictado cifra a cifra. Es a
  propósito, para que el agente pueda devolver la llamada. Nunca copies ese texto al repo.

### Análisis de llamadas
- **Transferencias:** los outputs de «Initiate customer connection» son la fuente de verdad. Además
  de los resultados de la regla común:
  - `invalid phone number … NO DISPONIBLE`: el bot intentó transferir a Gestión cerrada;
  - `whisper_transfer_no_bridge` en Gestión en fin de semana puede salir aunque no cogiera nadie
    (RingCentral lo da como Missed);
  - `transfer_result_timeout` con `no_response` a 360 s: el agente atendió;
  - `max_duration_reached` (unos 600 s): límite del agente de voz, también mientras espera la
    transferencia;
  - si la llamada conecta con una persona, su duración puede pasar de los 600 s (624, 865 o 900 s).
- **El extract no es fiable** y además evalúa también al agente humano tras la transferencia:
  - dan muchos falsos positivos `resuelto_sin_transferencia`, `hubo_transferencia`,
    `invento_informacion`, `pidio_dato_personal` y `dijo_precio_o_penalizacion`;
  - el prompt del extract prohíbe dar «el importe de la penalización» y teléfonos de oficina, pero
    el prompt del bot sí permite la penalización de 50 €/día, otras tarifas generales y los teléfonos
    de Benidorm y Torrevieja.
  - Un fallo del bot solo cuenta si se ve en los turnos `assistant`.
- **Problemas de conversación ya vistos** (de la conversación, no del prompt): turnos cortados,
  bloques largos repetidos, el bucle de «¿ha entrado alguna vez en su cuenta?» y suposiciones sin
  preguntar (que el coche es de empresa, que la reserva no ha empezado).

## 4. Rutina diaria de calidad

`rutinas/informe-prolongaciones.md` es una rutina en la nube, «Centauro Prolongaciones - informe
diario», que se ejecuta cada día a las 22:05 de Madrid. Hace tres cosas:
- analiza las llamadas del día en HappyRobot y RingCentral, en solo lectura;
- escribe las cifras en los dos artefactos de abajo;
- devuelve el informe.

El fichero del repo está actualizado a la V11. La rutina programada en la nube sigue con el prompt
del 09/10 (V8) y no se ha cambiado.

| Artefacto | Compartido con | La rutina escribe en | Solo lo escriben los revisores |
|---|---|---|---|
| [Calidad Prolongaciones](https://claude.ai/artifact/3i8Reh68FkdQDACdZdFq3A) | personas concretas | `informes` (doc_id = AAAA-MM-DD) | dentro de `informes`, los campos `evaluacion_versiones`, `diff_versiones`, `mejoras` e `info_que_falta`, que se escriben a mano |
| [Respuestas de Daniel](https://claude.ai/artifact/L4cpA1DVsHPdT3ELCQJY2Y) | toda la organización | `volumen` (doc_id = fecha) y `detectadas` (doc_id = slug de la pregunta) | `reviews`, `rev`, `offices`, `contra` y `miss` |

- **Calidad Prolongaciones:**
  - arriba muestra el seguimiento diario;
  - en medio, la tabla «versión a versión», que se calcula con los campos `version` y `versiones`
    de cada informe;
  - al final, el análisis del día 1 (05/10).
- **Respuestas de Daniel:** es la revisión compartida de lo que debe contestar el bot. El equipo
  marca cada respuesta como correcta, por cambiar o descartada, y rellena las contradicciones, lo
  que falta y la tabla de oficinas. La rutina solo añade el volumen por tema y las preguntas nuevas
  que el bot no supo contestar.
- Las claves de cada documento y su significado están en la sección 7 del prompt de la rutina.
