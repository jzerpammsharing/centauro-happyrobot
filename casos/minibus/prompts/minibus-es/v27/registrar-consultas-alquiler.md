<!-- workflow: 019f7594-2cce-7eed-b995-dd9ea64a1062 · versión: v27 (e4qv98cib2dm) · nodo: Registrar consultas del alquiler · copiado: 2026-10-24 -->

# Registrar consultas del alquiler (AI Extract)

- Node ID: `01a16f5f-671d-7303-b2f5-9987b965bb54` · Persistent ID: `01a118bc-7788-7661-894a-a3fed090d2c9`
- Tipo: action (AI Extract), event_id `01926f30-36a3-7394-8f73-eeead5d7f948`
- Modelo: `gpt-5.6-luna` (GPT-5.6 Luna), estático
- Cambia frente a v26: el párrafo WHATSAPP del prompt y la descripción de `punto_whatsapp`.

## Input

```
TRANSCRIPCIÓN DE LA LLAMADA:
{{019f8045-5a02-7105-9e51-23b284430c73.transcript}}
DATOS TÉCNICOS (fuente de verdad):
Tema con el que se abrió la fase de consultas del alquiler desde el triaje: {{01a118bb-7770-7166-b302-5c34f97e52f6.tema}}
Pregunta con la que se abrió la fase de consultas del alquiler desde el triaje: {{01a118bb-7770-7166-b302-5c34f97e52f6.pregunta}}
Tema con el que se abrió la fase de consultas del alquiler desde el punto de encuentro: {{01a1305c-93e2-753f-9318-debd132bf553.tema}}
Pregunta con la que se abrió la fase de consultas del alquiler desde el punto de encuentro: {{01a1305c-93e2-753f-9318-debd132bf553.pregunta}}
Tema con el que se abrió la fase de consultas del alquiler desde la información de oficina: {{01a1305c-fd17-7fe2-9ed6-d04b2ba552b0.tema}}
Pregunta con la que se abrió la fase de consultas del alquiler desde la información de oficina: {{01a1305c-fd17-7fe2-9ed6-d04b2ba552b0.pregunta}}
Extensión solicitada en la fase de consultas del alquiler: {{01a118bb-77e5-7509-93ea-c28b9a771285.extension_destino}}
Motivo de transferencia indicado en la fase de consultas del alquiler: {{01a118bb-77e5-7509-93ea-c28b9a771285.motivo_transferencia}}
Transferencia completada en la fase de consultas del alquiler: {{01a118bb-77ea-7f44-bf28-ea4f1e6b9bb8.transfer_succeeded}}
Modo virtual, centro de atención cerrado y sin operadores (true/false): {{019fd418-5a5d-7bd4-93f8-eae309f8dc7a.modo_virtual}}
Idioma de la línea: {{019fd418-5a5d-7bd4-93f8-eae309f8dc7a.idioma_nombre}}
TABLA DE COLAS:
minibus = {{019feb2c-0554-7b99-a980-42f896779230.cola_horario_minibus}}
asistencia = {{019feb2c-0554-7b99-a980-42f896779230.cola_asistencia}}
gestion_reserva = {{019feb2c-0554-7b99-a980-42f896779230.cola_gestion_reserva}}
nueva_reserva = {{019feb2c-0554-7b99-a980-42f896779230.cola_nueva_reserva}}
Se podía ofrecer el WhatsApp a este número (true/false): {{019fd418-5a5d-7bd4-93f8-eae309f8dc7a.whatsapp_disponible}}
Aeropuerto consultado en la herramienta de punto de encuentro: {{8c1ce1ec-a026-4eb6-ac92-59a7f7046e4b.aeropuerto}}
Terminal consultada en la herramienta de punto de encuentro: {{8c1ce1ec-a026-4eb6-ac92-59a7f7046e4b.terminal}}
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

WHATSAPP: el agente solo ofrece el WhatsApp con el punto de encuentro de Madrid (terminales uno, dos y cuatro), Sevilla y Málaga, que son los aeropuertos con seguimiento en directo del minibús. Si se podía ofrecer el WhatsApp y la llamada era en español, lo ofrece una sola vez: al cerrar, después de dar el punto de encuentro, o cuando el cliente ya está esperando en el punto y pregunta cada cuánto pasa el minibús (entonces lo ofrece con un enlace para ver el minibús en directo). Registra si lo ofreció, si el cliente aceptó y a qué punto de encuentro se refieren las indicaciones.
```

## Campos (parameters)

Todos son `type: string` y `required: true`.

1. **paso_por_consultas** (ejemplo: `no`): Indica si la llamada pasó por la fase de consultas del alquiler. Valores permitidos EXACTOS: "si", "no". Pon "si" si alguno de los tres datos técnicos de tema viene informado.
2. **tema_consulta** (ejemplo: `ninguno`): Tema principal que se trató en la fase de consultas. Valores permitidos EXACTOS: "prolongar", "recoger_tarde", "reserva_no_iniciada", "devolucion", "cargos_y_reembolsos", "requisitos", "durante_el_alquiler", "otro", "ninguno". Usa el dato técnico de tema que venga informado (triaje, punto de encuentro o información de oficina); si el cliente cambió de tema, pon el que más peso tuvo. Si no pasó por esa fase, pon "ninguno".
3. **consulta_resuelta** (ejemplo: `no_aplica`): Indica si el agente respondió la consulta con la información de sus instrucciones sin necesitar a una persona. Valores permitidos EXACTOS: "si", "no", "no_aplica". Pon "no" si hubo que transferir o si el cliente se quedó sin respuesta. Pon "no_aplica" si no pasó por esa fase.
4. **hubo_transferencia_consultas** (ejemplo: `no`): Indica si se pidió una transferencia desde la fase de consultas. Valores permitidos EXACTOS: "si", "no". Pon "si" si el dato técnico de extensión de esa fase viene informado, aunque no llegara a completarse.
5. **cola_destino_consultas** (ejemplo: `ninguna`): Cola a la que se transfirió desde la fase de consultas. Valores permitidos EXACTOS: "minibus", "asistencia", "gestion_reserva", "nueva_reserva", "ninguna". Compara la extensión con la TABLA DE COLAS. Si no hubo transferencia o no coincide, pon "ninguna".
6. **motivo_transferencia_consultas** (ejemplo: `ninguno`): Motivo de la transferencia de la fase de consultas. Valores permitidos EXACTOS: "no_iniciada", "web_no_disponible", "pregunta_reserva_concreta", "aseguradora", "enfado", "error_tecnico", "minibus", "asistencia", "nueva_reserva", "otro", "ninguno". Usa el dato técnico si viene informado. Si no hubo transferencia, pon "ninguno".
7. **dio_pasos_prolongacion** (ejemplo: `no_aplica`): Solo para consultas de prolongar. Indica si el agente llegó a dar los pasos de la web ("Mis reservas y facturas", "Gestionar mi reserva", "Prolongar mi reserva") o, si el cliente prefería una oficina, se lo recordó. Valores permitidos EXACTOS: "si", "no", "no_aplica".
8. **dio_precio_prohibido** (ejemplo: `no`): Indica si el agente dio un precio o una estimación de una prolongación, un importe concreto de la reserva del cliente o confirmó un dato de su reserva concreta (hora de devolución, días, si puede prolongar). Valores permitidos EXACTOS: "si", "no". Las tarifas generales de sus instrucciones (penalización, conductor adicional, sillas, salir de España, servicio de espera, multas, limpieza, cadenas) NO cuentan.
9. **invento_condicion** (ejemplo: `no`): Indica si el agente afirmó una condición, una cifra, un plazo o un servicio que no está entre los que tiene en sus instrucciones (por ejemplo un periodo de cortesía al devolver, un método de pago, un horario de oficina o que el seguro cubre los días extra). Valores permitidos EXACTOS: "si", "no".
10. **resumen_consulta** (ejemplo: `El cliente quería prolongar dos días; se le explicó la contraseña y los pasos de la web`): Resumen de UNA SOLA FRASE de la fase de consultas, en español, sin datos personales, máximo 25 palabras. Si no pasó por esa fase, pon "no_aplica".
11. **whatsapp_ofrecido** (ejemplo: `no`): Indica si el agente ofreció enviar las indicaciones del punto de encuentro por WhatsApp. Valores permitidos EXACTOS: "si", "no".
12. **whatsapp_aceptado** (ejemplo: `no`): Indica si el cliente aceptó claramente recibir las indicaciones por WhatsApp después de que el agente se lo ofreciera. Valores permitidos EXACTOS: "si", "no". Pon "si" solo si el agente lo ofreció y el cliente dijo que sí; cualquier duda, "no".
13. **punto_whatsapp** (ejemplo: `ninguno`): Punto de encuentro al que se refieren las indicaciones, como código. Valores permitidos EXACTOS: "MAD-T1", "MAD-T2", "MAD-T4", "SVQ" (Sevilla), "AGP" (Málaga), "ninguno". Es el punto cuya indicación dio el agente o, si el cliente ya estaba esperando en el punto, el punto donde espera. En Madrid elige la terminal que quede clara en la conversación o en el dato técnico de terminal. Pon "ninguno" si no se habló de ningún punto, si fue otro aeropuerto o la terminal tres de Madrid, o si no está claro cuál.
14. **idioma_cliente** (ejemplo: `es`): Idioma en que se habló con el cliente durante la mayor parte de la llamada. Valores permitidos EXACTOS: "es", "en", "it", "pt", "fr", "otro".
