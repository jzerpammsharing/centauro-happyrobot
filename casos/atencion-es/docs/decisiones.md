# Decisiones del caso Atención España

Las decisiones comunes están en `docs/decisiones.md` de la raíz (C-NNN). Aquí van las de este caso (D-NNN), la
más reciente arriba, con la misma plantilla.

Plantilla:

```
## D-NNN · AAAA-MM-DD · Título corto
- **Qué:** …
- **Por qué:** … (datos: run_id, cifras, llamadas de ejemplo)
- **Afecta a:** versión(es)
- **Quién:** persona(s)
- **Estado:** propuesta | aprobada | aplicada en vX | descartada
```

---

## D-009 · 2026-10-19 · Saltos: «a qué hora pasa el minibús» va a Punto de encuentro y evals de salto ajustadas
- **Qué:** (1) la descripción de `buscar_punto_de_encuentro` de Información de oficina (`01a155d9-5db4-…`, Tarea 12)
  añade «También si pregunta a qué hora pasa el minibús, si hay minibús a una hora concreta o por el de vuelta: no lo
  contestes tú, aunque sea fuera del horario de la oficina». (2) La de `volver_al_triaje` de Prolongación añade
  «También si solo dice que tiene otra consulta o gestión, sin decir cuál: no le preguntes cuál, el triaje lo hace»
  (va en la herramienta, no en el prompt, que está en el límite de 22.000). (3) Evals cambiadas: SALTO-01a, 02a y 03b
  pasan de «quiero que borren mis datos de cliente» a «tengo otra consulta distinta»; la expectativa de PRO-2 ya no
  exige que el motivo diga que el punto se da a cualquier hora.
- **Por qué:** (1) ADV-12 daba 0/3: Información de oficina contestaba él si había minibús a las cinco (el horario del
  minibús es de Punto de encuentro). (2) SALTO-03b daba 0/3: Prolongación preguntaba cuál era la consulta. (3) Borrar
  datos no es de ningún módulo y los módulos, con razón, lo trataban como gestión o duda del alquiler; el motivo de
  la llamada no es lo que se valora en PRO-2.
- **Afecta a:** v2, herramientas de salto y evals de «Bot único · Saltos». La devolución en aeropuertos con minibús
  (`informacion-de-oficina.md`, sección de devolución, punto 3) sigue siendo de Información de oficina: IDO-3,
  «Sevilla aeropuerto a medianoche» y «Alicante aeropuerto de madrugada» se pasaron en la ronda 25 para comprobarlo.
- **Ronda de arreglos 2 (23:29–23:30):** GC-IO1 (crítica) cayó a 0/3 con las herramientas nuevas de Información de
  oficina («cambiar la hora de devolución» se iba a gestión). La viñeta de gestión de ESCALADO del prompt dice ahora
  «Alargar el alquiler o cambiar la hora o el día de devolución no son de esta línea: consultas_alquiler (prolongar si es
  más tarde, devolucion si es antes; si no lo dice, pregúntaselo una vez), también con gestión cerrada», y la
  descripción de `consultas_alquiler` del nodo, «Alargar el alquiler o cambiar la hora o el día de devolución
  (prolongar si es más tarde, devolucion si es antes) siempre va aquí». GC-IO1 vuelve a 3/3 (ronda 26).
- **Quién:** el agente de la Tarea 12 (vuelta de arreglos y rondas de arreglos 1 y 2); lo revisa el responsable.
- **Estado:** aplicada en v2.

## D-008 · 2026-10-19 · Punto de encuentro e Información de oficina: saltos por herramienta y aviso de cierre en el módulo
- **Qué:** en los dos módulos (Tarea 11), lo que en la v25 se transfería a la cola de MINIBÚS porque «no lo tienes en
  esta parte de la llamada» pasa a la herramienta del módulo que lo sabe: en Información de oficina, el minibús o el
  punto de encuentro de un aeropuerto van a `buscar_punto_de_encuentro`; en Punto de encuentro, una oficina que no es
  de aeropuerto va a `informacion_oficina`. Lo que no es del módulo ni una duda del alquiler, a `volver_al_triaje`.
  «Devolver en otra oficina» pasa a `consultas_alquiler` con el tema `devolucion` (deja de repetirse en los dos
  prompts, C-005). El aviso de oficina de aeropuerto cerrada (LISTAS 1 a 4 de `nocturno_*`, Paso 2 y 3 del Triaje
  de la v25) lo da Punto de encuentro, antes de dar el punto.
- **Por qué:** spec §5.6 y §5.7 (matriz de saltos y herramientas por módulo) y §5.4 (las listas nocturnas pasan a
  Punto de encuentro; desde la Tarea 8 el Triaje llama siempre a `buscar_punto_de_encuentro`). Mandar a la cola de
  Minibús una pregunta que otro módulo responde es una transferencia evitable.
- **Afecta a:** v2. Hasta la Tarea 12 esas herramientas no existen en estos dos nodos: en las evals, Información de
  oficina llama a `consultas_alquiler` o contesta cuando le preguntan por el minibús (ADV-12, «VIRTUAL · pregunta por
  el minibús», «ES · pregunta por el minibús (Palma)», 0/3, no cuentan, R5). **Hasta la Tarea 12 Información de
  oficina empeora frente a la v1 en las preguntas del minibús**: la v1 transfería a Minibús y la v2 contesta o salta a
  Consultas.
- **Quién:** el agente de la Tarea 11, con el spec como autoridad; lo revisa el responsable.
- **Estado:** aplicada en v2. Las herramientas `informacion_oficina`, `buscar_punto_de_encuentro` y `volver_al_triaje`
  de estos dos módulos se crearon en la Tarea 12 (19/10/2026), con su Module Change (el responsable, en el editor);
  ADV-12, «VIRTUAL · pregunta por el minibús» y «ES · pregunta por el minibús (Palma)» cuentan desde entonces y dan
  3/3 (`prompts/atencion-es/v2/saltos.md`).

## D-007 · 2026-10-19 · Prolongación: reserva que aún no ha empezado, sin envío ni transferencia
- **Qué:** en el prompt «Prolongación» de la v2, si la reserva aún no ha empezado, el bot ejecuta `buscar_respuesta`
  con `reserva_no_iniciada` y, si al cliente le falta la contraseña, le da una instrucción propia: centauro punto net o
  la app, «Mi cuenta», el correo con el que hizo la reserva y «¿Has olvidado tu contraseña?»; le llegará un enlace para
  crear una nueva. No ofrece el envío del correo de contraseña ni transfiere. No usa el plan B de EXPLICACIÓN (que habla
  del correo de la recogida y acaba en «¿Seguimos con los pasos para prolongar?»).
- **Por qué:** el envío (`enviar_correo_contrasena`) comprueba el correo contra el alquiler en curso (spec §5.7); con
  una reserva futura no hay recogida ni correo de la oficina. Con el plan B de EXPLICACIÓN, NOINI-P1 daba 0/3 y 1/3
  (rondas 9 y 10) y el plan B nuevo rompió CORREO-09 (3/3 → 0/3). Ronda 11: `informes/evals-v2.md`.
- **Afecta a:** v2 (nodo «Prolongación»).
- **Quién:** el responsable de la construcción, con la revisión de la Tarea 10 (ronda de arreglos 1, R33).
- **Estado:** aplicada en v2.

## D-006 · 2026-10-18 · Prolongación: detalles poco frecuentes por `buscar_respuesta`
- **Qué:** el prompt «Prolongación» (máximo 22.000 caracteres) no copia enteras DETALLES QUE PUEDES DAR ni LA WEB NO LE
  DEJA de `comun/bloques/consultas-alquiler.md`. Quedan en el prompt los casos frecuentes (precio, importe que muestra
  la web, penalización, prolongar en una oficina, precio caro, condiciones generales; disponibilidad, pago, correo que
  no llega, no ve la reserva) y el resto se pide a `buscar_respuesta` con `detalles_prolongacion` o
  `la_web_no_le_deja`: pagar, el mismo día, ¿está bien hecha?, contrato vencido (y vencido sin poder prolongar),
  devolver antes de la nueva fecha, le falta depósito, otra reserva y esa reserva nueva,
  si ya lo prolongó antes, cobrado sin confirmar, ¿número de reserva?, usuario bloqueado, condiciones, fecha u hora no
  válida y, desde la ronda de arreglos 1 (19/10), «Cuánto se puede prolongar» (desde la ronda de arreglos 4, si pide su propio dato, cola gestion en la misma línea del prompt). «Cambiar de coche» salió en la ronda de arreglos 1 y volvió al prompt en la ronda de arreglos 3 (19/10): fuera, el bot no llamaba a la herramienta (BORDE-05 a 0/3 en la ronda 12). Una línea al final
  de LA WEB NO LE DEJA dice qué tema lleva cada uno.
- **Por qué:** el texto entero del bloque no cabe con el bloque común, el correo de contraseña y la pista (spec §5.4 y
  §5.9: el conocimiento llega por `buscar_respuesta`, no copiado). Los textos son los mismos (`consultas_alquiler.py`).
- **Riesgo:** el bot tiene que llamar a la herramienta con el tema correcto; TARDE-06 usó una vez `la_web_no_le_deja`
  en vez de `detalles_prolongacion` (ronda 10).
- **Afecta a:** v2 (nodo «Prolongación»).
- **Quién:** el responsable de la construcción (Tarea 10).
- **Estado:** aplicada en v2.

## D-005 · 2026-10-18 · Consultas del alquiler se queda con gpt-4.1 (comparación de modelos del spec §7.3)
- **Qué:** el módulo «Consultas del alquiler» de la v2 se queda con `fast-gpt-4.1` (gpt-4.1). Sustituye a D-002 (provisional).
  No cambia ningún nodo: el modelo ya era ese.
- **Por qué:** se pasaron las mismas 56 evals (19 críticas y 37 del resto; BR-05 no cuenta, es de la Tarea 12), 3 veces
  cada una, con los tres modelos y el prompt vigente (23aa720), intercalando los modelos por bloques para que la hora real no
  favoreciera a ninguno (`informes/evals-v2.md`, «Tarea 9c»). Resto: gpt-5.4 93,7 % (104/111), gpt-4.1 91,9 % (102/111),
  gpt-4.1-fast 88,3 % (98/111). Total (168): 91,1 %, 88,1 % y 86,3 %. Ningún modelo cumple «sin fallos críticos» (6, 6 y 5
  críticas por debajo de 3/3), así que se aplica el criterio al resto: el más barato a ≤ 3 puntos del mejor. gpt-4.1 queda a
  1,8 puntos del mejor (2,98 con el total); gpt-4.1-fast, a 5,4 (4,8), fuera. Entre gpt-4.1 y gpt-5.4 el más barato es
  gpt-4.1: el orden de precios sale de las mediciones del repo (spec §1 y §9: gpt-4.1-fast 2,1 créditos por respuesta;
  Consultas con gpt-4.1, 2–2,5; gpt-5.4 con 22.000 caracteres, 4–5), porque HappyRobot no publica tarifa por modelo en su
  documentación.
- **Críticas por debajo de 3/3 (pasan a la puerta 0, Tarea 16):** con gpt-4.1: TEL-C1 0/3, FDS-02 0/3, DEVOL-03a 1/3,
  DEVOL-03c 2/3, FDS-03 2/3 y GC-C1 2/3. Con gpt-4.1-fast: TEL-C1 0/3, FDS-02 0/3, DEVOL-03c 1/3, DEVOL-03a 2/3 y FDS-03
  2/3. Con gpt-5.4: VIRT-C1 2/3, DEVOL-03c 1/3, DEVOL-03a 2/3, FDS-03 2/3, FDS-02 1/3 y GC-C1 2/3. Solo gpt-5.4 pasa TEL-C1
  (3/3); gpt-4.1 y gpt-4.1-fast dan el número de España «para Portugal» en 6 de 6.
- **Riesgo si me equivoco:** gpt-5.4 saca 1,8 puntos más en el resto y es el único que pasa TEL-C1; si negocio quiere
  TEL-C1 resuelta con el modelo y no con el contenido (quitar la crítica o reforzar el prompt), habría que subir a gpt-5.4 y
  arreglar ADV-6 (0/3 con gpt-5.4: llama a `buscar_respuesta` en vez de `buscar_punto_de_encuentro`). Tres ejecuciones por eval
  dejan mucha dispersión (DEVOL-03a con gpt-4.1: 3/3 en la 5b y 1/3 aquí).
- **Afecta a:** v2 (nodo «Consultas del alquiler»); en la Tarea 10, Prolongación sigue con `fast-gpt-5.4` (otra decisión).
- **Quién:** el responsable de la construcción (punto 1 de R25), con las evals de la Tarea 9c.
- **Estado:** aplicada en v2 (sin cambios en el nodo; las críticas abiertas, en `pendientes.md`).

## D-004 · 2026-10-18 · Red de seguridad del modo virtual en «Preparar transferencia»
- **Qué:** de 22:00 a 8:00 (hora peninsular, calculada al ejecutarse el nodo, como la de Gestión), «Preparar
  transferencia» solo transfiere a `asistencia`. Si el modelo pide `minibus` o `nueva_reserva`, no transfiere y
  devuelve `resultado: modo_virtual` con un detalle fijo: no hay compañeros en esa cola a esta hora, no lo vuelvas a
  intentar con ella; si es una avería o un accidente, a la cola asistencia; si no, sigue MODO DE ATENCIÓN (volver a
  llamar a partir de las ocho) sin decir que le pasas con nadie. Si pide `gestion` de noche, gana `gestion_cerrada`
  (Gestión cierra a las 21:00, así que de noche siempre está cerrada). Cambia el spec §5.8 y §5.11. El prompt no
  cambia: el detalle remite a lo que ya dice el bloque de reglas comunes.
- **Por qué:**
  - en modo virtual el modelo a veces transfería igualmente a minibus (ADV-2 de Consultas 1/3 en la ronda 3;
    «VIRTUAL · pide persona» del Triaje 2/3), y una transferencia nocturna deja al cliente en una cola vacía;
  - la excepción del modo virtual en la descripción de `buscar_punto_de_encuentro` del Triaje no sirve: con ella
    VIRT-T1 cae a 0/3 (ronda de arreglos 1 de la Tarea 9). Se queda fuera del Triaje; la de Consultas se mantiene;
  - gana `gestion_cerrada` sobre `modo_virtual` porque COLA DE GESTIÓN CERRADA da el horario real de Gestión y el
    bloque de reglas comunes ya manda seguirla en un caso de gestión, también en modo virtual; con `modo_virtual`
    el bot diría «a partir de las ocho», falso de viernes a domingo y en vísperas de festivo. Así además Gestión se
    transfiere exactamente cuando `gestion_abierta_en` dice que está abierta (lo comprueba la prueba de equivalencia).
- **Afecta a:** v2 (los dos «Preparar transferencia», Triaje y Consultas; los de Prolongación y los demás módulos
  copiarán el mismo código). Código y pruebas: `codigo/preparar_transferencia.py` y
  `codigo/test_preparar_transferencia.py` (71 casos).
- **Quién:** jzerpa (responsable), 18/10/2026, a propuesta de la revisión de la Tarea 9 (R24).
- **Estado:** aplicada en v2 (Tarea 9b).

## D-003 · 2026-10-18 · Consultas: ofrecer la transferencia que manda la sección y transferir al sí
- **Qué:** cuando la sección de `buscar_respuesta` manda transferir («Transfiere a GESTIÓN DE RESERVA…») y el cliente
  no ha pedido hablar con nadie, el bot de Consultas le pregunta si quiere que le pase y transfiere cuando acepta; si
  el cliente ya lo ha pedido, transfiere en ese turno. Cambia el prompt («CÓMO LEER LA SECCIÓN») y la descripción de
  `transfer_to_human_agent`. DEVOL-03 se parte en tres evals críticas: 03a (ofrece o transfiere; valen las dos), 03b
  (acepta la oferta → cola gestion, motivo otro) y 03c (Gestión cerrada: ni ofrece ni transfiere, da el horario).
  REQ-09 (objeto olvidado) pasa a aceptar también la oferta.
- **Por qué:** con «ejecútala en ese mismo turno, sin preguntarle si quiere», los modelos seguían ofreciendo en vez
  de transferir (DEVOL-03: gpt-4.1 0/9 en las rondas 1 a 3; gpt-4.1-fast 0/3). Ofrecer antes es aceptable para el cliente y
  no salta a una cola que no ha pedido (R21 de la revisión de la Tarea 9).
- **Afecta a:** v2 (nodo «Consultas del alquiler» y su `transfer_to_human_agent`).
- **Quién:** el responsable de la construcción, a propuesta de la revisión de la Tarea 9.
- **Estado:** aplicada en v2 (ronda de arreglos 1 de la Tarea 9; resultado en `docs/informes/evals-v2.md`).

## D-002 · 2026-10-18 · Consultas del alquiler con gpt-4.1 hasta comparar modelos
- **Qué:** el módulo «Consultas del alquiler» de la v2 queda con `fast-gpt-4.1`. La comparación del spec §7.3
  (gpt-4.1, gpt-4.1-fast y gpt-5.4; el más barato a ≤ 3 puntos del mejor y sin fallos críticos) se hace en una sesión
  posterior, antes de la Tarea 16.
- **Por qué:** acabar antes la Tarea 9. Lo que se llegó a ver, con el mismo prompt (vuelta 2): gpt-4.1 86,9 % (153
  ejecuciones) y gpt-4.1-fast 89,0 % (136); los dos fallan la crítica DEVOL-03 (`docs/informes/evals-v2.md`).
- **Afecta a:** v2 (nodo «Consultas del alquiler»).
- **Quién:** el responsable de la construcción, a través del controlador de la Tarea 9.
- **Estado:** sustituida por D-005 (18/10/2026, Tarea 9c).

## D-001 · 2026-10-18 · Arquitectura del bot único y plan de migración (fase 1: Minibús + Prolongación)
- **Qué:** spec `specs/2026-10-18-bot-unico-arquitectura.md`. Resumen:
  - **Workflow nuevo** «Centauro Atención España», duplicando Minibús ES v25 (ver C-004).
  - **Triaje** corto (gpt-4.1-fast, ≤ 9.000 caracteres) que solo encamina, y cuatro módulos: Punto de encuentro e
    Información de oficina (los de la v25), **Prolongación** (de la v12, gpt-5.4, ≤ 22.000 caracteres) y
    **Consultas del alquiler** (gpt-4.1 o el que digan las evals).
  - **Saltos:** el Triaje es el centro (`volver_al_triaje` en cada módulo) y hay atajos solo entre los pares
    frecuentes. 12 Module Change: 4 ya existen en la v25 y 8 los crea una persona.
  - **Conocimiento:** el bloque común de consultas llega por la herramienta `buscar_respuesta` (Python generado
    desde `comun/bloques/consultas-alquiler.md`), no copiado en los prompts ni en una base de conocimiento de
    HappyRobot.
  - **Transferencias:** `cola` cerrada en vez de extensión; red de seguridad de Gestión cerrada en el código; el
    bot sigue en la llamada (whisper) mientras se afina.
  - **Extract único** para todos los módulos; medición común para los tres workflows (resolución real y créditos
    por llamada resuelta).
  - **Migración:** primero la línea de Prolongación (ES y EN), después la de Minibús ES; dos semanas por línea con
    puertas de calidad y coste. Las líneas actuales se mueven al workflow nuevo al pasar a producción; la vuelta
    atrás es republicar la versión antigua con sus líneas (ensayado antes con la línea de pruebas).
  - **Decidido además el 18/10:** identificar por correo o por número de reserva (con la pista del dominio del
    correo, `pista_correo`) sin cambiar la regla de envío; de 22 a 8 h solo se transfiere a Asistencia, también en
    la línea de Prolongación; Gestión no atiende los festivos nacionales.
- **Por qué:**
  - Coste medido: 118 créditos por llamada en Prolongaciones V11 frente a 64 en Minibús v25; el LLM por respuesta
    va de 2,1 (Triaje) a 12,4 (V11). Estimación del bot único: 60–75 créditos en la línea de Prolongación.
  - Resolución: 38 % hoy en Prolongaciones (transcripciones), 53 % realista con las respuestas nuevas y el MCP.
  - Las respuestas del alquiler están copiadas en dos bots y se contradicen.
- **Afecta a:** workflow nuevo; Minibús ES y Prolongaciones solo como control y vuelta atrás.
- **Quién:** jzerpa (arquitectura y workflow nuevo aprobados el 18/10; el resto del spec, en revisión).
- **Estado:** propuesta.
