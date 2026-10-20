# Decisiones comunes a todos los casos

Decisiones que afectan a más de un caso (colas, extensiones, forma de trabajar). Las de un solo
caso van en `casos/<caso>/docs/decisiones.md`. Numeración `C-NNN`, la más reciente arriba.

Plantilla:

```
## C-NNN · AAAA-MM-DD · Título corto
- **Qué:** …
- **Por qué:** … (datos: run_id, cifras, llamadas de ejemplo)
- **Afecta a:** casos y workflows
- **Quién:** persona(s)
- **Estado:** propuesta | aprobada | aplicada | descartada
```

---

## C-006 · 2026-10-20 · Bloque de consultas: cinco párrafos ajustados por las evals del bot único (Tarea 16)
- **Qué:** cambios en `comun/bloques/consultas-alquiler.md` (y en el `buscar_respuesta` generado de los dos nodos del
  bot único):
  - **Mañana (ronda de la pasada, D-015 del caso):** vuelo retrasado (explicar el servicio de espera aunque pregunte
    hasta qué hora abre, sin pedir el aeropuerto); otra oficina (decir las tres cosas: se indica al reservar, el precio
    depende del trayecto y, en curso, el recargo se paga en la oficina de devolución); reclamar un cargo con Gestión
    cerrada (decir que está cerrada y su horario); contrato vencido («dilo entero, con la cifra»).
  - **Oficina cerrada, reescrito en la ronda de arreglos 1 de la revisión:** sale «Se acuerda al recoger el coche» y la
    condición «si no lo acordó»; entra «En su oficina le dicen si lo permite; si quiere que lo revisen en su caso,
    GESTIÓN DE RESERVA». El aviso de gastos y daños queda como dato (sin «siempre»). Se mantiene la cláusula de
    Gestión cerrada (no decir que un compañero lo revisará: horario de Gestión). Adenda a C-005, punto 3: el «se acuerda
    al recoger» de C-005 deja de estar en el texto.
- **Por qué:** DEVOL-03a y DEVOL-03c (críticas): con «se acuerda al recoger» el bot decía «solo si lo acordó» y ofrecía
  un compañero; con «Dile siempre» el aviso de daños no mejoraba y DEVOL-03a bajó de 2/3 a 0/3. FDS-02, DEVOL-02,
  HOR-C1, CARGO-04 y TARDE-05 por los otros párrafos. Resultados en
  `casos/atencion-es/docs/informes/evals-v2.md` («Tarea 16»).
- **Afecta a:** los bots que usen el bloque: hoy, solo el bot único de Atención España (Consultas y Prolongación).
- **Quién:** el agente de la Tarea 16 a propuesta de la revisión (ronda de arreglos 1), 20/10/2026.
- **Ronda de arreglos 2 (re-revisión, 20/10/2026):** «algunas tienen buzón de llaves y otras no lo permiten» pasa a
  «algunas tienen buzón de llaves; depende de la oficina»; en RECOGER TARDE, «Su vuelo llega…» y «Su tren llega tarde…»
  van delante de «Llega de noche o con la oficina cerrada», y el párrafo del vuelo añade «Con Gestión cerrada, no
  ofrezcas pasarle: dile que Gestión está cerrada y su horario» (FDS-02). DEVOL-03a y DEVOL-03c se reescribieron con
  este texto (sin «se acuerda al recoger»; aviso de daños opcional en las dos; la 03c con un turno en el que pide que
  se lo miren).
- **Estado:** aplicada en el bloque y en Atención España v2.

## C-005 · 2026-10-18 · Bloque de consultas: fuera los teléfonos de asistencia de otros países y la oficina cerrada «depende de la oficina»
- **Qué:** dos decisiones sobre `comun/bloques/consultas-alquiler.md` («Qué falta decidir», puntos 7 y 3):
  - **Punto 7:** se quitan del bloque los teléfonos de asistencia en carretera de Portugal, Italia y Grecia hasta que
    negocio valide los números; vuelven cuando estén validados. Siguen por decidir los de reservas nuevas en otros
    países y el correo y el teléfono del departamento de flotas. En su lugar, la sección dice que el bot no tiene esos
    teléfonos y que no diga que el de España sirve allí (añadido en la Tarea 9b al ver que el bot lo decía); el bloque
    de reglas comunes dice además «Asistencia en carretera en España» (R30). **Pendiente de validar con negocio:**
    «remítele a centauro punto net» para la asistencia de otros países.
  - **Punto 3 (resuelto):** devolver con la oficina cerrada «depende de la oficina; se acuerda al recoger el coche»,
    como dice el bloque. El bot nunca dice que no está permitido ni cita la norma de Minibús v25 («por norma, fuera
    del horario no se puede»); si no lo acordó al recoger, se transfiere a Gestión, y con Gestión cerrada se da su
    horario. Se añade al texto «No digas que no está permitido ni que solo se puede si lo acordó: depende de la
    oficina».
- **Por qué:** en el bot único (Atención España v2, ronda 4 de evals) el bot de Consultas daba el número de Portugal
  que traía la sección aunque el prompt solo permite cuatro teléfonos (TEL-C1 0/3), y con Gestión cerrada inventaba
  que no está permitido dejar el coche fuera (DEVOL-03c 0/3). Dar un número sin validar (el de Grecia tenía una
  errata) es peor que remitir a la web.
- **Afecta a:** los bots que usen el bloque: hoy, el bot único de Atención España (`buscar_respuesta`, generado del
  bloque; Consultas del alquiler y, desde la Tarea 10, Prolongación). Prolongaciones V11 y Minibús ES v25 no cambian.
- **Quién:** jzerpa (responsable), 18/10/2026.
- **Estado:** aplicada en el bloque y en Atención España v2 (`casos/atencion-es/docs/informes/evals-v2.md`, ronda 5).

## C-004 · 2026-10-18 · Bot único de atención de España en un workflow nuevo, al que migran las opciones del menú
- **Qué:** se crea «Centauro Atención España», un workflow nuevo duplicando Minibús ES v25, con un Triaje corto y
  módulos especialistas (caso `casos/atencion-es/`, spec y D-001 allí). Las opciones del menú pasan a él una a una
  moviendo su línea al workflow nuevo al pasar a producción: primero Prolongación, después Minibús ES; más
  adelante, por decidir,
  Gestión cuando está cerrada, el triaje de Nueva Reserva y Gestión en horario. Los workflows de Minibús ES y de
  Prolongaciones siguen publicados, sin tocar, como control y vuelta atrás.
- **Por qué:**
  - el diseño marca el coste: 118 créditos por llamada en Prolongaciones V11 frente a 64 en Minibús v25;
  - un workflow nuevo permite conectar y deshacer cada opción por separado, tener datos limpios (tabla de Twin,
    extract y rutina propios) sin cambiar el esquema de los bots actuales, y no choca con el experimento de la
    v25 (solo puede haber uno activo por workflow);
  - descartado el fork de Minibús v25: mezclaría las llamadas de Prolongación en la tabla y la rutina de Minibús,
    y su ventaja (un experimento de HappyRobot contra los bots actuales) solo valdría para la línea de Minibús.
- **Afecta a:** Minibús ES (`casos/minibus/`) y Prolongaciones (`casos/prolongaciones/`), que dejarán de recibir
  esas opciones cuando se conecten; las colas de `docs/extensiones.md` no cambian.
- **Quién:** jzerpa.
- **Estado:** aprobada (workflow nuevo); spec en revisión.

## C-003 · 2026-10-11 · Un solo repo para todos los casos de HappyRobot, con una carpeta por caso
- **Qué:** el repo `centauro-happyrobot` reúne todos los casos de uso de Centauro en HappyRobot.
  Lo común (colas, reglas de transferencia, scripts, convenciones) está en la raíz; cada caso
  tiene su carpeta en `casos/`. Sustituye a la D-008 de Minibús, que hacía un repo solo para
  Minibús.
- **Por qué:**
  - los casos comparten colas de RingCentral (Minibús España y Prolongaciones usan 18057, 18061,
    18001, 18006 y 18034), la extensión de salida y el workspace de HappyRobot;
  - las decisiones comunes se escriben una sola vez;
  - Claude Code lee el `CLAUDE.md` común y el del caso.
  - Se harían repos separados solo si un caso lo lleva otro equipo con otros permisos, si tiene
    código propio desplegable o si se entrega a un tercero.
- **Afecta a:** todos los casos.
- **Quién:** jzerpa.
- **Estado:** aplicada.

## C-002 · antes del 10/10/2026 · Los análisis de llamadas son de solo lectura
- **Qué:** las rutinas y los análisis no modifican workflows ni runs (no cancelan, marcan ni
  lanzan) y no escriben en RingCentral. Solo escriben en sus propios informes (p. ej. la colección
  `informes` del artefacto de Minibús).
- **Por qué:** evitar cambios en producción sin revisión humana.
- **Afecta a:** todos los casos (definida en Minibús como D-001).
- **Estado:** aplicada.

## C-001 · 2026-10-10 · Las extensiones 2114, 2115 y 2119 no pueden ser destino de transferencia
- **Qué:** ningún workflow debe transferir a 2114, 2115 (asistencia en carretera ES/EN) ni a 2119
  («RA IT-EN-OPCIONES»). Las averías y los accidentes van a la cola de agentes de asistencia (en
  España, 18034).
- **Por qué:** son menús automáticos, no agentes.
  - 09/10: 3 averías de Minibús ES perdidas (v17 y v18).
  - 10/10: una avería a la 2115 (Minibús ES v19, `c6ffa5b5`) y otra a la 2119 (Minibús IT v2,
    `7463c774`).
- **Afecta a:** todos los workflows que transfieren averías. Confirmado en Minibús ES e IT.
  Prolongaciones, revisado el 11/10/2026: la V6 mandaba las averías a 2114/2115; desde la V7 van a
  18034/18035 y la V11 no usa ninguna de las tres. Falta revisar Reembolsos.
- **Quién:** pendiente.
- **Estado:** propuesta (antes era la D-005 de Minibús).
