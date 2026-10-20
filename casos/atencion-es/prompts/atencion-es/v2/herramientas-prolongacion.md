<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v2 (x8xd0llbdp3j) · nodo: herramientas (tool) de Prolongación · copiado: 2026-10-18 (Tarea 10) -->

# Herramientas de «Prolongación» (v2)

Las herramientas del prompt «Prolongación» (`01a14f69-b09d-7689-ad9e-8e8de0fd6fb4`, hijo de `prolongar_alquiler` del
Triaje). Un nodo `tool` solo define la función que ve el agente; lo que pasa al ejecutarla lo hacen sus hijos. Todas se
crearon por API en la Tarea 10 (persistent_id = ID de nodo en la v2).

- Fuente de las descripciones (R3): `{{gestion_abierta}}` se escribe al subir como
  `{{e51cd732-f403-4ef7-95d4-490347960a93.gestion_abierta}}`, como nodo de variable de Plate.
- `informacion_oficina` (Module Change → Información de oficina) y `volver_al_triaje` (Module Change → Triaje) (spec
  §5.7): creadas en la Tarea 12; definición, ids y destinos en `saltos.md`.
- Música de espera «holdacent»: asset `01a0fc02-a13d-77a2-8de3-82459eb2a2a6`; la URL firmada del nodo se sustituye
  aquí por `<URL_FIRMADA>`.

## 1. enviar_correo_contrasena

> Ronda de arreglos 1 de la revisión de la Tarea 16 (20/10/2026): en `nombre_completo` y `fecha_nacimiento` se añade
> «Si ya los dio (la dio) para pista_correo, úsalos (úsala); no los pidas (la pidas).» (PISTA-04).

- Cadena de 4 nodos igual que en Prolongaciones v12 (detalle y código: `enviar-correo-contrasena.md`).
- `message` tipo `ai`: «Un momento, lo compruebo.» (descripción de la v12, sin cambios).
- **Descripción y parámetros:** los de la v12, tal cual (`casos/prolongaciones/prompts/prolongacion-es/v12/enviar-correo-contrasena.md`).
  Parámetros obligatorios `email` (ejemplo `prueba.prueba@example.com`), `nombre_completo` (`Prueba Prueba`) y
  `fecha_nacimiento` (`01/01/1990`).

## 2. pista_correo (nueva)

> Tarea 16 (20/10/2026, ronda de arreglos): la última frase de la descripción pide enviar con el nombre y la fecha ya dados (PISTA-04, 0/3 en la pasada).

- Hijos: MCP Call «Identificar al cliente (consultar_reserva)» → Python «Pista del correo» (`pista-correo.md`).
- `message` tipo `ai`: el de `enviar_correo_contrasena` («Un momento, lo compruebo.»).

**Descripción:** Comprueba con el número de reserva, el nombre completo y la fecha de nacimiento del titular si la reserva es suya y, si lo es, devuelve SOLO el dominio del correo de su alquiler (por ejemplo gmail.com), para que el cliente recuerde con qué correo está y te lo dicte. Úsala solo cuando el cliente no sabe con qué correo está su alquiler y te ha dicho los tres datos. MÁXIMO DOS LLAMADAS POR CONVERSACIÓN. Devuelve resultado: verificado (con el dominio, si consta), no_verificado (no digas qué dato falla), dato_no_interpretado (pide el dato que indica detalle) o no_disponible (plan B). Nunca devuelve el correo completo ni otro dato de la reserva; tú no digas nada más que el dominio. Después, en cuanto el cliente te confirme el correo, ejecuta enviar_correo_contrasena con ese correo y con el nombre completo y la fecha de nacimiento que ya te dio para esta herramienta: no se los vuelvas a pedir.

**Parámetros (los tres obligatorios):**
- `numero_reserva` (ejemplo `ER00000000`): Número de reserva tal como lo dicta el cliente, con letras y cifras, en mayúsculas y sin espacios ni guiones: 'e erre, uno dos tres...' -> 'ER123...'. Si lo corrigió, usa su versión. Nunca lo inventes ni lo completes: si no te lo ha dicho entero, pídeselo antes.
- `nombre_completo` (ejemplo `Prueba Prueba`): la descripción de `enviar_correo_contrasena`.
- `fecha_nacimiento` (ejemplo `03/03/1990`): la descripción de `enviar_correo_contrasena`.

## 3. buscar_respuesta

- Hijo: Python «Buscar respuesta» con `casos/atencion-es/codigo/consultas_alquiler.py` tal cual (el mismo código que el
  de Consultas; `buscar-respuesta.md`). Entradas `tema` y `pregunta` de esta herramienta.
- `message`: `{"type": "none"}`. Parámetros `tema` y `pregunta`: los de Consultas, sin cambios (`herramientas-consultas.md`, §1).

**Descripción** (la de Consultas con la última frase adaptada al módulo): Devuelve el texto de las condiciones de Centauro sobre un tema, para responder una duda del alquiler. Úsala ante cada duda nueva, sin decir nada antes, y responde solo con lo que devuelva, en una o dos frases; si lo que pregunta no está, no lo inventes. Si ya tienes en la conversación la sección de ese tema, no la vuelvas a pedir. Si devuelve encontrado: false porque el tema no era de la lista, vuelve a llamarla con un tema válido antes de decir que no tienes el dato. Sirve a cualquier hora, también en modo virtual y con gestión cerrada. NO la uses para lo que ya tienen tus instrucciones (EXPLICACIÓN, DEVOLVER TARDE, COCHE DE ASEGURADORA O DE EMPRESA, DETALLES QUE PUEDES DAR, LA WEB NO LE DEJA), salvo un detalle que no esté en ellas; ni para el horario o la dirección de una oficina (informacion_oficina) ni para el minibús (volver_al_triaje).

## 4. transfer_to_human_agent

- Hijo: Python «Preparar transferencia» → Paths «¿Transferir?» → «Transferir» → Transfer «Initiate customer
  connection» (mismo patrón y misma configuración que Consultas: `preparar-transferencia.md` y `transfer.md`).
  `outside_agent_transfer: false` desde la creación.
- `execution`: no se guarda por API (queda el de por defecto).
- `hold_music`: estático, «holdacent», URL `<URL_FIRMADA>`.
- **message** (tipo `ai`; cambiado en la Tarea 15b, R34, D-013, y en la Tarea 16, R45, D-014: el aviso depende de la cola): ejemplo el de siempre («…Le paso ahora mismo con un compañero… no cuelgue, por favor.»). Descripción (`{{gestion_abierta}}` y `{{modo_virtual}}` son nodos de variable de Plate con `group_id` `e51cd732-…`): Gestión ahora: {{gestion_abierta}}. Modo virtual: {{modo_virtual}}. El aviso depende de la cola que pones. Solo si la transferencia puede no salir (cola gestion con Gestión ahora false, o una cola que no sea asistencia con Modo virtual true) no digas que le pasas con nadie: di solo, en su idioma, «Un momento, por favor, no cuelgue.» (si está molesto, valida antes su molestia en una frase corta). En los demás casos, y siempre con la cola asistencia: informa al cliente, en su idioma, de que le vas a pasar con un compañero que le va a ayudar. Sé breve y tranquilizador. Termina SIEMPRE avisando de que puede tardar unos segundos en atenderle y pidiéndole que no cuelgue (por ejemplo: "puede tardar unos segundos, no cuelgue, por favor"). Si el cliente está molesto, frustrado o ya ha tenido que insistir para que le pases con alguien, valida primero su emoción en una frase corta y sincera antes de anunciar la transferencia: reconoce la molestia concreta que te ha expresado, sin excusas largas ni justificaciones. Nunca anuncies la transferencia en seco a un cliente enfadado. No menciones colas, extensiones ni números. No prometas una oficina concreta ni un equipo específico.

**Descripción** (desde la ronda de arreglos 3, 19/10/2026, empieza con la variable): Gestión ahora: {{gestion_abierta}}. Si Gestión ahora es false y el caso es de gestión, no la llames: di que gestión está cerrada y su horario. Transfiere la llamada a una cola de compañeros. Úsala en los casos de ESCALADO, cuando tus secciones mandan transferir (por ejemplo, no_coincide del correo de contraseña) o si no puedes seguir al cliente por el idioma. Si el cliente ya ha pedido que lo mire alguien, o la sección manda transferir en ese turno, ejecútala en ese turno; si solo ofreces pasarle, espera a que acepte. En modo virtual, solo para una avería o un accidente (cola asistencia). Con gestión cerrada, nunca con la cola gestion. Prolongar, devolver tarde, la web que no deja, la contraseña y el coche de aseguradora o de empresa no se transfieren por sí solos: tienes instrucciones para ellos. Ejecútala en el mismo turno en que decides transferir, sin decir antes «le paso». Si devuelve gestion_cerrada, no la repitas: sigue COLA DE GESTIÓN CERRADA.

**Parámetros (los tres obligatorios):**
- `cola` (`{{gestion_abierta}}` como nodo de variable de Plate): Cola de destino. Valores permitidos EXACTOS: "asistencia" (avería o accidente, o acepta que le pases por un aviso del coche o por la grúa; funciona siempre), "nueva_reserva" (quiere hacer una reserva nueva o acepta que un compañero se la prepare), "minibus" (idioma que no puedes seguir), "gestion" (lo que tus secciones mandan a GESTIÓN DE RESERVA, el correo que no coincide, un dato concreto de su reserva, o una persona sin motivo; solo con gestión abierta). Gestión ahora: {{gestion_abierta}}. Si es false, nunca uses "gestion".
- `motivo_transferencia`: Por qué transfieres. Valores permitidos EXACTOS: "no_iniciada", "web_no_disponible", "pregunta_reserva_concreta", "aseguradora", "enfado", "error_tecnico", "minibus", "asistencia", "nueva_reserva", "correo_no_coincide", "otro". En Prolongación: el que diga la sección; correo_no_coincide si enviar_correo_contrasena devuelve no_coincide; error_tecnico si la web o el correo siguen fallando; aseguradora si llama la aseguradora, una mutua o el gestor de una empresa; pregunta_reserva_concreta para un dato concreto de su reserva; si no, "asistencia", "nueva_reserva", "minibus", "enfado" (cliente muy enfadado que exige una persona) u "otro".
- `resumen_para_agente`: la descripción de Consultas, con los ejemplos cambiados a casos de Prolongación ('Cliente quiere prolongar; el correo que dio para la contraseña no coincide con el de su alquiler.', 'Cliente con pinchazo en carretera, necesita asistencia.', 'Cliente no puede pagar la prolongación en la web tras probar otro dispositivo y otra tarjeta.').

## Configuración

| Nodo | ID de nodo en la v2 (= persistent_id) |
|---|---|
| enviar_correo_contrasena | `01a150c7-08df-73fd-abac-19c873b9533d` |
| → MCP Call «Comprobar correo (consultar_reserva)» | `01a150c7-08ea-725d-a22c-f6dd3d5161d4` |
| → Python «Decidir envío» | `01a150c7-08fd-7f91-9dc8-5b5d5290896e` |
| → MCP Call «Enviar correo (enviar_reset_contrasena)» | `01a150c7-090c-7f7b-b5f7-38aa1b1614d9` |
| → Python «Resultado para el agente» | `01a150c7-091b-7abf-a101-539b1b7ec049` |
| pista_correo | `01a150c7-0928-79dc-a21c-4d9348ca038d` |
| → MCP Call «Identificar al cliente (consultar_reserva)» | `01a150c7-0930-723c-89d9-eaeb76a0599e` |
| → Python «Pista del correo» | `01a150c7-0940-76a7-8129-f132e4373895` |
| buscar_respuesta | `01a150c9-677e-791b-8f74-957f60586f02` |
| → Python «Buscar respuesta» | `01a150c9-6786-7e05-95c4-8007aa1e06d4` |
| transfer_to_human_agent | `01a150ca-b67d-726a-845b-19c18b2e891e` |
| → Python «Preparar transferencia» | `01a150ca-b684-7698-a2ff-ccdefe784483` |
| → Paths «¿Transferir?» | `01a150ca-dc54-7efe-8af0-9eab480b758a` |
| → condition «Transferir» → Transfer «Initiate customer connection» | `01a150ca-dc5d-7979-b66d-fa2f4033c5b6` → `01a150ca-dc8b-73ca-84c2-08eca941b971` |

Entradas de «Preparar transferencia»: `cola` = `{{01a150ca-b67d-726a-845b-19c18b2e891e.cola}}` y las cuatro `cola_*` de
«Resolver colas» (`081e2b5d-…`). Transfer: `number` = `fallback_number` = `{{01a150ca-b684-….numero}}`; whisper
«Llamada del asistente de atención.» + `resumen_para_agente` de esta herramienta + `telefono_dictado`.
