<!-- workflow: 01a03a65-3700-74c1-9c7b-e9c708833c4b · versión: v3 (jgkjecsoaxp4) · nodo: buscar_punto_de_encuentro, transfer_to_human_agent (Triaje y horario), transfer_to_human_agent (Punto de encuentro) · copiado: 2026-10-12 -->

# Herramientas (v3)

Variables Plate escritas como `{{persistent_id.variable}}`.

## buscar_punto_de_encuentro

- persistent_id: `6b61402c-932e-4061-a8e5-3dbc89d20a48`

### Descripción

Úsala cuando ya sabes en qué aeropuerto está el cliente Y el valor de su lista es false (la oficina de ese aeropuerto sigue abierta). Sirve para consultar y darle el punto de encuentro del minibús. Úsala también, sea cual sea el valor, si pregunta por el horario de la oficina de ese aeropuerto o por dónde devolver el coche allí. NO la uses para el minibús si el valor de su lista es true: en ese caso la oficina ya ha cerrado y solo se avisa del cierre y de la hora de apertura (Paso 3). NO la uses si el cliente se queja de que el minibús no llega, se ha ido sin él o lleva tiempo esperando: eso se transfiere a la cola de MINIBÚS. NO la uses para una oficina de estación o de ciudad, para prolongar, para un retraso ni para dudas del alquiler. NO la uses si todavía no sabes el aeropuerto. Nunca preguntes por la terminal solo para poder llamar a esta herramienta: la terminal es opcional y la consulta funciona sin ella.

### Parámetros

- `aeropuerto` (obligatorio): Nombre del aeropuerto donde se encuentra el cliente o por el que pregunta, tal como lo ha dicho (por ejemplo: Roma-Fiumicino, Milán-Malpensa, Nápoles, Venecia, Madrid).
- `terminal` (opcional): Terminal o puerta de salida, SOLO si el cliente la ha mencionado espontáneamente. Si el cliente no ha dicho la terminal, OMITE este parámetro por completo: no lo incluyas en la llamada y no lo envíes como texto vacío, ni con guiones, ni con valores como "no indicada" o "desconocida". Nunca deduzcas ni inventes una terminal, y nunca se la preguntes al cliente solo para rellenar este campo.

### Configuración

```json
{"message": {"type": "none"}}
```

## transfer_to_human_agent (fase «Triaje y horario»)

- persistent_id: `7a3776a5-7ee5-4031-81c7-0e3bd02c31c9`

### Descripción

Transfiere la llamada a la cola de agentes humanos que corresponda al MOTIVO del cliente. IMPORTANTE: en modo virtual (centro de atención cerrado) NO hay compañeros: no uses esta herramienta salvo para una avería o un accidente (cola de asistencia). Con el centro de atención abierto, úsala cuando: 1) el cliente tiene una avería o accidente, 2) necesita algo de su reserva, prolongarla, cambiar la devolución, tiene una duda sobre las condiciones del alquiler o va a llegar tarde a recoger, 3) todavía no tiene reserva y quiere alquilar un coche, 4) se queja del minibús (no llega, se fue sin él, lleva tiempo esperando, quiere reclamar), 5) pide hablar con una persona y, después de preguntarle una vez qué necesita, lo repite sin dar motivo, 6) pide datos de una oficina de estación o de ciudad, 7) no puedes seguir al cliente con fiabilidad por idioma. Ejecútala en el mismo turno en que decides transferir. Debes elegir SIEMPRE la extensión correcta según el motivo, usando la tabla del parámetro extension_destino, y rellenar siempre resumen_para_agente.

### Parámetros

- `extension_destino` (obligatorio): La extensión de la cola destino. Copia EXACTAMENTE uno de estos cuatro valores, sin inventar ni alterar ningún dígito. Queja o problema del minibús (se fue sin él, aún no pasa, mucha espera), cliente perdido, oficina de estación o de ciudad, petición de hablar con una persona sin motivo o idioma no soportado: {{4e0b9531-326f-4c5f-8f49-bbe460868570.cola_horario_minibus}}. Avería o accidente: {{4e0b9531-326f-4c5f-8f49-bbe460868570.cola_asistencia}}. Algo de una reserva existente (cambiar, cancelar, prolongar, cambiar la devolución, facturación, un cargo, consultar un dato), dudas sobre las condiciones del alquiler o retraso en la recogida: {{4e0b9531-326f-4c5f-8f49-bbe460868570.cola_gestion_reserva}}. Reserva nueva (todavía no tiene reserva y quiere alquilar, o pregunta precios o disponibilidad para un alquiler nuevo, aunque diga «reservar» o «mi reserva»): {{4e0b9531-326f-4c5f-8f49-bbe460868570.cola_nueva_reserva}}. Si dudas entre varias, usa la del minibús. Este parámetro es obligatorio: nunca lo dejes vacío ni lo rellenes con un texto genérico.
- `resumen_para_agente` (obligatorio): Resumen del motivo de la llamada que se le leerá en voz alta al compañero que recibe la transferencia, antes de conectarle con el cliente. SIEMPRE en italiano, aunque el cliente hable otro idioma. Una sola frase, de 10 a 25 palabras, en tercera persona, que diga qué quiere el cliente, en qué aeropuerto está si lo sabes y qué se ha intentado ya. Sin datos personales (nombre, reserva, matrícula, correo, teléfono), sin códigos, extensiones ni importes. Si el cliente habla otro idioma, añade al final 'Il cliente parla inglese' (o el idioma que sea). Ejemplos: 'Cliente a Roma Fiumicino aspetta il minibus da venti minuti e non è ancora passato.' 'Cliente con una foratura in strada, ha bisogno di assistenza.' 'Cliente vuole cambiare l'orario di riconsegna della sua prenotazione.'

### Mensaje (type: ai)

- Descripción: Informa al cliente, en su idioma, de que le vas a pasar con un compañero que le va a ayudar. Sé breve y tranquilizador. Termina SIEMPRE avisando de que puede tardar unos segundos en atenderle y pidiéndole que no cuelgue (por ejemplo: "puede tardar unos segundos, no cuelgue, por favor"). Si el cliente está molesto, frustrado o ya ha tenido que insistir para que le pases con alguien, valida primero su emoción en una frase corta y sincera antes de anunciar la transferencia: reconoce la molestia concreta que te ha expresado, sin excusas largas ni justificaciones. Nunca anuncies la transferencia en seco a un cliente enfadado. No menciones colas, extensiones ni números. No prometas una oficina concreta ni un equipo específico.
- Ejemplo: «Entiendo su enfado, y siento que haya tenido que esperar tanto. Le paso ahora mismo con un compañero que le va a ayudar. Puede tardar unos segundos, no cuelgue, por favor.»

### Configuración

```json
{"message": {"type": "ai"}, "execution": {"async": false, "force_invoke_llm_on_result": false}, "hold_music": {"type": "static", "static": {"id": "https://storage.googleapis.com/happyrobot-public/on-hold/acoustic.8k.wav", "name": "Acoustic"}}}
```

## transfer_to_human_agent (fase «Punto de encuentro»)

- persistent_id: `d37cbb84-a6a7-4dc6-928e-03c871087eef`

### Descripción

Transfiere la llamada a la cola de agentes humanos que corresponda al MOTIVO del cliente. IMPORTANTE: en modo virtual (centro de atención cerrado) NO hay compañeros: no uses esta herramienta salvo para una avería o un accidente (cola de asistencia). Con el centro de atención abierto, úsala cuando: 1) el cliente está enfadado o tiene una queja real del minibús (se fue sin él, aún no pasa, lleva esperando igual o más que la frecuencia de su aeropuerto, quiere reclamar), 2) el cliente sigue perdido tras darle la indicación una vez, 3) estás en Palma de Mallorca y el cliente no encuentra el punto, 4) el cliente tiene una avería o accidente, 5) necesita algo de su reserva, prolongarla, cambiar la devolución, va a llegar tarde a recoger o tiene una duda sobre las condiciones del alquiler, 6) todavía no tiene reserva y quiere alquilar un coche, 7) el cliente pide hablar con una persona sin dar motivo, 8) no puedes seguir al cliente con fiabilidad por idioma, 9) pregunta algo que no está en tus instrucciones. Ejecútala en el mismo turno en que decides transferir. Debes elegir SIEMPRE la extensión correcta según el motivo, usando la tabla del parámetro extension_destino, y rellenar siempre resumen_para_agente.

### Parámetros

- `extension_destino` (obligatorio): La extensión de la cola destino. Copia EXACTAMENTE uno de estos cuatro valores, sin inventar ni alterar ningún dígito. Queja o problema del minibús (se fue sin él, aún no pasa, mucha espera), cliente perdido, Palma de Mallorca, oficina de estación o de ciudad, petición genérica de hablar con una persona, idioma no soportado o pregunta que no está en tus instrucciones: {{4e0b9531-326f-4c5f-8f49-bbe460868570.cola_horario_minibus}}. Avería o accidente: {{4e0b9531-326f-4c5f-8f49-bbe460868570.cola_asistencia}}. Reserva existente (algo que hay que mirar o cambiar, prolongar, cambiar el día o la oficina de devolución, retraso en la recogida, dudas sobre las condiciones del alquiler): {{4e0b9531-326f-4c5f-8f49-bbe460868570.cola_gestion_reserva}}. Reserva nueva (todavía no tiene reserva y quiere alquilar, o pregunta precios o disponibilidad para un alquiler nuevo, aunque diga «reservar» o «mi reserva»): {{4e0b9531-326f-4c5f-8f49-bbe460868570.cola_nueva_reserva}}. Si dudas entre varias, usa la del minibús. Este parámetro es obligatorio: nunca lo dejes vacío ni lo rellenes con un texto genérico.
- `resumen_para_agente` (obligatorio): Resumen del motivo de la llamada que se le leerá en voz alta al compañero que recibe la transferencia, antes de conectarle con el cliente. SIEMPRE en italiano, aunque el cliente hable otro idioma. Una sola frase, de 10 a 25 palabras, en tercera persona, que diga qué quiere el cliente, en qué aeropuerto y terminal está y qué se ha intentado ya. Sin datos personales (nombre, reserva, matrícula, correo, teléfono), sin códigos, extensiones ni importes. Si el cliente habla otro idioma, añade al final 'Il cliente parla inglese' (o el idioma que sea). Ejemplos: 'Cliente a Milano Malpensa T1 è al punto d'incontro da venti minuti e il minibus non è passato.' 'Cliente a Napoli non trova il punto d'incontro dopo l'indicazione.'

### Mensaje (type: ai)

- Descripción: Informa al cliente, en su idioma, de que le vas a pasar con un compañero que le va a ayudar. Sé breve y tranquilizador. Termina SIEMPRE avisando de que puede tardar unos segundos en atenderle y pidiéndole que no cuelgue (por ejemplo: "puede tardar unos segundos, no cuelgue, por favor"). Si el cliente está molesto, valida primero su enfado. No menciones colas, extensiones ni números. No prometas llamar al conductor ni a una oficina concreta.
- Ejemplo: «Lo entiendo, y tiene razón. Le paso ahora mismo con un compañero para que vea qué está pasando. Puede tardar unos segundos, no cuelgue, por favor.»

### Configuración

```json
{"message": {"type": "ai"}, "execution": {"async": false, "force_invoke_llm_on_result": false}, "hold_music": {"type": "static", "static": {"id": "https://storage.googleapis.com/happyrobot-public/on-hold/acoustic.8k.wav", "name": "Acoustic"}}}
```
