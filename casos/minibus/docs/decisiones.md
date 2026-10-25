# Decisiones del caso Minibús

Las decisiones comunes a todos los casos están en `docs/decisiones.md` de la raíz (C-NNN).

Una entrada por decisión, la más reciente arriba. Cada una dice qué se decidió, por qué, a qué
afecta y quién la tomó. Si una decisión sustituye a otra, enlázala ("sustituye a D-003").

Plantilla:

```
## D-NNN · AAAA-MM-DD · Título corto
- **Qué:** …
- **Por qué:** … (datos: run_id, cifras del informe, llamadas de ejemplo)
- **Afecta a:** bot(s) y versión(es)
- **Quién:** persona(s)
- **Estado:** propuesta | aprobada | aplicada en vX | descartada
```

> Las entradas D-001 a D-004 se reconstruyeron el 11/10/2026 a partir de los nombres de las
> versiones y del análisis de calidad. Faltan fechas exactas y responsables: complétalos quien lo
> sepa.

---

## D-014 · 2026-10-25 · v28: la dirección de la oficina se da, no se manda a buscarla al navegador (sin publicar)
- **Qué:**
  - Fork de la v27 (en producción): v28 (`arjyj8ufclwz`), «v28 · v27 + dirección de las oficinas
    desde Punto de encuentro».
  - Si el cliente pide la dirección de una oficina, también la de su aeropuerto (va en taxi o en su
    coche), «Punto de encuentro» ya no le dice que la busque en el navegador: cambia a «Información
    de oficina», que le da la dirección de la ficha tal cual, como hacen los agentes.
  - Para eso «Punto de encuentro» tiene una herramienta nueva, `informacion_oficina` (tema
    `direccion`), que necesita un «Module Change» hacia «Información de oficina». También la usa
    para los datos de una oficina que no es de aeropuerto, que antes se transferían a la cola de
    MINIBÚS, y en modo virtual.
  - «Información de oficina» gana una sección DIRECCIÓN: la de la ficha, tal cual; si va en su coche,
    también «Para llegar en coche»; el navegador solo si la ficha no tiene dirección o lo dice. Nunca
    inventa ni cambia una dirección.
  - Detalle y copias en `prompts/minibus-es/v28/`.
  - El mismo arreglo, en el bot único de Atención España: v6 (`lxkt96mlluxz`), sin publicar. Allí el
    Module Change ya existía; cambian la herramienta y los dos prompts (se documenta en el caso
    `atencion-es`).
- **Por qué:**
  - Run `f7b98d60-17e7-4f1b-9e47-3995401098c2` (25/10, 08:19, Málaga): el cliente va en taxi y pide
    la dirección de la oficina. El bot le dice que no la tiene y que la busque en el navegador. El
    cliente se queja: es el teléfono de información y no tiene la dirección.
  - La frase «Dile que busque en el navegador "Centauro Rent a Car" y el nombre del aeropuerto» ya
    estaba en la v17 y no hay ninguna decisión que la justifique. «Punto de encuentro» no tenía las
    direcciones, que solo están en «Información de oficina».
  - Los agentes humanos dan la dirección cuando se la piden. Google Maps lo usan solo como apoyo:
    Málaga (`fa8f81ff`), Bilbao (`ca14fdc4`) y Sevilla (`f3432d00`).
  - Se elige el Module Change y no copiar las direcciones en «Punto de encuentro» para no mantener
    los datos de 33 oficinas en dos sitios.
  - Datos: `docs/informes/2026-10-25-v28-direccion.md`.
- **Afecta a:** Minibús ES v28 y Atención España v6. Las colas no cambian. La cola de MINIBÚS deja de
  recibir las preguntas de datos de una oficina que no es de aeropuerto hechas desde «Punto de
  encuentro».
- **Quién:** jzerpa.
- **Estado:** sin publicar.
  - **Bloqueo:** una persona tiene que crear en el editor el Module Change debajo de
    `informacion_oficina` (en «Punto de encuentro» de la v28) hacia «Información de oficina». Sin él,
    la herramienta devuelve vacío y el bot puede inventarse la respuesta (eval DIR-2: dio un horario
    inventado). **No publicar la v28 sin ese enlace.**
  - Evals (`docs/informes/2026-10-25-v28-direccion.md`): DIR-1 y DIR-3 pasan 2 de 2 en v28 y fallan
    en v27. La regresión no muestra fallos nuevos.
  - Falta una llamada de prueba real. Publicar lo hace una persona.

## D-013 · 2026-10-24 · v27: el WhatsApp del punto de encuentro, cierre normal y para el cliente que ya espera (publicada)
- **Qué:**
  - Fork de la v26 (en producción): v27 (`e4qv98cib2dm`), «v27 · v26 + WhatsApp como cierre normal
    y para el cliente que ya espera».
  - En Madrid (T1, T2 y T4), Sevilla y Málaga, la pregunta del WhatsApp («¿Quiere que le mande
    estas indicaciones por WhatsApp a este número?») pasa a ser el cierre normal tras dar el punto de
    encuentro, **en lugar de** «¿Puedo ayudarle en algo más?». Nunca las dos en el mismo turno.
  - También se ofrece al cliente que **ya espera** en el punto y pregunta cada cuánto pasa o si va a
    venir, sin quejarse: se le da la frecuencia y la referencia de su punto, y se le ofrece el
    WhatsApp con el enlace para ver el minibús en directo. En Madrid hace falta la terminal.
  - **Se sigue preguntando** (opt-in de Meta): se ofrece una sola vez y no se envía nada sin el «sí».
  - Condiciones sin cambios, pero escritas antes de la oferta y con prioridad: WhatsApp disponible
    (línea española y móvil), conversación en español, uno de esos cinco puntos, y cliente sin queja
    ni transferencia.
  - Extract «Registrar consultas del alquiler»: `punto_whatsapp` recoge también el punto donde ya
    espera el cliente. Sin esto, al que ya espera y acepta no le llegaría el WhatsApp.
  - Nodos tocados: el prompt «Punto de encuentro» y el extract «Registrar consultas del alquiler».
    Detalle y copias en `prompts/minibus-es/v27/`.
- **Por qué:**
  - Con v25 (del 15 al 24/10), en las llamadas aptas (línea española, Madrid T1/T2/T4, Sevilla o
    Málaga, el bot da el punto y cierra sin transferir) el bot ofrecía el WhatsApp en 42 de 93
    (45 %): Madrid 34 de 63, Málaga 8 de 14 y **Sevilla 0 de 16**.
  - Causa: el cierre por defecto («¿Puedo ayudarle en algo más?») ganaba a la excepción del
    WhatsApp, que estaba entre paréntesis y en otra sección del prompt.
  - Muchos clientes llaman cuando ya están en el punto, y a esos no se les ofrecía nunca, aunque el
    enlace para ver el minibús en directo es justo lo que necesitan.
  - Cuando se ofrece, funciona: dicen que sí unos dos de cada tres clientes.
  - Datos: `docs/informes/2026-10-24-v27-whatsapp.md`.
- **Afecta a:** Minibús ES v27. Más WhatsApp enviados con la plantilla `minibus_punto_texto_boton`.
- **Quién:** jzerpa.
- **Estado:** pendiente de publicar.
  - Evals (`docs/informes/2026-10-24-v27-whatsapp.md`): batería nueva de 14, 27 de 28 en v27
    (dos ejecuciones) frente a 8 de 14 en v26. Regresión de «Punto de encuentro»: 18 de 21, los
    mismos fallos que ya había (ADV-8 y ADV-9, y ADV-10, que también falla en v26 con todas las
    variables fijadas).
  - Comprobado: prompt y extract releídos tras subirlos (mismo texto, mismas variables) y
    `fix_broken_vars` sin referencias rotas.
  - Falta una llamada de prueba real desde un móvil (ver `pendientes.md`). Publicar lo hace una
    persona.
  - **Publicada:** en producción el 25/10/2026 (comprobado con `manage_versions`; las llamadas de ese
    día desde las 08:01 entran por ella). Primera llamada apta (Málaga, 08:19): cierra con la
    pregunta del WhatsApp, el cliente dice que no y no se envía nada.

## D-012 · 2026-10-24 · v26: servicio de espera y avisos de retraso, a la cola de Minibús (publicada)
- **Qué:**
  - Fork de la v25 (en producción): v26 (`fw02geuq54cv`), «v26 · v25 + servicio de espera y avisos
    de retraso a la cola de Minibús».
  - Cuando el cliente va a llegar tarde a recoger el coche porque su vuelo o tren se retrasa, el
    bot le pasa a la cola de **Minibús** (18056 en español, 18059 en inglés) con
    `motivo_transferencia` `minibus` en dos casos:
    - acepta que comprueben el servicio de espera (40 €);
    - después de explicarle que no hace falta, insiste en avisar a la oficina.
  - Antes iba a Gestión de reserva.
  - Va **siempre** a Minibús, esté Gestión abierta o cerrada: una sola regla para que el bot no se
    equivoque.
  - Lo demás no cambia:
    - el bot explica primero que la reserva se guarda doce horas dentro del horario de la oficina, y
      el servicio de espera sin prometer nada;
    - si solo quiere avisar, le dice que no hace falta y no le ofrece pasarle con nadie;
    - en modo virtual (centro de atención cerrado) no se transfiere;
    - el resto de casos de Gestión siguen sin ir a Minibús cuando Gestión está cerrada.
  - Nodos tocados: los prompts «Prolongación y consultas», «Punto de encuentro» e «Información de
    oficina», y sus tres `transfer_to_human_agent`. «Triaje y horario» no cambia. Detalle y copias
    en `prompts/minibus-es/v26/`.
- **Por qué:**
  - Gestión solo atiende de lunes a viernes de 8 a 21 h. Fuera de ese horario (fines de semana y
    tardes), al cliente cuyo vuelo llega tarde el bot no le daba ninguna opción: le decía que
    llamara en horario de Gestión o que fuera a la oficina, justo cuando necesita el servicio de
    espera.
  - En las evals, v25 llega a pasar el servicio de espera a la 18057 con Gestión cerrada, donde solo
    suena la locución de cerrado.
  - El call center confirma que la cola de Minibús, que atiende los siete días, puede gestionar el
    servicio de espera.
- **Afecta a:**
  - Minibús ES v26. Las colas 18056 y 18059 recibirán estas llamadas (ver `docs/extensiones.md`).
  - Prolongaciones (V11) y el bot único de Atención España mandan todavía el servicio de espera a
    Gestión (ver `pendientes.md`).
- **Quién:** jzerpa, a petición del call center.
- **Estado:** publicada: v26 está en producción (comprobado el 24/10/2026; sustituye a v25).
  - Evals (`docs/informes/2026-10-24-v26-evals.md`): batería nueva 17 de 17 en v26; regresión sin
    fallos nuevos frente a v25.
  - Comprobado: prompts y herramientas releídos tras subirlos (mismo texto, mismas variables) y
    `fix_broken_vars` sin referencias rotas.
  - Según jzerpa, el 24/10 ya ha pasado bien algunas llamadas reales de retraso a la cola de
    Minibús. Falta revisarlo con datos en el informe diario (ver `pendientes.md`).

## D-011 · 2026-10-15 · v25: rama por defecto en «¿Enviar WhatsApp?» (publicada)
- **Qué:**
  - Fork de la v24: v25 (`k2in5n9kk01x`), «v25 · v24 + rama por defecto en ¿Enviar WhatsApp?».
  - Único cambio: el nodo de rutas «¿Enviar WhatsApp?» tiene una segunda rama, «Fallback» (tipo
    `fallback`), sin ninguna acción detrás. La rama «Enviar» (`enviar` es true → «Enviar WhatsApp
    del punto de encuentro») no cambia.
  - Prompts, Python «Preparar WhatsApp minibús», plantilla y resto de nodos: los de v24 (ver
    `prompts/minibus-es/v25/README.md`).
- **Por qué:**
  - En v24, cuando `enviar` es false (el cliente no acepta, aeropuerto sin seguimiento, otro
    idioma…: lo normal), no se cumple ninguna rama y el run termina en «failed» con «paths node
    '¿Enviar WhatsApp?' has no matching condition and no fallback branch», aunque la llamada haya
    ido bien.
  - Ejemplos: 52019f08-6f67-4055-8537-db12c2c7cd57 (primer caso) y
    4ca09060-423f-4b37-b45d-9fe7f5ee6172 (15/10, 18:06).
  - Esos «failed» no son fallos de la llamada: ensucian el test A/B (C-004) y la rutina horaria
    tiene que descontarlos aparte.
- **Afecta a:** Minibús ES v25, que sustituirá a v24 en el test A/B.
- **Quién:** jzerpa.
- **Estado:** publicada: v25 está en producción (comprobado el 24/10/2026).
  - Comprobado: la estructura es v24 + la rama (37 nodos frente a 36; 4 condiciones frente a 3) y
    `fix_broken_vars` no encuentra referencias rotas. En el test solo fallan los 4 «Initiate
    customer connection», que necesitan una llamada en curso.
  - Sin probar los dos caminos: el nodo de rutas no se puede probar suelto (el motor no tiene
    ejecutor de prueba para «Paths»), el workflow empieza con una llamada entrante y probar «Enviar
    WhatsApp» manda el mensaje de verdad. Revisar en los primeros runs de v25: con `enviar` false,
    run «completed»; con `enviar` true, WhatsApp enviado como en v24.
  - Al publicar: cambiar v24 por v25 en el test A/B (lo hace una persona) y actualizar
    `rutinas/vigilancia-v24-ab.md`.

## D-010 · 2026-10-15 · v24: WhatsApp del punto de encuentro solo con seguimiento en directo (borrador)
- **Qué:**
  - Fork de la v23: v24 (`5g6422lgdcem`).
  - El agente ofrece una vez el WhatsApp con el punto de encuentro, y se envía al terminar la llamada,
    solo para Madrid (T1, T2, T4), Sevilla y Málaga: los aeropuertos con seguimiento en directo en
    buscentauro.com.
  - Plantilla de Meta nueva `minibus_punto_texto_boton` (español, botón «Ver minibús en directo»).
    La de inglés aún no existe: solo se envía en llamadas en español.
  - El diccionario `TRACKING` de «Preparar WhatsApp minibús» decide por aeropuerto.
  - `frecuencia` = «15 o 20 minutos» en el WhatsApp para los tres aeropuertos.
  - Detalle en `prompts/minibus-es/v24/`.
- **Por qué:**
  - El botón de seguimiento solo sirve donde el minibús tiene geolocalización; enviar el mensaje
    en el resto de aeropuertos daría un enlace sin datos.
  - Retoma el envío de la v20 (borrador sin publicar) sobre la v23, con la plantilla nueva.
- **Afecta a:** Minibús ES v24.
- **Quién:** jzerpa.
- **Estado:** borrador (sin probar ni publicar).
  - **Revisar en el editor:** el nodo «Enviar WhatsApp del punto de encuentro» se montó sin poder
    leer la plantilla desde Meta; hay que reseleccionarla y comprobar que las cuatro variables
    quedan asignadas.
  - **Frecuencia:** unificada en «quince o veinte minutos» (voz) y «15 o 20 minutos» (WhatsApp)
    en Madrid T1/T2/T4, Sevilla y Málaga. Los demás aeropuertos siguen con su frecuencia.

## D-009 · 2026-10-12 · v23: saltos entre módulos (borrador)
- **Qué:**
  - Fork de la v22: v23 (`3o04zrwgfj0g`).
  - «Punto de encuentro» e «Información de oficina» pueden pasar a «Prolongación y consultas» con
    `consultas_alquiler`.
  - «Prolongación y consultas» puede pasar a «Información de oficina» (a cualquier hora) y a
    «Punto de encuentro» (solo fuera del modo virtual).
  - Se quitan las copias resumidas de «OTRAS PREGUNTAS DEL ALQUILER» de los dos primeros módulos:
    ahora remiten a `consultas_alquiler`.
  - Prompts en `prompts/minibus-es/v23/`.
- **Por qué:**
  - En la v22, cuando el cliente pasa de prolongar o recoger tarde a preguntar por el minibús, el
    bot transfiere a la cola de Minibús aunque el workflow tiene el dato. Pasó en ac24fb7b, 900cb235
    y d53861dc (10-11/10).
  - El conocimiento de prolongación estaba en tres sitios (bot de Prolongaciones, módulo de la v22 y
    resumen en Punto de encuentro/Información de oficina), y ya empezaban a divergir.
- **Afecta a:** Minibús ES v23.
- **Quién:** jzerpa.
- **Estado:** borrador completo (los 4 «Module Change» se enlazaron en el editor el 12/10).
  - Falta probarlo y medirlo frente a la v22 antes de publicar.

## D-008 · 2026-10-11 · El repo es solo del caso Minibús
- **Qué:** el proyecto se llama `centauro-happyrobot-minibus` y cubre solo los tres workflows de
  Minibús (ES, IT y PT). Otros bots de Centauro en HappyRobot, como Prolongaciones, irían en su
  propio repo.
- **Por qué:** cada caso tiene su contexto, sus decisiones y su histórico propios.
- **Quién:** jzerpa.
- **Estado:** sustituida por C-003 (un solo repo con carpeta por caso).

## D-007 · 2026-10-11 · Rutina diaria: corrección del prompt
- **Qué:**
  - Las transferencias de Minibús ES a 18057, 18061, 18001, 18006 y 18034 cuentan en el informe;
    se ignoran solo las patas de esas colas que no casan con un intento de Minibús.
  - La 2119 se añade a los menús prohibidos.
  - La 18066 (PT-EN) se añade a las colas de Minibús.
  - `consultas_alquiler` e `informacion_oficina` vacías no son error.
  - El listado de runs se extrae con python, no copiado a mano.
  - Los teléfonos se guardan solo como hash.
  - Se tolera el retraso de RingCentral en los últimos 15 minutos del periodo.
  - Se reintenta ante el límite de peticiones del conector.
- **Por qué:** en el informe del 10/10, las versiones v19 y siguientes de ES transfirieron 21 veces
  a Gestión (18057 y 18061) y ahí se perdieron 2 llamadas porque el agente no pulsó 1. Con el
  prompt anterior esas transferencias se habrían ignorado. También hubo una avería a la 2119 en
  Italia.
- **Afecta a:** `rutinas/informe-minibus.md`.
- **Quién:** pendiente de aplicar en la rutina programada.
- **Estado:** aplicada en el repo; falta pegarla en la rutina.

## D-006 · 2026-10-11 · Mejoras de prompt para Minibús (propuesta)
- **Qué:**
  - preguntas frecuentes con respuestas validadas (recogida tarde, devoluciones, oficinas,
    políticas);
  - dar el punto de encuentro en una frase y repetirlo si el cliente interrumpe;
  - transferir tras 2 preguntas sin respuesta;
  - no dar frecuencias del minibús que no estén en la ficha;
  - responder en el idioma del cliente;
  - permitir dar la dirección de la oficina al cliente que está en el aeropuerto.
- **Por qué:** el 10/10, 31 de 252 llamadas se podrían haber resuelto sin herramientas nuevas.
  La tasa de resueltas pasaría del 42 % al 54 % aproximadamente. Ejemplos: `4673ac2f`
  (frecuencia inventada), `a625edab` (idioma), `c6ffa5b5` (pregunta repetida 4 veces).
- **Afecta a:** Minibús ES, IT y PT.
- **Quién:** pendiente.
- **Estado:** propuesta.

## D-005 · 2026-10-10 · Extensiones 2114, 2115 y 2119 → movida a C-001
Afecta a varios casos: ver `docs/decisiones.md` de la raíz.

## D-004 · antes del 10/10/2026 · Nuevas versiones de ES con prolongaciones y consultas (v19, v21, v22)
- **Qué:** se añaden el módulo «Prolongación y consultas» (herramientas `consultas_alquiler` e
  `informacion_oficina`), los ajustes de voz y de Palma, las respuestas validadas y el horario de
  la cola de Gestión.
- **Por qué:** resolver consultas del alquiler sin transferir.
- **Nota:** el 10/10, 70 de 133 llamadas de ES entraron por estas versiones aunque la publicada
  es la v17. Hay que decidir cuál es la buena y dejar una sola en producción.
- **Estado:** en prueba (sin publicar).

## D-003 · antes del 10/10/2026 · Horario 08:00–23:00 y modo virtual (ES v17, publicada)
- **Qué:** amplía el horario de atención y añade el modo virtual.
- **Estado:** aplicada en ES v17.

## D-002 · antes del 10/10/2026 · `buscar_punto_de_encuentro` es un cambio de módulo, no una consulta
- **Qué:** la herramienta devuelve siempre vacío (Data null, SUCCESS). La lista de puntos de
  encuentro vive en el prompt del nodo «Punto de encuentro».
- **Por qué:** comprobado en 7 transcripciones: el bot da el punto correcto.
- **Consecuencia:** los campos del extract `herramientas_con_error=buscar_punto_de_encuentro` e
  `invento_informacion=si` son falsos positivos del analizador (el 08/10 salieron en 129 y 115 de
  278 llamadas).
- **Estado:** aplicada.

## D-001 · antes del 10/10/2026 · El analista de calidad es de solo lectura
- **Qué:** la rutina diaria no modifica workflows ni runs ni escribe en RingCentral. Solo escribe
  en la colección `informes` del artefacto de Minibús.
- **Por qué:** evitar cambios en producción sin revisión humana.
- **Estado:** aplicada.
