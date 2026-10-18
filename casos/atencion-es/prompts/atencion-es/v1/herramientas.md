<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v1 (veavliy3k6jx) · nodo: herramientas (tool) de Triaje y horario, Punto de encuentro, Información de oficina y Prolongación y consultas · copiado: 2026-10-18 -->

# Herramientas (v1)

Las 11 herramientas (nodos `tool`) de la v1, agrupadas por módulo. Un nodo `tool` solo define la función que ve el
agente (descripción y parámetros); lo que ocurre al ejecutarla lo hacen sus hijos: el siguiente prompt (salto de
módulo), un «Module Change» (vuelta a un módulo ya abierto) o un «Initiate customer connection» (transferencia).

- Las variables se escriben como `{{persistent_id.variable}}`. Los `tool_index_id` / `tool_index_hash` son internos
  de cada versión y se omiten.
- `081e2b5d-b260-41a6-bd2a-6f82b26193d1` es «Resolver colas por idioma»; `e51cd732-f403-4ef7-95d4-490347960a93` es
  «Calcular horario nocturno».
- En la música de espera «holdacent» (asset `01a0fc02-a13d-77a2-8de3-82459eb2a2a6`) se ha sustituido la URL firmada
  por `<URL_FIRMADA>`. La del Triaje es una URL pública sin firma.
- Persistent ID de cada herramienta = ID de nodo en la v1.

## A. Triaje y horario (`c5a70932-117c-4360-9be8-adce260fe13e`)

### A1. buscar_punto_de_encuentro

- persistent_id: `72261523-5d3f-4830-ac36-67ab187d93ed`
- Hijo: prompt «Punto de encuentro»
- `message`: `{"type": "none"}`

**Descripción:** Úsala cuando ya sabes en qué aeropuerto está el cliente Y el valor de su lista es false (la oficina de ese aeropuerto sigue abierta). Sirve para consultar y darle el punto de encuentro del minibús. NO la uses si el valor de su lista es true: en ese caso la oficina ya ha cerrado y solo se avisa del cierre y de la hora de apertura (Paso 3). NO la uses si el cliente se queja de que el minibús no llega, se ha ido sin él o lleva tiempo esperando: eso se transfiere a la cola de MINIBÚS. NO la uses si pregunta por el horario de una oficina o por dónde devolver el coche: para eso está informacion_oficina. NO la uses para prolongar, para un retraso o para dudas del alquiler: para eso está consultas_alquiler. NO la uses si todavía no sabes el aeropuerto. Nunca preguntes por la terminal solo para poder llamar a esta herramienta: la terminal es opcional y la consulta funciona sin ella.

**Parámetros:**
- `aeropuerto` (obligatorio): Nombre del aeropuerto donde se encuentra el cliente, tal como lo ha dicho (por ejemplo: Valencia, Rodas, Lisboa, Madrid).
- `terminal` (opcional): Terminal o puerta de salida, SOLO si el cliente la ha mencionado espontáneamente. Si el cliente no ha dicho la terminal, OMITE este parámetro por completo: no lo incluyas en la llamada y no lo envíes como texto vacío, ni con guiones, ni con valores como "no indicada" o "desconocida". Nunca deduzcas ni inventes una terminal, y nunca se la preguntes al cliente solo para rellenar este campo.

### A2. transfer_to_human_agent

- persistent_id: `17c682a0-82d2-42f6-88fa-817d8cba0783`
- Hijo: «Initiate customer connection» (`b4439401-fdae-4a3b-9a42-9a5c2de8f1b2`)
- `execution`: `{"async": false, "force_invoke_llm_on_result": false}`
- `hold_music`: estático, «Acoustic» (`https://storage.googleapis.com/happyrobot-public/on-hold/acoustic.8k.wav`)

**message** (tipo `ai`). Ejemplo: «Entiendo su enfado, y siento que haya tenido que esperar tanto. Le paso ahora mismo con un compañero que le va a ayudar. Puede tardar unos segundos, no cuelgue, por favor.» Descripción: Informa al cliente, en su idioma, de que le vas a pasar con un compañero que le va a ayudar. Sé breve y tranquilizador. Termina SIEMPRE avisando de que puede tardar unos segundos en atenderle y pidiéndole que no cuelgue (por ejemplo: "puede tardar unos segundos, no cuelgue, por favor"). Si el cliente está molesto, frustrado o ya ha tenido que insistir para que le pases con alguien, valida primero su emoción en una frase corta y sincera antes de anunciar la transferencia: reconoce la molestia concreta que te ha expresado, sin excusas largas ni justificaciones. Nunca anuncies la transferencia en seco a un cliente enfadado. No menciones colas, extensiones ni números. No prometas una oficina concreta ni un equipo específico.

**Descripción:** Transfiere la llamada a la cola de agentes humanos que corresponda al MOTIVO del cliente. IMPORTANTE: en modo virtual (centro de atención cerrado) NO hay compañeros: no uses esta herramienta salvo para una avería o un accidente (cola de asistencia). Con el centro de atención abierto, úsala cuando: 1) el cliente tiene una avería o accidente, 2) necesita que alguien mire o cambie un dato concreto de su reserva, 3) todavía no tiene reserva y quiere alquilar un coche, 4) se queja del minibús (no llega, se fue sin él, lleva tiempo esperando, quiere reclamar), 5) pide hablar con una persona y, después de preguntarle una vez qué necesita, lo repite sin dar motivo, 6) no puedes seguir al cliente con fiabilidad por idioma. Las prolongaciones, los retrasos y las dudas generales del alquiler NO se transfieren desde aquí: van a consultas_alquiler. Ejecútala en el mismo turno en que decides transferir. Debes elegir SIEMPRE la extensión correcta según el motivo, usando la tabla del parámetro extension_destino, y rellenar siempre resumen_para_agente.

**Parámetros:**
- `extension_destino` (obligatorio): La extensión de la cola destino. Copia EXACTAMENTE uno de estos cuatro valores, sin inventar ni alterar ningún dígito. Queja o problema del minibús (se fue sin él, aún no pasa, mucha espera), cliente perdido, petición de hablar con una persona sin motivo o idioma no soportado: `{{081e2b5d-b260-41a6-bd2a-6f82b26193d1.cola_horario_minibus}}`. Avería o accidente: `{{081e2b5d-b260-41a6-bd2a-6f82b26193d1.cola_asistencia}}`. Un dato concreto de una reserva existente que hay que mirar o cambiar: `{{081e2b5d-b260-41a6-bd2a-6f82b26193d1.cola_gestion_reserva}}`. Reserva nueva (todavía no tiene reserva y quiere alquilar, o pregunta precios o disponibilidad para un alquiler nuevo, aunque diga «reservar» o «mi reserva»): `{{081e2b5d-b260-41a6-bd2a-6f82b26193d1.cola_nueva_reserva}}`. Si dudas entre varias, usa la del minibús. Este parámetro es obligatorio: nunca lo dejes vacío ni lo rellenes con un texto genérico.
- `resumen_para_agente` (obligatorio): Resumen del motivo de la llamada que se le leerá en voz alta al compañero que recibe la transferencia, antes de conectarle con el cliente. SIEMPRE en español, aunque el cliente hable otro idioma. Una sola frase, de 10 a 25 palabras, en tercera persona, que diga qué quiere el cliente, en qué aeropuerto u oficina está si lo sabes y qué se ha intentado ya. Sin datos personales (nombre, reserva, matrícula, correo, teléfono), sin códigos, extensiones ni importes. Si el cliente habla otro idioma, añade al final 'El cliente habla inglés' (o el idioma que sea). Ejemplos: 'Cliente en Madrid T4 lleva veinte minutos esperando el minibús y no ha pasado.' 'Cliente con pinchazo en carretera, necesita asistencia.' 'Cliente quiere cambiar la hora de devolución de su reserva.'

### A3. informacion_oficina

- persistent_id: `414b964d-bb29-428a-b9a1-92b1a3a8d6be`
- Hijo: prompt «Información de oficina»
- `message`: `{"type": "none"}`

**Descripción:** Úsala cuando el cliente quiera saber el horario de una oficina de Centauro, cómo llegar a una oficina de estación o de ciudad, o dónde devolver el coche. Sirve a cualquier hora, también en horario nocturno. NO la uses para el minibús ni para el punto de encuentro de un aeropuerto: para eso está buscar_punto_de_encuentro.

**Parámetros:**
- `tema` (obligatorio): Lo que quiere saber el cliente. Valores permitidos EXACTOS: "horario" (horario de la oficina), "como_llegar" (cómo llegar a una oficina de estación o de ciudad para recoger el coche), "devolucion" (dónde devolver el coche). Si pregunta por varias cosas, pon la primera que haya pedido.
- `oficina` (opcional): La oficina, ciudad, estación o aeropuerto tal como lo ha dicho el cliente (por ejemplo: Málaga estación, Atocha, Madrid, Alicante aeropuerto). Si el cliente todavía no lo ha dicho, OMITE este parámetro por completo: no lo envíes vacío ni con valores como "desconocida". Nunca lo deduzcas ni lo preguntes solo para rellenarlo: la herramienta se encarga de identificar la oficina.

### A4. consultas_alquiler

- persistent_id: `414bdc8c-aacc-4125-b323-acc6a2ae3373`
- Hijo: prompt «Prolongación y consultas»
- `message`: `{"type": "none"}`

**Descripción:** Úsala cuando el cliente quiere prolongar el alquiler que tiene en curso, devolver el coche más tarde, en otra oficina o antes de tiempo, va a llegar tarde a recoger el coche (vuelo o tren retrasado), o tiene una duda general sobre su alquiler o las condiciones de Centauro: cancelar o cambiar una reserva que aún no ha empezado, contraseña o área de cliente de la web, fianza, combustible, documentos, carnet, tarjeta, edad, conductor adicional, sillas para niños, kilómetros, salir de España, multas, facturas, reclamar un cargo, daños, un testigo encendido, el aire acondicionado, mascotas. Sirve a cualquier hora, también en modo virtual. NO la uses para el minibús o el punto de encuentro (buscar_punto_de_encuentro), para el horario, la dirección o dónde devolver el coche en una oficina (informacion_oficina), para una avería o un accidente, para una reserva nueva ni cuando necesita que alguien mire o cambie un dato concreto de su reserva: eso se transfiere. No digas nada especial antes: la herramienta continúa la conversación.

**Parámetros:**
- `tema` (obligatorio): Tema de la consulta. Valores permitidos EXACTOS: "prolongar" (quedarse el coche más tiempo o devolverlo más tarde), "recoger_tarde" (va a llegar tarde a recoger, vuelo o tren retrasado), "reserva_no_iniciada" (cancelar, cambiar o adelantar una reserva que aún no ha empezado), "devolucion" (devolver antes, en otra oficina o con la oficina cerrada), "cargos_y_reembolsos" (fianza, combustible, cargos, multas, facturas, reembolsos), "requisitos" (carnet, edad, documentos, tarjeta, conductor adicional), "durante_el_alquiler" (daños, testigos, aire acondicionado, kilómetros, salir de España, limpieza, mascotas, sillas, cadenas), "otro". Si pregunta por varias cosas, pon la primera.
- `pregunta` (opcional): La pregunta del cliente en una frase corta, tal como la ha dicho, sin datos personales (ni nombre, ni reserva, ni matrícula, ni correo, ni teléfono). Si todavía no ha concretado la pregunta, OMITE este parámetro.

## B. Punto de encuentro (`a80fca22-b295-41e3-a735-a3c878af4eee`)

### B1. consultas_alquiler

- persistent_id: `3f1c2be8-8768-455f-895b-047063ea7938`
- Hijo: «Module Change» → «Prolongación y consultas» (ver `module-change.md`)
- `message`: `{"type": "none"}`
- Parámetros `tema` y `pregunta`: iguales que en A4.

**Descripción:** Úsala cuando el cliente quiere prolongar el alquiler que tiene en curso, devolver el coche más tarde o antes de tiempo, va a llegar tarde a recoger el coche (vuelo o tren retrasado), o tiene una duda general sobre su alquiler o las condiciones de Centauro: cancelar o cambiar una reserva que aún no ha empezado, contraseña o área de cliente de la web, fianza, combustible, documentos, carnet, tarjeta, edad, conductor adicional, sillas para niños, kilómetros, salir de España, multas, facturas, reclamar un cargo, daños, un testigo encendido, el aire acondicionado, mascotas. Sirve a cualquier hora, también en modo virtual. NO la uses para el minibús, el punto de encuentro o el horario y la devolución en un aeropuerto (eso lo resuelves tú en esta parte de la llamada), para una avería o un accidente, para una reserva nueva ni cuando necesita que alguien mire o cambie un dato concreto de su reserva: eso se transfiere. No digas nada especial antes: la herramienta continúa la conversación.

### B2. transfer_to_human_agent

- persistent_id: `00435498-eccf-4110-9cf1-eb17821af3ed`
- Hijo: «Initiate customer connection» (`37fb8053-214e-4357-be80-0fc8f832ecbc`)
- `execution`: `{"async": false, "force_invoke_llm_on_result": false}`
- `hold_music`: estático, «holdacent» (asset `01a0fc02-a13d-77a2-8de3-82459eb2a2a6`), URL `<URL_FIRMADA>`

**message** (tipo `ai`). Ejemplo: «Lo entiendo, y tiene razón. Le paso ahora mismo con un compañero para que vea qué está pasando. Puede tardar unos segundos, no cuelgue, por favor.» Descripción: Informa al cliente, en su idioma, de que le vas a pasar con un compañero que le va a ayudar. Sé breve y tranquilizador. Termina SIEMPRE avisando de que puede tardar unos segundos en atenderle y pidiéndole que no cuelgue (por ejemplo: "puede tardar unos segundos, no cuelgue, por favor"). Si el cliente está molesto, valida primero su enfado. No menciones colas, extensiones ni números. No prometas llamar al conductor ni a una oficina concreta.

**Descripción:** Transfiere la llamada a la cola de agentes humanos que corresponda al MOTIVO del cliente. IMPORTANTE: en modo virtual (centro de atención cerrado) NO hay compañeros: no uses esta herramienta salvo para una avería o un accidente (cola de asistencia). Con el centro de atención abierto, úsala cuando: 1) el cliente está enfadado o tiene una queja real del minibús (se fue sin él, aún no pasa, lleva esperando igual o más que la frecuencia de su aeropuerto, quiere reclamar), 2) el cliente sigue perdido tras darle la indicación una vez, 3) estás en Palma de Mallorca y el cliente no encuentra el punto, 4) el cliente tiene una avería o accidente, 5) necesita que alguien mire o cambie algo de su reserva, pregunta algo del alquiler que no está en tus instrucciones, o acepta que un compañero compruebe el servicio de espera, 6) todavía no tiene reserva y quiere alquilar un coche, 7) el cliente pide hablar con una persona sin dar motivo, 8) no puedes seguir al cliente con fiabilidad por idioma, 9) pregunta algo que no está en tus instrucciones. Ejecútala en el mismo turno en que decides transferir. Debes elegir SIEMPRE la extensión correcta según el motivo, usando la tabla del parámetro extension_destino, y rellenar siempre resumen_para_agente.

**Parámetros:**
- `extension_destino` (obligatorio): La extensión de la cola destino. Copia EXACTAMENTE uno de estos cuatro valores, sin inventar ni alterar ningún dígito. Queja o problema del minibús (se fue sin él, aún no pasa, mucha espera), cliente perdido, Palma de Mallorca, petición genérica de hablar con una persona, idioma no soportado o pregunta que no está en tus instrucciones: `{{081e2b5d-b260-41a6-bd2a-6f82b26193d1.cola_horario_minibus}}`. Avería o accidente: `{{081e2b5d-b260-41a6-bd2a-6f82b26193d1.cola_asistencia}}`. Reserva existente (algo que hay que mirar o cambiar, servicio de espera por vuelo retrasado, cambio de día de devolución, preguntas del alquiler que no están en tus instrucciones): `{{081e2b5d-b260-41a6-bd2a-6f82b26193d1.cola_gestion_reserva}}`. Reserva nueva (todavía no tiene reserva y quiere alquilar, o pregunta precios o disponibilidad para un alquiler nuevo, aunque diga «reservar» o «mi reserva»): `{{081e2b5d-b260-41a6-bd2a-6f82b26193d1.cola_nueva_reserva}}`. Si dudas entre varias, usa la del minibús. Este parámetro es obligatorio: nunca lo dejes vacío ni lo rellenes con un texto genérico.
- `resumen_para_agente` (obligatorio): Resumen del motivo de la llamada que se le leerá en voz alta al compañero que recibe la transferencia, antes de conectarle con el cliente. SIEMPRE en español, aunque el cliente hable otro idioma. Una sola frase, de 10 a 25 palabras, en tercera persona, que diga qué quiere el cliente, en qué aeropuerto y terminal está y qué se ha intentado ya (por ejemplo, que ya recibió la indicación del punto de encuentro). Sin datos personales (nombre, reserva, matrícula, correo, teléfono), sin códigos, extensiones ni importes. Si el cliente habla otro idioma, añade al final 'El cliente habla inglés' (o el idioma que sea). Ejemplos: 'Cliente en Barcelona T1 lleva veinte minutos en el punto de encuentro y el minibús no ha pasado.' 'Cliente en Palma no encuentra el punto de encuentro tras darle la indicación.'

## C. Información de oficina (`0c60218b-8901-47bd-95de-40e0e1af1296`)

### C1. consultas_alquiler

- persistent_id: `6edd13ac-b226-4d1c-87dc-748b46ce5638`
- Hijo: «Module Change» → «Prolongación y consultas» (ver `module-change.md`)
- `message`: `{"type": "none"}`
- Parámetros `tema` y `pregunta`: iguales que en A4.

**Descripción:** Úsala cuando el cliente quiere prolongar el alquiler que tiene en curso, devolver el coche más tarde o antes de tiempo, va a llegar tarde a recoger el coche (vuelo o tren retrasado), o tiene una duda general sobre su alquiler o las condiciones de Centauro: cancelar o cambiar una reserva que aún no ha empezado, contraseña o área de cliente de la web, fianza, combustible, documentos, carnet, tarjeta, edad, conductor adicional, sillas para niños, kilómetros, salir de España, multas, facturas, reclamar un cargo, daños, un testigo encendido, el aire acondicionado, mascotas. Sirve a cualquier hora, también en modo virtual. NO la uses para el horario, la dirección o dónde devolver el coche en una oficina (eso lo resuelves tú en esta parte de la llamada), para una avería o un accidente, para una reserva nueva ni cuando necesita que alguien mire o cambie un dato concreto de su reserva: eso se transfiere. No digas nada especial antes: la herramienta continúa la conversación.

### C2. transfer_to_human_agent

- persistent_id: `62c5b6dd-5dde-4b3a-9a93-adb638c0bd66`
- Hijo: «Initiate customer connection» (`faec6a20-257a-4b8c-8c75-8dd336beead7`)
- `execution`: `{"async": false, "force_invoke_llm_on_result": false}`
- `hold_music`: estático, «holdacent» (asset `01a0fc02-a13d-77a2-8de3-82459eb2a2a6`), URL `<URL_FIRMADA>`

**message** (tipo `ai`). Ejemplo: «Lo entiendo. Le paso ahora mismo con un compañero que le va a ayudar. Puede tardar unos segundos, no cuelgue, por favor.» Descripción: igual que B2.

**Descripción:** Transfiere la llamada a la cola de agentes humanos que corresponda al MOTIVO del cliente. IMPORTANTE: en modo virtual (centro de atención cerrado) NO hay compañeros: no uses esta herramienta salvo para una avería o un accidente (cola de asistencia). Con el centro de atención abierto, úsala cuando: 1) el cliente va a llegar tarde y acepta que un compañero compruebe el servicio de espera, o quiere cambiar el día de devolución, 2) pregunta por un cargo concreto, el código de un parking, tiene problemas con Smartkey o pregunta algo del alquiler que no está en tus instrucciones, 3) necesita algo de su reserva, 4) tiene una avería o accidente, 5) todavía no tiene reserva y quiere alquilar un coche, 6) pregunta por el minibús o el punto de encuentro de un aeropuerto, 7) no se identifica la oficina o no hay datos y el cliente no lo resuelve, 8) está enfadado o pide hablar con una persona, 9) no puedes seguirle con fiabilidad por idioma. Ejecútala en el mismo turno en que decides transferir. Debes elegir SIEMPRE la extensión correcta según el motivo, usando la tabla del parámetro extension_destino, y rellenar siempre resumen_para_agente.

**Parámetros:**
- `extension_destino` (obligatorio): La extensión de la cola destino. Copia EXACTAMENTE uno de estos cuatro valores, sin inventar ni alterar ningún dígito. Pregunta por el minibús o el punto de encuentro de un aeropuerto, oficina no identificada o sin datos, cliente enfadado, petición genérica de hablar con una persona o idioma no soportado: `{{081e2b5d-b260-41a6-bd2a-6f82b26193d1.cola_horario_minibus}}`. Avería o accidente: `{{081e2b5d-b260-41a6-bd2a-6f82b26193d1.cola_asistencia}}`. Reserva existente (servicio de espera por vuelo o tren retrasado, cambiar el día de devolución, un cargo concreto, código de un parking, problemas con Smartkey, consultar un dato, preguntas del alquiler que no están en tus instrucciones): `{{081e2b5d-b260-41a6-bd2a-6f82b26193d1.cola_gestion_reserva}}`. Reserva nueva (todavía no tiene reserva y quiere alquilar, o pregunta precios o disponibilidad para un alquiler nuevo, aunque diga «reservar» o «mi reserva»): `{{081e2b5d-b260-41a6-bd2a-6f82b26193d1.cola_nueva_reserva}}`. Si dudas entre varias, usa la del minibús. Este parámetro es obligatorio: nunca lo dejes vacío ni lo rellenes con un texto genérico.
- `resumen_para_agente` (obligatorio): Resumen del motivo de la llamada que se le leerá en voz alta al compañero que recibe la transferencia, antes de conectarle con el cliente. SIEMPRE en español, aunque el cliente hable otro idioma. Una sola frase, de 10 a 25 palabras, en tercera persona, que diga qué quiere el cliente, de qué oficina habla y qué se ha intentado ya. Sin datos personales (nombre, reserva, matrícula, correo, teléfono), sin códigos, extensiones ni importes. Si el cliente habla otro idioma, añade al final 'El cliente habla inglés' (o el idioma que sea). Ejemplos: 'Cliente llega a Valencia aeropuerto después del cierre y quiere comprobar el servicio de espera.' 'Cliente pregunta por un cargo de parking en su alquiler de Madrid Atocha.'

## D. Prolongación y consultas (`38378785-0846-4920-b41a-583f7c5773fb`)

### D1. buscar_punto_de_encuentro

- persistent_id: `eda4aa10-c99e-4319-b7ae-dbf5dc6db949`
- Hijo: «Module Change» → «Punto de encuentro» (ver `module-change.md`)
- `message`: `{"type": "none"}`
- Parámetros `aeropuerto` y `terminal`: iguales que en A1.

**Descripción:** Úsala SOLO si el modo virtual es false (centro de atención abierto) y el cliente pregunta dónde se coge el minibús o cuál es el punto de encuentro en un aeropuerto, y ya sabes en qué aeropuerto está o va a estar. Sirve para darle el punto de encuentro del minibús. NO la uses en modo virtual: en ese caso sigue lo que dice MODO DE ATENCIÓN. NO la uses si el cliente se queja de que el minibús no llega, se ha ido sin él o lleva tiempo esperando: eso se transfiere a la cola de MINIBÚS. NO la uses para el horario, la dirección o dónde devolver el coche en una oficina: para eso está informacion_oficina. NO la uses si todavía no sabes el aeropuerto: pregúntalo una vez, sin deducirlo. Nunca preguntes por la terminal solo para poder llamar a esta herramienta.

### D2. informacion_oficina

- persistent_id: `0be9b6d8-9353-41de-8049-c2e477ed6668`
- Hijo: «Module Change» → «Información de oficina» (ver `module-change.md`)
- `message`: `{"type": "none"}`
- Parámetros `tema` y `oficina`: iguales que en A3.

**Descripción:** Úsala cuando el cliente quiera saber el horario de una oficina de Centauro, cómo llegar a una oficina de estación o de ciudad, o dónde devolver el coche. Sirve a cualquier hora, también en modo virtual. NO la uses para el minibús ni para el punto de encuentro de un aeropuerto: para eso está buscar_punto_de_encuentro. No digas nada especial antes: la herramienta continúa la conversación.

### D3. transfer_to_human_agent

- persistent_id: `fbe2e40e-4915-4f44-9bac-59c318862e97`
- Hijo: «Initiate customer connection» (`1dce23f2-c76c-4bfc-afbc-a1675318c082`)
- `execution`: `{"async": false, "force_invoke_llm_on_result": false}`
- `hold_music`: estático, «holdacent» (asset `01a0fc02-a13d-77a2-8de3-82459eb2a2a6`), URL `<URL_FIRMADA>`

**message** (tipo `ai`). Ejemplo: «Le paso con un compañero que le ayuda. Puede tardar unos segundos, no cuelgue, por favor.» Descripción: Informa al cliente, en su idioma, de que le vas a pasar con un compañero que le va a ayudar. Sé breve y tranquilizador. Termina SIEMPRE avisando de que puede tardar unos segundos en atenderle y pidiéndole que no cuelgue (por ejemplo: "puede tardar unos segundos, no cuelgue, por favor"). Si el cliente está molesto, frustrado o ya ha tenido que llamar varias veces, valida primero su emoción en una frase corta y sincera antes de anunciar la transferencia. Nunca anuncies la transferencia en seco a un cliente enfadado. No menciones colas, extensiones ni números. No prometas una oficina concreta ni un equipo específico.

**Descripción:** Transfiere la llamada a la cola de agentes humanos que corresponda al MOTIVO del cliente. IMPORTANTE: en modo virtual (centro de atención cerrado) NO hay compañeros: no uses esta herramienta salvo para una avería o un accidente (cola de asistencia). Úsala SOLO cuando el cliente necesita a una persona y no basta con la información de tus instrucciones (EXPLICACIÓN, DEVOLVER TARDE, COCHE DE ASEGURADORA O DE EMPRESA, DETALLES QUE PUEDES DAR, LA WEB NO LE DEJA, CONSULTAS FRECUENTES): si la respuesta está ahí, dala primero. Casos: 1) pregunta un dato de su reserva concreta (hora de devolución, días que lleva, si puede prolongar en su caso, correo); 2) la web sigue fallando tras probar las alternativas, el correo de contraseña sigue sin llegar tras comprobarlo, o tras dos intentos no encuentra la opción; 3) el coche no está disponible y quiere que alguien lo revise; 4) después de darle el canal de reclamaciones, quiere que alguien revise ahora un cargo, una penalización o un reembolso concreto; 5) reserva aún no iniciada que prefiere que cambie o cancele un compañero; 6) reclamación que quiere hacer hablando con alguien, cliente enfadado, o cliente que sigue pidiendo una persona después de preguntarle qué necesita; 7) llama una aseguradora, mutua, empresa de asistencia, agencia, partner o gestor de empresa; 8) el cliente PIDE hacer una reserva nueva o ha ACEPTADO que un compañero se la prepare; 9) avería o accidente; 10) pregunta por el minibús, el punto de encuentro o los datos de una oficina concreta; 11) el cliente habla un idioma que no atendemos; 12) quiere comprobar hoy el servicio de espera, se ha dejado algo en el coche, o cualquier otra gestión que no esté en tus instrucciones. Si la grúa municipal se ha llevado el coche, da el teléfono de asistencia y ofrece pasarle con asistencia; transfiere a la cola de asistencia solo si dice que sí. Un cliente con coche de aseguradora, de mutua o de empresa NO se transfiere por ese motivo. Cuando TÚ ofreces una reserva nueva o pasarle con un compañero, espera la respuesta del cliente antes de llamar a esta herramienta. Cuando la transferencia es obligatoria, ejecútala en el mismo turno en que la anuncias. Rellena siempre extension_destino, motivo_transferencia y resumen_para_agente.

**Parámetros:**
- `extension_destino` (obligatorio): La extensión de la cola destino. Copia EXACTAMENTE uno de estos cuatro valores, sin inventar ni alterar ningún carácter. Minibús, punto de encuentro o datos de una oficina concreta (horario, dirección, dónde se devuelve), o idioma que no atendemos: `{{081e2b5d-b260-41a6-bd2a-6f82b26193d1.cola_horario_minibus}}`. Avería o accidente: `{{081e2b5d-b260-41a6-bd2a-6f82b26193d1.cola_asistencia}}`. Gestión de una reserva (dato de su reserva concreta, error de la web que sigue tras probar las alternativas, correo de contraseña que sigue sin llegar, coche no disponible y quiere que alguien lo revise, cargo, penalización o reembolso concreto que quiere que alguien revise ahora, reserva no iniciada que prefiere que cambie o cancele un compañero, servicio de espera por vuelo o tren, objetos olvidados, reclamación, cliente enfadado, cliente que sigue pidiendo una persona, llamadas de aseguradoras, mutuas, asistencias, agencias, partners o gestores de empresa, cualquier otra gestión que no esté en tus instrucciones): `{{081e2b5d-b260-41a6-bd2a-6f82b26193d1.cola_gestion_reserva}}`. Reserva nueva (el cliente quiere HACER UNA RESERVA NUEVA o un alquiler nuevo, tanto si lo pide él como si acepta que un compañero se la prepare; también si quiere otro coche distinto): `{{081e2b5d-b260-41a6-bd2a-6f82b26193d1.cola_nueva_reserva}}`. Una reserva nueva NUNCA va a gestión de reserva. Si dudas entre varias (y no es una reserva nueva), usa la de gestión de reserva. Este parámetro es obligatorio: nunca lo dejes vacío ni lo rellenes con un texto genérico.
- `motivo_transferencia` (obligatorio): Motivo de la transferencia. Usa EXACTAMENTE uno de estos valores: no_iniciada, web_no_disponible, pregunta_reserva_concreta, aseguradora, enfado, error_tecnico, minibus, asistencia, nueva_reserva, otro. minibus incluye el punto de encuentro, los datos de una oficina concreta y un idioma que no atendemos. Si el motivo es nueva_reserva, extension_destino debe ser la cola de reserva nueva.
- `resumen_para_agente` (obligatorio): Resumen del motivo de la llamada que se le leerá en voz alta al compañero que recibe la transferencia, antes de conectarle con el cliente. SIEMPRE en español, aunque el cliente hable otro idioma. Una sola frase, de 10 a 25 palabras, en tercera persona, que diga qué quiere el cliente y qué se ha intentado ya. Sin datos personales (nombre, reserva, matrícula, correo, teléfono), sin códigos de motivo, extensiones ni importes. Si el cliente habla otro idioma, añade al final 'El cliente habla inglés' (o el idioma que sea). Ejemplos: 'Cliente quiere prolongar pero el pago falla en la web; ya ha probado la app y otra tarjeta.' 'Cliente con pinchazo en carretera, necesita asistencia.' 'Cliente quiere adelantar la recogida de una reserva que aún no ha empezado.'
