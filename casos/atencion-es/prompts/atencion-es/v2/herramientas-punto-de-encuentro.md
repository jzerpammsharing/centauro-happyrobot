<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v2 (x8xd0llbdp3j) · nodo: herramientas (tool) de Punto de encuentro · copiado: 2026-10-19 (Tarea 11) -->

# Herramientas de «Punto de encuentro» (v2)

Las herramientas del prompt «Punto de encuentro» (`a80fca22-b295-41e3-a735-a3c878af4eee`, ID de nodo en la v2
`01a14f1d-0397-7c91-b2bc-a12efeed5595`).

- Fuente de las descripciones (R3): `{{gestion_abierta}}` va en HappyRobot como nodo de variable de Plate con
  `group_id` `e51cd732-f403-4ef7-95d4-490347960a93`.
- `informacion_oficina` y `volver_al_triaje` (spec §5.7): creadas en la Tarea 12, cada una con su Module Change;
  definición, ids y destinos en `saltos.md`.

## 1. consultas_alquiler (descripción cambiada en las rondas de arreglos 1 y 2)

- Hijo: «Module Change» → «Consultas del alquiler» (viene del duplicado; no se toca, R5).
- `message`: `{"type": "none"}`. Parámetros (`tema`, `pregunta`) los de la v25. Descripción: la de la v25 con tres
  cambios (rondas de arreglos 1 y 2): delante, «NO la uses si en el mismo turno se queja del minibús (se fue sin él, no
  pasa, lleva esperando igual o más que la frecuencia): eso va primero (ESCALADO), salvo si PRIMERO dio true: entonces
  sigue PRIMERO.»; «Alargar el alquiler (devolverlo otro día) siempre va aquí, también con gestión cerrada.»; y «…que
  alguien mire o cambie un dato concreto de su reserva sin alargarla».

## 2. transfer_to_human_agent

- Hijo **hoy**: el Transfer «Initiate customer connection» heredado de la v25 (`01a14f1d-0396-7961-a5d9-ee9de58e701b`),
  directamente bajo la herramienta. **Pendiente** (ver `docs/pendientes.md`, «Comprobaciones de la Tarea 11»): borrar
  ese Transfer (es una hoja) y crear Python «Preparar transferencia» → Paths «¿Transferir?» → «Transferir» → Transfer
  nuevo con `outside_agent_transfer: false`, igual que en Prolongación (`preparar-transferencia.md`, `transfer.md`).
  El borrado lo rechazó el sistema de permisos el 19/10/2026 a las 11:15.
- `execution`: no se guarda por API (queda el de por defecto).
- `hold_music`: estático, «holdacent» (asset `01a0fc02-a13d-77a2-8de3-82459eb2a2a6`), URL `<URL_FIRMADA>`.
- **message** (tipo `ai`, el de la v25 sin cambios). Ejemplo: «Lo entiendo, y tiene razón. Le paso ahora mismo con un
  compañero para que vea qué está pasando. Puede tardar unos segundos, no cuelgue, por favor.»

**Descripción** (19/10/2026, Tarea 11 y ronda de arreglos 3; empieza con la variable, como en Prolongación, R34): Gestión ahora: {{gestion_abierta}}. Si Gestión ahora es false y el caso es de gestión, no la llames: di que gestión está cerrada y su horario. Transfiere la llamada a una cola de compañeros. Úsala en los casos de ESCALADO: queja real del minibús, cliente perdido que sigue sin encontrar el punto, avería o accidente, algo de su reserva que hay que mirar o cambiar (un dato ya acordado que no sea alargar el alquiler), reserva nueva, una persona sin motivo o un idioma que no puedes seguir. Alargar el alquiler no es de gestión: consultas_alquiler. En modo virtual, solo para una avería o un accidente (cola asistencia): si se queja del minibús o pide una persona, no la llames y sigue EN MODO VIRTUAL. Con gestión cerrada, nunca con la cola gestion. El punto de encuentro, el horario y la devolución en su aeropuerto y las dudas del alquiler no se transfieren: los das tú o tienen su herramienta. Ejecútala en el mismo turno en que decides transferir, sin decir antes «le paso». Si devuelve gestion_cerrada, no la repitas: sigue COLA DE GESTIÓN CERRADA.

**Parámetros (los tres obligatorios; sustituyen al parámetro de la extensión de la v25):**
- `cola`: Cola de destino. Valores permitidos EXACTOS: "minibus" (queja real del minibús, cliente perdido que sigue sin encontrar el punto, Palma de Mallorca, aeropuerto sin datos, pregunta del minibús que no está en tus instrucciones, una persona sin motivo o idioma que no puedes seguir), "asistencia" (avería o accidente; funciona siempre), "gestion" (algo de una reserva que ya tiene: cambiar un dato ya acordado que no sea alargar el alquiler, devolver con la oficina cerrada sin haberlo acordado, el servicio de espera; solo con gestión abierta), "nueva_reserva" (aún no tiene reserva y quiere alquilar). Alargar el alquiler no es de gestión: consultas_alquiler. Gestión ahora: {{gestion_abierta}}. Si es false, nunca uses "gestion". Si dudas entre dos, "minibus".
- `motivo_transferencia`: Por qué transfieres. Valores permitidos EXACTOS: "no_iniciada", "web_no_disponible", "pregunta_reserva_concreta", "aseguradora", "enfado", "error_tecnico", "minibus", "asistencia", "nueva_reserva", "correo_no_coincide", "otro". En Punto de encuentro: "minibus" para una queja o un problema del minibús o del punto de encuentro; "asistencia"; "pregunta_reserva_concreta" para algo de su reserva; "nueva_reserva"; "enfado" (cliente muy enfadado que exige una persona) u "otro" (una persona sin motivo, idioma que no puedes seguir).
- `resumen_para_agente`: Resumen del motivo de la llamada que se le leerá en voz alta al compañero que recibe la transferencia, antes de conectarle con el cliente. SIEMPRE en español, aunque el cliente hable otro idioma. Una o dos frases, de 10 a 25 palabras, en tercera persona, que digan qué quiere el cliente, en qué aeropuerto y terminal está y qué se ha intentado ya (por ejemplo, que ya recibió la indicación del punto de encuentro). Sin datos personales (nombre, reserva, matrícula, correo, teléfono), sin códigos, extensiones ni importes. Si el idioma de la llamada no es español, la ÚLTIMA frase es SIEMPRE «El cliente habla <idioma>» (por ejemplo, «El cliente habla inglés»). Ejemplos: 'Cliente en Barcelona T1 lleva veinte minutos en el punto de encuentro y el minibús no ha pasado.' 'Cliente en Valencia lleva veinticinco minutos esperando el minibús en el pe seis. El cliente habla inglés.'

## Configuración

| Nodo | ID de nodo en la v2 | persistent_id |
|---|---|---|
| consultas_alquiler → Module Change | `01a14f1d-0398-7a4b-84e7-313e054df714` → `01a14f1d-039b-7e6e-91ee-a0401da2c7e3` | `3f1c2be8-8768-455f-895b-047063ea7938` |
| transfer_to_human_agent | `01a14f1d-0398-75cb-939a-e2f512c94a01` | `00435498-eccf-4110-9cf1-eb17821af3ed` |
| → Initiate customer connection (v25, por sustituir) | `01a14f1d-0396-7961-a5d9-ee9de58e701b` | `37fb8053-214e-4357-be80-0fc8f832ecbc` |

Cuando se cree «Preparar transferencia», su entrada `cola` es `{{00435498-eccf-4110-9cf1-eb17821af3ed.cola}}` y las
cuatro `cola_*` de «Resolver colas» (`081e2b5d-…`); el whisper del Transfer lleva el `resumen_para_agente` de esta
herramienta.

**Ronda de arreglos 3 (19/10/2026).** En `transfer_to_human_agent`: el caso de gestión es «cambiar un dato ya acordado que
no sea alargar el alquiler» (antes «la hora o el día de devolución», que hacía que el bot tratara alargar como caso de
gestión: causa de ADV-11), en la descripción y en `cola`, con «Alargar el alquiler no es de gestión: consultas_alquiler»;
y en `resumen_para_agente`, «Si el idioma de la llamada no es español, la ÚLTIMA frase es SIEMPRE «El cliente habla
<idioma>»».

**Ronda de arreglos 4 (19/10/2026).** El cuerpo de esta sección se copió de lo subido a HappyRobot (`get_node_details`): descripción, `cola` y `resumen_para_agente` ya tenían los cambios de la ronda 3. En `resumen_para_agente`, «Una sola frase» pasa a «Una o dos frases» para que no choque con «la ÚLTIMA frase».

**Ronda de arreglos 5 (19/10/2026).** `motivo_transferencia` copiado literal de lo subido (los 11 valores).
