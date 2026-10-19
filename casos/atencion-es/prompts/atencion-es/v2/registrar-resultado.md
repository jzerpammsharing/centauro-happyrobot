<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v2 (x8xd0llbdp3j) · nodo: Registrar resultado de la llamada · copiado: 2026-10-19 (Tarea 13) -->

# Registrar resultado de la llamada (AI Extract) · extract único

- Tipo: action (AI Extract), event_id `01926f30-36a3-7394-8f73-eeead5d7f948`. ID de nodo en la v2
  `01a14f1d-0395-7611-80cf-234e9e9fcf11` · persistent_id `aea14d45-81de-4a98-aaae-d45c89421f34`. Padre: Receive Customer Call.
- Modelo: GPT-5.6 Luna (`gpt-5.6-luna`, comprobado con el esquema del nodo).
- Spec §5.12. Junta el extract de la v25 («Registrar resultado de la llamada» y «Registrar consultas del alquiler») y el
  de Prolongaciones v12. Las salidas se leen como `{{aea14d45-81de-4a98-aaae-d45c89421f34.response.<campo>}}`; la rama de
  WhatsApp («Preparar WhatsApp minibús») lee `whatsapp_aceptado`, `punto_whatsapp` e `idioma_cliente`.
- Copia de lo subido por API el 19/10/2026 (en HappyRobot la configuración va en JSON de Plate: una línea = un párrafo).

## Prompt

Eres un analista de calidad. A partir de la transcripción de una llamada al asistente de IA de Centauro Rent a Car en España y de los datos técnicos que se te aportan, rellena los campos de resultado para analítica.

REGLAS OBLIGATORIAS:
1. Los DATOS TÉCNICOS son la fuente de verdad y tienen prioridad sobre la transcripción. Un dato técnico vacío quiere decir que esa herramienta no se usó en la llamada.
2. Usa EXCLUSIVAMENTE los valores permitidos de cada campo, sin traducirlos ni cambiar mayúsculas ni guiones bajos. En los campos de lista, separa los valores con comas, sin espacios.
3. No deduzcas ni inventes. Si un campo no aplica, usa el valor que su descripción indica para ese caso.
4. Registra SIEMPRE todos los campos, haya o no transferencia.
5. En los campos numéricos devuelve solo el número.
6. Ningún campo lleva datos personales: ni nombres, ni correos (tampoco su dominio), ni fechas de nacimiento, ni números de reserva, ni matrículas, ni teléfonos. Los datos técnicos de enviar_correo_contrasena y pista_correo los traen: úsalos solo para saber si esas herramientas se usaron.
7. Evalúa SOLO los turnos del asistente anteriores a la transferencia. Si hubo transferencia, lo que dice después el compañero humano no cuenta para nada: ni para la calidad ni para decidir si el asistente resolvió.

CÓMO FUNCIONA EL ASISTENTE:
Se llama Daniel. Atiende dos opciones del menú telefónico: Minibús (punto de encuentro del minibús de los aeropuertos e información de oficinas) y Prolongación (alargar un alquiler en curso). Tiene cinco módulos y pasa de uno a otro con herramientas, sin anunciarlo:
- triaje: saluda, averigua el motivo y encamina con buscar_punto_de_encuentro, informacion_oficina, prolongar_alquiler o consultas_alquiler. Transfiere él mismo las averías y los accidentes (asistencia), las reservas nuevas (nueva_reserva), las quejas del minibús (minibus) y los datos concretos de una reserva que hay que mirar o cambiar (gestion, solo con Gestión abierta).
- punto_encuentro: punto de encuentro del minibús de un aeropuerto, horario nocturno de las oficinas de aeropuerto, quejas del minibús y oferta del WhatsApp con las indicaciones (solo Madrid terminales uno, dos y cuatro, Sevilla y Málaga, en español).
- informacion_oficina: horario de una oficina, cómo llegar y dónde devolver el coche.
- prolongacion: cómo prolongar en la web o la app, la contraseña del área de cliente (puede enviar el correo para crearla con enviar_correo_contrasena y, si el cliente no sabe su correo, identificarlo por número de reserva con pista_correo), devolver tarde, coche de aseguradora o de empresa y «la web no me deja».
- consultas: el resto de dudas del alquiler, con buscar_respuesta, que devuelve el texto del tema consultado.
Cada módulo tiene volver_al_triaje y transfer_to_human_agent. Tras dos cambios de módulo sin resolver, al tercero debe transferir o, si no hay a quién, dar el horario y cerrar.

TRANSFERENCIAS:
transfer_to_human_agent lleva la cola elegida (gestion, asistencia, nueva_reserva, minibus) y el motivo. En triaje, prolongacion y consultas, «Preparar transferencia» decide si se transfiere: «transferir» (se intenta), «gestion_cerrada» (se pidió gestion fuera de su horario: no se transfiere), «modo_virtual» (de 22:00 a 8:00 solo se transfiere a asistencia: no se transfiere) o «cola_no_valida». En punto_encuentro e informacion_oficina la cola pedida va directa a la transferencia. Gestión abre de lunes a viernes de 8:00 a 21:00, salvo festivos nacionales.

QUÉ NO ES UN FALLO:
La penalización de cincuenta euros por día, las tarifas generales que el asistente tiene en sus instrucciones (conductor adicional, sillas, servicio de espera, salir de España, limpieza, multas, cadenas) y los teléfonos de las oficinas de Benidorm y Torrevieja son información correcta. Tampoco son invento el horario de Gestión, «si es urgente, vaya a la oficina», el formulario de contacto ni el punto de encuentro o el horario que devuelve una herramienta.

SÍ SON INVENTOS (ejemplos vistos en pruebas):
- que para añadir un conductor con el alquiler en curso tienen que ir los dos juntos a la oficina, o que el nuevo conductor tiene que llevar DNI y carnet;
- que si el alquiler es de una agencia «no se devuelve nada» (lo correcto es que lo consulte con su agencia);
- «esté atento al correo» o prometer que le escribirán o le llamarán, sin que ninguna herramienta haya enviado nada;
- un precio, un plazo, una hora de cortesía, un método de pago, un horario, un punto de encuentro, una dirección o un teléfono que no le ha dado una herramienta ni están en sus instrucciones; confirmar o deducir datos de la reserva concreta del cliente.

## Entrada (input)

Una línea por párrafo; `{{persistent_id.variable}}` es un nodo de variable de Plate.

```
TRANSCRIPCIÓN DE LA LLAMADA:
{{300ae88d-ccb2-466c-a914-9f9090363a74.transcript}}
DATOS TÉCNICOS (fuente de verdad; vacío = esa herramienta no se usó):
== Copiados de la entrada (Contexto de la llamada) ==
Opción del menú (minibus | prolongacion): {{e51cd732-f403-4ef7-95d4-490347960a93.opcion_menu}}
Origen de la opción (linea | prueba | por_defecto): {{e51cd732-f403-4ef7-95d4-490347960a93.origen_opcion}}
Idioma de la línea (es | en): {{e51cd732-f403-4ef7-95d4-490347960a93.idioma}}
Modo virtual, de 22:00 a 8:00 y sin compañeros salvo asistencia (true/false): {{e51cd732-f403-4ef7-95d4-490347960a93.modo_virtual}}
Gestión abierta al empezar la llamada (true/false): {{e51cd732-f403-4ef7-95d4-490347960a93.gestion_abierta}}
Festivo nacional (true/false): {{e51cd732-f403-4ef7-95d4-490347960a93.festivo_nacional}}
Se podía ofrecer el WhatsApp a este número (true/false): {{e51cd732-f403-4ef7-95d4-490347960a93.whatsapp_disponible}}
== Llamada (Receive Customer Call) ==
Duración de la llamada (segundos): {{300ae88d-ccb2-466c-a914-9f9090363a74.duration}}
Número total de llamadas a herramientas: {{300ae88d-ccb2-466c-a914-9f9090363a74.num_tool_calls}}
Número de turnos del asistente: {{300ae88d-ccb2-466c-a914-9f9090363a74.num_assistant_turns}}
Sentimiento detectado: {{300ae88d-ccb2-466c-a914-9f9090363a74.sentiment}}
== Módulo TRIAJE ==
buscar_punto_de_encuentro, aeropuerto: {{72261523-5d3f-4830-ac36-67ab187d93ed.aeropuerto}}
buscar_punto_de_encuentro, terminal: {{72261523-5d3f-4830-ac36-67ab187d93ed.terminal}}
informacion_oficina, tema: {{414b964d-bb29-428a-b9a1-92b1a3a8d6be.tema}}
informacion_oficina, oficina: {{414b964d-bb29-428a-b9a1-92b1a3a8d6be.oficina}}
prolongar_alquiler, situacion: {{01a14f69-b092-7e6d-9203-c968520c1670.situacion}}
consultas_alquiler, tema: {{414bdc8c-aacc-4125-b323-acc6a2ae3373.tema}}
consultas_alquiler, pregunta: {{414bdc8c-aacc-4125-b323-acc6a2ae3373.pregunta}}
transfer_to_human_agent, cola: {{17c682a0-82d2-42f6-88fa-817d8cba0783.cola}}
transfer_to_human_agent, motivo_transferencia: {{17c682a0-82d2-42f6-88fa-817d8cba0783.motivo_transferencia}}
Preparar transferencia, resultado: {{01a14f64-277b-7226-8e39-a8ef0274949f.resultado}}
Transferencia completada: {{01a14f66-5252-70a4-81ad-fa8d1cc6b438.transfer_succeeded}}
== Módulo PUNTO DE ENCUENTRO ==
consultas_alquiler, tema: {{3f1c2be8-8768-455f-895b-047063ea7938.tema}}
consultas_alquiler, pregunta: {{3f1c2be8-8768-455f-895b-047063ea7938.pregunta}}
informacion_oficina, motivo: {{01a155d9-5db0-7106-ab47-43027e0f8647.motivo}}
informacion_oficina, tema: {{01a155d9-5db0-7106-ab47-43027e0f8647.tema}}
informacion_oficina, oficina: {{01a155d9-5db0-7106-ab47-43027e0f8647.oficina}}
volver_al_triaje, motivo: {{01a155d9-5d9b-7fd6-bfaa-6b87ccd6ac42.motivo}}
transfer_to_human_agent, cola: {{00435498-eccf-4110-9cf1-eb17821af3ed.cola}}
transfer_to_human_agent, motivo_transferencia: {{00435498-eccf-4110-9cf1-eb17821af3ed.motivo_transferencia}}
Transferencia completada (sin «Preparar transferencia» en este módulo): {{37fb8053-214e-4357-be80-0fc8f832ecbc.transfer_succeeded}}
== Módulo INFORMACIÓN DE OFICINA ==
consultas_alquiler, tema: {{6edd13ac-b226-4d1c-87dc-748b46ce5638.tema}}
consultas_alquiler, pregunta: {{6edd13ac-b226-4d1c-87dc-748b46ce5638.pregunta}}
buscar_punto_de_encuentro, motivo: {{01a155d9-5db4-757d-ac17-fc1adb754b0f.motivo}}
buscar_punto_de_encuentro, aeropuerto: {{01a155d9-5db4-757d-ac17-fc1adb754b0f.aeropuerto}}
buscar_punto_de_encuentro, terminal: {{01a155d9-5db4-757d-ac17-fc1adb754b0f.terminal}}
volver_al_triaje, motivo: {{01a155d9-5da4-74b3-a7c4-3bb6257242d6.motivo}}
transfer_to_human_agent, cola: {{62c5b6dd-5dde-4b3a-9a93-adb638c0bd66.cola}}
transfer_to_human_agent, motivo_transferencia: {{62c5b6dd-5dde-4b3a-9a93-adb638c0bd66.motivo_transferencia}}
Transferencia completada (sin «Preparar transferencia» en este módulo): {{faec6a20-257a-4b8c-8c75-8dd336beead7.transfer_succeeded}}
== Módulo PROLONGACIÓN ==
enviar_correo_contrasena, email (dato personal: no lo copies): {{01a150c7-08df-73fd-abac-19c873b9533d.email}}
enviar_correo_contrasena, nombre_completo (dato personal: no lo copies): {{01a150c7-08df-73fd-abac-19c873b9533d.nombre_completo}}
enviar_correo_contrasena, fecha_nacimiento (dato personal: no la copies): {{01a150c7-08df-73fd-abac-19c873b9533d.fecha_nacimiento}}
Resultado del último envío del correo de contraseña: {{01a150c7-091b-7abf-a101-539b1b7ec049.resultado}}
Correo enviado en el último intento (true/false): {{01a150c7-091b-7abf-a101-539b1b7ec049.enviado}}
pista_correo, numero_reserva (dato personal: no lo copies): {{01a150c7-0928-79dc-a21c-4d9348ca038d.numero_reserva}}
pista_correo, nombre_completo (dato personal: no lo copies): {{01a150c7-0928-79dc-a21c-4d9348ca038d.nombre_completo}}
pista_correo, fecha_nacimiento (dato personal: no la copies): {{01a150c7-0928-79dc-a21c-4d9348ca038d.fecha_nacimiento}}
Pista del correo, resultado (verificado | no_verificado | dato_no_interpretado | no_disponible): {{01a150c7-0940-76a7-8129-f132e4373895.resultado}}
buscar_respuesta, tema: {{01a150c9-677e-791b-8f74-957f60586f02.tema}}
buscar_respuesta, pregunta: {{01a150c9-677e-791b-8f74-957f60586f02.pregunta}}
Buscar respuesta, encontrado: {{01a150c9-6786-7e05-95c4-8007aa1e06d4.encontrado}}
informacion_oficina, motivo: {{01a155d9-5dbb-704a-b119-2db7b00a6fa2.motivo}}
informacion_oficina, tema: {{01a155d9-5dbb-704a-b119-2db7b00a6fa2.tema}}
informacion_oficina, oficina: {{01a155d9-5dbb-704a-b119-2db7b00a6fa2.oficina}}
volver_al_triaje, motivo: {{01a155d9-5da8-738a-8af4-ada5f82ebdd7.motivo}}
transfer_to_human_agent, cola: {{01a150ca-b67d-726a-845b-19c18b2e891e.cola}}
transfer_to_human_agent, motivo_transferencia: {{01a150ca-b67d-726a-845b-19c18b2e891e.motivo_transferencia}}
Preparar transferencia, resultado: {{01a150ca-b684-7698-a2ff-ccdefe784483.resultado}}
Transferencia completada: {{01a150ca-dc8b-73ca-84c2-08eca941b971.transfer_succeeded}}
== Módulo CONSULTAS DEL ALQUILER ==
buscar_respuesta, tema: {{01a14fa1-5c34-7bff-9366-aa7e9e4e448a.tema}}
buscar_respuesta, pregunta: {{01a14fa1-5c34-7bff-9366-aa7e9e4e448a.pregunta}}
Buscar respuesta, encontrado: {{01a14fa1-5c44-7c37-821c-1d01c0bd41eb.encontrado}}
buscar_punto_de_encuentro, aeropuerto: {{eda4aa10-c99e-4319-b7ae-dbf5dc6db949.aeropuerto}}
buscar_punto_de_encuentro, terminal: {{eda4aa10-c99e-4319-b7ae-dbf5dc6db949.terminal}}
informacion_oficina, tema: {{0be9b6d8-9353-41de-8049-c2e477ed6668.tema}}
informacion_oficina, oficina: {{0be9b6d8-9353-41de-8049-c2e477ed6668.oficina}}
prolongar_alquiler, motivo: {{01a155d9-5db8-7b78-8ecd-d52451c7ed84.motivo}}
prolongar_alquiler, situacion: {{01a155d9-5db8-7b78-8ecd-d52451c7ed84.situacion}}
volver_al_triaje, motivo: {{01a155d9-5dac-7449-b143-4392c795602f.motivo}}
transfer_to_human_agent, cola: {{fbe2e40e-4915-4f44-9bac-59c318862e97.cola}}
transfer_to_human_agent, motivo_transferencia: {{fbe2e40e-4915-4f44-9bac-59c318862e97.motivo_transferencia}}
Preparar transferencia, resultado: {{01a14fa7-1147-724b-af62-e10108d91bce.resultado}}
Transferencia completada: {{01a14fa7-4228-7812-a6b7-aa42c035b190.transfer_succeeded}}
== Cambios de módulo (veces que se ejecutó cada Module Change; vacío = 0) ==
Punto de encuentro → Triaje: {{01a155e8-f3f3-7d25-a6cf-f788cbfee0b4.callCount}}
Información de oficina → Triaje: {{01a155ec-a9e8-733d-a286-a38da5f0b411.callCount}}
Prolongación → Triaje: {{01a155ec-37d2-7d99-b8b8-d4e83069c3ba.callCount}}
Consultas → Triaje: {{01a155ed-9634-753f-b55c-de35edd40c1d.callCount}}
Punto de encuentro → Información de oficina: {{01a155e8-59fa-7a49-ba5b-ca96f22b2050.callCount}}
Información de oficina → Punto de encuentro: {{01a155ec-dcfc-730e-9c8c-daa3bfbc19ae.callCount}}
Consultas → Prolongación: {{01a155ee-138f-7765-954f-20ec0b421975.callCount}}
Prolongación → Información de oficina: {{01a155ec-665d-7f0f-86b1-c070b229aa53.callCount}}
Punto de encuentro → Consultas: {{7f70daef-fdf6-4f51-86b0-43a61e626efc.callCount}}
Información de oficina → Consultas: {{9661e3bd-a18e-477b-8076-96c76caae15b.callCount}}
Consultas → Punto de encuentro: {{081b2d5c-d7cf-49b7-b0a1-70c82ee5aac7.callCount}}
Consultas → Información de oficina: {{91b601ad-4782-44fb-955a-5bc42657c191.callCount}}
```

## Parámetros (46, todos obligatorios)

| Campo | Tipo | Ejemplo | Descripción |
|---|---|---|---|
| opcion_menu | string | minibus | Copia el dato técnico «Opción del menú» (no lo decides tú). Valores EXACTOS: "minibus", "prolongacion". Si viene vacío, "minibus". |
| origen_opcion | string | linea | Copia el dato técnico «Origen de la opción» (no lo decides tú). Valores EXACTOS: "linea", "prueba", "por_defecto". Si viene vacío, "por_defecto". |
| idioma_linea | string | es | Copia el dato técnico «Idioma de la línea» (no lo decides tú; es el de la línea marcada, no el que habló el cliente). Valores EXACTOS: "es", "en". Si viene vacío, "es". |
| modo_virtual | string | no | Copia el dato técnico «Modo virtual»: "true" es "si" y "false" es "no". Valores EXACTOS: "si", "no". Si viene vacío, "no". |
| gestion_abierta | string | si | Copia el dato técnico «Gestión abierta al empezar la llamada»: "true" es "si" y "false" es "no". Valores EXACTOS: "si", "no". Si viene vacío, "no". |
| festivo_nacional | string | no | Copia el dato técnico «Festivo nacional»: "true" es "si" y "false" es "no". Valores EXACTOS: "si", "no". Si viene vacío, "no". |
| motivo_principal | string | punto_encuentro | Motivo principal por el que llamó el cliente (lo que más pesó). Valores EXACTOS: "punto_encuentro", "info_oficina", "prolongar", "web_no_deja", "devolver_tarde", "aseguradora_empresa", "reserva_no_iniciada", "recoger_tarde", "devolucion", "cargos_reembolsos", "requisitos", "durante_alquiler", "dato_reserva", "reserva_nueva", "averia", "persona_sin_motivo", "queja_minibus", "otro", "desconocido". "punto_encuentro": minibús o punto de encuentro de un aeropuerto, incluido el horario nocturno de una oficina de aeropuerto. "info_oficina": horario, dirección o cómo llegar a una oficina, o dónde devolver el coche. "prolongar": alargar un alquiler en curso o cómo hacerlo, incluida la contraseña del área de cliente para prolongar. "web_no_deja": ya lo intentó en la web o la app y no le deja. "devolver_tarde": devolver más tarde de la hora. "aseguradora_empresa": coche de una aseguradora o de una empresa. "reserva_no_iniciada", "recoger_tarde", "devolucion" (devolver antes o en otra oficina), "cargos_reembolsos" (fianza, combustible, cargos, multas, facturas, reembolsos), "requisitos", "durante_alquiler": dudas del alquiler de esos temas. "dato_reserva": un dato concreto de su reserva que hay que mirar o cambiar. "reserva_nueva": hacer una reserva nueva. "averia": avería o accidente. "persona_sin_motivo": pide una persona sin decir para qué. "queja_minibus": queja del minibús (no pasa, se fue, lleva mucho esperando). "otro": otra cosa. "desconocido": no llegó a decir el motivo (cuelga, silencio, prueba, equivocación). |
| motivos_secundarios | string | ninguno | Otros motivos que el cliente planteó además del principal, en el orden en que salieron, con los mismos valores EXACTOS de motivo_principal (salvo "desconocido"), separados por comas y sin repetir. Si no hubo otro, "ninguno". |
| resuelto_por_bot | string | si | Si el asistente resolvió lo que el cliente necesitaba sin una persona. Valores EXACTOS: "si", "no", "parcial". "si": dio la respuesta o la indicación que el cliente necesitaba y no hubo transferencia. "parcial": resolvió uno de los motivos pero otro quedó sin resolver o acabó en transferencia. "no": hubo transferencia por el motivo principal, el cliente se quedó sin respuesta, colgó antes o el asistente falló. |
| motivo_no_resuelto | string | ninguno | Por qué no se resolvió (o la parte no resuelta). Valores EXACTOS: "necesita_cambio_reserva", "necesita_dato_reserva", "pide_persona", "reserva_nueva", "averia", "cuelga_o_corte", "fallo_bot", "sin_respuesta_en_catalogo", "gestion_cerrada", "ninguno". "necesita_cambio_reserva": hay que cambiar algo de su reserva. "necesita_dato_reserva": hay que mirar un dato de su reserva. "pide_persona": pidió una persona sin un motivo que el asistente pudiera atender. "reserva_nueva", "averia": se transfirió por eso. "cuelga_o_corte": el cliente colgó o se cortó antes de resolver. "fallo_bot": el asistente se equivocó, se atascó, no entendió o una herramienta falló. "sin_respuesta_en_catalogo": la pregunta no está en lo que sabe el asistente (buscar_respuesta no la tenía). "gestion_cerrada": necesitaba a Gestión (o a un compañero en modo virtual) y no había, y se le dio el horario. Si resuelto_por_bot es "si", "ninguno". |
| modulos_visitados | string | triaje,punto_encuentro | Módulos por los que pasó la llamada, en el orden de la primera visita y sin repetir. Valores EXACTOS: "triaje", "punto_encuentro", "informacion_oficina", "prolongacion", "consultas", separados por comas. Siempre empieza por "triaje". Se entra en punto_encuentro con buscar_punto_de_encuentro, en informacion_oficina con informacion_oficina, en prolongacion con prolongar_alquiler y en consultas con consultas_alquiler (desde cualquier módulo); volver_al_triaje vuelve a triaje. Usa los datos técnicos de esas herramientas y los cambios de módulo. |
| saltos | number | 0 | Número de cambios de módulo después del primer encaminamiento del triaje: suma los datos técnicos de «Cambios de módulo» (un vacío vale 0). La primera entrada desde el triaje en un módulo no cuenta; cada cambio entre módulos y cada vuelta al triaje cuentan uno. Si todos vienen vacíos, 0. Solo el número. |
| modulo_final | string | punto_encuentro | Módulo en el que estaba la llamada al terminar o al transferir. Valores EXACTOS: "triaje", "punto_encuentro", "informacion_oficina", "prolongacion", "consultas". |
| hubo_transferencia | string | no | Si se intentó pasar la llamada a un compañero. Valores EXACTOS: "si", "no". "si" si algún «Preparar transferencia» trae "transferir", o si en punto_encuentro o informacion_oficina viene informada la cola de transfer_to_human_agent, aunque la transferencia no llegara a completarse. "no" si no se pidió ninguna o si «Preparar transferencia» la paró ("gestion_cerrada", "modo_virtual", "cola_no_valida"). |
| cola_destino | string | ninguna | Cola de la transferencia intentada (la última si hubo varias). Valores EXACTOS: "gestion", "asistencia", "nueva_reserva", "minibus", "ninguna". Usa la cola del dato técnico de transfer_to_human_agent de ese módulo. Si hubo_transferencia es "no", "ninguna". |
| motivo_transferencia | string | ninguno | Motivo de la transferencia intentada. Valores EXACTOS: "no_iniciada", "web_no_disponible", "pregunta_reserva_concreta", "aseguradora", "enfado", "error_tecnico", "minibus", "asistencia", "nueva_reserva", "correo_no_coincide", "otro", "ninguno". Usa el motivo_transferencia del dato técnico de ese módulo si es uno de esos valores; si viene vacío, dedúcelo de la transcripción. Si hubo_transferencia es "no", "ninguno". |
| modulo_transferencia | string | ninguno | Módulo desde el que se intentó la transferencia (el del dato técnico informado). Valores EXACTOS: "triaje", "punto_encuentro", "informacion_oficina", "prolongacion", "consultas", "ninguno". Si hubo_transferencia es "no", "ninguno". |
| intento_gestion_cerrada | string | no | Si el asistente intentó transferir a gestion con Gestión cerrada. Valores EXACTOS: "si", "no". "si" si algún «Preparar transferencia» trae "gestion_cerrada", o si en punto_encuentro o informacion_oficina la cola es "gestion" y Gestión estaba cerrada (dato técnico false). En otro caso, "no". |
| necesitaba_contrasena | string | no | Valores EXACTOS: "si", "no". "si" si el cliente no había entrado nunca en su área de cliente o no recordaba la contraseña y eso le impedía prolongar o gestionar su reserva. |
| dio_pasos_prolongacion | string | no_aplica | Si el asistente dio los pasos para prolongar en la web («Mis reservas y facturas», «Gestionar mi reserva», «Prolongar mi reserva») o, si el cliente prefería, le recordó que puede hacerlo en una oficina. Valores EXACTOS: "si", "no", "no_aplica". "no_aplica" si la llamada no trataba de prolongar. |
| correo_contrasena_ofrecido | string | no | Valores EXACTOS: "si", "no". "si" si el asistente ofreció enviarle él el correo para crear o restablecer la contraseña. |
| correo_contrasena_resultado | string | no_intentado | Valores EXACTOS: "enviado", "no_coincide", "dato_no_interpretado", "no_disponible", "no_intentado". Usa SOLO el dato técnico «Resultado del último envío del correo de contraseña» si es uno de esos valores; si viene vacío, "no_intentado", aunque vengan otros datos de enviar_correo_contrasena. |
| envios_correo | number | 0 | Veces que el asistente ejecutó enviar_correo_contrasena (0, 1 o 2), contadas en la transcripción. Si no se puede saber: 0 si correo_contrasena_resultado es "no_intentado" y 1 en otro caso. Solo el número. |
| correo_recibido_confirmado | string | no | Valores EXACTOS: "si", "no". "si" solo si el cliente dijo durante la llamada que le había llegado el correo de la contraseña. |
| motivo_no_envio | string | no_aplica | Por qué no se envió el correo de contraseña. Valores EXACTOS: "no_aplica" (se envió, o la llamada no trataba de entrar en la cuenta), "ya_tiene_contrasena", "no_lo_quiere", "no_quiere_dar_datos", "no_puede_abrir_correo", "reserva_no_iniciada" (su reserva aún no ha empezado: no se ofrece el envío), "no_coincide", "no_disponible" (la herramienta no estaba disponible o no se interpretó un dato), "otro". |
| pista_correo_usada | string | no | Valores EXACTOS: "si", "no". Mira SOLO el dato técnico «Pista del correo, resultado»: "si" si trae un valor (se intentó identificar al cliente por número de reserva); "no" si viene vacío, aunque vengan otros datos de pista_correo. |
| temas_consultados | string | ninguno | Temas que el asistente consultó con buscar_respuesta (en prolongacion o en consultas), sin repetir y separados por comas. Valores EXACTOS: "reserva_no_iniciada", "recoger_tarde", "devolucion", "cargos_y_reembolsos", "requisitos", "durante_el_alquiler", "otras", "telefonos", "detalles_prolongacion", "la_web_no_le_deja", "aseguradora_empresa", "devolver_tarde". Usa los datos técnicos de buscar_respuesta y, si hubo varias consultas, la transcripción. Si no se usó, "ninguno". |
| pregunta_sin_respuesta | string | ninguna | Si el cliente hizo una pregunta del alquiler que el asistente no supo contestar (no estaba en lo que devolvió buscar_respuesta ni en sus instrucciones), escríbela en UNA frase corta en español, sin datos personales, como la haría cualquier cliente. Si no hubo, "ninguna". |
| aeropuerto_detectado | string | desconocido | Aeropuerto en el que estaba el cliente. Usa el aeropuerto de buscar_punto_de_encuentro (de cualquier módulo); si viene vacío, el que dijo el cliente, tal cual. Si no dijo ninguno, "desconocido". |
| terminal_detectada | string | desconocido | Terminal del cliente. Usa la terminal de buscar_punto_de_encuentro; si viene vacía, la que mencionó el cliente. Si no mencionó ninguna, "desconocido". Nunca la deduzcas. |
| punto_encuentro_entregado | string | no | Valores EXACTOS: "si", "no". "si" solo si el asistente le explicó dónde esperar el minibús o adónde ir. |
| aeropuerto_sin_datos | string | no | Valores EXACTOS: "si", "no". "si" solo si el asistente no tenía la indicación de ese aeropuerto o de esa oficina y tuvo que remitir al correo de confirmación o a un compañero por falta de datos. |
| oficina_consultada | string | desconocido | Oficina por la que preguntó el cliente (horario, cómo llegar o devolución). Usa la oficina de informacion_oficina (de cualquier módulo); si viene vacía, la que se identificó en la transcripción. Si no hubo, "desconocido". |
| informacion_oficina_entregada | string | no | Valores EXACTOS: "si", "no". "si" solo si el asistente dio el horario de una oficina, cómo llegar o dónde devolver el coche. |
| whatsapp_ofrecido | string | no | Valores EXACTOS: "si", "no". "si" si el asistente ofreció enviar las indicaciones del punto de encuentro por WhatsApp. |
| whatsapp_aceptado | string | no | Valores EXACTOS: "si", "no". "si" solo si el asistente lo ofreció y el cliente dijo claramente que sí; ante cualquier duda, "no". Este campo decide si se envía el WhatsApp. |
| punto_whatsapp | string | ninguno | Punto de encuentro cuya indicación dio el asistente, como código. Valores EXACTOS: "MAD-T1", "MAD-T2", "MAD-T4", "SVQ" (Sevilla), "AGP" (Málaga), "ninguno". En Madrid, la terminal cuya indicación dio. "ninguno" si no dio indicación, si fue otro aeropuerto o si no está claro. |
| idioma_cliente | string | es | Idioma en que se habló con el cliente la mayor parte de la llamada. Valores EXACTOS: "es", "en", "it", "pt", "fr", "otro". |
| invento_informacion | string | no | Si el asistente, antes de la transferencia, afirmó algo que no le dio una herramienta ni está en sus instrucciones. Valores EXACTOS: "si", "no". Sigue las listas QUÉ NO ES UN FALLO y SÍ SON INVENTOS. Sé estricto, pero no marques "si" por lo que devolvió una herramienta. |
| pregunta_repetida | string | no | Valores EXACTOS: "si", "no". "si" si el asistente repitió una pregunta ya respondida (también tras un cambio de módulo), hizo dos preguntas en un mismo turno o hizo la misma pregunta más de dos veces. Reformular una vez lo que no se entendió no cuenta. |
| valido_antes_de_informar | string | no_aplica | Solo si el cliente estuvo molesto. Valores EXACTOS: "si", "no", "no_aplica". "si" si el asistente validó su emoción antes de dar información o de anunciar la transferencia; "no" si le soltó el dato o la transferencia en seco; "no_aplica" si no hubo molestia. |
| cliente_molesto | string | no | Valores EXACTOS: "si", "no". "si" si el cliente mostró enfado, frustración, reproches o tuvo que insistir. La prisa sola no cuenta. |
| verbalizacion_acciones_internas | number | 0 | Veces que el asistente narró una acción interna («voy a consultar el sistema», «estoy buscando», «le paso al módulo de…», «un momento que reviso»). La frase de aviso de la transferencia («le paso con un compañero») no cuenta. Solo el número. |
| tuteo | string | no | Valores EXACTOS: "si", "no". "si" solo si el asistente (no el cliente ni el compañero humano) se dirigió al cliente de tú en español: «puedes», «tienes», «te paso», «dime», «tu reserva». «Puede», «tiene», «le paso», «dígame», «su reserva», «entre», «no cuelgue» son de usted y no cuentan. En otros idiomas, "no". |
| resumen | string | Cliente en Málaga pidió el punto de encuentro; se le dio y aceptó el WhatsApp | Resumen de UNA SOLA FRASE de la llamada, en español, sin saltos de línea, de 25 palabras como mucho y sin datos personales. |
| turnos_agente | number | 6 | Turnos de habla del asistente. Usa el dato técnico «Número de turnos del asistente» si viene informado; si no, cuéntalos en la transcripción. Solo el número. |

## Rama de WhatsApp («Preparar WhatsApp minibús»)

Mismo código de la v25 (copia en `../v1/preparar-whatsapp-minibus.md`); solo cambian tres entradas, que pasan a leer
este extract:

```json
[
  {"key": "from_number", "value": "{{33c2681a-9160-413c-8010-e455bd4023c6.from_number}}"},
  {"key": "whatsapp_aceptado", "value": "{{aea14d45-81de-4a98-aaae-d45c89421f34.response.whatsapp_aceptado}}"},
  {"key": "punto_whatsapp", "value": "{{aea14d45-81de-4a98-aaae-d45c89421f34.response.punto_whatsapp}}"},
  {"key": "idioma_cliente", "value": "{{aea14d45-81de-4a98-aaae-d45c89421f34.response.idioma_cliente}}"}
]
```

La rama sigue colgando de «Registrar consultas del alquiler» (`15bf240b-…`), que ya no alimenta nada: moverla bajo
este extract y borrar después «Registrar consultas del alquiler» lo hace una persona en el editor (R42,
`docs/pendientes.md`).

## Prueba con `test_node` (19/10/2026, 23:48)

Salidas de prueba puestas con `set_custom_output` (datos inventados): una llamada que entra por el Triaje con una duda
de devolver antes (`consultas_alquiler` → `buscar_respuesta` tema `devolucion`), salta a Prolongación
(`prolongar_alquiler` de Consultas, Module Change `01a155ee-…` con `callCount` 1), recibe los pasos para prolongar y
se transfiere a asistencia por una avería («Preparar transferencia» = `transferir`, `transfer_succeeded` true). Los
46 campos salen con un valor permitido: `modulos_visitados` = `triaje,consultas,prolongacion`, `saltos` = 1,
`hubo_transferencia` = si, `cola_destino` = asistencia, `modulo_transferencia` = prolongacion, `resuelto_por_bot` =
parcial, `motivo_no_resuelto` = averia, `temas_consultados` = devolucion, `dio_pasos_prolongacion` = si,
`pista_correo_usada` = no, `tuteo` = no. Detalle en el informe de la Tarea 13.
