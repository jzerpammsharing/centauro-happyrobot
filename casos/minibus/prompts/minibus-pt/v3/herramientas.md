<!-- workflow: 01a05977-3a33-76da-acb2-a757f3947cf9 · versión: v3 (2139o3pf25qm) · nodo: buscar_punto_de_encuentro, transfer_to_human_agent (Triaje y horario), transfer_to_human_agent (Punto de encuentro) · copiado: 2026-10-12 -->

# Herramientas (v3)

Variables Plate escritas como `{{persistent_id.variable}}`.

## buscar_punto_de_encuentro

- persistent_id: `cadf6598-45fa-48e2-8e0e-a205b3faf7cd`

### Descripción

Úsala cuando ya sabes en qué aeropuerto está el cliente Y el valor de su lista es false (la oficina de ese aeropuerto sigue abierta). Sirve para consultar y darle el punto de encuentro del minibús. Úsala también, sea cual sea el valor, si pregunta por el horario de la oficina de ese aeropuerto o por dónde devolver el coche allí. NO la uses para el minibús si el valor de su lista es true: en ese caso la oficina ya ha cerrado y solo se avisa del cierre y de la hora de apertura (Paso 3). NO la uses si el cliente se queja de que el minibús no llega, se ha ido sin él o lleva tiempo esperando: eso se transfiere a la cola de MINIBÚS. NO la uses para una oficina de estación o de ciudad, para prolongar, para un retraso ni para dudas del alquiler. NO la uses si todavía no sabes el aeropuerto. Nunca preguntes por la terminal solo para poder llamar a esta herramienta: la terminal es opcional y la consulta funciona sin ella.

### Parámetros

- `aeropuerto` (obligatorio): Nombre del aeropuerto donde se encuentra el cliente o por el que pregunta, tal como lo ha dicho (por ejemplo: Lisboa, Oporto, Faro, Madeira, Madrid).
- `terminal` (opcional): Terminal o puerta de salida, SOLO si el cliente la ha mencionado espontáneamente. Si el cliente no ha dicho la terminal, OMITE este parámetro por completo: no lo incluyas en la llamada y no lo envíes como texto vacío, ni con guiones, ni con valores como "no indicada" o "desconocida". Nunca deduzcas ni inventes una terminal, y nunca se la preguntes al cliente solo para rellenar este campo.

### Configuración

```json
{"message": {"type": "none"}}
```

## transfer_to_human_agent (fase «Triaje y horario»)

- persistent_id: `302bc6a5-b38f-4baf-9b2c-c62e533e3b2c`

### Descripción

Transfiere la llamada a la cola de agentes humanos que corresponda al MOTIVO del cliente. IMPORTANTE: en modo virtual (centro de atención cerrado) NO hay compañeros: no uses esta herramienta salvo para una avería o un accidente (cola de asistencia). Con el centro de atención abierto, úsala cuando: 1) el cliente tiene una avería o accidente, 2) necesita algo de su reserva, prolongarla, cambiar la devolución, tiene una duda sobre las condiciones del alquiler o va a llegar tarde a recoger, 3) todavía no tiene reserva y quiere alquilar un coche, 4) se queja del minibús (no llega, se fue sin él, lleva tiempo esperando, quiere reclamar), 5) pide hablar con una persona y, después de preguntarle una vez qué necesita, lo repite sin dar motivo, 6) pide datos de una oficina de estación o de ciudad, 7) no puedes seguir al cliente con fiabilidad por idioma. Ejecútala en el mismo turno en que decides transferir. Debes elegir SIEMPRE la extensión correcta según el motivo, usando la tabla del parámetro extension_destino, y rellenar siempre resumen_para_agente.

### Parámetros

- `extension_destino` (obligatorio): La extensión de la cola destino. Copia EXACTAMENTE uno de estos cuatro valores, sin inventar ni alterar ningún dígito. Queja o problema del minibús (se fue sin él, aún no pasa, mucha espera), cliente perdido, oficina de estación o de ciudad, petición de hablar con una persona sin motivo o idioma no soportado: {{96b01012-31c0-4328-9bb4-1650bcdbf1dc.cola_horario_minibus}}. Avería o accidente: {{96b01012-31c0-4328-9bb4-1650bcdbf1dc.cola_asistencia}}. Algo de una reserva existente (cambiar, cancelar, prolongar, cambiar la devolución, facturación, un cargo, consultar un dato), dudas sobre las condiciones del alquiler o retraso en la recogida: {{96b01012-31c0-4328-9bb4-1650bcdbf1dc.cola_gestion_reserva}}. Reserva nueva (todavía no tiene reserva y quiere alquilar, o pregunta precios o disponibilidad para un alquiler nuevo, aunque diga «reservar» o «mi reserva»): {{96b01012-31c0-4328-9bb4-1650bcdbf1dc.cola_nueva_reserva}}. Si dudas entre varias, usa la del minibús. Este parámetro es obligatorio: nunca lo dejes vacío ni lo rellenes con un texto genérico.
- `resumen_para_agente` (obligatorio): Resumen del motivo de la llamada que se le leerá en voz alta al compañero que recibe la transferencia, antes de conectarle con el cliente. SIEMPRE en portugués, aunque el cliente hable otro idioma. Una sola frase, de 10 a 25 palabras, en tercera persona, que diga qué quiere el cliente, en qué aeropuerto está si lo sabes y qué se ha intentado ya. Sin datos personales (nombre, reserva, matrícula, correo, teléfono), sin códigos, extensiones ni importes. Si el cliente habla otro idioma, añade al final 'O cliente fala inglês' (o el idioma que sea). Ejemplos: 'Cliente em Lisboa está à espera do minibus há vinte minutos e ainda não passou.' 'Cliente com um furo na estrada, precisa de assistência.' 'Cliente quer mudar a hora de devolução da sua reserva.'

### Mensaje (type: ai)

- Descripción: Informa al cliente, en su idioma, de que le vas a pasar con un compañero que le va a ayudar. Sé breve y tranquilizador. Termina SIEMPRE avisando de que puede tardar unos segundos en atenderle y pidiéndole que no cuelgue (por ejemplo: "puede tardar unos segundos, no cuelgue, por favor"). Si el cliente está molesto, frustrado o ya ha tenido que insistir para que le pases con alguien, valida primero su emoción en una frase corta y sincera antes de anunciar la transferencia: reconoce la molestia concreta que te ha expresado, sin excusas largas ni justificaciones. Nunca anuncies la transferencia en seco a un cliente enfadado. No menciones colas, extensiones ni números. No prometas una oficina concreta ni un equipo específico.
- Ejemplo: «Entiendo su enfado, y siento que haya tenido que esperar tanto. Le paso ahora mismo con un compañero que le va a ayudar. Puede tardar unos segundos, no cuelgue, por favor.»

### Configuración

```json
{"message": {"type": "ai"}, "execution": {"async": false, "force_invoke_llm_on_result": false}, "hold_music": {"type": "static", "static": {"id": "https://storage.googleapis.com/happyrobot-public/on-hold/acoustic.8k.wav", "name": "Acoustic"}}}
```

## transfer_to_human_agent (fase «Punto de encuentro»)

- persistent_id: `9e8601c0-cab7-49de-9590-785d03341d87`

### Descripción

Transfiere la llamada a la cola de agentes humanos que corresponda al MOTIVO del cliente. IMPORTANTE: en modo virtual (centro de atención cerrado) NO hay compañeros: no uses esta herramienta salvo para una avería o un accidente (cola de asistencia). Con el centro de atención abierto, úsala cuando: 1) el cliente está enfadado o tiene una queja real del minibús (se fue sin él, aún no pasa, lleva esperando igual o más que la frecuencia de su aeropuerto, quiere reclamar), 2) el cliente sigue perdido tras darle la indicación una vez, 3) estás en Palma de Mallorca y el cliente no encuentra el punto, 4) el cliente tiene una avería o accidente, 5) necesita algo de su reserva, prolongarla, cambiar la devolución, va a llegar tarde a recoger o tiene una duda sobre las condiciones del alquiler, 6) todavía no tiene reserva y quiere alquilar un coche, 7) el cliente pide hablar con una persona sin dar motivo, 8) no puedes seguir al cliente con fiabilidad por idioma, 9) pregunta algo que no está en tus instrucciones. Ejecútala en el mismo turno en que decides transferir. Debes elegir SIEMPRE la extensión correcta según el motivo, usando la tabla del parámetro extension_destino, y rellenar siempre resumen_para_agente.

### Parámetros

- `extension_destino` (obligatorio): La extensión de la cola destino. Copia EXACTAMENTE uno de estos cuatro valores, sin inventar ni alterar ningún dígito. Queja o problema del minibús (se fue sin él, aún no pasa, mucha espera), cliente perdido, Palma de Mallorca, oficina de estación o de ciudad, petición genérica de hablar con una persona, idioma no soportado o pregunta que no está en tus instrucciones: {{96b01012-31c0-4328-9bb4-1650bcdbf1dc.cola_horario_minibus}}. Avería o accidente: {{96b01012-31c0-4328-9bb4-1650bcdbf1dc.cola_asistencia}}. Reserva existente (algo que hay que mirar o cambiar, prolongar, cambiar el día o la oficina de devolución, retraso en la recogida, dudas sobre las condiciones del alquiler): {{96b01012-31c0-4328-9bb4-1650bcdbf1dc.cola_gestion_reserva}}. Reserva nueva (todavía no tiene reserva y quiere alquilar, o pregunta precios o disponibilidad para un alquiler nuevo, aunque diga «reservar» o «mi reserva»): {{96b01012-31c0-4328-9bb4-1650bcdbf1dc.cola_nueva_reserva}}. Si dudas entre varias, usa la del minibús. Este parámetro es obligatorio: nunca lo dejes vacío ni lo rellenes con un texto genérico.
- `resumen_para_agente` (obligatorio): Resumen del motivo de la llamada que se le leerá en voz alta al compañero que recibe la transferencia, antes de conectarle con el cliente. SIEMPRE en portugués, aunque el cliente hable otro idioma. Una sola frase, de 10 a 25 palabras, en tercera persona, que diga qué quiere el cliente, en qué aeropuerto y terminal está y qué se ha intentado ya. Sin datos personales (nombre, reserva, matrícula, correo, teléfono), sin códigos, extensiones ni importes. Si el cliente habla otro idioma, añade al final 'O cliente fala inglês' (o el idioma que sea). Ejemplos: 'Cliente no Porto está no ponto de encontro há vinte minutos e o minibus não passou.' 'Cliente em Faro não encontra o ponto de encontro depois da indicação.'

### Mensaje (type: ai)

- Descripción: Informa al cliente, en su idioma, de que le vas a pasar con un compañero que le va a ayudar. Sé breve y tranquilizador. Termina SIEMPRE avisando de que puede tardar unos segundos en atenderle y pidiéndole que no cuelgue (por ejemplo: "puede tardar unos segundos, no cuelgue, por favor"). Si el cliente está molesto, valida primero su enfado. No menciones colas, extensiones ni números. No prometas llamar al conductor ni a una oficina concreta.
- Ejemplo: «Lo entiendo, y tiene razón. Le paso ahora mismo con un compañero para que vea qué está pasando. Puede tardar unos segundos, no cuelgue, por favor.»

### Configuración

```json
{"message": {"type": "ai"}, "execution": {"async": false, "force_invoke_llm_on_result": false}, "hold_music": {"type": "static", "static": {"id": "https://storage.googleapis.com/happyrobot-public/on-hold/acoustic.8k.wav", "name": "Acoustic"}}}
```
