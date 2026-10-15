# Workflows del caso Reembolsos

Los tres están en la carpeta de Centauro (`019d8144-ce27-7aaf-b9e5-21d006083063`). Comprobado con
`get_workflows` el 12/10/2026: la versión que aparece como actual de cada workflow es la que indica
la columna «Estado».

## Centauro Reembolsos (`01a0defb-9c46-7f81-b966-69ca9d211709`, slug `ey9623r10ly2`)

> **Congelado desde el 15/10/2026 (D-004).** El único bot de voz de Reembolsos es W1 («Centauro Reembolsos
> Llamada + w»). Este workflow no se borra ni se publica (la V5 queda sin publicar); los cambios se hacen solo en W1.

Voicebot de reembolsos y fianzas. Copia del prompt de la V4:
`prompts/reembolsos-v4/receive-customer-call.md`.

### Flujo
Por nombre de nodo, en línea:
1. Inbound Call (trigger).
2. Calcular idioma y saludo (Python Sandbox).
3. Receive Customer Call (agente de voz), con el prompt «Reembolsos» y sus herramientas:
   `consultar_reembolso` y `transfer_to_human_agent` (con «Initiate customer connection»).
4. Registrar resultado de la llamada (AI Extract).

### Versiones
| Versión | Slug | Nombre en HappyRobot | Descripción | Estado |
|---|---|---|---|---|
| 4 | `m87e6xzgo405` | Version 4 | Versión en producción | Base de la V5. Ojo: el 14/10/2026 HappyRobot la lista como no publicada (la publicada es la V3, `1ahurz19vb34`); confirmar cuál recibe llamadas |
| 5 | `gwe1rc4d1po6` | Version 5 | V4 + identificación por email o DNI/NIE (D-003) | Sin publicar y congelada (D-004): su contenido está en W1 v3/v4. Copia: `prompts/reembolsos-v5/` |

## Centauro Reembolsos WhatsApp (`01a12d4e-7c03-7494-8e0c-194e1256f8fb`, slug `j2cgq0sfra2q`) · W1

Voz. Copia de la V4 con la oferta de WhatsApp (decisión D-001, spec en `docs/specs/`). El agente
ofrece mandar un WhatsApp para que el cliente escriba reserva, nombre, email y matrícula; la
respuesta vuelve a la llamada como señal. La fecha de nacimiento sigue siendo por voz.

### Flujo
1. Inbound Call (trigger).
2. Calcular idioma y saludo: lo de la V4 más `telefono_e164` y `whatsapp_posible`. El teléfono sale
   de `from_number`; si es `web` (llamada de prueba) usa la variable `TELEFONO_PRUEBA`.
3. Receive Customer Call (agente de voz) con Signals activado (`shouldRespondOnSignal`); prompt
   «Reembolsos» con las reglas de WhatsApp y herramientas:
   - `enviar_whatsapp` (parámetro `idioma`) con el nodo «POST petición de datos» a W2 (URL y API key
     en variables del workflow `WA_DATOS_URL` y `WA_DATOS_API_KEY`);
   - `consultar_reembolso`;
   - `transfer_to_human_agent` con «Initiate customer connection».
4. Registrar resultado de la llamada (AI Extract): los campos de la V4 más `whatsapp_ofrecido`,
   `whatsapp_aceptado`, `whatsapp_datos_recibidos`, `identificacion_via`, `email_whatsapp` y
   `matricula_whatsapp`.

Copias de los prompts: `prompts/reembolsos-whatsapp/v1/` (nodos), `v2/` (prompt y extract) y `v3/` a `v5/` (prompt).

### Versiones
| Versión | Slug | Nombre en HappyRobot | Descripción | Estado |
|---|---|---|---|---|
| v1 | `1g52kgh7y4pn` | v1 · V4 + datos por WhatsApp | Copia de la V4 + Signals + `enviar_whatsapp` | Publicada por una persona para las pruebas de la señal; superada por la v2 |
| v2 | `pc4zvke3xdjl` | v2 · v1 + oferta de WhatsApp y lectura de señales | Prompt con reglas de WhatsApp, evals 10/10, extract de WhatsApp | Publicada por una persona; recibió las llamadas de la línea +34 911 200 3002 desde el 12/10/2026. Superada |
| v3 | `o9e9ly8yd6bx` | Version 3 | v2 + identificación por email o DNI/NIE (D-003); la señal de WhatsApp trae `dni` en vez de `matricula` | Publicada (live el 15/10/2026, no por Claude). Copia: `prompts/reembolsos-whatsapp/v3/` |
| v4 | `n9k51iiu8ehw` | v4 · v3 + WhatsApp solo con dificultad y «ya he encontrado su reserva» | Sin oferta inicial de WhatsApp: se ofrece una vez, solo con dificultad (corrección de un dato repetido, dato confuso al segundo intento, no encontrada, verificado false o dato no interpretado). Al verificar dice «Ya he encontrado su reserva» (D-004) | Publicada el 15/10/2026 (no por Claude). Prueba por voz de la tarde con fallos: informe `docs/informes/2026-10-15-pruebas-tarde-w1-v4.md`. Superada por la v5 el mismo día. Copia: `prompts/reembolsos-whatsapp/v4/` |
| v5 | `ok9wpis1yhs3` | v5 · v4 + nombre sin inventar, email sin guiones y espera del WhatsApp | Nombre solo si lo da el cliente; email deletreado sin guiones de la transcripción; «Me ha llegado» solo con señal; espera del WhatsApp sin repetir ni ofrecer voz por silencio; tercera consulta con datos de WhatsApp; `consultar_reembolso` ajustada (D-005) | **Actual**: publicada el 15/10/2026 por la tarde (por una persona, junto con W2 v9), con evals en verde y sin prueba por voz previa. Copia: `prompts/reembolsos-whatsapp/v5/` |

El workflow se llama ahora en HappyRobot «Centauro Reembolsos Llamada + w» (visto el 14/10/2026).

## Centauro Reembolsos · Datos por WhatsApp (`01a12d4c-5fe2-76d7-a233-3d5a16972ffd`, slug `p45rx5hlsber`) · W2

Texto. Lo llama W1 por webhook, escribe al cliente por WhatsApp, recoge los datos y los publica
como señal en la sesión de la llamada.

### Flujo (v4)
1. Petición desde la llamada (trigger «Incoming hook» con API key): `telefono`, `session_key`,
   `idioma`, `entorno`.
2. Agente de WhatsApp (Outbound Text Agent): credencial «Whatsapp Centauro», número de empresa
   +34 914 83 13 55 (id `1359458737254289`; hasta el 12/10/2026 a las 09:50 se usó +44 20 4621 5219),
   plantilla inicial mock `info_minibus`, inactividad de 15 minutos. Herramienta
   `pasar_a_llamada`.
3. Señal a la llamada (API): Webhook POST a `https://platform.eu.happyrobot.ai/api/v2/signals` con
   `Authorization: Bearer` y la variable oculta `HR_SIGNALS_API_KEY`. Comprueba `status == "published"`.

### Cambios de la v7 (D-002)
- Nodo nuevo «Elegir plantilla» (Python Sandbox) tras el trigger: da `idioma_plantilla` (`es`, o
  `en` para el resto).
- Nodo de rutas «Idioma de la plantilla»: «Español» → «Agente de WhatsApp (es)»; «Fallback» →
  «Agente de WhatsApp (en)». Cada agente lleva `datos_reserva` en modo estático con el idioma fijado
  por la API, sin parámetros, y su copia de `pasar_a_llamada` y del POST «Señal a la llamada (API)».
  **Los cambios de prompt, herramienta o POST van en las dos ramas.**
- Prompt sin la primera línea de la plantilla mock.
- No editar la plantilla desde el desplegable del editor: guarda la inglesa en las dos ramas.

Copias: `prompts/reembolsos-whatsapp-datos/` (v1, v3 a v9).

### Versiones
| Versión | Slug | Nombre en HappyRobot | Descripción | Estado |
|---|---|---|---|---|
| v1 | `2afxs944xpxt` | Version 1 | Modo prueba: Send Signal con payload fijo | Publicada por una persona para pruebas; superada |
| v2 | `xc8n9t2rbods` | v2 · v1 + payload en message | Payload también en `message` | Superada: la señal seguía llegando con el payload vacío |
| v3 | `j0utp12shz0v` | v3 · señal por API de signals | Webhook POST en lugar de Send Signal | Superada por la v4 |
| v4 | `qw83lg2g3sa6` | v4 · agente de WhatsApp (plantilla mock info_minibus) | Agente de texto de WhatsApp con la plantilla mock y `pasar_a_llamada` | **Actual** (publicada por una persona para pruebas) |
| v5 | `0urzqrnn4yfr` | v5 · v4 + plantilla datos_reserva (es/en por ID) | Plantilla `datos_reserva` en modo dinámico con el ID de Meta (D-002) | No funciona (`template_not_found`: busca por nombre). Publicada solo en development para la prueba |
| v6 | `ag32yoirx45a` | v6 · prueba: plantilla estática datos_reserva con idioma es | Prueba: plantilla estática con `language = es` fijado por la API | Llega en español. Publicada solo en development para la prueba |
| v7 | `63eqtfk9nrdl` | v7 · v4 + plantilla datos_reserva (rama es / en) | Plantilla real con una rama y un agente por idioma (D-002) | Publicada (vista live el 14/10/2026) |
| v8 | `fm6g5527v6lw` | Version 8 | v7 + el agente acepta número, email o DNI/NIE y pasa `dni` en lugar de `matricula` (D-003, en las dos ramas) | Publicada (live el 15/10/2026, no por Claude). Copia: `prompts/reembolsos-whatsapp-datos/v8/`. La plantilla `datos_reserva` no cambia: sigue pidiendo número, nombre, y email y matrícula opcionales |
| v9 | `n1ij39vr42xd` | v9 · v8 + pide el nombre y no repite la pregunta | Contesta según lo que ya tiene: con el dato de la reserva pide solo el nombre; email o DNI/NIE valen como dato; no repite mensajes; el nombre no sale del email; el número ER no va en `dni` (D-005, en las dos ramas) | **Actual**: publicada el 15/10/2026 por la tarde (por una persona, junto con W1 v5). Copia: `prompts/reembolsos-whatsapp-datos/v9/` |

El workflow se llama ahora en HappyRobot «Centauro Reembolsos (wa) · Datos por WhatsApp».

**Entrada de llamadas (12/10/2026):** W1 v2 recibe las llamadas de la línea +34 911 200 3002 (las
primeras, a las 09:44). Mientras W2 use la plantilla mock `info_minibus`, un cliente que acepte el
WhatsApp recibirá el mensaje del minibús: ver «Antes de publicar a clientes». La V4 tiene asignado el
número «Onboarding» +1 628 214 2490 y en los runs revisados solo se ven llamadas web.

**Si no llegan los WhatsApp:** W2 tiene que tener una versión publicada; el webhook de W1 solo llega a
la versión publicada (el 12/10/2026 dejaron de llegar mientras W2 estaba despublicada para cambiar el
número). Al cambiar el número en el nodo, elígelo de nuevo en el desplegable y comprueba en Meta que
está en la misma cuenta de WhatsApp Business (`970312032038916`), donde está aprobada la plantilla.

## Antes de publicar a clientes

Checklist para W1 y W2. Esta rama debe revisarse antes de publicar (CLAUDE.md raíz, apartado 3).

- [ ] **Plantilla mock.** W2 v4 usa `info_minibus`. La v7 la sustituye por `datos_reserva` (rama
  es/en; D-002). Antes de publicarla: comprobar con un envío real en `es` y en `en` que llega cada
  plantilla en su idioma.
- [ ] **`HR_SIGNALS_API_KEY`.** Tiene un rol con `workflow.trigger` en todo el workspace y no caduca:
  limitarla por etiquetas a Centauro y darle caducidad y rotación.
- [ ] **Hook de W2.** El hook publicado solo está protegido por `WA_DATOS_API_KEY`: quien la tenga
  puede hacer que el número de Centauro envíe WhatsApps y publicar señales en sesiones. Limitar y
  rotar la clave.
- [ ] **Variables de W1.** `TELEFONO_PRUEBA` vacío en producción y `WA_DATOS_URL` apuntando al hook de
  producción (el valor de desarrollo es `/hooks/development/…`).
- [ ] **Dependencias.** Se depende de `/api/v2/signals` (si HappyRobot arregla Send Signal se puede
  volver) y del escape de JSON de `{{$var}}` en `body.raw`, sin verificar.
- [ ] **Texto del cliente.** Lo que escribe el cliente llega al agente de voz (riesgo de inyección de
  instrucciones). Mitigado porque la fecha de nacimiento va por voz y la verificación es en el
  servidor.
- [ ] **Sin probar:** 5.b–5.f, comillas en los datos, fijo u oculto en una llamada real, error del
  webhook (caso 11), cierre a los 15 minutos, caso 12, una llamada real en otro idioma. Además, un
  fijo extranjero da `whatsapp_posible = true`.
- [ ] **Datos personales en HappyRobot.** `email_whatsapp` y `matricula_whatsapp` (extract) y los
  outputs del trigger de W2 (teléfono y cabeceras) quedan guardados. No copiarlos al repo y valorar
  la retención.
- [ ] Pendientes abiertos en `docs/pendientes.md` revisados.

