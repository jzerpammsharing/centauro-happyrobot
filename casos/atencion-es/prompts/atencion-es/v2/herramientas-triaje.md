<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v2 (x8xd0llbdp3j) · nodo: herramientas (tool) del Triaje · copiado: 2026-10-18 -->

# Herramientas del Triaje (v2)

Las cinco herramientas del prompt «Triaje» (`c5a70932-117c-4360-9be8-adce260fe13e`). Un nodo `tool` solo define la
función que ve el agente; lo que pasa al ejecutarla lo hacen sus hijos.

- Fuente de las descripciones (R3): los marcadores `{{variable}}` se escriben al subir como
  `{{<persistent_id>.variable}}`. `{{gestion_abierta}}` es la salida de «Contexto de la llamada»
  (`e51cd732-f403-4ef7-95d4-490347960a93`).
- Persistent ID = ID de nodo en la v1 para las cuatro que vienen del duplicado; el de `prolongar_alquiler` es el
  del nodo creado en la v2.
- Música de espera «holdacent»: asset `01a0fc02-a13d-77a2-8de3-82459eb2a2a6`; la URL firmada del nodo se sustituye
  aquí por `<URL_FIRMADA>`.

## 1. buscar_punto_de_encuentro

- persistent_id: `72261523-5d3f-4830-ac36-67ab187d93ed`
- Hijo: prompt «Punto de encuentro» (sin cambios en esta tarea)
- `message`: `{"type": "none"}`

**Descripción:** Úsala cuando el cliente pregunta por el minibús, por el punto de encuentro o por cómo llegar del aeropuerto a la oficina de Centauro, y ya sabes en qué aeropuerto está. La herramienta continúa la conversación: da el punto de encuentro o avisa de que la oficina de ese aeropuerto ya ha cerrado. Sirve a cualquier hora, también en modo virtual. NO la uses si se queja de que el minibús no llega, se ha ido sin él o lleva tiempo esperando (salvo que lleve menos de diez minutos): eso se transfiere a la cola minibus. NO la uses para el horario, la dirección o la devolución en una oficina (informacion_oficina), ni para prolongar o para dudas del alquiler. Si todavía no sabes el aeropuerto, pregúntalo antes. Nunca preguntes la terminal solo para poder llamarla: es opcional.

> Ronda de arreglos 1 de la Tarea 9: se probó a añadir aquí la excepción del modo virtual («…salvo en modo virtual:
> entonces no transfieras; dile que a esta hora no hay compañeros…»). Con ella, VIRT-T1 (crítica) pasó de 3/3 a 0/3
> (el Triaje ejecutaba transfer_to_human_agent para una reserva nueva de noche); al quitarla volvió a 3/3. Se dejó sin
> la excepción, que sí está en la de Consultas. Detalle en `docs/informes/evals-v2.md`.

**Parámetros:**
- `aeropuerto` (obligatorio): Nombre del aeropuerto donde está el cliente, tal como lo ha dicho (por ejemplo: Valencia, Rodas, Lisboa, Madrid).
- `terminal` (opcional): Terminal o puerta de salida, SOLO si el cliente la ha mencionado espontáneamente. Si no la ha dicho, OMITE este parámetro por completo: no lo envíes vacío, con guiones ni con valores como "no indicada" o "desconocida". Nunca la deduzcas, la inventes ni la preguntes solo para rellenar este campo.

## 2. informacion_oficina

- persistent_id: `414b964d-bb29-428a-b9a1-92b1a3a8d6be`
- Hijo: prompt «Información de oficina» (sin cambios en esta tarea)
- `message`: `{"type": "none"}`

**Descripción:** Úsala cuando el cliente quiera saber el horario de una oficina de Centauro, cómo llegar a una oficina de estación o de ciudad, o dónde se devuelve el coche en una oficina. Sirve a cualquier hora, también en modo virtual. NO la uses para el minibús ni para el punto de encuentro de un aeropuerto (buscar_punto_de_encuentro). Devolver el coche antes de tiempo o en otra oficina distinta de la del contrato es una duda del alquiler: consultas_alquiler.

**Parámetros:**
- `tema` (obligatorio): Lo que quiere saber el cliente. Valores permitidos EXACTOS: "horario" (horario de la oficina), "como_llegar" (cómo llegar a una oficina de estación o de ciudad para recoger el coche), "devolucion" (dónde devolver el coche). Si pregunta por varias cosas, pon la primera que haya pedido.
- `oficina` (opcional): La oficina, ciudad, estación o aeropuerto tal como lo ha dicho el cliente (por ejemplo: Málaga estación, Atocha, Madrid, Alicante aeropuerto). Si todavía no lo ha dicho, OMITE este parámetro por completo: no lo envíes vacío ni con valores como "desconocida". Nunca lo deduzcas ni lo preguntes solo para rellenarlo: la herramienta se encarga de identificar la oficina.

## 3. prolongar_alquiler (nueva)

- persistent_id (= ID de nodo en la v2): `01a14f69-b092-7e6d-9203-c968520c1670`
- Hijo: prompt «Prolongación» (`01a14f69-b09d-7689-ad9e-8e8de0fd6fb4`). **Provisional** hasta la Tarea 10 (modelo
  `fast-gpt-5.4`, sin `initial_message`), con
  este texto de una línea: «Prompt provisional (lo sustituye la Tarea 10): dile al cliente, en su idioma y en una
  frase, que enseguida le ayudas con su alquiler y pregúntale cuántos días más necesita.»
- `message`: `{"type": "none"}`

**Descripción:** Úsala cuando el cliente quiere prolongar el alquiler que tiene en curso o devolver el coche más tarde, cuando la web no le deja prolongar, cuando no recuerda o no tiene la contraseña de su área de cliente en la web, o cuando su coche es de una aseguradora, de un taller o de su empresa. Sirve a cualquier hora, también en modo virtual y con gestión cerrada. En la línea de Prolongación, si al saludo responde que sí quiere prolongar, ejecútala en ese mismo turno, sin preguntar nada más. No digas nada antes: la herramienta continúa la conversación.

**Parámetros:**
- `situacion` (obligatorio): Lo que necesita el cliente. Valores permitidos EXACTOS: "prolongar" (quedarse el coche más días), "devolver_tarde" (devolverlo más tarde el mismo día), "web_no_deja" (la web no le deja prolongar), "contrasena" (no recuerda o no tiene la contraseña del área de cliente), "aseguradora_empresa" (coche de aseguradora, de taller o de empresa). Si dice varias cosas, pon la primera.

## 4. consultas_alquiler

- persistent_id: `414bdc8c-aacc-4125-b323-acc6a2ae3373`
- Hijo: prompt «Prolongación y consultas» (pasa a «Consultas del alquiler» en la Tarea 9)
- `message`: `{"type": "none"}`

**Descripción:** Úsala para cualquier otra duda sobre su alquiler o sobre las condiciones de Centauro: cancelar, cambiar o adelantar una reserva que aún no ha empezado; llegar tarde a recoger (vuelo o tren retrasado); devolver antes, en otra oficina o con la oficina cerrada; fianza, combustible, cargos, multas, facturas o reembolsos; requisitos (carnet, edad, documentos, tarjeta, conductor adicional); y lo que pasa durante el alquiler (daños, un testigo encendido, el aire acondicionado, kilómetros, salir de España, limpieza, mascotas, sillas, cadenas). Sirve a cualquier hora, también en modo virtual y con gestión cerrada. NO la uses para prolongar, devolver más tarde, la web que no le deja prolongar, la contraseña o un coche de aseguradora o de empresa (prolongar_alquiler), para el minibús (buscar_punto_de_encuentro), para el horario o la dirección de una oficina (informacion_oficina), ni para una avería o un accidente, una reserva nueva o cuando hay que mirar o cambiar un dato concreto de su reserva: eso se transfiere. No digas nada antes: la herramienta continúa la conversación.

**Parámetros:**
- `tema` (obligatorio): Tema de la consulta. Valores permitidos EXACTOS: "recoger_tarde" (va a llegar tarde a recoger, vuelo o tren retrasado), "reserva_no_iniciada" (cancelar, cambiar o adelantar una reserva que aún no ha empezado), "devolucion" (devolver antes, en otra oficina o con la oficina cerrada), "cargos_y_reembolsos" (fianza, combustible, cargos, multas, facturas, reembolsos), "requisitos" (carnet, edad, documentos, tarjeta, conductor adicional), "durante_el_alquiler" (daños, testigos, aire acondicionado, kilómetros, salir de España, limpieza, mascotas, sillas, cadenas), "otro". Si pregunta por varias cosas, pon la primera.
- `pregunta` (opcional): La pregunta del cliente en una frase corta, tal como la ha dicho, sin datos personales (ni nombre, ni reserva, ni matrícula, ni correo, ni teléfono). Si todavía no ha concretado la pregunta, OMITE este parámetro.

## 5. transfer_to_human_agent

- persistent_id: `17c682a0-82d2-42f6-88fa-817d8cba0783`
- Hijo: Python «Preparar transferencia» → Paths «¿Transferir?» → «Transferir» → Transfer «Initiate customer
  connection» (ver `preparar-transferencia.md` y `transfer.md`)
- `execution`: se envió `{"async": false, "force_invoke_llm_on_result": false}` (como en la v25), pero la API no lo
  guarda: queda el valor por defecto
- `hold_music`: estático, «holdacent» (asset `01a0fc02-a13d-77a2-8de3-82459eb2a2a6`), URL `<URL_FIRMADA>`
  (en la v25 el Triaje usaba «Acoustic»; spec §5.8)

**message** (tipo `ai`, igual que en la v25). Ejemplo: «Entiendo su enfado, y siento que haya tenido que esperar tanto. Le paso ahora mismo con un compañero que le va a ayudar. Puede tardar unos segundos, no cuelgue, por favor.» Descripción: Informa al cliente, en su idioma, de que le vas a pasar con un compañero que le va a ayudar. Sé breve y tranquilizador. Termina SIEMPRE avisando de que puede tardar unos segundos en atenderle y pidiéndole que no cuelgue (por ejemplo: "puede tardar unos segundos, no cuelgue, por favor"). Si el cliente está molesto, frustrado o ya ha tenido que insistir para que le pases con alguien, valida primero su emoción en una frase corta y sincera antes de anunciar la transferencia: reconoce la molestia concreta que te ha expresado, sin excusas largas ni justificaciones. Nunca anuncies la transferencia en seco a un cliente enfadado. No menciones colas, extensiones ni números. No prometas una oficina concreta ni un equipo específico.

**Descripción:** Transfiere la llamada a una cola de compañeros. Úsala solo en los casos de TRANSFIERES TÚ y de NO INSISTAS, o si no puedes seguir al cliente por el idioma. En modo virtual, solo para una avería o un accidente (cola asistencia). Con gestión cerrada, nunca con la cola gestion. Prolongar, la web, la contraseña, el minibús, las oficinas y las dudas del alquiler no se transfieren: tienen su herramienta. Ejecútala en el mismo turno en que decides transferir, sin decir antes «le paso». Si devuelve gestion_cerrada, no la repitas: sigue COLA DE GESTIÓN CERRADA.

**Parámetros (los tres obligatorios):**
- `cola` (en HappyRobot, `{{gestion_abierta}}` va como nodo de variable de Plate): Cola de destino. Valores permitidos EXACTOS: "asistencia" (avería o accidente; funciona siempre), "nueva_reserva" (todavía no tiene reserva y quiere alquilar, o pregunta precios o disponibilidad para un alquiler nuevo), "minibus" (queja del minibús, persona sin motivo en la línea de Minibús, idioma que no puedes seguir o conversación atascada), "gestion" (hay que mirar o cambiar un dato concreto de su reserva, o persona sin motivo en la línea de Prolongación; solo con gestión abierta). Gestión ahora: {{gestion_abierta}}. Si es false, nunca uses "gestion".
- `motivo_transferencia`: Por qué transfieres. Valores permitidos EXACTOS: "no_iniciada", "web_no_disponible", "pregunta_reserva_concreta", "aseguradora", "enfado", "error_tecnico", "minibus", "asistencia", "nueva_reserva", "correo_no_coincide", "otro". En el Triaje: "asistencia" (avería o accidente), "nueva_reserva", "minibus" (queja del minibús), "pregunta_reserva_concreta" (dato concreto de su reserva), "enfado" (cliente muy enfadado que exige una persona) u "otro" (persona sin motivo, idioma o conversación atascada).
- `resumen_para_agente`: Resumen del motivo de la llamada que se le leerá en voz alta al compañero que recibe la transferencia, antes de conectarle con el cliente. SIEMPRE en español, aunque el cliente hable otro idioma. Una sola frase, de 10 a 25 palabras, en tercera persona, que diga qué quiere el cliente, en qué aeropuerto u oficina está si lo sabes y qué se ha intentado ya. Sin datos personales (nombre, reserva, matrícula, correo, teléfono), sin códigos, extensiones ni importes. Si el cliente habla otro idioma, añade al final 'El cliente habla inglés' (o el idioma que sea). Ejemplos: 'Cliente en Madrid T4 lleva veinte minutos esperando el minibús y no ha pasado.' 'Cliente con pinchazo en carretera, necesita asistencia.' 'Cliente quiere cambiar el conductor principal de su reserva.'

## Configuración

| Herramienta | ID de nodo en la v2 | persistent_id |
|---|---|---|
| buscar_punto_de_encuentro | `01a14f1d-0397-715b-ab9d-56f6a46a9f60` | `72261523-5d3f-4830-ac36-67ab187d93ed` |
| informacion_oficina | `01a14f1d-0399-7f31-a5b5-1d49d3808d0e` | `414b964d-bb29-428a-b9a1-92b1a3a8d6be` |
| consultas_alquiler | `01a14f1d-0399-770c-9155-7167deaf5c99` | `414bdc8c-aacc-4125-b323-acc6a2ae3373` |
| transfer_to_human_agent | `01a14f1d-0397-721d-9dab-ad0e44f6e642` | `17c682a0-82d2-42f6-88fa-817d8cba0783` |
| prolongar_alquiler | `01a14f69-b092-7e6d-9203-c968520c1670` | `01a14f69-b092-7e6d-9203-c968520c1670` |
