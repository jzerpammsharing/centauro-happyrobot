<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v3 (5cu7jiosi6n7) · nodo: herramientas (tool) de Prolongación · copiado: 2026-10-18 (Tarea 10) · actualizado: 2026-10-22 (D-018) -->

# Herramientas de «Prolongación» (v3)

Las herramientas del prompt «Prolongación» (`01a14f69-b09d-7689-ad9e-8e8de0fd6fb4`, hijo de `prolongar_alquiler` del
Triaje). Un nodo `tool` solo define la función que ve el agente; lo que pasa al ejecutarla lo hacen sus hijos. Todas se
crearon por API en la Tarea 10 (persistent_id = ID de nodo en la v2).

- Fuente de las descripciones (R3): `{{gestion_abierta}}` se escribe al subir como
  `{{e51cd732-f403-4ef7-95d4-490347960a93.gestion_abierta}}`, como nodo de variable de Plate.
- `informacion_oficina` (Module Change → Información de oficina) y `volver_al_triaje` (Module Change → Triaje) (spec
  §5.7): creadas en la Tarea 12; definición, ids y destinos en `saltos.md`.
- Música de espera «holdacent»: asset `01a0fc02-a13d-77a2-8de3-82459eb2a2a6`; la URL firmada del nodo se sustituye
  aquí por `<URL_FIRMADA>`.

## 1 y 2. enviar_correo_contrasena y pista_correo: quitadas en la v3

Borradas el 22/10/2026 (D-018) con sus cadenas: «Comprobar correo (consultar_reserva)», «Decidir envío», «Enviar correo
(enviar_reset_contrasena)» y «Resultado para el agente»; «Identificar al cliente (consultar_reserva)» y «Pista del
correo». Su definición, tal como estaba, sigue en `../v2/herramientas-prolongacion.md`. En la v3 el módulo tiene cuatro
herramientas: `buscar_respuesta`, `transfer_to_human_agent`, `volver_al_triaje` e `informacion_oficina`.

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

**Descripción** (desde la ronda de arreglos 3, 19/10/2026, empieza con la variable): Gestión ahora: {{gestion_abierta}}. Si Gestión ahora es false y el caso es de gestión, no la llames: di que gestión está cerrada y su horario. Transfiere la llamada a una cola de compañeros. Úsala en los casos de ESCALADO, cuando tus secciones mandan transferir (por ejemplo, un dato concreto de su reserva) o si no puedes seguir al cliente por el idioma. Si el cliente ya ha pedido que lo mire alguien, o la sección manda transferir en ese turno, ejecútala en ese turno; si solo ofreces pasarle, espera a que acepte. En modo virtual, solo para una avería o un accidente (cola asistencia). Con gestión cerrada, nunca con la cola gestion. Prolongar, devolver tarde, la web que no deja, la contraseña y el coche de aseguradora o de empresa no se transfieren por sí solos: tienes instrucciones para ellos. Ejecútala en el mismo turno en que decides transferir, sin decir antes «le paso». Si devuelve gestion_cerrada, no la repitas: sigue COLA DE GESTIÓN CERRADA.

**Parámetros (los tres obligatorios):**
- `cola` (`{{gestion_abierta}}` como nodo de variable de Plate): Cola de destino. Valores permitidos EXACTOS: "asistencia" (avería o accidente, o acepta que le pases por un aviso del coche o por la grúa; funciona siempre), "nueva_reserva" (quiere hacer una reserva nueva o acepta que un compañero se la prepare), "minibus" (idioma que no puedes seguir), "gestion" (lo que tus secciones mandan a GESTIÓN DE RESERVA, un dato concreto de su reserva, o una persona sin motivo; solo con gestión abierta). Gestión ahora: {{gestion_abierta}}. Si es false, nunca uses "gestion".
- `motivo_transferencia`: Por qué transfieres. Valores permitidos EXACTOS: "no_iniciada", "web_no_disponible", "pregunta_reserva_concreta", "aseguradora", "enfado", "error_tecnico", "minibus", "asistencia", "nueva_reserva", "otro". En Prolongación: el que diga la sección; error_tecnico si la web o el correo de la contraseña siguen fallando; aseguradora si llama la aseguradora, una mutua o el gestor de una empresa; pregunta_reserva_concreta para un dato concreto de su reserva; si no, "asistencia", "nueva_reserva", "minibus", "enfado" (cliente muy enfadado que exige una persona) u "otro".
- `resumen_para_agente`: la descripción de Consultas, con los ejemplos cambiados a casos de Prolongación ('Cliente quiere prolongar; no le llega el correo para crear la contraseña tras pedirlo dos veces en la web.', 'Cliente con pinchazo en carretera, necesita asistencia.', 'Cliente no puede pagar la prolongación en la web tras probar otro dispositivo y otra tarjeta.').

## Configuración

> v3 (22/10/2026, D-018): descripción y parámetros de `transfer_to_human_agent` sin el correo de contraseña (ejemplo de
> la descripción, «el correo que no coincide» de `cola`, el valor `correo_no_coincide` de `motivo_transferencia` y el
> ejemplo de `resumen_para_agente`). El resto de la función, igual. Las otras herramientas, sin cambios.

| Nodo | ID de nodo en la v3 | persistent_id |
|---|---|---|
| buscar_respuesta | `01a16336-ef18-7f46-a547-c3d4992955d6` | `01a150c9-677e-791b-8f74-957f60586f02` |
| transfer_to_human_agent | `01a16336-ef19-7b73-9636-ff4b0c8071d4` | `01a150ca-b67d-726a-845b-19c18b2e891e` |
| volver_al_triaje | `01a16336-ef0e-78a1-a32e-a71b08496666` | `01a155d9-5da8-738a-8af4-ada5f82ebdd7` |
| informacion_oficina | `01a16336-ef11-7fad-a91f-a080ce05f420` | `01a155d9-5dbb-704a-b119-2db7b00a6fa2` |
