# Pendientes del caso Reembolsos

- [ ] Documentar el caso: `CLAUDE.md` y `docs/workflows.md`.
- [x] Guardar en `prompts/` los prompts de la versión publicada (V4 en `prompts/reembolsos-v4/`).
- [ ] Revisar que no transfiere a 2114, 2115 ni 2119 (C-001).
- [ ] Reembolsos WhatsApp: la herramienta `enviar_whatsapp` no puede devolver `ya_enviado`: HappyRobot no expone un contador de llamadas por herramienta (solo `num_tool_calls` global del agente). Se confía en la regla del prompt («nunca ejecutes enviar_whatsapp más de una vez por llamada»); revisar en las pruebas del caso 4.e.
