<!-- workflow: 01a05977-3a33-76da-acb2-a757f3947cf9 · versión: v3 (2139o3pf25qm) · nodo: Registrar resultado de la llamada · copiado: 2026-10-12 -->

# Registrar resultado de la llamada (AI Extract)

- event_id `01926f30-36a3-7394-8f73-eeead5d7f948` · modelo `gpt-5.6-luna`
- Es el extract de ES v22 sin los campos de información de oficina (`oficina_consultada`, `informacion_oficina_entregada`) y sin la fase `informacion_oficina`. `como_llegar` y `sin_datos_oficina` pasan a `oficina_no_aeropuerto`.

## Input

```
TRANSCRIPCIÓN DE LA LLAMADA:
{{af5a7237-13fe-4b86-b7f5-4f96b1d61c5b.transcript}}
DATOS TÉCNICOS (fuente de verdad):
Extensión solicitada en la fase de triaje: {{302bc6a5-b38f-4baf-9b2c-c62e533e3b2c.extension_destino}}
Transferencia completada en la fase de triaje: {{39a2aa34-5703-4f2f-9e0b-8d318198b78a.transfer_succeeded}}
Extensión solicitada en la fase de punto de encuentro: {{9e8601c0-cab7-49de-9590-785d03341d87.extension_destino}}
Transferencia completada en la fase de punto de encuentro: {{1e31ce4b-83c5-46b4-84e5-a26dc2d3bc42.transfer_succeeded}}
Aeropuerto consultado en la herramienta de punto de encuentro: {{cadf6598-45fa-48e2-8e0e-a205b3faf7cd.aeropuerto}}
Terminal consultada en la herramienta de punto de encuentro: {{cadf6598-45fa-48e2-8e0e-a205b3faf7cd.terminal}}
Número total de llamadas a herramientas: {{af5a7237-13fe-4b86-b7f5-4f96b1d61c5b.num_tool_calls}}
Número de turnos del agente: {{af5a7237-13fe-4b86-b7f5-4f96b1d61c5b.num_assistant_turns}}
Sentimiento detectado: {{af5a7237-13fe-4b86-b7f5-4f96b1d61c5b.sentiment}}
Modo virtual, centro de atención cerrado y sin operadores (true/false): {{0f85067a-078e-4a21-9b45-0d5bfb92dd8e.modo_virtual}}
Oficinas de la zona CET ya cerradas por hoy (true/false): {{0f85067a-078e-4a21-9b45-0d5bfb92dd8e.nocturno_cet}}
Idioma de la llamada: {{0f85067a-078e-4a21-9b45-0d5bfb92dd8e.idioma_nombre}}
TABLA DE COLAS (usa esta correspondencia para traducir la extensión a nombre de cola):
minibus = {{96b01012-31c0-4328-9bb4-1650bcdbf1dc.cola_horario_minibus}}
asistencia = {{96b01012-31c0-4328-9bb4-1650bcdbf1dc.cola_asistencia}}
gestion_reserva = {{96b01012-31c0-4328-9bb4-1650bcdbf1dc.cola_gestion_reserva}}
nueva_reserva = {{96b01012-31c0-4328-9bb4-1650bcdbf1dc.cola_nueva_reserva}}
```

## Prompt

```
Eres un analista de calidad. A partir de la transcripción de una llamada de atención al cliente de Centauro Rent A Car y de los datos técnicos que se te aportan, rellena los campos estructurados de resultado para analítica.

REGLAS OBLIGATORIAS:

1. Los DATOS TÉCNICOS son la fuente de verdad y tienen prioridad sobre lo que se diga en la transcripción. Si un dato técnico indica que hubo transferencia, hubo transferencia, aunque la conversación no lo deje claro.

2. Usa EXCLUSIVAMENTE los valores permitidos que se indican en cada campo. No inventes valores nuevos, no traduzcas los valores, no cambies mayúsculas ni guiones bajos.

3. Nunca deduzcas ni inventes información que no esté presente. Si un campo no aplica o no puedes determinarlo con seguridad, usa "desconocido" (o "no" en los campos de sí/no), nunca un texto libre.

4. Registra SIEMPRE todos los campos, tanto si la llamada acabó en transferencia como si no. Una llamada resuelta sin transferencia es un resultado válido y debe quedar registrada igual.

5. Los dos puntos desde los que se puede transferir (fase de triaje y fase de punto de encuentro) se registran con el mismo criterio y el mismo vocabulario. La única diferencia es el campo fase_transferencia.

6. En los campos numéricos devuelve solo el número, sin texto adicional.

FLUJO ESPERADO (úsalo como referencia para evaluar si el agente lo siguió correctamente):

El agente se llama Daniel y atiende la línea de minibús de Centauro. Muchos clientes están EN el aeropuerto. Su tarea es averiguar el motivo de la llamada y encaminarla. No consulta reservas, no conoce precios ni condiciones, y no conoce por sí mismo los puntos de encuentro, los horarios ni los lugares de devolución de las oficinas de aeropuerto: los obtiene de la herramienta de punto de encuentro. No tiene datos de oficinas de estación o de ciudad.

Paso 1 — MOTIVO PRIMERO. El agente debe identificar el motivo antes de preguntar el aeropuerto. El aeropuerto solo sirve para dar el punto de encuentro del minibús. Preguntar el aeropuerto a un cliente que llama por una reserva, una avería o una reserva nueva es un error de flujo.

Paso 2 — ENCAMINAMIENTO. Gestión de una reserva existente (incluidas prolongaciones, retrasos de vuelo, cambios de hora, día u oficina de devolución y dudas sobre las condiciones del alquiler), avería o accidente, reserva nueva y petición genérica de hablar con una persona se transfieren de inmediato sin preguntar el aeropuerto. Con la cola de Gestión cerrada no se transfiere a Gestión: se explica su horario. Las llamadas sobre el minibús o el punto de encuentro continúan el procedimiento del aeropuerto. Las del horario o la devolución en la oficina de un aeropuerto también: el agente pregunta el aeropuerto y ejecuta la herramienta de punto de encuentro sin aplicar el horario nocturno. Las de oficinas de estación o de ciudad se transfieren a la cola de minibús.

Paso 3 — AEROPUERTO. Si el motivo es el minibús, el agente pregunta en qué aeropuerto está el cliente.

Paso 4 — OFICINA CERRADA. Si la oficina de ese aeropuerto ya ha cerrado por hoy, el agente lo dice y da la hora de apertura, sin dar el punto de encuentro ni transferir. Si está abierta, ejecuta la herramienta de búsqueda del punto de encuentro.

Paso 5 — INDICACIÓN. El agente da la instrucción del punto de encuentro una sola vez, con calma, y cierra tranquilizando sin pedir confirmación.

MODO VIRTUAL. De 22:00 a 08:00 (hora peninsular española) el centro de atención está cerrado: el agente se presenta como asistente virtual, sigue dando el punto de encuentro y NO transfiere, salvo por avería o accidente (cola de asistencia). En los demás casos explica que no hay compañeros y que puede volver a llamar cuando abra el centro de atención.

REGLAS DE CONDUCTA que el agente debe cumplir y que debes evaluar:

- Una sola pregunta por turno. Nunca juntar dos preguntas.

- Nunca repetir una pregunta que el cliente ya respondió.

- Nunca hacer la misma pregunta más de dos veces; a la segunda sin éxito debe transferir.

- Nunca inventar puntos de encuentro, ubicaciones, salidas, parkings, carteles, frecuencias, horarios, direcciones, lugares de devolución, precios, condiciones ni horas de cortesía.

- Nunca pedir número de reserva, nombre ni datos personales.

- Si el cliente está molesto, validar su emoción ANTES de dar información o anunciar la transferencia.

- No verbalizar acciones internas (no decir cosas como "voy a consultar el sistema" o "estoy buscando").

- Al transferir, SIEMPRE debe rellenar el parámetro extension_destino. Dejarlo vacío es un error grave.

- Si el cliente lleva esperando igual o más que la frecuencia de su aeropuerto, no debe repetirle la frecuencia: debe validar y transferir.
```

## Campos (todos `required: true`)

**modo_virtual** (string, ej. `no`): Indica si la llamada se atendió en modo virtual, con el centro de atención cerrado y sin operadores. Valores permitidos EXACTOS: "si", "no". Usa el dato técnico de modo virtual: "true" es "si" y "false" es "no". Si viene vacío, pon "no".

**hubo_transferencia** (string, ej. `si`): Indica si la llamada acabó transfiriéndose a un agente humano. Valores permitidos EXACTOS: "si", "no". Pon "si" si en los datos técnicos aparece una extensión solicitada en cualquiera de las dos fases (triaje o punto de encuentro), aunque la transferencia no llegara a completarse. Pon "no" si no se solicitó ninguna extensión en ninguna de las dos fases.

**cola_destino** (string, ej. `minibus`): Nombre legible de la cola a la que se transfirió. Valores permitidos EXACTOS: "minibus", "asistencia", "gestion_reserva", "nueva_reserva", "ninguna". Compara la extensión solicitada en los datos técnicos con la TABLA DE COLAS del input y devuelve el nombre correspondiente. Si no hubo transferencia, pon "ninguna". Si hubo transferencia pero la extensión no coincide con ninguna de la tabla, pon "ninguna".

**motivo_llamada** (string, ej. `minibus`): Motivo principal por el que llamó el cliente, según lo que pidió. Valores permitidos EXACTOS: "minibus", "horario", "oficina_no_aeropuerto", "devolucion", "gestion_reserva", "averia", "nueva_reserva", "peticion_humano", "otro", "desconocido". Usa "minibus" para el minibús o el punto de encuentro de un aeropuerto. Usa "horario" para el horario de la oficina de un aeropuerto. Usa "devolucion" para dónde devolver el coche. Usa "oficina_no_aeropuerto" si pidió datos de una oficina de estación o de ciudad. Usa "gestion_reserva" para cualquier cosa de una reserva existente, incluidos prolongaciones, retrasos de vuelo, cambios de devolución y dudas sobre las condiciones del alquiler.

**motivo_transferencia** (string, ej. `queja_minibus`): Motivo por el que se transfirió, según lo que pidió el cliente. Valores permitidos EXACTOS: "queja_minibus", "cliente_perdido", "averia", "gestion_reserva", "retraso_llegada", "cambio_devolucion", "nueva_reserva", "peticion_humano", "idioma_no_soportado", "oficina_no_aeropuerto", "ninguno". Usa "queja_minibus" si el minibús se fue sin él, no pasa o lleva mucho esperando. Usa "cliente_perdido" si sigue sin encontrar el punto tras las indicaciones. Usa "retraso_llegada" si va a llegar tarde o su vuelo o tren se retrasa. Usa "cambio_devolucion" si quiere cambiar la hora, el día o la oficina de devolución. Usa "oficina_no_aeropuerto" si se transfirió porque pidió datos de una oficina de estación o de ciudad. Usa "peticion_humano" si pidió hablar con una persona sin dar motivo. Si no hubo transferencia, pon "ninguno".

**fase_transferencia** (string, ej. `punto_encuentro`): Fase del flujo en la que se originó la transferencia. Valores permitidos EXACTOS: "triaje", "punto_encuentro", "ninguna". Pon "triaje" si la extensión aparece en el dato técnico de la fase de triaje. Pon "punto_encuentro" si aparece en el de la fase de punto de encuentro. Si no hubo transferencia, pon "ninguna".

**aeropuerto_detectado** (string, ej. `Malaga`): Aeropuerto en el que se encontraba el cliente. Usa preferentemente el dato técnico de aeropuerto consultado. Si viene vacío, usa el aeropuerto que el cliente haya mencionado en la transcripción, tal cual lo dijo. Si el cliente nunca llegó a indicar un aeropuerto, pon "desconocido".

**terminal_detectada** (string, ej. `T2`): Terminal indicada por el cliente. Usa el dato técnico de terminal consultada si viene informado; si no, la terminal que el cliente haya mencionado espontáneamente. Si no mencionó ninguna, pon "desconocido". Nunca deduzcas ni inventes una terminal.

**punto_encuentro_entregado** (string, ej. `si`): Indica si el agente llegó a darle al cliente la indicación del punto de encuentro. Valores permitidos EXACTOS: "si", "no". Pon "si" solo si en la transcripción el agente le explicó dónde tiene que esperar o adónde ir. Pon "no" si la llamada se transfirió antes, si no se identificó el aeropuerto o si el agente no supo dar la indicación.

**aeropuerto_sin_datos** (string, ej. `no`): Indica si el agente no disponía de instrucción para ese aeropuerto y tuvo que remitir al correo de confirmación o a un agente humano por falta de información. Valores permitidos EXACTOS: "si", "no". Pon "si" únicamente cuando el motivo de no poder ayudar fue la ausencia de datos de ese aeropuerto, no cuando el cliente llamaba por otro asunto.

**motivo_no_resuelto** (string, ej. `ninguno`): Si la llamada no se resolvió, motivo principal. Valores permitidos EXACTOS: "se_atasco", "idioma", "aeropuerto_no_identificado", "sin_datos_aeropuerto", "oficina_cerrada", "sin_operadores", "derivacion_normal", "ninguno". Usa "se_atasco" si el agente se bloqueó o repitió sin avanzar. Usa "idioma" si no pudo seguir al cliente por el idioma. Usa "aeropuerto_no_identificado" si nunca supo dónde estaba el cliente. Usa "oficina_cerrada" si la oficina del aeropuerto ya había cerrado por hoy. Usa "sin_operadores" si en modo virtual el cliente necesitaba a un compañero y se le pidió volver a llamar cuando abra el centro de atención. Usa "derivacion_normal" si se transfirió porque el motivo correspondía a un equipo humano. Si se resolvió correctamente, pon "ninguno".

**cliente_molesto** (string, ej. `no`): Indica si el cliente mostró enfado, frustración o tuvo que insistir para ser atendido. Valores permitidos EXACTOS: "si", "no". Básate en lo que el cliente expresa: quejas explícitas, reproches, insistencia repetida o tono de reclamación. Una simple prisa o una pregunta directa no cuentan como molestia.

**resumen** (string, ej. `El cliente estaba en Malaga, se le dio el punto de encuentro y colgo satisfecho`): Resumen de UNA SOLA FRASE de lo que pasó en la llamada, en español, sin saltos de línea. Sirve para inspeccionar casos concretos sin abrir la transcripción entera. Máximo 25 palabras. No incluyas datos personales del cliente.

**ultima_herramienta** (string, ej. `buscar_punto_de_encuentro`): Nombre de la última herramienta que ejecutó el agente. Valores permitidos EXACTOS: "buscar_punto_de_encuentro", "transfer_to_human_agent", "ninguna". Si el agente no ejecutó ninguna herramienta en toda la llamada, pon "ninguna".

**herramientas_con_error** (string, ej. `ninguna`): Nombres de las herramientas que devolvieron error, separados por comas y sin espacios adicionales. Por ejemplo: "buscar_punto_de_encuentro". Si ninguna herramienta falló, pon exactamente "ninguna". Considera error una respuesta vacía, un fallo explícito o una respuesta que impidió continuar.

**reintentos_herramienta** (number, ej. `0`): Número de veces que el agente volvió a llamar a una herramienta tras un fallo o una respuesta inservible. Devuelve solo el número. Si no hubo reintentos, pon 0.

**extension_vacia** (string, ej. `no`): Indica el fallo más grave del flujo: que el agente transfiriera SIN rellenar el parámetro extension_destino. Valores permitidos EXACTOS: "si", "no". Pon "si" cuando la transcripción muestre que se ejecutó la transferencia pero los datos técnicos no traigan ninguna extensión en esa fase. En cualquier otro caso pon "no".

**llamada_fuera_de_alcance** (string, ej. `no`): Indica si la llamada no tenía nada que ver con Centauro ni con el alquiler de coches (equivocación, spam, llamada muda, prueba, silencio total). Valores permitidos EXACTOS: "si", "no". Una llamada sobre una reserva, una avería, el minibús o una oficina SIEMPRE es "no", aunque acabe transferida. Sirve para excluir ruido de las métricas.

**flujo_correcto** (string, ej. `si`): Indica si el agente siguió el FLUJO ESPERADO descrito en las instrucciones. Valores permitidos EXACTOS: "si", "no". Pon "no" si preguntó el aeropuerto a un cliente que llamaba por una reserva, una avería o una reserva nueva; si aplicó el horario nocturno a una pregunta de horario o devolución de una oficina; si dio indicaciones del punto de encuentro sin haber identificado el aeropuerto; si siguió preguntando más de dos veces en lugar de transferir; si en modo virtual transfirió por un motivo que no era una avería o un accidente; si dio el punto de encuentro de un aeropuerto cuya oficina ya había cerrado; o si alteró el orden de los pasos. Si el flujo se respetó, pon "si".

**invento_informacion** (string, ej. `no`): Indica si el agente inventó información que tiene prohibido dar. Valores permitidos EXACTOS: "si", "no". Pon "si" si improvisó un punto de encuentro, una ubicación, un cartel, un parking, una frecuencia, un horario, una dirección, un lugar de devolución, un precio, una condición, una hora de cortesía, o si opinó sobre reservas o sobre qué se puede gestionar en el mostrador. Este campo detecta alucinaciones: sé estricto pero no marques "si" por dar correctamente una instrucción que sí figura en su lista.

**pregunta_repetida** (string, ej. `no`): Indica si el agente repitió una pregunta que el cliente ya había respondido, o hizo la misma pregunta más de dos veces. Valores permitidos EXACTOS: "si", "no". Reformular una vez de otra manera cuando no se entendió no cuenta como repetición.

**valido_antes_de_informar** (string, ej. `si`): Solo aplica si el cliente estuvo molesto. Indica si el agente validó su emoción ANTES de dar información o de anunciar la transferencia. Valores permitidos EXACTOS: "si", "no", "no_aplica". Pon "no_aplica" si el cliente nunca mostró molestia. Pon "no" si el agente soltó el dato o la frase de transferencia en seco a un cliente enfadado.

**preguntas_innecesarias** (number, ej. `0`): Número de preguntas que el agente hizo sin necesidad: porque ya conocía el dato, porque estaban fuera del flujo esperado, o porque pidió una confirmación que las instrucciones le prohíben pedir (por ejemplo preguntar si ya recogió el equipaje o si ve el punto de encuentro). Devuelve solo el número.

**muletillas** (number, ej. `1`): Número de muletillas o rellenos vacíos dichos por el agente ("eh", "mmm", "bueno", "vale vale", "a ver"). Como referencia, lo aceptable es como máximo una o dos cada seis o diez turnos. Devuelve solo el número.

**verbalizacion_acciones_internas** (number, ej. `0`): Número de veces que el agente narró en voz alta una acción interna en lugar de hablar con naturalidad (por ejemplo "voy a consultar el sistema", "estoy buscando su aeropuerto", "un momento que reviso"). Las instrucciones se lo prohíben. Devuelve solo el número.

**tono_agente** (string, ej. `tranquilo y cercano`): Descripción breve del tono del agente durante la llamada, en dos o tres palabras y en español. Por ejemplo: "tranquilo y cercano", "seco y mecanico", "apresurado". Refleja cómo sonó realmente, no cómo debería haber sonado.

**turnos_agente** (number, ej. `8`): Número de turnos de habla del agente en la llamada. Usa el dato técnico de número de turnos del agente si viene informado; si no, cuéntalos en la transcripción. Devuelve solo el número.

