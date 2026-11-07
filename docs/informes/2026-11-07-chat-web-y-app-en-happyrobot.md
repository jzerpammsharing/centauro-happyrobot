# Chat en la web y en la app con HappyRobot: qué se puede hacer

- **Fecha:** 07/11/2026
- **Para qué:** ver si HappyRobot sirve para un agente de chat en la web y en la app de Centauro, y cómo.
- **Fuentes:** la búsqueda de documentación del conector de HappyRobot (la web de documentación pide un
  código de acceso), los esquemas de los nodos del workspace de Centauro (`get_node_config_schema`) y
  los tipos y el README del SDK `@happyrobot-ai/sdk` 0.2.2 de npm.
- **Lo que no se ha probado:** nada se ha montado ni ejecutado. Todo sale de la documentación y de los esquemas.

## 1. Resumen

HappyRobot tiene un canal de **chat web propio**, sin credenciales de terceros. Funciona con los mismos
prompts, herramientas y Module Change que los bots de voz. Hay dos formas de usarlo:

1. **Widget listo para usar:** se pega un script en la web y aparece la burbuja de chat.
   No hace falta programar nada.
2. **Interfaz propia con el SDK:** la app o la web pinta el chat a su manera y habla con HappyRobot por
   WebSocket. Para esto hace falta un pequeño backend que genere tokens.

**No hay SDK nativo de iOS ni de Android.** Para la app hay tres caminos (apartado 4).

## 2. Piezas del workflow

| Pieza | Nodo | Notas |
|---|---|---|
| Disparador | **Chatbot Request** (`019a7b24-…`) o **Inbound Text Message** | Su única configuración son los `params`: los datos que la web pasa al empezar el chat |
| Agente | **Inbound Text Agent** con `channel = chatbot` | El mismo nodo sirve para WhatsApp, SMS, email, Slack y Teams |
| Mensaje fijo | **Deliver Text Session Message** | Mete un mensaje en el chat sin pasar por el LLM, por ejemplo un enlace o un aviso legal |

Opciones del Inbound Text Agent que importan para Centauro:

- **Dominios registrados** (`registeredDomains`): el widget solo carga en esos dominios y en los demás falla
  sin avisar. Hay que poner todas las variantes, como `centauro.net` y `www.centauro.net`.
  Desde mayo de 2026 se pueden tener prompts, herramientas y dominios distintos para producción,
  staging y desarrollo.
- **Sesión:** se puede fijar el tiempo de inactividad (`idleTimeoutMinutes`), la duración máxima y el mensaje
  de cierre por inactividad, que puede ser fijo, generado por la IA o ninguno. También hay recordatorios
  si el cliente deja de contestar (`reminderConfig`).
- **Horario** (`respect_business_hours`): reutiliza los ajustes de horario de la organización.
- **Paso a una persona** (`escalationConfig.mode`): `hr_platform` (bandeja de HappyRobot), `cxone` (NICE),
  `richpanel`, `email_in_thread` o `generic_webhook`. El webhook genérico avisa al empezar el paso, en
  cada mensaje del cliente y al terminar, y recibe las respuestas de la persona con un secreto.
  **RingCentral no está entre las opciones.** Hay que decidir quién atiende los chats que el bot no
  resuelve (apartado 5).
- **Archivos:** OCR de imágenes y documentos (Gemini o Reducto) y transcripción de audio (Whisper o Soniox).
  Por defecto admite 25 archivos de hasta 50 MB cada uno. Sirve, por ejemplo, para fotos de daños,
  tickets o el carné.
- **Memoria del contacto** (`enableMemory`, `interactionLimit` de 0 a 10): el bot ve las conversaciones
  anteriores del contacto. En un chat web anónimo solo funciona si sabemos quién es el cliente
  (apartado 3).
- **Modelos:** los mismos que en voz. En chat la latencia importa menos, así que puede valer la pena
  un modelo mejor que el de voz.

## 3. Saber quién es el cliente

- **Widget:** antes de cargar el script, la web rellena `window.HappyRobotConfig = { payload: {…} }` con los
  `params` que declara el disparador, como `idioma`, `pagina`, `id_reserva` o `id_cliente`. El objeto tiene
  que ser plano, sin anidar. **El navegador puede cambiar estos datos**, así que no sirven para dar
  información de una reserva sin verificarla.
- **SDK:** el backend crea el token con `client.chat.createToken({ workflow_id, data, env, ttl_seconds })`.
  Los datos de `data` los pone el servidor y el cliente no los puede cambiar. Con esto, un cliente que ya
  ha iniciado sesión en la web o en la app puede entrar al chat ya identificado, sin el paso de número
  de reserva y fecha de nacimiento que tienen los bots de voz.

## 4. La app

| Camino | Cómo | Esfuerzo | Pegas |
|---|---|---|---|
| **A. WebView con el widget** | Una página de Centauro con el widget, abierta dentro de la app | Bajo | El aspecto lo decide el widget. La página tiene que estar en un dominio registrado |
| **B. Chat nativo con el SDK** | Interfaz nativa con `HappyRobotChatClient`, más un backend de tokens | Medio o alto | Solo hay SDK en TypeScript. En React Native debería funcionar porque usa `fetch` y `WebSocket`, pero **no está comprobado**. En Swift o Kotlin habría que llamar al API REST y al WebSocket a mano |
| **C. WhatsApp** | Un botón en la app que abre WhatsApp con el número de Centauro | Bajo | No es un chat dentro de la app. Ya tenemos la credencial «Whatsapp Centauro» (`casos/reembolsos/`) |

Lo que permite el cliente de chat del SDK, `HappyRobotChatClient`, que funciona sin clave de API:

- `createSession()`, `connect()` (WebSocket con respuesta en streaming: inicio, trozos y fin), `sendMessage()`,
  `getHistory()`, `uploadFile()` y `endSession()`;
- renovación del token sin cortar la conversación (`getToken`). El token dura una hora por defecto, y entre
  60 segundos y 24 horas como mucho;
- `cluster: "us" | "eu"`. Hay que confirmar en qué cluster está Centauro.

Además, el SDK trae `HappyRobotVoiceClient`, que sirve para una **llamada de voz desde el navegador o la app**
(LiveKit, con el disparador «Web call»). Con eso, un botón de «hablar con el asistente» podría usar el bot
de voz sin pasar por la telefonía.

## 5. Qué se reutiliza de los bots de voz

- **Sí se reutiliza:** la estructura del bot único de Atención España (Triaje, módulos especialistas y
  Module Change), las herramientas (consulta de reservas, oficinas, horarios, etc.) y gran parte de las
  reglas de los prompts.
- **Hay que rehacer:**
  - **Las transferencias a colas de RingCentral no sirven en chat.** Hay que decidir el paso a una persona:
    la bandeja de HappyRobot, un webhook hacia la herramienta de chat o tickets que use Centauro, o
    «te escribimos por email o WhatsApp».
  - Las reglas pensadas para voz: deletreos, números dichos en voz alta, frases cortas o «pulsa 1».
    En chat se pueden mandar enlaces, listas y la dirección de la oficina tal cual.
  - La identificación, si el cliente llega ya identificado (apartado 3).

## 6. Preguntas abiertas antes de diseñar

1. **Dónde:** ¿solo la web, la web y la app, o primero la web? ¿La app es nativa, React Native o Flutter?
2. **Quién lo usa:** ¿clientes con sesión iniciada (se pueden identificar con `data` firmado) o cualquier
   visitante (solo información general)?
3. **Qué hace:** ¿lo mismo que el bot único (Minibús y Prolongación) o algo más, como preguntas antes de
   reservar, estado de un reembolso o cómo se recoge el coche?
4. **Paso a una persona:** ¿Centauro tiene hoy chat con agentes? ¿Con qué herramienta? Esto decide el
   `escalationConfig`.
5. **Idiomas:** ¿los mismos que en voz (ES, EN, IT, PT…)?
6. **Coste:** no hay datos de créditos por mensaje en la documentación. Hay que preguntárselo a HappyRobot
   o medirlo con una prueba (`scripts/creditos_runs.py`).

## 7. Usar el chat de Salesforce y que conteste HappyRobot

Petición del 07/11/2026: usar el chat de Salesforce en la web y en la app, con HappyRobot detrás,
sin construir el agente en Agentforce (cuesta más y es difícil trabajar con él), y pasar a un agente
cuando el bot no resuelva.

### 7.1 Qué hay en el Salesforce de Centauro (consultado el 07/11/2026, solo lectura)

- Org de producción, Unlimited Edition.
- **No hay canales de mensajería** (`MessagingChannel` está vacío) **ni bots** (`BotDefinition` está vacío).
  Hoy no se atiende ningún chat desde Salesforce.
- **Licencias de mensajería:** «Enhanced Chat User» (144), «Messaging User» (62 y 72),
  «Partner Messaging User» (62) y «Agentforce Service Agent User» (200). No se usa ninguna.
- **Permisos:** existe el conjunto de permisos «SCRT2 Integration User» (`sfdc_scrt2`), que pide
  Bring Your Own Bot, y otro llamado «HappyRobot Integration».
- **Colas:** hay 25, entre ellas `CustomerService`, `Reservations`, `Web`, `SupportW2C` y `ContactCenter`.
- **Casos de los últimos 30 días por origen:** email 17.130, formulario web 10.191 y teléfono 1.584.
- **En HappyRobot** ya está conectada la credencial de Salesforce «SalesforceC», con consultas SOQL y
  alta, lectura y edición de registros. HappyRobot no tiene canal nativo para el chat de Salesforce.

### 7.2 Opciones

| | Cómo funciona | A favor | En contra |
|---|---|---|---|
| **A. Bring Your Own Bot (BYOB)** | El chat de Salesforce (Enhanced Chat, antes Messaging for In-App and Web) es la carcasa. Una pasarela nuestra recibe cada mensaje del cliente de Salesforce (evento de plataforma por Pub/Sub API), se lo pasa a HappyRobot (API de chat) y publica la respuesta como el bot (Interaction Service API). Cuando HappyRobot decide pasar a una persona (escalado `generic_webhook`), la pasarela pide a Salesforce que enrute la conversación por Omni-Channel | Es la vía oficial de Salesforce para bots externos. El agente ve toda la conversación del bot en su consola. Sirve en la web y en la app con los SDK de Salesforce, que sí tienen iOS y Android. No consume créditos de Agentforce por cada turno (por confirmar) | Pide la licencia adicional **«Partner Messaging Bot»** sobre Agentforce Contact Center Digital. **No sabemos si Centauro la tiene ni lo que cuesta.** Hay que montar y mantener la pasarela. Parte de la documentación está detrás de un inicio de sesión |
| **B. Bot mejorado de Einstein como carcasa** | Un Enhanced Bot con un solo diálogo en bucle: cada mensaje llama, con Apex o un Flow, a HappyRobot y muestra la respuesta. Si HappyRobot dice «escalar», el bot usa *Transfer to Agent* | Usa licencias que ya existen. Puede no necesitar servidor propio, porque Apex llama al API de HappyRobot | Einstein Bots solo recibe mantenimiento. Las llamadas son síncronas y tienen límites de tiempo, y HappyRobot responde de forma asíncrona. Hay un cupo de conversaciones incluido por licencia (unas 25 al mes, sin confirmar) |
| **C. Agentforce como carcasa** | Un agente de Agentforce con una única acción que llama a HappyRobot | Es lo más integrado | Se paga Agentforce en cada turno (unos 2 $ por conversación o 0,10 $ por acción, según fuentes de terceros) **y además** HappyRobot. **Descartada** por coste |
| **D. Al revés** | El widget de HappyRobot en la web. Al escalar, una pasarela abre una sesión de Partner Messaging (BYOC) en Salesforce y el agente contesta desde su consola | No pide la licencia de bot | La carcasa no es la de Salesforce y la app no tiene SDK nativo. Queda como alternativa |

### 7.3 Pendiente de confirmar con Salesforce

- Si la licencia «Partner Messaging Bot» está incluida en lo que tiene Centauro y, si no, lo que cuesta.
- Si BYOB funciona en Enhanced Chat (web y app) o solo en otros canales de mensajería.
- Si una conversación atendida por un bot BYOB consume créditos de Agentforce.

### 7.4 Comprobado sin Salesforce (07/11/2026, consultas de solo lectura)

- **BYOB no está contratado.** La guía de BYOB pide el SKU *Agentforce Contact Center Digital*
  y la licencia adicional *Partner Messaging Bot*. Ninguna aparece entre las 191 licencias de
  conjunto de permisos ni entre las licencias de usuario. Sí aparece *Partner Messaging User*
  (62), que es Partner Messaging / BYOC, otro producto. Precio de *Partner Messaging Bot*: no
  es público.
- **BYOB solo sirve para hablar bot con cliente.** El paso solo va de bot externo a agentes con
  licencia dentro de Salesforce. Tampoco hay ningún `ExtConvParticipantIntegDef` creado.
- **Opción B (Einstein Bot como carcasa).** No hay ningún bot creado (`BotDefinition` vacío).
  Cupos del contrato: 1.800 sesiones de chatbot al mes («Maximum Chatbot Sessions Allowed»,
  igual en Engaged y API) y 1.550 conversaciones de mensajería con agente al mes («Maximum
  Billed Agent Conversations for Messaging»). Frente a unos 10.000 casos al mes del formulario
  web, 1.800 sesiones se quedan cortas si el chat se pone en toda la web.
- **Licencias de agentes:** 144 de Enhanced Chat User y 62 de Messaging User, todas sin usar.
  Licencias de Salesforce: 66 usadas de 72.
- **Catálogo de compra de «Su cuenta» (contrato 05438756):** no ofrece *Partner Messaging Bot*,
  *Agentforce Contact Center Digital* ni nada de mensajería o chat. BYOB solo se puede contratar
  a través del comercial de Salesforce. Sí se pueden comprar Flex Credits (100.000 por 500 €) y
  sandboxes. Sales Cloud Agentforce 1 sale a 190,80 € frente a 550 € de tarifa (un 65 % menos).

### 7.5 De qué tratan los casos del formulario web (30 días hasta el 07/11/2026)

Consulta de solo lectura: `Origin = 'Web'`, agrupado por `Type` y `Subtype__c`. Total: unos 10.200.

| Tipo | Casos | Subtipos principales |
|---|---|---|
| Alquiler terminado | 5.069 | Reembolso de combustible 1.376 · Reembolso de preautorización 1.333 · Otros 786 · Facturas 759 · Pagos hechos 528 · Multas 205 · Objetos perdidos 82 |
| Reserva ya hecha | 1.906 | Otros 556 · Cancelación directa 372 · Modificación directa 280 · Dudas de recogida 244 · Información del vuelo 153 · Documentación 101 · Modificación por intermediario 83 |
| Alquiler en curso | 1.675 | Otros 778 · Dudas de devolución 285 · Daños, km o combustible previos 280 · Prolongación 203 · Asistencia en carretera 72 · Añadir extras 57 |
| Reserva nueva | 1.153 | Condiciones 360 · Otros 338 · Hacer una reserva 227 · Pago 119 · Documentación 84 |
| Cuenta de cliente | 263 | Cambiar datos 115 · Problemas de acceso 114 · Gold Club 34 |
| Resto | unos 140 | Extras, combustible, franquicia, multas, coche… |

- **Idiomas:** inglés 3.921, español 2.997, italiano 834, alemán 715, francés 675, portugués
  493, neerlandés 279 y otros 289.
- **Estado:** unos 6.300 están «Closed automatically». No he comprobado qué significa ese estado.
  En «Alquiler terminado» hay 1.593 reabiertos.

### 7.6 Créditos de Agentforce ya pagados (Cartera digital, 07/11/2026)

- **Flex Credits prepagados:** 3.083.333, del 01/01/2026 al 31/01/2029 (unos 1.000.000 al año).
  Gastados 24.132 (1 %); quedan 3.059.201. Van incluidos en Agentforce 1 Edition, sin línea de
  precio aparte.
- **Cuenta aproximada.** Supuestos: 20 créditos por acción (precio público, sin confirmar en el
  contrato) y unas 5 acciones por conversación (supuesto mío). Lo que queda daría para unas
  153.000 acciones, es decir, unas 30.000 conversaciones de chat. Eso son unos 3 meses con
  todo el volumen del formulario web (unos 10.200 al mes), o 17 meses con 1.800 al mes.
  Agotada la bolsa, a 0,005 € por crédito, saldría por unos 0,50 € por conversación: unos
  5.100 € al mes con todo el volumen del formulario web.
- **Precio de compra en «Su cuenta»:** 100.000 Flex Credits por 500 €, es decir, 0,005 € por
  crédito. A ese precio, la bolsa entera vale unos 15.400 €, y lo que queda, unos 15.300 €.
- **Qué gastó los 24.132 créditos (últimos 90 días):**
  - Producción: *Basic Prompts*, 11.759 × 2 = 23.518; *Standard Prompts*, 99 × 4 = 396.
  - Sandbox: 218.
  - Son plantillas de prompt, no agentes. Se concentran en unos 5 días con 4.000–4.700 créditos
    diarios y después bajan casi a cero.
  - Por tanto, la tarifa por acción de agente (los 20 créditos) sigue sin confirmar en el contrato.
- **Consecuencia:** Agentforce no supone coste nuevo hasta que se gaste la bolsa, pero la bolsa
  vale unos 15.000 € y con todo el volumen se acabaría en unos 3 meses. Para compararlo con
  HappyRobot falta el coste por conversación de chat en HappyRobot.

**Fuentes:**
- [BYOB: Get Started](https://developer.salesforce.com/docs/service/messaging-byob/guide/get-started.html)
- [BYOB Setup Entities](https://developer.salesforce.com/docs/service/messaging-byob/references)
- [Enable Third Party Bots (BYOC CCaaS)](https://developer.salesforce.com/docs/service/messaging-byoc-ccaas/guide/third-party-bots.html)
- [byo-demo-connector](https://github.com/salesforce-misc/byo-demo-connector)
- [Set Up Enhanced Bots](https://help.salesforce.com/s/articleView?id=sf.bots_service_enhanced.htm&language=en_US)
- [Precios de Agentforce (tercero)](https://www.jitendrazaa.com/blog/salesforce/salesforce-agentforce-credits-cost-model-complete-guide-2026/)
