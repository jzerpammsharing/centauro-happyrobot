# Pendientes del caso Atención España

## Antes de construir
- [x] Aprobar el spec (`specs/2026-10-18-bot-unico-arquitectura.md`) (18/10/2026).
- [ ] Revisar el plan de construcción (`planes/2026-10-18-bot-unico-construccion.md`) y elegir cómo se ejecuta.

## Al construir (comprobaciones del spec, §11)
- [x] Qué copia el duplicado de la v25: Module Change, evals, agente de voz (18/10/2026; detalle en «Comprobaciones de
      la Tarea 6»). Copia los 4 Module Change, el agente de voz y los 37 nodos; **no** copia evals, líneas del trigger,
      ajustes del workflow ni tabla de Twin.
- [ ] Que un Module Change pueda volver al Triaje. **Por configuración, sí** (Tarea 12, 19/10/2026): el editor deja
      elegir el Triaje como destino y los 4 Module Change de `volver_al_triaje` tienen `moduleId` del Triaje
      (`01a14f1d-0397-7925-…`, persistent `c5a70932-…`). En evals, el Triaje con el historial de otro módulo no saluda y
      encamina (SALTO-ENTRADA-TR 3/3). **Falta verlo en una llamada** (Tarea 17): que el salto ocurre de verdad, que el
      Triaje no saluda y que un salto a Prolongación sigue en inglés si se hablaba inglés.
- [ ] Que el módulo de destino ve el historial. Las evals lo simulan (las SALTO-ENTRADA traen el historial y dan 3/3),
      pero eso no prueba qué recibe el módulo en una llamada real. Para la llamada de prueba por web de la Tarea 17 (hay
      que publicar en development y decidir `require_webcall_auth`: lo decide una persona, R4 y R13).
- [ ] Cómo cortar la cadena de la transferencia sin transferir con Gestión cerrada, y qué recibe el agente. **Forma
      provisional elegida en la Tarea 8:** Paths «¿Transferir?» después de «Preparar transferencia» (rama «Fallback»
      sin hijos); detalle en «Comprobaciones de la Tarea 8» y en `prompts/atencion-es/v2/transfer.md`. **Falta la
      comprobación conversacional (Tarea 17):** llamada web con `OPCION_PRUEBA = prolongacion` y Gestión cerrada;
      al pedir Gestión, el agente recibe `resultado: gestion_cerrada`, no sale ninguna llamada en RingCentral y el bot
      sigue hablando.
- [ ] Que el whisper es lo que mantiene al bot en la llamada tras transferir (confirmar con HappyRobot).
- [ ] Que un nodo Python acepta el código de `buscar_respuesta`.
- [ ] Que la tabla de Twin se crea sola con los campos del extract (18/10/2026: aún no existe la tabla del workflow
      nuevo, solo las de los workflows que ya tienen runs; se verá con la primera ejecución o al publicar).
- [ ] Horario real de las colas de Minibús y Nueva Reserva de noche (RingCentral, solo lectura).
- [ ] Cómo se mueve una línea entre workflows (publicar el antiguo sin ella o despublicarlo; números que siguen
      en versiones antiguas y borradores).
- [x] Calendario de festivos nacionales de 2026 y 2027 en «Contexto de la llamada» (código de la Tarea 1, pegado en
      la v2 en la Tarea 8, 18/10/2026). Hay que añadir 2028 antes de que acabe 2027 (aquí y en «Preparar
      transferencia»).

## Comprobaciones de la Tarea 6 (18/10/2026)

Duplicado de Minibús ES v25 → workflow `01a14f1b-4ea9-7827-a4f3-4cfb06a896f6` (ver `workflows.md`). Resultado de
las comprobaciones de los apartados 11.1 y 11.7 del spec:

- **Module Change: se copian los 4**, con 37 nodos en total (4 prompt, 14 action, 11 tool, 4 module-change,
  4 condition). Cada uno apunta a un nodo **del workflow nuevo**, no a los de Minibús ES:
  `informacion_oficina` (en Prolongación y consultas) → Información de oficina; `buscar_punto_de_encuentro` (en
  Prolongación y consultas) → Punto de encuentro; `consultas_alquiler` (en Información de oficina) y
  `consultas_alquiler` (en Punto de encuentro) → Prolongación y consultas. Detalle en
  `prompts/atencion-es/v1/module-change.md`.
- **Evals: no se copian.** 0 en los 4 prompts del workflow nuevo, frente a 24 (Triaje), 17 (Información de oficina),
  21 (Punto de encuentro) y 12 (Prolongación y consultas) en la v25, 74 en total. Tampoco hay carpetas de evals.
  Hay que crearlas por API en los nodos nuevos (spec §7.1).
- **Trigger «Inbound Call»: no se copian las líneas** de Minibús (sin configuración, `numbers` vacío), así que no
  hizo falta quitar nada. Tampoco copia `require_webcall_auth: false`: por defecto es `true`, y una prueba por
  llamada web necesitará ponerlo en `false` (decisión de la persona) antes de usar `OPCION_PRUEBA`.
- **Ajustes del workflow: no se copian.** En el workflow nuevo `out_of_office_hours` está vacío (Minibús ES tenía
  `default` con un día de excepción y `horariominibus`), las auditorías no están activadas (Minibús ES: activadas,
  muestreo del 10 %) y el nodo «Receive Customer Call» sigue apuntando a `business_hours_setting_name: "default"`,
  que no existe en el workflow nuevo. Comprobar antes de las primeras llamadas de prueba que el agente no depende de
  ese horario, y decidir si se activan las auditorías.
- **Tabla de Twin:** no existe todavía una para el workflow nuevo (solo `centauro_minibus_spain_runs`,
  `centauro_minibus_italy_runs`, `centauro_minibus_portugal_runs`, `centauro_prolongacion_spain_runs` y
  `centauro_reembolsos_runs`). Revisar su creación y sus columnas tras la primera ejecución o la publicación.
- **Variables en el duplicado:** el JSON de Plate de los nodos apunta bien a los persistent_id nuevos
  (p. ej. «Calcular horario nocturno» pasa de `019fd418-…` a `e51cd732-…`). Pero el **markdown** que devuelve
  `get_node_details` para los prompts conserva los ids antiguos; no pegarlo tal cual al actualizar un prompt.
  `fix_broken_vars` en simulación no encontró referencias rotas.
- **`fix_broken_vars` / test-all:** aunque se acotó con `node_ids`, recorrió la versión entera (12 nodos: 4 bien,
  4 con error, 4 saltados). Los 4 «Initiate customer connection» fallan con «room name is required for inbound voice
  agents», que es lo esperado sin una llamada en curso; no se transfirió nada ni se envió ningún WhatsApp. No es
  una prueba de que las transferencias funcionen.
- **`delete` de `update_workflow_nodes` borra el nodo con todo su subárbol.** Comprobado con nodos desechables
  (un Paths de prueba con una condición y un hijo: desaparecieron los tres; los nodos de prueba ya no están en la
  v2). No hay forma por API de reenganchar un nodo a otro padre (`parent_id` no se puede cambiar con `update`;
  `add` solo inserta un nodo nuevo entre un padre y sus hijos). **Para las tareas siguientes: no borrar nunca un
  nodo con hijos esperando que se reenganchen.**

## Comprobaciones de la Tarea 8 (18/10/2026)

Entrada, transferencias y Triaje en la v2 (detalle en `.superpowers/sdd/2026-10-18-bot-unico-construccion/task-8-report.md`
y en las copias de `prompts/atencion-es/v2/`):

- **«Contexto de la llamada» y «Resolver colas»** pegados y renombrados (los persistent_id no cambian). `LINEAS` lleva
  en HappyRobot los números reales de las cuatro líneas actuales (leídos de los triggers de Minibús ES v25 y de
  Prolongaciones V11); en el repo siguen los marcadores y el trigger de la v2 sigue sin números. El comentario del
  código de la v25 cita como línea española de Minibús una que ya no está en su trigger (desde la v22 la usa
  Reembolsos): la que vale es la del trigger.
- **Variable `OPCION_PRUEBA`**: HappyRobot no admite valores vacíos; vale `ninguna` (el código lo trata como vacía). Para
  la Tarea 17, ponerla a `prolongacion` en *development*. La salida fijada del trigger de la v2 quedó con
  `from_number` = `to_number` = `web` (solo afecta a `test_node`).
- **Transferencia del Triaje** con el patrón nuevo (herramienta con `cola` → «Preparar transferencia» → Paths →
  Transfer). Hallazgos para las Tareas 9 a 11:
  - `test_node` de un Python no usa la salida fijada de una herramienta (los argumentos llegan vacíos): para probar
    «Preparar transferencia» hay que poner `cola` como texto fijo y volver a dejar la variable.
  - `test_node` no ejecuta un Paths («unable to find activityType=PathsExecutor»).
  - Un Transfer creado por API trae `outside_agent_transfer: true` por defecto y falla con «whisper transfer not
    supported for outside agent transfers»: hay que ponerlo a `false`.
  - Un Transfer con número vacío **se ejecuta** en `test_node` (sale `transfer_succeeded: true`, simulado): por eso
    se descartó cortar la cadena con el número vacío.
  - En una herramienta, un `{{persistent_id.variable}}` dentro de un texto plano se queda literal: la variable tiene
    que ir como nodo de variable de Plate.
  - `execution` de la herramienta no se guarda por API; se queda el de por defecto.
  - El Transfer antiguo del Triaje (`b4439401-…`) se borró (era una hoja) y se creó uno nuevo bajo la rama
    «Transferir». **Resuelto en la Tarea 13:** el extract «Registrar resultado de la llamada» leía
    `17c682a0-….extension_destino` (el parámetro ya se llama `cola`) y `b4439401-….transfer_succeeded` (nodo borrado);
    `fix_broken_vars` no lo detectaba porque el extract pasa la prueba. Ahora lee `cola`, `motivo_transferencia`, el
    `resultado` de «Preparar transferencia» y el Transfer nuevo.
- **Evals del Triaje** (37: 24 de la v25 adaptadas y 13 nuevas) en las carpetas «Bot único · Triaje» y «Triaje · de la
  v25 (adaptadas)». Cosas del entorno de evals que conviene saber para las Tareas 9 a 12:
  - `manage_custom_evals get` no devuelve `test_messages`, `variables` ni `expected_tool_calls`: las conversaciones
    de la v25 se rehicieron a partir del nombre y del resultado esperado de cada eval.
  - Las evals **ejecutan la cadena de la herramienta**: un salto pasa la conversación al módulo siguiente (su texto
    aparece después de la llamada) y la transferencia ejecuta «Preparar transferencia» con la hora real (en fin de
    semana, `cola = gestion` devuelve `gestion_cerrada`) y sin las salidas de «Resolver colas» si no se pasan como
    variables (`cola_no_valida`). La transferencia nunca se completa, así que el bot reintenta y da el teléfono.
    El resultado esperado tiene que decir que solo se valora el turno del módulo hasta la llamada; si no, el juez
    suspende por el texto posterior.
  - Cambiar una eval **no** reinicia su lista de ejecuciones (comprobado en la Tarea 9): las de cada ronda se cuentan
    por la hora de creación.
- [x] **Prompt «Prolongación»** provisional (una línea) bajo `prolongar_alquiler`: sustituido en la Tarea 10.

## Comprobaciones de la Tarea 9 (18/10/2026)

- **Consultas del alquiler** construido sobre el nodo heredado «Prolongación y consultas» (mismo nodo, renombrado):
  prompt de 7.979 caracteres con el bloque común, herramienta `buscar_respuesta` → Python «Buscar respuesta» con
  `consultas_alquiler.py` entero (el nodo aceptó los 39.173 caracteres: no hace falta partir `SECCIONES`, §11.6) y el
  patrón de transferencia del Triaje. Los Module Change de `buscar_punto_de_encuentro` e `informacion_oficina` siguen
  como estaban. Ficheros: `prompts/atencion-es/v2/consultas-del-alquiler.md`, `herramientas-consultas.md`,
  `buscar-respuesta.md`.
- [x] **Elegir el modelo de Consultas** (hecho en la Tarea 9c, 18/10/2026; D-005). Comparación del spec §7.3 con el
      prompt vigente (23aa720), 56 evals ×3 por modelo, intercalando los modelos (`informes/evals-v2.md`, «Tarea 9c»):
      resto gpt-5.4 93,7 %, gpt-4.1 91,9 %, gpt-4.1-fast 88,3 %. Se queda `fast-gpt-4.1`. Ningún modelo pasa todas las
      críticas: lo abierto sigue en la lista de abajo.
- [ ] **Evals de Consultas que no cumplen** tras la Tarea 9b (ronda 5, 18/10/2026 20:17, `fast-gpt-4.1`; detalle en
      `informes/evals-v2.md`, «Tarea 9b»). Una sola vuelta de arreglos; sin más: quedan para la sesión de elección de
      modelo y la puerta 0.
  - TEL-C1 (crítica, 0/3 en la 5b y en la ronda 6): el bot ya no da el de Portugal, pero sigue diciendo que el de
    España sirve allí, también con «Asistencia en carretera en España» en el bloque común (R30, ronda 6).
  - DEVOL-03c (crítica, 1/3): ya no dice «no está permitido» (C-005), pero con Gestión cerrada a veces dice «solo si lo
    acordó» o no da el horario de Gestión.
  - FDS-02 (crítica, 0/3): no explica primero el servicio de espera por vuelo retrasado. Depende del modelo.
  - FDS-03 (crítica, **2/3 en la ronda 5b**, cifra oficial; la fallida, por «Gestión está cerrada ahora»). Aparte, como
    dato: con la expectativa aclarada, 2/3 en la 5c; la fallida dice «esté atento al correo» (invento del bot).
  - GC-C1 (crítica, **0/3 en la ronda 5b**, cifra oficial; el juez suspendía por «Gestión está cerrada ahora» y
    «puede llamar», que manda el bloque común). Aparte, como dato: con la expectativa aclarada (ratificada por el
    controlador, R31), 2/3 en la 5c; la fallida dice que la reserva nueva se hace desde el área de cliente.
  - **Tarea 9c (ronda 8, 21:28-21:43, tres modelos; D-005):** críticas por debajo de 3/3 con `fast-gpt-4.1` (el elegido):
    TEL-C1 0/3, FDS-02 0/3, DEVOL-03a 1/3, DEVOL-03c 2/3, FDS-03 2/3 y GC-C1 2/3. TEL-C1 solo la pasa gpt-5.4 (3/3): con
    gpt-4.1 es de modelo, no de contenido. Para la puerta 0 hay tres salidas: reforzar el prompt de Consultas (7.988/8.000, sin
    sitio), subir a gpt-5.4 (más caro; hay que arreglar ADV-6, 0/3 con ese modelo) o aceptar que TEL-C1 y FDS-02 no son
    críticas para este modelo. DEVOL-03a/03c, FDS-03 y GC-C1 fallan con los tres modelos: mezcla de inventos pequeños del bot y
    del juez. NOINI-03 falla (1/3) con los tres: es de contenido («área de cliente» en vez de «Mis reservas y facturas»).
  - Resueltas en la Tarea 9b: REQ-09 3/3 (expectativa), ADV-3 3/3, DEVOL-03a/03b 3/3. GC-C1 3/3 en la ronda 6.
  - DEVOL-03c sigue en 1/3 en la ronda 6 (ofrece un compañero o no da el horario de Gestión).
- [x] **VIRT-T1 (Triaje, crítica)**: cayó a 1/3 en la ronda 6 al nombrar `modo_virtual` en CÓMO TRANSFERIR. Corregido
      en la ronda de arreglos 2 de la Tarea 9b: CÓMO TRANSFERIR vuelve a nombrar solo `gestion_cerrada` y SI LA
      TRANSFERENCIA FALLA dice «otro error sin detalle». Ronda 7 (20:55): VIRT-T1 6/6, VIRT-T2 3/3, VIRT-C2 3/3 y
      VIRT-C1 3/3.
- [x] **Triaje: VIRT-T1 y la descripción de `buscar_punto_de_encuentro`** (cerrado en la Tarea 9b). La excepción del
      modo virtual no se vuelve a poner en el Triaje (con ella VIRT-T1 caía a 0/3); en su lugar, la red de seguridad del
      modo virtual de «Preparar transferencia» (D-004). VIRT-T1 3/3 en la 5b. «VIRTUAL · avería»: expectativa aclarada
      (el reintento tras el fallo es correcto), 3/3.
- **Evals de Consultas:** 56 en el nodo (55 cuentan; BR-05 espera `prolongar_alquiler` y se ejecuta en la Tarea 12).
  Quedan para la Tarea 10 las de Minibús ES v25 ADV-1, PRO-1 y PRO-2 (empiezan en una prolongación). Para el juez:
  - No ve el prompt: lo que el bot puede decir porque está en el bloque común (horario de gestión, «si es urgente, que
    vaya a la oficina», el formulario) tiene que estar en el resultado esperado o lo cuenta como inventado.
  - Lee la frase de aviso de `transfer_to_human_agent` («le paso con un compañero…») como dicha antes de la llamada;
    las evals de transferencia lo aclaran.
  - Suspende por la pregunta final de cortesía y por omitir detalles opcionales si no se le dice; las 34 evals de
    respuesta llevan una nota común (texto en `informes/evals-v2.md`).
- `prolongar_alquiler` y `volver_al_triaje` los nombra el prompt de Consultas, pero las herramientas las crea la Tarea
  12: hasta entonces el bot no puede llamarlas (en una llamada real no saltaría).
- **Resuelto en la Tarea 13** (el extract único ya no lee estas variables; «Registrar consultas del alquiler» queda sin
  uso hasta que lo borre una persona, ver «Para la persona»): el extract «Registrar consultas del alquiler» lee `fbe2e40e-….extension_destino` (parámetro
  quitado de `transfer_to_human_agent` de Consultas) y `1dce23f2-….transfer_succeeded` (el Transfer de Consultas
  borrado en la Tarea 9): `hubo_transferencia_consultas` y `cola_destino_consultas` saldrán siempre «no» / «ninguna»
  hasta que se rehaga. Al rehacerlo, seguir con `invento_condicion` los inventos que se vieron en evals (REQ-03 y
  DEVOL-01).
- **`fix_broken_vars` no se ejecutó en la Tarea 9** (R23), ni en simulación: el `dry_run` hace un test-all de la
  versión y la v2 tiene el nodo «Enviar WhatsApp del punto de encuentro». Las variables se escribieron con
  `{{persistent_id.variable}}` y la estructura se comprobó con `get_workflows`.
- [x] **R24: red de seguridad del modo virtual en «Preparar transferencia»** — hecha en la Tarea 9b (D-004): de 22 a
      8 h solo se transfiere a asistencia; minibus y nueva_reserva devuelven `modo_virtual`; gestion de noche,
      `gestion_cerrada`. Pegada en los dos «Preparar transferencia» de la v2. La Tarea 10 copia el mismo código.
- [ ] **Comprobar `modo_virtual` con `test_node` después de las 22:00** (`cola` fija `minibus` en un «Preparar
      transferencia» y después otra vez la variable). En la Tarea 9b las pruebas fueron a las 20:06–20:07; lo cubren las
      pruebas locales (71) y las evals VIRT-C2 y VIRT-T2, que dan el resultado como mensaje `tool`.
- [ ] **Bloque de consultas, C-005:** los teléfonos de asistencia de Portugal, Italia y Grecia vuelven cuando negocio los
      valide (punto 7 de «Qué falta decidir»); siguen por decidir los de reservas nuevas de otros países y el correo
      del departamento de flotas.
- **El Python de `buscar_respuesta` se llama «Buscar respuesta»** (`workflows.md`); la Tarea 10 debe usar el mismo
  nombre en Prolongación.

## Comprobaciones de la Tarea 10 (18/10/2026)

- **Prolongación** construido: prompt de 21.978/22.000 caracteres (21.946 tras la ronda 13, 21.998 tras la 14 y 21.994 tras la 15; `fast-gpt-5.4`), `enviar_correo_contrasena` (cadena
  de la v12), `pista_correo`, `buscar_respuesta` y la transferencia. Ids en `workflows.md`.
- [ ] **Evals de Prolongación que no cumplen** (ronda 10, 18/10/2026 23:28–23:42; detalle y motivos en
      `informes/evals-v2.md`, «Prolongación (Tarea 10)»). Críticas 60/72, resto 84,5 %. Hecha la única vuelta de arreglos
      que permite la ficha; sin más iteraciones. Críticas por debajo de 3/3:
  - CORREO-09 (0/3): tras dos envíos que no llegan da el plan B en vez de transferir a `gestion` / `error_tecnico`.
    Regresión de la vuelta de arreglos (el plan B de la reserva no iniciada); en la ronda 9 daba 3/3.
  - FDS-06 (0/3) y FDS-01 (1/3): con gestión cerrada no dice que está cerrada ni su horario (o añade el área de cliente
    sin pregunta).
  - HOR-C1 (1/3): con gestión cerrada ejecuta `transfer_to_human_agent` (la red de seguridad no transfiere, pero el
    turno queda mal).
  - FDS-05 (2/3, «would you like me to connect you») y BORDE-09 (2/3, no repite el teléfono).
  - Del resto a 0/3: PISTA-04 (pide otra vez un dato en vez de enviar), PROL-05 (pregunta si seguimos), PROL-06 (vuelve
    a preguntar por la cuenta), TARDE-02 (confirma la cifra), ASEG-03 (no remite a la aseguradora), CIERRE-01 (no
    termina con la despedida), CORREO-20 (da los pasos antes de tiempo) y CORREO-04 (entorno: la cadena real devuelve
    `no_coincide` y el bot transfiere después).
  - Para la próxima vuelta: «da ya los pasos» y el plan B nuevo chocan con CORREO-20 y CORREO-09; el prompt está a 22
    caracteres del máximo, así que cualquier arreglo pide sacar más texto a `buscar_respuesta`.
- [x] **(Sustituido por la ronda 12, abajo.) Tras la ronda de arreglos 1 de la revisión (ronda 11, 19/10 9:22–9:26, Gestión abierta por el reloj real;
      `informes/evals-v2.md`):** críticas 48/72. Arregladas FDS-01, ASEG-03 y CIERRE-01. Siguen por el bot:
  - HOR-C1 (crítica, 0/3 dos veces): con `gestion_abierta: false` ejecuta a veces `transfer_to_human_agent` (en una
    llamada real la variable y el reloj coinciden y la red de seguridad del código no transfiere, pero el turno queda
    mal) o no dice el cierre.
  - FDS-06 (crítica, 2/3 dos veces): a veces da la alternativa sin decir que gestión está cerrada.
  - CORREO-09 (crítica): transfiere bien a `gestion` / `error_tecnico` en 5 de 6, pero en 1 de 6 anuncia sin ejecutar;
    el resto de fallos son del entorno (abajo).
  - CORREO-20 (0/3): sigue dando los pasos en el turno del plan B.
  - NOINI-P1 (1/3): no menciona el enlace.
  - HOR-A1 (2/3): no da la regla general de cuánto se puede prolongar antes de transferir. Causa probable: la línea «Otra duda
    del alquiler… buscar_respuesta… sin salir de aquí» de TU TAREA (abajo, ronda 14).
- [x] **Evals de transferencia con la hora real (entorno):** arreglado en la ronda de arreglos 2: las 14 evals de transferencia
      llevan las `cola_*` como variables y la nota «una segunda llamada tras un error del entorno no es un fallo».
- [ ] **Tras la ronda de arreglos 2 (ronda 12, 19/10 9:49–10:17, con las `cola_*` en las evals de transferencia;
      `informes/evals-v2.md`):** críticas 63/72, resto 87,2 %. Sin más vueltas (R33). Quedan:
  - HOR-C1 (crítica, 0/3): con `gestion_abierta: false` ejecuta `transfer_to_human_agent` (2 de 3). No lo arregla ni la
    regla sobre lo que devuelve `buscar_respuesta` ni la frase propia de gestión cerrada en ESCALADO.
  - FDS-06 (crítica, 0/3): da la alternativa sin decir el cierre. Pendiente de la regla de la v12 en el bloque común
    (abajo).
  - HOR-A1 (crítica, 1/3): da la regla y se queda. Causa probable: la línea «Otra duda del alquiler… buscar_respuesta… sin
    salir de aquí» de TU TAREA (abajo, ronda 14); no la frase de la ronda de arreglos 2.
  - BORDE-05 (0/3): por sacar «Cambiar de coche» a `buscar_respuesta` (D-006). Devuelta al prompt en la ronda de
    arreglos 3.
  - HOR-01 (crítica, 2/3): una vez dice que «lo deriva» al equipo de gestión.
  - **PROL-05 (0/3 en las rondas 9, 10 y 12):** tras una respuesta que no es sí/no, vuelve a preguntar si seguimos en
    vez de dar los pasos. Se quitó la cláusula «da ya los pasos» porque rompía CORREO-20 (ahora 3/3); PROL-05 queda
    abierta con ese motivo.
  - Del resto a 0/3: PISTA-04 (pide otra vez un dato en vez de enviar), PROL-06 (vuelve a preguntar por la cuenta) y
    TARDE-02 (añade cortesía y penalización en vez de «es la tarifa vigente»). WEB-08 (1/3) suspende porque el juez
    exige una pregunta que la expectativa no pide.
- [ ] **Tras la ronda de arreglos 3 (ronda 13, 19/10 10:30–10:33, Gestión abierta por el reloj; `informes/evals-v2.md`):**
      críticas 67/72. FDS-06 arreglada (3/3), BORDE-05 3/3. Sin más vueltas. Quedan:
  - HOR-C1 (crítica, 1/3): aún ejecuta a veces `transfer_to_human_agent` con `gestion_abierta: false`. El arreglo
    estructural va a la puerta 0 (siguiente punto).
  - HOR-A1 (crítica, 1/3): no ofrece ni ejecuta la transferencia tras decir que gestión lo tiene que revisar. Causa
    probable: la línea «Otra duda del alquiler… buscar_respuesta… sin salir de aquí» de TU TAREA: «cuánto se puede prolongar»
    pasa por ahí y el bot da la regla y se queda, sin seguir a ESCALADO. Arreglo en la ronda de arreglos 4.
  - HOR-01 (crítica, 2/3): una vez manda a la oficina en vez de al área de cliente.
  - PISTA-04 (0/3): sigue pidiendo otra vez el nombre.
- [ ] **Tras la ronda de arreglos 4 (ronda 14, 19/10 10:40–10:47, lunes, Gestión abierta por el reloj;
      `informes/evals-v2.md`):** críticas 69/72; PISTA-01 a 03, CORREO-20 y NOINI-P1 a 3/3. Sin más vueltas. Quedan:
  - HOR-A1 (crítica, 2/3, antes 1/3): con «; si pide un dato de su reserva, cola gestion» en la línea de «Otra duda
    del alquiler», una de tres sigue diciendo que gestión debe revisarlo y le remite a la web, sin ofrecer ni ejecutar
    la transferencia.
  - HOR-C1 (crítica, 2/3): fuera de esta ronda (R34, punto siguiente).
  - BORDE-09 (crítica, 2/3): una vez no dice el uno uno dos ni que ahora no puede pasarle. Ejecución suelta del modelo;
    en las rondas 12 y 13 dio 3/3.
  - HOR-01 (3/3 en la ronda 14). Los fallos de las rondas 12 y 13 no venían de la línea de HOR-A1: «lo deriva» al
    equipo de gestión (ronda 12) y manda a la oficina sin el área de cliente (ronda 13). Lo segundo lo permite el
    bloque común («si es urgente para hoy, que vaya a la oficina») y la eval pide el área de cliente; el bloque dice
    «ese horario o su área de cliente». Es del modelo o de la eval; no se tocó el prompt.
  - PISTA-04 (0/3): con «Pide solo los datos que falten, uno por turno» y «sin pedirlos de nuevo» en PISTA, sigue
    pidiendo el nombre en vez de ejecutar `enviar_correo_contrasena`. Falta mirar la conversación de la eval: si el
    nombre y la fecha no están en los turnos `user` (solo en la llamada a `pista_correo`), el bot no los ve como
    dados.
- [x] **R34: HOR-C1 va a la puerta 0 con el arreglo estructural** (Tarea 15b, D-013: ver «Comprobaciones de la Tarea 15b»). Tres redacciones del prompt no la llevan a 3/3
      (rondas 11 a 13). El arreglo es el del punto siguiente (el aviso del `message` `ai` suena antes de «Preparar
      transferencia», y la herramienta decide por el reloj). Afecta a los tres módulos y se hace en la Tarea 12/16 y
      en la puerta 0. Hasta entonces es una crítica abierta (2/3 en la ronda 14, sin tocarla).
- [ ] **Tras la ronda de arreglos 5 (ronda 15, la última, 19/10 10:57–10:59, lunes, Gestión abierta por el reloj;
      `informes/evals-v2.md`):** críticas 73/75 (HOR-A1 6/6). La regla «si pide un dato de su reserva, cola gestion»
      está en los tres sitios por los que puede entrar «cuánto se puede prolongar» (EXPLICACIÓN, «Otra duda del
      alquiler» y «Otros detalles» de LA WEB NO LE DEJA). La causa de HOR-A1 sigue sin probar. Quedan:
  - HOR-01 (crítica, 2/3): una vez no dice el cierre ni el área de cliente y sugiere la oficina.
  - FDS-05 (crítica, 2/3): una vez «Would you like me to connect you…».
  - BORDE-09 (crítica): 2/3 en la ronda 14 y 3/3 en la 15. Dispersión del modelo, como HOR-01 y FDS-05: no se tocan.
  - PISTA-04 (0/3): la eval está bien (el nombre y la fecha están en el primer turno `user`). Sigue pidiendo el
    nombre en vez de ejecutar `enviar_correo_contrasena`; queda con el motivo del juez.
  - HOR-C1: 3/3 en la ronda 15, sin tocarla. Sigue en R34.
- [x] **El aviso «le paso con un compañero» suena antes de saber si Gestión está cerrada (Tarea 12/16 y puerta 0).** Tarea 15b, D-013: hecho en Prolongación y Consultas; el Triaje queda abierto en «Comprobaciones de la Tarea 15b».
      Es el `message` tipo `ai` de `transfer_to_human_agent`: el agente lo dice al ejecutar la herramienta, antes de que
      «Preparar transferencia» devuelva `gestion_cerrada` (o `modo_virtual`). Con Gestión cerrada el cliente oye «le
      paso» y después «no he podido». Afecta a los tres módulos con transferencia (Triaje, Consultas y Prolongación).
      Salidas posibles: `message` tipo `none` y que el agente diga el aviso solo tras `transferir`, o un Paths antes del
      mensaje. HOR-C1 (0/3 en la ronda 12) depende de esto: el arreglo estructural pasa a la puerta 0.
- [ ] **Hora real en las evals que esperan Gestión cerrada:** con `gestion_abierta: false` en la eval pero el reloj en
      horario de Gestión, «Preparar transferencia» sí transfiere (usa el reloj, no la variable). Las evals HOR-C*, FDS-*
      y GC-P1 no deben medirse por la cadena real: el juez solo puede valorar la decisión del bot.
- [ ] **Mejora de la spec §5.7 sin hacer:** que «Enviar correo» no se ejecute si el correo no coincide. Se puede hacer
      por API: un Paths nuevo bajo «Decidir envío» (`estado` = `coincide` / resto) con un «Resultado para el agente» en
      cada rama (en la rama de envío, después de «Enviar correo»; en la otra, solo con la salida de «Decidir envío»). Lo
      que falta comprobar es si el agente recibe como resultado de la herramienta la salida del «Resultado» que se
      ejecuta (hoy toma la del último nodo de la cadena; con dos ramas no está visto). Hoy, si no coincide, «Enviar
      correo» se ejecuta con `email` vacío y el MCP lo rechaza (como en la v12). No construido.
- [ ] **Regla de la v12 perdida, para la Tarea 12/16 (FDS-06, FDS-01):** la v12 decía en GESTIÓN CERRADA (punto 3,
      `casos/prolongaciones/prompts/prolongacion-es/v12/prolongacion.md`): «En el PRIMER turno en que el cliente pida
      una persona, un agente o algo que solo un compañero puede hacer, dile con claridad que ese equipo está cerrado y
      qué puede hacer… No esperes a que lo pida varias veces». El bloque común solo dice «en cuanto necesite algo que solo
      puede hacer gestión», y en Prolongación ganaba ESCALADO («Pide una persona: pregunta una vez qué necesita»), así
      que con gestión cerrada el bot preguntaba o daba la alternativa sin decir el cierre. No se toca el bloque común
      (no tiene sitio, R33). Arreglo dentro de Prolongación (ronda de arreglos 1, 19/10): ESCALADO separa «pide una
      persona con gestión cerrada» (decir en ese turno que está cerrada, su horario y que llame entonces; si es cliente,
      ofrecer ayuda) de «con gestión abierta» (preguntar una vez qué necesita). Al revisar el bloque común (Tarea 12/16),
      recuperar la frase de la v12 para todos los módulos.
- [ ] **`pista_correo`: ramas sin confirmar.** El Paso 3 (22:54, datos inventados) solo vio `no_verificado`
      (`encontrada: false`, sin error). No se ha visto el texto real del MCP cuando no interpreta la reserva o el nombre
      (`dato_no_interpretado`) ni el caso `verificado` con `email_hint`: este último solo con una reserva real, en la
      puerta 0. Si el texto de error no casa, sale el detalle genérico (correcto, pero menos útil).
- [ ] **Evals que esperan `volver_al_triaje`** (ESC-04, PRO-1, PRO-2): no se ejecutaron (R5); van en la Tarea 12.
- **`fix_broken_vars` no se ejecutó en la Tarea 10** (R23). Variables escritas con `{{persistent_id.variable}}` y
  comprobadas con `get_workflows` y `get_node_details`.

## Comprobaciones de la Tarea 11 (19/10/2026)

Punto de encuentro e Información de oficina con el bloque de reglas comunes (prompts subidos, 34.595 y 33.210
caracteres; modelos sin cambios). Detalle en `.superpowers/sdd/2026-10-18-bot-unico-construccion/task-11-report.md`,
`prompts/atencion-es/v2/punto-de-encuentro.md`, `informacion-de-oficina.md` y sus `herramientas-*.md`.

- [ ] **Transferencia de los dos módulos a medio hacer (bloqueante antes de cualquier llamada de prueba).** Las dos
      `transfer_to_human_agent` ya tienen los parámetros nuevos (`cola`, `motivo_transferencia`, `resumen_para_agente`)
      y la descripción que empieza por «Gestión ahora: [gestion_abierta]», pero siguen colgando del Transfer de la v25
      (`01a14f1d-0396-7961-…` en Punto de encuentro y `01a14f1d-0396-788f-…` en Información de oficina), cuyo
      `number` lee el parámetro de la extensión que ya no existe y cuyo `fallback_number` es la cola de Minibús: en
      una llamada, **cualquier transferencia de estos módulos iría a Minibús y sin la red de seguridad de Gestión
      cerrada ni del modo virtual; también una avería, que iría a la cola Minibús y no a Asistencia**. R35: el
      responsable no ha autorizado borrar los Transfer. El 19/10 a las 11:15 el sistema de permisos rechazó borrar esos dos Transfer
      (son hojas). Falta, con permiso de la persona o en el editor: borrar los dos Transfer y crear en cada herramienta
      Python «Preparar transferencia» (código de `codigo/preparar_transferencia.py`, `cola` =
      `{{00435498-eccf-4110-9cf1-eb17821af3ed.cola}}` / `{{62c5b6dd-5dde-4b3a-9a93-adb638c0bd66.cola}}` y las cuatro
      `cola_*`) → Paths «¿Transferir?» → «Transferir» (`transferir` es true) → Transfer con `number` y
      `fallback_number` = `numero`, whisper «Llamada del asistente de atención.» + `resumen_para_agente` de la herramienta +
      `telefono_dictado` (spec §5.8; el Transfer viejo dice «Llamada del asistente de minibús.») y
      `outside_agent_transfer: false`, como en Prolongación. Después, repetir las evals de transferencia y GC-PE1,
      GC-IO1 y VIRT-PE1.
- [ ] **ADV-7 (crítica, 0/3 en las rondas 16 y 17):** con una queja del minibús y una pregunta de prolongar en el mismo
      turno, ejecuta `consultas_alquiler` antes de transferir a minibus, también con la regla «la queja va primero».
      Para la Tarea 16: probar a ponerlo en SI "EL BUS TARDA DEMASIADO" o en la descripción de `consultas_alquiler` de
      este nodo («NO la uses si en el mismo turno se queja del minibús»).
- [ ] **Ronda 18 (ronda de arreglos 1, 17:58–18:00):** ADV-7 3/3 (arreglado). Quedan ADV-11 (crítica, 0/3: con
      Gestión cerrada y «páseme con quien lo gestione» da el horario de gestión en vez de `consultas_alquiler`
      prolongar; depende de R36) y PE-NOCT-1 0/3 (sigue preguntando la puerta de Atenas pese a «antes de preguntar la
      terminal o la puerta»). ADV-8 2/3.
- [ ] **Ronda 19 (ronda de arreglos 2, 18:25–18:27):** críticas 20/27.
  - ADV-11 (crítica) sigue a 0/3: con Gestión cerrada y «páseme con quien lo gestione» da el horario de gestión y el
    área de cliente sin llamar a `consultas_alquiler`. Causa (revisión de la ronda de arreglos 3): el esquema de
    `transfer_to_human_agent` ponía «la hora o el día de devolución» como caso de gestión, no el bloque común. Arreglado
    en la ronda 20 (3/3).
  - «VIRTUAL · cambiar hora de devolución» (crítica) cae a 0/3 por la eval, no por el bot: con R36 el bot ya ejecuta
    `consultas_alquiler` (prolongar) y no transfiere, pero el juez valora el texto posterior de Consultas («puede
    retrasarla», «depende de disponibilidad») contra una expectativa que aún pide el horario de gestión. Hay que
    adaptar la eval a R36 (esperar `consultas_alquiler` y no valorar lo posterior).
  - «Idioma · EN · 25 minutos» (crítica) 2/3: en una el resumen no termina con «El cliente habla inglés».
  - PE-NOCT-3 (nueva) 0/3: con PRIMERO true, ante «el minibús no pasa y mi vuelo llegó tarde» da el punto P6 de
    Valencia en vez del aviso de cierre y no llama a `consultas_alquiler`. Causa parcial (revisión): la viñeta 2 de EN MODO
    VIRTUAL («si el minibús no llega… que espere en el punto indicado»). La ronda de arreglos 3 puso «Si PRIMERO dio
    true, esta sección no se aplica» al principio de EN MODO VIRTUAL y sigue a 0/3 en la ronda 20 (da el punto P6 y no
    llama a la herramienta). Causa añadida en la ronda de arreglos 4 (las variables de la eval están bien:
    `nocturno_cet` y `modo_virtual` true en la llamada `create`): «SI EL VALOR ES true» solo nombraba el vuelo
    retrasado, no la queja de que el minibús no pasa, y el último párrafo de SI «EL BUS TARDA DEMASIADO» («como mucho,
    una frase con el cartel») no estaba condicionado a PRIMERO.
  - ADV-8 1/3: anuncia que consulta el precio sin ejecutar la herramienta.
  - Arreglados: PE-NOCT-1 3/3 (0/3 en la ronda 18).
- [ ] **Ronda 20 (ronda de arreglos 3, 21:53–21:58, lunes; a las 22:00 empieza el modo virtual por el reloj, pero
      estas evals fijan `modo_virtual` por variable y estos módulos aún no tienen «Preparar transferencia»):** críticas
      26/27. ADV-11 3/3, «VIRTUAL · cambiar hora» 3/3 (eval reescrita por R36), «Idioma · EN · 25 minutos» 3/3.
      Quedan: GC-IO1 2/3 (con R36 ahora llama a `consultas_alquiler` prolongar ante «¿me cambian la hora de
      devolución?» y en una el juez exige el horario de gestión: la eval tiene que aceptar ese camino, ya lo admitía en
      el texto), PE-NOCT-3 0/3 (arriba) y ADV-8 0/3 (ahora ejecuta `consultas_alquiler` antes de dar el punto y el juez,
      por la nota «valora solo lo dicho antes de la primera llamada», no ve el punto: la nota de la eval choca con la
      regla nueva «da el punto y ejecuta la herramienta en ese mismo turno»).
- [ ] **Ronda 21 (ronda de arreglos 4, 22:10–22:11, lunes; el reloj ya estaba en modo virtual, pero estas evals
      fijan `modo_virtual` por variable y estos módulos aún no tienen «Preparar transferencia»):** críticas 26/27.
      GC-PE1 3/3 y GC-IO1 2/3, reescritas por R36 (esperan `consultas_alquiler` prolongar); el fallo de GC-IO1 es del
      juez, que toma la `pregunta` de la llamada por «texto previo». ADV-8 2/3 (en una nombra que consulta el precio y
      hace una segunda llamada). PE-NOCT-1 3/3, PE-NOCT-2 3/3. **PE-NOCT-3 sigue 0/3** (da el punto P6 y no llama a
      `consultas_alquiler`) aunque «SI EL VALOR ES true» ya cubre la queja del minibús: no se puede ver con qué valores
      se resolvieron las variables en la ejecución (`get` no las devuelve, `list_runs` solo da el veredicto y el run de
      la eval no existe en `monitor_runs`). Siguiente paso propuesto: una eval de control «Valencia, ¿dónde está el
      minibús?» con `nocturno_cet` true y sin queja, para saber si el modelo lee el valor en LISTA 1.
- [ ] **Ronda 22 (ronda de arreglos 5, la última; 22:19–22:21, lunes, reloj en modo virtual; las evals lo fijan por
      variable):** críticas **27/27** (GC-IO1 3/3 con la aclaración de que la `pregunta` no es texto previo). ADV-8 2/3
      (dispersión: en una nombra que consultará el precio antes de la llamada; prompt sin tocar). PE-NOCT-1 3/3,
      PE-NOCT-2 3/3. **Sigue abierto PE-NOCT-3 (R38)**, con «EL BUS TARDA DEMASIADO» ya condicionado a PRIMERO false:
      - PE-NOCT-3 (queja + vuelo, `modo_virtual` true, `nocturno_cet` true): 0/3, da el punto P6.
      - PE-NOCT-3b (queja + vuelo, `modo_virtual` false, `nocturno_cet` true): 0/3, transfiere a minibus (dos veces).
      - PE-NOCT-3c (sin queja, «¿dónde cojo el minibús?», `modo_virtual` true, `nocturno_cet` true): 1/3; en 2 da el P6.
      Diagnóstico: falla con Valencia y la LISTA 1 aunque no haya queja ni modo virtual de por medio, mientras que
      PE-NOCT-1 (Atenas, LISTA 3) pasa 3/3. El modelo (`fast-turbo-one`) no aplica PRIMERO de forma fiable en un
      aeropuerto español; con queja, la regla de la queja (transferir o el consejo del modo virtual) gana siempre.
      Propuesta: que el código decida el cierre (por ejemplo, que «Contexto de la llamada» o el Triaje pase
      `oficina_cerrada` del aeropuerto ya resuelto, en lugar de que el modelo busque en las cuatro listas), o subir
      Punto de encuentro a un modelo que razone. Fuera del alcance de la Tarea 11.
- [ ] **Resto por debajo del 90 % (89,2 %, ronda 17):** PE-NOCT-1 1/3 (pregunta la puerta de Atenas antes de dar el
      aviso de cierre: la regla de las terminales de QUÉ HACER AHORA compite con PRIMERO), Sevilla falso meeting point
      1/3 y caseta 2/3 (añade dónde espera el minibús), ADV-8 2/3, Madrid ambiguo 2/3, Sevilla a medianoche 2/3, Sants
      2/3, PDE-2 2/3 (juez). Motivos en `informes/evals-v2.md`.
- [ ] **R36 (para que lo confirme el responsable): «devolver más tarde».** En los dos módulos, quedarse el coche más
      tiempo (devolverlo otro día o más tarde, alargando el alquiler) es prolongar (`consultas_alquiler`, tema
      `prolongar`), aunque pida que le pasen con alguien o con gestión y también con gestión cerrada: lo hace el
      cliente en la web o la app. Cambiar un dato ya acordado que no sea alargar (el buzón de llaves…) es un caso de
      gestión. R37 (ronda de arreglos 2): se quitó el ejemplo «otra hora el mismo día». ADV-11 exige
      `consultas_alquiler`.
- [ ] **Ronda 23 (Tarea 12, 19/10/2026, 22:30–22:31; reloj en modo virtual, las evals lo fijan por variable):** la
      queja y el «enfadado o puede perder una conexión» de Punto de encuentro llevan ya la excepción de PRIMERO (arrastre
      de la Tarea 11; prompt 36.382 caracteres, subido a las 22:29). Críticas de Punto de encuentro (GC-PE1, VIRT-PE1,
      PDE-5, ADV-7, «DÍA · 25 minutos», «Idioma · EN · 25 minutos») **18/18**. **PE-NOCT-3 0/3** (da el punto P6, sin
      `consultas_alquiler`) y **PE-NOCT-3b 0/3** (transfiere a minibus dos veces): el texto no basta; sigue la propuesta
      de que el código decida el cierre.
- [x] **Saltos que nombra el prompt** (Tarea 12): las 8 herramientas se crearon por API el 19/10/2026 a las 22:27 y
      el responsable creó sus 8 Module Change en el editor (12 en total; `prompts/atencion-es/v2/saltos.md`). ADV-12,
      «VIRTUAL · pregunta por el minibús» y «ES · pregunta por el minibús (Palma)» ya cuentan: 3/3 (ADV-12 tras añadir a
      `buscar_punto_de_encuentro` de Información de oficina «a qué hora pasa el minibús… no lo contestes tú»). Antes de la Tarea 12:
      `informacion_oficina` y `volver_al_triaje` en Punto
      de encuentro; `buscar_punto_de_encuentro` y `volver_al_triaje` en Información de oficina. Hasta entonces,
      Información de oficina contesta o llama a `consultas_alquiler` cuando le preguntan por el minibús (ADV-12,
      «VIRTUAL · pregunta por el minibús» y «ES · pregunta por el minibús (Palma)», 0/3, no cuentan).
- [ ] **`consultas_alquiler` de estos dos nodos** conserva la descripción y los temas de la v25 (incluido `prolongar`,
      que en el Triaje ya va por `prolongar_alquiler`). No se tocó (R5: sus Module Change apuntan a Consultas). Revisar
      en la Tarea 12 si el tema `prolongar` debe pasar a `prolongar_alquiler`.
- **Evals:** 43 (25 + 18), de Minibús ES v25 (conversaciones recuperadas del registro de sesiones) y 5 nuevas.
  `create` no guarda `folder_id`: hay que pasarlo después con `update`. Con `expected_tool_calls: []` el juez no
  exige ninguna herramienta (ADV-8 pasa con o sin `consultas_alquiler`).
- **`fix_broken_vars` no se ejecutó** (R23). Variables escritas con `{{persistent_id.variable}}`; `get_node_details`
  (Plate) muestra 8 nodos de variable en Punto de encuentro y 3 en Información de oficina, todos con `group_id`
  `e51cd732-…`.

## Comprobaciones de la Tarea 12 (19/10/2026)

- [x] **SALTO-03b:** 3/3 en la ronda 25 con la frase nueva en la descripción de `volver_al_triaje` de Prolongación
      (D-009). Historia:
      Antes de la ronda 25 (Prolongación, «tengo otra consulta distinta, que no es de mi alquiler»): en vez de
      `volver_al_triaje` pregunta qué consulta es (antes de la vuelta de arreglos, con «quiero que borren mis datos»,
      llamaba a `buscar_respuesta` y ofrecía un compañero, 1/3). Punto de encuentro, Información de oficina y Consultas
      saltan en el mismo caso (SALTO-01a/01b, 02a/02b, 04b, 3/3). Es el único modelo que razona (`fast-gpt-5.4`):
      preguntar antes de saltar no es grave (al contestar, salta), pero cuesta un turno. Propuesta: en la línea de
      `volver_al_triaje` del prompt de Prolongación, «también si solo dice que tiene otra consulta, sin decir cuál».
- [x] **GC-IO1: 3/3 en la ronda 26** tras la ronda de arreglos 2 (viñeta de ESCALADO y descripción de `consultas_alquiler` de Información de oficina, D-009). Antes: **0/3 en la ronda 25 (regresión de la Tarea 12)** (3/3 en la ronda 22): con Gestión cerrada, «¿me cambian la hora de
      devolución?» ya no llama a `consultas_alquiler` prolongar; dice que gestión está cerrada y da los pasos de la
      web. No ejecuta ninguna herramienta de salto. Entre las dos rondas cambió la lista de herramientas de Información
      de oficina (se añadieron `buscar_punto_de_encuentro` y `volver_al_triaje`, y la frase del minibús). La causa no
      está probada. Para la siguiente vuelta: mirar la conversación de la ejecución. Si es por el número de
      herramientas, reforzar la línea de prolongar del prompt.
- [ ] **Críticas de Consultas por debajo de 3/3 en la ronda 25:** TEL-C1 0/3, FDS-02 0/3, DEVOL-03c 1/3, DEVOL-03a
      2/3, FDS-03 2/3 y GC-C1 2/3. Son las mismas de la Tarea 9 con `fast-gpt-4.1` (D-005, puerta 0); no las causa la
      Tarea 12. Prolongación: HOR-C3 2/3 y FDS-05 2/3.
- [ ] **IDO-1 1/3 en la ronda 26:** la llamada es correcta; el juez valora el texto posterior (en una se contradice). Añadir a su expectativa la nota «lo posterior a la llamada no cuenta», como en GC-IO1.
- [ ] **«Borrar mis datos de cliente»** no es de ningún módulo: Punto de encuentro lo manda a `consultas_alquiler` y
      Información de oficina transfiere a gestión. Falta decidir con negocio a dónde va (probablemente gestión).
- [ ] **SALTO-ENTRADA-PE:** en una ejecución ofrece el WhatsApp con `whatsapp_disponible` false (el juez lo dio por
      bueno). Vigilar.
- [ ] **En una llamada (Tarea 17):** §11.2 y §11.3 (arriba, «Al construir»).

## Comprobaciones de la Tarea 13 (19/10/2026)

- [x] **Extract único** «Registrar resultado de la llamada» (`aea14d45-…`): 46 campos (los 45 de §5.12 y
      `origen_opcion`), entrada con la transcripción, «Contexto de la llamada» y los parámetros y salidas de las
      herramientas de los cinco módulos, más el `callCount` de los 12 Module Change. Copia en
      `prompts/atencion-es/v2/registrar-resultado.md`. Las referencias rotas que se arrastraban (Tareas 8 y 9) ya no
      están.
- [x] **Rama de WhatsApp:** «Preparar WhatsApp minibús» lee `whatsapp_aceptado`, `punto_whatsapp` e `idioma_cliente`
      del extract único. Comprobado con `get_available_variables`: las 46 salidas `response.*` del extract son
      visibles desde ese nodo.
- [x] **«Receive Customer Call»:** `transcription_context` ampliado y `business_hours_setting_name` vacío (R12). La voz
      ya era solo «Pablo Galvez HR». Copia en `receive-customer-call.md`.
- [x] **`test_node` del extract** con una llamada inventada (Triaje → Consultas → Prolongación, un salto y una
      transferencia a asistencia): los 46 campos con un valor permitido. Para la prueba se pusieron salidas de prueba
      (`set_custom_output`) en 11 nodos: «Receive Customer Call», `consultas_alquiler` del Triaje, `buscar_respuesta` y
      «Buscar respuesta» de Consultas, `prolongar_alquiler` de Consultas y su Module Change, la transferencia de
      Prolongación («transfer_to_human_agent», «Preparar transferencia», «Initiate customer connection»), «Resultado
      para el agente» y «Pista del correo» (estas dos, vacías). Son solo datos de prueba de la v2; un `test_node` de esos
      nodos los vuelve a escribir.
- [x] **`fix_broken_vars` no se ejecutó** (R41), ni en simulación: las variables del extract, de «Preparar WhatsApp
      minibús» y de «Receive Customer Call» se comprobaron una a una con `get_available_variables` (97 referencias del
      extract, 0 rotas).
- [ ] **`invento_condicion` no existe en §5.12:** los inventos de las evals (REQ-03, DEVOL-01 y FDS-03, «esté atento al
      correo») se siguen con `invento_informacion`, que los cita como ejemplos. Si se quiere separar «condición
      inventada» de otros inventos, añadir el campo al spec antes.
- [ ] **Punto de encuentro e Información de oficina** siguen con el Transfer de la v25 sin «Preparar transferencia»
      (R35): el extract lo tiene en cuenta (`hubo_transferencia` = si con `cola` informada; `intento_gestion_cerrada`
      con `gestion_abierta` false). Cuando se cree su cadena, añadir al extract el `resultado` de sus «Preparar
      transferencia» y el `transfer_succeeded` de sus Transfer nuevos.
- [x] **`medir_bots.py` y la rutina** deben leer los nombres y valores de `registrar-resultado.md` (spec §5.12). La cola
      va como `gestion` (no `gestion_reserva` como en la v25 y la v12). Hecho en la Tarea 15: `normalizar_llamadas.py`
      iguala `gestion_reserva` y `gestion` y la rutina lee `motivo_principal`, `saltos` e `intento_gestion_cerrada`.

## Comprobaciones de la Tarea 15 (19/10/2026)

- [ ] **Créditos por run sin probar contra la API: no hay `HAPPYROBOT_API_KEY`.** `scripts/creditos_runs.py` está hecho
      y probado sin red (31 casos); sin clave sale con código 2 y la rutina deja `creditos` = null (en la prueba, 20 de
      20 llamadas sin créditos, y el artefacto lo avisa). Para probarlo de verdad con 3 runs de la V11 hace falta:
      1. una clave de API de HappyRobot del workspace de Centauro con permiso de lectura de facturación, puesta como
         variable de entorno (`export HAPPYROBOT_API_KEY=…` en la sesión o en la configuración de la rutina; nunca en
         el repo);
      2. `python3 -I scripts/creditos_runs.py <fichero con 3 run_id de la V11> --crudo` para ver la forma real de la
         respuesta (la documentación da la ruta, `GET /billing/usage/runs/{run_id}`, pero no los campos);
      3. si la base no es `https://platform.happyrobot.ai` (la de los ejemplos de la API pública), ponerla en
         `HAPPYROBOT_API_BASE`; si la respuesta no trae el total en `total_credits`, `credits` o `total` (ni partidas
         con `credits`), añadir su campo a `creditos_de_respuesta` con una prueba;
      4. comparar con lo conocido: unos 118 créditos por llamada en la V11 (spec §8.2).
      Runs de la V11 del 16/10/2026 para la prueba: los tres primeros de la muestra (en
      `datos/atencion-es-2026-10-19-prueba/ids_v11_3.txt`, no versionado).
- [ ] **Separar los créditos por módulo y voz** (spec §6): la API por run da el total; si da partidas, añadir el
      reparto al informe.
- [ ] **La rutina no está programada** (lo decide una persona). Prompt: `rutinas/informe-atencion-es.md`; propuesta a
      las 07:30 de Madrid sobre el día anterior.
- [ ] **El artefacto [Calidad Atención España](https://claude.ai/artifact/4YyyT2jrKTe1TjhGdApnh7) es privado**: solo lo
      ve su dueño hasta que lo comparta desde el menú Compartir. Tiene un documento de prueba (`informes/2026-10-16`,
      muestra de 20 llamadas). Borrarlo o dejarlo lo decide el responsable; la rutina no borra documentos.
- [ ] **Saltos de Minibús ES:** la v25 también salta entre módulos, pero su extract no los cuenta; la rutina deja
      `saltos` = null en los bots actuales y el % con 3 o más saltos solo se mide en el bot único.
- [ ] **`llego_agente` en la prueba** salió de las patas salientes de la 19236 (pata grabada = cogió un agente). La
      rutina usa además los registros de cola (`Accepted`/`Missed`), que no se descargaron en la prueba.
- [x] **Hash del número (ronda de arreglos 1):** `from_hash` es un sha256 sin sal de los últimos 9 dígitos, recortado a 10
      caracteres. Con la lista de números posibles se podría deshacer: es un dato seudonimizado que solo vive en
      `datos/` (no se versiona) y nunca sale al artefacto, al informe ni al repo. Si algún día hay que guardarlo fuera,
      usar un HMAC con una sal secreta en el entorno.
- [x] **Margen del emparejamiento con RingCentral:** la rutina empareja a ±10 s (§4 del `CLAUDE.md` raíz).
      `scripts/emparejar_ringcentral.py`, que usan otros casos, sigue a ±15 s y la rutina solo lo usa como
      comprobación (un intento que solo casa entre 10 y 15 s deja `llego_agente` en null).
- [ ] **El bot único no tiene runs** (ni web): las evals y `test_node` no crean runs. La puerta 0 «medición con los runs
      de prueba» queda «sin datos» hasta las llamadas de prueba de la Tarea 17.

## Comprobaciones de la Tarea 15b (20/10/2026)

Arreglos estructurales R39 (Parte A) y R34 (Parte B). Detalle en
`.superpowers/sdd/2026-10-18-bot-unico-construccion/task-15b-report.md` e `informes/evals-v2.md` («Tarea 15b»).

- [x] **R39: el cierre de la oficina del aeropuerto lo resuelve el código (D-012).** Herramienta `estado_oficina` en
      Punto de encuentro; las LISTAS 1 a 4 salen del prompt. En las rondas A1 a A3 (05:42–05:51, martes, reloj en
      modo virtual; las evals no dependen del reloj) el bot no dio el punto con la oficina cerrada ninguna vez (54
      ejecuciones). PE-EST-1 y PE-EST-3 (llama a `estado_oficina` antes de nada) 6/6 cada una; PE-NOCT-3c 9/9;
      críticas de Punto de encuentro 18/18 en la ronda A2. Cierra también R38 y la propuesta de la ronda 22 de la Tarea 11.
- [ ] **PE-NOCT-3 y PE-NOCT-3b (vuelo retrasado con la oficina cerrada), 0/3 tras la única vuelta.** Ya no dan el
      punto, pero no hacen las dos cosas en el orden pedido. Con la frase del vuelo en la `instruccion` de la
      herramienta (ronda A2) ejecutan `consultas_alquiler` recoger_tarde primero y el aviso llega después; sin ella
      (ronda A3, estado actual) dan el aviso y preguntan, sin `consultas_alquiler`. La frase del vuelo se quitó porque
      hacía que PE-NOCT-1 preguntara por retrasos (0/3). Propuesta para la Tarea 16: que `consultas_alquiler` de Punto
      de encuentro diga en su descripción que, con la oficina cerrada, va después del aviso en el mismo turno, o
      aceptar en la eval el aviso dicho por Consultas tras el salto (el cliente lo oye igual).
- [ ] **PE-NOCT-1, 2/3 en la ronda A3:** en una usa tres frases (regla de voz). Dispersión.
- [ ] **VIRT-PE1 (crítica), 2/3 en la ronda A1 y 3/3 en la A2:** en una dio el horario de gestión sin que lo pidiera.
- [x] **Datos de horario que no casan** (hecho en la Tarea 16, D-014: `estado_oficina` usa el horario concreto de cada oficina que dice el prompt; antes: las `nocturno_*` cierran todas las
      oficinas de 23:00 a 07:00 (Murcia de 22:00 a 08:00), pero el prompt dice que Alicante cierra a las once y media
      y que Bari, Florencia, Nápoles y Venecia abren a las ocho. Entre las 07:00 y las 08:00 de esos cuatro, el bot da
      el punto con la oficina aún cerrada; entre las 23:00 y las 23:30 de Alicante, dice que ha cerrado. Es lo mismo
      que hacía la v25. Si se quiere afinar, `estado_oficina.py` puede calcular con la hora local y su propio horario.)
- [x] **La hora es la del principio de la llamada** (hecho en la Tarea 16, D-014: ahora la del momento en que se ejecuta la herramienta, con `HORA_PRUEBA` para las evals; antes, las `nocturno_*`, como en la v25): una llamada que empieza a
      las 22:58 y pide el punto a las 23:02 lo recibe. Si importa, pasar a calcularlo con el reloj (el código ya lo
      hace cuando la variable no llega).
- [x] **R34: aviso «le paso» antes de saber si se transfiere (D-013; regla sustituida por D-014 en la Tarea 16: el aviso depende de la cola, y con `asistencia` es el de siempre; R34-P1/C1 pasan a medir la avería de noche con el aviso de siempre y R34-T1 el aviso de siempre del Triaje).** Hecho en Prolongación y Consultas: con
      Gestión cerrada (y en modo virtual) el aviso es «Un momento, por favor, no cuelgue»; con Gestión abierta, el de
      siempre (R34-P1 3/3, R34-C1 2/3, R34-P2 3/3). **Queda abierto:**
  - Triaje: el aviso neutro hizo que VIRT-T1 transfiriera en modo virtual (1/3, y 0/6 tras la única vuelta); se
    deshizo y el Triaje sigue con «le paso» (R34-T1 0/3, la eval queda como RED). Ideas para la Tarea 16: que la
    condición vaya en la descripción de la herramienta y no en la del `message`, o aceptar la frase incómoda (§5.8).
  - Tarea 17: oír en una llamada qué dice el aviso en los tres casos (transfiere, `gestion_cerrada`, `modo_virtual`) y
    si hay silencio antes de la música. La documentación no explica `handoff_message` del Transfer.
  - HOR-C1: 3/3 en la ronda B1 (la decisión del modelo; el aviso no se mide en esa eval).
  - Pasada de transferencias (rondas B1 y B2, 05:55–06:05, reloj en modo virtual): Prolongación 68/72 (HOR-02 1/3,
    el juez valora el texto tras `gestion_cerrada` que da el reloj; FDS-05 y BORDE-09 2/3, dispersión), Triaje 25/27
    tras el cambio (VIRT-T1 1/3, deshecho) y Consultas 33/36 (DEVOL-03c 0/3, ya abierta desde la Tarea 9).
- [ ] **Evals de Punto de encuentro que dan el punto en el historial sin la llamada a `estado_oficina`** (PDE-1 a 4,
      ADV-8 a 10, las v18, «ES · …» y SALTO-*): no se tocaron. Con el prompt nuevo el bot puede llamar a la herramienta
      en ellas antes de contestar; PDE-2 dio 6/6. Revisarlas en la pasada completa de la Tarea 16.

## Para la persona (editor de HappyRobot)

- [ ] **Mover la rama de WhatsApp y borrar «Registrar consultas del alquiler»** (Tarea 13, R42). Por API no se puede:
      `delete` borra el subárbol y no hay cambio de padre. En el editor de la v2: mover «Preparar WhatsApp minibús» (con
      «¿Enviar WhatsApp?» y lo que cuelga) para que cuelgue de «Registrar resultado de la llamada» y, después, borrar
      «Registrar consultas del alquiler» (`01a14f1d-0396-7b8c-ac8b-76817e8d62e8`), que ya no alimenta nada (sus
      variables siguen rotas y gasta una llamada al modelo por llamada). Comprobar después con `get_workflows` que
      «Preparar WhatsApp minibús» tiene como padre `01a14f1d-0395-7611-80cf-234e9e9fcf11`.

- [x] **Crear los 8 Module Change de la Tarea 12** (hecho por el responsable el 19/10/2026; comprobado por API: 12
      `module-change`, todos al destino de la tabla de `saltos.md`).

- [ ] **Quitar el Paths «Entrada» y su condición «Siempre» de la v2** y dejar «Receive Customer Call» colgando
      directamente de «Resolver colas por idioma» (Paso 5 de la Tarea 6, no hecho por API). Hay que hacerlo en el
      editor **sin borrar el agente** (mover «Receive Customer Call» con todo lo que cuelga y después borrar
      «Entrada»/«Siempre»). La v2 ya no tiene la rama «Fallback» (vacía) de «Entrada». Después, comprobar con
      `get_workflows` que la cadena es Inbound Call → Calcular horario nocturno → Resolver colas → Receive Customer
      Call. Las tareas siguientes pueden construirse sobre la v2 tal como está (el Paths no estorba), pero no hay
      que publicarla con él.
- [ ] **Líneas telefónicas:** la v1 y la v2 no tienen números en el trigger. La tabla línea → opción del menú y los
      números se ponen al pasar a producción (puerta 0 del spec §8.4); ahora mismo no entra ninguna llamada por
      este workflow. Los números van como `<LINEA_PROLONGACION_ES>`, `<LINEA_PROLONGACION_EN>`,
      `<LINEA_MINIBUS_ES>` y `<LINEA_MINIBUS_EN>` en el repo; en `LINEAS` de «Contexto de la llamada» de la v2 ya
      están los reales (Tarea 8). Si cambia alguna línea antes de producción, actualizar `LINEAS`.
- [ ] **Bloquear la v1** (`manage_versions action=lock`) si se quiere proteger la referencia: el fork no la bloquea.
      No se hizo por no estar pedido.

## Antes de conectar la primera línea (puerta 0, spec §8.4)
- [ ] Comprobar que la variable del workflow `HORA_PRUEBA` vale `ninguna` en los tres entornos (si no, `estado_oficina`
      usa esa hora en vez del reloj; D-014).
- [ ] Evals en verde (Tarea 16, 20/10/2026, tras la ronda de arreglos 4: no lo están). Bloqueos, con su motivo, en
      `informes/evals-v2.md` («Ronda de arreglos 4»): VIRT-T1 2/3 (Triaje, modelo); HOR-C1 2/3 (Prolongación,
      modelo); en Consultas, FDS-02 0/3 (modelo y eval: añade cuándo llamar o la web; el enrutado lo mide FDS-02r,
      3/3, porque FDS-02 trae sembrada la llamada a `buscar_respuesta`), TEL-C1 0/3 (negocio, C-005, y modelo),
      DEVOL-03a 1/3, DEVOL-03c 2/3 y CARGO-05 1/3 (modelo); resto de Punto de encuentro al 87,3 % (modelo; Madrid
      ambiguo, prompt o modelo). Prolongación pasa del 90 % en el resto (92,7 %); siguen PISTA-04, PROL-05, PROL-06 y
      CORREO-08 a 0/3, IDIOMA-01 e IDIOMA-05 a 1/3 y CORREO-03 y BORDE-02 a 2/3 (modelo).
- [ ] Caso «coincide» del correo de contraseña probado con una reserva real (pendiente heredado de la v12).
- [ ] `pista_correo` probada con una reserva real (verifica y devuelve solo el dominio).
- [ ] Rutina diaria, artefacto y `scripts/medir_bots.py` funcionando. Hechos y probados con V11 y Minibús ES
      (Tarea 15); falta medir las llamadas de prueba del bot único (Tarea 17) y los créditos (clave de la API).
- [ ] Movimiento de líneas y vuelta atrás ensayados, ida y vuelta, con la línea «Test SIP RingCentral».
- [ ] Cerrar el experimento de Minibús ES v25 antes de la fase 2 (mover las líneas de Minibús).

## Preguntas abiertas de la Tarea 18 (para el responsable)
- [ ] **¿Qué líneas quedan en Minibús ES al quitar las dos movidas en la fase 2?** Reembolsos usa una línea española
      que antes era de Minibús (Tarea 8). Listar el trigger de la v25 y decidir. Control de la fase 2: Minibús ES
      v25 (R46). Ver `procedimiento-lineas.md`, apartado 4.
- [ ] Los puntos «por comprobar» del ensayo (Paso 2): qué variante libera el número, duplicados, ventana sin
      llamadas entre publicaciones, duración de la vuelta atrás. `procedimiento-lineas.md`.

## Para negocio
- [ ] Los 7 «DECIDIR» de `comun/bloques/consultas-alquiler.md`.
- [ ] Si después se conecta la opción de Gestión cuando está cerrada.
- [ ] Confirmar con Centauro que Gestión no atiende los festivos autonómicos (hoy se tratan como laborables).
