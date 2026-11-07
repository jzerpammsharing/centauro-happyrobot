<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v2 (x8xd0llbdp3j) · nodo: herramientas (tool) de Información de oficina · copiado: 2026-10-19 (Tarea 11) · cadena de transferencia: 2026-10-20 (Tarea R35) -->

# Herramientas de «Información de oficina» (v2)

Las herramientas del prompt «Información de oficina» (`0c60218b-8901-47bd-95de-40e0e1af1296`, ID de nodo en la v2
`01a14f1d-0396-717d-8b6f-52f789dbe9a3`).

- Fuente de las descripciones (R3): `{{gestion_abierta}}` va en HappyRobot como nodo de variable de Plate con
  `group_id` `e51cd732-f403-4ef7-95d4-490347960a93`.
- `buscar_punto_de_encuentro` y `volver_al_triaje` (spec §5.7): creadas en la Tarea 12, cada una con su Module Change;
  definición, ids y destinos en `saltos.md`.

## 1. consultas_alquiler (descripción cambiada en la ronda de arreglos 2)

- Hijo: «Module Change» → «Consultas del alquiler» (viene del duplicado; no se toca, R5).
- `message`: `{"type": "none"}`. Parámetros (`tema`, `pregunta`) los de la v25. Descripción: la de la v25 con dos
  cambios (ronda de arreglos 2 de la Tarea 11): «Alargar el alquiler (devolverlo otro día) siempre va aquí, también
  con gestión cerrada.» y «…que alguien mire o cambie un dato concreto de su reserva sin alargarla». En la Tarea 12
  (ronda de arreglos 2, 19/10/2026, D-009) la primera pasa a «Alargar el alquiler o cambiar la hora o el día de
  devolución (prolongar si es más tarde, devolucion si es antes) siempre va aquí, también con gestión cerrada.»

## 2. transfer_to_human_agent

- Hijo: Python «Preparar transferencia» → Paths «¿Transferir?» → «Transferir» → Transfer «Initiate customer
  connection», con «Fallback» vacía (mismo patrón y configuración que Consultas y Prolongación:
  `preparar-transferencia.md` y `transfer.md`). Creada por API en la Tarea R35 (20/10/2026), después de que el
  responsable borrara en el editor el Transfer heredado de la v25. Ids en «Configuración».
  - «Preparar transferencia»: código de `codigo/preparar_transferencia.py`; entradas `cola` =
    `{{62c5b6dd-5dde-4b3a-9a93-adb638c0bd66.cola}}` y las cuatro `cola_*` de «Resolver colas» (`081e2b5d-…`).
  - «Transferir»: `transferir` de «Preparar transferencia» es true (`boolean_true`).
  - Transfer: `number` = `fallback_number` = `{{01a15973-c373-7e08-9265-75a323398201.numero}}`; whisper «Llamada del asistente de
    atención.» + `resumen_para_agente` de esta herramienta + «Teléfono del cliente:» `telefono_dictado`;
    `outside_agent_transfer: false`; el resto como el de Consultas (`skip_digit_press` false,
    `record_transfer_conversation` true, `transfer_timeout` 300). Salida fijada con `set_custom_output`
    (`transfer_succeeded`, `error`…) para que el extract vea la variable.
- `execution`: no se guarda por API (queda el de por defecto).
- `hold_music`: estático, «holdacent» (asset `01a0fc02-a13d-77a2-8de3-82459eb2a2a6`, también en `hold_music_asset_id`
  desde la Tarea R35), URL `<URL_FIRMADA>`.
- **message** (tipo `ai`; alineado con Consultas y Prolongación en la Tarea R35, 20/10/2026: el aviso depende de la cola, D-014): ejemplo «Lo entiendo. Le paso ahora mismo con un compañero que le va a ayudar. Puede tardar unos segundos, no cuelgue, por favor.» Descripción (`{{gestion_abierta}}` y `{{modo_virtual}}` son nodos de variable de Plate con `group_id` `e51cd732-…`): Gestión ahora: {{gestion_abierta}}. Modo virtual: {{modo_virtual}}. El aviso depende de la cola que pones. Solo si la transferencia puede no salir (cola gestion con Gestión ahora false, o una cola que no sea asistencia con Modo virtual true) no digas que le pasas con nadie: di solo, en su idioma, «Un momento, por favor, no cuelgue.» (si está molesto, valida antes su molestia en una frase corta). En los demás casos, y siempre con la cola asistencia: informa al cliente, en su idioma, de que le vas a pasar con un compañero que le va a ayudar. Sé breve y tranquilizador. Termina SIEMPRE avisando de que puede tardar unos segundos en atenderle y pidiéndole que no cuelgue (por ejemplo: "puede tardar unos segundos, no cuelgue, por favor"). Si el cliente está molesto, frustrado o ya ha tenido que insistir para que le pases con alguien, valida primero su emoción en una frase corta y sincera antes de anunciar la transferencia: reconoce la molestia concreta que te ha expresado, sin excusas largas ni justificaciones. Nunca anuncies la transferencia en seco a un cliente enfadado. No menciones colas, extensiones ni números. No prometas llamar al conductor ni a una oficina concreta. (Igual que la de Consultas salvo la última frase, que es la de la v25 de este módulo.)

**Descripción** (19/10/2026, Tarea 11 y ronda de arreglos 3; empieza con la variable, como en Prolongación, R34): Gestión ahora: {{gestion_abierta}}. Si Gestión ahora es false y el caso es de gestión, no la llames: di que gestión está cerrada y su horario. Transfiere la llamada a una cola de compañeros. Úsala en los casos de ESCALADO: algo de su reserva que hay que mirar o cambiar (un dato ya acordado que no sea alargar el alquiler, un cargo concreto, el código de un parking, Smartkey), avería o accidente, reserva nueva, oficina sin datos que el cliente no resuelve, una persona sin motivo o un idioma que no puedes seguir. Alargar el alquiler no es de gestión: consultas_alquiler. En modo virtual, solo para una avería o un accidente (cola asistencia). Con gestión cerrada, nunca con la cola gestion. El horario, cómo llegar y dónde devolver los das tú; el minibús y las dudas del alquiler tienen su herramienta. Ejecútala en el mismo turno en que decides transferir, sin decir antes «le paso». Si devuelve gestion_cerrada, no la repitas: sigue COLA DE GESTIÓN CERRADA.

**Parámetros (los tres obligatorios; sustituyen al parámetro de la extensión de la v25):**
- `cola`: Cola de destino. Valores permitidos EXACTOS: "gestion" (algo de su reserva: cambiar un dato ya acordado que no sea alargar el alquiler, devolver con la oficina cerrada sin haberlo acordado, el servicio de espera, un cargo concreto, el código de un parking, problemas con Smartkey; solo con gestión abierta), "asistencia" (avería o accidente; funciona siempre), "nueva_reserva" (aún no tiene reserva y quiere alquilar), "minibus" (oficina que no identificas o sin datos y el cliente no lo resuelve, festivos, una persona sin motivo, cliente muy enfadado o idioma que no puedes seguir). Alargar el alquiler no es de gestión: consultas_alquiler. Gestión ahora: {{gestion_abierta}}. Si es false, nunca uses "gestion". Si dudas entre dos, "minibus".
- `motivo_transferencia`: Por qué transfieres. Valores permitidos EXACTOS: "no_iniciada", "web_no_disponible", "pregunta_reserva_concreta", "aseguradora", "enfado", "error_tecnico", "minibus", "asistencia", "nueva_reserva", "correo_no_coincide", "otro". En Información de oficina: "pregunta_reserva_concreta" para algo de su reserva; "asistencia"; "nueva_reserva"; "enfado" (cliente muy enfadado que exige una persona) u "otro" (oficina sin datos, festivos, una persona sin motivo, idioma que no puedes seguir).
- `resumen_para_agente`: Resumen del motivo de la llamada que se le leerá en voz alta al compañero que recibe la transferencia, antes de conectarle con el cliente. SIEMPRE en español, aunque el cliente hable otro idioma. Una o dos frases, de 10 a 25 palabras, en tercera persona, que digan qué quiere el cliente, de qué oficina habla y qué se ha intentado ya. Sin datos personales (nombre, reserva, matrícula, correo, teléfono), sin códigos, extensiones ni importes. Si el idioma de la llamada no es español, la ÚLTIMA frase es SIEMPRE «El cliente habla <idioma>» (por ejemplo, «El cliente habla inglés»). Ejemplos: 'Cliente llega a Valencia aeropuerto después del cierre y quiere comprobar el servicio de espera.' 'Cliente pregunta por un cargo de parking en su alquiler de Madrid Atocha.'

## Configuración

| Nodo | ID de nodo en la v2 | persistent_id |
|---|---|---|
| consultas_alquiler → Module Change | `01a14f1d-0398-71cd-be10-a50ab91d1f5d` → `01a14f1d-039b-7e2a-90f5-a43135ba4453` | `6edd13ac-b226-4d1c-87dc-748b46ce5638` |
| transfer_to_human_agent | `01a14f1d-0399-7faf-a630-5c199b3e3efc` | `62c5b6dd-5dde-4b3a-9a93-adb638c0bd66` |
| → Python «Preparar transferencia» (Tarea R35) | `01a15973-c373-7e08-9265-75a323398201` | = ID de nodo |
| → Paths «¿Transferir?» | `01a15974-0f1c-7db1-8128-1182eab1eb18` | = ID de nodo |
| → condition «Transferir» → Transfer «Initiate customer connection» | `01a15974-0f2b-7f09-9657-cc6934a0a05c` → `01a15974-0f32-7195-bc20-40ffed8c52da` | = ID de nodo |
| → condition «Fallback» (sin hijos) | `01a15974-0f1c-7db1-8128-118349d27177` | = ID de nodo |

El Transfer heredado de la v25 (`01a14f1d-0396-788f-81ca-75cf199aabbd`, persistent_id `faec6a20-257a-4b8c-8c75-8dd336beead7`) lo borró el responsable en el
editor el 20/10/2026 (R35); la cadena nueva se creó por API ese mismo día.

**Ronda de arreglos 3 (19/10/2026).** En `transfer_to_human_agent`: el caso de gestión es «cambiar un dato ya acordado que
no sea alargar el alquiler» (antes «la hora o el día de devolución», que hacía que el bot tratara alargar como caso de
gestión: causa de ADV-11), en la descripción y en `cola`, con «Alargar el alquiler no es de gestión: consultas_alquiler»;
y en `resumen_para_agente`, «Si el idioma de la llamada no es español, la ÚLTIMA frase es SIEMPRE «El cliente habla
<idioma>»».

**Ronda de arreglos 4 (19/10/2026).** El cuerpo de esta sección se copió de lo subido a HappyRobot (`get_node_details`): descripción, `cola` y `resumen_para_agente` ya tenían los cambios de la ronda 3. En `resumen_para_agente`, «Una sola frase» pasa a «Una o dos frases» para que no choque con «la ÚLTIMA frase».

**Ronda de arreglos 5 (19/10/2026).** `motivo_transferencia` copiado literal de lo subido (los 11 valores).
