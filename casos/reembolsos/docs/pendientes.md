# Pendientes del caso Reembolsos

- [ ] **La V4 no recibe llamadas de clientes** (comprobado el 17/10/2026). En HappyRobot figura en
  producción, pero solo tiene 2 llamadas reales (07 y 08/10) y unas 80 de prueba del 27/09; en Twin hay
  2 filas.
  - En RingCentral España no existe una cola de Reembolsos. Las colas de atención al cliente son Nueva
    Reserva (18001), Prolongación (18002 y 18058), Mini Bus (18045 y 18056), Modif. Cancelac. (18046),
    Otras consultas (18047) y Gestión (18057).
  - Las dudas de reembolsos acaban en Gestión: en el análisis de 705 llamadas de la 18057 (del 1 al 25/09),
    253 (36 %) eran de combustible, fianza o reembolsos. Es el tema más frecuente. Una llamada puede tocar
    dos temas.
  - Otras consultas (18047) no ha recibido ninguna llamada desde el 01/09; las llamadas directas del número
    principal entran por Gestión (18057).
  - Volumen de la 18057, según los informes diarios de la rutina de Prolongaciones (llamadas directas de
    clientes, sin contar las que transfieren los bots):
    - entre semana, unas 490 al día (del 6 al 16/10) y se pierde el 30 %;
    - en fin de semana, 230 y 206 (10 y 11/10), todas perdidas porque Gestión no atiende.
  - Estimación de reembolsos (36 % como máximo): unas 175 llamadas al día entre semana (unas 50 perdidas) y
    unas 80 al día en fin de semana (todas perdidas).
  - Falta decidir a qué número u opción del menú se conecta el bot. Lo decide y lo hace una persona.
- [ ] Documentar el caso: `CLAUDE.md` y `docs/workflows.md`.
- [x] Guardar en `prompts/` los prompts de la versión publicada (V4 en `prompts/reembolsos-v4/`).
- [ ] Revisar que no transfiere a 2114, 2115 ni 2119 (C-001).
- [ ] Reembolsos WhatsApp: la herramienta `enviar_whatsapp` no puede devolver `ya_enviado`: HappyRobot no expone un contador de llamadas por herramienta (solo `num_tool_calls` global del agente). Se confía en la regla del prompt («nunca ejecutes enviar_whatsapp más de una vez por llamada»); revisar en las pruebas del caso 4.e.
- [ ] Reembolsos WhatsApp (W2 v4): pedir en Meta las plantillas `datos_llamada_es`, `datos_llamada_en`, `datos_llamada_it` y `datos_llamada_pt` (textos en `prompts/reembolsos-whatsapp-datos/v4/agente-whatsapp.md`).
- [ ] Reembolsos WhatsApp (W2 v4): sustituir la plantilla mock `info_minibus` por `datos_llamada_*` y quitar del prompt la primera línea (solo válida para el mock).
- [ ] Reembolsos WhatsApp (W2): selección de plantilla por `idioma` (rama por idioma antes del agente o plantilla dinámica); hoy solo hay una plantilla fija.
- [ ] Reembolsos WhatsApp (W2 v4): comprobar si HappyRobot escapa los valores `{{$var}}` dentro de `body.raw` JSON (comillas, `\` y saltos de línea en los datos del cliente); si no, valorar construir el payload en un nodo Python que haga `json.dumps`. Hoy solo hay instrucciones de limpieza en la herramienta y el prompt, sin probar.
- [ ] Reembolsos WhatsApp: casos de prueba 5.b–5.f sin hacer (reserva en minúsculas o con espacios, captura del correo con OCR, nota de voz, pregunta de fianza o reembolso por WhatsApp, reescribir datos tras enviarlos). Informe en `docs/informes/2026-10-12-pruebas-whatsapp.md`.
- [ ] Reembolsos WhatsApp: la API key «Reembolsos · señales WhatsApp» (variable `HR_SIGNALS_API_KEY` de W2) tiene un rol con `workflow.trigger` en TODO el workspace y no caduca. Antes de publicar: limitarla por etiquetas a Centauro y darle caducidad y rotación.
- [ ] Reembolsos WhatsApp: vaciar `TELEFONO_PRUEBA` en producción (W1); no debe quedar un número personal en la variable.
- [ ] Reembolsos WhatsApp: mostrar email y matrícula al agente humano (whisper o popup): hoy solo quedan en el extract (`email_whatsapp`, `matricula_whatsapp`) y el susurro de la transferencia está vacío.
- [ ] Reembolsos WhatsApp: decidir a qué número de entrada se conecta W1 (uno de prueba o el de Reembolsos en lugar de la V4). Lo decide y lo publica una persona.
- [ ] Reembolsos WhatsApp: mejora del prompt: tras «no encontrada» con datos llegados por WhatsApp, pedir que revise lo que escribió en el WhatsApp antes de dictar carácter a carácter.
- [ ] Cambiar en el prompt de HappyRobot (V4 y W1) los ejemplos de «Verificado false» (nombre y fecha reales) y de «DICTADO POR PARTES» y de confirmación de número de reserva (posibles números reales) por otros inventados (versión nueva, la publica una persona).
- [ ] Lógica del teléfono (`codigo/telefono_whatsapp.py`): `+0034…` no se normaliza; los extranjeros no tienen cota superior ni comprobación de solo dígitos; 9 cifras sin prefijo se asumen de España (documentarlo); faltan pruebas de esos casos límite. Si se cambia, hay que pegar de nuevo las funciones en «Calcular idioma y saludo» de W1.
- [ ] Reembolsos WhatsApp (W2): el nombre visible del agente de WhatsApp es «Centauro Rent a Car» en vez de «Daniel»; decidir.
- [ ] Reembolsos WhatsApp: el juez del eval 4a3 es permisivo con el acuse corto; endurecer el criterio.
- [ ] Reembolsos WhatsApp: `whatsapp_datos_recibidos = si` del extract no está probado con una transcripción real con señal; revisar en el primer análisis tras publicar.
- [ ] W1 v2, «No encontrada»: la SEGUNDA OFERTA va antes de las reglas de la V4 de «cobro de un intento web» y «reserva de otra compañía», así que un cliente con una reserva de otra compañía podría recibir la oferta de WhatsApp en vez de «esa reserva no es de Centauro». En la próxima versión, que la segunda oferta sustituya solo el paso «pide que te repita el número despacio» y relanzar el eval 4d.
- [ ] W1 v2, `enviar_whatsapp`: no puede devolver «enviado» o «error» como dice el spec §4.1.3; devuelve la respuesta cruda del POST, y el nodo POST sale «succeeded» aunque haya 4xx. Con una clave caducada o una URL mala el agente diría «Se lo acabo de enviar». En la próxima versión, comprobar la respuesta del hook de W2 (como `pasar_a_llamada` con «published») y probar el caso 11 antes de publicar.
- [ ] W1 v2: el agente de voz dice al cliente que escriba email y matrícula, pero la regla «nunca pidas el correo» y `incumplio_restriccion` del extract lo penalizan. Añadir una excepción en el prompt y en el extract.
- [ ] W1 v2: el prompt aún menciona `ya_enviado`, que la herramienta no devuelve (referencia muerta); quitarla.
- [ ] W1 v2: la segunda oferta tras «verificado false» es más estrecha que en el spec (solo «si no sabe qué corregir»); ampliarla o aceptarlo (anotado en el spec §11).
- [ ] W1 v2: posible conflicto entre «repite despacio y vuelve a ejecutar» y el máximo de dos consultas cuando los datos de WhatsApp también dan «no encontrada»; aclarar en el prompt.
- [ ] W2 v4: «pide el @ una vez» del agente de texto puede retrasar `pasar_a_llamada`; preguntarlo después de enviar o quitar la comprobación.
- [ ] `codigo/test_telefono_whatsapp.py` es un script, no un módulo de pytest; ejecutarlo con `python3 -I`.
- [ ] W1 v2: posibles frases duplicadas al enviar («Un momento, se lo envío.» del mensaje de la herramienta y «Se lo acabo de enviar…» del prompt); revisar con una llamada real.
