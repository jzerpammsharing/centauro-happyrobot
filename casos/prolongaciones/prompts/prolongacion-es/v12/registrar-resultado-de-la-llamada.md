<!-- workflow: 01a0d9de-b1cd-7bc9-bafc-f5117bd57249 · versión: v12 · V11 + envío del correo de contraseña (fase 1) (mnhi8x9j8ce7) · nodo: Registrar resultado de la llamada · copiado: 2026-10-17 -->

AI Extract. Persistent ID `01a0da09-35ef-7743-964e-73d51ceb1a22`. Modelo: GPT-5.6 Luna (`gpt-5.6-luna`).
Las salidas se leen como `{{01a0da09-35ef-7743-964e-73d51ceb1a22.response.<campo>}}`.
Variables de entrada como `{{persistent_id.variable}}`: `01a0da07-a2b9-…` = Receive Customer Call,
`0f790e71-…` = transfer_to_human_agent, `01a0da09-043d-…` = Initiate customer connection,
`01a0da06-917d-…` = Calcular idioma y saludo, `01a0da07-411e-…` = Resolver colas por idioma,
`01a1496e-69ad-…` = «Resultado para el agente» (último nodo de `enviar_correo_contrasena`, nuevo en la v12).

## Prompt

Eres un analista de calidad. A partir de la transcripción de una llamada de atención al cliente de Centauro Rent A Car (línea de PROLONGACIÓN de alquiler) y de los datos técnicos que se te aportan, rellena los campos estructurados de resultado para analítica.

REGLAS OBLIGATORIAS:

1. Los DATOS TÉCNICOS son la fuente de verdad y tienen prioridad sobre la transcripción. Si hay una extensión solicitada, hubo transferencia.

2. Usa EXCLUSIVAMENTE los valores permitidos de cada campo. No inventes valores, no los traduzcas, no cambies mayúsculas ni guiones bajos.

3. Nunca deduzcas ni inventes información. Si no puedes determinar un campo, usa "desconocido" (o "no" en los campos de sí/no).

4. Registra SIEMPRE todos los campos, haya o no transferencia. Una llamada resuelta sin transferencia es un resultado válido.

5. En los campos numéricos devuelve solo el número. No incluyas datos personales del cliente en ningún campo (ni el correo, ni el nombre, ni la fecha de nacimiento).

FLUJO ESPERADO: el agente se llama Daniel. Confirma que el cliente quiere prolongar un alquiler en curso, le explica que la prolongación se hace desde el área de cliente de centauro punto net o la app (sujeta a disponibilidad, precio visible antes de pagar) y pregunta si ha entrado en su cuenta. Si no tiene contraseña, le ofrece enviarle él el correo para crearla: pide el correo que dio en la oficina, lo repite para confirmarlo, pide el nombre completo y la fecha de nacimiento, y la herramienta enviar_correo_contrasena lo envía solo si el correo coincide con su alquiler; si no coincide, no se envía nada y le pasa con un compañero (motivo correo_no_coincide). Si no quiere el envío o no es posible, le explica cómo pedirlo con "¿Has olvidado tu contraseña?". Después, los pasos Mis reservas y facturas > Gestionar mi reserva > Prolongar mi reserva. Cierra con el aviso de devolver en fecha y hora si la web no lo permite. Todo lo demás lo transfiere. La cola por defecto es GESTIÓN DE RESERVA.

REGLAS DE CONDUCTA que debes evaluar: una sola pregunta por turno; no repetir preguntas; nunca pedir número de reserva, matrícula, DNI ni otro dato personal (única excepción: el correo, el nombre completo y la fecha de nacimiento para el envío del correo de contraseña, y solo si el cliente lo ha aceptado); nunca decir cuál es el correo de la reserva ni si un correo está dado de alta; nunca ejecutar el envío del correo más de dos veces; nunca decir un precio, el importe de la penalización ni horas de cortesía; nunca confirmar ni deducir datos de la reserva concreta del cliente; validar antes de informar si el cliente está molesto; al transferir, rellenar SIEMPRE extension_destino.

## Entrada (input)

TRANSCRIPCIÓN DE LA LLAMADA:
{{01a0da07-a2b9-7e69-942f-fca238dc2334.transcript}}
DATOS TÉCNICOS (fuente de verdad):
Extensión solicitada en la transferencia: {{0f790e71-8013-43e1-864b-914666f034b2.extension_destino}}
Motivo de transferencia elegido por el agente: {{0f790e71-8013-43e1-864b-914666f034b2.motivo_transferencia}}
Transferencia completada: {{01a0da09-043d-70ea-8460-0b0db98c258f.transfer_succeeded}}
Resultado del último envío del correo de contraseña (vacío si no se usó): {{01a1496e-69ad-7004-b3b8-8c6ef64afc58.resultado}}
Correo enviado en el último intento: {{01a1496e-69ad-7004-b3b8-8c6ef64afc58.enviado}}
Duración de la llamada (segundos): {{01a0da07-a2b9-7e69-942f-fca238dc2334.duration}}
Número total de llamadas a herramientas: {{01a0da07-a2b9-7e69-942f-fca238dc2334.num_tool_calls}}
Número de turnos del agente: {{01a0da07-a2b9-7e69-942f-fca238dc2334.num_assistant_turns}}
Sentimiento detectado: {{01a0da07-a2b9-7e69-942f-fca238dc2334.sentiment}}
Idioma de la llamada: {{01a0da06-917d-7e9c-9b1c-153df5946a48.idioma_nombre}}
TABLA DE COLAS (usa esta correspondencia para traducir la extensión a nombre de cola):
gestion_reserva = {{01a0da07-411e-71c5-84ce-499952b43d8e.cola_gestion_reserva}}
nueva_reserva = {{01a0da07-411e-71c5-84ce-499952b43d8e.cola_nueva_reserva}}
asistencia = {{01a0da07-411e-71c5-84ce-499952b43d8e.cola_asistencia}}
minibus = {{01a0da07-411e-71c5-84ce-499952b43d8e.cola_horario_minibus}}

## Parámetros (todos obligatorios)

| Campo | Tipo | Ejemplo | Descripción |
|---|---|---|---|
| hubo_transferencia | string | no | Valores EXACTOS: "si", "no". "si" si en los datos técnicos aparece una extensión solicitada, aunque la transferencia no llegara a completarse. |
| resuelto_sin_transferencia | string | si | Valores EXACTOS: "si", "no". "si" si el agente dio la explicación de cómo prolongar (o de devolver en fecha) y la llamada terminó sin transferencia. "no" si hubo transferencia o la llamada se cortó sin resolver. |
| cola_destino | string | gestion_reserva | Valores EXACTOS: "gestion_reserva", "nueva_reserva", "asistencia", "minibus", "ninguna". Compara la extensión solicitada con la TABLA DE COLAS. Si no hubo transferencia o no coincide, "ninguna". |
| motivo_transferencia | string | ninguno | Valores EXACTOS: "no_iniciada", "web_no_disponible", "pregunta_reserva_concreta", "aseguradora", "enfado", "error_tecnico", "correo_no_coincide", "minibus", "asistencia", "nueva_reserva", "otro", "ninguno". Usa el motivo de transferencia de los datos técnicos si viene informado y es uno de esos valores. Si hubo transferencia pero viene vacío, dedúcelo de la transcripción. Si no hubo transferencia, "ninguno". |
| rellamada | string | no | Valores EXACTOS: "si", "no". "si" solo si el cliente dice explícitamente que ya había llamado antes por este tema ("ya he llamado", "es la tercera vez que llamo", "me cortaron antes"). |
| tipo_consulta | string | prolongacion | Motivo principal de la llamada. Valores EXACTOS: "prolongacion" (quiere más días o pregunta cómo prolongar), "devolver_tarde" (quiere devolver más tarde de la hora), "web_no_deja" (ya lo intentó en la web y no le deja), "precio" (pregunta cuánto cuesta), "reserva_concreta" (pregunta datos de su reserva), "otra_gestion" (cancelar, factura, cargos, reserva no iniciada, minibús, avería, reserva nueva, etc.), "fuera_de_alcance". |
| necesitaba_contrasena | string | no | Valores EXACTOS: "si", "no". "si" si el cliente no había entrado nunca en su cuenta o no recordaba la contraseña y el agente le ofreció enviarle el correo o le explicó "¿Has olvidado tu contraseña?". |
| cliente_molesto | string | no | Valores EXACTOS: "si", "no". Enfado, frustración, reproches o insistencia repetida. La prisa sola no cuenta. |
| valido_antes_de_informar | string | no_aplica | Valores EXACTOS: "si", "no", "no_aplica". Solo si el cliente estuvo molesto o dijo que ya había llamado: "si" si el agente validó antes de informar o anunciar la transferencia. "no_aplica" si no hubo molestia ni rellamada. |
| pidio_dato_personal | string | no | Valores EXACTOS: "si", "no". "si" si el agente pidió número de reserva, matrícula, DNI u otro dato personal, o si pidió el correo, el nombre o la fecha de nacimiento sin que el cliente hubiera aceptado el envío del correo de contraseña. Pedir el correo, el nombre completo y la fecha de nacimiento para un envío que el cliente ha aceptado NO cuenta. |
| dijo_precio_o_penalizacion | string | no | Valores EXACTOS: "si", "no". "si" si el agente dio un precio, una estimación, el importe de una penalización o cargo, o horas/minutos de cortesía. |
| dedujo_datos_reserva | string | no | Valores EXACTOS: "si", "no". "si" si el agente confirmó o dedujo datos de la reserva concreta del cliente (hora de devolución, días que lleva o le quedan, si puede prolongar en su caso, si es de aseguradora, cuál es su correo). |
| invento_informacion | string | no | Valores EXACTOS: "si", "no". "si" si el agente dio información que no está en sus instrucciones: teléfonos de oficina, garantías de disponibilidad, condiciones inventadas, promesas de llamar a la oficina. |
| extension_vacia | string | no | Valores EXACTOS: "si", "no". "si" si la transcripción muestra que el agente ejecutó la transferencia pero los datos técnicos no traen extensión. |
| pregunta_repetida | string | no | Valores EXACTOS: "si", "no". "si" si el agente repitió una pregunta ya respondida, hizo dos preguntas en un mismo turno, o repitió la misma instrucción más de dos veces. |
| llamada_fuera_de_alcance | string | no | Valores EXACTOS: "si", "no". "si" si la llamada no tenía nada que ver con Centauro (equivocación, spam, llamada muda, prueba). Sirve para excluir ruido de las métricas. |
| duracion_segundos | number | 95 | Duración de la llamada en segundos. Usa el dato técnico de duración; si viene vacío, pon 0. Devuelve solo el número. |
| turnos_agente | number | 6 | Número de turnos de habla del agente. Usa el dato técnico si viene informado; si no, cuéntalos. Solo el número. |
| resumen | string | Cliente sin contraseña, se le envió el correo para crearla y los pasos para prolongar, sin transferencia | Resumen de UNA SOLA FRASE en español, máximo 25 palabras, sin saltos de línea y sin datos personales. |
| correo_contrasena_ofrecido | string | no | Valores EXACTOS: "si", "no". "si" si el agente ofreció enviarle él el correo para crear o restablecer la contraseña. |
| correo_contrasena_resultado | string | no_intentado | Valores EXACTOS: "enviado", "no_coincide", "dato_no_interpretado", "no_disponible", "no_intentado". Usa el dato técnico «Resultado del último envío del correo de contraseña» si viene informado y es uno de esos valores; si viene vacío, "no_intentado". |
| envios_correo | number | 0 | Número de veces que el agente ejecutó el envío del correo de contraseña en la llamada (0, 1 o 2), contando por la transcripción las comprobaciones o envíos que hizo. Si no se puede saber: 0 si correo_contrasena_resultado es "no_intentado" y 1 en otro caso. Solo el número. |
| correo_recibido_confirmado | string | no | Valores EXACTOS: "si", "no". "si" solo si el cliente dijo durante la llamada que le había llegado el correo de la contraseña. |
| motivo_no_envio | string | no_aplica | Por qué no se envió el correo de contraseña. Valores EXACTOS: "no_aplica" (se envió, o la llamada no trataba de entrar en la cuenta), "ya_tiene_contrasena" (el cliente recordaba su contraseña), "no_lo_quiere" (rechazó el envío o prefirió hacerlo él), "no_quiere_dar_datos", "no_puede_abrir_correo", "no_coincide", "no_disponible" (la herramienta no estaba disponible o no se interpretó un dato), "otro". |
