# Workflows del caso Reembolsos

Los tres están en la carpeta de Centauro (`019d8144-ce27-7aaf-b9e5-21d006083063`). Comprobado con
`get_workflows` el 12/10/2026: la versión que aparece como actual de cada workflow es la que indica
la columna «Estado».

## Centauro Reembolsos (`01a0defb-9c46-7f81-b966-69ca9d211709`, slug `ey9623r10ly2`)

Voicebot de reembolsos y fianzas. Es la **V4**, en producción y sin cambios. Copia del prompt:
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
| 4 | `m87e6xzgo405` | Version 4 | Versión en producción | **Actual (producción)** |

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

Copias de los prompts: `prompts/reembolsos-whatsapp/v1/` (nodos) y `v2/` (prompt y extract).

### Versiones
| Versión | Slug | Nombre en HappyRobot | Descripción | Estado |
|---|---|---|---|---|
| v1 | `1g52kgh7y4pn` | v1 · V4 + datos por WhatsApp | Copia de la V4 + Signals + `enviar_whatsapp` | Publicada por una persona para las pruebas de la señal; superada por la v2 |
| v2 | `pc4zvke3xdjl` | v2 · v1 + oferta de WhatsApp y lectura de señales | Prompt con reglas de WhatsApp, evals 10/10, extract de WhatsApp | **Actual** (publicada por una persona para pruebas, no conectada a ningún número de clientes) |

## Centauro Reembolsos · Datos por WhatsApp (`01a12d4c-5fe2-76d7-a233-3d5a16972ffd`, slug `p45rx5hlsber`) · W2

Texto. Lo llama W1 por webhook, escribe al cliente por WhatsApp, recoge los datos y los publica
como señal en la sesión de la llamada.

### Flujo (v4)
1. Petición desde la llamada (trigger «Incoming hook» con API key): `telefono`, `session_key`,
   `idioma`, `entorno`.
2. Agente de WhatsApp (Outbound Text Agent): credencial «Whatsapp Centauro», número de empresa
   +44 20 4621 5219, plantilla inicial mock `info_minibus`, inactividad de 15 minutos. Herramienta
   `pasar_a_llamada`.
3. Señal a la llamada (API): Webhook POST a `https://platform.eu.happyrobot.ai/api/v2/signals` con
   `Authorization: Bearer` y la variable oculta `HR_SIGNALS_API_KEY`. Comprueba `status == "published"`.

Copias: `prompts/reembolsos-whatsapp-datos/` (v1, v3 y v4).

### Versiones
| Versión | Slug | Nombre en HappyRobot | Descripción | Estado |
|---|---|---|---|---|
| v1 | `2afxs944xpxt` | Version 1 | Modo prueba: Send Signal con payload fijo | Publicada por una persona para pruebas; superada |
| v2 | `xc8n9t2rbods` | v2 · v1 + payload en message | Payload también en `message` | Superada: la señal seguía llegando con el payload vacío |
| v3 | `j0utp12shz0v` | v3 · señal por API de signals | Webhook POST en lugar de Send Signal | Superada por la v4 |
| v4 | `qw83lg2g3sa6` | v4 · agente de WhatsApp (plantilla mock info_minibus) | Agente de texto de WhatsApp con la plantilla mock y `pasar_a_llamada` | **Actual** (publicada por una persona para pruebas) |

Las versiones de W1 y W2 publicadas lo fueron para probar; no hay nada conectado a clientes. Antes
de publicar a clientes, ver los pendientes de WhatsApp en `docs/pendientes.md`.

## Antes de publicar a clientes

Checklist para W1 y W2. Esta rama debe revisarse antes de publicar (CLAUDE.md raíz, apartado 3).

- [ ] **Plantilla mock.** W2 v4 usa `info_minibus`. W1 no debe conectarse a números de clientes hasta
  que `datos_llamada_*` estén aprobadas y se elija la plantilla por idioma.
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

