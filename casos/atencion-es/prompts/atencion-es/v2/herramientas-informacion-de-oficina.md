<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v2 (x8xd0llbdp3j) · nodo: herramientas (tool) de Información de oficina · copiado: 2026-10-19 (Tarea 11) -->

# Herramientas de «Información de oficina» (v2)

Las herramientas del prompt «Información de oficina» (`0c60218b-8901-47bd-95de-40e0e1af1296`, ID de nodo en la v2
`01a14f1d-0396-717d-8b6f-52f789dbe9a3`).

- Fuente de las descripciones (R3): `{{gestion_abierta}}` va en HappyRobot como nodo de variable de Plate con
  `group_id` `e51cd732-f403-4ef7-95d4-490347960a93`.
- `buscar_punto_de_encuentro` y `volver_al_triaje` (spec §5.7) las crea la Tarea 12 con su Module Change; el prompt
  ya las nombra.

## 1. consultas_alquiler (descripción cambiada en la ronda de arreglos 2)

- Hijo: «Module Change» → «Consultas del alquiler» (viene del duplicado; no se toca, R5).
- `message`: `{"type": "none"}`. Parámetros (`tema`, `pregunta`) los de la v25. Descripción: la de la v25 con dos
  cambios (ronda de arreglos 2): «Alargar el alquiler (devolverlo otro día) siempre va aquí, también con gestión
  cerrada.» y «…que alguien mire o cambie un dato concreto de su reserva sin alargarla».

## 2. transfer_to_human_agent

- Hijo **hoy**: el Transfer «Initiate customer connection» heredado de la v25 (`01a14f1d-0396-788f-81ca-75cf199aabbd`),
  directamente bajo la herramienta. **Pendiente** (ver `docs/pendientes.md`, «Comprobaciones de la Tarea 11»): borrar
  ese Transfer (es una hoja) y crear Python «Preparar transferencia» → Paths «¿Transferir?» → «Transferir» → Transfer
  nuevo con `outside_agent_transfer: false`, igual que en Prolongación (`preparar-transferencia.md`, `transfer.md`).
  El borrado lo rechazó el sistema de permisos el 19/10/2026 a las 11:15.
- `execution`: no se guarda por API (queda el de por defecto).
- `hold_music`: estático, «holdacent» (asset `01a0fc02-a13d-77a2-8de3-82459eb2a2a6`), URL `<URL_FIRMADA>`.
- **message** (tipo `ai`, el de la v25 sin cambios). Ejemplo: «Lo entiendo. Le paso ahora mismo con un compañero que le
  va a ayudar. Puede tardar unos segundos, no cuelgue, por favor.»

**Descripción** (19/10/2026, Tarea 11 y ronda de arreglos 3; empieza con la variable, como en Prolongación, R34): Gestión ahora: {{gestion_abierta}}. Si Gestión ahora es false y el caso es de gestión, no la llames: di que gestión está cerrada y su horario. Transfiere la llamada a una cola de compañeros. Úsala en los casos de ESCALADO: algo de su reserva que hay que mirar o cambiar (un dato ya acordado que no sea alargar el alquiler, un cargo concreto, el código de un parking, Smartkey), avería o accidente, reserva nueva, oficina sin datos que el cliente no resuelve, una persona sin motivo o un idioma que no puedes seguir. Alargar el alquiler no es de gestión: consultas_alquiler. En modo virtual, solo para una avería o un accidente (cola asistencia). Con gestión cerrada, nunca con la cola gestion. El horario, cómo llegar y dónde devolver los das tú; el minibús y las dudas del alquiler tienen su herramienta. Ejecútala en el mismo turno en que decides transferir, sin decir antes «le paso». Si devuelve gestion_cerrada, no la repitas: sigue COLA DE GESTIÓN CERRADA.

**Parámetros (los tres obligatorios; sustituyen al parámetro de la extensión de la v25):**
- `cola`: Cola de destino. Valores permitidos EXACTOS: "gestion" (algo de su reserva: cambiar un dato ya acordado que no sea alargar el alquiler, devolver con la oficina cerrada sin haberlo acordado, el servicio de espera, un cargo concreto, el código de un parking, problemas con Smartkey; solo con gestión abierta), "asistencia" (avería o accidente; funciona siempre), "nueva_reserva" (aún no tiene reserva y quiere alquilar), "minibus" (oficina que no identificas o sin datos y el cliente no lo resuelve, festivos, una persona sin motivo, cliente muy enfadado o idioma que no puedes seguir). Alargar el alquiler no es de gestión: consultas_alquiler. Gestión ahora: {{gestion_abierta}}. Si es false, nunca uses "gestion". Si dudas entre dos, "minibus".
- `motivo_transferencia`: Por qué transfieres. Valores permitidos EXACTOS: los 11 de siempre. En Información de oficina: "pregunta_reserva_concreta" para algo de su reserva; "asistencia"; "nueva_reserva"; "enfado" (cliente muy enfadado que exige una persona) u "otro" (oficina sin datos, festivos, una persona sin motivo, idioma que no puedes seguir).
- `resumen_para_agente`: Resumen del motivo de la llamada que se le leerá en voz alta al compañero que recibe la transferencia, antes de conectarle con el cliente. SIEMPRE en español, aunque el cliente hable otro idioma. Una o dos frases, de 10 a 25 palabras, en tercera persona, que digan qué quiere el cliente, de qué oficina habla y qué se ha intentado ya. Sin datos personales (nombre, reserva, matrícula, correo, teléfono), sin códigos, extensiones ni importes. Si el idioma de la llamada no es español, la ÚLTIMA frase es SIEMPRE «El cliente habla <idioma>» (por ejemplo, «El cliente habla inglés»). Ejemplos: 'Cliente llega a Valencia aeropuerto después del cierre y quiere comprobar el servicio de espera.' 'Cliente pregunta por un cargo de parking en su alquiler de Madrid Atocha.'

## Configuración

| Nodo | ID de nodo en la v2 | persistent_id |
|---|---|---|
| consultas_alquiler → Module Change | `01a14f1d-0398-71cd-be10-a50ab91d1f5d` → `01a14f1d-039b-7e2a-90f5-a43135ba4453` | `6edd13ac-b226-4d1c-87dc-748b46ce5638` |
| transfer_to_human_agent | `01a14f1d-0399-7faf-a630-5c199b3e3efc` | `62c5b6dd-5dde-4b3a-9a93-adb638c0bd66` |
| → Initiate customer connection (v25, por sustituir) | `01a14f1d-0396-788f-81ca-75cf199aabbd` | `faec6a20-257a-4b8c-8c75-8dd336beead7` |

Cuando se cree «Preparar transferencia», su entrada `cola` es `{{62c5b6dd-5dde-4b3a-9a93-adb638c0bd66.cola}}` y las
cuatro `cola_*` de «Resolver colas» (`081e2b5d-…`); el whisper del Transfer lleva el `resumen_para_agente` de esta
herramienta.

**Ronda de arreglos 3 (19/10/2026).** En `transfer_to_human_agent`: el caso de gestión es «cambiar un dato ya acordado que
no sea alargar el alquiler» (antes «la hora o el día de devolución», que hacía que el bot tratara alargar como caso de
gestión: causa de ADV-11), en la descripción y en `cola`, con «Alargar el alquiler no es de gestión: consultas_alquiler»;
y en `resumen_para_agente`, «Si el idioma de la llamada no es español, la ÚLTIMA frase es SIEMPRE «El cliente habla
<idioma>»».

**Ronda de arreglos 4 (19/10/2026).** El cuerpo de esta sección se copió de lo subido a HappyRobot (`get_node_details`): descripción, `cola` y `resumen_para_agente` ya tenían los cambios de la ronda 3. En `resumen_para_agente`, «Una sola frase» pasa a «Una o dos frases» para que no choque con «la ÚLTIMA frase».
