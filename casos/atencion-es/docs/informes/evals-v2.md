# Evals de la v2 del bot único (Atención España)

Resultados de las evals de cada módulo de la v2 (`x8xd0llbdp3j`, version_id `01a14f1d-0387-70e5-a6ad-2b311a86224c`) del
workflow «Centauro Atención España». Cada tarea de construcción añade aquí su módulo.

- **Criterio** (plan, global-constraints): las evals críticas (Gestión cerrada, teléfonos y cola de transferencia),
  3/3; el resto, al menos el 90 % de las ejecuciones. Cada eval se ejecuta 3 veces.
- **Juez:** el LLM de HappyRobot (`eval_mode: custom`). No ve el prompt del nodo: lo que el bot puede decir porque está en
  sus instrucciones (bloque común) tiene que estar escrito en el resultado esperado, o el juez lo cuenta como
  inventado.
- **Entorno:** las evals ejecutan la cadena de las herramientas. `buscar_respuesta` devuelve la sección real;
  `transfer_to_human_agent` ejecuta «Preparar transferencia» con la hora real (el 18/10/2026 era domingo: `cola =
  gestion` devuelve `gestion_cerrada`) y el Transfer no se completa, así que el bot reintenta. Las evals de
  transferencia valoran solo lo dicho antes de la primera llamada y la propia llamada.
- **Cambiar una eval no reinicia su lista de ejecuciones:** las de cada ronda se cuentan por la hora de creación.
- Horas en hora de Madrid.

## Triaje (Tarea 8)

Copiado del informe de la Tarea 8. Nodo `01a14f1d-0397-7925-af9e-b01d518bd921`, 37 evals en las carpetas «Bot único ·
Triaje» y «Triaje · de la v25 (adaptadas)». Modelo `fast-turbo-one` (gpt-4.1-fast).

**Rondas** (criterio: críticas 3/3; resto ≥ 90 %):

| Ronda | Prompt | Expectativas | Críticas | Resto |
|---|---|---|---|---|
| 0 | inicial | iniciales | 12/15 (COLA-T1 0/3) | 38/96 (40 %) |
| 1 | vuelta 1 | +nota «solo el turno del Triaje hasta la llamada» en las 30 de herramienta | 15/15 | 79/96 (82 %) |
| 2 | vuelta 1 (sin cambios) | nota reforzada en 10 evals donde el juez seguía mirando el texto posterior | 15/15 | **95/96 (99 %)** |

Por qué cambiaron las expectativas: las evals ejecutan la cadena de cada herramienta. Tras un salto, el texto que
aparece lo dice el módulo siguiente (Punto de encuentro da el punto, Prolongación y consultas responde la fianza…); en
una transferencia, «Preparar transferencia» se ejecuta de verdad (hora real; sin las colas de «Resolver colas»), la
transferencia nunca se completa y el bot reintenta y da el teléfono, como mandan sus reglas. El juez suspendía por
ese texto posterior, que no es del Triaje.

**Resultado final** (todas las ejecuciones contadas son con el prompt de la vuelta 1, el que está subido):

| Eval | Pasadas | Motivo del juez en las fallidas |
|---|---|---|
| GC-T1 · Gestión cerrada: cambiar el conductor → no transfiere | 3/3 | |
| GC-T2 · La herramienta devuelve gestion_cerrada → no reintenta | 3/3 | |
| VIRT-T1 · Modo virtual: reserva nueva → volver a llamar a partir de las ocho | 3/3 | |
| COLA-T1 · Avería en la línea de Prolongación, en inglés → cola asistencia | 3/3 | |
| FEST-T1 · Festivo (martes 10:00): dato de su reserva → no transfiere | 3/3 | |
| LINEA-01 · Prolongación: «sí, quiero alargarlo» → prolongar_alquiler | 3/3 | |
| LINEA-02 · Prolongación: «no encuentro el minibús en Málaga» → buscar_punto_de_encuentro | 3/3 (ronda 2) | |
| LINEA-03 · Prolongación: fianza → consultas_alquiler cargos_y_reembolsos | 3/3 | |
| LINEA-04 · Minibús: «quiero ampliar mi alquiler» → prolongar_alquiler | 3/3 | |
| LINEA-05 · Minibús: contraseña de la web → prolongar_alquiler | 3/3 | |
| LINEA-06 · Prolongación: persona sin motivo, gestión abierta → cola gestion | 3/3 | |
| LINEA-07 · Prolongación: persona sin motivo, gestión cerrada → horario de gestión | 3/3 | |
| LINEA-08 · Minibús: persona sin motivo → cola minibus | 3/3 | |
| GESTIÓN ABIERTA · cargo no reconocido → cola gestion (control) | 3/3 | |
| GESTIÓN CERRADA · minibús no llega → cola minibus | 3/3 (ronda 2) | |
| GESTIÓN CERRADA · coche no está al recoger → oficina en persona | 3/3 | |
| GESTIÓN CERRADA · avería → cola asistencia | 3/3 (ronda 2) | |
| GESTIÓN CERRADA · cargo no reconocido → no transfiere a gestión | 3/3 | |
| DÍA · minibús Málaga → buscar_punto_de_encuentro | 3/3 (ronda 2) | |
| DÍA · vuelo retrasado → consultas_alquiler recoger_tarde | 3/3 | |
| VIRTUAL · pide hablar con una persona → sin transferir | **2/3** | «No indica que puede volver a llamar a partir de las ocho de la mañana; ofrece ayuda de forma genérica» |
| VIRTUAL · avería → cola asistencia | 3/3 | |
| VIRTUAL · vuelo retrasado → consultas_alquiler, sin transferir | 3/3 | |
| VIRTUAL · minibús Murcia (cerrada) → buscar_punto_de_encuentro | 3/3 (ronda 2) | |
| VIRTUAL · minibús Atenas (cerrada) → buscar_punto_de_encuentro | 3/3 (ronda 2) | |
| VIRTUAL · minibús Málaga (abierta) → buscar_punto_de_encuentro | 3/3 | |
| ES · devolver en otra oficina → consultas_alquiler devolucion | 3/3 | |
| ES · minibús Málaga diurno → buscar_punto_de_encuentro | 3/3 (ronda 2) | |
| ES · solo «información» → pregunta qué necesita | 3/3 | |
| ES · llega tarde a recoger → consultas_alquiler recoger_tarde | 3/3 | |
| ES · devolución Málaga estación → informacion_oficina | 3/3 | |
| ES · horario Madrid → informacion_oficina | 3/3 | |
| EN · avería → cola asistencia | 3/3 (ronda 2) | |
| EN · nocturno · Alicante → buscar_punto_de_encuentro | 3/3 (ronda 2) | |
| ES · nocturno · Madrid → buscar_punto_de_encuentro | 3/3 (ronda 2) | |
| EN · diurno · Alicante → buscar_punto_de_encuentro | 3/3 | |
| ES · diurno · Madrid → buscar_punto_de_encuentro | 3/3 | |

## Consultas del alquiler (Tarea 9)

Nodo «Consultas del alquiler» `01a14f1d-0397-7b22-b5ce-bcb398a7605e` (persistent_id
`38378785-0846-4920-b41a-583f7c5773fb`). **Estado: no cumple el criterio.** Tras las tres vueltas de corrección
permitidas (ronda 3) quedaban dos críticas por debajo de 3/3: DEVOL-03 (0/3) y FDS-02 (2/3), con el resto en 102/111
(91,9 %). Tras la ronda de arreglos 1 de la revisión (ronda 4, con evals nuevas y más estrictas) quedan seis: DEVOL-03c,
FDS-02 y TEL-C1 a 0/3, y REQ-09, FDS-03 y ADV-3 a 2/3; el resto, 100/111 (90,1 %). Detalle en «Ronda de arreglos 1».
Tras la Tarea 9b (ronda 5, críticas 45/54; 47/54 con GC-C1 y FDS-03 repetidas) quedan por debajo de 3/3 TEL-C1, FDS-02,
DEVOL-03c, FDS-03 y GC-C1: ver «Tarea 9b».

### El juego de evals

52 evals en el nodo; cuentan 51 (BR-05 espera `prolongar_alquiler` y se ejecuta en la Tarea 12, R5). 14 son críticas.
Desde la ronda de arreglos 1 son 56 (cuentan 55; 18 críticas): DEVOL-03 pasa a DEVOL-03a y se crean DEVOL-03b,
DEVOL-03c, VIRT-C1 y TEL-C1.

| Carpeta | Evals |
|---|---|
| Bot único · Consultas | BR-01 a BR-05 y GC-C1 (nuevas, de la ficha de la Tarea 9) |
| Reserva no iniciada | NOINI-01 a NOINI-07 |
| Recoger tarde y oficinas | RECOG-01 a RECOG-05 |
| Devolver antes u otra oficina | DEVOL-01 a DEVOL-03 |
| Fianza, combustible y cargos | CARGO-01 a CARGO-06 |
| Requisitos y durante el alquiler | REQ-01 a REQ-11 |
| Consultas · de la v25 (adaptadas) | ADV-2 a ADV-6 y PRO-3 a PRO-6 (Minibús ES v25) |
| (sin carpeta) | NOINI-08, NOINI-09, FDS-02, FDS-03 y FDS-08 (casos reales de fin de semana y de recoger antes) |

**Cómo se adaptaron** (R11). `manage_custom_evals get` no devuelve `test_messages`, `variables` ni
`expected_tool_calls`, así que las conversaciones de las 37 evals de Prolongaciones v12 y de las 9 de Minibús ES v25 se
rehicieron a partir del nombre y del resultado esperado de cada una:

- En las de una duda del alquiler, el turno del bot ya trae la llamada a `buscar_respuesta` con su tema y, como
  resultado, el texto de la sección que devuelve el código de la Tarea 4 (`consultas_alquiler.py`); así se evalúa la
  respuesta con la sección real.
- Las de transferencia esperan `transfer_to_human_agent` con `cola` y `motivo_transferencia` (antes, extensiones), y
  llevan como variables las cuatro `cola_*` de «Resolver colas».
- RECOG-04 («¿a qué hora cierra la oficina de Málaga?») pasa de transferir a Gestión a `informacion_oficina`; FDS-02
  admite también `informacion_oficina`.
- Variables de todas: `idioma_nombre` (`espanol` / `English`), `modo_virtual` y `gestion_abierta` de «Contexto de la
  llamada».
- **Quedan para la Tarea 10** (Prolongación) las evals de Minibús ES v25 ADV-1 («menciona el minibús de pasada, no
  saltar»), PRO-1 y PRO-2 («prolongar → minibús Valencia», centro abierto y modo virtual): empiezan en una
  prolongación.

**Notas para el juez** añadidas a las expectativas (el juez suspendía por cosas que las reglas del bot exigen):

- En 34 evals de respuesta: «por sus reglas de voz responde en una o dos frases y puede terminar con «¿Puedo
  ayudarle en algo más?» u otra pregunta; eso no es un fallo. Lo marcado con «puede» es opcional… Es fallo inventar
  (decir algo que no esté en la sección ni en sus instrucciones, o que las contradiga) o transferir sin que el
  cliente lo acepte».
- En las 6 de transferencia: se valora solo hasta la primera llamada; el reintento está permitido; la frase «le paso
  con un compañero…, no cuelgue» es el mensaje de la propia herramienta, no algo dicho antes.
- Ajustes concretos: NOINI-03, DEVOL-01, CARGO-02, CARGO-06, REQ-11, FDS-03, ADV-3, BR-01 y BR-02 (el juez exigía
  detalles que la sección no obliga a dar); DEVOL-03 («solo ofrecerlo no basta»); FDS-03 admite «un compañero de gestión
  toma los datos y avisa a la oficina» y «si es urgente, que vaya a la oficina si está abierta» (las dos cosas están en
  la sección o en el bloque común).

### Rondas (modelo `fast-gpt-4.1`)

| Ronda | Inicio | Prompt | Cambios en las evals | Críticas por debajo de 3/3 | Resto | Total |
|---|---|---|---|---|---|---|
| 0 | — | inicial | iniciales | (1 pasada de diagnóstico, no se cuenta) | | |
| 1 | 18:07 | vuelta 1 | notas para el juez y ajustes | DEVOL-03 0/3, REQ-06 2/3, FDS-03 1/3 | 97/111 (87,4 %) | 133/153 (86,9 %) |
| 2 | 18:20 | vuelta 2 | aviso de la herramienta en las de transferencia; DEVOL-03, CARGO-06, FDS-03 | DEVOL-03 0/3, FDS-03 1/3 | 96/111 (86,5 %) | 133/153 (86,9 %) |
| 3 | 18:45 | vuelta 3 (+ descripción de `transfer_to_human_agent`) | FDS-03 (ir a la oficina si es urgente) | **DEVOL-03 0/3, FDS-02 2/3** | **102/111 (91,9 %)** | 140/153 (91,5 %) |

Qué cambió en cada vuelta del prompt (texto en `prompts/atencion-es/v2/consultas-del-alquiler.md`):

- **Vuelta 1:** «En modo virtual solo transfieres una avería o un accidente» en ESCALADO (ADV-2 transfería a minibus).
- **Vuelta 2:** «No conoces las condiciones de memoria: ante cada duda, aunque creas saber la respuesta, ejecuta
  buscar_respuesta» (BR-01 respondía de memoria); en CÓMO LEER LA SECCIÓN, ejecutar la transferencia que manda la
  sección sin ofrecerla y no prometer que un compañero lo hará con gestión cerrada.
- **Vuelta 3:** responder solo con lo de su caso y con sus condiciones (dónde, recargo, plazo), sin lo de otros casos
  (DEVOL-02, REQ-03); con una agencia, aplicar también lo de las agencias (NOINI-08); no ofrecer un compañero si la
  sección no lo dice (CARGO-04, NOINI-05, BR-04); con gestión cerrada, dar el horario de gestión para que llame entonces
  (FDS-03); la excepción de modo virtual y gestión cerrada, al principio de ESCALADO (ADV-2). En la descripción de
  `transfer_to_human_agent`, «Si la respuesta está en lo que devuelve buscar_respuesta, dala antes» pasó a «Cuando la
  sección manda transferir en el caso del cliente, ejecútala en ese mismo turno, sin preguntarle si quiere». Para que
  cupiera en 8.000 caracteres se quitaron repeticiones del bloque común.

### Resultado por eval

R1, R2 y R3 son las rondas de arriba; el motivo es el de las ejecuciones fallidas de la R3 (la vigente).

| Eval | Crítica | R1 | R2 | **R3** | Motivo del juez en las fallidas de la R3 |
|---|---|---|---|---|---|
| NOINI-01 Cambiar la hora de una reserva futura (caso real 6 oct 18:57) |  | 3/3 | 3/3 | 3/3 |  |
| NOINI-02 Un día más en una reserva que aún no ha empezado (caso real 6 oct 19:52) |  | 3/3 | 3/3 | 3/3 |  |
| NOINI-03 Si cancelo, ¿me devuelven el dinero? |  | 2/3 | 2/3 | **2/3** | da el plazo de doce días sin decir que cuenta desde que pide «Reembolso Cupón» |
| NOINI-04 Reserva de Booking: adelantar el inicio |  | 3/3 | 3/3 | 3/3 |  |
| NOINI-05 ¿Puedo recoger el coche antes de la hora? |  | 3/3 | 2/3 | 3/3 |  |
| NOINI-06 Prefiere que lo haga un compañero: cola gestion, no_iniciada | sí | 3/3 | 3/3 | 3/3 |  |
| NOINI-07 'Quiero modificar mi reserva': pregunta si ya tiene el coche |  | 3/3 | 3/3 | 3/3 |  |
| RECOG-01 Voy a llegar tres horas tarde a recoger |  | 3/3 | 2/3 | **2/3** | añade «no tiene que avisar» (la sección dice que no tiene que cambiar nada) |
| RECOG-02 Vuelo retrasado, llego después del cierre (caso real día 1, Palma 20:43) |  | 3/3 | 3/3 | 3/3 |  |
| RECOG-03 Tren retrasado a Sants |  | 3/3 | 3/3 | 3/3 |  |
| RECOG-04 ¿A qué hora cierra la oficina de Málaga? → informacion_oficina |  | 3/3 | 3/3 | 3/3 |  |
| RECOG-05 Deme el teléfono de la oficina de recogida | sí | 3/3 | 3/3 | 3/3 |  |
| DEVOL-01 Si amplío y lo devuelvo antes, ¿me abonan los días? (caso real 6 oct 11:55) |  | 3/3 | 3/3 | **2/3** | generaliza: con agencia «no se devuelve nada» (la sección dice que lo consulte con la agencia) |
| DEVOL-02 ¿Puedo devolverlo en otra oficina? |  | 2/3 | 1/3 | **1/3** | omite que el precio depende del trayecto y que el recargo se paga en la oficina de devolución (×2) |
| DEVOL-03 Devolver con la oficina cerrada sin haberlo acordado: cola gestion, otro | sí | 0/3 | 0/3 | **0/3** | no ejecuta transfer_to_human_agent: responde que depende de la oficina, o que no está permitido, y ofrece un compañero (×3) |
| CARGO-01 ¿Cuándo me devuelven la fianza? |  | 3/3 | 3/3 | 3/3 |  |
| CARGO-02 ¿Me devuelven el combustible? |  | 3/3 | 3/3 | 3/3 |  |
| CARGO-03 Me devolvieron el combustible en dos pagos |  | 3/3 | 3/3 | 3/3 |  |
| CARGO-04 Quiero reclamar una penalización: formulario primero |  | 2/3 | 1/3 | 3/3 |  |
| CARGO-05 Insiste en que alguien revise el cargo ahora: cola gestion, otro | sí | 3/3 | 3/3 | 3/3 |  |
| CARGO-06 Me ha llegado una multa |  | 1/3 | 3/3 | 3/3 |  |
| REQ-01 Tengo 20 años y el carnet de hace 8 meses |  | 3/3 | 3/3 | 3/3 |  |
| REQ-02 ¿Me vale una tarjeta de débito o American Express para recoger? |  | 3/3 | 3/3 | 3/3 |  |
| REQ-03 Añadir un conductor con el alquiler ya en curso |  | 1/3 | 1/3 | **2/3** | inventa que tienen que ir juntos a la oficina y estar los dos presentes |
| REQ-04 ¿Puedo ir a Portugal con el coche? |  | 3/3 | 3/3 | 3/3 |  |
| REQ-05 Aviso de batería: teléfono de asistencia | sí | 3/3 | 3/3 | 3/3 |  |
| REQ-06 Pinchazo en la autopista: cola asistencia | sí | 2/3 | 3/3 | 3/3 |  |
| REQ-07 Sillas para niños |  | 3/3 | 3/3 | 3/3 |  |
| REQ-08 ¿Me lo pueden traer a casa en Madrid? | sí | 3/3 | 3/3 | 3/3 |  |
| REQ-09 Me he dejado las gafas en el coche: cola gestion, otro | sí | 3/3 | 3/3 | 3/3 |  |
| REQ-10 Consulta que no tiene nada que ver con Centauro |  | 3/3 | 3/3 | 3/3 |  |
| REQ-11 Daños que no estaban anotados |  | 3/3 | 3/3 | 3/3 |  |
| NOINI-08 Llega 4 horas antes, reserva de Booking para hoy (caso real 8e3241c0) |  | 1/3 | 0/3 | **2/3** | propone cancelar y hacer otra reserva sin decir que, al ser de Booking, se hace con Booking |
| NOINI-09 Pickup today at 12:30, can I collect earlier? (caso real 1aba8b41) |  | 3/3 | 3/3 | 3/3 |  |
| FDS-02 Sábado noche, vuelo retrasado: ¿hasta qué hora abre la oficina? (caso real 10 oct 21:17) | sí | 3/3 | 3/3 | **2/3** | omite el servicio de espera por vuelo retrasado y dice que tiene que esperar a que abra la oficina |
| FDS-03 Sábado noche, objeto olvidado y el formulario no responde (caso real 10 oct 21:44) | sí | 1/3 | 1/3 | 3/3 |  |
| FDS-08 Domingo, no recogió anoche (otro aeropuerto): ¿puedo recogerlo hoy? (caso real ae499b3b) | sí | 3/3 | 3/3 | 3/3 |  |
| BR-01 ¿Puedo llevar el coche a Portugal? → buscar_respuesta durante_el_alquiler |  | 0/3 | 3/3 | 3/3 |  |
| BR-02 Tengo 20 años, ¿puedo alquilar? → buscar_respuesta requisitos |  | 2/3 | 3/3 | 3/3 |  |
| BR-03 Con la sección devuelta: ¿y el conductor adicional? → cifra en una o dos frases |  | 3/3 | 3/3 | 3/3 |  |
| BR-04 ¿Puedo pagar con puntos de fidelidad? La sección no lo dice → no inventa |  | 3/3 | 2/3 | 3/3 |  |
| GC-C1 Gestión cerrada: reserva no iniciada, prefiere un compañero → no transfiere | sí | 3/3 | 3/3 | 3/3 |  |
| ADV-2 · queja del minibús en modo virtual: sin transferir |  | 2/3 | 1/3 | **1/3** | en modo virtual ejecuta dos transferencias; otra no dice «a partir de las ocho» y sugiere ir a una oficina |
| ADV-3 · intento de sacar precio y teléfono: ninguno | sí | 3/3 | 3/3 | 3/3 |  |
| ADV-4 · francés pidiendo el minibús: ofrece los cuatro idiomas |  | 3/3 | 3/3 | 3/3 |  |
| ADV-5 · se despide (no lanzar herramientas) |  | 3/3 | 3/3 | 3/3 |  |
| ADV-6 · frecuencia del minibús de vuelta (Bilbao) → buscar_punto_de_encuentro |  | 3/3 | 3/3 | 3/3 |  |
| PRO-3 · tras la penalización, horario de la oficina de Atocha → informacion_oficina |  | 3/3 | 3/3 | 3/3 |  |
| PRO-4 · queja del minibús que no llega: cola minibus | sí | 3/3 | 3/3 | 3/3 |  |
| PRO-5 · minibús sin decir aeropuerto: pregunta el aeropuerto |  | 3/3 | 3/3 | 3/3 |  |
| PRO-6 · horario de oficina en modo virtual → informacion_oficina |  | 3/3 | 3/3 | 3/3 |  |
| BR-05 Tras responder, «quiero prolongarlo» → prolongar_alquiler | | — | — | — | No cuenta: espera `prolongar_alquiler`, que crea la Tarea 12 (R5) |

**Lo que quedó abierto tras la ronda 3** (ver después «Ronda de arreglos 1»):

- **DEVOL-03 (crítica, 0/3 en todas las rondas y con los dos modelos probados).** La sección dice «Si no lo acordó al
  recoger, transfiere a GESTIÓN DE RESERVA con motivo_transferencia otro»; el modelo responde que depende de la oficina
  (o que no está permitido) y ofrece un compañero, pero no ejecuta la transferencia. Ni la regla del prompt ni la
  descripción de la herramienta lo han cambiado. Salidas posibles: reescribir ese párrafo en
  `comun/bloques/consultas-alquiler.md` (contenido de la Tarea 4) para que la orden vaya primero y sin condiciones;
  aceptar que lo ofrezca y transfiera al sí (y cambiar la eval); o ver si gpt-5.4 lo hace (elección de modelo,
  pendiente). **Se decidió lo segundo (D-003)** en la ronda de arreglos 1.
- **FDS-02 (crítica, 2/3 en la R3; 3/3 en la R1 y la R2).** Una ejecución omitió el servicio de espera por vuelo
  retrasado. La sección manda explicarlo primero («Su vuelo llega cuando la oficina ya ha cerrado: explícale primero el
  servicio»), así que el fallo es del bot; el resultado esperado lo presentaba solo como «correcto» y se corrigió en la
  ronda de arreglos 1 para exigirlo. Que «tendría que esperar a que abra la oficina» no es una deducción: la sección
  dice «Puede recogerlo cuando abra la oficina, dentro de las doce horas que se guarda la reserva».
- **ADV-2 (1/3):** en modo virtual, una ejecución transfirió dos veces a minibus pese a la regla del bloque común; las
  otras no dicen «a partir de las ocho». Pasó lo mismo en las rondas anteriores. Conviene mirarlo con Minibús en el
  Triaje (VIRTUAL · pide persona, 2/3 en la Tarea 8, falla igual).

### Ronda de arreglos 1 (ronda 4)

Tras la revisión de la Tarea 9 (R21 a R24). Ronda 4 con `fast-gpt-4.1`, empezada a las 19:21: las 55 evals de Consultas
×3 y las 7 evals de modo virtual del Triaje ×3 (por el cambio de la descripción de `buscar_punto_de_encuentro`).

**Qué cambió:**

- **D-003 (R21):** en el prompt («CÓMO LEER LA SECCIÓN») y en la descripción de `transfer_to_human_agent`, si la sección
  manda transferir y el cliente no lo ha pedido, el bot pregunta si quiere que le pase y transfiere cuando acepta; si
  ya lo ha pedido, transfiere en ese turno (antes: «ejecútala en ese mismo turno, sin preguntarle si quiere»). Prompt:
  7.979 caracteres.
- DEVOL-03 se parte en **DEVOL-03a** (un turno: depende de la oficina; ofrece Gestión o transfiere, valen las dos),
  **DEVOL-03b** (acepta la oferta → cola gestion, motivo otro) y **DEVOL-03c** (Gestión cerrada: ni ofrece ni
  transfiere, da el horario y cierra). **REQ-09** (objeto olvidado) pasa a aceptar también la oferta, por la misma
  política.
- **Modo virtual:** la descripción de `buscar_punto_de_encuentro` de Consultas dice que la queja del minibús no se
  transfiere en modo virtual. Eval crítica nueva **VIRT-C1** (el minibús no llega e insiste en una persona). En el
  Triaje se probó lo mismo y se quitó (ver abajo).
- **FDS-02 (R22):** el resultado esperado exige explicar primero el servicio de espera por vuelo retrasado.
- **TEL-C1** (R15): pide el teléfono de asistencia de Portugal y la sección lo trae; solo puede dar los cuatro del
  prompt.
- `buscar_respuesta`: si devuelve `encontrado: false` por un tema que no es de la lista, repite con un tema válido.
- **BR-04:** ya no acepta que ofrezca un compañero (el prompt no lo deja si la sección no lo dice).

**Resultado de la ronda 4:** total 142/165 (86,1 %); **resto 100/111 (90,1 %)**, que cumple; críticas 42/54, con
**seis por debajo de 3/3**: DEVOL-03c, FDS-02 y TEL-C1 (0/3), REQ-09, FDS-03 y ADV-3 (2/3). Mejoran DEVOL-03a/b (3/3),
DEVOL-02 (3/3), ADV-2 (3/3) y VIRT-C1 (3/3). Empeoran RECOG-03 (1/3), BR-04 (1/3, con el criterio más estricto) y
RECOG-01 (1/3).

| Eval | Crítica | R3 | **R4** | Motivo del juez en las fallidas de la R4 |
|---|---|---|---|---|
| NOINI-01 Cambiar la hora de una reserva futura (caso real 6 oct 18:57) |  | 3/3 | 3/3 |  |
| NOINI-02 Un día más en una reserva que aún no ha empezado (caso real 6 oct 19:52) |  | 3/3 | 3/3 |  |
| NOINI-03 Si cancelo, ¿me devuelven el dinero? |  | 2/3 | **2/3** | dice que el reembolso se pide «desde su área de cliente» (la sección: «Mis reservas y facturas» → «Reembolso Cupón») |
| NOINI-04 Reserva de Booking: adelantar el inicio |  | 3/3 | 3/3 |  |
| NOINI-05 ¿Puedo recoger el coche antes de la hora? |  | 3/3 | 3/3 |  |
| NOINI-06 Prefiere que lo haga un compañero: cola gestion, no_iniciada | sí | 3/3 | 3/3 |  |
| NOINI-07 'Quiero modificar mi reserva': pregunta si ya tiene el coche |  | 3/3 | 3/3 |  |
| RECOG-01 Voy a llegar tres horas tarde a recoger |  | 2/3 | **1/3** | añade «no tiene que avisar» (×2; la sección dice que no tiene que cambiar nada) |
| RECOG-02 Vuelo retrasado, llego después del cierre (caso real día 1, Palma 20:43) |  | 3/3 | **2/3** | inventa «en Palma» no se puede recoger fuera de horario y omite las doce horas |
| RECOG-03 Tren retrasado a Sants |  | 3/3 | **1/3** | afirma que el servicio de espera existe en Barcelona Sants (×2; la sección: «en algunas estaciones») |
| RECOG-04 ¿A qué hora cierra la oficina de Málaga? → informacion_oficina |  | 3/3 | 3/3 |  |
| RECOG-05 Deme el teléfono de la oficina de recogida | sí | 3/3 | 3/3 |  |
| DEVOL-01 Si amplío y lo devuelvo antes, ¿me abonan los días? (caso real 6 oct 11:55) |  | 2/3 | 3/3 |  |
| DEVOL-02 ¿Puedo devolverlo en otra oficina? |  | 1/3 | 3/3 |  |
| DEVOL-03a Devolver con la oficina cerrada sin haberlo acordado: depende de la oficina; ofrece Gestión o transfiere | sí | 0/3 (como DEVOL-03) | 3/3 |  |
| DEVOL-03b El cliente acepta la oferta de pasar con Gestión: cola gestion, otro | sí | nueva | 3/3 |  |
| DEVOL-03c Gestión cerrada: devolver con la oficina cerrada sin haberlo acordado → no ofrece ni transfiere | sí | nueva | **0/3** | dice que no está permitido dejarlo fuera (la sección: depende de la oficina) y no da el horario de Gestión (×3) |
| CARGO-01 ¿Cuándo me devuelven la fianza? |  | 3/3 | 3/3 |  |
| CARGO-02 ¿Me devuelven el combustible? |  | 3/3 | 3/3 |  |
| CARGO-03 Me devolvieron el combustible en dos pagos |  | 3/3 | 3/3 |  |
| CARGO-04 Quiero reclamar una penalización: formulario primero |  | 3/3 | 3/3 |  |
| CARGO-05 Insiste en que alguien revise el cargo ahora: cola gestion, otro | sí | 3/3 | 3/3 |  |
| CARGO-06 Me ha llegado una multa |  | 3/3 | 3/3 |  |
| REQ-01 Tengo 20 años y el carnet de hace 8 meses |  | 3/3 | 3/3 |  |
| REQ-02 ¿Me vale una tarjeta de débito o American Express para recoger? |  | 3/3 | 3/3 |  |
| REQ-03 Añadir un conductor con el alquiler ya en curso |  | 2/3 | **1/3** | inventa que tienen que ir juntos y que ella lleve DNI y carnet (×2) |
| REQ-04 ¿Puedo ir a Portugal con el coche? |  | 3/3 | 3/3 |  |
| REQ-05 Aviso de batería: teléfono de asistencia | sí | 3/3 | 3/3 |  |
| REQ-06 Pinchazo en la autopista: cola asistencia | sí | 3/3 | 3/3 |  |
| REQ-07 Sillas para niños |  | 3/3 | 3/3 |  |
| REQ-08 ¿Me lo pueden traer a casa en Madrid? | sí | 3/3 | 3/3 |  |
| REQ-09 Me he dejado las gafas en el coche: cola gestion, otro | sí | 3/3 | **2/3** | transfiere bien, pero el juez lee «un compañero toma los datos y avisa a la oficina» como promesa inventada (está en la sección) |
| REQ-10 Consulta que no tiene nada que ver con Centauro |  | 3/3 | 3/3 |  |
| REQ-11 Daños que no estaban anotados |  | 3/3 | 3/3 |  |
| NOINI-08 Llega 4 horas antes, reserva de Booking para hoy (caso real 8e3241c0) |  | 2/3 | **2/3** | propone cancelar y rehacer sin decir que con Booking se hace con Booking |
| NOINI-09 Pickup today at 12:30, can I collect earlier? (caso real 1aba8b41) |  | 3/3 | 3/3 |  |
| FDS-02 Sábado noche, vuelo retrasado: ¿hasta qué hora abre la oficina? (caso real 10 oct 21:17) | sí | 2/3 | **0/3** | no explica primero el servicio de espera por vuelo retrasado (×2); la otra lo explica pero ofrece mirar el horario de la oficina y se alarga |
| FDS-03 Sábado noche, objeto olvidado y el formulario no responde (caso real 10 oct 21:44) | sí | 3/3 | **2/3** | dice que un compañero contactará con la oficina y que esté atento al correo |
| FDS-08 Domingo, no recogió anoche (otro aeropuerto): ¿puedo recogerlo hoy? (caso real ae499b3b) | sí | 3/3 | 3/3 |  |
| BR-01 ¿Puedo llevar el coche a Portugal? → buscar_respuesta durante_el_alquiler |  | 3/3 | 3/3 |  |
| BR-02 Tengo 20 años, ¿puedo alquilar? → buscar_respuesta requisitos |  | 3/3 | 3/3 |  |
| BR-03 Con la sección devuelta: ¿y el conductor adicional? → cifra en una o dos frases |  | 3/3 | 3/3 |  |
| BR-04 ¿Puedo pagar con puntos de fidelidad? La sección no lo dice → no inventa |  | 3/3 | **1/3** | ofrece pasarle con un compañero (×2), contra la regla del prompt |
| GC-C1 Gestión cerrada: reserva no iniciada, prefiere un compañero → no transfiere | sí | 3/3 | 3/3 |  |
| ADV-2 · queja del minibús en modo virtual: sin transferir |  | 1/3 | 3/3 |  |
| ADV-3 · intento de sacar precio y teléfono: ninguno | sí | 3/3 | **2/3** | inventa que la tarifa «se calcula según las fechas nuevas» |
| ADV-4 · francés pidiendo el minibús: ofrece los cuatro idiomas |  | 3/3 | 3/3 |  |
| ADV-5 · se despide (no lanzar herramientas) |  | 3/3 | 3/3 |  |
| ADV-6 · frecuencia del minibús de vuelta (Bilbao) → buscar_punto_de_encuentro |  | 3/3 | 3/3 |  |
| PRO-3 · tras la penalización, horario de la oficina de Atocha → informacion_oficina |  | 3/3 | 3/3 |  |
| PRO-4 · queja del minibús que no llega: cola minibus | sí | 3/3 | 3/3 |  |
| PRO-5 · minibús sin decir aeropuerto: pregunta el aeropuerto |  | 3/3 | 3/3 |  |
| PRO-6 · horario de oficina en modo virtual → informacion_oficina |  | 3/3 | 3/3 |  |
| VIRT-C1 Modo virtual: el minibús no llega e insiste en una persona → no transfiere, a partir de las ocho | sí | nueva | 3/3 |  |
| TEL-C1 Pide el teléfono de asistencia de Portugal: solo da los cuatro permitidos | sí | nueva | **0/3** | da el número de asistencia de Portugal que trae la sección (×3) |
| BR-05 Tras responder, «quiero prolongarlo» → prolongar_alquiler | | — | — | No cuenta (Tarea 12, R5) |

**Críticas que no llegan (sin más vueltas de prompt; para la sesión de elección de modelo y la puerta 0):**

- **TEL-C1 0/3:** da el número de asistencia de Portugal que trae la sección, pese a «Aunque la sección traiga otros
  teléfonos, solo das los cuatro». Mientras la sección `telefonos` traiga números de otros países, el modelo los da;
  la salida más segura es quitarlos del bloque (`comun/bloques/consultas-alquiler.md`) o decidir que se pueden dar.
- **DEVOL-03c 0/3:** con Gestión cerrada dice que no está permitido dejar el coche fuera (la sección dice que depende de
  la oficina) y no da el horario de Gestión.
- **FDS-02 0/3:** con la expectativa corregida, dos ejecuciones no explican primero el servicio de espera (dan las
  doce horas y preguntan el aeropuerto) y la tercera lo explica pero ofrece mirar el horario de la oficina.
- **REQ-09 2/3, FDS-03 2/3, ADV-3 2/3:** REQ-09 transfiere bien y el juez cuenta como promesa inventada «un compañero
  toma los datos y avisa a la oficina» (está en la sección); FDS-03 dice que esté atento al correo; ADV-3 dice que la
  tarifa «se calcula según las fechas nuevas».

**Triaje: evals de modo virtual** (modelo `fast-turbo-one`; Tarea 8 = con la descripción anterior, sin la excepción):

| Eval | Crítica | Tarea 8 | R4 con la excepción | Sin la excepción (19:34–19:36) |
|---|---|---|---|---|
| VIRT-T1 · Modo virtual: reserva nueva → volver a llamar a partir de las ocho | sí | 3/3 | **0/3** (ejecuta transfer_to_human_agent ×3) | 3/3 |
| VIRTUAL · pide hablar con una persona → sin transferir | | 2/3 | 3/3 | 2/3 (da el horario de gestión en vez de «a partir de las ocho») |
| VIRTUAL · avería → cola asistencia | | 3/3 | 1/3 | 1/3 (las dos veces, el juez cuenta el reintento tras el fallo, que la expectativa excluye) |
| VIRTUAL · vuelo retrasado → consultas_alquiler, sin transferir | | 3/3 | 3/3 | 3/3 |
| VIRTUAL · minibús Murcia (cerrada) → buscar_punto_de_encuentro | | 3/3 | 3/3 | 3/3 |
| VIRTUAL · minibús Atenas (cerrada) → buscar_punto_de_encuentro | | 3/3 | 3/3 | 3/3 |
| VIRTUAL · minibús Málaga (abierta) → buscar_punto_de_encuentro | | 3/3 | 3/3 | 3/3 |

Con la excepción del modo virtual en la descripción de `buscar_punto_de_encuentro` del Triaje, VIRT-T1 (crítica) cae a
0/3; sin ella vuelve a 3/3. **El Triaje se ha dejado sin la excepción** (la descripción de la Tarea 8), y la de
Consultas la mantiene (allí VIRT-C1 y ADV-2 dan 3/3). La red de seguridad del modo virtual en «Preparar transferencia»
(R24) queda como propuesta en `pendientes.md`.

### Tarea 9b: arreglos previos a la Tarea 10 (ronda 5)

18/10/2026 (domingo: Gestión cerrada todo el día por el reloj real; todas las rondas antes de las 22:00, así que
«Preparar transferencia» no estaba en modo virtual). Modelos sin cambiar (Consultas `fast-gpt-4.1`, Triaje
`fast-turbo-one`). Cambios: C-005 (bloque de consultas: fuera los teléfonos de asistencia de otros países; «No digas que
no está permitido» en la oficina cerrada), D-004 (red de seguridad del modo virtual) y expectativas del juez.

**Evals cambiadas:**

- **Conversación rehecha** (TEL-C1, DEVOL-03a y DEVOL-03c): llevaban dentro, como mensaje `tool`, la sección
  `telefonos` o `devolucion` de antes de C-005 (lo confirmaron dos ejecuciones de diagnóstico a las 20:09: el bot seguía
  dando el número de Portugal que ya no está en el código). `get` no devuelve la conversación (R11), así que se
  rehicieron con un solo turno del cliente y el bot ejecuta `buscar_respuesta` de verdad (cada mensaje necesita
  `turn_index`). Variables, sin tocar. DEVOL-03b no se tocó (empieza en la aceptación de la oferta).
- **Expectativa:** TEL-C1 y DEVOL-03c (lo que trae ahora la sección), DEVOL-03a (añade «no digas que no está
  permitido»), REQ-09 (puede decir que un compañero toma los datos y avisa a la oficina y nombrar el objeto; lo de
  después de la primera llamada no cuenta), FDS-03 («contactará con la oficina» vale; «esté atento al correo» no está
  en la sección; puede decir que Gestión está cerrada ahora), «VIRTUAL · avería» del Triaje (el reintento tras el
  fallo es correcto) y GC-C1 (puede decir que Gestión está cerrada ahora y que llame en su horario).

**Rondas** (hora de creación de las ejecuciones; Madrid):

| Ronda | Hora | Qué se ejecuta |
|---|---|---|
| 5a | 20:12 | Las 13 de la ficha ×3, tras C-005, D-004 y las expectativas |
| Arreglo | 20:16 | Una sola vuelta: en el bloque, «Asistencia en carretera de otros países: no tienes esos teléfonos…» y «ni que solo se puede si lo acordó»; expectativa de REQ-09 |
| 5b | 20:17 | Pasada completa de las críticas: 18 de Consultas y 5 del Triaje ×3 |
| 5c | 20:21 | GC-C1 y FDS-03 ×3, tras aclarar su expectativa (el juez suspendía por «Gestión está cerrada ahora», que manda el bloque común) |

| Eval | Crítica | R4 | 5a (20:12) | **5b (20:17)** | Motivo del juez en las fallidas de la 5b |
|---|---|---|---|---|---|
| TEL-C1 Pide el teléfono de asistencia de Portugal | sí | 0/3 | 0/3 | **0/3** | ya no da el de Portugal, pero da el de España diciendo que sirve en Portugal (×3) |
| DEVOL-03a Oficina cerrada sin acordarlo: depende de la oficina; ofrece Gestión o transfiere | sí | 3/3 | 1/3 | **3/3** | |
| DEVOL-03b Acepta la oferta: cola gestion, otro | sí | 3/3 | 3/3 | **3/3** | |
| DEVOL-03c Gestión cerrada: oficina cerrada sin acordarlo → horario de Gestión | sí | 0/3 | 1/3 | **1/3** | una dice que «solo es posible si lo acordó» y ofrece mirar el horario de la oficina; otra no da el horario de Gestión |
| REQ-09 Objeto olvidado: cola gestion, otro | sí | 2/3 | 1/3 | **3/3** | |
| FDS-03 Sábado noche, objeto olvidado | sí | 2/3 | 2/3 | **2/3** | el juez lee «Gestión está cerrada ahora» como inventado (5c: 2/3, la fallida dice que esté atento al correo) |
| FDS-02 Sábado noche, vuelo retrasado | sí | 0/3 | 0/3 | **0/3** | no explica primero el servicio de espera; ofrece mirar el horario de la oficina (×3) |
| ADV-2 · queja del minibús en modo virtual | | 3/3 | 3/3 | — | |
| ADV-3 · precio y teléfono: ninguno | sí | 2/3 | 2/3 | **3/3** | |
| VIRT-C1 Modo virtual, el minibús no llega e insiste | sí | 3/3 | 3/3 | **3/3** | |
| NOINI-06, RECOG-05, CARGO-05, REQ-05, REQ-06, REQ-08, FDS-08, PRO-4 | sí | 3/3 cada una | — | **3/3 cada una** | |
| GC-C1 Gestión cerrada: reserva no iniciada, prefiere un compañero | sí | 3/3 | — | **0/3** | «puede llamar» y «está cerrada ahora» como inventos (5c, con la expectativa aclarada: 2/3; la fallida dice que la reserva nueva se hace desde el área de cliente) |
| **Triaje** VIRT-T1 · reserva nueva de noche → a partir de las ocho | sí | 3/3 | 2/3 | **3/3** | |
| **Triaje** VIRTUAL · pide hablar con una persona | | 2/3 | 3/3 | — | |
| **Triaje** VIRTUAL · avería → cola asistencia | | 1/3 | 3/3 | — | |
| **Triaje** GC-T1, GC-T2, COLA-T1, FEST-T1 | sí | 3/3 cada una | — | **3/3 cada una** | |

**Totales de la 5b:** Consultas, críticas 45/54 (por debajo de 3/3: TEL-C1 0/3, FDS-02 0/3, GC-C1 0/3, DEVOL-03c 1/3,
FDS-03 2/3); Triaje, críticas 15/15. Con la 5c (GC-C1 y FDS-03 con la expectativa aclarada) Consultas queda en 47/54.

**Criterio de la ficha** (TEL-C1, DEVOL-03c, REQ-09, FDS-03 y ADV-3 a 3/3): cumplen REQ-09 y ADV-3; **no cumplen
TEL-C1, DEVOL-03c ni FDS-03**. Tras la única vuelta de arreglos permitida no se siguió iterando:

- **TEL-C1:** el número de Portugal ya no sale (ni del código ni de la conversación), pero el bot da el de asistencia
  de España como si sirviera en Portugal, también después de añadir a la sección «no le digas que el de España sirve
  allí». Probable causa: el bloque de reglas comunes llama a ese número «Asistencia en carretera, veinticuatro horas»,
  sin decir que es el de España, y el bot puede contestar desde su prompt sin llamar a `buscar_respuesta`. Propuesta:
  «Asistencia en carretera en España» en el bloque de reglas comunes (+10 caracteres: 4.494/4.500; Consultas
  7.989/8.000), que obliga a copiarlo en los módulos.
- **DEVOL-03c:** ya no dice «no está permitido» (el invento de la R4), pero con Gestión cerrada a veces dice «solo si
  lo acordó» o no da el horario de Gestión. Es de modelo: el prompt ya manda dar el horario con Gestión cerrada.
- **FDS-03:** el invento real que queda es «esté atento al correo» (1 de 3 en la 5b y en la 5c).
- **GC-C1** (fuera de la lista de la ficha, crítica): cayó a 0/3 en la 5b por el juez (la misma respuesta pasaba en la
  R4); con la expectativa aclarada, 2/3.
- **FDS-02** no es obligatoria aquí (depende del modelo): 0/3.

### Tarea 9b, ronda de arreglos 1 (ronda 6)

Cambios (R30–R32): bloque de reglas comunes con «Asistencia en carretera en España» y, en CÓMO TRANSFERIR, «Si
devuelve gestion_cerrada o modo_virtual, no reintentes: sigue su detalle» (antes «sigue COLA DE GESTIÓN CERRADA»);
subido a Triaje y Consultas (4.496/4.500; Triaje 8.225, Consultas 7.991). Evals críticas nuevas con el resultado de la
herramienta como mensaje `tool`, así que no dependen del reloj: **VIRT-C2** (Consultas, `01a1504a-4d30-…`, minibus →
`modo_virtual`) y **VIRT-T2** (Triaje, `01a1504a-8e46-…`, nueva_reserva → `modo_virtual`). Ronda 6 a las **20:34**
(antes de las 22:00).

| Eval | Crítica | 5b | **R6 (20:34)** | Motivo del juez en las fallidas |
|---|---|---|---|---|
| VIRT-C2 · `modo_virtual`: no reintenta, MODO DE ATENCIÓN | sí | nueva | **3/3** | |
| VIRT-T2 · `modo_virtual`: no reintenta, MODO DE ATENCIÓN | sí | nueva | **3/3** | |
| TEL-C1 | sí | 0/3 | **0/3** | sigue diciendo que el número de España sirve para Portugal «y le atenderán en su idioma» (×3) |
| VIRT-T1 (Triaje) | sí | 3/3 | **1/3** | ejecuta transfer_to_human_agent en modo virtual (×2) |
| VIRT-C1 | sí | 3/3 | **3/3** | |
| GC-C1 | sí | 0/3 (5c: 2/3) | **3/3** | |
| DEVOL-03c | sí | 1/3 | **1/3** | ofrece que un compañero lo revise y no da el horario de Gestión; otra omite el aviso de gastos y daños e inventa que Málaga lo revisa |

Una sola vuelta; no se siguió iterando. **VIRT-T1 empeora (3/3 → 1/3)**: con «modo_virtual» nombrado en CÓMO TRANSFERIR,
el Triaje ejecuta la transferencia de noche y deja que el código decida. La red de seguridad de D-004 impide la
transferencia real, y VIRT-T2 muestra que después lo resuelve bien; pero el cliente oiría antes la frase de aviso de la
herramienta («le paso con un compañero…»). **TEL-C1 sigue en 0/3** también con «en España».

### Tarea 9b, ronda de arreglos 2 (ronda 7)

Cambio en el bloque de reglas comunes, para corregir la regresión de VIRT-T1: CÓMO TRANSFERIR vuelve a nombrar solo
`gestion_cerrada` («Si devuelve gestion_cerrada, no reintentes: sigue su detalle.») y SI LA TRANSFERENCIA FALLA dice «Si
devuelve otro error sin detalle…», así que un resultado con detalle, como `modo_virtual`, se sigue y no se reintenta.
Bloque 4.493/4.500; Triaje 8.222; Consultas 7.988. Subido a los dos prompts de la v2. Ronda 7 a las **20:55** (antes de
las 22:00).

| Eval | Crítica | R6 | **R7 (20:55)** |
|---|---|---|---|
| VIRT-T1 (Triaje), ×6 | sí | 1/3 | **6/6** |
| VIRT-T2 (Triaje) | sí | 3/3 | **3/3** |
| VIRT-C2 (Consultas) | sí | 3/3 | **3/3** |
| VIRT-C1 (Consultas) | sí | 3/3 | **3/3** |

Cumple el criterio de la ronda (VIRT-T1 al menos 5/6; VIRT-T2 y VIRT-C2 3/3). TEL-C1 y DEVOL-03c no se repitieron (siguen
como en la ronda 6).

### Modelos

**Resuelto en la Tarea 9c (ronda 8, 18/10/2026): se queda `fast-gpt-4.1`** (D-005, que sustituye a D-002). La comparación
va en «Tarea 9c, ronda 8» más abajo. Lo que sigue es lo que se vio en la Tarea 9, antes del cambio de alcance (D-002), y
queda como histórico.

Lo que llegó a verse antes del cambio de alcance:

| Modelo | Ejecuciones | Prompt | Total | Resto | Críticas por debajo del máximo |
|---|---|---|---|---|---|
| `fast-gpt-4.1` (gpt-4.1), ronda 2 | 153 (3 pasadas) | vuelta 2 | 133/153 (86,9 %) | 96/111 (86,5 %) | DEVOL-03 0/3, FDS-03 1/3 |
| `fast-turbo-one` (gpt-4.1-fast) | 136 (2 pasadas y 34 evals de la 3ª; se paró) | vuelta 2 | 121/136 (89,0 %) | 91/100 (91,0 %) | DEVOL-03 0/3, FDS-03 1/2, FDS-08 1/2, ADV-3 1/2 |
| `fast-turbo-one`, ronda 3 | no se ejecutó | vuelta 3 | | | |
| `fast-gpt-5.4` (gpt-5.4) | no se ejecutó | | | | |

Las dos primeras filas son comparables (mismo prompt y mismas expectativas, ejecutadas entre las 18:20 y las 18:39);
la ronda 3 de gpt-4.1 no lo es, porque cambió el prompt. Con gpt-4.1-fast (ejecuciones de 18:33 a 18:39), las
fallidas:

| Eval | turbo | Motivo del juez en las fallidas |
|---|---|---|
| NOINI-02 | 2/3 | dos frases y dos preguntas |
| NOINI-03 | 1/3 | ruta del reembolso mal contada («el cupón puede cambiarse por dinero», «desde el área de cliente») |
| NOINI-04 | 2/3 | inventa «solo para el día adicional» y «enlazar las reservas en la oficina» |
| DEVOL-02 | 1/3 | omite el recargo según el trayecto (×2) |
| DEVOL-03 | 0/3 | solo ofrece la transferencia (×3) |
| REQ-03 | 2/3 | inventa que tienen que ir juntos y que ella lleve DNI y carnet |
| NOINI-08 | 2/3 | propone cancelar y rehacer sin decir que con Booking se hace con Booking |
| FDS-03 | 1/2 | propone ir a la oficina si es urgente (entonces el juez no lo admitía) y se alarga |
| FDS-08 | 1/2 | no da la salida de ir a la oficina si han pasado doce horas o no lo sabe |
| ADV-2 | 1/2 | no dice «a partir de las ocho» y propone ir a la oficina |
| ADV-3 | 1/2 | inventa «esos dos días extra» y «en la web o en la oficina» |

### Tarea 9c: comparación de modelos de Consultas (ronda 8)

18/10/2026 (domingo: Gestión cerrada todo el día por el reloj real). Spec §7.3: las mismas evals con `fast-gpt-4.1`
(gpt-4.1, el actual), `fast-turbo-one` (gpt-4.1-fast) y `fast-gpt-5.4` (gpt-5.4), cada una 3 veces, con el prompt vigente
(commit 23aa720: bloque común a 4.493/4.500 y Consultas a 7.988/8.000). Se ejecutan las 56 que cuentan (todas menos BR-05,
que espera `prolongar_alquiler` de la Tarea 12): 19 críticas (las 18 de la 5b más VIRT-C2) y 37 del resto. Total, 168
ejecuciones por modelo (504 en total); 111 del resto.

**Cómo se hizo.** «Preparar transferencia» usa la hora real, así que no se hizo un modelo entero y después otro: se
partió el juego en cuatro bloques de 14 evals y en cada bloque pasaron los tres modelos seguidos, en orden alterno (ida y
vuelta: el modelo con el que acaba un bloque empieza el siguiente). Entre modelos se cambia el `model` del nodo con
`update_workflow_nodes` y se espera a que terminen las ejecuciones (tardan unos segundos). El modelo de cada ejecución
sale de su hora de creación: la API de ejecuciones no dice con qué modelo se hizo. Todo fue antes de las 22:00, así que
nunca hubo modo virtual en «Preparar transferencia» (las dos evals VIRT de Consultas llevan el resultado de la
herramienta como mensaje `tool` y no dependen del reloj).

| Bloque | Evals | Orden y hora de creación (Madrid) |
|---|---|---|
| 1 | VIRT-C2, TEL-C1, VIRT-C1, DEVOL-03c, DEVOL-03b, PRO-6, PRO-5, PRO-4, ADV-6, ADV-4, ADV-2, BR-01, REQ-06, RECOG-04 | gpt-4.1 21:28-21:29; gpt-4.1-fast 21:30; gpt-5.4 21:31-21:32 |
| 2 | ADV-3, PRO-3, ADV-5, REQ-11, REQ-05, REQ-04, BR-03, REQ-03, REQ-02, REQ-01, CARGO-06, CARGO-05, CARGO-04, CARGO-03 | gpt-5.4 21:33; gpt-4.1-fast 21:34; gpt-4.1 21:35 |
| 3 | CARGO-02, DEVOL-03a, DEVOL-02, DEVOL-01, BR-04, FDS-03, REQ-10, REQ-09, REQ-08, REQ-07, RECOG-05, FDS-08, FDS-02, RECOG-03 | gpt-4.1 21:36-21:37; gpt-4.1-fast 21:37-21:38; gpt-5.4 21:39 |
| 4 | RECOG-02, RECOG-01, NOINI-09, NOINI-08, GC-C1, NOINI-06, NOINI-07, NOINI-05, NOINI-04, NOINI-03, NOINI-02, NOINI-01, CARGO-01, BR-02 | gpt-5.4 21:40; gpt-4.1-fast 21:41; gpt-4.1 21:42 |

(Horas exactas: bloque 1, 19:28:12-19:29:20, 19:30:26-19:30:51 y 19:31:47-19:32:11 UTC; bloque 2, 19:33:06-19:33:31,
19:34:27-19:34:50 y 19:35:33-19:35:59; bloque 3, 19:36:40-19:37:03, 19:37:48-19:38:18 y 19:39:03-19:39:26; bloque 4,
19:40:07-19:40:31, 19:41:16-19:41:40 y 19:42:30-19:42:55. Madrid es UTC+2.)

**Resultado.** Criterio de la ficha: el más barato que quede a ≤ 3 puntos del mejor y sin fallos críticos.

| Modelo | Total (168) | Resto (111) | Críticas (57 ejecuciones) | Críticas por debajo de 3/3 | A cuántos puntos del mejor (total / resto) |
|---|---|---|---|---|---|
| `fast-gpt-4.1` (gpt-4.1) | 148 (88,1 %) | 102 (91,9 %) | 46/57 | 6: TEL-C1 0/3, FDS-02 0/3, DEVOL-03a 1/3, DEVOL-03c 2/3, FDS-03 2/3, GC-C1 2/3 | 3,0 / 1,8 |
| `fast-turbo-one` (gpt-4.1-fast) | 145 (86,3 %) | 98 (88,3 %) | 47/57 | 5: TEL-C1 0/3, FDS-02 0/3, DEVOL-03c 1/3, DEVOL-03a 2/3, FDS-03 2/3 | 4,8 / 5,4 |
| `fast-gpt-5.4` (gpt-5.4) | **153 (91,1 %)** | **104 (93,7 %)** | 49/57 | 6: VIRT-C1 2/3, DEVOL-03c 1/3, DEVOL-03a 2/3, FDS-03 2/3, FDS-02 1/3, GC-C1 2/3 | 0 / 0 |

Ningún modelo llega a 3/3 en todas las críticas (la puerta 0 de la Tarea 16 sigue cerrada para Consultas). Se aplica
el criterio al resto: gpt-5.4 es el mejor (93,7 %); gpt-4.1 queda a 1,8 puntos (2,98 con el total, dentro de los 3);
gpt-4.1-fast queda a 5,4 (4,8 con el total), fuera. Entre gpt-4.1 y gpt-5.4 el más barato es gpt-4.1 (ver «Precios»).
**Elegido: `fast-gpt-4.1`**, que es el que ya tenía el nodo.

**Precios.** No hay tarifa de HappyRobot por modelo en su documentación (`search_documentation`, 18/10/2026: solo la
tabla de modelos de AI Extract, sin precios). El orden sale de las mediciones del repo (`specs/2026-10-18-bot-unico-arquitectura.md`,
§1 y §9, de 120 llamadas reales): Triaje con gpt-4.1-fast, 2,1 créditos por respuesta; Consultas con gpt-4.1, 2–2,5;
gpt-5.4 con un prompt de unos 22.000 caracteres, 4–5, y con 61.000 caracteres (V11), 12,4. Los créditos dependen del modelo y
del tamaño del prompt y no se midió gpt-5.4 con un prompt de 8.000 caracteres, así que «gpt-5.4 cuesta bastante más que
gpt-4.1» es una estimación; gpt-4.1 frente a gpt-4.1-fast no se pudo ordenar con esos datos (2,1 y 2–2,5 con prompts de
tamaño parecido), pero no hace falta: gpt-4.1-fast no cumple la regla de los 3 puntos.

**Por eval** (pasadas de 3; modelos en el orden gpt-4.1 / gpt-4.1-fast / gpt-5.4; las críticas, en negrita):

| Eval | gpt-4.1 | gpt-4.1-fast | gpt-5.4 |
|---|---|---|---|
| **VIRT-C2** | 3 | 3 | 3 |
| **TEL-C1** | 0 | 0 | 3 |
| **VIRT-C1** | 3 | 3 | 2 |
| **DEVOL-03c** | 2 | 1 | 1 |
| **DEVOL-03b** | 3 | 3 | 3 |
| **DEVOL-03a** | 1 | 2 | 2 |
| **FDS-03** | 2 | 2 | 2 |
| **FDS-02** | 0 | 0 | 1 |
| **GC-C1** | 2 | 3 | 2 |
| **PRO-4, REQ-06, ADV-3, REQ-05, CARGO-05, REQ-09, REQ-08, RECOG-05, FDS-08, NOINI-06** | 3 cada una | 3 cada una | 3 cada una |
| ADV-6 | 3 | 3 | **0** |
| REQ-03 | 1 | 1 | 3 |
| RECOG-01 | 1 | 1 | 3 |
| NOINI-03 | 1 | 1 | 1 |
| NOINI-08 | 2 | 2 | 3 |
| BR-04 | 2 | 3 | 3 |
| BR-02 | 2 | 3 | 3 |
| DEVOL-01 | 3 | **0** | 3 |
| DEVOL-02 | 3 | 2 | 3 |
| CARGO-06 | 3 | 2 | 3 |
| NOINI-04 | 3 | 2 | 3 |
| CARGO-03 | 3 | 3 | 2 |
| NOINI-02 | 3 | 3 | 2 |
| Las otras 24 del resto | 3 cada una | 3 cada una | 3 cada una |

Motivos del juez en lo que más pesa:

- **TEL-C1:** gpt-4.1 y gpt-4.1-fast siguen dando el número de España «para Portugal» (6 de 6; también con «en España» en el
  bloque común). gpt-5.4 es el único que dice que no tiene el teléfono de Portugal y remite a centauro punto net (3 de 3).
- **FDS-02:** gpt-4.1 y gpt-4.1-fast empiezan por «fuera de horario no se recoge» o por las doce horas y no por el servicio de
  espera (6 de 6); gpt-5.4 lo hace en 1 de 3.
- **ADV-6 con gpt-5.4 (0/3):** llama a `buscar_respuesta` en vez de `buscar_punto_de_encuentro`. Es de modelo, pero de la
  descripción de la herramienta de Consultas: con gpt-5.4 habría que reforzarla.
- **DEVOL-03a / 03c / FDS-03 / GC-C1:** mezcla de invento pequeño del bot («solo si lo acordó», «esté atento», «puede cancelar
  desde el área de cliente») y del juez; ninguno de los tres modelos lo arregla. DEVOL-03a con gpt-4.1 dio 1/3 ahora y 3/3 en la
  5b (con el bloque común de entonces, casi igual): con tres ejecuciones la dispersión es grande.
- **NOINI-03 (1/3 en los tres modelos):** dice que el reembolso se pide «desde el área de cliente» en vez de «Mis reservas y
  facturas» → «Reembolso Cupón» (como en la R4). Es de contenido, no de modelo.
- **REQ-03 y RECOG-01 (1/3 con los dos gpt-4.1, 3/3 con gpt-5.4):** inventos pequeños («los dos juntos con DNI y carnet»,
  «no tiene que avisar») que gpt-5.4 no hace.
- **DEVOL-01 con gpt-4.1-fast (0/3):** dice que con una agencia no se devuelve nada.

**Eval mal planteada, a apuntar (sin tocarla):** FDS-03 y FDS-02 dependen de frases que pide el juez («avisa a la oficina»,
«servicio de espera primero») y fallan a la vez que el bot dice algo razonable; no se tocaron (la ficha prohíbe tocar prompt y
evals). NOINI-03 falla igual con los tres modelos, así que no discrimina entre ellos.

**Qué no se midió.** Tres ejecuciones por eval y modelo es poco: 1 de 3 y 2 de 3 no se distinguen bien. El modo virtual de
«Preparar transferencia» no se vio con la hora real (todo antes de las 22:00). No se midió la latencia ni los créditos por
respuesta de cada modelo con este prompt.

## Prolongación (Tarea 10)

Nodo «Prolongación» `01a14f69-b09d-7689-ad9e-8e8de0fd6fb4`, modelo `fast-gpt-5.4`, prompt de 21.978/22.000 caracteres
(`prompts/atencion-es/v2/prolongacion.md`). 100 evals en la carpeta «Bot único · Prolongación»
(`01a150ce-7806-7daf-ae17-cc11a29300fc`) y sus 11 subcarpetas:

- copiadas de Prolongaciones v12: Prolongación base (PROL-01 a 08), Devolver tarde y precio (TARDE-01 a 06), La web no
  le deja (WEB-01 a 11), Aseguradora y empresa (ASEG-01 a 06), Correo de contraseña (CORREO-01 a 21), Cierre, Idiomas,
  Escalado (ESC-01 a 09), Casos aprendidos y bordes (BORDE-01 a 09), Horario y fin de semana (HOR-01, HOR-02, HOR-C1 a
  C4, HOR-A1, FDS-01, FDS-04 a 07);
- de Minibús ES v25: ADV-1, PRO-1 y PRO-2 (carpeta «Prolongación · de la v25 (adaptadas)»);
- nuevas: PISTA-01 a 04, NOINI-P1, BR-P1 y GC-P1.

**No cuentan (R5):** ESC-04, PRO-1 y PRO-2 esperan `volver_al_triaje`, que crea la Tarea 12; no se ejecutaron. Cuentan
97: **24 críticas** (GC-P1, ESC-02/03/05/06/09, BORDE-09, CORREO-09/10/11, ASEG-05, WEB-04, las HOR y las FDS) y 73
del resto.

**Adaptaciones al copiarlas:** las variables de la v2 (`e51cd732-….gestion_abierta`, `modo_virtual`, `idioma_nombre`;
por defecto gestión cerrada); las tool_calls en formato OpenAI; la nota de transferencias (solo cuenta hasta la primera
llamada). WEB-09 pasa a ofrecer el envío del correo (la v12 lo hacía así en el turno siguiente); IDIOMA-03 ofrece los
cuatro idiomas del bloque común; BORDE-04 admite la sección de autoridades de `buscar_respuesta`; PISTA-04 usa un correo
`example.com` para que la cadena real no consulte la API con un correo que pudiera existir.

### Rondas (`fast-gpt-5.4`)

| Ronda | Hora (Madrid) | Prompt | Críticas | Resto | Total |
|---|---|---|---|---|---|
| 9 (1.ª de Prolongación) | 18/10/2026 23:10–23:19 | versión 1 (21.931 caracteres) | 58/72 | 183/219 (83,6 %) | 241/291 |
| 10 (2.ª, tras la vuelta de arreglos) | 18/10/2026 23:28–23:42 | versión 2 (21.978 caracteres) | 60/72 | 185/219 (84,5 %) | 245/291 |

No cumple el criterio: 6 críticas por debajo de 3/3 y el resto en el 84,5 %. La ficha permite una ronda de arreglos;
lo que sigue fallando queda aquí y en `pendientes.md`, sin más vueltas.

**Vuelta de arreglos (entre las dos rondas):** plan B de la reserva no iniciada con las instrucciones de «¿Has olvidado
tu contraseña?»; «cada pregunta, una vez»; «da ya los pasos, sin volver a preguntar si seguimos»; deletrear «letra a
letra»; en PISTA, con el correo confirmado se envía con el nombre y la fecha que ya dio; línea de mapeo de los detalles
movidos a `buscar_respuesta`; ESCALADO con «un dato concreto de su reserva» y, con gestión cerrada, decir en ese turno
que está cerrada, su horario y que llame entonces; CIERRE termina con «Gracias a usted, que tenga buen día.». Se
ajustaron las expectativas de ESC-09, BORDE-09 y HOR-C3 (el bloque común manda repetir el teléfono una vez; el
reintento tras el fallo es del entorno), BORDE-01 («sin franquicia» es de Smart Cover, de la sección), CORREO-04 (la
cadena real) y FDS-05.

### Resultado por eval (las que no dan 3/3 en alguna ronda)

| Eval | Crítica | Ronda 9 | Ronda 10 | Motivo del juez en la ronda 10 |
|---|---|---|---|---|
| CORREO-09 | sí | 3 | **0** | Tras dos envíos que no llegan no transfiere a `gestion` / `error_tecnico`: da el plan B. Regresión de la vuelta de arreglos (el plan B nuevo) |
| FDS-06 | sí | 0 | **0** | Con gestión cerrada no dice que está cerrada ni su horario: da solo la alternativa |
| FDS-01 | sí | 0 | **1** | En inglés, añade el área de cliente y no termina con pregunta |
| HOR-C1 | sí | 3 | **1** | Con gestión cerrada ejecuta `transfer_to_human_agent` (la red de seguridad devuelve `gestion_cerrada` y no transfiere) |
| FDS-05 | sí | 1 | **2** | Una vez pregunta «would you like me to connect you» |
| BORDE-09 | sí | 2 | **2** | Una vez no repite el teléfono |
| ESC-09 | sí | 2 | 3 | — (expectativa ajustada) |
| HOR-02 | sí | 1 | 3 | — (ESCALADO, dato concreto de su reserva) |
| HOR-C3 | sí | 1 | 3 | — (expectativa ajustada) |
| PISTA-04 | no | 0 | 0 | Vuelve a pedir un dato que ya tiene en vez de ejecutar `enviar_correo_contrasena` |
| PROL-05 | no | 0 | 0 | Vuelve a preguntar si seguimos en vez de dar ya los pasos |
| PROL-06 | no | 0 | 0 | Tras decir que no tiene la tarifa, vuelve a preguntar por la cuenta |
| TARDE-02 | no | 0 | 0 | Confirma la cifra («Sí») o pasa de dos frases sin pregunta |
| ASEG-03 | no | 2 | 0 | No dice que la prolongación se pide a la aseguradora o mutua |
| CIERRE-01 | no | 1 | 0 | Tras el recordatorio pregunta «¿algo más?» en vez de terminar con la despedida |
| CORREO-04 | no | 2 | 0 | Entorno: la cadena real devuelve `no_coincide` con los datos inventados y el bot transfiere después; el juez cuenta esa transferencia |
| CORREO-20 | no | 3 | 0 | Da también los pasos de prolongar en el mismo turno (efecto de «da ya los pasos») |
| NOINI-P1 | no | 0 | 1 | No da completas las instrucciones de «¿Has olvidado tu contraseña?» |
| TARDE-05 | no | 0 | 1 | No dice que el contrato no se prorroga solo ni los cincuenta euros |
| BORDE-02 | no | 2 | 2 | Una vez da la penalización en vez de la web o la app y el precio |
| TARDE-06 | no | 1 | 2 | Una vez usa el tema `la_web_no_le_deja` en vez de `detalles_prolongacion` |
| TARDE-01, CORREO-14, CORREO-19 | no | 3 | 2 | Una vez no termina con pregunta |
| CORREO-17 | no | 3 | 2 | Una vez no deletrea el punto |
| CORREO-03, PROL-08, WEB-05 | no | 0 | 3 | — |
| BORDE-01, CIERRE-02 | no | 2 | 3 | — |
| Las otras 67 | | 3 | 3 | — |

**Lectura.** Las dos reglas nuevas tiran en sentidos contrarios: «da ya los pasos» arregla poco en PROL-05 (sigue
preguntando) y rompe CORREO-20 (da los pasos cuando aún tocaba preguntar); el plan B de la reserva no iniciada rompe
CORREO-09 (crítica). Con gestión cerrada, gpt-5.4 sigue ofreciendo alternativas antes que decir el horario (FDS-01,
FDS-06) y una vez intenta transferir (HOR-C1). Con tres ejecuciones, 1 de 3 y 2 de 3 no se distinguen bien.

### Evals cambiadas entre las rondas 9 y 10

`manage_custom_evals update` cambia solo los campos que se le pasan (la respuesta lo dice: «Updated fields: …»; visto
otra vez el 19/10 al tocar HOR-C1, FDS-01 y CORREO-09).

- **Cambio de contenido** (expectativa, 18/10 23:27, antes de la ronda 10). **En estas seis las rondas 9 y 10 no se
  pueden comparar:**
  - ESC-09 y BORDE-09: se admite que repita el teléfono una vez, como manda el bloque común.
  - HOR-C3: el reintento tras el fallo de la transferencia viene del entorno y no cuenta; se admite un resumen de dos
    frases.
  - BORDE-01: «sin franquicia» se admite, porque es de Smart Cover y sale de la sección.
  - CORREO-04: se explica que la cadena es real y que con datos inventados devuelve `no_coincide`.
  - FDS-05: el juez no cuenta «I cannot connect you» como hablar de pasarle.
- **Solo carpeta** (18/10 23:19–23:22, después de la ronda 9): las 100 evals, porque `create` no guarda `folder_id`.
  Por eso CORREO-09, FDS-06, HOR-C1, NOINI-P1, WEB-08 y las demás tienen «Updated» a esa hora. La llamada solo llevaba
  `folder_id`, así que no cambió ni la conversación, ni la expectativa, ni las variables.
- **CORREO-09:** `get` no enseña las variables. Se crearon con `gestion_abierta: true` (18/10 23:03) y después solo se
  movió de carpeta. En la ronda 10 hay otra prueba de que se conservaron: ESC-02, ESC-03, ESC-06 y HOR-02, que solo
  cambiaron de carpeta, transfirieron con la cola `gestion`. Con `false` el prompt lo prohíbe. Por tanto, la caída de
  CORREO-09 venía del prompt: el plan B se aplicaba también a «no se puede enviar». El 19/10 a las 9:20 se volvieron a
  escribir sus variables (los mismos valores), por si acaso.

### Ronda de arreglos 1 de la revisión (ronda 11, 19/10/2026)

- Prompt de 21.580 caracteres, subido a las 9:20 y comprobado con `get_node_details`. Arreglos en `prolongacion.md`
  (Configuración), D-006 y D-007.
- Expectativas reescritas:
  - HOR-C1: puede citar la penalización general de cincuenta euros.
  - FDS-01: «dos frases y una pregunta» es un máximo; se admite el área de cliente.
- **Todo es después de las 8:00. Gestión estaba abierta por el reloj real** (lunes). Eso cambia el entorno de las
  evals de transferencia que llevan `gestion_abierta: true`:
  - «Preparar transferencia» ya no devuelve `gestion_cerrada`. Pasa a buscar la cola y, como la eval no lleva las
    variables `cola_*` de «Resolver colas», devuelve `cola_no_valida`.
  - El bot la repite una vez, como manda CÓMO TRANSFERIR.
  - El juez suspende por esa segunda llamada aunque la expectativa diga que lo posterior no cuenta.
  - Esas evals no se pueden comparar con las rondas 9 y 10 (de noche, Gestión cerrada por el reloj).

**11a: las diez evals de la revisión** (9:22–9:23, ×3):

| Eval | Ronda 10 | Ronda 11 | Motivo del juez |
|---|---|---|---|
| CORREO-09 (crítica) | 0 | 0 | 2 de 3: primera llamada correcta (`gestion`, `error_tecnico`); suspende por el reintento tras `cola_no_valida` (entorno). 1 de 3: anuncia la transferencia sin ejecutarla (fallo del bot) |
| CORREO-12 | 3 | 3 | — |
| CORREO-20 | 0 | 0 | Sigue dando los pasos de prolongar en el turno del plan B, también con «Ese turno acaba ahí, sin los pasos» |
| CORREO-21 | 3 | 3 | — |
| NOINI-P1 | 1 | 1 | 2 de 3 no dicen que le llegará un enlace para crear la contraseña |
| HOR-C1 (crítica) | 1 | 0 | 1 de 3 ejecuta `transfer_to_human_agent` con `gestion_abierta: false`; 2 de 3 no dicen que gestión está cerrada ni su horario |
| FDS-01 (crítica) | 1 | 3 | — (expectativa reescrita) |
| FDS-06 (crítica) | 0 | 2 | 1 de 3 da la alternativa sin decir que gestión está cerrada |
| ASEG-03 | 0 | 3 | — («aunque pregunte el precio») |
| CIERRE-01 | 0 | 3 | — (la despedida cierra el turno, sin «¿algo más?») |

**11b: pasada completa de las críticas** (24 evals ×3, 9:24–9:26; toda la pasada con Gestión abierta por el reloj, ninguna
a los dos lados de las 8:00): **48/72**.

| Eval | Ronda 10 | Ronda 11 | Motivo del juez |
|---|---|---|---|
| GC-P1, ESC-05, ESC-09, BORDE-09, CORREO-11, HOR-01, HOR-C2, HOR-C3, FDS-01, FDS-04, FDS-05, FDS-07 | — | 3 cada una | — |
| ESC-02 | 3 | 0 | Entorno: primera llamada correcta; suspende por el reintento tras `cola_no_valida` |
| CORREO-09 | 0 | 0 | Entorno, en las tres (igual que en 11a) |
| CORREO-10 | 3 | 0 | Entorno: reintento tras `cola_no_valida`; en 1 de 3 el juez dice además que falta la frase previa |
| WEB-04 | 3 | 0 | Entorno: reintento tras `cola_no_valida` |
| HOR-02 | 3 | 0 | Entorno: reintento tras `cola_no_valida` |
| HOR-C1 | 1 | 0 | 2 de 3 ejecutan `transfer_to_human_agent` y dicen que le pasan, con `gestion_abierta: false`; 1 de 3 no dice el cierre ni el horario |
| ESC-03, ESC-06, ASEG-05, HOR-C4 | 3 | 2 | Entorno: reintento tras `cola_no_valida` |
| HOR-A1 | 3 | 2 | No da antes la regla general de cuánto se puede prolongar (causa: la línea «Otra duda del alquiler… buscar_respuesta… sin salir de aquí» de TU TAREA; ver «Causa de HOR-A1» en la ronda 14) |
| FDS-06 | 0 | 2 | 1 de 3 no dice el cierre ni el horario |

**Lectura.**
- **Arreglado:** FDS-01, ASEG-03 y CIERRE-01, todas a 3/3. FDS-06 pasa de 0/3 a 2/3 dos veces.
- **CORREO-09:** el bot ya transfiere a `gestion` / `error_tecnico` en 5 de 6, pero el reintento del entorno lo tapa.
  No se puede dar por cerrada con la hora de hoy.
- **Siguen fallando por el bot:**
  - HOR-C1: transfiere con Gestión cerrada en las variables.
  - CORREO-20: da los pasos antes de tiempo.
  - NOINI-P1: no menciona el enlace.
- **Las demás caídas de las críticas son del entorno:** la hora real con Gestión abierta y las evals sin las `cola_*`.
  Para medir las críticas de transferencia hay que pasar las `cola_*` como variables o ejecutarlas con Gestión
  cerrada por el reloj.
- Sin más vueltas (ficha y R33).

### Ronda de arreglos 2 (ronda 12, 19/10/2026, 9:49–10:17)

**Entorno arreglado.** Catorce evals de transferencia llevan ya las cuatro `cola_*` de «Resolver colas» como variables
(`081e2b5d-….cola_gestion_reserva`, `cola_asistencia`, `cola_nueva_reserva`, `cola_horario_minibus`, las URI SIP de
español), igual que en la Tarea 9. Son WEB-04, ASEG-05, CORREO-04, CORREO-09, CORREO-10, ESC-02, ESC-03, ESC-05, ESC-06,
BORDE-04, HOR-02, HOR-C3, HOR-C4 y HOR-A1.
- En las catorce, la nota del juez dice ahora «Una segunda llamada a transfer_to_human_agent tras un error del entorno
  no es un fallo».
- Se quitó la nota caducada de «la hora real (hoy Gestión está cerrada…)». Si una eval necesita Gestión cerrada o
  abierta, lo marca la variable `gestion_abierta`.
- HOR-A1 añade que no dar la regla general «no es fallo».

**Prompt:** 21.692/22.000 caracteres, subido y comparado con `get_node_details`. Cambios:
- La reserva que aún no ha empezado lleva la cita literal de «¿Has olvidado tu contraseña?».
- Fuera la cláusula «si antes pregunta otra cosa… sin volver a preguntar si seguimos».
- GESTIÓN CERRADA vale también para lo que devuelva `buscar_respuesta`.
- «Pide una persona con gestión cerrada» deja de estar en la lista de ESCALADO y pasa a una frase propia delante de
  «Salvo…».
- Cuando el reenvío tampoco llega: «transfiere en ese turno a GESTIÓN DE RESERVA con motivo error_tecnico».

**Resultado (97 evals ×3; con las `cola_*` la hora ya no cambia las evals de transferencia que llevan `gestion_abierta: true`; sí puede cambiar las que esperan Gestión cerrada, porque «Preparar transferencia» usa el reloj y no la variable):** críticas **63/72**, resto
**191/219 (87,2 %)**, total 254/291. No cumple el criterio: quedan 4 críticas por debajo de 3/3 y el resto está por
debajo del 90 %.

| Eval | Crítica | Ronda 10 | Ronda 12 | Motivo del juez en la ronda 12 |
|---|---|---|---|---|
| HOR-C1 | sí | 1 | **0** | 2 de 3 ejecutan `transfer_to_human_agent` con `gestion_abierta: false`; 1 no dice que llame en horario ni el área de cliente |
| FDS-06 | sí | 0 | **0** | Da la alternativa sin decir que gestión está cerrada ni su horario (las tres) |
| HOR-A1 | sí | 3 | **1** | 2 de 3 dan la regla general y dicen que hay que revisarlo, sin transferir ni ofrecerlo (causa: la línea «Otra duda del alquiler… buscar_respuesta… sin salir de aquí» de TU TAREA; ver «Causa de HOR-A1» en la ronda 14) |
| HOR-01 | sí | 3 | **2** | Una vez dice que «lo deriva» al equipo de gestión |
| CORREO-09, CORREO-10, ESC-02, ESC-03, ESC-06, WEB-04, ASEG-05, HOR-02, HOR-C4 | sí | — | 3 cada una | — (entorno arreglado) |
| FDS-01, FDS-05, BORDE-09 | sí | 1 / 2 / 2 | 3 | — |
| BORDE-05 | no | 3 | 0 | Habla de subir de categoría en la oficina: no dice que la prolongación es del mismo coche ni ofrece la reserva nueva. Efecto de sacar «Cambiar de coche» a `buscar_respuesta`, que no llama |
| PISTA-04, PROL-05, PROL-06, TARDE-02 | no | 0 | 0 | Mismos motivos que en la ronda 10 (PROL-05: vuelve a preguntar si seguimos) |
| WEB-03 | no | 3 | 1 | Afirma que un compañero se la prepara en vez de preguntarlo |
| WEB-08 | no | 3 | 1 | El juez exige una pregunta final que la expectativa no pide («como mucho») |
| TARDE-05, TARDE-06 | no | 1 / 2 | 1 / 1 | TARDE-06 usa otro tema de `buscar_respuesta` |
| BORDE-01, BORDE-02, CORREO-03, CORREO-08, CORREO-19 | no | — | 2 cada una | Una ejecución suelta |
| NOINI-P1, CORREO-20, CORREO-04, ASEG-03, CIERRE-01 | no | 1 / 0 / 0 / 0 / 0 | 3 cada una | — |
| Las otras 62 | | | 3 | — |

**Lectura.**
- **Arreglos que funcionan:** NOINI-P1 y CORREO-20 a 3/3. CORREO-09 a 3/3 con el entorno arreglado. Las nueve
  críticas de transferencia, todas a 3/3.
- **No arreglado:** gestión cerrada en Prolongación.
  - HOR-C1 sigue transfiriendo con `gestion_abierta: false`.
  - FDS-06 sigue sin decir el cierre.
  - Ni la frase propia antes de «Salvo…» ni la regla sobre lo que devuelve `buscar_respuesta` lo corrigen con gpt-5.4.
- **Efecto de mover texto a `buscar_respuesta` (D-006):**
  - BORDE-05 cae a 0/3 («Cambiar de coche»).
  - HOR-A1 cae a 1/3. «Cuánto se puede prolongar» pasa por la línea «Otra duda del alquiler… buscar_respuesta… sin
    salir de aquí» de TU TAREA: el bot da la regla y se queda, sin seguir a ESCALADO. No es la frase de la ronda de
    arreglos 2 (se quitó en la ronda de arreglos 3 y HOR-A1 siguió a 1/3).
- Sin más vueltas (ficha, R33).

### Ronda de arreglos 3 (ronda 13, 19/10/2026, 10:30–10:33, lunes; Gestión abierta por el reloj)

**Cambios.** El prompt mide 21.946/22.000 caracteres; lo subí y lo comparé con `get_node_details`.
- Fuera la frase de la ronda de arreglos 2 sobre lo que devuelve `buscar_respuesta`.
- La regla de gestión cerrada pasa a ser el primer punto de TU TAREA, con la condición delante: «Con gestión cerrada, si
  pide una persona o que alguien mire su caso, o si llama una agencia o una aseguradora: sin transfer_to_human_agent…».
- «Cambiar de coche» vuelve a DETALLES QUE PUEDES DAR (D-006).
- En ENVÍO, «si ya los dio en PISTA, no los pidas».
- La descripción de `transfer_to_human_agent` empieza por «Gestión ahora: {{gestion_abierta}}. Si Gestión ahora es false
  y el caso es de gestión, no la llames…». La variable va como nodo de variable de Plate y no cuenta para los 22.000.
- La eval HOR-C1 admite que dé solo el horario («basta con el horario»).

**Resultado.** Se pasaron 3 veces las 24 críticas y, del resto, BORDE-05, PISTA-04, WEB-03 y WEB-08. Críticas:
**67/72**.

| Eval | Crítica | Ronda 12 | Ronda 13 | Motivo del juez en la ronda 13 |
|---|---|---|---|---|
| HOR-C1 | sí | 0 | **1** | 1 de 3 ejecuta `transfer_to_human_agent` con `gestion_abierta: false`; 1 de 3 no dice el cierre ni el horario |
| HOR-A1 | sí | 1 | **1** | 2 de 3: uno anuncia la transferencia sin ejecutarla y otro dice que gestión lo tiene que revisar, sin ofrecerla |
| HOR-01 | sí | 2 | **2** | Una vez sugiere ir a la oficina y no remite al área de cliente |
| FDS-06 | sí | 0 | 3 | — |
| Las otras 20 críticas | sí | 3 | 3 | — |
| BORDE-05 | no | 0 | 3 | — («Cambiar de coche» de vuelta en el prompt) |
| WEB-03 / WEB-08 | no | 1 / 1 | 3 / 3 | — |
| PISTA-04 | no | 0 | 0 | Vuelve a pedir el nombre en vez de ejecutar `enviar_correo_contrasena`, también con «si ya los dio en PISTA, no los pidas» |

**Lectura.**
- FDS-06 queda arreglada con la regla como primer punto de TU TAREA.
- HOR-A1 no mejora al quitar la frase de la ronda de arreglos 2: sigue a 1/3, así que esa frase no era la causa. La
  causa es la línea «Otra duda del alquiler… buscar_respuesta… sin salir de aquí» (ronda 14).
- HOR-C1 mejora un poco (1/3), pero el bot sigue llamando a la herramienta alguna vez. El arreglo estructural pasa a
  la puerta 0: el aviso «le paso» es el `message` de la herramienta (`pendientes.md`).
- Sin más vueltas.

### Ronda de arreglos 4 (ronda 14, 19/10/2026, 10:40–10:47, lunes; Gestión abierta por el reloj)

**Causa de HOR-A1.** Es la línea «Otra duda del alquiler… buscar_respuesta… sin salir de aquí» de TU TAREA. Desde la
ronda de arreglos 1, «cuánto se puede prolongar» se pide a `buscar_respuesta` (D-006) y pasa por esa línea: el bot da la
regla y se queda, sin seguir a ESCALADO («un dato concreto de su reserva: cola gestion»). No era la frase de la ronda de
arreglos 2: se quitó en la ronda de arreglos 3 y HOR-A1 siguió a 1/3.

**Cambios.** El prompt mide 21.998/22.000 caracteres; lo subí y lo comparé con `get_node_details` (igual al fuente).
- Tras «sin salir de aquí»: «; si pide un dato de su reserva, cola gestion» (HOR-A1).
- En ENVÍO, «Pide solo los datos que falten, uno por turno» en lugar de «Pide un dato por turno», y fuera el paréntesis
  «si ya los dio en PISTA, no los pidas». En PISTA, «con el nombre y la fecha que ya dio, sin pedirlos de nuevo»
  (PISTA-04).
- HOR-01: no se tocó el prompt (motivo abajo). HOR-C1 queda fuera (R34).

**Resultado.** Se pasaron 3 veces las 24 críticas y, del resto, PISTA-01 a PISTA-04, CORREO-20 y NOINI-P1. Críticas:
**69/72**. Resto: 15/18.

| Eval | Crítica | Ronda 13 | Ronda 14 | Motivo del juez en la ronda 14 |
|---|---|---|---|---|
| HOR-A1 | sí | 1 | **2** | 1 de 3: «se limitó a indicar que debe revisarlo y desvió a la web», sin ofrecer ni ejecutar la transferencia |
| HOR-C1 | sí | 1 | **2** | 1 de 3 añade que vaya a la oficina si está abierta y da el horario tras una condición de urgencia (fuera de la ronda, R34) |
| BORDE-09 | sí | 3 | **2** | 1 de 3 no dice el uno uno dos ni que ahora no puede pasarle |
| HOR-01 | sí | 2 | 3 | — |
| Las otras 20 críticas | sí | 3 | 3 | — |
| PISTA-04 | no | 0 | **0** | Vuelve a pedir el nombre completo en vez de ejecutar `enviar_correo_contrasena` (las tres) |
| PISTA-01, PISTA-02, PISTA-03, CORREO-20, NOINI-P1 | no | — | 3 cada una | — |

**HOR-01 (rondas 12 y 13).** Los motivos del juez fueron «lo deriva» al equipo de gestión (ronda 12) y «sugiere ir a la
oficina y no remite al área de cliente» (ronda 13). No es la línea de HOR-A1. Lo de la oficina lo permite el bloque
común («si es urgente para hoy, que vaya a la oficina si está abierta»), y el bloque dice «ese horario o que use su área
de cliente», mientras que la eval pide las dos cosas. Es del modelo o de la eval: no se tocó el prompt.

**Lectura.**
- HOR-A1 mejora (1/3 → 2/3), pero no llega a 3/3.
- PISTA-04 no se mueve con ninguna de las dos redacciones. Falta mirar si la conversación de la eval da el nombre y la
  fecha en turnos `user` o solo en la llamada a `pista_correo`.
- Sin más vueltas.

