# Decisiones del caso Reembolsos

Las decisiones comunes están en `docs/decisiones.md` de la raíz (C-NNN). Aquí van las de este
caso (D-NNN), la más reciente arriba, con la misma plantilla.

---

## D-005 · 2026-10-15 · Nombre sin inventar, email sin guiones y espera tranquila del WhatsApp
- **Qué:** tras las pruebas por voz de la tarde con W1 v4 (informe
  `docs/informes/2026-10-15-pruebas-tarde-w1-v4.md`):
  - W1 v5, prompt «Reembolsos»:
    - el nombre solo vale si lo dice el cliente o llega en `nombre_completo` por WhatsApp; nunca se saca
      del email; antes de consultar se comprueba que los tres datos los ha dado el cliente;
    - el email se deletrea entero letra a letra y sin los guiones, puntos o espacios que mete la
      transcripción; solo lleva guion, punto o guion bajo si el cliente los dice;
    - «Me ha llegado» solo con una señal `datos_whatsapp` en la conversación; si el cliente dice que ya lo
      escribió y no hay señal: «Todavía no me ha llegado; a veces tarda unos segundos»;
    - espera del WhatsApp: la frase de espera se dice una vez; en silencio no habla (como mucho «Sin
      prisa.» una vez); no ofrece seguir por voz por un silencio, solo si el cliente dice que no le llega,
      no sabe o prefiere dictar;
    - si los datos del WhatsApp llegan tras dos consultas, se permite una tercera con esos datos;
    - si la consulta con datos de WhatsApp no aparece, no se pide escribir más en el WhatsApp: se pregunta
      si lo escribió bien y se sigue por voz;
    - si el `nombre_completo` de la señal no parece un nombre (una palabra o igual al email), se pide por
      voz.
  - W1 v5, herramienta `consultar_reembolso`: la descripción admite la tercera consulta con datos de
    WhatsApp; el nombre no se inventa ni se saca del email; el email sin guiones de la transcripción; el
    mensaje al consultar con datos de WhatsApp es «Me ha llegado, gracias».
  - W2 v9 (las dos ramas): el agente decide qué contestar según lo que ya tiene en toda la conversación:
    con el dato de la reserva y sin nombre pide solo el nombre; un email o DNI/NIE ya es el dato de la
    reserva; no repite el mismo mensaje; el nombre no sale del email; un número que empieza por ER va en
    `numero_reserva`, nunca en `dni`.
- **Por qué:** en las cuatro llamadas de prueba Daniel dijo «Me ha llegado» sin señal y consultó con un
  nombre sacado del email; W2 no pedía el nombre (repetía «¿Tiene el número de reserva?…» aunque ya
  tenía el email); el email se consultó con un guion que puso la transcripción; Daniel ofrecía seguir por
  voz a los pocos segundos de enviar el WhatsApp y repetía la espera; y el límite de dos consultas dejaba
  sin usar los datos del WhatsApp.
- **Afecta a:** Reembolsos (W1 v5 y W2 v9). La voz (`voice_speed`) no cambia.
- **Quién:** jzerpa.
- **Estado:** construidas con evals (resultados en `pruebas/evals-whatsapp.md`, ronda D-005); sin
  publicar, pendientes de la prueba por voz. W1 v4 y W2 v8 siguen publicadas.

---

## D-004 · 2026-10-15 · Un solo bot de voz (W1) y WhatsApp solo cuando hay dificultad
- **Qué:**
  - W1 («Centauro Reembolsos Llamada + w») es el único bot de voz de Reembolsos. «Centauro Reembolsos»
    (V3/V4/V5) se congela: no se publica la V5 ni se borra nada; los cambios se hacen solo en W1. W2 sigue
    aparte (es el agente de texto de WhatsApp, lo dispara un webhook).
  - W1 v4: no ofrece el WhatsApp al empezar. Lo ofrece una sola vez, en el primer momento con dificultad:
    el cliente corrige lo que Daniel le repite o pide que lo repita, un dato no queda claro al segundo
    intento, o la consulta da no encontrada, verificado false o dato no interpretado. Si no lo acepta, no
    se vuelve a ofrecer.
  - Al verificar, Daniel empieza con «Ya he encontrado su reserva» (con email o DNI: «Ya he encontrado una
    reserva a su nombre…, ¿es ese?»).
  - El WhatsApp solo puede ir al número desde el que llama el cliente, y solo si es un móvil. El agente no
    elige el destino (`enviar_whatsapp` solo tiene `idioma`) y nunca se envía a un número dictado, para que
    nadie pueda usar el bot para mandar el WhatsApp a otra persona. En W1 v4, «Calcular idioma y saludo» da
    `telefono_whatsapp` (vacío si no es un móvil) y el POST usa ese campo en vez de `telefono_e164`.
  - En «no encontrada», las reglas de intento web y de reserva de otra compañía van antes de la oferta de
    WhatsApp (resuelve el pendiente de la «segunda oferta»). Se quita la referencia muerta a `ya_enviado`.
- **Por qué:** dos bots casi iguales obligaban a duplicar cada cambio. La oferta inicial alargaba todas las
  llamadas, también las que no tienen problema con el dictado; el WhatsApp ayuda cuando el dictado falla.
  «Ya he encontrado su reserva» da al cliente la confirmación de que se ha localizado.
- **Afecta a:** Reembolsos (W1 v4; Centauro Reembolsos queda congelado).
- **Quién:** jzerpa.
- **Estado:** W1 v4 construida con evals; sin publicar, pendiente de la prueba por voz.

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

