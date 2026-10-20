<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v1 (veavliy3k6jx) · nodo: Registrar resultado de la llamada · copiado: 2026-10-18 -->

# Registrar resultado de la llamada (AI Extract)

- Tipo: action (AI Extract), event_id `01926f30-36a3-7394-8f73-eeead5d7f948`
- Persistent ID: `aea14d45-81de-4a98-aaae-d45c89421f34`
- Padre: «Receive Customer Call» (`300ae88d-ccb2-466c-a914-9f9090363a74`)
- Hijo: «Registrar consultas del alquiler»
- Modelo: `gpt-5.6-luna` (GPT-5.6 Luna), estático
- 29 campos, todos `required: true`.

## Input

Las variables se muestran como `{{persistent_id.variable}}`.

```
TRANSCRIPCIÓN DE LA LLAMADA:
{{300ae88d-ccb2-466c-a914-9f9090363a74.transcript}}
DATOS TÉCNICOS (fuente de verdad):
Extensión solicitada en la fase de triaje: {{17c682a0-82d2-42f6-88fa-817d8cba0783.extension_destino}}
Transferencia completada en la fase de triaje: {{b4439401-fdae-4a3b-9a42-9a5c2de8f1b2.transfer_succeeded}}
Extensión solicitada en la fase de punto de encuentro: {{00435498-eccf-4110-9cf1-eb17821af3ed.extension_destino}}
Transferencia completada en la fase de punto de encuentro: {{37fb8053-214e-4357-be80-0fc8f832ecbc.transfer_succeeded}}
Extensión solicitada en la fase de información de oficina: {{62c5b6dd-5dde-4b3a-9a93-adb638c0bd66.extension_destino}}
Transferencia completada en la fase de información de oficina: {{faec6a20-257a-4b8c-8c75-8dd336beead7.transfer_succeeded}}
Aeropuerto consultado en la herramienta de punto de encuentro: {{72261523-5d3f-4830-ac36-67ab187d93ed.aeropuerto}}
Terminal consultada en la herramienta de punto de encuentro: {{72261523-5d3f-4830-ac36-67ab187d93ed.terminal}}
Tema consultado en la herramienta de información de oficina: {{414b964d-bb29-428a-b9a1-92b1a3a8d6be.tema}}
Oficina consultada en la herramienta de información de oficina: {{414b964d-bb29-428a-b9a1-92b1a3a8d6be.oficina}}
Número total de llamadas a herramientas: {{300ae88d-ccb2-466c-a914-9f9090363a74.num_tool_calls}}
Número de turnos del agente: {{300ae88d-ccb2-466c-a914-9f9090363a74.num_assistant_turns}}
Sentimiento detectado: {{300ae88d-ccb2-466c-a914-9f9090363a74.sentiment}}
Modo virtual, centro de atención cerrado y sin operadores (true/false): {{e51cd732-f403-4ef7-95d4-490347960a93.modo_virtual}}
Oficinas de la zona CET ya cerradas por hoy (true/false): {{e51cd732-f403-4ef7-95d4-490347960a93.nocturno_cet}}
Idioma de la llamada: {{e51cd732-f403-4ef7-95d4-490347960a93.idioma_nombre}}
TABLA DE COLAS (usa esta correspondencia para traducir la extensión a nombre de cola):
minibus = {{081e2b5d-b260-41a6-bd2a-6f82b26193d1.cola_horario_minibus}}
asistencia = {{081e2b5d-b260-41a6-bd2a-6f82b26193d1.cola_asistencia}}
gestion_reserva = {{081e2b5d-b260-41a6-bd2a-6f82b26193d1.cola_gestion_reserva}}
nueva_reserva = {{081e2b5d-b260-41a6-bd2a-6f82b26193d1.cola_nueva_reserva}}
```

## Prompt

```
Eres un analista de calidad. A partir de la transcripción de una llamada de atención al cliente de Centauro Rent A Car y de los datos técnicos que se te aportan, rellena los campos estructurados de resultado para analítica.

REGLAS OBLIGATORIAS:

1. Los DATOS TÉCNICOS son la fuente de verdad y tienen prioridad sobre lo que se diga en la transcripción. Si un dato técnico indica que hubo transferencia, hubo transferencia, aunque la conversación no lo deje claro.

2. Usa EXCLUSIVAMENTE los valores permitidos que se indican en cada campo. No inventes valores nuevos, no traduzcas los valores, no cambies mayúsculas ni guiones bajos.

3. Nunca deduzcas ni inventes información que no esté presente. Si un campo no aplica o no puedes determinarlo con seguridad, usa "desconocido" (o "no" en los campos de sí/no), nunca un texto libre.

4. Registra SIEMPRE todos los campos, tanto si la llamada acabó en transferencia como si no. Una llamada resuelta sin transferencia es un resultado válido y debe quedar registrada igual.

5. Los tres puntos desde los que se puede transferir (fase de triaje, fase de punto de encuentro y fase de información de oficina) se registran con el mismo criterio y el mismo vocabulario. La única diferencia es el campo fase_transferencia.

6. En los campos numéricos devuelve solo el número, sin texto adicional.

FLUJO ESPERADO (úsalo como referencia para evaluar si el agente lo siguió correctamente):

El agente se llama Daniel y atiende la opción de la IVR de minibús e información de oficinas. Muchos clientes están EN el aeropuerto. Su tarea es averiguar el motivo de la llamada y encaminarla. No consulta reservas, no conoce precios ni condiciones, y no conoce por sí mismo los puntos de encuentro, los horarios ni los lugares de devolución: los obtiene de sus herramientas.

Paso 1 — MOTIVO PRIMERO. El agente debe identificar el motivo antes de preguntar el aeropuerto. El aeropuerto solo sirve para dar el punto de encuentro del minibús. Preguntar el aeropuerto a un cliente que llama por una reserva, una avería o una reserva nueva es un error de flujo.

Paso 2 — ENCAMINAMIENTO. Gestión de una reserva existente (incluidos retrasos de vuelo y cambios de hora, día u oficina de devolución), avería o accidente, reserva nueva y petición genérica de hablar con una persona se transfieren de inmediato sin preguntar el aeropuerto. Las llamadas sobre el minibús o el punto de encuentro continúan el procedimiento del aeropuerto. Las de horario de una oficina, cómo llegar a una oficina de estación o de ciudad, o dónde devolver el coche van a la herramienta de información de oficina, sin preguntar el aeropuerto ni aplicar el horario nocturno.

Paso 3 — AEROPUERTO. Si el motivo es el minibús, el agente pregunta en qué aeropuerto está el cliente.

Paso 4 — OFICINA CERRADA. Si la oficina de ese aeropuerto ya ha cerrado por hoy, el agente lo dice y da la hora de apertura, sin dar el punto de encuentro ni transferir. Si está abierta, ejecuta la herramienta de búsqueda del punto de encuentro.

Paso 5 — INDICACIÓN. El agente da la instrucción del punto de encuentro una sola vez, con calma, y cierra tranquilizando sin pedir confirmación.

MODO VIRTUAL. De 22:00 a 08:00 (hora peninsular) el centro de atención está cerrado: el agente se presenta como asistente virtual, sigue dando el punto de encuentro y la información de oficinas y NO transfiere, salvo por avería o accidente (cola de asistencia). En los demás casos explica que no hay compañeros y que puede volver a llamar a partir de las ocho de la mañana.

Paso 6 — INFORMACIÓN DE OFICINA. En esa fase el agente identifica la oficina (como mucho una pregunta si la ciudad tiene varias) y da solo el dato pedido: el horario, cómo llegar o dónde devolver el coche, avisando de forma explícita cuando la devolución es en un sitio distinto de la oficina. Si la oficina no tiene datos, remite una vez al correo de confirmación y, si no basta, transfiere.

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

## Campos (parameters)

Todos son `required: true`.

| # | Campo | Tipo | Ejemplo | Valores permitidos |
|---|---|---|---|---|
| 1 | modo_virtual | string | no | si, no |
| 2 | hubo_transferencia | string | si | si, no |
| 3 | cola_destino | string | minibus | minibus, asistencia, gestion_reserva, nueva_reserva, ninguna |
| 4 | motivo_llamada | string | minibus | minibus, horario, como_llegar, devolucion, gestion_reserva, averia, nueva_reserva, peticion_humano, otro, desconocido |
| 5 | motivo_transferencia | string | queja_minibus | queja_minibus, cliente_perdido, averia, gestion_reserva, retraso_llegada, cambio_devolucion, nueva_reserva, peticion_humano, idioma_no_soportado, sin_datos_oficina, ninguno |
| 6 | fase_transferencia | string | punto_encuentro | triaje, punto_encuentro, informacion_oficina, ninguna |
| 7 | aeropuerto_detectado | string | Malaga | libre (o "desconocido") |
| 8 | terminal_detectada | string | T2 | libre (o "desconocido") |
| 9 | oficina_consultada | string | Malaga estacion | libre (o "desconocido") |
| 10 | punto_encuentro_entregado | string | si | si, no |
| 11 | informacion_oficina_entregada | string | no | si, no |
| 12 | aeropuerto_sin_datos | string | no | si, no |
| 13 | motivo_no_resuelto | string | ninguno | se_atasco, idioma, aeropuerto_no_identificado, oficina_no_identificada, sin_datos_aeropuerto, sin_datos_oficina, oficina_cerrada, sin_operadores, derivacion_normal, ninguno |
| 14 | cliente_molesto | string | no | si, no |
| 15 | resumen | string | El cliente estaba en Malaga, se le dio el punto de encuentro y colgo satisfecho | libre (una frase, máx. 25 palabras) |
| 16 | ultima_herramienta | string | buscar_punto_de_encuentro | buscar_punto_de_encuentro, informacion_oficina, transfer_to_human_agent, ninguna |
| 17 | herramientas_con_error | string | ninguna | lista separada por comas o «ninguna» |
| 18 | reintentos_herramienta | number | 0 | número |
| 19 | extension_vacia | string | no | si, no |
| 20 | llamada_fuera_de_alcance | string | no | si, no |
| 21 | flujo_correcto | string | si | si, no |
| 22 | invento_informacion | string | no | si, no |
| 23 | pregunta_repetida | string | no | si, no |
| 24 | valido_antes_de_informar | string | si | si, no, no_aplica |
| 25 | preguntas_innecesarias | number | 0 | número |
| 26 | muletillas | number | 1 | número |
| 27 | verbalizacion_acciones_internas | number | 0 | número |
| 28 | tono_agente | string | tranquilo y cercano | libre (dos o tres palabras) |
| 29 | turnos_agente | number | 8 | número |

### Descripciones literales

**modo_virtual:** Indica si la llamada se atendió en modo virtual, con el centro de atención cerrado y sin operadores. Valores permitidos EXACTOS: "si", "no". Usa el dato técnico de modo virtual: "true" es "si" y "false" es "no". Si viene vacío, pon "no".

**hubo_transferencia:** Indica si la llamada acabó transfiriéndose a un agente humano. Valores permitidos EXACTOS: "si", "no". Pon "si" si en los datos técnicos aparece una extensión solicitada en cualquiera de las tres fases (triaje, punto de encuentro o información de oficina), aunque la transferencia no llegara a completarse. Pon "no" si no se solicitó ninguna extensión en ninguna de las tres fases.

**cola_destino:** Nombre legible de la cola a la que se transfirió. Valores permitidos EXACTOS: "minibus", "asistencia", "gestion_reserva", "nueva_reserva", "ninguna". Compara la extensión solicitada en los datos técnicos con la TABLA DE COLAS del input y devuelve el nombre correspondiente. Si no hubo transferencia, pon "ninguna". Si hubo transferencia pero la extensión no coincide con ninguna de la tabla, pon "ninguna".

**motivo_llamada:** Motivo principal por el que llamó el cliente, según lo que pidió. Valores permitidos EXACTOS: "minibus", "horario", "como_llegar", "devolucion", "gestion_reserva", "averia", "nueva_reserva", "peticion_humano", "otro", "desconocido". Usa "minibus" para el minibús o el punto de encuentro de un aeropuerto. Usa "horario" para el horario de una oficina. Usa "como_llegar" para cómo llegar a una oficina de estación o de ciudad. Usa "devolucion" para dónde devolver el coche. Usa "gestion_reserva" para cualquier cosa de una reserva existente, incluidos retrasos de vuelo y cambios de devolución.

**motivo_transferencia:** Motivo por el que se transfirió, según lo que pidió el cliente. Valores permitidos EXACTOS: "queja_minibus", "cliente_perdido", "averia", "gestion_reserva", "retraso_llegada", "cambio_devolucion", "nueva_reserva", "peticion_humano", "idioma_no_soportado", "sin_datos_oficina", "ninguno". Usa "queja_minibus" si el minibús se fue sin él, no pasa o lleva mucho esperando. Usa "cliente_perdido" si sigue sin encontrar el punto tras las indicaciones. Usa "retraso_llegada" si va a llegar tarde o su vuelo o tren se retrasa. Usa "cambio_devolucion" si quiere cambiar la hora, el día o la oficina de devolución. Usa "sin_datos_oficina" si se transfirió porque no había datos de la oficina o no se pudo identificar. Usa "peticion_humano" si pidió hablar con una persona sin dar motivo. Si no hubo transferencia, pon "ninguno".

**fase_transferencia:** Fase del flujo en la que se originó la transferencia. Valores permitidos EXACTOS: "triaje", "punto_encuentro", "informacion_oficina", "ninguna". Pon "triaje" si la extensión aparece en el dato técnico de la fase de triaje. Pon "punto_encuentro" si aparece en el de la fase de punto de encuentro. Pon "informacion_oficina" si aparece en el de la fase de información de oficina. Si no hubo transferencia, pon "ninguna".

**aeropuerto_detectado:** Aeropuerto en el que se encontraba el cliente. Usa preferentemente el dato técnico de aeropuerto consultado. Si viene vacío, usa el aeropuerto que el cliente haya mencionado en la transcripción, tal cual lo dijo. Si el cliente nunca llegó a indicar un aeropuerto, pon "desconocido".

**terminal_detectada:** Terminal indicada por el cliente. Usa el dato técnico de terminal consultada si viene informado; si no, la terminal que el cliente haya mencionado espontáneamente. Si no mencionó ninguna, pon "desconocido". Nunca deduzcas ni inventes una terminal.

**oficina_consultada:** Oficina sobre la que el cliente pidió información (horario, cómo llegar o devolución). Usa el dato técnico de oficina consultada si viene informado; si no, la oficina que se identificó en la transcripción, tal cual. Si la llamada no fue de información de oficina o no se llegó a identificar, pon "desconocido".

**punto_encuentro_entregado:** Indica si el agente llegó a darle al cliente la indicación del punto de encuentro. Valores permitidos EXACTOS: "si", "no". Pon "si" solo si en la transcripción el agente le explicó dónde tiene que esperar o adónde ir. Pon "no" si la llamada se transfirió antes, si no se identificó el aeropuerto o si el agente no supo dar la indicación.

**informacion_oficina_entregada:** Indica si el agente llegó a darle al cliente el horario, cómo llegar a la oficina o dónde devolver el coche. Valores permitidos EXACTOS: "si", "no". Pon "si" solo si en la transcripción el agente le dio ese dato. Pon "no" si la llamada no fue de información de oficina, si se transfirió antes o si el agente no tenía el dato.

**aeropuerto_sin_datos:** Indica si el agente no disponía de instrucción para ese aeropuerto u oficina y tuvo que remitir al correo de confirmación o a un agente humano por falta de información. Valores permitidos EXACTOS: "si", "no". Pon "si" únicamente cuando el motivo de no poder ayudar fue la ausencia de datos de ese aeropuerto u oficina, no cuando el cliente llamaba por otro asunto.

**motivo_no_resuelto:** Si la llamada no se resolvió, motivo principal. Valores permitidos EXACTOS: "se_atasco", "idioma", "aeropuerto_no_identificado", "oficina_no_identificada", "sin_datos_aeropuerto", "sin_datos_oficina", "oficina_cerrada", "sin_operadores", "derivacion_normal", "ninguno". Usa "se_atasco" si el agente se bloqueó o repitió sin avanzar. Usa "idioma" si no pudo seguir al cliente por el idioma. Usa "aeropuerto_no_identificado" si nunca supo dónde estaba el cliente. Usa "oficina_no_identificada" si no se llegó a saber por qué oficina preguntaba. Usa "oficina_cerrada" si la oficina del aeropuerto ya había cerrado por hoy. Usa "sin_operadores" si en modo virtual el cliente necesitaba a un compañero y se le pidió volver a llamar a partir de las ocho. Usa "derivacion_normal" si se transfirió porque el motivo correspondía a un equipo humano. Si se resolvió correctamente, pon "ninguno".

**cliente_molesto:** Indica si el cliente mostró enfado, frustración o tuvo que insistir para ser atendido. Valores permitidos EXACTOS: "si", "no". Básate en lo que el cliente expresa: quejas explícitas, reproches, insistencia repetida o tono de reclamación. Una simple prisa o una pregunta directa no cuentan como molestia.

**resumen:** Resumen de UNA SOLA FRASE de lo que pasó en la llamada, en español, sin saltos de línea. Sirve para inspeccionar casos concretos sin abrir la transcripción entera. Máximo 25 palabras. No incluyas datos personales del cliente.

**ultima_herramienta:** Nombre de la última herramienta que ejecutó el agente. Valores permitidos EXACTOS: "buscar_punto_de_encuentro", "informacion_oficina", "transfer_to_human_agent", "ninguna". Si el agente no ejecutó ninguna herramienta en toda la llamada, pon "ninguna".

**herramientas_con_error:** Nombres de las herramientas que devolvieron error, separados por comas y sin espacios adicionales. Por ejemplo: "buscar_punto_de_encuentro". Si ninguna herramienta falló, pon exactamente "ninguna". Considera error una respuesta vacía, un fallo explícito o una respuesta que impidió continuar.

**reintentos_herramienta:** Número de veces que el agente volvió a llamar a una herramienta tras un fallo o una respuesta inservible. Devuelve solo el número. Si no hubo reintentos, pon 0.

**extension_vacia:** Indica el fallo más grave del flujo: que el agente transfiriera SIN rellenar el parámetro extension_destino. Valores permitidos EXACTOS: "si", "no". Pon "si" cuando la transcripción muestre que se ejecutó la transferencia pero los datos técnicos no traigan ninguna extensión en esa fase. En cualquier otro caso pon "no".

**llamada_fuera_de_alcance:** Indica si la llamada no tenía nada que ver con Centauro ni con el alquiler de coches (equivocación, spam, llamada muda, prueba, silencio total). Valores permitidos EXACTOS: "si", "no". Una llamada sobre una reserva, una avería, el minibús o una oficina SIEMPRE es "no", aunque acabe transferida. Sirve para excluir ruido de las métricas.

**flujo_correcto:** Indica si el agente siguió el FLUJO ESPERADO descrito en las instrucciones. Valores permitidos EXACTOS: "si", "no". Pon "no" si preguntó el aeropuerto a un cliente que llamaba por una reserva, una avería, una reserva nueva o información de una oficina; si aplicó el horario nocturno a una pregunta de información de oficina; si dio indicaciones del punto de encuentro sin haber identificado el aeropuerto; si dio información de una oficina sin haberla identificado; si siguió preguntando más de dos veces en lugar de transferir; si en modo virtual transfirió por un motivo que no era una avería o un accidente; si dio el punto de encuentro de un aeropuerto cuya oficina ya había cerrado; o si alteró el orden de los pasos. Si el flujo se respetó, pon "si".

**invento_informacion:** Indica si el agente inventó información que tiene prohibido dar. Valores permitidos EXACTOS: "si", "no". Pon "si" si improvisó un punto de encuentro, una ubicación, un cartel, un parking, una frecuencia, un horario, una dirección, un lugar de devolución, un precio, una condición, una hora de cortesía, o si opinó sobre reservas o sobre qué se puede gestionar en el mostrador. Este campo detecta alucinaciones: sé estricto pero no marques "si" por dar correctamente una instrucción que sí figura en su lista.

**pregunta_repetida:** Indica si el agente repitió una pregunta que el cliente ya había respondido, o hizo la misma pregunta más de dos veces. Valores permitidos EXACTOS: "si", "no". Reformular una vez de otra manera cuando no se entendió no cuenta como repetición.

**valido_antes_de_informar:** Solo aplica si el cliente estuvo molesto. Indica si el agente validó su emoción ANTES de dar información o de anunciar la transferencia. Valores permitidos EXACTOS: "si", "no", "no_aplica". Pon "no_aplica" si el cliente nunca mostró molestia. Pon "no" si el agente soltó el dato o la frase de transferencia en seco a un cliente enfadado.

**preguntas_innecesarias:** Número de preguntas que el agente hizo sin necesidad: porque ya conocía el dato, porque estaban fuera del flujo esperado, o porque pidió una confirmación que las instrucciones le prohíben pedir (por ejemplo preguntar si ya recogió el equipaje o si ve el punto de encuentro). Devuelve solo el número.

**muletillas:** Número de muletillas o rellenos vacíos dichos por el agente ("eh", "mmm", "bueno", "vale vale", "a ver"). Como referencia, lo aceptable es como máximo una o dos cada seis o diez turnos. Devuelve solo el número.

**verbalizacion_acciones_internas:** Número de veces que el agente narró en voz alta una acción interna en lugar de hablar con naturalidad (por ejemplo "voy a consultar el sistema", "estoy buscando su aeropuerto", "un momento que reviso"). Las instrucciones se lo prohíben. Devuelve solo el número.

**tono_agente:** Descripción breve del tono del agente durante la llamada, en dos o tres palabras y en español. Por ejemplo: "tranquilo y cercano", "seco y mecanico", "apresurado". Refleja cómo sonó realmente, no cómo debería haber sonado.

**turnos_agente:** Número de turnos de habla del agente en la llamada. Usa el dato técnico de número de turnos del agente si viene informado; si no, cuéntalos en la transcripción. Devuelve solo el número.
