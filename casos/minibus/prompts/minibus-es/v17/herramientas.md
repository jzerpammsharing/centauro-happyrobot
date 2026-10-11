<!-- workflow: 019f7594-2cce-7eed-b995-dd9ea64a1062 · versión: v17 (i0syf61bujsz) · nodo: buscar_punto_de_encuentro, informacion_oficina, transfer_to_human_agent (Triaje y horario), transfer_to_human_agent (Punto de encuentro), transfer_to_human_agent (Información de oficina) · copiado: 2026-10-11 -->

# Herramientas (v17)

Las variables Plate se escriben como `{{persistent_id.variable}}`. Los persistent_id no cambian
entre v17 y v22, así que no ha hecho falta sustituirlos. Los `tool_index_id` / `tool_index_hash`
son internos de cada versión y se omiten.

## 1. buscar_punto_de_encuentro

- persistent_id: `8c1ce1ec-a026-4eb6-ac92-59a7f7046e4b`

### Descripción

Úsala cuando ya sabes en qué aeropuerto está el cliente Y el valor de horario nocturno de su lista es false (no está en horario nocturno). Sirve para consultar y darle el punto de encuentro del minibús. NO la uses si el valor de su lista es true: en ese caso hay que transferir con transfer_to_human_agent. NO la uses si todavía no sabes el aeropuerto. Nunca preguntes por la terminal solo para poder llamar a esta herramienta: la terminal es opcional y la consulta funciona sin ella.

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

Transfiere la llamada a la cola de agentes humanos que corresponda al MOTIVO del cliente. IMPORTANTE: en modo virtual (centro de atención cerrado) NO hay compañeros: no uses esta herramienta salvo para una avería o un accidente (cola de asistencia). Con el centro de atención abierto, úsala cuando: 1) el cliente tiene una avería o accidente, 2) el cliente necesita algo de su reserva (cambiar, cancelar, facturación, consultar un dato, un retraso o un cambio de devolución), 3) el cliente quiere hacer una reserva nueva, 4) el cliente está enfadado o tiene una queja real del minibús (se fue sin él, lleva mucho esperando, quiere reclamar), 5) el cliente pide hablar con una persona sin dar motivo, 6) el cliente sigue perdido tras tus indicaciones, 7) no puedes seguir al cliente con fiabilidad por idioma. Debes elegir SIEMPRE la extensión correcta según el motivo, usando la tabla del parámetro extension_destino.

### Parámetros

- `extension_destino` (obligatorio): La extensión de la cola destino. Copia EXACTAMENTE uno de estos cuatro valores, sin inventar ni alterar ningún dígito. Queja o problema del minibús (se fue sin él, aún no pasa, mucha espera), cliente perdido, petición genérica de hablar con una persona o idioma no soportado: {{019feb2c-0554-7b99-a980-42f896779230.cola_horario_minibus}}. Avería o accidente: {{019feb2c-0554-7b99-a980-42f896779230.cola_asistencia}}. Gestión de una reserva existente (cambios, cancelaciones, facturación, consultar un dato, retrasos, cambios de devolución): {{019feb2c-0554-7b99-a980-42f896779230.cola_gestion_reserva}}. Reserva nueva: {{019feb2c-0554-7b99-a980-42f896779230.cola_nueva_reserva}}. Si dudas entre varias, usa la del minibús. Este parámetro es obligatorio: nunca lo dejes vacío ni lo rellenes con un texto genérico.

### Mensaje (type: ai)

- Descripción: Informa al cliente, en su idioma, de que le vas a pasar con un compañero que le va a ayudar. Sé breve y tranquilizador. Si el cliente está molesto, frustrado o ya ha tenido que insistir para que le pases con alguien, valida primero su emoción en una frase corta y sincera antes de anunciar la transferencia: reconoce la molestia concreta que te ha expresado, sin excusas largas ni justificaciones. Nunca anuncies la transferencia en seco a un cliente enfadado. No menciones colas, extensiones ni números. No prometas una oficina concreta ni un equipo específico.
- Ejemplo: «Entiendo su enfado, y siento que haya tenido que esperar tanto. Le paso ahora mismo con un compañero que le va a ayudar. Un momento, por favor.»

### Configuración

```json
{"message": {"type": "ai"}}
```

(Sin `execution`, sin `hold_music`.)

## 4. transfer_to_human_agent (fase «Punto de encuentro»)

- persistent_id: `09353184-6e92-450d-a8b2-94f556b356ae`

### Descripción

Transfiere la llamada a la cola de agentes humanos que corresponda al MOTIVO del cliente. IMPORTANTE: en modo virtual (centro de atención cerrado) NO hay compañeros: no uses esta herramienta salvo para una avería o un accidente (cola de asistencia). Con el centro de atención abierto, úsala cuando: 1) el cliente está enfadado o tiene una queja real del minibús (se fue sin él, aún no pasa, lleva esperando igual o más que la frecuencia de su aeropuerto, quiere reclamar), 2) el cliente sigue perdido tras darle la indicación una vez, 3) estás en Palma de Mallorca y el cliente no encuentra el punto, 4) el cliente tiene una avería o accidente, 5) el cliente necesita algo de su reserva (cambiar, cancelar, facturación, consultar un dato, un retraso o un cambio de devolución), 6) el cliente quiere hacer una reserva nueva, 7) el cliente pide hablar con una persona sin dar motivo, 8) no puedes seguir al cliente con fiabilidad por idioma. Debes elegir SIEMPRE la extensión correcta según el motivo, usando la tabla del parámetro extension_destino.

### Parámetros

- `extension_destino` (obligatorio): La extensión de la cola destino. Copia EXACTAMENTE uno de estos cuatro valores, sin inventar ni alterar ningún dígito. Queja o problema del minibús (se fue sin él, aún no pasa, mucha espera), cliente perdido, Palma de Mallorca, petición genérica de hablar con una persona o idioma no soportado: {{019feb2c-0554-7b99-a980-42f896779230.cola_horario_minibus}}. Avería o accidente: {{019feb2c-0554-7b99-a980-42f896779230.cola_asistencia}}. Gestión de una reserva existente (cambios, cancelaciones, facturación, consultar un dato, retrasos, cambios de devolución): {{019feb2c-0554-7b99-a980-42f896779230.cola_gestion_reserva}}. Reserva nueva: {{019feb2c-0554-7b99-a980-42f896779230.cola_nueva_reserva}}. Si dudas entre varias, usa la del minibús. Este parámetro es obligatorio: nunca lo dejes vacío ni lo rellenes con un texto genérico.

### Mensaje (type: ai)

- Descripción: Informa al cliente, en su idioma, de que le vas a pasar con un compañero que le va a ayudar. Sé breve y tranquilizador. Si el cliente está molesto, valida primero su enfado. No menciones colas, extensiones ni números. No prometas llamar al conductor ni a una oficina concreta.
- Ejemplo: «Lo entiendo, y tiene razón. Le paso ahora mismo con un compañero para que vea qué está pasando. Un momento, por favor.»

### Configuración

```json
{"message": {"type": "ai"}}
```

(Sin `execution`, sin `hold_music`.)

## 5. transfer_to_human_agent (fase «Información de oficina»)

- persistent_id: `01a103fb-1a54-7564-a74e-03cdc4d4a656`

### Descripción

Transfiere la llamada a la cola de agentes humanos que corresponda al MOTIVO del cliente. IMPORTANTE: en modo virtual (centro de atención cerrado) NO hay compañeros: no uses esta herramienta salvo para una avería o un accidente (cola de asistencia). Con el centro de atención abierto, úsala cuando: 1) el cliente va a llegar tarde, su vuelo o tren se retrasa, o quiere cambiar la hora, el día o la oficina de devolución, 2) pregunta por cargos, combustible, el código de un parking o tiene problemas con Smartkey, 3) necesita algo de su reserva, 4) tiene una avería o accidente, 5) quiere hacer una reserva nueva, 6) pregunta por el minibús o el punto de encuentro de un aeropuerto, 7) no se identifica la oficina o no hay datos y el cliente no lo resuelve, 8) está enfadado o pide hablar con una persona, 9) no puedes seguirle con fiabilidad por idioma. Debes elegir SIEMPRE la extensión correcta según el motivo, usando la tabla del parámetro extension_destino.

### Parámetros

- `extension_destino` (obligatorio): La extensión de la cola destino. Copia EXACTAMENTE uno de estos cuatro valores, sin inventar ni alterar ningún dígito. Pregunta por el minibús o el punto de encuentro de un aeropuerto, oficina no identificada o sin datos, cliente enfadado, petición genérica de hablar con una persona o idioma no soportado: {{019feb2c-0554-7b99-a980-42f896779230.cola_horario_minibus}}. Avería o accidente: {{019feb2c-0554-7b99-a980-42f896779230.cola_asistencia}}. Gestión de una reserva existente (llega tarde o su vuelo se retrasa, cambiar la hora, el día o la oficina de devolución, cargos, combustible, código de un parking, problemas con Smartkey, consultar un dato): {{019feb2c-0554-7b99-a980-42f896779230.cola_gestion_reserva}}. Reserva nueva: {{019feb2c-0554-7b99-a980-42f896779230.cola_nueva_reserva}}. Si dudas entre varias, usa la del minibús. Este parámetro es obligatorio: nunca lo dejes vacío ni lo rellenes con un texto genérico.

### Mensaje (type: ai)

- Descripción: Informa al cliente, en su idioma, de que le vas a pasar con un compañero que le va a ayudar. Sé breve y tranquilizador. Si el cliente está molesto, valida primero su enfado. No menciones colas, extensiones ni números. No prometas llamar al conductor ni a una oficina concreta.
- Ejemplo: «Lo entiendo. Le paso ahora mismo con un compañero que le va a ayudar. Un momento, por favor.»

### Configuración

```json
{"message": {"type": "ai"}}
```

(Sin `execution`, sin `hold_music`.)
