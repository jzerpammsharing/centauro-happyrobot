<!-- workflow: Centauro Reembolsos · Datos por WhatsApp · versión: v1 (modo prueba) · copiado: 2026-10-12 -->
# W2 · v1 (modo prueba)

- Trigger «Petición desde la llamada» (Predefined request, API key): telefono, session_key,
  idioma, entorno.
- «Señal de prueba» (Send Signal): publica en `session_key` el payload fijo
  `{"origen":"whatsapp","tipo":"datos_whatsapp","numero_reserva":"ER00000000","nombre_completo":"Prueba Prueba","email":"","matricula":""}`.
- Sin WhatsApp. Se sustituye en la v2 por el agente de texto.
