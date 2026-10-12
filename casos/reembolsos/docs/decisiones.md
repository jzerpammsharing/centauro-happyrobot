# Decisiones del caso Reembolsos

Las decisiones comunes están en `docs/decisiones.md` de la raíz (C-NNN). Aquí van las de este
caso (D-NNN), la más reciente arriba, con la misma plantilla.

---

## D-001 · 2026-10-12 · Datos por WhatsApp durante la llamada, con Signals
- **Qué:** workflows nuevos «Centauro Reembolsos WhatsApp» (W1, voz, copia de la V4) y «Centauro
  Reembolsos · Datos por WhatsApp» (W2, agente de texto). El agente de voz ofrece un WhatsApp; el
  cliente escribe reserva, nombre, email y matrícula; los datos vuelven a la llamada como señal a
  `session.<id>`. La fecha de nacimiento sigue siendo por voz. W2 publica la señal con un Webhook
  POST a `https://platform.eu.happyrobot.ai/api/v2/signals` (API key de la organización con el
  permiso `workflow.trigger`, variable `HR_SIGNALS_API_KEY`) y no con el nodo Send Signal.
- **Por qué:** el número de reserva y el nombre son lo que más falla al dictar. Signals evita Twin y
  las consultas periódicas; un tema por teléfono se descartó porque los temas personalizados no
  admiten variables. El nodo Send Signal se descartó porque entrega el payload vacío (runs de W2
  `4bb78986-a2b0-4773-905f-771dba3c2149` y `1a60e390-f559-4d7f-8518-78bdaffd281e`); con la API de
  signals el payload llega completo (run `d60f57b3-88da-4c93-9c84-1a00bfd64948`). Pruebas en
  `docs/informes/2026-10-12-pruebas-whatsapp.md`.
- **Afecta a:** Reembolsos. La V4 no cambia.
- **Quién:** jzerpa.
- **Estado:** aplicada en W1 v2 y W2 v4, publicadas por una persona solo para pruebas con plantilla
  mock `info_minibus` (no hay plantillas `datos_llamada_*` aprobadas); pendiente de publicar a
  clientes y de conectar W1 a un número. Pendientes en `docs/pendientes.md`.

