# Pendientes del caso Reembolsos

- [ ] Documentar el caso: `CLAUDE.md` y `docs/workflows.md`.
- [x] Guardar en `prompts/` los prompts de la versión publicada (V4 en `prompts/reembolsos-v4/`).
- [ ] Revisar que no transfiere a 2114, 2115 ni 2119 (C-001).
- [ ] Reembolsos WhatsApp: la herramienta `enviar_whatsapp` no puede devolver `ya_enviado`: HappyRobot no expone un contador de llamadas por herramienta (solo `num_tool_calls` global del agente). Se confía en la regla del prompt («nunca ejecutes enviar_whatsapp más de una vez por llamada»); revisar en las pruebas del caso 4.e.
- [ ] Reembolsos WhatsApp (W2 v4): pedir en Meta las plantillas `datos_llamada_es`, `datos_llamada_en`, `datos_llamada_it` y `datos_llamada_pt` (textos en `prompts/reembolsos-whatsapp-datos/v4/agente-whatsapp.md`).
- [ ] Reembolsos WhatsApp (W2 v4): sustituir la plantilla mock `info_minibus` por `datos_llamada_*` y quitar del prompt la primera línea (solo válida para el mock).
- [ ] Reembolsos WhatsApp (W2): selección de plantilla por `idioma` (rama por idioma antes del agente o plantilla dinámica); hoy solo hay una plantilla fija.
- [ ] Reembolsos WhatsApp (W2 v4): comprobar si HappyRobot escapa los valores `{{$var}}` dentro de `body.raw` JSON; si no, valorar construir el payload en un nodo Python que haga `json.dumps`.
- [ ] Reembolsos WhatsApp: casos de prueba 5.b–5.f sin hacer (reserva en minúsculas o con espacios, captura del correo con OCR, nota de voz, pregunta de fianza o reembolso por WhatsApp, reescribir datos tras enviarlos) y datos con comillas, `\` o saltos de línea. Informe en `docs/informes/2026-10-12-pruebas-whatsapp.md`.
- [ ] Reembolsos WhatsApp: la API key «Reembolsos · señales WhatsApp» (variable `HR_SIGNALS_API_KEY` de W2) tiene un rol con `workflow.trigger` en TODO el workspace y no caduca. Antes de publicar: limitarla por etiquetas a Centauro y darle caducidad y rotación.
- [ ] Reembolsos WhatsApp: vaciar `TELEFONO_PRUEBA` en producción (W1); no debe quedar un número personal en la variable.
- [ ] Reembolsos WhatsApp: mostrar email y matrícula al agente humano (whisper o popup): hoy solo quedan en el extract (`email_whatsapp`, `matricula_whatsapp`) y el susurro de la transferencia está vacío.
- [ ] Reembolsos WhatsApp: decidir a qué número de entrada se conecta W1 (uno de prueba o el de Reembolsos en lugar de la V4). Lo decide y lo publica una persona.
- [ ] Reembolsos WhatsApp: mejora del prompt: tras «no encontrada» con datos llegados por WhatsApp, pedir que revise lo que escribió en el WhatsApp antes de dictar carácter a carácter.
- [ ] Cambiar en el prompt de HappyRobot (V4 y W1) el ejemplo de «Verificado false», que usa un nombre y una fecha reales, por uno inventado (versión nueva, la publica una persona).
