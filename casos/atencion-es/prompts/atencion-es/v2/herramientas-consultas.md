<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v2 (x8xd0llbdp3j) · nodo: herramientas (tool) de Consultas del alquiler · copiado: 2026-10-18 -->

# Herramientas de «Consultas del alquiler» (v2)

Las herramientas del prompt «Consultas del alquiler» (`38378785-0846-4920-b41a-583f7c5773fb`, antes «Prolongación y
consultas»). Un nodo `tool` solo define la función que ve el agente; lo que pasa al ejecutarla lo hacen sus hijos.

- Fuente de las descripciones (R3): `{{gestion_abierta}}` se escribe al subir como
  `{{e51cd732-f403-4ef7-95d4-490347960a93.gestion_abierta}}`, como nodo de variable de Plate.
- `buscar_punto_de_encuentro`, `informacion_oficina` y `transfer_to_human_agent` vienen del duplicado (persistent_id
  = ID de nodo en la v1); `buscar_respuesta` es nueva (persistent_id = ID de nodo en la v2).
- `prolongar_alquiler` y `volver_al_triaje` (spec §5.7): creadas en la Tarea 12, cada una con su Module Change;
  definición, ids y destinos en `saltos.md`.
- Música de espera «holdacent»: asset `01a0fc02-a13d-77a2-8de3-82459eb2a2a6`; la URL firmada del nodo se sustituye
  aquí por `<URL_FIRMADA>`.

## 1. buscar_respuesta (nueva)

- Hijo: Python «Buscar respuesta» (código en `buscar-respuesta.md`; sale de `casos/atencion-es/codigo/consultas_alquiler.py`)
- `message`: `{"type": "none"}`
- La Tarea 10 crea otra igual en Prolongación (misma descripción y parámetros, mismo código).

**Descripción:** Devuelve el texto de las condiciones de Centauro sobre un tema, para responder una duda del alquiler. Úsala ante cada duda nueva, sin decir nada antes, y responde solo con lo que devuelva, en una o dos frases; si lo que pregunta no está, no lo inventes. Si ya tienes en la conversación la sección de ese tema, no la vuelvas a pedir. Si devuelve encontrado: false porque el tema no era de la lista, vuelve a llamarla con un tema válido antes de decir que no tienes el dato. Sirve a cualquier hora, también en modo virtual y con gestión cerrada. NO la uses para prolongar (prolongar_alquiler), para el horario o la dirección de una oficina (informacion_oficina) ni para el minibús (buscar_punto_de_encuentro).

**Parámetros:**
- `tema` (obligatorio): Tema de la duda. Valores permitidos EXACTOS: "reserva_no_iniciada" (cambiar, cancelar o adelantar una reserva que aún no ha empezado; cupón y reembolso de una cancelación; reservas de Booking u otra agencia; extras, Fast Key, Smart Key), "recoger_tarde" (va a llegar tarde a recoger, vuelo o tren retrasado, no pudo recogerlo a su hora), "devolucion" (devolver antes, en otra oficina o con la oficina cerrada; volver desde la oficina), "cargos_y_reembolsos" (fianza, combustible, cargos, reclamaciones, multas, facturas, contrato), "requisitos" (carnet, edad, documentos, tarjeta, pago en efectivo, conductor adicional, quién puede recoger el coche), "durante_el_alquiler" (otro coche del que reservó, daños, testigos y avisos, aire acondicionado, kilómetros, salir de España, coberturas y seguro, zonas de bajas emisiones, limpieza, mascotas), "otras" (sillas, cadenas, accesorios, entrega a domicilio, teléfono de una oficina, objetos olvidados, grúa, minibús adaptado, autoridades, consultas ajenas a Centauro y lo que no encaje en otro tema), "telefonos" (pide un teléfono de Centauro), "detalles_prolongacion" (precio y condiciones de prolongar, penalización por devolver tarde, cuánto se puede prolongar, contrato vencido), "devolver_tarde" (si hay margen o periodo de cortesía al devolver), "la_web_no_le_deja" (la web o la app no le deja prolongar o pagar, no le llega el correo de la contraseña, no ve su reserva), "aseguradora_empresa" (coche de sustitución de su aseguradora o coche de empresa). Si no encaja en ninguno, "otras".
- `pregunta` (opcional): La duda del cliente en una frase corta, sin datos personales (ni nombre, ni reserva, ni matrícula, ni correo, ni teléfono). Si todavía no la ha concretado, OMITE este parámetro.

## 2. buscar_punto_de_encuentro

- Hijo: «Module Change» → «Punto de encuentro» (existe desde la v25; no se toca)
- `message`: `{"type": "none"}`
- Parámetros `aeropuerto` y `terminal`: sin cambios (los de la v25).

**Descripción:** Úsala cuando el cliente pregunta por el minibús, por el punto de encuentro o por cómo llegar del aeropuerto a la oficina de Centauro, y ya sabes en qué aeropuerto está. La herramienta continúa la conversación: da el punto de encuentro o avisa de que la oficina de ese aeropuerto ya ha cerrado. Sirve a cualquier hora, también en modo virtual. NO la uses si se queja de que el minibús no llega, se ha ido sin él o lleva tiempo esperando (salvo que lleve menos de diez minutos): eso se transfiere a la cola minibus, salvo en modo virtual: entonces no transfieras; dile que a esta hora no hay compañeros y que puede volver a llamar a partir de las ocho de la mañana. NO la uses para el horario, la dirección o la devolución en una oficina (informacion_oficina). Si todavía no sabes el aeropuerto, pregúntalo antes. Nunca preguntes la terminal solo para poder llamarla: es opcional. No digas nada antes ni después.

## 3. informacion_oficina

- Hijo: «Module Change» → «Información de oficina» (existe desde la v25; no se toca)
- `message`: `{"type": "none"}`
- Parámetros `tema` y `oficina`: sin cambios (los de la v25).

**Descripción:** Úsala cuando el cliente quiera saber el horario de una oficina de Centauro, cómo llegar a una oficina de estación o de ciudad, o dónde se devuelve el coche en una oficina. Sirve a cualquier hora, también en modo virtual. NO la uses para el minibús ni para el punto de encuentro de un aeropuerto (buscar_punto_de_encuentro). Devolver el coche antes de tiempo o en otra oficina distinta de la del contrato es una duda del alquiler: buscar_respuesta con el tema devolucion. No digas nada antes ni después: la herramienta continúa la conversación.

## 4. transfer_to_human_agent

- Hijo: Python «Preparar transferencia» → Paths «¿Transferir?» → «Transferir» → Transfer «Initiate customer
  connection» (mismo patrón que el Triaje: `preparar-transferencia.md` y `transfer.md`; ids abajo)
- `execution`: no se guarda por API (queda el de por defecto)
- `hold_music`: estático, «holdacent» (asset `01a0fc02-a13d-77a2-8de3-82459eb2a2a6`), URL `<URL_FIRMADA>`
- **message** (tipo `ai`; cambiado en la Tarea 15b, R34, D-013; el del Triaje sigue sin cambios): ejemplo «Entiendo su enfado, y siento que haya tenido que esperar tanto. Le paso ahora mismo con un compañero que le va a ayudar. Puede tardar unos segundos, no cuelgue, por favor.» Descripción (`{{gestion_abierta}}` es un nodo de variable de Plate con `group_id` `e51cd732-…`): Gestión ahora: {{gestion_abierta}}. Si Gestión ahora es false, puede que no haya ningún compañero y que la transferencia no salga: no digas que le pasas con nadie; di solo, en su idioma, «Un momento, por favor, no cuelgue.» (si está molesto, valida antes su molestia en una frase corta). Si Gestión ahora es true: informa al cliente, en su idioma, de que le vas a pasar con un compañero que le va a ayudar. Sé breve y tranquilizador. Termina SIEMPRE avisando de que puede tardar unos segundos en atenderle y pidiéndole que no cuelgue (por ejemplo: "puede tardar unos segundos, no cuelgue, por favor"). Si el cliente está molesto, frustrado o ya ha tenido que insistir para que le pases con alguien, valida primero su emoción en una frase corta y sincera antes de anunciar la transferencia: reconoce la molestia concreta que te ha expresado, sin excusas largas ni justificaciones. Nunca anuncies la transferencia en seco a un cliente enfadado. No menciones colas, extensiones ni números. No prometas una oficina concreta ni un equipo específico.

**Descripción:** Transfiere la llamada a una cola de compañeros. Úsala solo en los casos de ESCALADO, o si no puedes seguir al cliente por el idioma. Cuando la sección manda transferir en el caso del cliente: si ya ha pedido que lo mire alguien, ejecútala en ese turno; si no, pregúntale antes si quiere que le pases (puedes decir antes una frase con la respuesta) y ejecútala cuando acepte. En modo virtual, solo para una avería o un accidente (cola asistencia). Con gestión cerrada, nunca con la cola gestion. Prolongar, la web, la contraseña, el minibús y las oficinas no se transfieren: tienen su herramienta. Ejecútala en el mismo turno en que decides transferir, sin decir antes «le paso». Si devuelve gestion_cerrada, no la repitas: sigue COLA DE GESTIÓN CERRADA.

**Parámetros (los tres obligatorios):**
- `cola` (en HappyRobot, `{{gestion_abierta}}` va como nodo de variable de Plate): Cola de destino. Valores permitidos EXACTOS: "asistencia" (avería o accidente, o acepta que le pases por un aviso del coche o por la grúa; funciona siempre), "nueva_reserva" (quiere hacer una reserva nueva o acepta que un compañero se la prepare), "minibus" (queja del minibús o idioma que no puedes seguir), "gestion" (lo que la sección manda a GESTIÓN DE RESERVA, un dato concreto de su reserva, o una persona sin motivo; solo con gestión abierta). Gestión ahora: {{gestion_abierta}}. Si es false, nunca uses "gestion".
- `motivo_transferencia`: Por qué transfieres. Valores permitidos EXACTOS: "no_iniciada", "web_no_disponible", "pregunta_reserva_concreta", "aseguradora", "enfado", "error_tecnico", "minibus", "asistencia", "nueva_reserva", "correo_no_coincide", "otro". En Consultas: el que diga la sección; si no dice ninguno, "pregunta_reserva_concreta" (dato concreto de su reserva), "asistencia", "nueva_reserva", "minibus", "enfado" (cliente muy enfadado que exige una persona) u "otro".
- `resumen_para_agente`: Resumen del motivo de la llamada que se le leerá en voz alta al compañero que recibe la transferencia, antes de conectarle con el cliente. SIEMPRE en español, aunque el cliente hable otro idioma. Una sola frase, de 10 a 25 palabras, en tercera persona, que diga qué quiere el cliente y qué se ha intentado ya. Sin datos personales (nombre, reserva, matrícula, correo, teléfono), sin códigos, extensiones ni importes. Si el cliente habla otro idioma, añade al final 'El cliente habla inglés' (o el idioma que sea). Ejemplos: 'Cliente quiere que un compañero cancele su reserva, que aún no ha empezado.' 'Cliente con pinchazo en carretera, necesita asistencia.' 'Cliente quiere que revisen ahora un cargo que no reconoce; ya conoce el formulario de reclamaciones.'

## Configuración

| Nodo | ID de nodo en la v2 | persistent_id |
|---|---|---|
| buscar_respuesta → Python «Buscar respuesta» | `01a14fa1-5c34-7bff-9366-aa7e9e4e448a` → `01a14fa1-5c44-7c37-821c-1d01c0bd41eb` | = ID de nodo |
| buscar_punto_de_encuentro → Module Change | `01a14f1d-0398-793a-a4f6-4cc4ed3a45c4` → `01a14f1d-039a-76cb-8e2c-fd908a63d1af` | `eda4aa10-c99e-4319-b7ae-dbf5dc6db949` → `081b2d5c-d7cf-49b7-b0a1-70c82ee5aac7` |
| informacion_oficina → Module Change | `01a14f1d-0398-78ce-93ed-6d599a4dcad6` → `01a14f1d-039a-7490-9015-e42727f49b17` | `0be9b6d8-9353-41de-8049-c2e477ed6668` → `91b601ad-4782-44fb-955a-5bc42657c191` |
| transfer_to_human_agent | `01a14f1d-0399-7dbf-9f55-4977771a298f` | `fbe2e40e-4915-4f44-9bac-59c318862e97` |
| → Python «Preparar transferencia» | `01a14fa7-1147-724b-af62-e10108d91bce` | = ID de nodo |
| → Paths «¿Transferir?» | `01a14fa7-420e-78db-a46a-1afc6823c0ac` | = ID de nodo |
| → condition «Transferir» → Transfer «Initiate customer connection» | `01a14fa7-421d-7c4b-ab14-17edc7ed95df` → `01a14fa7-4228-7812-a6b7-aa42c035b190` | = ID de nodo |
| → condition «Fallback» (sin hijos) | `01a14fa7-420f-76f4-b6af-ab7cbfd553da` | = ID de nodo |

El Transfer heredado de la v25 (`01a14f1d-0396-7a17-8d6f-6fbebc267578`, sin hijos) se borró en la Tarea 9. La
configuración de «Preparar transferencia» (entrada `cola` = `{{fbe2e40e-4915-4f44-9bac-59c318862e97.cola}}` y las
cuatro `cola_*` de «Resolver colas»), la condición y el Transfer son iguales a los del Triaje
(`preparar-transferencia.md`, `transfer.md`).

**Cambios de la Tarea 9.** La descripción de `transfer_to_human_agent` es la de la ronda de arreglos 1 (D-003): si la
sección manda transferir y el cliente no lo ha pedido, el bot ofrece pasarle y transfiere cuando acepta; si ya lo ha
pedido, transfiere en ese turno. (En la vuelta 3 decía «ejecútala en ese mismo turno, sin preguntarle si quiere», y
antes «Si la respuesta está en lo que devuelve buscar_respuesta, dala antes».) La de `buscar_respuesta` añade qué
hacer con `encontrado: false`, y la de `buscar_punto_de_encuentro`, la excepción del modo virtual. Las de `buscar_punto_de_encuentro`
e `informacion_oficina` se reescribieron (la de la v25 decía que no se usara en modo virtual).
