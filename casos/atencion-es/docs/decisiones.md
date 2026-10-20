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

## D-016 · 2026-10-20 · Créditos por llamada: solo el total, sin desglose (desviación del spec §6, pendiente)
- **Qué:** el spec §6 pide los créditos por llamada separados en LLM por módulo y voz (bot hablando / escuchando al
  agente). `scripts/creditos_runs.py` solo da el total por run (`GET /billing/usage/runs/{run_id}`) y `medir_bots.py`
  solo usa ese total. Queda registrado como **desviación pendiente**: no se hace en esta rama.
- **Por qué:** los indicadores principales del spec (créditos por llamada y por llamada resuelta) solo necesitan el
  total, y el desglose depende de la forma de la respuesta de facturación, que no se ha visto con partidas. El
  desglose por módulo sirve para ver dónde se va el coste (Prolongación es el único módulo que razona).
- **Qué falta:** leer las partidas de la respuesta (módulo y voz) en `creditos_runs.py` con una prueba sobre una
  respuesta real, y sacarlas en `medir_bots.py` y en el informe. Antes de la puerta 0 no es bloqueante; sí lo es si la
  puerta de coste se discute por módulo.
- **Afecta a:** `scripts/creditos_runs.py`, `scripts/medir_bots.py`, `rutinas/informe-atencion-es.md`.
- **Quién:** jzerpa (por decidir cuándo).
- **Estado:** propuesta (desviación pendiente).

## D-015 · 2026-10-20 · Ronda de arreglos de la pasada completa (Tarea 16)
- **Qué:** una ronda por módulo tras la pasada completa de evals (R45, paso 4). Triaje: sin cambios. Punto de
  encuentro: regla de orden en la descripción de `consultas_alquiler`, la frase de la devolución en el aeropuerto y
  «Solo eso…» en el falso punto de Sevilla. Información de oficina: «Di esa pregunta tal cual…». Prolongación y
  Consultas, fuera del prompt (están a 21.994/22.000 y 7.988/8.000): cinco párrafos del bloque
  `comun/bloques/consultas-alquiler.md` (oficina cerrada, vuelo retrasado, otra oficina, reclamar un cargo con Gestión
  cerrada y contrato vencido), con el código de `buscar_respuesta` regenerado y pegado en los dos nodos, y la
  descripción de `pista_correo` (enviar sin volver a pedir el nombre ni la fecha).
- **Por qué:** fallos de la pasada (HOR-C1, CARGO-04, DEVOL-03c, FDS-02, DEVOL-02, TARDE-05, PISTA-04; PE-NOCT-3,
  PE-EST-2). Medido repitiendo solo las tocadas ×3: arreglan HOR-C1 (1/3 → 3/3), CARGO-04 (2/3 → 3/3) y PE-EST-2
  (0/3 → 3/3); mejora poco TARDE-05 (0/3 → 1/3); DEVOL-03c sigue 0/3 (el «passed» del run 3da6cdb2 tenía un razonamiento de fallo y no cuenta); no cambian FDS-02, DEVOL-02, PISTA-04 ni PE-NOCT-3;
  empeora DEVOL-03a (2/3 → 0/3) y quizá PE-NOCT-1 (3/3 → 1/3). Detalle en `informes/evals-v2.md` («Tarea 16»).
- **Afecta a:** v2 (nodos «Buscar respuesta» de Consultas y Prolongación, herramienta `pista_correo`, prompts de Punto
  de encuentro e Información de oficina). El bloque de consultas es común: cualquier bot que lo use recibe el cambio.
- **Quién:** el agente de la Tarea 16, dentro del límite de una ronda por módulo (R45).
- **Edición de evals de la ronda (06:49):** ADV-8 pasa a permitir `estado_oficina` antes (obligatoria por R39, no
  cuenta como primera llamada) y a pedir el orden «primero el punto, después `consultas_alquiler`»; también se
  reescribieron SALTO-ENTRADA-PE, SALTO-05a y «ES · cómo llegar a Sants» (mismo motivo).
- **Ronda de arreglos 1 de la revisión (20/10/2026):** se deshace la regla de ORDEN de PE-NOCT-3 en la descripción de
  `consultas_alquiler` de Punto de encuentro (queda solo lo de ADV-10); «Con la oficina cerrada» del bloque reescrito
  (C-006 en `docs/decisiones.md`); en `buscar_respuesta` de Consultas, `tema`: «vuelo o tren retrasado, aunque
  pregunte hasta qué hora abre la oficina → recoger_tarde, antes de responder» (FDS-02); en `enviar_correo_contrasena`,
  `nombre_completo` y `fecha_nacimiento`: «si ya los dio para pista_correo, úsalos; no los pidas» (PISTA-04); GC-IO1
  aclara en la conversación que quiere devolverlo más tarde; Prolongación (R47) pasa a `buscar_respuesta` «Prolongar en
  una oficina», «Precio caro», «Cualquier otra pregunta», «Cuántos días» (aseguradora) y «Coche de empresa», con un
  puntero de una línea, y con el sitio libre refuerza PROL-05 y PROL-06 (no volver a preguntar por la cuenta).
  Resultado en `informes/evals-v2.md` («Ronda de arreglos 1 de la revisión»).
- **Ronda de arreglos 2 (re-revisión, 20/10/2026):** R47 deshecho en parte: «Precio caro» vuelve literal a DETALLES QUE
  PUEDES DAR y sale del puntero; fuera el refuerzo de EXPLICACIÓN. PROL-05 en la frase final de «Si dice que no»
  («si lo pregunta cuando ya iba a entrar, en ese turno los pasos y "¿Alguna duda?"»); PISTA-04 en ENVÍO DEL CORREO
  («si los dio en PISTA, no faltan»); PROL-06 sin cambio (en la eval el cliente no había contestado lo de la cuenta).
  Bloque (C-006): oficina cerrada «depende de la oficina» y RECOGER TARDE con el vuelo delante y Gestión cerrada.
  DEVOL-03a y DEVOL-03c reescritas. Prolongación: 21.147 caracteres. Resultado en `informes/evals-v2.md`
  («Ronda de arreglos 2 de la re-revisión»).
- **Ronda de arreglos 3 (20/10/2026):** FDS-02 era de enrutado («hasta qué hora abre» llevaba a `informacion_oficina`):
  la descripción de `buscar_respuesta` de Consultas añade «salvo vuelo o tren retrasado: recoger_tarde, aunque
  pregunte el horario» y, como el prompt de Consultas no tiene sitio (7.988/8.000), la de `informacion_oficina` de
  Consultas añade «No la uses si su vuelo o tren llega tarde: buscar_respuesta recoger_tarde». En la eval FDS-02 se
  cambia el resultado de `buscar_respuesta` que traía la conversación (texto viejo de la sección) por el actual.
  WEB-03: en LA WEB NO LE DEJA de Prolongación, la oferta pasa a pregunta («¿Prefiere que un compañero se la
  prepare?»; 21.165 caracteres). TARDE-02: la eval acepta lo que dice DEVOLVER TARDE (cortesía, periodos,
  penalización) y la pregunta final es opcional; el prompt no cambia. Resultado y bloqueos clasificados en
  `informes/evals-v2.md` («Ronda de arreglos 3»).
- **Ronda de arreglos 4 (20/10/2026):** FDS-02 no mide el enrutado (trae sembrada la llamada a `buscar_respuesta`); se
  quita «enrutado arreglado» y se crea FDS-02r (crítica: solo el turno del cliente, Gestión cerrada, espera
  `buscar_respuesta` recoger_tarde; 3/3). Bloque (C-006): «No añadas otras vías de contacto ni condiciones que no estén
  aquí» en el vuelo retrasado, «Solo si el cliente pide que lo revisen…; no se lo ofrezcas tú» en la oficina cerrada y
  la oferta de LA WEB NO LE DEJA como pregunta; regenerado y pegado en los dos «Buscar respuesta». Prompt de Consultas
  sin tocar («si necesita que alguien lo mire» de ESCALADO queda como propuesta: cambiarlo obliga a repetir todas las
  evals de Consultas). Evals: DEVOL-03a con el texto nuevo, DEVOL-03b reescrita (el cliente lo pide; ya no hay oferta
  que aceptar), WEB-05 y WEB-08 con la pregunta final opcional. Resultado en `informes/evals-v2.md` («Ronda de
  arreglos 4»): críticas de Consultas 58/69 (FDS-02r 3/3; FDS-02 0/3, TEL-C1 0/3, DEVOL-03a 1/3, CARGO-05 1/3,
  DEVOL-03c 2/3); Prolongación, resto 92,7 %.
- **Estado:** aplicada en v2.

## D-014 · 2026-10-20 · `estado_oficina` con la hora del momento y aviso de transferencia según la cola (R45)
- **Qué:** los dos Importantes de la revisión de la Tarea 15b, hechos al empezar la Tarea 16.
  1. **`estado_oficina`** calcula con la hora del momento en que se ejecuta (como «Preparar transferencia», D-004), no
     con las `nocturno_*` del principio de la llamada, y con el horario concreto de cada oficina que ya dice el prompt
     (hora local: de 7:00 a 23:00; Murcia de 8:00 a 22:00; Alicante de 7:00 a 23:30; Bari, Florencia, Nápoles y Venecia
     de 8:00 a 23:00). Nueva variable del workflow `HORA_PRUEBA` (`ninguna` en los tres entornos): si una eval la pone
     a `HH:MM` (hora peninsular), manda sobre el reloj. Las `nocturno_*` dejan de ser entradas del nodo.
  2. **Aviso de `transfer_to_human_agent` en Prolongación y Consultas:** sustituye la regla de D-013 («Gestión ahora
     false → neutro»). Ahora el aviso depende de la cola: neutro («Un momento, por favor, no cuelgue») solo si la
     transferencia puede no salir (cola `gestion` con Gestión cerrada, o una cola que no sea `asistencia` en modo
     virtual); en los demás casos, y siempre con `asistencia`, el de siempre («le paso con un compañero…, no
     cuelgue»). La descripción lleva las variables `gestion_abierta` y `modo_virtual`. El Triaje sigue con el de
     siempre (no cambia: con el aviso neutro VIRT-T1 transfería más, D-013).
- **Por qué:** con las `nocturno_*` una llamada que empieza a las 22:58 y pide el punto a las 23:02 lo recibía, y la
  herramienta se contradecía con el prompt (Bari a las 7:30 «abierta» y «abre a las ocho»; Alicante «cerrada» a las
  23:15). Con D-013, una avería de noche oía «un momento» aunque la cola de asistencia funciona siempre.
  Medido (20/10/2026): pruebas locales 239/239 (`test_estado_oficina.py`, con RED previo de 38 fallos); PE-NOCT-1, 2,
  3c, 4 (Sevilla, control nuevo) y 5 (Alicante 23:15, control nuevo) 3/3; PE-EST-1 y 3 3/3; con `HORA_PRUEBA` 10:00,
  SALTO-ENTRADA-PE dio el punto a las 06:28 (por el reloj, cerrada). Aviso: RED R34-P1 0/3 y R34-C1 2/3 (avería de
  noche, esperando el aviso de siempre); GREEN R34-P1 3/3, R34-C1 2/3 (la que falla, por el reintento, error del juez),
  R34-P2 3/3, R34-T1 3/3 y las nuevas R34-P3 y R34-C3 (Gestión cerrada, pide que alguien mire su reserva: sin «le
  paso») 3/3. Detalle en `informes/evals-v2.md` («Tarea 16»).
  Nota (revisión de la Tarea 16): PE-NOCT-1 a 5 miden al modelo con el resultado de `estado_oficina` ya escrito en la
  conversación de la eval; el código lo cubren las pruebas locales y SALTO-ENTRADA-PE, que ejecuta la herramienta de verdad.
- **Afecta a:** v2 (nodo «Estado de la oficina» y las `transfer_to_human_agent` de Prolongación y Consultas; variable
  `HORA_PRUEBA`). Sustituye la regla del aviso de D-013 y la decisión «las `nocturno_*` del principio» de D-012.
- **Quién:** el controlador de la construcción (R45), a propuesta de la revisión de la Tarea 15b.
- **Estado:** aplicada en v2 (Tarea 16).

## D-013 · 2026-10-20 · Aviso de transferencia neutro con Gestión cerrada (R34), en Prolongación y Consultas
- **Qué:** la descripción del `message` tipo `ai` de `transfer_to_human_agent` de Prolongación y de Consultas empieza
  por «Gestión ahora: [gestion_abierta]». Si es false (también en modo virtual), el aviso es neutro, «Un momento, por
  favor, no cuelgue», sin decir que le pasa con nadie; si es true, el de siempre («le paso con un compañero…, no
  cuelgue»). El Triaje se queda con el aviso de siempre. No cambia ningún prompt ni la cadena «Preparar transferencia».
- **Por qué:** el aviso suena al llamar a la herramienta, antes de que «Preparar transferencia» diga `gestion_cerrada`
  o `modo_virtual` (en la V10, «le paso» y después «invalid phone number», `casos/prolongaciones/docs/pendientes.md`).
  Opciones vistas (documentación de HappyRobot y nodos):
  1. `message: none` y aviso en el Transfer: el whisper lo oye el compañero, no el cliente, y `handoff_message` /
     `skip_handoff_message` del Transfer no están documentados (parecen del traspaso con aviso, `warm_handoff`). Sin
     una llamada no se sabe qué oiría el cliente ni si quedaría en silencio.
  2. Mensaje fijo condicionado: el tipo fijo no admite condiciones.
  3. Que el agente lo diga tras `transferir`: no hay turno, el Transfer arranca dentro de la misma cadena. Haría
     falta partir la herramienta en dos (comprobar y transferir), con texto nuevo en el bloque común (4.493/4.500) y
     en Prolongación (21.994/22.000): no cabe, y dobla la espera.
  4. **Elegida:** el aviso del `message` `ai` lo escribe el propio modelo al llamar (las evals lo ven como el argumento
     `_message`), así que se puede condicionar con la variable y medir en evals. En el peor caso, el cliente oye «un
     momento, no cuelgue» y la música de espera antes de una transferencia que sí sale, que es aceptable.
  Medido: R34-P1 3/3 y R34-C1 2/3 (aviso neutro con Gestión cerrada), R34-P2 3/3 (aviso de siempre con Gestión
  abierta). En el Triaje, R34-T1 dio 3/3 pero VIRT-T1 (crítica, modo virtual, reserva nueva) cayó de 3/3 a 1/3: con el
  aviso neutro transfería. La única vuelta («Esta frase no cambia cuándo se transfiere…») la dejó en 0/6, así que se
  deshizo (VIRT-T1 5/6 de nuevo). El spec (§5.8) ya aceptaba la frase incómoda como mal menor.
- **Afecta a:** v2 (dos herramientas; evals nuevas R34-P1, R34-P2, R34-T1 y R34-C1). Spec §5.8.
- **Pendiente:** comprobar en la llamada de la Tarea 17 que el cliente oye ese texto y que no hay silencio antes de la
  música; en el Triaje, el aviso de siempre hasta encontrar una forma que no cambie VIRT-T1.
- **Quién:** agente (Tarea 15b); revisa jzerpa en el PR.
- **Estado:** aplicada en v2 (Prolongación y Consultas).

## D-012 · 2026-10-20 · Cierre de la oficina del aeropuerto resuelto por código (`estado_oficina`, R39)
- **Qué:** Punto de encuentro tiene una herramienta nueva, `estado_oficina(aeropuerto)` (`message: none`), con un hijo
  Python «Estado de la oficina» (`codigo/estado_oficina.py`). El código reconoce el aeropuerto (nombre en español,
  inglés, italiano o portugués, con o sin «aeropuerto de»), lee la `nocturno_*` de su zona que da «Contexto de la
  llamada» y devuelve `oficina_cerrada`, `hora_apertura` y una `instruccion`. Las LISTAS 1 a 4 y las cuatro variables
  `nocturno_*` salen del prompt; PRIMERO manda ejecutar la herramienta antes de preguntar la terminal, dar el punto,
  transferir o usar otra herramienta, cuando lo que pide tiene que ver con el minibús o el punto de encuentro.
  Detalles:
  1. **Datos:** la tabla aeropuerto → zona es la de las LISTAS (la prueba lo compara una a una) y la hora de apertura
     la de PRIMERO. Aeropuerto desconocido: el valor de la LISTA 1, como decía el prompt.
  2. **Fuente de la hora:** las `nocturno_*` del principio de la llamada, como en la v25, y no el reloj del momento.
     Si la variable llega vacía o sin resolver, el reloj, con las mismas franjas de `contexto_llamada.py`.
  3. **Evals:** una eval solo valora un paso, así que hay dos clases. PE-EST-1 a 3 (nuevas) miden que llame a
     `estado_oficina` antes de nada; PE-NOCT-1 a 3c llevan ya la llamada y su resultado como mensaje `tool` y miden
     la respuesta al resultado. Las críticas con el punto ya dado (PDE-5, ADV-7, «DÍA · 25 minutos», «Idioma · EN · 25
     minutos», VIRT-PE1) y «VIRTUAL · 25 minutos» llevan en el historial la llamada con oficina abierta.
- **Por qué:** `fast-turbo-one` no cruzaba de forma fiable el aeropuerto con las listas: con Valencia (LISTA 1) daba
  el punto pe seis de madrugada (PE-NOCT-3 0/3, 3b 0/3 y 3c 1/3 en la ronda 22). El spec (§5.4) da a Punto de
  encuentro «el horario nocturno de los aeropuertos» y §5.8 ya decide por código lo que depende de la hora; la ficha
  prefería una herramienta. Con la herramienta, el bot no ha dado el punto con la oficina cerrada en ninguna de las 54
  ejecuciones con la oficina cerrada de las rondas A1 a A3. Se queda con las `nocturno_*` (punto 2) porque así las evals no dependen del reloj
  y el comportamiento es el de la v25.
- **Afecta a:** v2 (Punto de encuentro, su herramienta nueva y 13 evals). Spec §5.4 y §5.7.
- **Quién:** agente (Tarea 15b); revisa jzerpa en el PR.
- **Estado:** aplicada en v2.

## D-011 · 2026-10-19 · Medición diaria: normalización en código, informe con puertas y artefacto propio
- **Qué:** (1) La normalización de `llamadas.json` va en `scripts/normalizar_llamadas.py` con pruebas, no en el prompt
  de la rutina: `inicio` en UTC con Z, `opcion_menu` siempre informada (bots antiguos: la de su línea; bot único sin
  opción: minibus), colas con un solo nombre (`gestion_reserva` = `gestion`, extensiones traducidas) y los intentos
  parados por «Preparar transferencia» con `gestion_cerrada` o `modo_virtual` como transferencias con ese `error`
  (R43); `cola_no_valida` no se trata así. (2) `casos/atencion-es/codigo/informe_diario.py` arma el documento del día
  y evalúa las puertas de §8.4 con las cifras del día, marcadas como orientativas (las puertas 1 y 2 se deciden con
  dos semanas, §8.3); lo que no se mide en la rutina sale «a mano». (3) `medir_bots.py` acepta llamadas de contexto
  (otros días) solo para buscar rellamadas. (4) El hash del número es el sha256 de sus últimos 9 dígitos, para que
  `+34…`, `0034…` y el número sin prefijo coincidan entre bots. (5) El artefacto es una página propia con la capacidad
  `db` (colección `informes`, doc_id = fecha, lectura `view`, escritura `admin`), no el tipo «Dashboard».
- **Por qué:** (1) y (2) son reglas que tienen que dar lo mismo cada día; en código se prueban. (3) Una rellamada del
  día siguiente no se ve midiendo un solo día. (4) Los bots reciben el número con prefijos distintos. (5) La ficha y la
  rutina de Prolongaciones escriben un documento por día con `ArtifactData`; el tipo «Dashboard» guarda conjuntos de
  datos y la página en su propio almacén y no encaja con esa escritura diaria.
- **Afecta a:** rutina diaria (`rutinas/informe-atencion-es.md`), artefacto «Calidad Atención España», `scripts/`.
- **Quién:** agente (Tarea 15); revisa jzerpa en el PR.
- **Estado:** aplicada.

## D-010 · 2026-10-19 · Extract único: valores que el spec no fija
- **Qué:** en «Registrar resultado de la llamada» (Tarea 13, spec §5.12), donde la tabla del spec da solo el nombre del
  campo: (1) `cola_destino` usa los nombres de cola del bot único (`gestion`, `asistencia`, `nueva_reserva`, `minibus`,
  `ninguna`), no `gestion_reserva` de la v25 y la v12. (2) `saltos` es la suma de los `callCount` de los 12 Module
  Change: la primera entrada desde el Triaje no cuenta, y volver al Triaje y entrar en otro módulo cuenta uno (como en
  CAMBIOS DE MÓDULO de las reglas comunes). (3) `hubo_transferencia` = si solo si se intentó de verdad («Preparar
  transferencia» = `transferir`, o cola informada en los dos módulos que aún no tienen «Preparar transferencia»); un
  intento parado por Gestión cerrada va en `intento_gestion_cerrada`. (4) Los campos del correo de contraseña toman los
  valores de la v12, y `motivo_no_envio` añade `reserva_no_iniciada` (spec §5.7). (5) Los copiados de la entrada
  booleanos van como `si`/`no`, como `modo_virtual` en la v25. (6) Se añade `origen_opcion` (ruling de la Tarea 1).
  (7) `invento_condicion` no está en §5.12: los inventos vistos en evals (REQ-03, DEVOL-01, FDS-03) van como ejemplos
  de `invento_informacion`.
- **Por qué:** una sola forma de nombrar las colas en el bot único (la misma que `cola` de las herramientas); los
  `callCount` son el único dato técnico que cuenta todos los cambios de módulo (los parámetros de una herramienta solo
  guardan la última llamada); el spec manda sobre la ficha y no tiene `invento_condicion`.
- **Afecta a:** v2.
- **Quién:** agente (Tarea 13); revisa jzerpa en el PR.
- **Estado:** aplicada en v2.
- **Adenda (20/10/2026, Tarea R35):** con la cadena de Punto de encuentro e Información de oficina creada, el punto (3)
  pierde la excepción de esos dos módulos: `hubo_transferencia` e `intento_gestion_cerrada` salen solo del `resultado` de
  «Preparar transferencia», y el extract lee el `resultado` y el `transfer_succeeded` de las cinco cadenas.

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
- **Estado:** construida en v2, sin publicar (20/10/2026; puerta 0 pendiente, `pendientes.md`).
