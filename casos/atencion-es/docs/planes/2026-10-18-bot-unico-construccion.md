# Plan de construcción · Bot único de atención España (fase 1: Minibús + Prolongación)

> **Para agentes:** SUB-SKILL OBLIGATORIA: usa superpowers:subagent-driven-development (recomendada) o
> superpowers:executing-plans para ejecutar este plan tarea a tarea. Los pasos usan casillas (`- [ ]`).

**Objetivo:** construir, sin publicar, la versión `v2 · bot único: Triaje + 4 módulos` del workflow nuevo «Centauro
Atención España», con sus evals en verde, su medición y todo lo que pide la puerta 0 del spec.

**Arquitectura:** duplicado de Minibús ES v25. Triaje corto que encamina a cuatro módulos (Punto de encuentro,
Información de oficina, Prolongación, Consultas del alquiler) con herramientas y Module Change. Las respuestas del
alquiler llegan por la herramienta `buscar_respuesta` (Python generado desde el bloque común). Las transferencias
pasan por un Python que elige la extensión y no transfiere a Gestión cerrada.

**Herramientas:** MCP de HappyRobot, Python 3.11 de la biblioteca estándar (pruebas como scripts con
`python3 -I`, igual que `casos/prolongaciones/codigo/`), git.

**Spec:** `casos/atencion-es/docs/specs/2026-10-18-bot-unico-arquitectura.md` (léelo entero antes de empezar; las
referencias «§» de este plan son suyas).

**Fuera de este plan:** publicar la v2 y mover las líneas (fases 1 y 2 del spec). Lo hace una persona siguiendo
`casos/atencion-es/docs/procedimiento-lineas.md` (Tarea 18), cuando la puerta 0 esté superada.

## Restricciones globales

- **Nunca** editar ni publicar Minibús ES (`019f7594-…`), Prolongaciones (`01a0d9de-…`) ni ninguna versión
  publicada. **Publicar lo hace una persona**: el agente no ejecuta `manage_versions action=publish`.
- Todas las escrituras en HappyRobot piden confirmación (`.claude/settings.json`); no se esquivan.
- **«Centauro MCP» va contra la API real**: nunca se ejecuta una cadena con MCP con datos reales. En las pruebas
  de nodos solo datos inventados que no existen («Prueba Prueba», 03/03/1990, `prueba.prueba@example.com`,
  reserva `ER00000000`). En las evals, el resultado de las herramientas va como mensaje `tool`. **No hacer refresh**
  de servidores MCP.
- **Module Change no se crea por API**: lo crea el responsable (jzerpa) en el editor; el agente le da la lista
  exacta y espera.
- En el repo no van teléfonos, nombres, correos, reservas ni matrículas. Los números de las líneas van como
  `<LINEA_PROLONGACION_ES>`, `<LINEA_PROLONGACION_EN>`, `<LINEA_MINIBUS_ES>`, `<LINEA_MINIBUS_EN>`; los reales se
  ponen al pegar el código en HappyRobot.
- Variables en actualizaciones: `{{persistent_id.variable}}`, nunca índices. Salidas de AI Extract con
  `response.`. Después de cambios en bloque, `fix_broken_vars` con `dry_run: true` y luego sin él.
- Los nodos se localizan por **nombre**.
- Modelos: Triaje y Punto de encuentro `fast-turbo-one` (gpt-4.1-fast); Información de oficina `fast-gpt-4.1`;
  Prolongación `fast-gpt-5.4`; Consultas `fast-gpt-4.1` hasta que la Tarea 9 decida; extract GPT-5.6 Luna.
- Tamaños máximos de prompt (caracteres, contados en el fichero del repo): Triaje 9.000; Prolongación 22.000;
  Consultas 8.000; bloque de reglas comunes 4.500.
- Colas (`cola`): `gestion` 18057/18061, `asistencia` 18034/18035, `nueva_reserva` 18001/18006, `minibus`
  18056/18059 (español/inglés). Nunca 2114, 2115 ni 2119.
- `motivo_transferencia`: `no_iniciada`, `web_no_disponible`, `pregunta_reserva_concreta`, `aseguradora`, `enfado`,
  `error_tecnico`, `minibus`, `asistencia`, `nueva_reserva`, `correo_no_coincide`, `otro`.
- Horarios (hora peninsular): Gestión abierta de lunes a viernes de 8:00 a 21:00, salvo festivos nacionales; modo
  virtual de 22:00 a 8:00.
- Idioma de docs, commits y nombres de versión: castellano. Commits con
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. Rama: `comun/bot-unico-arquitectura`.

## Revisión: casos que ninguna tarea cubre por sí sola

1. **Gestión cierra durante la llamada** (empieza a las 20:55 y pide una persona a las 21:02): no se transfiere.
   «Preparar transferencia» calcula la hora al ejecutarse, no se fía de `gestion_abierta` del principio. Se fija
   en la Tarea 3 (caso `21:02 con gestion_abierta true`).
2. **Línea desconocida, número oculto o llamada web:** la llamada se atiende como Minibús en español, salvo que
   la variable de pruebas `OPCION_PRUEBA` diga otra cosa (así se prueba la línea de Prolongación por web). Se fija
   en la Tarea 1.
3. **Festivo nacional entre semana a las 10:00:** Gestión cerrada en el contexto y en la transferencia. Tareas 1
   y 3 (8/12/2026).
4. **El cliente cambia de tema tres veces:** al tercer salto se transfiere (o se da el horario si no hay a quién).
   Tarea 12 (SALTO-PING).
5. **La sección de `buscar_respuesta` no tiene la respuesta:** el bot lo dice y sigue las reglas de escalado, sin
   inventar. Tarea 9 (BR-04).

---

## Fase A · Código de los nodos (local, con pruebas)

Formato común de los ficheros de nodo (como `casos/prolongaciones/codigo/decidir_envio.py`): funciones puras y, al
final, el bloque `try: _entrada = input_data … except NameError` que asigna `output`. Cabecera de comentario con el
nodo donde se pega. Pruebas: `test_<nombre>.py`, que imprimen `N/N casos correctos` y salen con 1 si algo falla.

### Tarea 1: «Contexto de la llamada»

**Ficheros:**
- Crear: `casos/atencion-es/codigo/contexto_llamada.py`
- Crear: `casos/atencion-es/codigo/test_contexto_llamada.py`
- Referencia: el código de «Calcular horario nocturno» de la v25 (se guarda en la Tarea 6; mientras, el de la v22
  en `casos/minibus/prompts/minibus-es/v22/calcular-horario-nocturno.md` es casi igual).

**Interfaces:**
- Produce:
  - `LINEAS: dict[str, tuple[str, str]]` = `{"<LINEA_PROLONGACION_ES>": ("prolongacion", "es"), "<LINEA_PROLONGACION_EN>": ("prolongacion", "en"), "<LINEA_MINIBUS_ES>": ("minibus", "es"), "<LINEA_MINIBUS_EN>": ("minibus", "en")}`; la clave se compara con el final de los dígitos de `to_number`.
  - `FESTIVOS_NACIONALES: set[date]` (2026 y 2027).
  - `hora_madrid(ahora_utc: datetime) -> datetime` (horario de verano calculado a mano, como la v25: del último domingo de marzo a la 01:00 UTC al último domingo de octubre a la 01:00 UTC).
  - `gestion_abierta_en(ahora_utc: datetime) -> bool`
  - `modo_virtual_en(ahora_utc: datetime) -> bool`
  - `contexto(input_data: dict, ahora_utc: datetime | None = None, lineas: dict = LINEAS) -> dict`. Entrada: `from_number`, `to_number`, `opcion_prueba` (opcional). Salida: todas las de la v25 (§4 del informe en el spec: `nocturno_*`, `hora_*`, `callcenter_abierto`, `modo_virtual`, `saludo`, `saludo_en`, `saludo_localizado`, `idioma`, `idioma_nombre`, `numero_marcado`, `mensaje_inicial`, `recording_id`, `telefono_dictado`, `gestion_abierta`, `whatsapp_disponible`, `horario_verano`) más `opcion_menu` y `festivo_nacional`.

- [ ] **Paso 1: Escribir las pruebas que fallan** en `test_contexto_llamada.py`, con `LINEAS_PRUEBA = {"111": ("prolongacion", "es"), "222": ("prolongacion", "en"), "333": ("minibus", "es"), "444": ("minibus", "en")}` y horas UTC fijas:

```python
# (nombre, input_data, ahora_utc, comprobaciones)
("prolongación ES, martes 10:00", {"to_number": "+34900000111", "from_number": "+34600000000"},
 datetime(2026, 10, 20, 8, 0, tzinfo=UTC),
 {"opcion_menu": "prolongacion", "idioma": "es", "gestion_abierta": True, "modo_virtual": False}),
("mensaje de Prolongación ES", ...mismo..., {"mensaje_inicial": "Centauro Rent a Car, buenos días, le atiende Daniel, su asistente de IA. ¿Quiere prolongar un alquiler que tiene en curso?"}),
("mensaje de Prolongación EN", {"to_number": "+34900000222", ...}, mismo instante,
 {"idioma": "en", "mensaje_inicial": "Centauro Rent a Car, good morning, this is Daniel, your AI assistant. Would you like to extend a rental you currently have?"}),
("minibús ES conserva el saludo de la v25", {"to_number": "+34900000333", ...}, mismo instante,
 {"opcion_menu": "minibus", "mensaje_inicial": <el texto de la v25 para español, modo normal>}),
("línea desconocida → minibús es", {"to_number": "+34900000999", ...}, mismo instante, {"opcion_menu": "minibus", "idioma": "es"}),
("web con OPCION_PRUEBA", {"to_number": "web", "from_number": "web", "opcion_prueba": "prolongacion"}, mismo instante,
 {"opcion_menu": "prolongacion", "idioma": "es", "whatsapp_disponible": False}),
("21:00 en punto cierra Gestión", ..., datetime(2026, 10, 20, 19, 0, tzinfo=UTC), {"gestion_abierta": False, "modo_virtual": False}),
("20:59 sigue abierta", ..., datetime(2026, 10, 20, 18, 59, tzinfo=UTC), {"gestion_abierta": True}),
("22:00 entra el modo virtual", ..., datetime(2026, 10, 20, 20, 0, tzinfo=UTC), {"modo_virtual": True}),
("sábado 10:00 cerrada", ..., datetime(2026, 10, 24, 8, 0, tzinfo=UTC), {"gestion_abierta": False}),
("festivo 8/12/2026 10:00", ..., datetime(2026, 12, 8, 9, 0, tzinfo=UTC), {"gestion_abierta": False, "festivo_nacional": True}),
("cambio de hora: lunes 26/10 08:30 (UTC+1)", ..., datetime(2026, 10, 26, 7, 30, tzinfo=UTC), {"gestion_abierta": True}),
("viernes 23/10 08:30 (UTC+2)", ..., datetime(2026, 10, 23, 6, 30, tzinfo=UTC), {"gestion_abierta": True}),
("nocturno CET a las 23:30", ..., datetime(2026, 10, 20, 21, 30, tzinfo=UTC), {"nocturno_cet": True}),
```

  Más una prueba de que todas las fechas de `FESTIVOS_NACIONALES` caen en 2026 o 2027 y de que están las del spec:
  1/1, 6/1, 3/4, 1/5, 15/8, 12/10, 8/12 y 25/12 de 2026; 1/1, 6/1, 26/3, 1/5, 15/8, 12/10, 1/11, 6/12, 8/12 y
  25/12 de 2027.
- [ ] **Paso 2: Ejecutar y comprobar que fallan.** `python3 -I casos/atencion-es/codigo/test_contexto_llamada.py` → error de import.
- [ ] **Paso 3: Implementar `contexto_llamada.py`** portando el código de la v25 a funciones y añadiendo `opcion_menu`, `festivo_nacional`, los dos mensajes de Prolongación (texto exacto de las pruebas; en modo virtual, el mismo: §5.2) y `gestion_abierta = gestion_abierta_en(ahora)`. `opcion_prueba` solo se usa si `to_number` no está en `lineas`. Comprobar la lista de festivos de 2027 con la resolución del BOE si ya está publicada; si cambia, se cambia la prueba.
- [ ] **Paso 4: Ejecutar y comprobar que pasan.** Mismo comando → `N/N casos correctos`.
- [ ] **Paso 5: Commit.** `git add casos/atencion-es/codigo/contexto_llamada.py casos/atencion-es/codigo/test_contexto_llamada.py` y `git commit -m "Atención España: código de «Contexto de la llamada» con opción del menú y festivos"`.

### Tarea 2: «Resolver colas»

**Ficheros:**
- Crear: `casos/atencion-es/codigo/resolver_colas.py`
- Crear: `casos/atencion-es/codigo/test_resolver_colas.py`
- Referencia: `casos/minibus/prompts/minibus-es/v22/resolver-colas-por-idioma.md`

**Interfaces:**
- Produce: `COLAS: dict[str, dict[str, str]]` (clave → `{"es": ext, "en": ext}`, claves `nueva_reserva`, `horario_minibus`, `gestion_reserva`, `asistencia`) y `resolver(input_data: dict) -> dict`. Entrada: `idioma`, `gestion_abierta`. Salida: `idioma_colas` (`es` o `en`), `gestion_abierta` (bool), y por clave `cola_<clave>` (`sip:<ext>@hrpbx.buscentauro.com`), `cola_<clave>_ext`, `cola_<clave>_nombre`.

- [ ] **Paso 1: Pruebas que fallan:** `idioma="en"` → `cola_gestion_reserva == "sip:18061@hrpbx.buscentauro.com"`; `idioma="it"` → `idioma_colas == "es"` y `cola_asistencia_ext == "18034"`; con `gestion_abierta=False` → `cola_gestion_reserva == "sip:18057@hrpbx.buscentauro.com"` y `"NO DISPONIBLE" not in json.dumps(salida)`; no hay ninguna clave `cola_fuera_horario*`; ninguna extensión es `2114`, `2115` ni `2119`; `cola_asistencia_nombre == "RA ES-ES AVERÍAS"` y en inglés `"RA ES-EN Breakdowns"`.
- [ ] **Paso 2: Ejecutar y ver que fallan.** `python3 -I casos/atencion-es/codigo/test_resolver_colas.py`
- [ ] **Paso 3: Implementar** a partir del código de la v22/v25, quitando la sustitución por el texto «NO DISPONIBLE…» y la cola de fuera de horario.
- [ ] **Paso 4: Ejecutar y ver que pasan.**
- [ ] **Paso 5: Commit** (`Atención España: código de «Resolver colas» sin textos en lugar de extensiones`).

### Tarea 3: «Preparar transferencia»

**Ficheros:**
- Crear: `casos/atencion-es/codigo/preparar_transferencia.py`
- Crear: `casos/atencion-es/codigo/test_preparar_transferencia.py`

**Interfaces:**
- Consume: las salidas `cola_*` de la Tarea 2 (como entradas del nodo) y una **copia** de `hora_madrid`, `gestion_abierta_en` y `FESTIVOS_NACIONALES` de la Tarea 1 (el nodo de HappyRobot no puede importar).
- Produce: `preparar(input_data: dict, ahora_utc: datetime | None = None) -> dict`. Entrada: `cola` (`gestion` | `asistencia` | `nueva_reserva` | `minibus`), `cola_gestion_reserva`, `cola_asistencia`, `cola_nueva_reserva`, `cola_horario_minibus`. Salida: `transferir` (bool), `numero` (URI o `""`), `resultado` (`transferir` | `gestion_cerrada` | `cola_no_valida`), `detalle` (instrucción corta para el agente).
- Textos fijos de `detalle`:
  - `gestion_cerrada`: «No se ha transferido: el equipo de gestión de reservas atiende de lunes a viernes de ocho de la mañana a nueve de la noche, salvo festivos. Díselo al cliente con calma, no digas que le pasas con nadie y sigue con COLA DE GESTIÓN CERRADA.»
  - `cola_no_valida`: «No se ha transferido: la cola no es válida. Usa gestion, asistencia, nueva_reserva o minibus.»

- [ ] **Paso 1: Pruebas que fallan** (URIs de prueba `sip:1@x`, `sip:2@x`, `sip:3@x`, `sip:4@x`):
  - `cola="asistencia"`, sábado 03:00 → `transferir True`, `numero "sip:2@x"`;
  - `cola="gestion"`, martes 10:00 → `transferir True`, `numero "sip:1@x"`;
  - `cola="gestion"`, martes 21:02 (`datetime(2026,10,20,19,2,tzinfo=UTC)`) aunque la entrada traiga `gestion_abierta: True` → `resultado "gestion_cerrada"`, `numero ""`;
  - `cola="gestion"`, 8/12/2026 10:00 → `gestion_cerrada`;
  - `cola="gestion"`, domingo → `gestion_cerrada`;
  - `cola="minibus"` y `cola="nueva_reserva"` a las 23:00 → `transferir True` (el modo virtual lo controla el prompt, no este nodo);
  - `cola="GESTION "` (mayúsculas y espacios) → se normaliza;
  - `cola=""` o `cola="18057"` → `cola_no_valida`, `transferir False`;
  - una prueba que recorre todas las horas de una semana de octubre y de una de diciembre y comprueba que la copia de `gestion_abierta_en` da lo mismo que la de `contexto_llamada.py`.
- [ ] **Paso 2: Ejecutar y ver que fallan.** `python3 -I casos/atencion-es/codigo/test_preparar_transferencia.py`
- [ ] **Paso 3: Implementar.**
- [ ] **Paso 4: Ejecutar y ver que pasan.**
- [ ] **Paso 5: Commit** (`Atención España: «Preparar transferencia» con red de seguridad de Gestión cerrada`).

### Tarea 4: `buscar_respuesta` generada desde el bloque

**Ficheros:**
- Crear: `casos/atencion-es/codigo/generar_consultas.py`
- Crear (generado, se versiona): `casos/atencion-es/codigo/consultas_alquiler.py`
- Crear: `casos/atencion-es/codigo/test_consultas_alquiler.py`

**Interfaces:**
- Produce:
  - `python3 -I casos/atencion-es/codigo/generar_consultas.py` lee `comun/bloques/consultas-alquiler.md` y escribe `consultas_alquiler.py`.
  - En `consultas_alquiler.py`: `SECCIONES: dict[str, str]` y `buscar(input_data: dict) -> dict` con entrada `tema`, `pregunta` y salida `tema` (el usado), `texto`, `encontrado` (False si el tema no existía y se usó `otras`).
- Correspondencia título → tema: «DEVOLVER TARDE» → `devolver_tarde`; «COCHE DE ASEGURADORA O DE EMPRESA» → `aseguradora_empresa`; «DETALLES QUE PUEDES DAR» → `detalles_prolongacion`; «LA WEB NO LE DEJA» → `la_web_no_le_deja`; «RESERVA QUE AÚN NO HA EMPEZADO» → `reserva_no_iniciada`; «RECOGER TARDE» → `recoger_tarde`; «DEVOLVER ANTES, EN OTRA OFICINA…» → `devolucion`; «COMBUSTIBLE, FIANZA, CARGOS Y REEMBOLSOS» → `cargos_y_reembolsos`; «REQUISITOS Y CONDUCTORES» → `requisitos`; «DURANTE EL ALQUILER» → `durante_el_alquiler`; «OTRAS PREGUNTAS» → `otras`; «TELÉFONOS QUE PUEDES DAR» → `telefonos`. Cada subapartado de CONSULTAS FRECUENTES lleva delante el párrafo de introducción de esa sección.

- [ ] **Paso 1: Pruebas que fallan:** están los 12 temas; ningún texto tiene una línea que empiece por `>` ni contiene `DECIDIR`, `Solo en Minibús`, `Nuevo.` ni `Equipo (`; cada texto mide entre 1.000 y 6.000 caracteres; `reserva_no_iniciada` empieza con el párrafo «Son preguntas que no son de prolongación…»; `buscar({"tema": "fianza"})` → `tema "otras"`, `encontrado False`; `buscar({"tema": " Requisitos "})` → `requisitos`, `encontrado True`; generar en un directorio temporal y comparar con el `consultas_alquiler.py` versionado (tienen que ser idénticos); `len(open("consultas_alquiler.py").read()) < 45000`.
- [ ] **Paso 2: Ejecutar y ver que fallan.** `python3 -I casos/atencion-es/codigo/test_consultas_alquiler.py`
- [ ] **Paso 3: Implementar `generar_consultas.py`** (corta por los títulos `###`/`####` de la parte «## Bloque», quita las notas y escribe `SECCIONES` con `repr()`), y generar `consultas_alquiler.py`.
- [ ] **Paso 4: Ejecutar y ver que pasan.**
- [ ] **Paso 5: Commit** (`Atención España: buscar_respuesta generada desde el bloque de consultas`).

### Tarea 5: `pista_correo`

**Ficheros:**
- Crear: `casos/atencion-es/codigo/pista_correo.py`
- Crear: `casos/atencion-es/codigo/test_pista_correo.py`

**Interfaces:**
- Produce: `pista(input_data: dict) -> dict`. Entrada: `result` e `is_error` del MCP Call `consultar_reserva`. Salida: **solo** `verificado` (bool), `dominio` (str, vacío si no verifica), `resultado` (`verificado` | `no_verificado` | `dato_no_interpretado` | `no_disponible`) y `detalle`. Mismo tratamiento de errores que `decidir_envio.py` (copia sus funciones `a_dict`, `texto_error` y `clasificar_error`).

- [ ] **Paso 1: Pruebas que fallan:** resultado verificado con `estado`, `fecha_hora_devolucion`, `oficina_recogida` y `email_hint "gmail.com"` → salida con exactamente las cuatro claves, `dominio "gmail.com"`, y ninguno de los otros valores aparece en `json.dumps(salida)`; `email_hint "ana@gmail.com"` → `dominio "gmail.com"`; `email_hint` vacío y verificado → `verificado True`, `dominio ""`; no verificado → `dominio ""` aunque traiga `email_hint`; formato de contenido MCP (`[{"type": "text", "text": "{…}"}]`); `timeout` → `no_disponible`; «No se ha podido interpretar la fecha…» → `dato_no_interpretado` con el detalle de la fecha.
- [ ] **Paso 2: Ejecutar y ver que fallan.** `python3 -I casos/atencion-es/codigo/test_pista_correo.py`
- [ ] **Paso 3: Implementar.**
- [ ] **Paso 4: Ejecutar y ver que pasan.**
- [ ] **Paso 5: Commit** (`Atención España: pista_correo devuelve solo el dominio del correo`).

---

## Fase B · Workflow base

### Tarea 6: Duplicar la v25, comprobar qué se copia y abrir la v2

**Ficheros:**
- Crear: `casos/atencion-es/prompts/atencion-es/v1/*.md` (copia de todos los nodos con prompt, código o configuración relevante, con la cabecera de `prompts/README.md`)
- Modificar: `casos/atencion-es/docs/workflows.md`, `casos/atencion-es/docs/pendientes.md`, `casos/atencion-es/CLAUDE.md` (tabla con ids)

**Interfaces:**
- Produce: `workflow_id` y slugs de la v1 y la v2 del workflow nuevo, apuntados en `workflows.md`.

- [ ] **Paso 1:** `create_workflow` con `source.type = duplicate` desde Minibús ES, versión `k2in5n9kk01x`, nombre «Centauro Atención España», carpeta `019d8144-ce27-7aaf-b9e5-21d006083063`. Si `duplicate` no deja elegir versión, duplicar y comprobar que los nodos son los de la v25 (37 nodos, 4 `module-change`).
- [ ] **Paso 2: Comprobaciones §11.1 y §11.7** con `get_workflows` + `get_node_details`: que estén los 4 Module Change y apunten a los módulos del workflow nuevo (no a los de Minibús); qué evals hay en los prompts (`manage_custom_evals list`); que el trigger no ha copiado las líneas de Minibús (si las ha copiado, **quitarlas ya** de la v1 antes de nada: dos workflows con la misma línea es justo lo que no se quiere hasta producción); si existe tabla de Twin para el workflow nuevo. Apuntar el resultado en `pendientes.md`.
- [ ] **Paso 3:** renombrar la versión a `v1 · copia de Minibús ES v25` y guardar sus nodos en `prompts/atencion-es/v1/` (código Python incluido, con los números de línea sustituidos por los marcadores).
- [ ] **Paso 4:** `manage_versions action=fork` de la v1 → renombrar a `v2 · bot único: Triaje + 4 módulos`. **Toda la construcción va en la v2.**
- [ ] **Paso 5:** en la v2, borrar el Paths «Entrada» y sus condiciones «Siempre» y «Fallback», y enganchar «Receive Customer Call» directamente a «Resolver colas por idioma». `get_workflows` → la cadena es Inbound Call → Calcular horario nocturno → Resolver colas → Receive Customer Call.
- [ ] **Paso 6: Commit** (`Atención España: workflow creado (v1 copia de la v25, v2 en construcción)`).

### Tarea 7: Bloque de reglas comunes y comprobador de prompts

**Ficheros:**
- Crear: `comun/bloques/reglas-comunes.md`
- Crear: `casos/atencion-es/codigo/comprobar_prompts.py`
- Modificar: `comun/bloques/README.md` (fila del bloque nuevo)

**Interfaces:**
- Produce:
  - `reglas-comunes.md`: texto de prompt (sin notas `>` dentro del bloque) con las secciones de §5.10, en este orden: IDENTIDAD Y ESTILO (incluye validar el enfado antes de informar y no pedir datos personales, salvo los del correo de contraseña en Prolongación), REGLAS DE VOZ, IDIOMA DE ATENCIÓN, MODO DE ATENCIÓN, GESTIÓN CERRADA: REGLA DE MÁXIMA PRIORIDAD, TELÉFONOS QUE PUEDES DAR, CÓMO TRANSFERIR, SI LA TRANSFERENCIA FALLA, CAMBIOS DE MÓDULO. Usa las variables con los marcadores `{{idioma_nombre}}`, `{{modo_virtual}}`, `{{gestion_abierta}}`, que se cambian por la sintaxis de HappyRobot al subir. Sale de la V11 (Gestión cerrada, fallo de transferencia, teléfonos) y de la v25 (voz, idioma, modo virtual), con las resoluciones del equipo (francés con cuatro idiomas).
  - `python3 -I casos/atencion-es/codigo/comprobar_prompts.py <versión>` revisa `casos/atencion-es/prompts/atencion-es/<versión>/`: tamaños máximos (restricciones globales); que `triaje.md`, `punto-de-encuentro.md`, `informacion-de-oficina.md`, `prolongacion.md` y `consultas-del-alquiler.md` contienen el texto de `reglas-comunes.md` tal cual (sin contar los marcadores de variables); que ningún fichero contiene `NO DISPONIBLE`, `extension_destino`, `2114`, `2115`, `2119` ni una secuencia de 9 o más dígitos seguidos, con o sin espacios (los teléfonos permitidos se escriben en palabras, como en el bloque). Sale con 1 y la lista de fallos si algo no cumple.

- [ ] **Paso 1:** escribir `comprobar_prompts.py` y ejecutarlo sobre una carpeta de prueba con un prompt de 9.001 caracteres y otro sin el bloque → tiene que listar los dos fallos.
- [ ] **Paso 2:** escribir `reglas-comunes.md` y comprobar que mide ≤ 4.500 caracteres.
- [ ] **Paso 3: Commit** (`Común: bloque de reglas comunes y comprobador de prompts del bot único`).

### Tarea 8: Entrada, transferencias y Triaje

**Ficheros:**
- Crear: `casos/atencion-es/prompts/atencion-es/v2/triaje.md`, `herramientas-triaje.md`, `contexto-de-la-llamada.md`, `resolver-colas.md`, `preparar-transferencia.md`, `transfer.md`
- Modificar: `casos/atencion-es/docs/pendientes.md`

**Interfaces:**
- Consume: Tareas 1, 2, 3 y 7.
- Produce (los usan las Tareas 9 a 11):
  - el patrón de transferencia: herramienta `transfer_to_human_agent(cola, motivo_transferencia, resumen_para_agente)`, todos obligatorios, `message` tipo `ai` como en la v25, música «holdacent» → Python «Preparar transferencia» → Transfer «Initiate customer connection» con `number` = `fallback_number` = `{{<preparar>.numero}}`, whisper «Llamada del asistente de atención.» + resumen + `telefono_dictado`, `skip_digit_press: false`, `record_transfer_conversation: true`;
  - la forma de cortar la cadena con `transferir = false` (paso 4).

- [ ] **Paso 1:** pegar `contexto_llamada.py` en «Calcular horario nocturno» (renombrar el nodo a «Contexto de la llamada») y `resolver_colas.py` en «Resolver colas por idioma» (renombrar a «Resolver colas»), con los números reales en `LINEAS`. Crear la variable de workflow `OPCION_PRUEBA` (vacía) y pasarla como `opcion_prueba`. `test_node` de «Contexto de la llamada» con una entrada web → `opcion_menu` correcto.
- [ ] **Paso 2:** en la herramienta `transfer_to_human_agent` del Triaje, cambiar los parámetros a los de arriba (descripción de `cola` con las cuatro colas y, para `gestion`, el estado actual: «Gestión ahora: {{gestion_abierta}}»), e insertar el Python «Preparar transferencia» entre la herramienta y el Transfer.
- [ ] **Paso 3:** `test_node` de la cadena con `cola = "gestion"` y `cola = "asistencia"` (sin sala de llamada, el Transfer fallará como en la V11: lo que se mira es la salida del Python).
- [ ] **Paso 4: Comprobación §11.4.** Probar las dos formas de no transferir cuando `transferir = false` y quedarse con la primera que funcione:
  1. un Paths después del Python: «Transferir» (`transferir` es true) → Transfer; «Fallback» → sin hijos;
  2. Transfer con `numero` vacío.
  Criterio: en una llamada de prueba por web con `OPCION_PRUEBA = prolongacion` en un momento con Gestión cerrada, al pedir Gestión el agente recibe `resultado: gestion_cerrada` (o un error que el prompt sepa leer), no se marca ninguna llamada saliente y el bot sigue hablando. Apuntar la forma elegida en `pendientes.md` y en `transfer.md`.
- [ ] **Paso 5:** escribir `triaje.md` (≤ 9.000; contenido de §5.5; las listas nocturnas salen de aquí) y `herramientas-triaje.md` (descripciones de `buscar_punto_de_encuentro`, `informacion_oficina`, `consultas_alquiler` y la nueva `prolongar_alquiler(situacion)` con `message: none`). `python3 -I casos/atencion-es/codigo/comprobar_prompts.py v2` sin fallos para `triaje.md`.
- [ ] **Paso 6:** subir el prompt y las descripciones al Triaje. Crear la herramienta `prolongar_alquiler` (su hijo, el prompt «Prolongación», lo crea la Tarea 10; hasta entonces, un prompt provisional de una línea).
- [ ] **Paso 7: Evals del Triaje.** Adaptar las 24 de la v25: donde esperan `extension_destino` con una URI, pasan a esperar `cola` (18057/18061 → `gestion`, 18034/18035 → `asistencia`, 18001/18006 → `nueva_reserva`, 18056/18059 → `minibus`); las «nocturno · transfiere» de agosto pasan a esperar el aviso de cierre de la v25. Crear en la carpeta «Bot único · Triaje»:

| Eval | Conversación | Esperado |
|---|---|---|
| LINEA-01 | Línea de Prolongación; «Sí, quiero alargar el coche dos días» | `prolongar_alquiler`, sin preguntas antes |
| LINEA-02 | Línea de Prolongación; «No, es que no encuentro el minibús en Málaga» | `buscar_punto_de_encuentro` con aeropuerto Málaga |
| LINEA-03 | Línea de Prolongación; «¿Cuándo me devuelven la fianza?» | `consultas_alquiler` tema `cargos_y_reembolsos` |
| LINEA-04 | Línea de Minibús; «Quiero ampliar mi alquiler» | `prolongar_alquiler` |
| LINEA-05 | Línea de Minibús; «No me acuerdo de la contraseña de la web» | `prolongar_alquiler` |
| LINEA-06 | Línea de Prolongación; «Quiero hablar con una persona», luego «Nada, que me pase» (Gestión abierta) | `transfer_to_human_agent` `cola gestion`, `motivo otro` |
| LINEA-07 | Igual con Gestión cerrada | No transfiere; da el horario de Gestión |
| LINEA-08 | Línea de Minibús, igual que LINEA-06 | `cola minibus` |
| GC-T1 | Gestión cerrada; «Necesito que me cambien el conductor de mi reserva» | No transfiere; horario de Gestión y área de cliente |
| GC-T2 | Gestión cerrada; herramienta devuelve `gestion_cerrada` | No vuelve a intentarlo; da el horario sin «le paso» |
| VIRT-T1 | Modo virtual; reserva nueva | No transfiere; volver a llamar a partir de las ocho |
| COLA-T1 | Avería en la línea de Prolongación, inglés | `cola asistencia`, `motivo asistencia` |
| FEST-T1 | `gestion_abierta` false (festivo, martes 10:00); dato de su reserva | No transfiere |

  Las variables de cada eval fijan `opcion_menu`, `idioma_nombre`, `modo_virtual` y `gestion_abierta`. Ejecutar cada una 3 veces (`manage_custom_evals run` con la `version_id` de la v2). Criterio: críticas (GC-*, VIRT-*, COLA-*, FEST-*) 3/3; resto ≥ 90 %.
- [ ] **Paso 8:** `fix_broken_vars` (`dry_run: true`, luego sin él). Guardar las copias de los nodos tocados en `prompts/atencion-es/v2/`. Commit (`Atención España v2: entrada, transferencias y Triaje`).

---

## Fase C · Módulos

### Tarea 9: Consultas del alquiler

**Ficheros:**
- Crear: `casos/atencion-es/prompts/atencion-es/v2/consultas-del-alquiler.md`, `herramientas-consultas.md`, `buscar-respuesta.md`
- Crear: `casos/atencion-es/docs/informes/evals-v2.md` (lo continúan las Tareas 10 a 12 y 16)

**Interfaces:**
- Consume: Tarea 4 (`consultas_alquiler.py`), patrón de transferencia de la Tarea 8, Tarea 7.
- Produce: herramienta `buscar_respuesta(tema, pregunta)` (`tema` obligatorio, enum con los 12 temas de la Tarea 4; `pregunta` opcional, sin datos personales), `message: none`, hijo Python «Consultas del alquiler». La Tarea 10 crea otra igual en Prolongación.

- [ ] **Paso 1:** escribir `consultas-del-alquiler.md` (≤ 8.000): reglas comunes + qué atiende + uso de `buscar_respuesta` (§5.9: solo lo que devuelve, una o dos frases, si no está lo dice y escala) + escalado del módulo + cierre. `comprobar_prompts.py v2` sin fallos.
- [ ] **Paso 2:** en el nodo «Prolongación y consultas», renombrarlo a «Consultas del alquiler», subir el prompt, modelo `fast-gpt-4.1`; mantener `buscar_punto_de_encuentro` e `informacion_oficina` (Module Change existentes); cambiar su `transfer_to_human_agent` al patrón de la Tarea 8; crear `buscar_respuesta` con el Python de `consultas_alquiler.py` (comprobación §11.6: si el nodo no acepta el tamaño, partir `SECCIONES` en dos nodos Python por grupos de temas y apuntarlo); `prolongar_alquiler` y `volver_al_triaje` se crean en la Tarea 12.
- [ ] **Paso 3:** `test_node` de «Consultas del alquiler» (Python) con `tema = "requisitos"` → devuelve el texto.
- [ ] **Paso 4: Evals.** Copiar de «Prolongacion» (Prolongaciones v12, nodo `01a14967-184f-7e88-9762-0b35c8be6c44`) las carpetas Reserva no iniciada, Recoger tarde y oficinas, Devolver antes u otra oficina, Fianza combustible y cargos, Requisitos y durante el alquiler, y NOINI-08/09, FDS-02, FDS-03 y FDS-08 (`get` y `create` en el nodo nuevo, misma carpeta). Adaptar: la conversación empieza ya dentro del módulo (sin saludo); antes de la respuesta va la llamada a `buscar_respuesta` con su mensaje `tool` (texto de la sección generado por la Tarea 4); transferencias con `cola`; RECOG-04 (horario de Málaga) pasa a esperar `informacion_oficina`. Crear:

| Eval | Conversación | Esperado |
|---|---|---|
| BR-01 | «¿Puedo llevar el coche a Portugal?» sin herramienta previa | `buscar_respuesta` tema `durante_el_alquiler` |
| BR-02 | «Tengo 20 años, ¿puedo alquilar?» | `buscar_respuesta` tema `requisitos` |
| BR-03 | Con la sección devuelta, «¿y cuánto cuesta el conductor adicional?» | Cifra de la sección, una o dos frases, sin leer la sección entera |
| BR-04 | «¿Puedo pagar con puntos de fidelidad?»; la herramienta devuelve `otras` sin esa respuesta | Dice que no tiene ese dato; remite a la web o escala; no inventa |
| BR-05 | Tras responder, «vale, pues quiero prolongarlo» | Herramienta de salto a Prolongación (`prolongar_alquiler`) |
| GC-C1 | Gestión cerrada; reserva no iniciada, prefiere un compañero | No transfiere; horario de Gestión y área de cliente |

- [ ] **Paso 5: Elegir el modelo (§7.3).** Ejecutar el juego completo de Consultas 3 veces con `fast-gpt-4.1`, `fast-turbo-one` y `fast-gpt-5.4`. Quedarse con el más barato que esté a ≤ 3 puntos del mejor y sin fallos críticos. Apuntar la tabla en el informe de evals y dejar ese modelo en el nodo.
- [ ] **Paso 6:** guardar copias y commit (`Atención España v2: módulo Consultas del alquiler con buscar_respuesta`).

### Tarea 10: Prolongación

**Ficheros:**
- Crear: `casos/atencion-es/prompts/atencion-es/v2/prolongacion.md`, `herramientas-prolongacion.md`, `enviar-correo-contrasena.md`, `pista-correo.md`

**Interfaces:**
- Consume: Tareas 4, 5, 7, 8 y el código de `casos/prolongaciones/codigo/decidir_envio.py` y `resultado_envio.py` (sin cambios).
- Produce: prompt «Prolongación» como hijo de `prolongar_alquiler` (sustituye al provisional de la Tarea 8), con `enviar_correo_contrasena(email, nombre_completo, fecha_nacimiento)`, `pista_correo(numero_reserva, nombre_completo, fecha_nacimiento)`, `buscar_respuesta`, `informacion_oficina` (Module Change, Tarea 12), `volver_al_triaje` (Tarea 12) y `transfer_to_human_agent`.

- [ ] **Paso 1:** escribir `prolongacion.md` (≤ 22.000) a partir de `casos/prolongaciones/prompts/prolongacion-es/v12/prolongacion.md`: quitar lo que ya está en reglas comunes y CONSULTAS FRECUENTES (va por `buscar_respuesta`); dejar EXPLICACIÓN, ENVÍO DEL CORREO DE CONTRASEÑA, DEVOLVER TARDE, COCHE DE ASEGURADORA O DE EMPRESA (con la resolución del equipo), DETALLES QUE PUEDES DAR, LA WEB NO LE DEJA y CIERRE, en el texto del bloque común; añadir la pista del dominio (cuándo ofrecerla: el cliente no sabe con qué correo está su alquiler; qué decir: solo el dominio; después pide el correo y usa `enviar_correo_contrasena`) y la regla de §5.7 (reserva que no ha empezado → plan B, sin envío). `comprobar_prompts.py v2` sin fallos.
- [ ] **Paso 2:** subir el prompt (modelo `fast-gpt-5.4`, sin `initial_message`); crear `enviar_correo_contrasena` con su cadena de 4 nodos igual que en la v12 (`casos/prolongaciones/prompts/prolongacion-es/v12/enviar-correo-contrasena.md`: mismo texto de herramienta, credencial `01a0e1d8-9c92-7e58-8e25-caf109f1fadb`, event `019d4a7a-f3e9-7748-b002-efb988800cd3`); crear `pista_correo`: MCP Call `consultar_reserva` con `numero_reserva`, `nombre_completo` y `fecha_nacimiento` → Python `pista_correo.py`, `message` tipo `ai` («Un momento, lo compruebo»), como mucho dos llamadas por conversación; `buscar_respuesta` (copia de la de la Tarea 9) y la transferencia (patrón de la Tarea 8). La mejora de §5.7 (que «Enviar correo» no se ejecute si no coincide) solo se hace si en la Tarea 8 funcionó el Paths dentro de una herramienta y «Resultado para el agente» admite llegar desde las dos ramas; si no, queda apuntada en `pendientes.md` y la cadena sigue como en la v12.
- [ ] **Paso 3:** `test_node` de las dos cadenas MCP solo con los datos inventados de las restricciones globales → `enviar_correo_contrasena` devuelve `no_coincide` y `pista_correo` devuelve `no_verificado`. Ninguna otra prueba de MCP en esta tarea.
- [ ] **Paso 4: Evals.** Copiar de «Prolongacion» (v12) las carpetas Prolongación base, Devolver tarde y precio, La web no le deja, Aseguradora y empresa, Correo de contraseña (v12), Cierre, Idiomas, Escalado y transferencias, Casos aprendidos y bordes, y HOR-*, FDS-01, FDS-04 a FDS-07. Adaptar como en la Tarea 9; ESC-04 (minibús) pasa a esperar `volver_al_triaje`; PROL-03, PROL-04, ASEG-06, WEB-08 y WEB-09 esperan la oferta del correo (como en la v12); ASEG-01 y ASEG-03 esperan la resolución del equipo (primero la aseguradora). Crear:

| Eval | Conversación | Esperado |
|---|---|---|
| PISTA-01 | No sabe con qué correo está el alquiler; da número de reserva, nombre y fecha | `pista_correo` con los tres datos |
| PISTA-02 | `pista_correo` devuelve `verificado`, dominio `gmail.com` | Dice «es una dirección de gmail» y pide el correo; no dice nada más de la reserva |
| PISTA-03 | `pista_correo` devuelve `no_verificado` | No dice qué dato falla; ofrece repetir una vez o el plan B |
| PISTA-04 | Tras PISTA-02 dicta el correo y lo confirma | `enviar_correo_contrasena` con ese correo |
| NOINI-P1 | «Mi reserva es para el mes que viene y no tengo contraseña para cambiarla» | Plan B de «¿Has olvidado tu contraseña?», sin ofrecer el envío y sin transferir |
| BR-P1 | Tras dar los pasos, «¿y la fianza cuándo me la devuelven?» | `buscar_respuesta` tema `cargos_y_reembolsos`, sin salir del módulo |
| GC-P1 | Gestión cerrada; `enviar_correo_contrasena` → `no_coincide` | No transfiere ni lo anuncia (como CORREO-11) |

- [ ] **Paso 5:** ejecutar el juego 3 veces; criterio de §7.3. Apuntar en el informe de evals.
- [ ] **Paso 6:** guardar copias y commit (`Atención España v2: módulo Prolongación con correo de contraseña y pista del dominio`).

### Tarea 11: Punto de encuentro e Información de oficina

**Ficheros:**
- Crear: `casos/atencion-es/prompts/atencion-es/v2/punto-de-encuentro.md`, `informacion-de-oficina.md`

**Interfaces:**
- Consume: Tareas 7 y 8.

- [ ] **Paso 1:** en los dos prompts de la v1, sustituir sus secciones de idioma, voz, identidad, modo de atención y Gestión cerrada por el bloque de reglas comunes; añadir a Punto de encuentro las LISTAS 1 a 4 de `nocturno_*` y el PASO 2–3 del Triaje de la v25 (oficina de aeropuerto cerrada); quitar «OTRAS PREGUNTAS DEL ALQUILER» de los dos (va por `consultas_alquiler`). No cambiar puntos de encuentro, oficinas ni horarios. `comprobar_prompts.py v2` sin fallos.
- [ ] **Paso 2:** subir los prompts (modelos sin cambios) y cambiar sus `transfer_to_human_agent` al patrón de la Tarea 8.
- [ ] **Paso 3: Evals.** Copiar las de los dos nodos de la v1 (adaptando la cola) y crear: PE-NOCT-1 (Atenas a las 23:30 hora local → aviso de cierre, sin punto), PE-NOCT-2 (Málaga a las 10:00 → da el punto), GC-PE1 y GC-IO1 (Gestión cerrada, «¿me cambian la hora de devolución?» → no transfiere), VIRT-PE1 (modo virtual, queja del minibús → no transfiere; volver a llamar a partir de las ocho).
- [ ] **Paso 4:** ejecutar 3 veces; criterio de §7.3; informe de evals. Commit (`Atención España v2: Punto de encuentro e Información de oficina con reglas comunes`).

### Tarea 12: Saltos entre módulos

**Ficheros:**
- Crear: `casos/atencion-es/prompts/atencion-es/v2/saltos.md` (herramientas de salto y Module Change, con origen y destino)

**Interfaces:**
- Consume: los cinco módulos.
- Produce: estas herramientas de salto (todas `message: none`, parámetro obligatorio `motivo` y los de la v25 donde existan):

| # | En el módulo | Herramienta | Destino | Hijo |
|---|---|---|---|---|
| 1 | Punto de encuentro | `volver_al_triaje` | Triaje | Module Change nuevo |
| 2 | Información de oficina | `volver_al_triaje` | Triaje | Module Change nuevo |
| 3 | Prolongación | `volver_al_triaje` | Triaje | Module Change nuevo |
| 4 | Consultas | `volver_al_triaje` | Triaje | Module Change nuevo |
| 5 | Punto de encuentro | `informacion_oficina` | Información de oficina | Module Change nuevo |
| 6 | Información de oficina | `buscar_punto_de_encuentro` | Punto de encuentro | Module Change nuevo |
| 7 | Consultas | `prolongar_alquiler` | Prolongación | Module Change nuevo |
| 8 | Prolongación | `informacion_oficina` | Información de oficina | Module Change nuevo |
| — | Punto de encuentro, Información de oficina | `consultas_alquiler` | Consultas | Module Change (existe) |
| — | Consultas | `buscar_punto_de_encuentro`, `informacion_oficina` | Punto de encuentro, Oficina | Module Change (existe) |

- [ ] **Paso 1:** crear por API las 8 herramientas nuevas sin hijo y escribir `saltos.md`.
- [ ] **Paso 2: Pedir al responsable** que cree en el editor los 8 Module Change (la tabla, filas 1 a 8) y esperar a que confirme.
- [ ] **Paso 3: Comprobaciones §11.2 y §11.3:** `get_workflows` → los 12 Module Change apuntan donde dice la tabla; en una llamada de prueba por web, Consultas → `volver_al_triaje` → Triaje no saluda y encamina con lo ya dicho, y un salto a Prolongación sigue en inglés si se hablaba inglés. Si el Module Change no puede volver al Triaje, sustituir las filas 1 a 4 por atajos directos al resto de módulos (añade 3 Module Change) y apuntarlo en el spec y en `pendientes.md`.
- [ ] **Paso 4: Evals** (carpeta «Bot único · Saltos»): para cada fila de la tabla, dos evals en el módulo de origen que esperan esa herramienta (p. ej. SALTO-05a «Y la oficina de Málaga, ¿a qué hora cierra?» en Punto de encuentro → `informacion_oficina`); SALTO-ENTRADA en cada módulo destino (la conversación trae el salto en el historial: no saluda, no repite preguntas y contesta a lo último pedido); SALTO-PING (historial con dos saltos y el cliente pide otra cosa que no se resuelve → transfiere con la `cola` que toque o, con Gestión cerrada, da el horario y cierra); SALTO-IDIOMA (historial en inglés → sigue en inglés).
- [ ] **Paso 5:** ejecutar 3 veces; criterio de §7.3 (SALTO-PING es crítica). Commit (`Atención España v2: saltos entre módulos`).

### Tarea 13: Extract único, rama de WhatsApp y agente

**Ficheros:**
- Crear: `casos/atencion-es/prompts/atencion-es/v2/registrar-resultado.md`, `receive-customer-call.md`

**Interfaces:**
- Consume: todas las herramientas de las Tareas 8 a 12.
- Produce: «Registrar resultado de la llamada» con los campos de §5.12 (nombres y valores exactos de la tabla del spec), que leen la rutina y `medir_bots.py`.

- [ ] **Paso 1:** reescribir el prompt y los campos de «Registrar resultado de la llamada»: entradas = transcripción + parámetros y salidas de todas las herramientas de todos los módulos + `opcion_menu`, `idioma`, `modo_virtual`, `gestion_abierta`, `festivo_nacional` de «Contexto de la llamada»; evalúa solo los turnos del bot anteriores a la transferencia; la penalización de 50 €/día, las tarifas generales y los teléfonos de Benidorm y Torrevieja no son fallos.
- [ ] **Paso 2:** borrar «Registrar consultas del alquiler» y cambiar las entradas de «Preparar WhatsApp minibús» a `{{<registrar>.response.whatsapp_aceptado}}`, `…punto_whatsapp` y `…idioma_cliente`.
- [ ] **Paso 3:** en «Receive Customer Call», ampliar `transcription_context` a prolongaciones, contraseña, correo electrónico y número de reserva; una sola voz («Pablo Galvez HR»).
- [ ] **Paso 4:** `fix_broken_vars` (`dry_run: true`, luego sin él) → 0 variables rotas. `test_node` del extract con la transcripción de una de las llamadas de prueba de la Tarea 8 → todos los campos con un valor permitido.
- [ ] **Paso 5:** guardar copias y commit (`Atención España v2: extract único y rama de WhatsApp`).

---

## Fase D · Medición

### Tarea 14: `medir_bots.py`

**Ficheros:**
- Crear: `scripts/medir_bots.py`
- Crear: `scripts/test_medir_bots.py`

**Interfaces:**
- Consume: `gestion_abierta_en` y `modo_virtual_en` de `casos/atencion-es/codigo/contexto_llamada.py` (import por ruta).
- Produce: `python3 -I scripts/medir_bots.py <llamadas.json> [--fin AAAA-MM-DDTHH:MM:SSZ]`, que imprime una tabla y escribe `<llamadas>.indicadores.json`. `llamadas.json` es una lista de `{"run_id", "workflow" ("atencion" | "prolongaciones" | "minibus"), "version", "inicio" (ISO UTC), "from_hash" (10 caracteres o ""), "opcion_menu", "turnos_cliente", "transferencias": [{"cola", "ts", "error"}], "llego_agente" (bool o null), "creditos" (número o null), "saltos", "duracion_s", "motivo"}`. Funciones: `franja(inicio_utc: datetime) -> str` (`gestion_abierta` | `gestion_cerrada` | `modo_virtual`), `rellamadas(llamadas: list) -> set[str]` (run_id con otra llamada del mismo `from_hash` en las 48 h siguientes, en cualquier workflow), `resuelta(llamada, rellamadas) -> bool` (sin transferencias, `turnos_cliente >= 2`, sin rellamada), `indicadores(llamadas, fin: datetime) -> dict` por `(workflow, opcion_menu)` y por franja: `llamadas`, `resolucion_real`, `pct_transferidas`, `pct_llegan_agente`, `rellamadas_48h`, `creditos_llamada`, `creditos_resuelta`, `pct_3_saltos`, `cortes_600`, `duracion_media`.

- [ ] **Paso 1: Pruebas que fallan:** rellamada a las 47 h cuenta y a las 49 h no; `from_hash ""` nunca es rellamada; una llamada con un intento de transferencia fallido no es resuelta; 1 turno del cliente no es resuelta; las llamadas de las últimas 48 h antes de `fin` no entran en `resolucion_real` (sí en el resto); `creditos_resuelta` = suma de créditos / resueltas, y `null` si falta algún dato de créditos; `franja` de un martes a las 21:30 hora de Madrid es `gestion_cerrada` y a las 22:30 `modo_virtual`; el 8/12/2026 a las 10:00, `gestion_cerrada`.
- [ ] **Paso 2: Ejecutar y ver que fallan.** `python3 -I scripts/test_medir_bots.py`
- [ ] **Paso 3: Implementar.**
- [ ] **Paso 4: Ejecutar y ver que pasan.**
- [ ] **Paso 5: Commit** (`Scripts: medición común de los bots (resolución real y créditos por llamada resuelta)`).

### Tarea 15: Créditos por llamada, rutina diaria y artefacto

**Ficheros:**
- Crear: `scripts/creditos_runs.py`
- Crear: `casos/atencion-es/rutinas/informe-atencion-es.md`

**Interfaces:**
- Consume: Tareas 13 y 14.
- Produce: `python3 -I scripts/creditos_runs.py <run_ids.txt>` → JSON `{run_id: creditos}` usando `GET /billing/usage/runs/{run_id}` con la clave de la variable de entorno `HAPPYROBOT_API_KEY` (nunca en el repo); la rutina diaria del workflow nuevo y el artefacto «Calidad Atención España» (colección `informes`, doc_id = AAAA-MM-DD).

- [ ] **Paso 1:** averiguar la URL base y la cabecera de autenticación de la API (documentación con acceso o el informe del 18/10) y probar `creditos_runs.py` con 3 runs de Prolongaciones V11. Si falla, el campo `creditos` va a `null` y se apunta en `pendientes.md`; el resto de la medición sigue.
- [ ] **Paso 2:** escribir `informe-atencion-es.md` siguiendo la estructura de `casos/prolongaciones/rutinas/informe-prolongaciones.md`: listar runs del día del workflow nuevo y de los dos actuales (IDs con python), outputs por run en subagentes de unos 23 runs, teléfonos solo en hash, `llamadas.json` en `datos/`, `medir_bots.py`, emparejamiento con RingCentral, auditoría de 30 llamadas a la semana (los lunes) y escritura en el artefacto.
- [ ] **Paso 3:** crear el artefacto (cargar antes las skills `artifact-design` y `artifact-capabilities`; colección `informes` con la capacidad de base de datos) con: tabla diaria por línea y franja, comparación con los bots actuales y el estado de las puertas de §8.4.
- [ ] **Paso 4:** ejecutar la rutina a mano sobre los runs de prueba (web) de la v2 y sobre un día de V11 y de Minibús ES → el artefacto muestra los tres. Commit (`Atención España: créditos por run, rutina diaria y artefacto de calidad`).

---

## Fase E · Puerta 0

### Tarea 16: Pasada completa de evals

**Ficheros:**
- Modificar: `casos/atencion-es/docs/informes/evals-v2.md`

- [ ] **Paso 1:** ejecutar todas las evals de los cinco nodos 3 veces con la `version_id` de la v2.
- [ ] **Paso 2:** tabla por nodo y carpeta (pasadas / ejecuciones), lista de críticas y de fallos con el motivo del juez. Criterio de la puerta 0: críticas 3/3, resto ≥ 90 %. Si no se cumple, volver a la tarea del módulo, corregir el prompt en el repo, subirlo y repetir.
- [ ] **Paso 3:** `python3 -I casos/atencion-es/codigo/comprobar_prompts.py v2` y todas las pruebas de `casos/atencion-es/codigo/` y `scripts/test_medir_bots.py` sin fallos. Commit (`Atención España v2: evals en verde`).

### Tarea 17: Llamadas de prueba y comprobaciones con personas

**Ficheros:**
- Crear: `casos/atencion-es/pruebas/guion-llamadas.md`
- Modificar: `casos/atencion-es/docs/informes/evals-v2.md`, `casos/atencion-es/docs/pendientes.md`

- [ ] **Paso 1:** escribir el guion de 25 llamadas de §8.4 (prolongar con y sin cuenta; correo enviado y no coincide; pista del dominio; cada salto de la tabla de la Tarea 12 de ida y vuelta; Gestión cerrada llamando fuera de horario; modo virtual; avería; reserva nueva; inglés, italiano y francés), con `OPCION_PRUEBA` en cada una.
- [ ] **Paso 2: Con el responsable:** si las llamadas web lo exigen, que publique la v2 en *development*. Hacer las 25 llamadas (las hace una persona; el agente prepara el guion y analiza los runs) y anotar por llamada: resultado, fallos, créditos (`creditos_runs.py`).
- [ ] **Paso 3: Con el responsable:** caso «coincide» del correo y `pista_correo` con una reserva real en curso y un correo que alguien del equipo pueda abrir (confirmar qué trae el correo). Sin datos de la reserva en el repo.
- [ ] **Paso 4: Comprobaciones §11.5, §11.8 y §11.9** (solo lectura en RingCentral y en HappyRobot): duración facturada tras transferir con y sin whisper; horario real de 18056 y 18001 de noche; cómo se mueve una línea (preguntar a HappyRobot o probarlo con la línea «Test SIP RingCentral» y un workflow de pruebas, nunca con líneas de producción).
- [ ] **Paso 5:** puerta 0 punto por punto en el informe (evals, llamadas, «coincide», créditos ≤ 80 en llamadas de prolongación, medición). Commit (`Atención España v2: llamadas de prueba y comprobaciones de la puerta 0`).

### Tarea 18: Ensayo del movimiento de líneas, documentación y PR

**Ficheros:**
- Crear: `casos/atencion-es/docs/procedimiento-lineas.md`
- Modificar: `casos/atencion-es/docs/workflows.md`, `casos/atencion-es/CLAUDE.md`, `casos/atencion-es/docs/decisiones.md`, `docs/extensiones.md`, `casos/minibus/docs/pendientes.md`, `casos/prolongaciones/docs/pendientes.md`

- [ ] **Paso 1:** escribir `procedimiento-lineas.md`: pasos exactos para conectar Prolongación (fase 1) y Minibús ES (fase 2) y para volver atrás, según lo comprobado en la Tarea 17; quién lo hace; qué versión antigua se republica; cómo se comprueba que la primera llamada entra por el workflow nuevo.
- [ ] **Paso 2: Con el responsable:** ensayo de ida y vuelta con la línea «Test SIP RingCentral» siguiendo el procedimiento; cronometrar la vuelta (objetivo < 30 min).
- [ ] **Paso 3:** completar `workflows.md` (flujo, nodos con persistent ID, herramientas, extract, tabla de versiones), `CLAUDE.md` del caso (ids y estado), D-001 (estado «construida en v2, sin publicar»), `docs/extensiones.md` (columna «También la usa»: Atención España en 18057, 18061, 18001, 18006, 18034, 18035, 18056 y 18059) y una línea en los pendientes de Minibús y Prolongaciones que enlace la fase en que dejarán de recibir sus líneas.
- [ ] **Paso 4:** commit (`Atención España v2: procedimiento de líneas y documentación`) y PR a `main` con: ticket/decisiones (C-004, D-001), resumen y riesgos, impacto (workflow nuevo sin publicar; ningún workflow actual tocado), pruebas ejecutadas (evals, pruebas locales, llamadas) y lo que falta para publicar (puerta 0 pendiente si queda algo).
