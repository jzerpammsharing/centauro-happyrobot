# Pendientes del caso Atención España

## Antes de construir
- [x] Aprobar el spec (`specs/2026-10-18-bot-unico-arquitectura.md`) (18/10/2026).
- [ ] Revisar el plan de construcción (`planes/2026-10-18-bot-unico-construccion.md`) y elegir cómo se ejecuta.

## Al construir (comprobaciones del spec, §11)
- [x] Qué copia el duplicado de la v25: Module Change, evals, agente de voz (18/10/2026; detalle en «Comprobaciones de
      la Tarea 6»). Copia los 4 Module Change, el agente de voz y los 37 nodos; **no** copia evals, líneas del trigger,
      ajustes del workflow ni tabla de Twin.
- [ ] Que un Module Change pueda volver al Triaje.
- [ ] Que el módulo de destino ve el historial.
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
    «Transferir». **Para la Tarea 13:** el extract «Registrar resultado de la llamada» sigue leyendo
    `17c682a0-….extension_destino` (el parámetro ya se llama `cola`) y `b4439401-….transfer_succeeded` (nodo borrado);
    `fix_broken_vars` no lo detecta porque el extract pasa la prueba.
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
- **Para la Tarea 13:** el extract «Registrar consultas del alquiler» lee `fbe2e40e-….extension_destino` (parámetro
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

- **Prolongación** construido: prompt de 21.978/22.000 caracteres (`fast-gpt-5.4`), `enviar_correo_contrasena` (cadena
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
- [ ] **Mejora de la spec §5.7 sin hacer:** que «Enviar correo» no se ejecute si el correo no coincide. Pide un Paths con
      «Resultado para el agente» en las dos ramas, y en HappyRobot un nodo tiene un solo padre (por API no se reengancha).
      Hoy, si no coincide, el nodo se ejecuta con `email` vacío y el MCP lo rechaza (como en la v12). Se puede hacer en
      el editor duplicando «Resultado para el agente» en cada rama.
- [ ] **`pista_correo`: ramas sin confirmar.** El Paso 3 (22:54, datos inventados) solo vio `no_verificado`
      (`encontrada: false`, sin error). No se ha visto el texto real del MCP cuando no interpreta la reserva o el nombre
      (`dato_no_interpretado`) ni el caso `verificado` con `email_hint`: este último solo con una reserva real, en la
      puerta 0. Si el texto de error no casa, sale el detalle genérico (correcto, pero menos útil).
- [ ] **Evals que esperan `volver_al_triaje`** (ESC-04, PRO-1, PRO-2): no se ejecutaron (R5); van en la Tarea 12.
- **`fix_broken_vars` no se ejecutó en la Tarea 10** (R23). Variables escritas con `{{persistent_id.variable}}` y
  comprobadas con `get_workflows` y `get_node_details`.

## Para la persona (editor de HappyRobot)

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
- [ ] Caso «coincide» del correo de contraseña probado con una reserva real (pendiente heredado de la v12).
- [ ] `pista_correo` probada con una reserva real (verifica y devuelve solo el dominio).
- [ ] Rutina diaria, artefacto y `scripts/medir_bots.py` funcionando.
- [ ] Movimiento de líneas y vuelta atrás ensayados, ida y vuelta, con la línea «Test SIP RingCentral».
- [ ] Cerrar el experimento de Minibús ES v25 antes de la fase 2 (mover las líneas de Minibús).

## Para negocio
- [ ] Los 7 «DECIDIR» de `comun/bloques/consultas-alquiler.md`.
- [ ] Si después se conecta la opción de Gestión cuando está cerrada.
- [ ] Confirmar con Centauro que Gestión no atiende los festivos autonómicos (hoy se tratan como laborables).
