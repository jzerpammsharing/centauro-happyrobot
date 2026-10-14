# Decisiones del caso Reembolsos

Las decisiones comunes están en `docs/decisiones.md` de la raíz (C-NNN). Aquí van las de este
caso (D-NNN), la más reciente arriba, con la misma plantilla.

---

## D-003 · 2026-10-14 · Identificar por email o DNI/NIE cuando no hay número de reserva
- **Qué:** el MCP (`consultar_reembolso` y `consultar_reserva`) acepta `numero_reserva`, `email` o `dni`
  (prioridad en ese orden) más nombre y fecha de nacimiento. Con email o DNI devuelve la reserva más
  reciente ya iniciada del cliente. Versiones nuevas: V5 (voz), W1 v3 y W2 v8.
  - Herramienta `consultar_reembolso`: `numero_reserva` opcional, `email` y `dni` opcionales; el MCP Call
    envía los tres.
  - Filtro «Filtrar respuesta verificada»: ramas para email ilegible, DNI/NIE ilegible o con la letra
    mal, «falta identificador» (menciona las tres opciones) y «búsqueda no disponible». Clasifica por el
    dato que nombra el mensaje tras «interpretar».
  - Prompt, IDENTIFICACIÓN: número → email (repetido una vez, deletreando lo anterior a la arroba) →
    DNI/NIE (último recurso, cifra a cifra con la letra). Con email o DNI, tras verificar confirma de
    qué alquiler se trata (oficina y fecha de devolución) y, si no es, pide el número o transfiere.
    Se quitan «nunca pidas el correo» y «sin número no puedes consultar»; se mantienen «nunca la
    matrícula» y «nunca datos de tarjeta». `reserva_no_encontrada` = no aparece con ninguno de los tres.
  - W1/W2: la señal de WhatsApp trae `numero_reserva`, `email` y `dni` (la `matricula` desaparece);
    W2 acepta nombre + cualquiera de los tres.
- **Por qué:** muchos clientes llaman sin el número (no lo tienen a mano o reservó una empresa) y acababan
  en transferencia con `reserva_no_encontrada`. La matrícula se descarta: la API devuelve la última
  reserva del coche, que suele ser de otro cliente.
- **Afecta a:** Reembolsos (V5, W1 v3, W2 v8). El MCP ya lo soportaba.
- **Quién:** jzerpa.
- **Estado:** construidas y con evals; sin publicar, a la espera de la prueba por voz. Resultados en
  `pruebas/evals-identificacion.md`.

---

## D-002 · 2026-10-14 · Plantilla real `datos_reserva`, con una rama por idioma
- **Qué:** W2 v7 sustituye la plantilla mock `info_minibus` por `datos_reserva`, aprobada por Meta en
  `es` y `en` con el mismo nombre. El nodo nuevo «Elegir plantilla» da `idioma_plantilla` (`es`; `en`,
  `it`, `pt` y cualquier otro → `en`) y el nodo de rutas «Idioma de la plantilla» manda a «Agente de
  WhatsApp (es)» o «(en)». Cada agente lleva la plantilla en modo estático con el idioma fijado por
  la API. Se quitan los parámetros de `info_minibus` y la línea del prompt sobre la plantilla mock.
- **Por qué:**
  - el desplegable del editor solo distingue la plantilla por nombre: al elegir la española guardó
    la inglesa;
  - el modo dinámico («Template ID or name», v5) busca por nombre; con el ID de Meta falla con
    `template_not_found` (run `5e1fac1f-b7f8-41f5-8773-67c5f7a98481`);
  - en modo estático con `language = "es"` fijado por la API llega la española (v6, run
    `b4dc7352-0070-4fef-a3fb-3162b80756fd`);
  - lo limpio son dos plantillas con nombres distintos (`datos_reserva_es` y `datos_reserva_en`) y un
    solo agente con plantilla dinámica por nombre, pero Meta tarda unos dos días: la rama es la
    solución provisional.
  - No hay plantillas en `it` ni `pt`; se decide usar la inglesa.
  - Los nombres `datos_llamada_*` y los textos de la spec (apartado 6) no se usaron: Centauro dio de
    alta `datos_reserva` con otro texto (copiado en `prompts/reembolsos-whatsapp-datos/v7/`).
- **Afecta a:** Reembolsos (W2). W1 y la V4 no cambian.
- **Quién:** jzerpa.
- **Estado:** W2 v7 (`63eqtfk9nrdl`) construida, sin publicar. La v5 (por ID) no funciona; la v6 fue
  solo la prueba del idioma fijado por la API.

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

