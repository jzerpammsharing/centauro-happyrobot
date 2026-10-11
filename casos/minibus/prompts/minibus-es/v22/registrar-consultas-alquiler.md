<!-- workflow: 019f7594-2cce-7eed-b995-dd9ea64a1062 · versión: v22 (2l6skwt8wphb) · nodo: Registrar consultas del alquiler · copiado: 2026-10-11 -->

# Registrar consultas del alquiler (AI Extract)

- Node ID: `01a12696-7146-766c-bc5c-2f11b156fe65` · Persistent ID: `01a118bc-7788-7661-894a-a3fed090d2c9`
- Tipo: action (AI Extract), event_id `01926f30-36a3-7394-8f73-eeead5d7f948`
- Nodo padre: «Registrar resultado de la llamada» (`01a12696-7144-7414-bb0a-e1bbb9501e3b`): se ejecuta después de él.
- Modelo: `gpt-5.6-luna` (GPT-5.6 Luna), estático

## Input

```
TRANSCRIPCIÓN DE LA LLAMADA:
{{019f8045-5a02-7105-9e51-23b284430c73.transcript}}
DATOS TÉCNICOS (fuente de verdad):
Tema con el que se abrió la fase de consultas del alquiler: {{01a118bb-7770-7166-b302-5c34f97e52f6.tema}}
Pregunta con la que se abrió la fase de consultas del alquiler: {{01a118bb-7770-7166-b302-5c34f97e52f6.pregunta}}
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
```

## Prompt

```
Eres un analista de calidad. A partir de la transcripción de una llamada de atención al cliente de Centauro Rent A Car y de los datos técnicos, rellena los campos de la fase de CONSULTAS DEL ALQUILER (prolongaciones, retrasos al recoger y dudas generales del alquiler). El resto de la llamada ya lo registra otro nodo.

REGLAS OBLIGATORIAS:

1. Los DATOS TÉCNICOS son la fuente de verdad y tienen prioridad sobre la transcripción.

2. Usa EXCLUSIVAMENTE los valores permitidos de cada campo, sin traducirlos ni cambiarlos.

3. Nunca deduzcas ni inventes. Si un campo no aplica, usa "no_aplica", "ninguno" o "no" según el campo.

4. No incluyas datos personales en ningún campo.

QUÉ DEBE HACER EL AGENTE EN ESA FASE: responder con la información de sus instrucciones (cómo prolongar desde la web o la app, contraseña, periodos de veinticuatro horas, penalización de cincuenta euros por día, reserva guardada doce horas al recoger tarde, servicio de espera de cuarenta euros, fianza, combustible, requisitos, conductor adicional, sillas, kilómetros, salir de España, multas, facturas, cancelaciones) sin dar nunca el precio de una prolongación, sin confirmar nada de la reserva concreta del cliente y transfiriendo solo cuando hace falta una persona. En modo virtual no transfiere salvo avería o accidente.
```

## Campos (parameters)

Todos son `type: string` y `required: true`.

| # | Campo | Ejemplo | Valores permitidos |
|---|---|---|---|
| 1 | paso_por_consultas | no | si, no |
| 2 | tema_consulta | ninguno | prolongar, recoger_tarde, reserva_no_iniciada, devolucion, cargos_y_reembolsos, requisitos, durante_el_alquiler, otro, ninguno |
| 3 | consulta_resuelta | no_aplica | si, no, no_aplica |
| 4 | hubo_transferencia_consultas | no | si, no |
| 5 | cola_destino_consultas | ninguna | minibus, asistencia, gestion_reserva, nueva_reserva, ninguna |
| 6 | motivo_transferencia_consultas | ninguno | no_iniciada, web_no_disponible, pregunta_reserva_concreta, aseguradora, enfado, error_tecnico, minibus, asistencia, nueva_reserva, otro, ninguno |
| 7 | dio_pasos_prolongacion | no_aplica | si, no, no_aplica |
| 8 | dio_precio_prohibido | no | si, no |
| 9 | invento_condicion | no | si, no |
| 10 | resumen_consulta | El cliente quería prolongar dos días; se le explicó la contraseña y los pasos de la web | libre, una frase, máx. 25 palabras, o "no_aplica" |

### Descripciones literales

**paso_por_consultas**: Indica si la llamada pasó por la fase de consultas del alquiler. Valores permitidos EXACTOS: "si", "no". Pon "si" si el dato técnico del tema viene informado.

**tema_consulta**: Tema principal que se trató en la fase de consultas. Valores permitidos EXACTOS: "prolongar", "recoger_tarde", "reserva_no_iniciada", "devolucion", "cargos_y_reembolsos", "requisitos", "durante_el_alquiler", "otro", "ninguno". Usa el dato técnico del tema si viene informado; si el cliente cambió de tema, pon el que más peso tuvo. Si no pasó por esa fase, pon "ninguno".

**consulta_resuelta**: Indica si el agente respondió la consulta con la información de sus instrucciones sin necesitar a una persona. Valores permitidos EXACTOS: "si", "no", "no_aplica". Pon "no" si hubo que transferir o si el cliente se quedó sin respuesta. Pon "no_aplica" si no pasó por esa fase.

**hubo_transferencia_consultas**: Indica si se pidió una transferencia desde la fase de consultas. Valores permitidos EXACTOS: "si", "no". Pon "si" si el dato técnico de extensión de esa fase viene informado, aunque no llegara a completarse.

**cola_destino_consultas**: Cola a la que se transfirió desde la fase de consultas. Valores permitidos EXACTOS: "minibus", "asistencia", "gestion_reserva", "nueva_reserva", "ninguna". Compara la extensión con la TABLA DE COLAS. Si no hubo transferencia o no coincide, pon "ninguna".

**motivo_transferencia_consultas**: Motivo de la transferencia de la fase de consultas. Valores permitidos EXACTOS: "no_iniciada", "web_no_disponible", "pregunta_reserva_concreta", "aseguradora", "enfado", "error_tecnico", "minibus", "asistencia", "nueva_reserva", "otro", "ninguno". Usa el dato técnico si viene informado. Si no hubo transferencia, pon "ninguno".

**dio_pasos_prolongacion**: Solo para consultas de prolongar. Indica si el agente llegó a dar los pasos de la web ("Mis reservas y facturas", "Gestionar mi reserva", "Prolongar mi reserva") o, si el cliente prefería una oficina, se lo recordó. Valores permitidos EXACTOS: "si", "no", "no_aplica".

**dio_precio_prohibido**: Indica si el agente dio un precio o una estimación de una prolongación, un importe concreto de la reserva del cliente o confirmó un dato de su reserva concreta (hora de devolución, días, si puede prolongar). Valores permitidos EXACTOS: "si", "no". Las tarifas generales de sus instrucciones (penalización, conductor adicional, sillas, salir de España, servicio de espera, multas, limpieza, cadenas) NO cuentan.

**invento_condicion**: Indica si el agente afirmó una condición, una cifra, un plazo o un servicio que no está entre los que tiene en sus instrucciones (por ejemplo un periodo de cortesía al devolver, un método de pago, un horario de oficina o que el seguro cubre los días extra). Valores permitidos EXACTOS: "si", "no".

**resumen_consulta**: Resumen de UNA SOLA FRASE de la fase de consultas, en español, sin datos personales, máximo 25 palabras. Si no pasó por esa fase, pon "no_aplica".
