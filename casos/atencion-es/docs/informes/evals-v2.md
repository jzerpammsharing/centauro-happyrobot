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

### Modelos

**Pendiente.** Por decisión del controlador (pedida por el responsable para acabar antes), la Tarea 9 no hace la
comparación de modelos del spec §7.3 (gpt-4.1, gpt-4.1-fast y gpt-5.4; quedarse con el más barato a ≤ 3 puntos del mejor
y sin fallos críticos). El nodo queda con `fast-gpt-4.1`. La comparación se hace en una sesión posterior, antes de la
Tarea 16 (`docs/pendientes.md`).

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
