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
