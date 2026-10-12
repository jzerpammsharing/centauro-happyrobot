# Pendientes del caso Reembolsos

- [ ] Documentar el caso: `CLAUDE.md` y `docs/workflows.md`.
- [x] Guardar en `prompts/` los prompts de la versión publicada (V4 en `prompts/reembolsos-v4/`).
- [ ] Revisar que no transfiere a 2114, 2115 ni 2119 (C-001).
- [ ] Reembolsos WhatsApp: la herramienta `enviar_whatsapp` no puede devolver `ya_enviado`: HappyRobot no expone un contador de llamadas por herramienta (solo `num_tool_calls` global del agente). Se confía en la regla del prompt («nunca ejecutes enviar_whatsapp más de una vez por llamada»); revisar en las pruebas del caso 4.e.
- [ ] Reembolsos WhatsApp (W2 v4): pedir en Meta las plantillas `datos_llamada_es`, `datos_llamada_en`, `datos_llamada_it` y `datos_llamada_pt` (textos en `prompts/reembolsos-whatsapp-datos/v4/agente-whatsapp.md`).
- [ ] Reembolsos WhatsApp (W2 v4): sustituir la plantilla mock `info_minibus` por `datos_llamada_*` y quitar del prompt la primera línea (solo válida para el mock).
- [ ] Reembolsos WhatsApp (W2): selección de plantilla por `idioma` (rama por idioma antes del agente o plantilla dinámica); hoy solo hay una plantilla fija.
