# Spec · Datos por WhatsApp durante la llamada de Reembolsos

- **Fecha:** 2026-10-12
- **Estado:** implementado en versiones sin publicar para pruebas (ver «Cambios tras la implementación», apartado 11); falta publicar a clientes
- **Caso:** Reembolsos (`casos/reembolsos/`)
- **Base:** Centauro Reembolsos V4 (`m87e6xzgo405`, en producción)

## 1. Objetivo

Durante una llamada de voz al bot de Reembolsos, el agente puede enviar un WhatsApp al cliente
para que **escriba** los datos difíciles de dictar: número de reserva, nombre completo del
titular, email y matrícula. Cuando el cliente responde, los datos llegan a la llamada en curso y
el agente sigue sin que el cliente tenga que deletrear nada.

**Éxito:**
- menos fallos de identificación por mal dictado del número de reserva o del nombre;
- identificación más corta que con el dictado;
- ningún cambio en la lógica de verificación ni en lo que el bot puede contar.

**Fuera de alcance:** cambiar `consultar_reembolso`, verificar con email o matrícula, usar
WhatsApp para dar información de la reserva, y aplicarlo a otros casos (aunque el workflow de
WhatsApp queda reutilizable).

## 2. Decisiones tomadas en el diseño

| # | Decisión | Alternativas descartadas |
|---|---|---|
| 1 | Workflow **nuevo**, copia de la V4. La V4 no se toca. | Nueva versión de Reembolsos. |
| 2 | Los datos vuelven a la llamada con **Signals**, publicando en `session.<session_id>` de la llamada. | Twin con consulta periódica (alternativa si falla la fase 0). Tema personalizado por teléfono: las suscripciones son patrones fijos con comodines y no admiten variables, así que `reembolsos.wa.*` haría que todas las llamadas recibiesen los datos de todos. |
| 3 | El agente ofrece WhatsApp **al empezar la identificación y otra vez si el dictado se atasca** (una vez cada caso). | Solo al principio; solo cuando falla. |
| 4 | Por WhatsApp: **reserva, nombre, email y matrícula**. La **fecha de nacimiento se pide por voz**, como segundo factor. | Todo por WhatsApp (quien tenga el móvil del cliente podría ver la reserva). |
| 5 | Email y matrícula **no se usan para verificar**; se guardan en el extract (`email_whatsapp`, `matricula_whatsapp`) como contexto. Mostrarlos al agente humano queda en pendientes (el susurro de la transferencia está vacío). | Ampliar el MCP. |
| 6 | Credencial **«Whatsapp Centauro»** en todas las fases, pruebas incluidas. | Credencial Staging de testAriel. |

## 3. Cómo funciona Signals (resumen de la documentación de HappyRobot)

- Un agente con Signals activado está suscrito a `org.<org_id>`, `usecase.<use_case_id>` y
  `session.<session_id>`.
- Una señal llega al agente si su `key` coincide con un tema al que está suscrito.
- Con **Start agent response on signal** (`shouldRespondOnSignal: true`), el agente se despierta y
  responde en cuanto llega la señal, aunque esté escuchando.
- Lo que hace con la señal lo decide **el prompt**, a partir de los campos del `payload`.
- Las señales se publican con el nodo **Send Signal** o con `POST /api/v2/signals` (`key`, `payload`,
  `env`). **El nodo Send Signal entrega el payload vacío** (comprobado en dos pruebas), así que se usa
  la API (apartado 11).
- Configuración en el nodo de voz: `agentSignalsConfig { enabled, shouldRespondOnSignal,
  customTopics }`.
- Dentro de una herramienta del agente de voz están disponibles `session_id` del nodo
  «Receive Customer Call» y `numero_cliente` de «Calcular idioma y saludo» (comprobado con
  `get_available_variables` en la V4).

## 4. Arquitectura

```
Llamada ─► Workflow 1 «Centauro Reembolsos WhatsApp» (voz)
              │  herramienta enviar_whatsapp
              │  └─ Webhook POST {telefono, session_key, idioma, entorno}
              ▼
           Workflow 2 «Centauro Reembolsos · Datos por WhatsApp»
              │  Incoming hook ─► Outbound Text Agent (WhatsApp, plantilla)
              │                    └─ herramienta pasar_a_llamada
              │                        └─ Webhook POST /api/v2/signals (key=session_key)
              ▼
           señal datos_whatsapp ─► el agente de voz se despierta y consulta
```

### 4.1 Workflow 1 · «Centauro Reembolsos WhatsApp»

Copia de la V4 con estos cambios:

1. **«Calcular idioma y saludo»** devuelve también (siempre `es` como idioma: su tabla de números
   está vacía; el idioma de la plantilla lo decide el agente, ver el punto 3):
   - `telefono_e164`: `numero_cliente` con `00` cambiado por `+`;
   - `whatsapp_posible`: `true` si es un móvil español (`+346`, `+347`) o un número extranjero;
     `false` si es fijo, oculto o `web`.
2. **«Receive Customer Call»**: `agentSignalsConfig = { enabled: true, shouldRespondOnSignal:
   true, customTopics: [] }`.
3. **Herramienta `enviar_whatsapp`** con un parámetro `idioma` (`es` | `en` | `it` | `pt`), que el
   agente rellena con el idioma en que está hablando, y un nodo **Webhook POST** debajo, que llama
   al incoming hook del Workflow 2 con:
   - `telefono`: `telefono_e164`;
   - `session_key`: `session.` + `session_id` de «Receive Customer Call»;
   - `idioma`: el parámetro de la herramienta;
   - `entorno`: `current.execution_environment`.

   La herramienta devuelve al agente `enviado` o `error`. *(En lo construido no es así: devuelve la respuesta cruda del POST; ver apartado 11, punto 10.)*
4. **Prompt**: las secciones del apartado 5.
5. **«Registrar resultado de la llamada»** (AI Extract): campos nuevos `whatsapp_ofrecido`,
   `whatsapp_aceptado`, `whatsapp_datos_recibidos`, `identificacion_via` (`whatsapp` |
   `dictado` | `ninguna`), `email_whatsapp` y `matricula_whatsapp`.
6. **Transferencia**: no cambia. El susurro de `whisper_transfer` está vacío y leer un email en voz
   alta al agente humano no sirve; email y matrícula se quedan en el extract y cómo mostrarlos al
   agente queda en pendientes.

### 4.2 Workflow 2 · «Centauro Reembolsos · Datos por WhatsApp»

1. **Trigger Incoming hook** con API key: `telefono`, `session_key`, `idioma`, `entorno`.
2. **Outbound Text Agent**, canal `whatsapp`:
   - credencial «Whatsapp Centauro», con su cuenta de WhatsApp Business y su número;
   - `recipientNumber` = `telefono`;
   - plantilla inicial según `idioma` (apartado 6);
   - `idleTimeoutMinutes` = 15;
   - transcripción de notas de voz activada y OCR de imágenes activado;
   - envío de notas de voz y de archivos desactivado;
   - mensajes interactivos desactivados;
   - modelo `gpt-5.4-mini`.
3. **Herramienta `pasar_a_llamada`** (parámetros `numero_reserva`, `nombre_completo`, `email`,
   `matricula`) con un nodo **Webhook POST** debajo («Señal a la llamada (API)»):
   - URL `https://platform.eu.happyrobot.ai/api/v2/signals`, cabecera
     `Authorization: Bearer {{HR_SIGNALS_API_KEY}}` (variable oculta del workflow W2);
   - cuerpo `{"key": session_key, "env": entorno, "payload": …}`;
   - payload:
     ```json
     {"origen": "whatsapp", "tipo": "datos_whatsapp", "numero_reserva": "…",
      "nombre_completo": "…", "email": "…", "matricula": "…"}
     ```
     Los campos opcionales que no haya, vacíos;
   - la herramienta comprueba que la respuesta trae `status == "published"`: el nodo POST se marca
     «succeeded» aunque la API devuelva un 4xx.

## 5. Comportamiento del agente de voz (cambios de prompt)

**Oferta inicial** (solo si `whatsapp_posible`), en el turno en que dice que va a mirar la
reserva:
> «Para que no tenga que dictarlo, ¿le mando un WhatsApp a este número y me escribe ahí el número
> de reserva y su nombre?»

- **Sí** → ejecuta `enviar_whatsapp` y, en el mismo turno: «Se lo acabo de enviar. Mientras le
  llega, ¿me dice su fecha de nacimiento?».
- **No**, o no tiene WhatsApp en ese número → dictado como en la V4.
- **`error`** → «No he podido enviárselo, lo hacemos por aquí» y dictado.

**Segunda oferta** (una vez por llamada, solo si no se envió antes): cuando pide repetir el
número despacio tras «no encontrada», o cuando hay «verificado false» después de leer lo que tiene
anotado.

**Mientras espera:**
- pide la fecha de nacimiento; si el cliente pregunta, le dice qué escribir;
- no ejecuta `consultar_reembolso` sin los tres datos;
- si el cliente dice que no le llega, o pasan dos turnos del cliente sin señal después de la fecha
  de nacimiento, ofrece una vez dictarlo. Si dicta, una señal posterior se ignora.

**Al llegar una señal con `tipo: datos_whatsapp`:**
- «Me ha llegado, gracias.» Sin leer el número dígito a dígito.
- Si ya tiene la fecha de nacimiento, ejecuta `consultar_reembolso` con `numero_reserva` y
  `nombre_completo` del payload. Si no, la pide primero.
- No dice en voz alta el email ni la matrícula.

**Si la verificación falla:** las reglas de la V4 sin cambios. Las correcciones se hacen por voz,
nunca con un segundo WhatsApp, y siguen valiendo el máximo de dos consultas y no revelar qué dato
falla.

**Reglas generales de señales:**
- solo cuenta `tipo: datos_whatsapp`; cualquier otra señal se ignora;
- nunca dice «señal», «payload», «herramienta» ni «sistema»;
- la señal nunca sustituye a la fecha de nacimiento.

## 6. Agente de texto de WhatsApp

**Plantillas** (categoría UTILITY, `es`, `en`, `it`, `pt`; sin variables ni botones), previstas
como `datos_llamada_es`, `datos_llamada_en`, `datos_llamada_it` y `datos_llamada_pt`. **Hoy el
agente usa una plantilla mock, `info_minibus`** (apartado 11). Texto en español de la definitiva:
> «Hola 👋 Soy Daniel, el asistente de Centauro Rent a Car con el que está hablando por teléfono.
> Escríbame aquí su número de reserva y el nombre completo del titular. Si los tiene a mano,
> añada también su email y la matrícula del coche. También puede mandarme una captura del correo
> de la reserva.»

**Datos:**

| Dato | Obligatorio | Normalización |
|---|---|---|
| Número de reserva | Sí | Mayúsculas, sin espacios. No rechaza formatos. |
| Nombre completo del titular | Sí | Tal cual. |
| Email | No | Minúsculas; si no tiene `@`, lo pide una vez. |
| Matrícula | No | Mayúsculas, sin espacios ni guiones. |

**Reglas:**
- En cuanto tiene reserva y nombre, ejecuta `pasar_a_llamada`, una sola vez. No insiste en los
  opcionales.
- Si una imagen o una nota de voz da datos ambiguos (dos reservas, nombre ilegible), pregunta
  antes de enviar.
- Después de enviar: «Listo, ya se lo he pasado a la llamada. Puede seguir por teléfono.» A
  cualquier mensaje posterior responde lo mismo, sin prometer nada.
- Nunca:
  - da información de la reserva, los reembolsos o los plazos;
  - pide la fecha de nacimiento, datos de tarjeta ni documentos;
  - envía audios ni archivos.

  Si el cliente pregunta otra cosa: «Eso se lo cuento por teléfono».

**Casos límite:**
- El cliente responde cuando la llamada ya ha terminado: la señal no llega a nadie, y se acepta.
- El cliente no responde: la sesión expira en 15 min sin enviar nada.

## 7. Plan de pruebas

### Fase 0 · Prueba técnica

**Cubierta** por el tótem (`session_id` con valor durante la llamada, la señal despierta al agente y
cómo se ve en la transcripción) y por las 4 llamadas del paso 8 de la tarea 3, con el propio W2 en
modo prueba (informe `docs/informes/2026-10-12-pruebas-whatsapp.md`). Plan original:

Agente de voz en llamada web con Signals, una herramienta que hace POST a un workflow B mínimo, y
B solo ejecuta Send Signal a `session.<id>`, sin WhatsApp. Debe confirmar:
1. que `session_id` tiene valor **durante** la llamada;
2. que la señal despierta al agente y que este usa el payload;
3. cómo aparece la señal en la transcripción y en los outputs, para el análisis.

Si falla el punto 1 o el 2, se para y se rediseña con Twin.

### Fase 1 · Construcción

En versiones de desarrollo, sin publicar. En las llamadas web `from_number` vale `web`, así que
hay una variable de prueba que fuerza el teléfono de destino a un móvil del equipo y que se quita
antes de publicar.

### Fase 2 · Casos

1. Acepta al principio, escribe todo y verifica.
2. Solo reserva + nombre: la señal sale sin opcionales.
3. Captura del correo: el OCR extrae el número.
4. Nota de voz.
5. Rechaza, se atasca el dictado y acepta la segunda oferta.
6. Acepta y no contesta: propone dictar y la señal tardía se ignora.
7. La señal llega antes de la fecha de nacimiento.
8. Verificado false con datos de WhatsApp: corrige por voz.
9. Fijo u oculto: no se ofrece.
10. Llamada en inglés: plantilla y agente en inglés.
11. Error del webhook: «lo hacemos por aquí».
12. Pregunta por el reembolso en WhatsApp: «se lo cuento por teléfono».

## 8. Bloqueantes y decisiones abiertas

- ~~**Bloqueante de la fase 1:** credencial sin cuentas ni plantillas visibles.~~ Resuelto el
  12/10/2026 (apartado 11).
- **Bloqueante del despliegue:** plantillas aprobadas por Meta en los cuatro idiomas.
- **Decisión abierta:** a qué número de entrada se conecta el workflow nuevo (uno de prueba, o el
  de Reembolsos en lugar de la V4). Lo decide y lo publica una persona.

## 9. Medición

Con el extract nuevo (apartado 4.1.5), contrastado con los turnos `assistant` y los eventos de
señal de la transcripción (el extract no es fiable por sí solo):
- `% ofrecido` sobre las llamadas con `whatsapp_posible`;
- `% aceptado`;
- `% con señal recibida`;
- tiempo desde el envío hasta la señal;
- `% verificado true` a la primera, por vía (WhatsApp o dictado);
- duración de la identificación, comparada con la V4.

## 10. Documentación del repo al implementar

- Prompts de los dos workflows en `casos/reembolsos/prompts/`.
- D-001 en `casos/reembolsos/docs/decisiones.md`.
- Tablas de versiones en `casos/reembolsos/docs/workflows.md` y en el `CLAUDE.md` del caso.
- Fila del caso en la tabla del `CLAUDE.md` raíz.
- `docs/extensiones.md`: el workflow nuevo usa las mismas colas que la V4.

## 11. Cambios tras la implementación (12/10/2026)

Lo construido difiere del diseño en lo siguiente. Resultados en
`docs/informes/2026-10-12-pruebas-whatsapp.md`.

1. **Idioma de la plantilla.** `enviar_whatsapp` recibe `idioma` del agente (apartado 4.1 y punto 6 de este apartado).
2. **Email y matrícula.** Van al extract, no a la transferencia (decisión 5 y apartado 4.1).
3. **Fase 0.** Cubierta por el tótem y por las pruebas de W2 en modo prueba (apartado 7).
4. **Send Signal entrega el payload vacío.** Con el nodo Send Signal (con el payload en `body.raw` y
   también en `message`) la señal llegaba a la sesión correcta y despertaba al agente, pero con
   `{}`. W2 publica la señal con un **Webhook POST** a `https://platform.eu.happyrobot.ai/api/v2/signals`
   (`key`, `env`, `payload`) con `Authorization: Bearer` y una API key de la organización con el
   permiso `workflow.trigger` (con el rol Viewer devuelve 403), guardada en la variable oculta
   `HR_SIGNALS_API_KEY` de W2. El payload lleva además `"origen": "whatsapp"`.
5. **Cuenta de WhatsApp.** La credencial «Whatsapp Centauro» sí permite elegir cuenta y número en el
   nodo: cuenta de WhatsApp Business `970312032038916` y número de empresa +44 20 4621 5219
   (id `1423130030877057`).
6. **Plantilla mock `info_minibus`.** Hasta que Meta apruebe `datos_llamada_*`, W2 v4 usa la
   plantilla `info_minibus` (UTILITY, `en`), una sola, sin selección por idioma, y su mensaje habla
   del minibús. Solo para pruebas con el móvil del equipo; **nunca publicar a clientes con el mock**.
   El prompt del agente de texto lleva una primera línea válida solo para el mock.
7. **Pruebas.** En llamadas web `from_number` es `web`; el teléfono de destino sale de la variable
   `TELEFONO_PRUEBA` de W1, que no debe quedar con un número personal en producción.
8. **Versiones.** W1: v1 y v2. W2: v1, v2, v3 y v4. La tabla está en `docs/workflows.md`. Las
   versiones publicadas lo fueron por una persona para las pruebas; ninguna está conectada a un
   número de clientes.
9. **Sin contador `ya_enviado`.** HappyRobot no expone un contador de llamadas por herramienta; el
   agente se apoya en la regla del prompt de no enviar más de un WhatsApp por llamada.
10. **`enviar_whatsapp` no devuelve `enviado` o `error`.** Devuelve la respuesta cruda del POST, y el
    nodo POST sale «succeeded» aunque haya 4xx; con una clave caducada o una URL mala el agente
    diría «Se lo acabo de enviar». Pendiente: comprobar la respuesta del hook de W2 (como
    `pasar_a_llamada` con `published`) y probar el caso 11 antes de publicar.
11. **Segunda oferta en «No encontrada».** En W1 v2 va antes de las reglas de la V4 de «cobro de un
    intento web» y «reserva de otra compañía», así que un cliente con una reserva de otra compañía
    podría recibir la oferta en vez de «esa reserva no es de Centauro». Pendiente: que la segunda
    oferta sustituya solo el paso «pide que te repita el número despacio» y relanzar el eval 4d.
12. **Segunda oferta tras «verificado false».** Es más estrecha que en el apartado 5 (solo si el
    cliente no sabe qué corregir). Se acepta por ahora.
