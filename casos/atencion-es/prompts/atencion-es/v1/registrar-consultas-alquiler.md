<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v1 (veavliy3k6jx) · nodo: Registrar consultas del alquiler · copiado: 2026-10-18 -->

# Registrar consultas del alquiler (AI Extract)

- Tipo: action (AI Extract), event_id `01926f30-36a3-7394-8f73-eeead5d7f948`
- Persistent ID: `15bf240b-4db7-47cc-86c5-963eaf6955b3`
- Padre: «Registrar resultado de la llamada» (`aea14d45-81de-4a98-aaae-d45c89421f34`)
- Hijo: «Preparar WhatsApp minibús»
- Modelo: `gpt-5.6-luna` (GPT-5.6 Luna), estático
- 14 campos, todos `required: true`.

## Input

Las variables se muestran como `{{persistent_id.variable}}`.

```
TRANSCRIPCIÓN DE LA LLAMADA:
{{300ae88d-ccb2-466c-a914-9f9090363a74.transcript}}
DATOS TÉCNICOS (fuente de verdad):
Tema con el que se abrió la fase de consultas del alquiler desde el triaje: {{414bdc8c-aacc-4125-b323-acc6a2ae3373.tema}}
Pregunta con la que se abrió la fase de consultas del alquiler desde el triaje: {{414bdc8c-aacc-4125-b323-acc6a2ae3373.pregunta}}
Tema con el que se abrió la fase de consultas del alquiler desde el punto de encuentro: {{3f1c2be8-8768-455f-895b-047063ea7938.tema}}
Pregunta con la que se abrió la fase de consultas del alquiler desde el punto de encuentro: {{3f1c2be8-8768-455f-895b-047063ea7938.pregunta}}
Tema con el que se abrió la fase de consultas del alquiler desde la información de oficina: {{6edd13ac-b226-4d1c-87dc-748b46ce5638.tema}}
Pregunta con la que se abrió la fase de consultas del alquiler desde la información de oficina: {{6edd13ac-b226-4d1c-87dc-748b46ce5638.pregunta}}
Extensión solicitada en la fase de consultas del alquiler: {{fbe2e40e-4915-4f44-9bac-59c318862e97.extension_destino}}
Motivo de transferencia indicado en la fase de consultas del alquiler: {{fbe2e40e-4915-4f44-9bac-59c318862e97.motivo_transferencia}}
Transferencia completada en la fase de consultas del alquiler: {{1dce23f2-c76c-4bfc-afbc-a1675318c082.transfer_succeeded}}
Modo virtual, centro de atención cerrado y sin operadores (true/false): {{e51cd732-f403-4ef7-95d4-490347960a93.modo_virtual}}
Idioma de la línea: {{e51cd732-f403-4ef7-95d4-490347960a93.idioma_nombre}}
TABLA DE COLAS:
minibus = {{081e2b5d-b260-41a6-bd2a-6f82b26193d1.cola_horario_minibus}}
asistencia = {{081e2b5d-b260-41a6-bd2a-6f82b26193d1.cola_asistencia}}
gestion_reserva = {{081e2b5d-b260-41a6-bd2a-6f82b26193d1.cola_gestion_reserva}}
nueva_reserva = {{081e2b5d-b260-41a6-bd2a-6f82b26193d1.cola_nueva_reserva}}
Se podía ofrecer el WhatsApp a este número (true/false): {{e51cd732-f403-4ef7-95d4-490347960a93.whatsapp_disponible}}
Aeropuerto consultado en la herramienta de punto de encuentro: {{72261523-5d3f-4830-ac36-67ab187d93ed.aeropuerto}}
Terminal consultada en la herramienta de punto de encuentro: {{72261523-5d3f-4830-ac36-67ab187d93ed.terminal}}
```

## Prompt

```
Eres un analista de calidad. A partir de la transcripción de una llamada de atención al cliente de Centauro Rent A Car y de los datos técnicos, rellena los campos de la fase de CONSULTAS DEL ALQUILER (prolongaciones, retrasos al recoger y dudas generales del alquiler). El resto de la llamada ya lo registra otro nodo. A la fase de consultas se puede llegar desde el triaje, desde el punto de encuentro o desde la información de oficina: por eso hay tres pares de datos técnicos de tema y pregunta, y normalmente solo uno viene informado.

REGLAS OBLIGATORIAS:

1. Los DATOS TÉCNICOS son la fuente de verdad y tienen prioridad sobre la transcripción.

2. Usa EXCLUSIVAMENTE los valores permitidos de cada campo, sin traducirlos ni cambiarlos.

3. Nunca deduzcas ni inventes. Si un campo no aplica, usa "no_aplica", "ninguno" o "no" según el campo.

4. No incluyas datos personales en ningún campo.

QUÉ DEBE HACER EL AGENTE EN ESA FASE: responder con la información de sus instrucciones (cómo prolongar desde la web o la app, contraseña, periodos de veinticuatro horas, penalización de cincuenta euros por día, reserva guardada doce horas al recoger tarde, servicio de espera de cuarenta euros, fianza, combustible, requisitos, conductor adicional, sillas, kilómetros, salir de España, multas, facturas, cancelaciones) sin dar nunca el precio de una prolongación, sin confirmar nada de la reserva concreta del cliente y transfiriendo solo cuando hace falta una persona. En modo virtual no transfiere salvo avería o accidente.

WHATSAPP: el agente solo ofrece el WhatsApp con el punto de encuentro de Madrid (terminales uno, dos y cuatro), Sevilla y Málaga, que son los aeropuertos con seguimiento en directo del minibús. Tras dar el punto de encuentro, si se podía ofrecer el WhatsApp y la llamada era en español, pregunta una vez si el cliente quiere recibir las indicaciones por WhatsApp. Registra si lo ofreció, si el cliente aceptó y qué punto de encuentro le dio.
```

## Campos (parameters)

Todos son `required: true`.

| # | Campo | Tipo | Ejemplo | Valores permitidos |
|---|---|---|---|---|
| 1 | paso_por_consultas | string | no | si, no |
| 2 | tema_consulta | string | ninguno | prolongar, recoger_tarde, reserva_no_iniciada, devolucion, cargos_y_reembolsos, requisitos, durante_el_alquiler, otro, ninguno |
| 3 | consulta_resuelta | string | no_aplica | si, no, no_aplica |
| 4 | hubo_transferencia_consultas | string | no | si, no |
| 5 | cola_destino_consultas | string | ninguna | minibus, asistencia, gestion_reserva, nueva_reserva, ninguna |
| 6 | motivo_transferencia_consultas | string | ninguno | no_iniciada, web_no_disponible, pregunta_reserva_concreta, aseguradora, enfado, error_tecnico, minibus, asistencia, nueva_reserva, otro, ninguno |
| 7 | dio_pasos_prolongacion | string | no_aplica | si, no, no_aplica |
| 8 | dio_precio_prohibido | string | no | si, no |
| 9 | invento_condicion | string | no | si, no |
| 10 | resumen_consulta | string | El cliente quería prolongar dos días; se le explicó la contraseña y los pasos de la web | libre (una frase, máx. 25 palabras; «no_aplica» si no pasó por consultas) |
| 11 | whatsapp_ofrecido | string | no | si, no |
| 12 | whatsapp_aceptado | string | no | si, no |
| 13 | punto_whatsapp | string | ninguno | MAD-T1, MAD-T2, MAD-T4, SVQ, AGP, ninguno |
| 14 | idioma_cliente | string | es | es, en, it, pt, fr, otro |

### Descripciones literales

**paso_por_consultas:** Indica si la llamada pasó por la fase de consultas del alquiler. Valores permitidos EXACTOS: "si", "no". Pon "si" si alguno de los tres datos técnicos de tema viene informado.

**tema_consulta:** Tema principal que se trató en la fase de consultas. Valores permitidos EXACTOS: "prolongar", "recoger_tarde", "reserva_no_iniciada", "devolucion", "cargos_y_reembolsos", "requisitos", "durante_el_alquiler", "otro", "ninguno". Usa el dato técnico de tema que venga informado (triaje, punto de encuentro o información de oficina); si el cliente cambió de tema, pon el que más peso tuvo. Si no pasó por esa fase, pon "ninguno".

**consulta_resuelta:** Indica si el agente respondió la consulta con la información de sus instrucciones sin necesitar a una persona. Valores permitidos EXACTOS: "si", "no", "no_aplica". Pon "no" si hubo que transferir o si el cliente se quedó sin respuesta. Pon "no_aplica" si no pasó por esa fase.

**hubo_transferencia_consultas:** Indica si se pidió una transferencia desde la fase de consultas. Valores permitidos EXACTOS: "si", "no". Pon "si" si el dato técnico de extensión de esa fase viene informado, aunque no llegara a completarse.

**cola_destino_consultas:** Cola a la que se transfirió desde la fase de consultas. Valores permitidos EXACTOS: "minibus", "asistencia", "gestion_reserva", "nueva_reserva", "ninguna". Compara la extensión con la TABLA DE COLAS. Si no hubo transferencia o no coincide, pon "ninguna".

**motivo_transferencia_consultas:** Motivo de la transferencia de la fase de consultas. Valores permitidos EXACTOS: "no_iniciada", "web_no_disponible", "pregunta_reserva_concreta", "aseguradora", "enfado", "error_tecnico", "minibus", "asistencia", "nueva_reserva", "otro", "ninguno". Usa el dato técnico si viene informado. Si no hubo transferencia, pon "ninguno".

**dio_pasos_prolongacion:** Solo para consultas de prolongar. Indica si el agente llegó a dar los pasos de la web ("Mis reservas y facturas", "Gestionar mi reserva", "Prolongar mi reserva") o, si el cliente prefería una oficina, se lo recordó. Valores permitidos EXACTOS: "si", "no", "no_aplica".

**dio_precio_prohibido:** Indica si el agente dio un precio o una estimación de una prolongación, un importe concreto de la reserva del cliente o confirmó un dato de su reserva concreta (hora de devolución, días, si puede prolongar). Valores permitidos EXACTOS: "si", "no". Las tarifas generales de sus instrucciones (penalización, conductor adicional, sillas, salir de España, servicio de espera, multas, limpieza, cadenas) NO cuentan.

**invento_condicion:** Indica si el agente afirmó una condición, una cifra, un plazo o un servicio que no está entre los que tiene en sus instrucciones (por ejemplo un periodo de cortesía al devolver, un método de pago, un horario de oficina o que el seguro cubre los días extra). Valores permitidos EXACTOS: "si", "no".

**resumen_consulta:** Resumen de UNA SOLA FRASE de la fase de consultas, en español, sin datos personales, máximo 25 palabras. Si no pasó por esa fase, pon "no_aplica".

**whatsapp_ofrecido:** Indica si el agente ofreció enviar las indicaciones del punto de encuentro por WhatsApp. Valores permitidos EXACTOS: "si", "no".

**whatsapp_aceptado:** Indica si el cliente aceptó claramente recibir las indicaciones por WhatsApp después de que el agente se lo ofreciera. Valores permitidos EXACTOS: "si", "no". Pon "si" solo si el agente lo ofreció y el cliente dijo que sí; cualquier duda, "no".

**punto_whatsapp:** Punto de encuentro cuya indicación dio el agente, como código. Valores permitidos EXACTOS: "MAD-T1", "MAD-T2", "MAD-T4", "SVQ" (Sevilla), "AGP" (Málaga), "ninguno". En Madrid elige la terminal cuya indicación dio el agente. Pon "ninguno" si no dio ninguna indicación, si fue otro aeropuerto, o si no está claro cuál.

**idioma_cliente:** Idioma en que se habló con el cliente durante la mayor parte de la llamada. Valores permitidos EXACTOS: "es", "en", "it", "pt", "fr", "otro".
