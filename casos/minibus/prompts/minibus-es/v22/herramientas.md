<!-- workflow: 019f7594-2cce-7eed-b995-dd9ea64a1062 · versión: v22 (2l6skwt8wphb) · nodo: buscar_punto_de_encuentro, informacion_oficina, transfer_to_human_agent (Triaje y horario), transfer_to_human_agent (Punto de encuentro), transfer_to_human_agent (Información de oficina) · copiado: 2026-10-11 -->

# Herramientas (v22)

Las variables Plate se escriben como `{{persistent_id.variable}}`. Los persistent_id no cambian
entre v17 y v22, así que no ha hecho falta sustituirlos. Los `tool_index_id` / `tool_index_hash`
son internos de cada versión y se omiten. En la URL firmada de la música de espera «holdacent»
se ha sustituido la query string (cuenta de servicio y firma) por [REDACTADO].

## 1. buscar_punto_de_encuentro

- persistent_id: `8c1ce1ec-a026-4eb6-ac92-59a7f7046e4b`

### Descripción

Úsala cuando ya sabes en qué aeropuerto está el cliente Y el valor de su lista es false (la oficina de ese aeropuerto sigue abierta). Sirve para consultar y darle el punto de encuentro del minibús. NO la uses si el valor de su lista es true: en ese caso la oficina ya ha cerrado y solo se avisa del cierre y de la hora de apertura (Paso 3). NO la uses si el cliente se queja de que el minibús no llega, se ha ido sin él o lleva tiempo esperando: eso se transfiere a la cola de MINIBÚS. NO la uses si pregunta por el horario de una oficina o por dónde devolver el coche: para eso está informacion_oficina. NO la uses para prolongar, para un retraso o para dudas del alquiler: para eso está consultas_alquiler. NO la uses si todavía no sabes el aeropuerto. Nunca preguntes por la terminal solo para poder llamar a esta herramienta: la terminal es opcional y la consulta funciona sin ella.

### Parámetros

- `aeropuerto` (obligatorio): Nombre del aeropuerto donde se encuentra el cliente, tal como lo ha dicho (por ejemplo: Valencia, Rodas, Lisboa, Madrid).
- `terminal` (opcional): Terminal o puerta de salida, SOLO si el cliente la ha mencionado espontáneamente. Si el cliente no ha dicho la terminal, OMITE este parámetro por completo: no lo incluyas en la llamada y no lo envíes como texto vacío, ni con guiones, ni con valores como "no indicada" o "desconocida". Nunca deduzcas ni inventes una terminal, y nunca se la preguntes al cliente solo para rellenar este campo.

### Configuración

```json
{"message": {"type": "none"}}
```

## 2. informacion_oficina

- persistent_id: `01a103f3-3c08-75cc-bd0b-8163c6ea8af8`

### Descripción

Úsala cuando el cliente quiera saber el horario de una oficina de Centauro, cómo llegar a una oficina de estación o de ciudad, o dónde devolver el coche. Sirve a cualquier hora, también en horario nocturno. NO la uses para el minibús ni para el punto de encuentro de un aeropuerto: para eso está buscar_punto_de_encuentro.

### Parámetros

- `tema` (obligatorio): Lo que quiere saber el cliente. Valores permitidos EXACTOS: "horario" (horario de la oficina), "como_llegar" (cómo llegar a una oficina de estación o de ciudad para recoger el coche), "devolucion" (dónde devolver el coche). Si pregunta por varias cosas, pon la primera que haya pedido.
- `oficina` (opcional): La oficina, ciudad, estación o aeropuerto tal como lo ha dicho el cliente (por ejemplo: Málaga estación, Atocha, Madrid, Alicante aeropuerto). Si el cliente todavía no lo ha dicho, OMITE este parámetro por completo: no lo envíes vacío ni con valores como "desconocida". Nunca lo deduzcas ni lo preguntes solo para rellenarlo: la herramienta se encarga de identificar la oficina.

### Configuración

```json
{"message": {"type": "none"}}
```

## 3. transfer_to_human_agent (fase «Triaje y horario»)

- persistent_id: `019f8461-4b58-75df-9ea4-7569ab2dc75b`

### Descripción

Transfiere la llamada a la cola de agentes humanos que corresponda al MOTIVO del cliente. IMPORTANTE: en modo virtual (centro de atención cerrado) NO hay compañeros: no uses esta herramienta salvo para una avería o un accidente (cola de asistencia). Con el centro de atención abierto, úsala cuando: 1) el cliente tiene una avería o accidente, 2) necesita que alguien mire o cambie un dato concreto de su reserva, 3) todavía no tiene reserva y quiere alquilar un coche, 4) se queja del minibús (no llega, se fue sin él, lleva tiempo esperando, quiere reclamar), 5) pide hablar con una persona y, después de preguntarle una vez qué necesita, lo repite sin dar motivo, 6) no puedes seguir al cliente con fiabilidad por idioma. Las prolongaciones, los retrasos y las dudas generales del alquiler NO se transfieren desde aquí: van a consultas_alquiler. Ejecútala en el mismo turno en que decides transferir. Debes elegir SIEMPRE la extensión correcta según el motivo, usando la tabla del parámetro extension_destino, y rellenar siempre resumen_para_agente.

### Parámetros

- `extension_destino` (obligatorio): La extensión de la cola destino. Copia EXACTAMENTE uno de estos cuatro valores, sin inventar ni alterar ningún dígito. Queja o problema del minibús (se fue sin él, aún no pasa, mucha espera), cliente perdido, petición de hablar con una persona sin motivo o idioma no soportado: {{019feb2c-0554-7b99-a980-42f896779230.cola_horario_minibus}}. Avería o accidente: {{019feb2c-0554-7b99-a980-42f896779230.cola_asistencia}}. Un dato concreto de una reserva existente que hay que mirar o cambiar: {{019feb2c-0554-7b99-a980-42f896779230.cola_gestion_reserva}}. Reserva nueva (todavía no tiene reserva y quiere alquilar, o pregunta precios o disponibilidad para un alquiler nuevo, aunque diga «reservar» o «mi reserva»): {{019feb2c-0554-7b99-a980-42f896779230.cola_nueva_reserva}}. Si dudas entre varias, usa la del minibús. Este parámetro es obligatorio: nunca lo dejes vacío ni lo rellenes con un texto genérico.
- `resumen_para_agente` (obligatorio): Resumen del motivo de la llamada que se le leerá en voz alta al compañero que recibe la transferencia, antes de conectarle con el cliente. SIEMPRE en español, aunque el cliente hable otro idioma. Una sola frase, de 10 a 25 palabras, en tercera persona, que diga qué quiere el cliente, en qué aeropuerto u oficina está si lo sabes y qué se ha intentado ya. Sin datos personales (nombre, reserva, matrícula, correo, teléfono), sin códigos, extensiones ni importes. Si el cliente habla otro idioma, añade al final 'El cliente habla inglés' (o el idioma que sea). Ejemplos: 'Cliente en Madrid T4 lleva veinte minutos esperando el minibús y no ha pasado.' 'Cliente con pinchazo en carretera, necesita asistencia.' 'Cliente quiere cambiar la hora de devolución de su reserva.'

### Mensaje (type: ai)

- Descripción: Informa al cliente, en su idioma, de que le vas a pasar con un compañero que le va a ayudar. Sé breve y tranquilizador. Termina SIEMPRE avisando de que puede tardar unos segundos en atenderle y pidiéndole que no cuelgue (por ejemplo: "puede tardar unos segundos, no cuelgue, por favor"). Si el cliente está molesto, frustrado o ya ha tenido que insistir para que le pases con alguien, valida primero su emoción en una frase corta y sincera antes de anunciar la transferencia: reconoce la molestia concreta que te ha expresado, sin excusas largas ni justificaciones. Nunca anuncies la transferencia en seco a un cliente enfadado. No menciones colas, extensiones ni números. No prometas una oficina concreta ni un equipo específico.
- Ejemplo: «Entiendo su enfado, y siento que haya tenido que esperar tanto. Le paso ahora mismo con un compañero que le va a ayudar. Puede tardar unos segundos, no cuelgue, por favor.»

### Configuración

```json
{
  "message": {"type": "ai"},
  "execution": {"async": false, "force_invoke_llm_on_result": false},
  "hold_music": {
    "type": "static",
    "static": {
      "id": "https://storage.googleapis.com/happyrobot-public/on-hold/acoustic.8k.wav",
      "name": "Acoustic"
    }
  }
}
```

## 4. transfer_to_human_agent (fase «Punto de encuentro»)

- persistent_id: `09353184-6e92-450d-a8b2-94f556b356ae`

### Descripción

Transfiere la llamada a la cola de agentes humanos que corresponda al MOTIVO del cliente. IMPORTANTE: en modo virtual (centro de atención cerrado) NO hay compañeros: no uses esta herramienta salvo para una avería o un accidente (cola de asistencia). Con el centro de atención abierto, úsala cuando: 1) el cliente está enfadado o tiene una queja real del minibús (se fue sin él, aún no pasa, lleva esperando igual o más que la frecuencia de su aeropuerto, quiere reclamar), 2) el cliente sigue perdido tras darle la indicación una vez, 3) estás en Palma de Mallorca y el cliente no encuentra el punto, 4) el cliente tiene una avería o accidente, 5) necesita que alguien mire o cambie algo de su reserva, pregunta algo del alquiler que no está en tus instrucciones, o acepta que un compañero compruebe el servicio de espera, 6) todavía no tiene reserva y quiere alquilar un coche, 7) el cliente pide hablar con una persona sin dar motivo, 8) no puedes seguir al cliente con fiabilidad por idioma, 9) pregunta algo que no está en tus instrucciones. Ejecútala en el mismo turno en que decides transferir. Debes elegir SIEMPRE la extensión correcta según el motivo, usando la tabla del parámetro extension_destino, y rellenar siempre resumen_para_agente.

### Parámetros

- `extension_destino` (obligatorio): La extensión de la cola destino. Copia EXACTAMENTE uno de estos cuatro valores, sin inventar ni alterar ningún dígito. Queja o problema del minibús (se fue sin él, aún no pasa, mucha espera), cliente perdido, Palma de Mallorca, petición genérica de hablar con una persona, idioma no soportado o pregunta que no está en tus instrucciones: {{019feb2c-0554-7b99-a980-42f896779230.cola_horario_minibus}}. Avería o accidente: {{019feb2c-0554-7b99-a980-42f896779230.cola_asistencia}}. Reserva existente (algo que hay que mirar o cambiar, servicio de espera por vuelo retrasado, cambio de día de devolución, preguntas del alquiler que no están en tus instrucciones): {{019feb2c-0554-7b99-a980-42f896779230.cola_gestion_reserva}}. Reserva nueva (todavía no tiene reserva y quiere alquilar, o pregunta precios o disponibilidad para un alquiler nuevo, aunque diga «reservar» o «mi reserva»): {{019feb2c-0554-7b99-a980-42f896779230.cola_nueva_reserva}}. Si dudas entre varias, usa la del minibús. Este parámetro es obligatorio: nunca lo dejes vacío ni lo rellenes con un texto genérico.
- `resumen_para_agente` (obligatorio): Resumen del motivo de la llamada que se le leerá en voz alta al compañero que recibe la transferencia, antes de conectarle con el cliente. SIEMPRE en español, aunque el cliente hable otro idioma. Una sola frase, de 10 a 25 palabras, en tercera persona, que diga qué quiere el cliente, en qué aeropuerto y terminal está y qué se ha intentado ya (por ejemplo, que ya recibió la indicación del punto de encuentro). Sin datos personales (nombre, reserva, matrícula, correo, teléfono), sin códigos, extensiones ni importes. Si el cliente habla otro idioma, añade al final 'El cliente habla inglés' (o el idioma que sea). Ejemplos: 'Cliente en Barcelona T1 lleva veinte minutos en el punto de encuentro y el minibús no ha pasado.' 'Cliente en Palma no encuentra el punto de encuentro tras darle la indicación.'

### Mensaje (type: ai)

- Descripción: Informa al cliente, en su idioma, de que le vas a pasar con un compañero que le va a ayudar. Sé breve y tranquilizador. Termina SIEMPRE avisando de que puede tardar unos segundos en atenderle y pidiéndole que no cuelgue (por ejemplo: "puede tardar unos segundos, no cuelgue, por favor"). Si el cliente está molesto, valida primero su enfado. No menciones colas, extensiones ni números. No prometas llamar al conductor ni a una oficina concreta.
- Ejemplo: «Lo entiendo, y tiene razón. Le paso ahora mismo con un compañero para que vea qué está pasando. Puede tardar unos segundos, no cuelgue, por favor.»

### Configuración

```json
{
  "message": {"type": "ai"},
  "execution": {"async": false, "force_invoke_llm_on_result": false},
  "hold_music": {
    "type": "static",
    "static": {
      "id": "https://storage.googleapis.com/happyrobot-audio-assets-eu/019d1ff1-108b-7b48-b8d0-a7011f552bfc/audio-assets/b5dc3128-6cc8-422d-b152-caf60cc80477.wav?[REDACTADO]",
      "name": "holdacent",
      "assetId": "01a0fc02-a13d-77a2-8de3-82459eb2a2a6",
      "description": "Custom ID: 01a0fc02-a13d-77a2-8de3-82459eb2a2a6"
    }
  },
  "hold_music_asset_id": "01a0fc02-a13d-77a2-8de3-82459eb2a2a6"
}
```

## 5. transfer_to_human_agent (fase «Información de oficina»)

- persistent_id: `01a103fb-1a54-7564-a74e-03cdc4d4a656`

### Descripción

Transfiere la llamada a la cola de agentes humanos que corresponda al MOTIVO del cliente. IMPORTANTE: en modo virtual (centro de atención cerrado) NO hay compañeros: no uses esta herramienta salvo para una avería o un accidente (cola de asistencia). Con el centro de atención abierto, úsala cuando: 1) el cliente va a llegar tarde y acepta que un compañero compruebe el servicio de espera, o quiere cambiar el día de devolución, 2) pregunta por un cargo concreto, el código de un parking, tiene problemas con Smartkey o pregunta algo del alquiler que no está en tus instrucciones, 3) necesita algo de su reserva, 4) tiene una avería o accidente, 5) todavía no tiene reserva y quiere alquilar un coche, 6) pregunta por el minibús o el punto de encuentro de un aeropuerto, 7) no se identifica la oficina o no hay datos y el cliente no lo resuelve, 8) está enfadado o pide hablar con una persona, 9) no puedes seguirle con fiabilidad por idioma. Ejecútala en el mismo turno en que decides transferir. Debes elegir SIEMPRE la extensión correcta según el motivo, usando la tabla del parámetro extension_destino, y rellenar siempre resumen_para_agente.

### Parámetros

- `extension_destino` (obligatorio): La extensión de la cola destino. Copia EXACTAMENTE uno de estos cuatro valores, sin inventar ni alterar ningún dígito. Pregunta por el minibús o el punto de encuentro de un aeropuerto, oficina no identificada o sin datos, cliente enfadado, petición genérica de hablar con una persona o idioma no soportado: {{019feb2c-0554-7b99-a980-42f896779230.cola_horario_minibus}}. Avería o accidente: {{019feb2c-0554-7b99-a980-42f896779230.cola_asistencia}}. Reserva existente (servicio de espera por vuelo o tren retrasado, cambiar el día de devolución, un cargo concreto, código de un parking, problemas con Smartkey, consultar un dato, preguntas del alquiler que no están en tus instrucciones): {{019feb2c-0554-7b99-a980-42f896779230.cola_gestion_reserva}}. Reserva nueva (todavía no tiene reserva y quiere alquilar, o pregunta precios o disponibilidad para un alquiler nuevo, aunque diga «reservar» o «mi reserva»): {{019feb2c-0554-7b99-a980-42f896779230.cola_nueva_reserva}}. Si dudas entre varias, usa la del minibús. Este parámetro es obligatorio: nunca lo dejes vacío ni lo rellenes con un texto genérico.
- `resumen_para_agente` (obligatorio): Resumen del motivo de la llamada que se le leerá en voz alta al compañero que recibe la transferencia, antes de conectarle con el cliente. SIEMPRE en español, aunque el cliente hable otro idioma. Una sola frase, de 10 a 25 palabras, en tercera persona, que diga qué quiere el cliente, de qué oficina habla y qué se ha intentado ya. Sin datos personales (nombre, reserva, matrícula, correo, teléfono), sin códigos, extensiones ni importes. Si el cliente habla otro idioma, añade al final 'El cliente habla inglés' (o el idioma que sea). Ejemplos: 'Cliente llega a Valencia aeropuerto después del cierre y quiere comprobar el servicio de espera.' 'Cliente pregunta por un cargo de parking en su alquiler de Madrid Atocha.'

### Mensaje (type: ai)

- Descripción: Informa al cliente, en su idioma, de que le vas a pasar con un compañero que le va a ayudar. Sé breve y tranquilizador. Termina SIEMPRE avisando de que puede tardar unos segundos en atenderle y pidiéndole que no cuelgue (por ejemplo: "puede tardar unos segundos, no cuelgue, por favor"). Si el cliente está molesto, valida primero su enfado. No menciones colas, extensiones ni números. No prometas llamar al conductor ni a una oficina concreta.
- Ejemplo: «Lo entiendo. Le paso ahora mismo con un compañero que le va a ayudar. Puede tardar unos segundos, no cuelgue, por favor.»

### Configuración

```json
{
  "message": {"type": "ai"},
  "execution": {"async": false, "force_invoke_llm_on_result": false},
  "hold_music": {
    "type": "static",
    "static": {
      "id": "https://storage.googleapis.com/happyrobot-audio-assets-eu/019d1ff1-108b-7b48-b8d0-a7011f552bfc/audio-assets/b5dc3128-6cc8-422d-b152-caf60cc80477.wav?[REDACTADO]",
      "name": "holdacent",
      "assetId": "01a0fc02-a13d-77a2-8de3-82459eb2a2a6",
      "description": "Custom ID: 01a0fc02-a13d-77a2-8de3-82459eb2a2a6"
    }
  },
  "hold_music_asset_id": "01a0fc02-a13d-77a2-8de3-82459eb2a2a6"
}
```
