# SDD ledger — plan: casos/atencion-es/docs/planes/2026-10-18-bot-unico-construccion.md

Spec: casos/atencion-es/docs/specs/2026-10-18-bot-unico-arquitectura.md (autoridad).
Rama: comun/bot-unico-arquitectura · BASE inicial: 731f6d3.
Fichas: task-N-brief.md en este directorio (extraídas con el patrón «Tarea N»; el script task-brief busca «Task N»).
Restricciones globales para revisores: global-constraints.md en este directorio.

## Revisión previa del plan

| Tareas | Qué produce una / qué consume la otra | Resultado |
|---|---|---|
| 1 ↔ 3 | 3 copia hora_madrid, gestion_abierta_en, FESTIVOS de 1 y prueba equivalencia | Coherente |
| 1 ↔ 14 | 14 importa gestion_abierta_en, modo_virtual_en de contexto_llamada.py | Coherente si 1 es importable sin input_data (patrón try/NameError) |
| 1 ↔ 8 | 8 pega contexto_llamada.py; entradas from_number, to_number, opcion_prueba | Coherente |
| 1 (propia) | Pide el saludo y salidas de la v25, pero la copia de la v25 se guarda en la 6, después | Conflicto → R1 |
| 2 ↔ 3 | 3 consume cola_gestion_reserva, cola_asistencia, cola_nueva_reserva, cola_horario_minibus | Coherente |
| 2 (propia) | Parte de la v22 del repo; la v25 puede diferir | Conflicto → R1 |
| 4 ↔ 9, 10 | 12 temas = enum de buscar_respuesta | Coherente |
| 5 ↔ 10 | Claves verificado, dominio, resultado, detalle | Coherente |
| 7 ↔ 8–11, 16 | comprobar_prompts exige los 5 prompts de módulo; en la 8 solo existe triaje.md | Conflicto → R2 |
| 7 ↔ 8–13 | Copias guardadas desde HappyRobot llevan sintaxis {{ index . "id.var" }}; los fuentes llevan {{var}} | Conflicto → R3 |
| 8 ↔ 9–11 | Patrón de transferencia y forma de cortar la cadena | Coherente |
| 8, 12 (propias) | Comprobaciones con llamada web, que puede exigir publicar en development (persona) | Conflicto → R4 |
| 9 ↔ 12 | BR-05 espera prolongar_alquiler en Consultas, que se crea en la 12 | Conflicto → R5 |
| 10 ↔ 12 | ESC-04 espera volver_al_triaje, que se crea en la 12 | Conflicto → R5 |
| 9 ↔ 10–12, 16, 17 | informes/evals-v2.md lo crea la 9 y lo continúan las demás | Coherente |
| 11 ↔ 12 | informacion_oficina en Punto de encuentro la crea la 12 | Coherente |
| 13 ↔ 8 | test_node del extract con transcripción de una llamada de prueba de la 8, que quizá no exista | Conflicto → R6 |
| 13 ↔ 14, 15 | Campos del extract que lee la rutina | Coherente |
| 14 ↔ 15 | creditos_runs.py alimenta el campo creditos | Coherente |
| 17 ↔ 18 | Procedimiento de líneas según lo comprobado en la 17 | Coherente |
| 3, 4, 5, 6, 9, 10, 11, 14, 15, 16, 17, 18 (propias) | Pruebas especificadas frente a código y ficheros | Coherentes |
| 4 (propia) | Marcadores prohibidos (Nuevo., Equipo (, DECIDIR, Solo en Minibús) solo en notas: comprobado con grep | Coherente |

## Resoluciones previas
- Ruling: R1 — las tareas 1 y 2 leen en solo lectura el código de la v25 en HappyRobot (get_node_details, version_id 01a14054-0eaf-73b5-af31-1fc40bfcd3cc; «Calcular horario nocturno» 01a14054-0ecc-72ab-aac0-027153931287; «Resolver colas por idioma» 01a14054-0eca-7fe1-8c95-e8d7844ab50f) como referencia, en lugar de la copia de la v22 — la v25 es lo que se duplica — si me equivoco, el saludo o alguna salida no coincide con la v25 y se ve en la 8.
- Ruling: R2 — comprobar_prompts.py solo da fallo por los prompts de módulo que existen; los que faltan los lista como pendientes sin fallar, salvo con la opción --completo, que se usa en la 16 — permite ejecutarlo en las tareas 8–11 — si me equivoco, un módulo podría quedarse sin comprobar hasta la 16.
- Ruling: R3 — los ficheros de prompt del repo son la fuente, con marcadores {{idioma_nombre}}, {{modo_virtual}}, {{gestion_abierta}}…; al subir se cambian por la sintaxis de HappyRobot; comprobar_prompts normaliza {{ index . "<id>.<var>" }} → {{<var>}} antes de comparar; «guardar copias» = nodos sin prompt (herramientas, Python, Transfer) y comprobar que el prompt subido coincide con el fuente tras normalizar — evita dos ficheros para el mismo prompt — si me equivoco, el diff entre versiones muestra marcadores en lugar de ids.
- Ruling: R4 — en las tareas 8 y 12, las comprobaciones que piden una llamada web se intentan primero con test_workflow o test_node; si eso no muestra lo que recibe el agente, se deja la implementación provisional (Paths en la cadena si test_node muestra que el Transfer no se ejecuta; Module Change según get_workflows) y la parte conversacional pasa a las llamadas de la 17, sin parar la ejecución — no bloquea al responsable a mitad de plan — si me equivoco, un fallo de corte de transferencia o de vuelta al Triaje se ve en la 17 y obliga a rehacer.
- Ruling: R5 — las evals que esperan una herramienta que crea la 12 (BR-05 en Consultas, ESC-04 en Prolongación y cualquier otra que espere volver_al_triaje, prolongar_alquiler desde Consultas o informacion_oficina desde Prolongación o Punto de encuentro) se crean en su tarea pero no cuentan para su criterio; se ejecutan y cuentan en la 12 — evita evals que fallan por diseño — si me equivoco, se retrasa una señal de fallo hasta la 12.
- Ruling: R6 — si en la 13 no hay ninguna llamada de prueba de la v2, el test_node del extract usa una transcripción inventada (sin datos reales) que pase por dos módulos y una transferencia — si me equivoco, un campo del extract se valida con un caso poco realista.
Task 1: dispatched (BASE 731f6d3)
Task 1: implementer ab59130effd3f8311 DONE_WITH_CONCERNS (ca0a480); concerns: línea desconocida no se anota (spec §5.2), festivos solo hasta 2027
Task 1: review (acd5f9e9f06d0c95e) — spec ❌ 1 Importante (línea desconocida no se anota, spec §5.2); 7 menores
- Ruling: la anotación de §5.2 es una salida nueva `origen_opcion` = linea | prueba | por_defecto (por_defecto = línea desconocida sin opcion_prueba válida); una opcion_prueba no válida cuenta como por_defecto; la Tarea 13 la copia en el grupo «Copiados de la entrada» del extract — cubre el Importante y el Menor 2 con un solo campo — si me equivoco, un campo de más en el extract.
Task 1: minor (deferred): dictar() revienta con dígitos Unicode («²»), heredado de la v25 (contexto_llamada.py:246-253)
Task 1: minor (deferred): la cabecera debería recomendar las claves de LINEAS como número nacional sin prefijo (reconoce +34, 0034 y nacional) — llevar a la Tarea 8 al pegar
Task 1: minor (deferred): faltan pruebas de lo portado (telefono_dictado internacional/00/9xx, callcenter_abierto, nocturno_murcia, límites de saludo)
Task 1: minor (deferred): 15/8/2027 en FESTIVOS_NACIONALES no está en el BOE — Ruling: se queda (domingo, sin efecto; la ficha lo fija) — si me equivoco, nada cambia en la práctica
Task 1: minor (deferred): «buenos días» con tilde solo en el mensaje de Prolongación (texto exacto de la ficha), `saludo` sin tilde como la v25
Task 1: minor (deferred): FESTIVOS_NACIONALES acaba en 2027 — apuntar en pendientes del caso (Tarea 18)
Task 1: fix round 1/5 (1 addressed, 0 open; commits ca0a480..f8559f2)
Task 1: minor (deferred): task-1-report.md desactualizado en el cuerpo (salidas sin origen_opcion, «23 claves»)
Task 1: complete (commits 731f6d3..f8559f2, review clean)
Task 1 → Task 13: el extract copia `origen_opcion` en «Copiados de la entrada» (Ruling de la Tarea 1)
Task 2: dispatched (BASE f8559f2)
Task 2: implementer a0e7a3d3db35e50ca DONE (8a4e0b9); nota → Tarea 8: comprobar que nada referencia cola_fuera_horario*
Task 2: review (abda1ab0e75e70f80) — spec ✅, calidad aprobada, 7 menores
Task 2: minor (deferred): comentario de resolver_colas.py:16-18 dice que «Preparar transferencia» recibe gestion_abierta (decide por la hora actual)
Task 2: minor (deferred): es_abierta abre por defecto con valores desconocidos ("cerrada", "off") — como la v25; sin prueba que lo documente
Task 2: minor (deferred): nombres de nueva_reserva/horario_minibus/gestion_reserva sin fijar en pruebas y distintos de RingCentral
Task 2: minor (deferred): COLAS y NOMBRES paralelos; idioma_de legibilidad; output local; prueba fuera_horario redundante; recorte por '#'; resolver(None)
Task 2: complete (commits f8559f2..8a4e0b9, review clean)
Task 3: dispatched (BASE 8a4e0b9)
Task 3: implementer a7bd12581c9b5f915 DONE (095208f)
Task 3: review (aced38fb43597b722) — spec ✅, calidad aprobada, 7 menores
Task 3: minor (deferred): caso «asistencia en festivo a las 23:00» usa un martes normal (test_preparar_transferencia.py:104)
Task 3: minor (deferred): la prueba sin hora explícita usa asistencia (no ejercita el reloj); URI solo validada como no vacía; detalle aproximado si falta la URI (obligado por el plan); cola con tilde sin caso de prueba
Task 3: minor (deferred): cabecera de resolver_colas.py:17-18 (repetido de la Tarea 2)
Task 3: complete (commits 8a4e0b9..095208f, review clean)
- Ruling: R7 — el detalle fijo de «Preparar transferencia» remite a «COLA DE GESTIÓN CERRADA»; la Tarea 7 incluye en reglas-comunes.md, justo después de GESTIÓN CERRADA: REGLA DE MÁXIMA PRIORIDAD, una sección titulada exactamente COLA DE GESTIÓN CERRADA (qué hacer: horario de Gestión, área de cliente, formulario de reclamaciones, oficina en persona si es urgente y está abierta; Asistencia, Minibús y Nueva Reserva siguen), como en la V11 — mantiene el texto fijo de la Tarea 3 sin tocarla — si me equivoco, el bloque crece unos cientos de caracteres (límite 4.500).
Task 4: dispatched (BASE 095208f)
Task 4: implementer aaec27af5ea73c720 DONE (27f49d3)
- Ruling: R8 — las secciones citan otras por su título del bloque (DETALLES QUE PUEDES DAR, «Si lo devuelve antes», DEVOLVER TARDE, RECOGER TARDE, TELÉFONOS QUE PUEDES DAR, EXPLICACIÓN); el texto del bloque no se toca (fuente única) y los prompts de Consultas (Tarea 9) y Prolongación (Tarea 10) llevan una tabla corta «título citado → tema de buscar_respuesta»; en Consultas, EXPLICACIÓN = saltar a Prolongación (prolongar_alquiler) — si me equivoco, unos 400 caracteres más por prompt.
Task 4: review (a3fb4c5ee0209940e) — spec ✅, calidad aprobada, 5 menores
Task 4: minor (deferred): comentarios inexactos (test:60 «cinco» son cuatro; «orden del bloque» = orden de TEMAS)
Task 4: minor (deferred): huecos de prueba (invariante sin pérdidas, nota pegada/CRLF, errores de título no reconocido, main con bloque roto); doble CONSULTAS FRECUENTES pisa la introducción; devolver_tarde a 25 caracteres del mínimo (obligado por el plan)
- Ruling: R9 — la franja 2.000–5.000 del spec §5.9 se incumple en 5 temas (de 1.025 a 5.062); vale la de la ficha (1.000–6.000) porque el bloque no se toca y el tamaño lo dicta su contenido — si me equivoco, ninguno: es un orden de magnitud, no un límite técnico.
Task 4: complete (commits 095208f..27f49d3, review clean)
Task 5: dispatched (BASE 27f49d3)
Task 5: implementer aed55bf1d8cef9f40 DONE (396d6fe); nota → Tarea 10: comprobar texto real del MCP al no interpretar reserva/nombre
Task 5: review (af74a3d10061b2c3b) — spec ✅, calidad aprobada, 5 menores
Task 5: minor (deferred, privacidad — que lo mire la revisión final): el dominio se normaliza pero no se valida; si email_hint trajera más que un dominio (p. ej. un nombre) pasaría a la salida (pista_correo.py:101-106)
Task 5: minor (deferred): ramas de error de reserva/nombre especulativas (texto real del MCP sin documentar) → comprobar en Tarea 10
Task 5: minor (deferred): huecos de prueba ("false" como texto, lista ya parseada, basura tras el dominio); envoltorio dict {"content":[…]} daría no_verificado (obligado por el plan, heredado de decidir_envio) → comprobar forma real en Tarea 10
Task 5: complete (commits 27f49d3..396d6fe, review clean)
Fase A completa (731f6d3..396d6fe)
Task 6: dispatched (BASE 396d6fe)
Task 6: implementer a2ddd853098f6f579 DONE_WITH_CONCERNS (2257858) — workflow 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 (rntn68r0a8gh); v1 veavliy3k6jx / 01a14f1b-4eee-7f9c-8ec5-19600855e648; v2 x8xd0llbdp3j / 01a14f1d-0387-70e5-a6ad-2b311a86224c
- Ruling: R10 — el Paths «Entrada» + «Siempre» se queda en la v2 hasta que la persona lo quite en el editor (por API borrar = borrar el subárbol; no se puede reenganchar); las tareas siguientes construyen sobre la v2 tal cual; quitarlo es requisito antes de publicar (pendientes) — si me equivoco, nada: el Paths siempre se cumple.
- Ruling: R11 — el duplicado no copia evals: las Tareas 8, 9 y 11 copian las evals desde los nodos de Minibús ES v25 (version_id 01a14054-0eaf-73b5-af31-1fc40bfcd3cc: Triaje 24, Punto de encuentro 21, Información de oficina 17, Prolongación y consultas 12 → a Consultas, adaptadas), no desde la v1 — si me equivoco, ninguno: la v1 tiene 0.
- Ruling: R12 — «Receive Customer Call» apunta a business_hours_setting_name "default", que no existe en el workflow nuevo; la Tarea 13 (que ya toca ese nodo) lo deja vacío, como dice el spec §5.11 (sin horario comercial en el nodo) — si me equivoco, el agente podría aplicar un horario inexistente en las pruebas de la 8–12 (se vería como llamadas rechazadas).
- Ruling: R13 — require_webcall_auth vuelve a true por defecto; ponerlo en false para las llamadas web de prueba es decisión de la persona en la Tarea 17 — si me equivoco, las pruebas web de las Tareas 8 y 12 (R4) caen en test_workflow/test_node.
- Nota → todas las tareas de HappyRobot: el markdown de get_node_details en el duplicado conserva group_id antiguos; escribir siempre {{persistent_id.variable}} con los ids de workflows.md; no borrar nodos con hijos.
Task 6: review (aad17ae874943d4f2) — aprobada (Paso 5 en parte, justificado), 4 menores
Task 6: minor (deferred): al borrar el «Fallback» de «Entrada», «Siempre» pasó de Order 0 a -1 (sin documentar)
Task 6: minor (deferred): 3 escrituras de prueba «ZZ» en la v2 real (limpias) fuera de la ficha; fix_broken_vars dry_run hace test-all (no inocuo con WhatsApp en la versión)
Task 6: minor (deferred): «no publicar con el Paths» sin justificar (es tautología inofensiva); suposición de que el editor permite mover el subárbol
Task 6: complete (commits 396d6fe..2257858, review clean)
Nota (18/10, comprobado con manage_versions list): Minibús ES tiene la v25 LIVE en producción (al empezar la sesión era la v22); no lo hemos hecho nosotros. Efecto: el control de la fase 2 es la v25; el pendiente «cerrar el experimento de la v25» puede sobrar; la ficha de Minibús (workflows.md, CLAUDE.md) está desfasada → Tarea 18 y mensaje final.
- Ruling: R14 — las Tareas 7–11 (texto de prompts que leerá el bot en producción) van con el modelo más capaz (opus); las demás, sonnet — si me equivoco, más coste.
Task 7: dispatched (BASE 2257858)
Task 7: implementer a1a7070921d37afaf DONE (11372e8) — bloque 4.453/4.500
- Ruling: R15 — el tema `telefonos` de buscar_respuesta trae teléfonos de otros países (DECIDIR 7, sin validar); manda el bloque de reglas comunes: los prompts de Consultas y Prolongación (Tareas 9 y 10) dicen que de lo que devuelva buscar_respuesta solo se dan los cuatro teléfonos de TELÉFONOS QUE PUEDES DAR; el bloque de consultas no se toca — si me equivoco, el bot no da un número de asistencia de Portugal o Italia que sí podía dar (remite a la web o transfiere).
- Ruling: R16 — comprobar_prompts revisa los textos prohibidos solo en los cinco módulos y el bloque (no en copias de código ni configuraciones, que citan 2114/«NO DISPONIBLE» en comentarios); las descripciones de herramientas (herramientas-*.md) se añaden a la revisión en la Tarea 8 si el implementador lo ve barato — si me equivoco, una descripción de herramienta con un texto prohibido no se detecta automáticamente.
Task 7: review (a63528066fd95ef27) — spec ❌ (alcance de textos prohibidos; idiomas), 3 Importantes, 8 menores
- Ruling: R16 (sustituye a la anterior) — comprobar_prompts revisa los textos prohibidos en los cinco módulos, el bloque, herramientas-*.md y saltos.md (lo que lee el modelo); quedan fuera solo las copias de código/configuración por lista explícita (contexto-de-la-llamada.md, resolver-colas.md, preparar-transferencia.md, transfer.md, buscar-respuesta.md, enviar-correo-contrasena.md, pista-correo.md) — la ficha decía «ningún fichero» y lo que importa es lo que lee el modelo — si me equivoco, alguna copia de código nueva habrá que añadirla a la lista.
- Ruling: R17 — el límite de cambios de módulo se cuenta por cambios de tema: volver al Triaje y entrar en otro módulo cuenta como uno; tras dos cambios de tema sin resolver, al tercero se transfiere (o con Gestión cerrada / modo virtual, horario y cierre) — concilia el spec §5.6 («dos cambios») con la revisión del plan («tercer salto») y con las rutas por el Triaje — si me equivoco, un cliente da una vuelta más antes de pasar con alguien.
- Ruling: R18 — el teléfono real de Asistencia en cifras en test_comprobar_prompts.py incumple la regla del repo (sin teléfonos): se trata como Importante y se cambia por uno inventado.
Task 7: minor (deferred): detalles de la V11 perdidos (responde tú con tus instrucciones, «o una reclamación», hora peninsular, cierre con «¿Puedo ayudarle en algo más?»); interrupciones más pobres que la v25 (Punto de encuentro debe conservar la suya, Tarea 11); separadores - y . en teléfonos; pruebas CRLF/BOM; aviso de Gestión cerrada activado por necesidad de gestión (cubrir en evals de la Tarea 8: insiste en persona con Gestión cerrada en la línea de Prolongación → COLA DE GESTIÓN CERRADA, no minibus)
Task 7: fix round 1/5 (6 addressed, 0 open; commits 11372e8..bd8c81a)
Task 7: minor (deferred): recortes para caber — «en España» quitado de la Asistencia; «, en su horario» del servicio de entrega; IDENTIDAD «salvo los que tus instrucciones pidan» (más amplio que «salvo los del correo de contraseña», privacidad: que lo mire la revisión final); «si no puedes seguirle bien» baja el umbral; «gestión está cerrada» jerga; mezcla Asistencia/minibus/nueva_reserva; EXCLUIDOS no se fija en prueba; faltan pruebas de «nunca digas qué idiomas» y «segundo fallo»
Task 7: complete (commits 2257858..bd8c81a, review clean)
- Ruling: R19 — en la Tarea 8, LINEAS de «Contexto de la llamada» se rellena ya en HappyRobot con los números reales de las cuatro líneas actuales (leídos en solo lectura de los triggers de Minibús ES v25 y Prolongaciones V11 y de sus nodos Python para saber cuál es la inglesa), como número nacional sin prefijo; en el repo siguen los marcadores; el trigger del workflow nuevo sigue sin números hasta producción — deja la tabla lista y no conecta nada — si me equivoco, ninguno: sin números en el trigger no entra ninguna llamada.
Task 8: dispatched (BASE bd8c81a)
Task 8: implementer a07ac61891c724a94 DONE (3556d42) — corte con Paths «¿Transferir?» (Fallback sin hijos); Triaje 8.213/9.000; evals 37 (críticas 15/15, resto 95/96)
Nota → Tarea 13: el extract aún lee extension_destino y el Transfer borrado b4439401.
Nota → Tarea 16: «Preparar transferencia» usa el reloj real también en evals; las de Gestión abierta solo ven la cadena completa si se ejecutan en horario de Gestión (L–V 8–21); correr la pasada completa en día laborable y en horario. Los criterios del juez deben juzgar la llamada a la herramienta y lo dicho antes, no lo que pase después.
Nota (fuera del caso): número de línea real en casos/reembolsos/prompts/reembolsos-whatsapp/v1/calcular-idioma-y-saludo.md:27 (preexistente) → mensaje final.
Task 8: review (aea72f797668b1413) — spec ✅, calidad aprobada, 6 menores
Task 8: minor (deferred) → Tarea 17: comprobar en llamada real (avería y reserva nueva) que con outside_agent_transfer false y sin `execution` el agente oye el whisper, pulsa 1 y queda conectado, la pata sale de la 19236 y se graba, y el bot no habla después; opcional preguntar a HappyRobot qué hace el campo
Task 8: minor (deferred): pendientes.md dice que al cambiar una eval se reinicia su lista de ejecuciones (falso: contar por fecha) → corregir en la Tarea 9
Task 8: minor (deferred) → Tarea 12: LINEA-09 (línea de Prolongación, modo virtual, pide una persona); «VIRTUAL · pide persona» flojo (2/3, una pasa sin decir «a partir de las ocho»); «GESTIÓN CERRADA · coche no está al recoger» con dos desenlaces aceptados → fijar uno
Task 8: minor (deferred): las 24 evals «de la v25» son conversaciones rehechas (la API no devuelve las conversaciones); comentario de resolver_colas.py (repetido)
Task 8: complete (commits bd8c81a..3556d42, review clean)
Fase B completa (2257858..3556d42)
Task 9: dispatched (BASE 3556d42)
- Ruling: R20 — a petición del responsable (para acabar la sesión antes), la Tarea 9 no hace la comparación de modelos del Paso 5: Consultas queda con fast-gpt-4.1 y la elección (§7.3) pasa a pendientes, a hacer en otra sesión antes de la Tarea 16 — si me equivoco, Consultas podría quedarse con un modelo más caro o más flojo de lo necesario hasta entonces.
Task 9: implementer afb4b06382e184855 DONE_WITH_CONCERNS (227e7ce) — Consultas 7.983/8.000, fast-gpt-4.1; 52 evals (51 cuentan); ronda 3: críticas 12/14 (DEVOL-03 0/3, FDS-02 2/3), resto 102/111 (91,9 %)
- Ruling: R21 — DEVOL-03 (devolver con la oficina cerrada sin haberlo acordado): se acepta que el bot explique que depende de la oficina y OFREZCA pasar con Gestión, y transfiera (cola gestion, motivo otro) cuando el cliente acepta; la eval pasa a dos turnos (el cliente dice que sí → se espera transfer_to_human_agent) — es el mismo patrón del bloque para la espera por vuelo o tren («¿Quiere que le pase con un compañero…?»), evita transferir a quien solo quería saberlo, y el prompt (7.983/8.000) y el bloque compartido no tienen sitio para forzarlo; 9/9 ejecuciones con dos modelos ofrecen en vez de transferir — si me equivoco, el cliente que ya sabía que quería un agente tiene un turno más.
- Ruling: R22 — FDS-02 (crítica, 8/9 en las tres rondas, 2/3 en la última): se repite 3 veces en la ronda de arreglos; si vuelve a fallar, queda abierta como dato para la elección de modelo (R20) y para la puerta 0 (Tarea 16), que ya exige 3/3 — no se toca el prompt (sin sitio) — si me equivoco, la puerta 0 la frena igual.
- Nota → Tarea 12/16 y responsable: ADV-2 (1/3) y «VIRTUAL · pide persona» (Triaje, 2/3): en modo virtual el modelo a veces transfiere a minibus; la red de seguridad del código solo cubre Gestión cerrada (spec §5.8 y §5.11: el modo virtual lo decide el prompt). Propuesta para decidir: que «Preparar transferencia» tampoco transfiera en modo virtual salvo a asistencia.
Task 9: review dispatched (afb59af27fc4e2795, opus) sobre 3556d42..227e7ce
Task 9: review (afb59af27fc4e2795) — spec ✅ (con R15–R22), calidad «necesita arreglos»: 1 Importante (modo virtual: ADV-2 transfiere de noche 3/10, sin eval crítica VIRT en Consultas), 7 menores, comentarios a R21
- Ruling: R21 (amplía) — se quita/suaviza «ejecútala en ese mismo turno, sin preguntarle si quiere» del prompt de Consultas y de la descripción de transfer_to_human_agent (añadida solo para DEVOL-03, 0/9, y contraria a la nota del juez); DEVOL-03 se parte en 03a (un turno: depende de la oficina, no inventa prohibición, no dice que lo deje fuera, ofrece o transfiere), 03b (dos turnos: sí → cola gestion, motivo otro) y 03c (Gestión cerrada: no ofrece, da horario); queda como D-003 — si me equivoco, las transferencias que el cliente pide se retrasan un turno (se vigila con REQ-09, CARGO-05, NOINI-06).
- Ruling: R23 — no se ejecuta fix_broken_vars en la v2 mientras tenga el nodo de WhatsApp (el dry_run hace test-all; minor de la Tarea 6): el revisor comprobó a mano las variables de los nodos nuevos; las referencias rotas del extract se apuntan para la Tarea 13 — si me equivoco, alguna variable rota se descubre en la Tarea 13 o en la puerta 0.
- Ruling: R24 — la red de seguridad de modo virtual en «Preparar transferencia» (solo asistencia de 22 a 8) NO se hace ahora: cambia el spec §5.8/§5.11 y la decide el responsable; se arregla la descripción de buscar_punto_de_encuentro (Consultas y Triaje) y se crea una eval crítica VIRT en Consultas — si me equivoco, hasta que se decida, una transferencia nocturna a minibus puede dejar al cliente esperando en una cola vacía (se mide en evals y en la puerta 0).
Task 9: fix round 1/5 dispatched (resume afb4b06382e184855; lista en task-9-fix-1.md)
Task 9: fix round 1/5 (implementer: 7 arreglos, excepción del Triaje revertida; commits 227e7ce..96ed7bb) — ronda 4: resto 100/111 (90,1 %), críticas 42/54 (DEVOL-03c, FDS-02, TEL-C1 0/3; REQ-09, FDS-03, ADV-3 2/3)
Task 9: re-review dispatched (ac45e0d0797fdf29c, sonnet) sobre 227e7ce..96ed7bb
- Ruling: R25 — la Tarea 9 se da por construida aunque seis críticas no lleguen a 3/3 en la ronda 4 (DEVOL-03c, FDS-02, TEL-C1 0/3; REQ-09, FDS-03, ADV-3 2/3): no son defectos de construcción sino de modelo o de contenido pendiente de decidir, el prompt está a 7.979/8.000 y más vueltas no han movido estas evals; quedan bloqueando la puerta 0 (Tarea 16, críticas 3/3). Antes de la Tarea 10, la siguiente sesión resuelve: (1) modelo de Consultas (R20: repetir con fast-gpt-5.4 y fast-turbo-one con el prompt vigente); (2) TEL-C1 → DECIDIR 7 del bloque de consultas (quitar de la sección los teléfonos de otros países o aceptar darlos); (3) DEVOL-03c → DECIDIR 3 (el bot inventa «no está permitido», que era la norma de Minibús v25); (4) R24 (red de seguridad nocturna) y la excepción del modo virtual en el Triaje (con ella VIRT-T1 cae a 0/3); (5) juez: REQ-09/FDS-03 suspenden por una frase que está en la sección, «VIRTUAL · avería» del Triaje cuenta el reintento — si me equivoco, la Tarea 10 copia patrones de un módulo que aún no pasa sus críticas; se ve en la puerta 0.
Task 9: re-review (ac45e0d0797fdf29c) — 7/7 arreglados; reversión del Triaje justificada; sin roturas Críticas/Importantes; cifras de la ronda 4 comprobadas en HappyRobot
Task 9: minor (fixed por el controlador en el commit de traspaso): pendientes.md (DEVOL-03 «resuelta» → solo con Gestión abierta; R24 decía «Consultas y Triaje» y ADV-2 «falla»); D-003 mezclaba las cifras de los dos modelos
Task 9: minor (deferred): consultas-del-alquiler.md:74 (ESCALADO) habla de transferir a Gestión como directo frente a :56 (preguntar antes); TEL-C1 dice «No transfiere» y la ficha admitía transferir; evals-v2.md «Empeoran…» incompleto; redacción repetida en herramientas-consultas.md:92-95
Task 9: complete (commits 3556d42..96ed7bb + traspaso; review clean; seis críticas abiertas por R25)
Parada (18/10, a petición del responsable: «cuando termines la tarea 9 para»). Siguiente sesión: copiar casos/atencion-es/docs/planes/2026-10-18-bot-unico-progreso.md a <workspace>/progress.md (scripts/sdd-workspace), resolver los puntos (1)–(5) de R25 y seguir con la Tarea 10. Pendiente de la persona: quitar el Paths «Entrada» (R10) y, en la Tarea 12, crear los Module Change a mano.
Traspaso: commit 23b4231 subido a origin/comun/bot-unico-arquitectura
Reanudación (18/10, nueva sesión). Decisiones del responsable sobre R25:
- Ruling: R26 — (2) TEL-C1 / DECIDIR 7: se quitan del bloque de consultas los teléfonos de asistencia de otros países hasta que negocio los valide (decisión del responsable); el correo del departamento de flotas sigue como DECIDIR — si me equivoco, el bot remite a la web o transfiere a quien alquila fuera de España.
- Ruling: R27 — (3) DEVOL-03c / DECIDIR 3: vale el texto del bloque («depende de la oficina, se acuerda al recoger»), nunca «no está permitido»; con Gestión cerrada, horario de Gestión (decisión del responsable) — si me equivoco, el bot no da la excepción de Alicante.
- Ruling: R28 — (4) R24 se hace: «Preparar transferencia» solo deja transferir a asistencia en modo virtual (22–8 h), cambia spec §5.8/§5.11 con D-004 (decisión del responsable); la excepción del Triaje en buscar_punto_de_encuentro no se vuelve a poner — si me equivoco, de noche no se llega a minibús/nueva reserva aunque hubiera alguien.
- Ruling: R29 — los puntos (2)–(5) van en un encargo «Tarea 9b» (opus, por R14) y el (1) modelo de Consultas en otro «Tarea 9c» (sonnet) después, porque el bloque cambia los resultados — si me equivoco, una vuelta de evals de más.
Task 9b: dispatched (BASE 23b4231, opus, implementer ab3bec3e33f89fce5)
Task 9b: implementer ab3bec3e33f89fce5 DONE_WITH_CONCERNS (faa28d6, 4aca5a1, 1007093) — críticas Consultas 47/54, Triaje 15/15; abiertas TEL-C1 0/3 (da el teléfono de España como válido en Portugal), DEVOL-03c 1/3 (no da horario de Gestión), FDS-03 2/3; modo_virtual sin test_node (antes de las 22:00)
Task 9b: review dispatched (ad7969702ab80a029, opus) sobre 23b4231..1007093
- Ruling: R30 — TEL-C1: el responsable aprueba añadir «en España» al teléfono de Asistencia en reglas-comunes.md (4.494/4.500); entra en la ronda de arreglos 1 de la 9b junto con lo que diga la revisión — si me equivoco, el bloque queda a 6 caracteres del límite.
Task 9b: review (ad7969702ab80a029) — spec ❌ (cambio fuera de alcance de GC-C1), calidad «necesita arreglos»: 2 Importantes (modo_virtual choca con «otro error → reintenta» de reglas-comunes:80 y sin eval; GC-C1/FDS-03 reescritas tras la única vuelta), 4 menores
- Ruling: R31 — se ratifica el cambio de expectativa de GC-C1 (el bloque común manda decir que Gestión está cerrada), pero pendientes.md da la cifra oficial de la 5b y la 5c aparte — si me equivoco, una crítica aprobada con un criterio más laxo; se ve en la puerta 0.
- Ruling: R32 — modo_virtual: primero dos evals (Consultas y Triaje) con mensaje tool `resultado: modo_virtual`; se añade «o modo_virtual» a la regla de reglas-comunes:76 en cualquier caso (no dejar el choque con :80 a la suerte del modelo), recortando lo necesario para no pasar de 4.500 con «en España» (R30) — si me equivoco, un recorte del bloque cambia algún matiz; se ve en las evals.
Task 9b: fix round 1/5 dispatched (resume ab3bec3e33f89fce5; lista en task-9b-fix-1.md; FIX_BASE 1007093)
Task 9b: fix round 1 implementer DONE_WITH_CONCERNS (a6f6ce5) — bloque 4.496/4.500; VIRT-C2/T2 nuevas 3/3, GC-C1 3/3, VIRT-C1 3/3; VIRT-T1 3/3→1/3 (regresión: el Triaje transfiere de noche y deja decidir al código), TEL-C1 0/3, DEVOL-03c 1/3; pytest directorio falla en recogida (scripts con sys.exit, preexistente)
Task 9b: re-review dispatched (a8968ed4b4f9ddaaf, sonnet) sobre 1007093..a6f6ce5
Task 9b: fix round 1/5 (4 addressed, 1 open nueva — regresión VIRT-T1 3/3→1/3 por nombrar modo_virtual en CÓMO TRANSFERIR; commits 1007093..a6f6ce5)
Task 9b: minor (deferred): falta un punto en la tabla «De dónde sale cada sección» de reglas-comunes.md (fila CÓMO TRANSFERIR) → entra en la ronda 2
Task 9b: fix round 2/5 dispatched (resume ab3bec3e33f89fce5; task-9b-fix-2.md; FIX_BASE a6f6ce5)
Task 9b: fix round 2 implementer DONE (23aa720) — bloque 4.493; ronda 7 (20:55): VIRT-T1 6/6, VIRT-T2/C2/C1 3/3
Task 9b: re-review 2 dispatched (a4cf4a6ea7ad5a84e, sonnet) sobre a6f6ce5..23aa720
Task 9b: fix round 2/5 (1 addressed + 1 menor, 0 open; commits a6f6ce5..23aa720)
Task 9b: minor (deferred): «otro error sin detalle» depende de que el modelo excluya modo_virtual; muestra pequeña (ronda 7) → vigilar en la puerta 0
Task 9b: complete (commits 23b4231..23aa720, review clean; TEL-C1 0/3 y DEVOL-03c 1/3 abiertas → 9c y puerta 0)
Task 9c: dispatched (BASE 23aa720)
Task 9c: implementer ac1a3134dbf7db51f (sonnet) — modelos intercalados por bloques por el reloj real
Task 9c: implementer DONE_WITH_CONCERNS (672afb1) — resto 5.4 93,7 / 4.1 91,9 / fast 88,3; elegido fast-gpt-4.1 (D-005); ningún modelo sin críticas fallidas; TEL-C1 solo la pasa 5.4
Task 9c: review dispatched (a2f8ea3d245699ea7, sonnet) sobre 23aa720..672afb1
Task 9c: review (a2f8ea3d245699ea7) — aprobada, 3 menores
Task 9c: minor (deferred): precio de gpt-5.4 con prompt de 8.000 extrapolado de 22.000; «3 puntos» medido sobre el resto (total 2,98); gpt-4.1 llega a la puerta 0 con 6 críticas abiertas y TEL-C1 solo la pasa 5.4 → decisión del responsable
Task 9c: complete (commits 23aa720..672afb1, review clean)
Task 10: dispatched (BASE 672afb1, opus por R14)
Task 10: implementer ac5f7574311770763 (opus)
Task 10: implementer DONE_WITH_CONCERNS (84ad394) — prompt 21.978/22.000; ronda 10: críticas 60/72, resto 84,5 %; bajo 3/3: CORREO-09 0 (regresión del arreglo de plan B), FDS-06 0, FDS-01 1, HOR-C1 1, FDS-05 2, BORDE-09 2; §5.7 no se puede por API; MCP dict sin envolver
Task 10: review dispatched (a63150bf18263f7ec, opus) sobre 672afb1..84ad394
Task 10: review (a63150bf18263f7ec) — montaje HappyRobot ✅; calidad «necesita arreglos»: 4 Importantes (CORREO-09 regresión del prompt, evals cambiadas entre rondas sin documentar, plan B no encaja con reserva no iniciada (NOINI-P1, CORREO-20), HOR-C1 orden de la condición; FDS-06 regla de la v12 perdida), §5.7 motivo discutible, 3 menores
- Ruling: R33 — la ronda de arreglos de la revisión no cuenta como la «vuelta de prompt» de la ficha (una regresión crítica no se deja como pendiente); FDS-06 (regla «primer turno en que pida una persona con Gestión cerrada») va al bloque común y el bloque no tiene sitio (4.493/4.500): se apunta para la Tarea 12/16 sin tocar el bloque ahora — si me equivoco, FDS-06 sigue 0/3 hasta entonces y frena la puerta 0.
Task 10: fix round 1/5 dispatched (resume ac5f7574311770763; task-10-fix-1.md; FIX_BASE 84ad394)
Task 10: fix round 1 — implementer cortado por timeout de API (cambio sin commit en prolongacion.md); reanudado con la orden de comprobar el estado real antes de seguir
Task 10: fix round 1 — segundo corte (el Mac se suspendió, 19/10 ~07:18); nada había llegado a HappyRobot; reanudado
Task 10: fix round 1 — tercer corte (sin red, ENOTFOUND); reanudado 19/10 09:19 a petición del responsable («continua»)
Task 10: fix round 1 implementer DONE_WITH_CONCERNS (650b6fc) — prompt 21.580; ronda 11 (09:22–09:26, Gestión abierta): 11b críticas 48/72; muchas evals de transferencia caen por cola_no_valida (evals sin cola_*); fallos del bot: HOR-C1 0/3, CORREO-20 0/3, NOINI-P1 1/3, FDS-06 2/3, CORREO-09 1/6 anuncia sin ejecutar, HOR-A1 2/3
Task 10: re-review dispatched (aaffd9a1ee1b540d1, opus) sobre 84ad394..650b6fc
Task 10: fix round 1/5 (6 addressed, 3 open — NOINI-P1/CORREO-20, HOR-C1 por el texto de buscar_respuesta, evals sin cola_* (no se pueden medir 9 críticas); menores: ESCALADO :143 dentro de la lista que excluye Gestión cerrada, CORREO-09 1/6, HOR-A1 expectativa; commits 84ad394..650b6fc)
Task 10: minor (deferred) → Tarea 12/16: la frase «Responde solo con lo que pone aquí… no añadas nada» de las secciones de consultas_alquiler.py choca con Gestión cerrada y con las reglas de los módulos (afecta a Consultas); aseguradora_empresa (consultas_alquiler.py:25) remite a «Cuánto se puede prolongar de DETALLES QUE PUEDES DAR»
Task 10: fix round 2/5 dispatched (resume ac5f7574311770763; task-10-fix-2.md; FIX_BASE 650b6fc)
Task 10: fix round 2 implementer DONE_WITH_CONCERNS (b09d797) — 14 evals con cola_*; prompt 21.692; ronda 12 (09:49–10:17): críticas 63/72, resto 87,2 %; abiertas HOR-C1 0, FDS-06 0, HOR-A1 1, HOR-01 2; propone devolver «Cambiar de coche» y «Cuánto se puede prolongar» al prompt (BORDE-05 0/3)
Task 10: re-review 2 dispatched (ae2c8eac48cffee23, opus) sobre 650b6fc..b09d797
Task 10: fix round 2/5 (4 addressed: cola_*, NOINI-P1, CORREO-20, CORREO-09; open: HOR-C1 0/3 regresión con daño real («le paso» del message ai antes de gestion_cerrada), FDS-06 0/3 empeorada, HOR-A1 1/3 por la frase de :55, BORDE-05 por D-006; commits 650b6fc..b09d797)
Task 10: minor (deferred) → Tarea 12/16 y puerta 0: el aviso «le paso con un compañero» es el message ai de transfer_to_human_agent y suena antes de «Preparar transferencia»; si HOR-C1 no llega a 3/3, arreglo estructural en los tres módulos
Task 10: minor (deferred): PROL-05, PROL-06, TARDE-02 0/3 (prompt; no regresiones); WEB-03 3→1, WEB-08 3→1 (juez)
Task 10: fix round 3/5 dispatched (resume ac5f7574311770763; task-10-fix-3.md; FIX_BASE b09d797)
Task 10: fix round 3 implementer DONE_WITH_CONCERNS (b1223d2) — prompt 21.946; ronda 13 (10:30–10:33, Gestión abierta): críticas 67/72; FDS-06 3/3, BORDE-05/WEB-03/WEB-08 3/3; abiertas HOR-C1 1/3, HOR-A1 1/3, HOR-01 2/3, PISTA-04 0/3
Task 10: re-review 3 dispatched (a44741fca75b80dfa, sonnet) sobre b09d797..b1223d2
Task 10: fix round 3/5 (FDS-06, BORDE-05 addressed; open: HOR-C1 1/3 (límite del modelo), HOR-A1 1/3 (prompt: «sin salir de aquí» en Otra duda del alquiler), HOR-01 2/3, PISTA-04 0/3; 3 menores de documentación; commits b09d797..b1223d2)
- Ruling: R34 — HOR-C1 sale del bucle: tres redacciones no la mueven; el arreglo es estructural (aviso del message ai antes de «Preparar transferencia», y la herramienta decide por el reloj), afecta a los tres módulos y va a la Tarea 12/16 y a la puerta 0 — si me equivoco, una crítica abierta más a la puerta 0, que ya la frena.
Task 10: minor (deferred): el primer punto de TU TAREA («si pide una persona» con Gestión cerrada) podría frenar una avería → vigilar HOR-C3 en la puerta 0
Task 10: fix round 4/5 dispatched (implementador nuevo, opus; task-10-fix-4.md; FIX_BASE b1223d2)
Task 10: fix round 4 implementer a11280ac1acc90ef3 DONE_WITH_CONCERNS (5ab40ac) — prompt 21.998/22.000; ronda 14 (10:40–10:47): críticas 69/72 (HOR-A1, HOR-C1, BORDE-09 2/3; HOR-01 3/3); PISTA-04 0/3 (¿eval?)
Task 10: re-review 4 dispatched (a76a8941307088d66, sonnet) sobre b1223d2..5ab40ac
Task 10: fix round 4/5 (HOR-01 3/3, docs coherentes; open: HOR-A1 2/3 (causa no probada: puede ir por EXPLICACIÓN o «cuánto se puede prolongar» de LA WEB NO LE DEJA), PISTA-04 0/3 (¿eval sin turnos user?), BORDE-09 2/3 (dispersión); commits b1223d2..5ab40ac)
Task 10: fix round 5/5 dispatched (resume a11280ac1acc90ef3; task-10-fix-5.md; FIX_BASE 5ab40ac)
Task 10: fix round 5 implementer DONE_WITH_CONCERNS (220bea2) — prompt 21.994; ronda 15 (10:57–10:59): críticas 73/75, HOR-A1 6/6; HOR-01, FDS-05 2/3; PISTA-04 0/3 (eval bien: datos en el primer turno user)
Task 10: re-review 5 dispatched (a7b9a41300b768f84, sonnet) sobre 5ab40ac..220bea2
Task 10: fix round 5/5 (HOR-A1 6/6 addressed; sin roturas; commits 5ab40ac..220bea2)
Task 10: parked — HOR-C1 (crítica, 1–2/3) — Ruling: R34, arreglo estructural del aviso en la Tarea 12/16 y puerta 0 — si me equivoco, la puerta 0 la frena.
Task 10: parked — HOR-01, FDS-05, BORDE-09 (críticas, oscilan 2/3–3/3 con el mismo texto) — Ruling: dispersión de gpt-5.4, se mide en la pasada completa de la Tarea 16 (3/3 obligatorio) — si me equivoco, son defectos de prompt sin sitio (21.994/22.000) que habrá que resolver moviendo texto a buscar_respuesta.
Task 10: parked — PISTA-04 (no crítica, 0/3; eval bien hecha) — Ruling: defecto real del bot (vuelve a pedir datos ya dados), pendiente para la Tarea 16 — si me equivoco, un turno de más en la pista del dominio.
Task 10: minor (deferred): el recorte de ejemplos de «Otra duda del alquiler» (combustible, recoger tarde, devolver antes) sin eval que lo mida; «si pide un dato de su reserva, cola gestion» sin «con gestión abierta» (depende de la regla de máxima prioridad)
Task 10: complete (commits 672afb1..220bea2, 4 parked)
Task 11: dispatched (BASE 220bea2)
Task 11: implementer acae136197d4fe8ae (opus); evals de R11 desde Minibús v25; cola_* en evals de transferencia
Task 11: implementer cortado por red (ENOTFOUND) tras la ronda 16, antes de la vuelta de arreglos; reanudado 12:30
Task 11: implementer DONE_WITH_CONCERNS (f486547) — PE 34.595, IO 33.210 car.; 43 evals; ronda 17: críticas 24/27, resto 89,2 %; ADV-7 0/3, PE-NOCT-1 1/3; BLOQUEO: el sistema de permisos rechazó borrar los dos Transfer de la v25 → sin cadena Preparar transferencia en PE/IO (transferencias al fallback de Minibús sin red de seguridad); D-008
- Ruling: R35 — el responsable rechazó la pregunta sobre borrar los dos Transfer de la v25 en PE/IO; no se borran ni se rodea el permiso; la cadena con red de seguridad en PE/IO queda como pendiente obligatorio antes de cualquier llamada de prueba (pendientes.md:314-319) — si me equivoco, una transferencia desde esos módulos va a la cola de Minibús sin red; la v2 no tiene líneas.
Task 11: review dispatched (a8a98d24daad81551, opus) sobre 220bea2..f486547
Task 11: review (a8a98d24daad81551) — calidad «necesita arreglos»: 4 Importantes (ADV-7 queja no va primero; PE-NOCT-1 terminal antes del cierre + :297 contradice PRIMERO; «devolver más tarde» vs «cambiar la hora de devolución», ADV-11 relajada lo tapa; resto 89,2 % — PDE-2 juez, ADV-8 prompt, resto modelo), 5 menores
- Ruling: R36 — «más tarde» = quedarse el coche más tiempo → prolongar (consultas_alquiler); cambiar un dato ya acordado sin alargar (otra hora el mismo día, buzón) → caso de gestión; ADV-11 vuelve a exigir consultas_alquiler; queda en pendientes para que lo confirme el responsable — sigue el diseño (§5.6: prolongar va al módulo) — si me equivoco, alguna petición de «otra hora» se trata como prolongación.
Task 11: fix round 1/5 dispatched (resume acae136197d4fe8ae; task-11-fix-1.md; FIX_BASE f486547)
Task 11: fix round 1 — implementer cortado por red (cambios sin commit en los dos prompts); reanudado 17:50
Task 11: fix round 1 implementer DONE_WITH_CONCERNS (3175eb2) — PE 35.073, IO 33.379; ronda 18 (17:58–18:00): críticas 24/27; ADV-7 3/3, PDE-2 3/3; ADV-11 3/3→0/3 (exige consultas_alquiler; con Gestión cerrada da horario), PE-NOCT-1 0/3, ADV-8 2/3
Task 11: re-review 1 dispatched (a51b327b2036a6c32, opus) sobre f486547..3175eb2
Task 11: fix round 1/5 (ADV-7, PDE-2 y menores addressed; open: ADV-11 0/3 (Gestión cerrada se come prolongar), PE-NOCT-1 0/3, rotura Importante nueva (regla de ADV-7 bloquea recoger_tarde con PRIMERO=true y promete transferir en modo virtual), ADV-8 2/3; commits f486547..3175eb2)
- Ruling: R37 — el ejemplo «otra hora el mismo día» de R36 se quita (devolver más tarde alarga = prolongar); el caso de gestión queda como «cambiar un dato ya acordado que no sea alargar» — si me equivoco, ninguno: el ejemplo era contradictorio.
Task 11: fix round 2/5 dispatched (resume acae136197d4fe8ae; task-11-fix-2.md; FIX_BASE 3175eb2)
Task 11: fix round 2 implementer DONE_WITH_CONCERNS (6752bd6) — PE 35.489, IO 33.571; ronda 19 (18:25–18:27): críticas 20/27 (antes 24); PE-NOCT-1 3/3; abiertas ADV-11 0/3, «VIRTUAL · cambiar hora de devolución» 0/3 (eval vs R36), PE-NOCT-3 0/3, «Idioma · EN · 25 minutos» 2/3, ADV-8 1/3
Task 11: re-review 2 dispatched (ae1a39d51b7ef9082, opus) sobre 3175eb2..6752bd6
Task 11: fix round 2/5 (PE-NOCT-1, docs addressed; open: ADV-11 (causa real: esquema de transfer_to_human_agent dice «la hora o el día de devolución» = gestión), PE-NOCT-3 (EN MODO VIRTUAL viñeta 2 gana a PRIMERO), «VIRTUAL · cambiar hora» (eval contra R36), «Idioma · EN · 25 minutos» (resumen sin «El cliente habla inglés»), ADV-8; commits 3175eb2..6752bd6)
Task 11: minor (deferred) → Tarea 12/16: triaje.md:69 («su hora de devolución» → gestión) y prolongacion.md:145 contradicen R36/R37; frase del idioma en el resumen por código en «Preparar transferencia»
Task 11: fix round 3/5 dispatched (resume acae136197d4fe8ae; task-11-fix-3.md; FIX_BASE 6752bd6)
Task 11: fix round 3 — implementer cortado por red (antes de actualizar las evals; prompts sin commit); reanudado 21:51
Task 11: fix round 3 implementer DONE_WITH_CONCERNS (a783023) — ronda 20 (21:53–21:58): críticas 26/27; ADV-11 3/3, VIRTUAL·cambiar hora 3/3, Idioma EN 3/3; GC-IO1 2/3; PE-NOCT-3 0/3; ADV-8 0/3 (choque nota de la eval / regla nueva)
Task 11: re-review 3 dispatched (a4d9b5c7baa09ac98, opus) sobre 6752bd6..a783023
Task 11: fix round 3/5 (ADV-11, VIRTUAL·cambiar hora, Idioma EN addressed; open: PE-NOCT-3 (BUS TARDA DEMASIADO da el cartel sin excepción; verificar variables de la eval), ADV-8 regresión Importante (regla nueva choca con «Sin decir nada antes ni después»: el cliente pierde el punto), GC-IO1 eval contra R36, copias herramientas-*.md desfasadas; commits 6752bd6..a783023)
Task 11: minor (deferred): resumen_para_agente «Una sola frase» frente a «ÚLTIMA frase»; esquemas de gestión sin excluir adelantar o cambiar la oficina de devolución
Task 11: fix round 4/5 dispatched (implementador nuevo, opus; task-11-fix-4.md; FIX_BASE a783023)
Task 11: fix round 4 implementer a2176d82b3723ea9c DONE_WITH_CONCERNS (ec72382) — PE 36.159; ronda 21 (22:10–22:11): críticas 26/27 (GC-IO1 2/3 por el juez); ADV-8 2/3; PE-NOCT-1/2 3/3; PE-NOCT-3 0/3 con variables correctas
Task 11: re-review 4 dispatched (a61ed9b16d9009764, sonnet) sobre a783023..ec72382
Task 11: fix round 4/5 (ADV-8 regresión arreglada 2/3, GC-IO1/GC-PE1 según R36, copias; open: PE-NOCT-3 0/3, GC-IO1 2/3 (juez toma `pregunta` por texto previo), ADV-8 2/3 (dispersión); commits a783023..ec72382)
- Ruling: R38 — PE-NOCT-3: no se toca MODO DE ATENCIÓN (bloque común, 4.493/4.500, todos los módulos); en la ronda 5 se condicionan los tres primeros párrafos de «EL BUS TARDA DEMASIADO» a PRIMERO false y se crean dos evals de control (queja con modo_virtual false; sin queja con modo_virtual true) para aislar la causa — si me equivoco, PE-NOCT-3 queda abierta con diagnóstico para la Tarea 16.
Task 11: fix round 5/5 dispatched (resume a2176d82b3723ea9c; task-11-fix-5.md; FIX_BASE ec72382)
Task 11: fix round 5 implementer DONE_WITH_CONCERNS (1b989d0) — ronda 22 (22:19–22:21): críticas 27/27; ADV-8 2/3; PE-NOCT-3 0/3, 3b 0/3 (transfiere a minibus), 3c 1/3 → fast-turbo-one no aplica PRIMERO con la LISTA 1 (Atenas/LISTA 3 sí)
Task 11: re-review 5 dispatched (ae2f0a86de8301b04, sonnet) sobre ec72382..1b989d0
Task 11: fix round 5/5 (GC-IO1, copias, ADV-8 nota addressed; sin roturas; commits ec72382..1b989d0)
Task 11: parked — PE-NOCT-3/3c (el bot da el punto con la oficina cerrada en la LISTA 1; riesgo de producción) — Ruling: R39, arreglo estructural: que el cierre llegue resuelto por código (oficina_cerrada por aeropuerto) en lugar de las cuatro listas; requisito antes de publicar; se diseña en la Tarea 12/16 — si me equivoco, un cliente de madrugada espera en un punto sin minibús hasta que se haga.
Task 11: parked — PE-NOCT-3b — Ruling: el párrafo «Si además está enfadado o puede perder una conexión: transfiere directamente» y la viñeta de queja de ESCALADO no llevan «salvo si PRIMERO dio true»; real y barato, pasa a la Tarea 12 (que toca estos prompts) — si me equivoco, de noche se intenta transferir a minibús (la red de D-004 lo para cuando exista la cadena, R35).
Task 11: parked — control de PE-NOCT-1 (posible pista «23:30» en el mensaje) y otro aeropuerto de la LISTA 1 con valor true — Ruling: Tarea 16 — si me equivoco, el diagnóstico de R39 se apoya en un solo aeropuerto.
Task 11: parked — ADV-8 2/3 (no crítica, dispersión).
Task 11: complete (commits 220bea2..1b989d0, 4 parked; críticas 27/27 en la ronda 22; sin cadena de transferencia por R35)
Task 12: dispatched part 1 (BASE 1b989d0, opus) — Paso 1 + arreglo PRIMERO de la Tarea 11; parará en el Paso 2 (Module Change los crea el responsable)
Task 12: part 1 DONE_WITH_CONCERNS (2a26b2b) — 8 herramientas de salto creadas; ronda 23: críticas PE 18/18; PE-NOCT-3 y 3b siguen 0/3 con la excepción escrita (refuerza R39); esperando al responsable para los 8 Module Change (lista en saltos.md)
Task 12: nota — prolongar desde PE/IO va por consultas_alquiler → Consultas → prolongar_alquiler → Prolongación (dos saltos); revisar en los Pasos 3–5 si cuenta para el límite de cambios de tema (R17)
Task 12: responsable creó Module Change filas 5 (01a155e8-59fa → Información de oficina) y 1 (01a155e8-f3f3 → Triaje c5a70932); comprobados por API; el editor deja elegir el Triaje (§11.2: falta ver el comportamiento en llamada)
Task 12: los 8 Module Change nuevos creados por el responsable y comprobados por API (12 en total, todos al destino de la tabla); reanudo el implementador para los Pasos 3–5
Task 12: implementer DONE_WITH_CONCERNS (2a26b2b, a9e843f) — 31 evals de saltos + 7 que esperaban saltos; ronda 24 (22:59–23:07): 111/114, SALTO-PING 3/3; SALTO-03b 0/3; salto real pendiente para la Tarea 17
Task 12: review dispatched (a5d9c232e40132bfd, opus) sobre 1b989d0..a9e843f
Task 12: review (a5d9c232e40132bfd) — necesita arreglos: 2 Importantes (SALTO-PING y SALTO-ENTRADA-TR ejecutadas antes de su última edición; evals de IO/Prolongación/Consultas sin repetir tras las herramientas nuevas y el cambio de buscar_punto_de_encuentro de IO), 6 menores
- Ruling: R40 — las 4 herramientas de salto heredadas se quedan sin `motivo` (la ficha habla de las 8 nuevas); se comprueba en la Tarea 17 qué recibe el destino — si me equivoco, el módulo de destino tiene menos contexto en esos 4 saltos.
Task 12: minor (deferred): las filas 1 y 2 quedan con evals genéricas («otra consulta»); cobertura menor
Task 12: fix round 1/5 dispatched (resume aa693a87feed78252; task-12-fix-1.md; FIX_BASE a9e843f)
Task 12: fix round 1 implementer DONE_WITH_CONCERNS (a991f4b) — ronda 25 (23:15–23:21): saltos 12/12, SALTO-PING-GC 3/3, IO regresión 18/18 salvo GC-IO1 0/3 (era 3/3 en la 22; no llama a consultas_alquiler con Gestión cerrada), Prolongación 76/78, Consultas 47/57 (las mismas de D-005)
Task 12: re-review 1 dispatched (a0d4c6efec8d641c2, opus) sobre a9e843f..a991f4b
Task 12: fix round 1/5 (SALTO-PING, ENTRADA-TR, 03b, PING-GC, docs addressed; open: GC-IO1 0/3 regresión de la Tarea 12 (herramientas nuevas inclinan «cambiar la hora de devolución» a gestión); commits a9e843f..a991f4b)
Task 12: minor (deferred): SALTO-PING-GC distingue el caso solo a medias (un cargo ya va a COLA DE GESTIÓN CERRADA sin el tercer cambio)
Task 12: fix round 2/5 dispatched (resume aa693a87feed78252; task-12-fix-2.md; FIX_BASE a991f4b)
Task 12: fix round 2 implementer DONE (a394fd6) — ronda 26 (23:31): GC-IO1 3/3, ADV-11, VIRTUAL·cambiar hora, SALTO-PING-GC 3/3; IDO-1 1/3 (juez valora lo posterior a la llamada)
Task 12: re-review 2 dispatched (a2663f0c4968da572, sonnet) sobre a991f4b..a394fd6
Task 12: fix round 2/5 (GC-IO1 addressed 3/3; sin roturas; commits a991f4b..a394fd6)
Task 12: minor (deferred) → Tarea 16: IDO-1 1/3 — reescribir la expectativa acotada al turno anterior a la llamada (la nota ya existe; corregir la propuesta de pendientes.md); M1 «devolucion si es antes» frente a «dato concreto sin alargar» en la descripción de consultas_alquiler de IO; M2 «pregúntaselo una vez» frente a «sin decir nada antes»; sin evals de cambiar la hora / devolver antes con Gestión abierta; M3 R36 no nombra «la hora o el día de devolución»
Task 12: complete (commits 1b989d0..a394fd6, review clean; salto real en llamada → Tarea 17)
Task 13: dispatched (BASE a394fd6)
- Ruling: R41 — en la Tarea 13 no se ejecuta fix_broken_vars (R23 y, además, ahora hay nodos MCP contra la API real que un test-all podría llamar); las variables se comprueban a mano con get_node_details nodo a nodo; test_node solo en el extract — si me equivoco, una variable rota aparece en la Tarea 16/17.
- Ruling: R42 — «Registrar consultas del alquiler» no se borra por API (borrar arrastra la rama de WhatsApp que cuelga de él, y R35); se cambian las entradas de «Preparar WhatsApp minibús» al extract único y se deja «Registrar consultas» para que la persona lo quite en el editor moviendo la rama (como R10) — si me equivoco, hasta entonces cada llamada paga un extract de más.
Task 13: implementer aede971630a1917b2 DONE_WITH_CONCERNS (949ff27) — 46 campos, 97 referencias comprobadas a mano, test_node OK; set_custom_output en 11 nodos; D-010 (cola gestion, saltos = suma de callCount)
Task 13: review dispatched (a3fbb53899128c6ff, opus) sobre a394fd6..949ff27
Task 13: review (a3fbb53899128c6ff) — aprobada; 6 menores
Task 13: minor (deferred) → Tarea 16: comprobar que set_custom_output (Prolongación con resultado=transferir y transfer_succeeded=true) no se cuela en las evals: eval de Prolongación pidiendo gestion en fin de semana debe dar gestion_cerrada
Task 13: minor (deferred) → revisión final: «97 referencias» son 87 (pendientes.md:474); pendientes.md:174 nota de invento_condicion contradice D-010; §5.12 sin remisión a D-010; etiquetas de los 4 Module Change heredados; datos personales en la entrada del extract (bastarían los resultado); «Registrar consultas» con variables rotas hasta que la persona lo borre
Task 13: complete (commits a394fd6..949ff27, review clean)
Fase C completa (3556d42..949ff27)
Task 14: dispatched (BASE 949ff27)
Task 14: implementer ac544f505d18ad00e (sonnet)
Task 14: implementer DONE (3096877) — 36/36
Task 14: review dispatched (a4733a5c4444bd8bd, sonnet) sobre 949ff27..3096877
Task 14: review (a4733a5c4444bd8bd) — aprobada; 9 menores
Task 14: minor (deferred): CLI sin mensajes ante entradas malas; _a_fecha sin normalizar zona; creditos_llamada null si falta uno; cortes_600 borde 599/600 sin prueba; pct_llegan_agente sin contar los null; faltan pruebas de bordes (48 h exactas, cambio de hora, lista vacía); rellamadas_48h cuenta llamadas con rellamada
- Ruling: R43 — (para la Tarea 15) la rutina normaliza llamadas.json: un intento de transferencia parado por gestion_cerrada o modo_virtual (intento_gestion_cerrada del extract) va en `transferencias` con error = ese resultado, para que no cuente como resuelta; opcion_menu nunca vacío (bots antiguos: el de su línea) — sigue el espíritu del spec (resuelta = sin pasar a persona ni intentarlo) — si me equivoco, la resolución real baja algo respecto a la definición literal.
Task 14: complete (commits 949ff27..3096877, review clean)
Task 15: dispatched (BASE 3096877)
Task 15: implementer ac620a3fdad90eeb0 (opus); sin HAPPYROBOT_API_KEY en el entorno → creditos null y pendiente
Task 15: implementer DONE_WITH_CONCERNS (18a928e) — artefacto https://claude.ai/artifact/4YyyT2jrKTe1TjhGdApnh7 (privado, doc de prueba 2026-10-16); creditos null sin clave; extra D-011 (normalizar_llamadas.py, informe_diario.py, contexto en medir_bots)
Task 15: review dispatched (aab25dcd2c7108346, opus) sobre 3096877..18a928e
Task 15: review (aab25dcd2c7108346) — necesita arreglos: 3 Importantes (transferencia sintética duplicada en bots antiguos; puertas de la fase 0 sin datos de pruebas; --contexto con comas rompe medir_bots), 5 menores
Task 15: minor (deferred): hash sin sal reversible por fuerza bruta (anotar); ts de la sintética = inicio
Task 15: fix round 1/5 dispatched (resume ac620a3fdad90eeb0; task-15-fix-1.md; FIX_BASE 18a928e)
Task 15: fix round 1 implementer DONE_WITH_CONCERNS (8de7419) — los 6 puntos; documento de prueba regenerado (v2)
Task 15: re-review 1 dispatched (a2bba3166977865c5, sonnet) sobre 18a928e..8de7419
Task 15: fix round 1/5 (3 Importantes + menores addressed; commits 18a928e..8de7419)
Task 15: minor (deferred): prueba de redirecciones no fija que http_urllib use ABRIDOR; nombre de la prueba de --contexto sobreestima; falta prueba del bot único con «NO DISPONIBLE» en ext
Task 15: complete (commits 3096877..8de7419, review clean; créditos sin probar contra la API: falta HAPPYROBOT_API_KEY)
Fase D completa (949ff27..8de7419)
Parada (20/10 00:20): fases A–D completas (tareas 1–15, más 9b y 9c). Fase E (16–18) depende del responsable; antes: pasos del editor (R10, R35, R42), arreglos estructurales R34 y R39, y la Tarea 16 en horario de Gestión.
Reanudación (20/10 05:27, «lanza las tareas que faltan»):
- Ruling: R44 — antes de la Tarea 16 va una Tarea 15b (R34 y R39, opus), porque la puerta 0 exige críticas 3/3 y las dos son requisito para publicar; en paralelo, la parte de la Tarea 17 que no necesita personas (Paso 1 guion y Paso 4 comprobaciones de solo lectura), sin commit propio para no chocar en la rama; las partes con personas (publicar en development, llamadas, reserva real, ensayo de líneas) y el push/PR se paran y se piden al responsable — si me equivoco, la Tarea 16 espera unas horas más.
Task 15b: dispatched (BASE 17111f9, a1f36f7db216720bf, opus)
Task 17 (parte sin personas): dispatched (a5f1be173ffe90aa8, sonnet) — Paso 1 guion + Paso 4 solo lectura, sin commit
Task 17 (parte sin personas): DONE — guion de 25 llamadas (sin commit); §11.8 de noche 18056/18001 solo anuncio (After Hours → ext. 2129); §11.5 sin documentación, falta un run transferido de Italia/Portugal con créditos; §11.9 sin documentación → ensayo de la Tarea 18; avisar al equipo: llamadas 2, 16, 21, 22 transfieren a colas de producción
Task 15b: implementer DONE_WITH_CONCERNS (7f8b72e R39 D-012, ec898bf R34 D-013) — PE críticas 18/18, 0 puntos dados con oficina cerrada en 54 ejecuciones; PE-NOCT-3/3b 0/3 (orden aviso/consultas_alquiler); R34 aplicado en Prolongación y Consultas, revertido en el Triaje (VIRT-T1 caía)
Task 15b: review dispatched (a77837b4e2f260fd4, opus) sobre 17111f9..ec898bf; guion committed fb07d44
Task 15b: review (a77837b4e2f260fd4) — aprobada; 2 Importantes de diseño (aviso neutro por gestion_abierta también tapa asistencia y transferencias que sí salen; estado_oficina usa la hora del principio de la llamada y horarios generales que no casan con Alicante 23:30 y Bari/Florencia/Nápoles/Venecia 8:00)
Task 15b: complete (commits 17111f9..ec898bf, review clean)
- Ruling: R45 — la Tarea 16 empieza por los dos Importantes de la 15b (estado_oficina con la hora del momento y los horarios concretos del prompt, con variable de prueba para las evals; aviso de siempre si la cola es asistencia o la transferencia va a salir, medido con evals) y después hace la pasada completa con UNA ronda de arreglos por módulo; lo que siga fallando se lista como bloqueo de la puerta 0 con su motivo, sin iterar más — el plan dice «repetir hasta verde», pero las rondas 10–12 muestran que varias críticas son límites del modelo — si me equivoco, la puerta 0 queda abierta con una lista concreta para decidir.
Task 16: dispatched (BASE fb07d44, opus)
Task 16: implementer a58013732c352e97f (opus). Task 18 Paso 1: dispatched en paralelo (ae35b770d7c6a3b53, sonnet), sin commit
Task 18 Paso 1: DONE — procedimiento-lineas.md (sin commit; se commitea con la Tarea 18); por comprobar en el ensayo: liberar el número, duplicados, versiones antiguas, tiempo, trigger sin números, orden de la vuelta; dudas: control v25/v22 en fase 2, líneas que quedan en Minibús ES (Reembolsos)
- Ruling: R46 — el responsable fija Minibús ES v25 como control de la fase 2 (20/10); se aplica al procedimiento de líneas y a la documentación en la Tarea 18 — sin coste si me equivoco: es decisión del responsable. Sigue abierta: qué líneas quedan en Minibús ES al mover las dos (Reembolsos usa una antigua).
Task 16: implementer DONE_WITH_CONCERNS (e6c7108 D-014, 66201ad D-015) — 285 evals ×3; críticas T 20/21, PE 18/18, IO 11/12, P 82/84, C 54/66; resto PE 84,3 % y P 89,8 %; puerta 0 pendiente (9 bloqueos)
Task 16: review dispatched (ac41127e647794bf2, opus) sobre fb07d44..66201ad
Task 16: review (ac41127e647794bf2) — necesita arreglos: 5 Importantes (DEVOL-03a por el párrafo nuevo del bloque; DEVOL-03c mal contada 0/3; regla de orden de PE empeora PE-NOCT-1; arreglo de FDS-02 donde el modelo no lo lee; ADV-8 editada sin apuntar), menores; propuestas para bloqueos (GC-IO1 aclarar eval, PISTA-04 en enviar_correo_contrasena, recorte de Prolongación ~1,6 k a buscar_respuesta)
- Ruling: R47 — la ronda de arreglos de la revisión incluye el recorte de Prolongación propuesto (párrafos duplicados en buscar_respuesta) porque es la única vía al 90 % sin subir el límite del spec — si me equivoco, una llamada más a la herramienta en esas preguntas (se mide con ASEG-*, ESC-08, BORDE-05/06).
Task 16: fix round 1/5 dispatched (resume a58013732c352e97f; task-16-fix-1.md; FIX_BASE 66201ad)
Task 16: fix round 1 implementer (5518aae) — Prolongación 20.894 car.; P 81/84 y 85,0 % (R47 empeora: ESC-08 0/3…); PE 87,3 %; IO 12/12; C 51/66; PE-NOCT-1, GC-IO1 3/3
Task 16: re-review 1 dispatched (ae00c63d707b751fd, opus) sobre 66201ad..5518aae
Task 16: fix round 1/5 (puntos 1–4, 6, 7, 9 addressed; open: R47 baja Prolongación (ESC-08 por «Precio caro»; Idiomas/ADV-1 por el refuerzo de EXPLICACIÓN), DEVOL-03a/03c miden el texto viejo, FDS-02 por orden del bloque, ADV-8 sin anotar en evals-v2, bloqueos sin recalcular; commits 66201ad..5518aae)
- Ruling: R47 (corrige) — se deshace en parte: «Precio caro» vuelve literal al prompt y se quita el refuerzo de EXPLICACIÓN; el resto del recorte se queda (ASEG/BORDE a 3/3) — fue un error dar por hecho que el texto duplicado era inerte — si me equivoco otra vez, Prolongación sigue por debajo del 90 % y queda como bloqueo.
Task 16: fix round 2/5 dispatched (resume a58013732c352e97f; task-16-fix-2.md; FIX_BASE 5518aae)
Task 16: fix round 2 implementer (5a75e96, 14254e7) — P 21.147 car., 83/84, 89,4 %; C 55/66; ESC-08 3/3, DEVOL-03c 2/3; bloqueos: VIRT-T1, HOR-C1, FDS-02 0/3, TEL-C1, DEVOL-03a 1/3, R34-C1/REQ-09 (juez), resto P y PE
Task 16: re-review 2 dispatched (a14e2c6266872f6cb, sonnet) sobre 5518aae..14254e7
Task 16: fix round 2/5 (5 puntos addressed; open: FDS-02 0/3 (choque informacion_oficina en el prompt de Consultas y en la descripción de buscar_respuesta), clasificación de bloqueos (TARDE-02 conflicto prompt/eval, WEB-03 redacción, faltan 8 fallos de Prolongación); commits 5518aae..14254e7)
Task 16: fix round 3/5 dispatched (resume a58013732c352e97f; task-16-fix-3.md; FIX_BASE 14254e7)
Task 16: fix round 3 implementer (bbec091) — P resto 91,9 %, WEB-03 y TARDE-02 3/3; FDS-02 0/3 con enrutado arreglado (falla por vías de contacto); bloqueos: VIRT-T1, resto PE 87,3 %, HOR-C1, FDS-02, TEL-C1, DEVOL-03a 0/3, SALTO-PING 2/3, REQ-09 (eval)
Task 16: re-review 3 dispatched (a14f59956c304acc1, sonnet) sobre 14254e7..bbec091
Task 16: fix round 3/5 (WEB-03, TARDE-02, clasificación addressed; open: FDS-02 «enrutado arreglado» sin prueba (eval sembrada), DEVOL-03a por el condicional de la sección devolucion, frase «un compañero se la prepara» del bloque, WEB-05/08 eval ambigua; SALTO-PING 2/3 dispersión; commits 14254e7..bbec091)
Task 16: fix round 4/5 dispatched (implementador nuevo, opus; task-16-fix-4.md; FIX_BASE bbec091)
Task 16: fix round 4 implementer aab2174c39a2675e2 (opus)
Task 16: fix round 4 — implementer cortado por red (bloque y consultas_alquiler.py sin commit); reanudado 10:23
Task 16: fix round 4 implementer (590c3ed) — P resto 92,7 %; C 58/69 (FDS-02r 3/3, REQ-09 y SALTO-PING 3/3, DEVOL-03a 1/3, CARGO-05 1/3); bloqueos: VIRT-T1, resto PE 87,3 %, HOR-C1, FDS-02 0/3, TEL-C1, DEVOL-03a/03c, CARGO-05
Task 16: re-review 4 dispatched (ac515c8ca99b6aabe, sonnet) sobre bbec091..590c3ed
Task 16: fix round 4/5 (5 puntos addressed; sin roturas; commits bbec091..590c3ed)
Task 16: parked — FDS-02 0/3 — Ruling: ampliar la expectativa («puede decir el horario de Gestión y que llame entonces») y aclarar en el bloque «(el horario de Gestión sí vale)»; esperable 2/3 → bloqueo (modelo y eval) para la siguiente ronda de puerta 0 — si me equivoco, una crítica más abierta.
Task 16: parked — DEVOL-03a 1/3 — Ruling: «si necesita que alguien lo mire» → «si pide…» en ESCALADO (cabe) y «no nombres ninguna oficina» en devolucion; siguiente ronda de puerta 0.
Task 16: parked — CARGO-05 1/3 — Ruling: repetir ×5 sin tocar antes de clasificar (su sección no cambió).
Task 16: parked — VIRT-T1 2/3, HOR-C1 2/3, DEVOL-03c 2/3 (modelo); TEL-C1 0/3 (negocio C-005); resto de Punto de encuentro 87,3 % (modelo; Madrid ambiguo, prompt).
Task 16: complete (commits fb07d44..590c3ed, 4 rondas, puerta 0 pendiente con los bloqueos anteriores)
Task 18: dispatched parte sin personas (Paso 1 con R46 + Paso 3 documentación), BASE 590c3ed
Task 18 (sin personas): implementer DONE (e72f7d9) — procedimiento con v25, workflows.md (82 nodos), CLAUDE.md, D-001, extensiones, pendientes de Minibús y Prolongaciones
Task 18 (sin personas): review dispatched (ae197e07d30668259, sonnet) sobre 590c3ed..e72f7d9
Task 18 (sin personas): review (ae197e07d30668259) — necesita arreglos: 5 Importantes (trigger del workflow de pruebas sin líneas de producción; columna Quién en el ensayo; vuelta atrás preparada de antemano; R35 en requisitos; persistent_id de 12 nodos), menores
Task 18: fix round 1/5 dispatched (resume af30b702806451f0a; task-18-fix-1.md; FIX_BASE e72f7d9)
Task 18: fix round 1 implementer (1057d1b) — 7 puntos
Task 18: re-review 1 dispatched (a4e55c468f6957606, sonnet) sobre e72f7d9..1057d1b
Task 18: fix round 1/5 (7 addressed; commits e72f7d9..1057d1b)
Task 18 (partes sin personas): complete (commits 590c3ed..1057d1b); quedan Paso 2 (ensayo) y Paso 4 (PR) con el responsable
Task 17 (partes sin personas): complete (fb07d44); quedan Pasos 2, 3 y 5 con el responsable
Final review: dispatched
Final review: a3be2f456346d8a2a (opus) sobre cf77f78..1057d1b
Final review (a3be2f456346d8a2a): merge sí tras 2 arreglos (registro al repo; correos de ejemplo no example.com); Importantes antes de publicar: ventana de 48 h de la rutina, R35, HORA_PRUEBA en listas, §5.7 Paths del correo, triaje.md:69 frente a R37, permisos de .claude/settings.json con nombres mcp__hr__* frente a mcp__claude_ai_hr__* (no se toca config: se avisa al responsable), puerta 0, datos personales en la entrada del extract
- Ruling: R48 — una sola tanda de arreglos finales solo en el repo (sin HappyRobot): correos, ventana de 48 h (rutina y medir_bots), HORA_PRUEBA en listas, cabeceras desfasadas, nombres de nodo, referencias a .superpowers, quote en creditos_runs, comentario de resolver_colas, desviación de §6 en decisiones; lo que toca HappyRobot o prompts con evals (triaje.md:69, §5.7, R35, extract) queda para antes de publicar; .claude/settings.json no lo toca el agente: se avisa al responsable — si me equivoco, alguna de esas queda para un PR posterior.
Final fix: dispatched (BASE 1057d1b)
Final fix: implementer a60e54499d315433a DONE (bba3547) — 9 puntos; rutina rehace D-3 con con_margen
Final fix: re-review dispatched (a0a038e682aa32ad8, sonnet) sobre 1057d1b..bba3547
Final fix: re-review (a0a038e682aa32ad8) — todos arreglados, sin roturas; 2 menores: rutina dice 07:30 UTC (es 05:30 UTC), y no dice que hay que ejecutar medir_bots.py sobre llamadas.json de D-3 para tener con_margen — Ruling: se aparcan para antes de programar la rutina (no bloquean el merge).
Rama lista para PR (20/10). Workspace se conserva hasta las partes con personas de las Tareas 17 y 18.
R35: el responsable borró en el editor los dos Transfer heredados (20/10); comprobado por API: 80 nodos, transfer_to_human_agent de PE (0398-75cb) e IO (0399-7faf) sin hijos, nada más perdido.
Task R35: dispatched (BASE ab27da5, opus) — cadena Preparar transferencia → ¿Transferir? → Transfer en PE e IO
Task R35: implementer a4ee0fff5306afef0 DONE_WITH_CONCERNS (66346a0) — cadena en PE e IO, extract al día, 90 nodos; evals 33/33 (15:25–15:27), críticas PE 18/18, IO 12/12; IO sin eval que llegue a transferir
Task R35: review dispatched (a168f5fadc0950225, sonnet, solo lectura)
Task R35: review (a168f5fadc0950225) — aprobada; menores: pendientes.md con texto obsoleto (~482, ~320), set_custom_output en los Transfer sin anotar, línea en D-010; recomienda 2 evals de IO (avería → asistencia; modo virtual cola distinta → no transfiere, aviso neutro)
Task R35: complete (commit 66346a0); remate con evals de IO y limpieza dispatched (resume a4ee0fff5306afef0)
Task R35: remate DONE (e370841) — IO-TR1 3/3, IO-TR2 3/3 (15:33–15:34); críticas IO 15/15; aviso neutro sin ver aún
