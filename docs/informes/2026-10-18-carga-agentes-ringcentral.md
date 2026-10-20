# Llamadas al día, agentes necesarios e impacto de la IA en plantilla (RingCentral)

Análisis de solo lectura del 18/10/2026. No se ha cambiado nada en RingCentral ni en HappyRobot.

## Fuentes y método
- **RingCentral:** registro de llamadas de todas las colas de atención de España, Italia y Portugal.
  - Jueves 15/10, día laborable con los bots funcionando: todas las colas.
  - Sábado 10/10: Gestión, Nueva Reserva, Minibús, Prolongación y Averías de España.
  - Jueves 01/10, antes del bot de Prolongaciones (empezó el 05/10): Gestión ES y EN, Minibús y
    Prolongación.
  - En total, 2.929 registros, extraídos por subagentes a CSV sin teléfonos ni nombres.
- **Tiempo de atención:** 55 llamadas atendidas del 15/10, leídas en detalle (patas de cada agente).
  Gestión ES 18057, Gestión EN 18061, Nueva Reserva ES 18001 y Averías ES 18034.
- **Bots:** informes diarios de los artefactos «Calidad Prolongaciones» y Minibús.
- **Cálculo de agentes:**
  - Erlang C por hora, con objetivo de 80 % de llamadas atendidas en 30 s.
  - Tiempo por llamada = conversación media + 30 s de trabajo posterior (supuesto).
  - Se suponen grupos de agentes compartidos por país (en la muestra, varios agentes atienden más de una
    cola).
  - Script: `scripts/carga_colas_ringcentral.py`.
- **Colas sin llamadas desde septiembre:** las antiguas de España (18002, 18004, 18030, 18045 a 18051) y
  las de Prolongación (18058 y 18062). Antes del bot, la opción de prolongar ya iba a Gestión (18057).

## 1. Cuántas llamadas se reciben al día (jueves 15/10)

| Grupo | Colas | Llamadas a colas | Las pasa un bot | Atendidas por agente | Perdidas | De ellas, colgadas en la bienvenida |
|---|---|---|---|---|---|---|
| ES atención | Gestión ES/EN, Nueva Reserva ES/EN, Minibús ES/EN | 1.004 | 103 | 801 | 158 | 133 |
| ES asistencia | Averías y accidentes ES/EN | 78 | 6 | 72 | 6 | 0 |
| Italia | Mod. Reserva, Nuova Prenotazione, Minibús | 315 | 37 | 246 | 55 | 15 |
| Portugal | Alteração, Management, Minibús | 142 | 9 | 110 | 22 | 7 |
| **Total colas** | | **1.539** | **155** | **1.229** | **241** | **155** |

El resto de registros (69) son llamadas fuera de horario que solo oyen el anuncio de cerrado.

- **Cuánto atiende la IA (HappyRobot) ese día:** 329 llamadas, 243 de Minibús (ES 128, IT 95, PT 20) y
  86 de Prolongaciones. Unas **174 terminan sin pasar a un agente**.
- **Llamadas de clientes al día:** unas **1.700**, sumando las 1.384 que entran directas en las colas y
  las 329 de los bots. La IA atiende el 19 % y resuelve sola el 10 %.
- **La cola que más llama es Gestión ES (18057):** 530 registros.
  - De las 148 perdidas, **130 cuelgan antes de 40 s**: los agentes empiezan a sonar a los ~37 s, así que
    se van durante la bienvenida, antes de que suene nadie. Solo 11 se pierden esperando a un agente.
  - Las pérdidas de Gestión no son por falta de agentes, sino por la bienvenida.
- **Fin de semana (sábado 10/10):**
  - Gestión ES y EN recibieron 504 llamadas y se perdieron todas, porque solo suena el anuncio de cerrado.
  - Nueva Reserva atendió 237 de 250.
  - Los bots atendieron 374: Minibús 252 y Prolongaciones 122.
- **Por carga de trabajo, Nueva Reserva (18001) pesa más que Gestión:** 304 atendidas de unos 4,5 min,
  unas 26 h de trabajo al día frente a las 21 h de Gestión.
- **Qué llega a Nueva Reserva.** Hay dos estudios y no coinciden:
  - el equipo comentó el 18/10 que el 80 % de las llamadas son gestiones y el 20 % reservas nuevas;
  - el análisis de automatización de 299 llamadas de Nueva Reserva ES, del 25/09 al 01/10
    (`analisis-automatizacion-2026-10-03-trabajo262.xlsx`, fuera del repo), da **61 % de intención de
    reserva nueva y 39 % de gestiones** de reservas que ya existen.
  - Dentro de ese 61 %, algo más de la mitad acaban con el agente pidiendo los datos para crear la reserva
    (un 31–35 % del total); el resto son consultas previas de precio, disponibilidad o condiciones. Puede
    que el 80/20 cuente como «gestión» todo lo que no acaba en reserva, pero ni así cuadra: saldría 65–69 %
    frente a 31–35 %.
  - En este informe se usa el reparto del Excel, que es el medido: con el volumen del 15/10, unas 129
    gestiones al día entran por Nueva Reserva. Las gestiones de atención al cliente en España son así unas
    **584 llamadas al día, el 71 % de la demanda**.
  - Una explicación probable de las gestiones en ventas: Nueva Reserva contesta enseguida (el primer agente
    suena a los 1,6 s y casi no pierde llamadas), y Gestión hace esperar 37 s de bienvenida y pierde el 28 %.
    Se puede comprobar contando cuántos números cuelgan en la bienvenida de Gestión y llaman a Nueva
    Reserva en los minutos siguientes (con los números cifrados).

## 2. Tiempo de atención (muestra del 15/10)

| Cola | Conversación media / mediana | Espera hasta que suena el agente |
|---|---|---|
| Gestión ES 18057 | 178 s / 143 s | 56 s de media (bienvenida de ~37 s) |
| Gestión EN 18061 | 283 s / 210 s | 37 s |
| Nueva Reserva ES 18001 | 277 s / 250 s | 22 s |
| Averías ES 18034 | 603 s / 572 s | 19 s |

En 49 llamadas atendidas aparecen **26 agentes distintos**, varios en más de una cola. Es decir, al teléfono
hay más personas que las que exige el volumen, repartiendo su tiempo. Sin datos de conexión de los agentes
no se puede saber cuánto tiempo dedican al teléfono.

## 3. Cuántos agentes se necesitan (80 % en 30 s, sin contar los que cuelgan en la bienvenida)

| Grupo (15/10) | Horario | Llamadas | Horas de trabajo | Horas-agente necesarias | Pico |
|---|---|---|---|---|---|
| ES atención | 8 a 22 h | 826 | 59,6 | 97 | 9 agentes (11 h y 17 h) |
| ES asistencia | 24 h | 78 | 13,7 | 39 | 4 |
| Italia | 8 a 22 h | 284 | 20,5 | 49 | 5 |
| Portugal | 8 a 22 h | 125 | 9,0 | 30 | 3 |
| **Total** | | **1.313** | **103** | **215** | |

- 215 horas-agente al teléfono son unos 27 turnos de 8 h dedicados solo a llamadas.
- Con un 30 % de merma (descansos, formación, ausencias), salen **unas 38 jornadas de 8 h un día
  laborable**.
- Agentes necesarios en ES atención, hora a hora:

| Hora | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Llamadas | 31 | 71 | 58 | 80 | 70 | 64 | 70 | 55 | 62 | 81 | 71 | 56 | 38 | 19 |
| Agentes | 4 | 8 | 7 | 9 | 8 | 7 | 8 | 7 | 7 | 9 | 8 | 7 | 5 | 3 |

## 4. Lo que ya ahorra la IA

- **Sin los bots**, las ~174 llamadas que resuelven solos irían a agentes:
  - ES atención pasaría de 97 a 108 horas-agente (pico de 9 a 10);
  - Italia, de 49 a 54 (pico de 5 a 6);
  - Portugal casi no cambia.
- **Ahorro hoy: unas 16 horas-agente al día.** Equivale a 2 agentes en turno o, con la merma, a unas 3
  jornadas diarias. En una semana de 7 días, unas **4 personas a jornada completa**. Ya quita 1 agente
  en la hora pico de España y de Italia.
- **Gestión antes y después**, comparando dos jueves (Gestión ES/EN y Minibús):
  - el 01/10 hubo 874 llamadas y 630 atendidas, unas 40 h de trabajo;
  - el 15/10, 654 llamadas y 475 atendidas, unas 30 h;
  - son unas 10 h de trabajo menos al día. El bot de Prolongaciones explica unas 3 h (unas 46 llamadas
    resueltas al día). El resto es probablemente la temporada: el 01/10 es principio de mes y en octubre
    baja el volumen.
  - Sin una cola de control no se puede separar del todo.

## 5. Escenarios con los casos previstos (ES atención, jueves tipo)

### Gestiones (reservas que ya existen)
Son unas 584 llamadas al día: 455 en Gestión ES/EN y unas 129 que entran por Nueva Reserva (39 % de esa
cola, según el Excel de automatización). Escenarios según el porcentaje de esas gestiones que resuelva la IA
sin agente:

| La IA resuelve | Llamadas que deja de atender un agente | Horas-agente al día | Pico | Ahorro frente a hoy | Jornadas al día |
|---|---|---|---|---|---|
| Hoy | — | 97 | 9 | — | — |
| 20 % de las gestiones | 117 | 87 | 8 | 10 h | 1,8 |
| 30 % | 175 | 83 | 7 | 14 h | 2,5 |
| 40 % | 233 | 76 | 7 | 21 h | 3,8 |
| 50 % | 292 | 71 | 6 | 26 h | 4,6 |

- **Referencias medidas:**
  - Prolongaciones resuelve hoy el 38 % de sus llamadas y Minibús el 47 %.
  - Con las respuestas nuevas y el MCP, Prolongaciones podría llegar al 53 %
    (`2026-10-17-respuestas-daniel-vs-bots.md`).
  - Para el conjunto de las gestiones, un 30–40 % es razonable.
- **Condición:** que la IA atienda también las gestiones que entran por la opción de Nueva Reserva. Por
  ejemplo, con una pregunta de triaje («¿tiene ya una reserva con nosotros?») que pase las gestiones a los
  bots y deje las reservas nuevas a los agentes de ventas.
- Reembolsos (fianza, combustible y reembolsos, un 36 % de las gestiones en septiembre) es una parte de este
  ahorro, no un ahorro aparte.

### Nueva Reserva según lo que necesitaría la IA (Excel, 299 llamadas)

| Nivel | Llamadas | Tiempo de agente | Qué hace falta |
|---|---|---|---|
| 1. Solo conocimiento | 19 % | 11 % | Lo que ya tienen los bots (condiciones, requisitos, oficinas) |
| 2. Leer la reserva o los cargos | 15 % | 13 % | MCP de reembolsos y reservas (`consultar_reserva`, `consultar_reembolso`) |
| 3. Ver disponibilidad o crear y cambiar reservas | 57 % | 64 % | Integración con el motor de reservas (hoy no existe) |
| 4. Persona o traspaso | 10 % | 12 % | Reclamaciones, decisiones, seguridad |

- **Con lo que ya hay (niveles 1 y 2):** un 34 % de las llamadas y un 24 % del tiempo. Si la IA resolviera
  el 55 %, serían unas 62 llamadas menos al día en Nueva Reserva y unas 8 horas-agente.
- **El salto grande está en el nivel 3:** las reservas nuevas y los cambios necesitan consultar
  disponibilidad y escribir en el motor de reservas. Con esa integración se llegaría al 91 % de las
  llamadas automatizables; al 55 % de resolución, unas 165 llamadas menos al día y unas 13–15
  horas-agente.
- **El propio Excel lo ve viable:** 91 % de las llamadas automatizables (17 % totalmente, 74 % con
  consulta a sistemas), riesgo bajo en el 90 % y criterio humano solo en el 7 %.

### Cuánto se puede automatizar y cuántos agentes, por fases

Los agentes no modifican reservas: igual que en Prolongaciones, mandan al cliente a la web y, si hace
falta, le ayudan a recuperar la contraseña. Por eso las modificaciones entran ya en la fase 2, que es lo que
hace hoy el bot de Prolongaciones (y la v12 con el envío del correo de contraseña).

Cada fase añade herramientas a la anterior. «Automatizable» es lo que la IA podría hacer con esas
herramientas; el ahorro realista supone que resuelve el 65 % de eso.

**Nueva Reserva** (Excel de 299 llamadas; hoy necesita 57 horas-agente un día laborable, con pico de 5):

| Fase | Qué se añade | Automatizable (llamadas / tiempo) |
|---|---|---|
| 1 | Entrenar al bot con las respuestas (condiciones, requisitos, coberturas, oficinas) | 19 % / 11 % |
| 2 | + MCP de lectura (reserva y cargos) y envío del correo de contraseña; modificar = pasos de la web | 47 % / 37 % |
| 3 | + precio y disponibilidad, y enlace para terminar la reserva en la web | 58 % / 45 % |
| 4 | + crear la reserva con pago desde el bot | 90 % / 88 % |

El 10 % de las llamadas (12 % del tiempo) seguirá necesitando a una persona: reclamaciones, decisiones y
seguridad. El 43 % del tiempo son llamadas en las que el agente hace la reserva nueva: eso solo se
automatiza en la fase 4, o en parte en la 3 si el cliente acaba la reserva con el enlace.

**Todo el centro de atención de 8 a 22 h** (España, Italia y Portugal), encima de lo que ya ahorran los
bots actuales. Supone que la IA resuelve el 50 % de las llamadas de Gestión en las fases 2 y 3 y el 55 %
en la 4 (Prolongaciones: 38 % hoy y 53 % posible con las mejoras), y en Italia y Portugal el mismo
porcentaje que en España:

| Fase | Llamadas menos para agentes (España) | Horas-agente al día menos (ES / IT / PT) | Personas equivalentes |
|---|---|---|---|
| 2 | 307 (37 %) | 26 / 11 / 5 | unas 9 |
| 3 | 324 (39 %) | 28 / 11 / 5 | unas 10 |
| 4 | 439 (53 %) | 39 / 17 / 7 | unas 14 |

- **Cómo se calcula:** contratos de 40 h, 30 % de merma y servicio de 7 días; el fin de semana, como un
  65 % de un día laborable.
- **Italia y Portugal:** su ahorro necesita bots en italiano y portugués para las gestiones; hoy solo
  tienen Minibús.
- **Ya en marcha:** a esto se suman las unas 4 personas que ya ahorran los bots actuales.
- **Con turnos reales:** son cifras de capacidad con turnos perfectamente flexibles. Con los turnos fijos
  del cuadrante y sin automatizar la creación de reservas, las cifras son las del apartado siguiente
  (~8–9 personas).

### El cuadrante de la plantilla frente a lo que piden las llamadas

Fuente: `Plantilla_Cuadrantes_CallCenter_3.xlsx` (cuadrante de septiembre a diciembre; fuera del repo, lleva
nombres). Grecia no la atiende este centro.

**Plantilla del cuadrante:** 60 personas activas.
- 38 agentes de 40 h, 13 de jornada reducida (28 h), 6 de coordinación y 3 de noche (de 0 a 8 h).
- El equipo habla de 70 personas; la diferencia puede ser el grupo de asistencia, que no está en el
  cuadrante.
- **Turnos:** mañana 8–16, 10–18 y reducida 8–15; tarde 14–22 y reducida 15–22; noche 0–8; formación sin
  llamadas.
- **Mínimos fijados:** entre semana, 20 de mañana y 14 de tarde; el fin de semana, 8 y 9; de noche, 2.
- **Horas programadas:** en octubre, unas 1.640 horas-persona a la semana de 8 a 22 h, sin contar
  coordinación ni noche. Es el 87 % de las horas de contrato; el resto son vacaciones, bajas y ausencias.

**Personas en turno frente a personas necesarias, jueves 15/10** (España, Italia y Portugal juntos; las
necesarias son las de Erlang divididas entre 0,85 por pausas dentro del turno):

| Hora | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| En turno (cuadrante) | 19 | 19 | 19 | 19 | 19 | 19 | 30 | 26 | 12 | 12 | 12 | 12 | 12 | 12 |
| Agentes necesarios (Erlang) | 7 | 13 | 13 | 16 | 13 | 14 | 14 | 14 | 14 | 15 | 14 | 12 | 10 | 7 |

- **La plantilla está cargada por la mañana y corta por la tarde.**
  - De 8 a 14 h entran 374 llamadas en España y de 14 a 22 h, 452.
  - Aun así, hay 19 personas de mañana y 12 de tarde, y los mínimos fijados son 20 y 14.
  - De 16 a 19 h faltan unos 4–6 agentes. Es la franja en la que Gestión pierde el 43–45 % de las
    llamadas directas.
- **Con turnos fijos de 8 h, la meta de 80 % en 30 s pediría unas 54 personas de 40 h**: entre semana, 19
  de mañana y 18 de tarde; el fin de semana, 12 y 12.
  - El cuadrante equivale a unas 47 personas de 40 h.
  - Hoy no sobra gente en conjunto: falta por la tarde y está justo por la mañana.
  - La cifra de 39 personas del apartado anterior era el mínimo con turnos perfectamente flexibles, no la
    referencia con los turnos reales.

**Potencial de la IA sin automatizar la creación de reservas**

La creación de reservas nuevas se deja a los agentes, porque venden mejor. Lo del Excel de Nueva Reserva
de España se extrapola a Nueva Reserva de Italia; en Gestión de los tres países, la IA resuelve el 50 %.

| Escenario | Personas en turno necesarias (L–V mañana / tarde) | Horas a la semana | Personas de 40 h | Frente al cuadrante actual |
|---|---|---|---|---|
| Hoy, para cumplir 80/30 | 19 / 18 | 1.864 | ~54 | faltan ~6 (la tarde) |
| IA sin dar precio ni crear reservas | 13 / 15 | 1.424 | ~41 | ~6 menos |
| **IA en todo menos crear reservas** | **13 / 13** | **1.344** | **~39** | **~8–9 menos** |
| IA también creando reservas (referencia) | 11 / 12 | 1.192 | ~34 | ~13 menos |

- **Lo primero que hace la IA es cubrir el hueco de la tarde** (unas 6 personas que hoy faltan para la
  meta). Después de eso empieza la reducción.
- **Con todo menos crear reservas** se podrían planificar unas 8–9 personas de 40 h menos que en el
  cuadrante de octubre, cumpliendo además la meta de 80/30. Es el 17 % de los 51 agentes.
- **Reequilibrar mañana y tarde sirve ya, sin IA:** pasar unas 4–6 personas de mañana a tarde reduciría
  las pérdidas de la tarde sin aumentar la plantilla.
- **Asistencia 24 h:** con 78 llamadas al día de unos 10 minutos y al menos 1 agente de noche, harían falta
  unas **10 personas**. El cuadrante tiene 3 de noche; el resto del grupo de asistencia no está en el Excel.

### ¿Se puede automatizar el 50 % del centro sin crear reservas?

Llamadas que llegan a agentes un jueves (España, Italia y Portugal, sin las que cuelgan en la bienvenida):
1.235. De ellas, 754 son de Gestión, 410 de Nueva Reserva y 71 las pasan los bots de Minibús.

| Escenario | Llamadas que resuelve la IA | Trabajo de agentes que quita | Personas de 40 h necesarias |
|---|---|---|---|
| Hoy, para cumplir 80/30 | — | — | ~54 (el cuadrante equivale a ~47) |
| Realista: Gestión al 50 %, Nueva Reserva al 65 % de lo automatizable | 43 % | 39 % | ~39 |
| **50 % de las llamadas: Gestión al 64 %, Nueva Reserva al 65 %** | **52 %** | **47 %** | **~36** |
| Techo: todo lo automatizable sin crear reservas | 62 % | 56 % | ~33 |

- **Como potencial, sí.** Sin crear reservas es automatizable el 62 % de las llamadas: en Nueva Reserva,
  todo menos la creación y lo que necesita una persona (58 %); en Gestión, un 70 %, porque los agentes
  también mandan los cambios a la web.
- **Para que la IA resuelva el 50 %** tiene que cerrar sola el 64 % de las llamadas de Gestión.
  - Hoy Minibús cierra el 47 % y Prolongaciones el 38 %; con las mejoras y el MCP, el 53 %.
  - Hace falta además el triaje en la opción de Nueva Reserva, el envío de la contraseña, la consulta de la
    reserva y los cargos, y WhatsApp para los datos difíciles de dictar.
- **Contando todo el centro**, también lo que ya resuelven los bots, ese escenario deja en la IA cerca de
  la mitad de las llamadas de clientes: unas 640 nuevas más las 174 de hoy, de unas 1.700 al día.
- **El 50 % de las llamadas no es el 50 % de la plantilla.**
  - Lo que queda en manos de agentes son las llamadas más largas (crear reservas y reclamaciones).
  - Los turnos son fijos de 8 h y hay que cubrir cada hora.
  - Hoy ya faltan unas 6 personas por la tarde.
  - Con el 50 % de llamadas, las personas necesarias pasan de ~54 a ~36 (un 33 % menos que lo que pide la
    meta) y quedan unas 11 por debajo del cuadrante actual (un 23 % menos).

### Ahorro en dinero y coste de HappyRobot

**Coste de una persona a jornada completa con el salario mínimo de 2026:**
- 1.221 € al mes en 14 pagas, 17.094 € al año (Real Decreto 126/2026).
- Con un 32 % de cotizaciones de empresa, unos **22.600 € al año**.
- Es un mínimo: el salario real por convenio será mayor.

**Minutos de HappyRobot**, medidos en Twin con todas las llamadas de cada bot:

| Bot | Sin transferir | Transferida |
|---|---|---|
| Prolongaciones | 1,7 min | 6,2 min (el bot sigue en la llamada mientras habla el agente) |
| Minibús España | 2,0 min | 3,3 min |
| Minibús Italia y Portugal | 1,2–1,3 min | 0,7–0,8 min (el bot suelta la llamada) |

**Supuestos del cálculo:**
- La IA hace de puerta de entrada de Gestión y de Nueva Reserva (con el triaje) en los tres países.
- Una llamada resuelta por la IA dura 2,5 min, porque identificar al cliente con el MCP alarga la llamada.
- Una transferida cuesta 1,2 min si el bot suelta la llamada y 6,2 min si se queda.
- El año tiene 52 semanas de 6,3 días laborables equivalentes.
- Se cuenta solo el coste añadido sobre lo que ya gastan los bots actuales: unos 257.000 min al año, entre
  28.000 y 51.000 €.

| Escenario | Personas menos | Ahorro bruto (más las 7 que no se contratan) | Coste extra de HappyRobot (0,11–0,20 €/min), si el bot suelta la llamada | Ahorro neto, si suelta | Coste extra, si se queda en la llamada | Ahorro neto, si se queda |
|---|---|---|---|---|---|---|
| Realista (43 %) | 8 | 181.000 € (339.000 €) | 66.000–119.000 € | 62.000–115.000 € (219.000–273.000 €) | 192.000–350.000 € | −169.000 a −12.000 € (−11.000 a 146.000 €) |
| Objetivo (50 %) | 11 | 248.000 € (406.000 €) | 71.000–129.000 € | 119.000–177.000 € (277.000–335.000 €) | 178.000–323.000 € | −75.000 a 71.000 € (83.000–228.000 €) |
| Techo (62 %) | 14 | 316.000 € (474.000 €) | 77.000–139.000 € | 177.000–239.000 € (335.000–397.000 €) | 161.000–293.000 € | 23.000–155.000 € (181.000–313.000 €) |

- **Facturación comprobada con la API de HappyRobot** (créditos por run, 18/10):
  - Tres llamadas: Minibús v25, 148 s, transferida a los 28 s; Minibús v22, 147 s, sin transferir;
    Prolongaciones V11, 889 s, transferida a los 43 s.
  - Tras la transferencia se sigue cobrando «Voice Orchestration», a unos 4,1–4,4 créditos por minuto,
    frente a 11–13 créditos por minuto mientras habla el bot (un 35 % aprox.). El LLM no se cobra
    después de la transferencia.
  - El LLM es lo más caro y depende del tamaño del prompt y del modelo: 1,5 créditos por turno del bot en
    el Triaje de Minibús v25, 8,8 en Minibús v22 y 9,9 en Prolongaciones, cuyo prompt tiene unos 61.000
    caracteres.
  - En la llamada de Prolongaciones, el 42 % de los créditos (unos 57 de 137) son de escuchar al agente.
  - Falta el precio del crédito en euros para pasar todo esto a dinero.
- **Lo que decide el caso es cómo transfiere el bot.** Si se queda en la llamada mientras habla el agente,
  como hace hoy Prolongaciones, se pagan también los minutos del agente y el ahorro puede desaparecer
  a 0,20 €/min.
- Hay que confirmar con HappyRobot cómo factura esos minutos y usar una transferencia que suelte la llamada,
  como la de Minibús Italia y Portugal, sobre todo en el triaje de Nueva Reserva.

### Ahorro contando las contrataciones evitadas (frente a atender bien sin IA)

Las 7 personas que hoy faltan por la tarde se cuentan como coste evitado: sin IA habría que contratarlas
para cumplir 80/30. La referencia es entonces lo que costaría atender bien sin IA: 54 personas de 40 h
(unos 1,22 millones de euros con salario mínimo) más lo que ya cuesta HappyRobot.

| Escenario | Personas (reducción + contrataciones evitadas) | Ahorro bruto | Ahorro neto (bot que suelta la llamada) | % del coste de atender bien sin IA |
|---|---|---|---|---|
| Realista (43 %) | 15 (8 + 7) | 338.000 € | 219.000–273.000 € | 17–22 % |
| Objetivo (50 %) | 18 (11 + 7) | 406.000 € | 277.000–335.000 € | 22–27 % |
| Techo (62 %) | 21 (14 + 7) | 474.000 € | 335.000–397.000 € | 26–32 % |

**Coste por llamada:**
- Una llamada atendida por un agente cuesta unos 1,50 € con salario mínimo: 4,3 min con el trabajo
  posterior, 70 % de ocupación, pausas y ausencias.
- Una resuelta por la IA cuesta 0,28–0,50 € (2,5 min a 0,11–0,20 €/min).

**Si crece la demanda:**
- Con un 20 % más de llamadas, sin IA harían falta unas 65 personas (11 más).
- Con la IA al 50 % harían falta unas 43 (7 más) y unos 20.000–36.000 € más de HappyRobot.

**Qué medir para demostrarlo:**
- Calidad del servicio: % de llamadas atendidas en 30 s, llamadas perdidas esperando a un agente (sobre
  todo de 17 a 21 h), espera media y rellamadas en 48 h.
- Crecimiento: llamadas y horas de agente por cada 1.000 alquileres, y coste por contacto (agente frente
  a IA).

## 6. Cuándo se traduce en menos personal

El ahorro solo se convierte en reducción de plantilla si se cumplen cuatro condiciones:
1. **El ahorro cae en las mismas franjas** y quita al menos un agente durante un turno entero. Hoy ya
   quita 1 en el pico de España y de Italia; el resto se reparte en fracciones por hora.
2. **Se mantiene 4 semanas seguidas** con el mismo nivel de servicio.
3. **No hay demanda oculta que lo absorba.** Si se acorta la bienvenida de Gestión y se recuperan las ~130
   llamadas que hoy cuelgan antes de 40 s, se añaden unas 7,5 h de trabajo al día y se compensa casi la
   mitad de lo que ahorran los bots.
4. **La plantilla tiene margen para ajustarse:** contratos temporales o de temporada, horas extra o pasar
   personas a otras tareas (correo, reclamaciones). Lo realista es aplicarlo en la próxima planificación de
   turnos y en la contratación de la temporada de 2027, no despidiendo hoy.

Regla práctica: **cada 5,6 horas-agente al día que se ahorren de forma estable en una franja equivalen a
una jornada**, porque una jornada de 8 h con un 30 % de merma da 5,6 h al teléfono. Con los bots actuales
ya hay unas 3 jornadas diarias de capacidad liberada; la fase 2 sumaría unas 7,5 más en todo el centro
(unas 9 personas a la semana).

## 7. Cómo medirlo y qué pista seguir

Indicadores semanales, comparando siempre el mismo día de la semana:
1. **Llamadas que llegan a agentes por cola y franja** (Accepted de más de 5 s; las que pasa el bot, aparte).
   Tienen que bajar.
2. **Horas de trabajo de agentes** = atendidas × tiempo medio.
3. **Horas-agente necesarias por franja** (Erlang, como en el apartado 3) frente a las **horas-agente
   programadas**. La diferencia es la capacidad liberada.
4. **Ocupación** = tiempo de atención / tiempo conectado. Si en una franja baja del 65–70 % durante 4
   semanas, sobra un agente en esa franja.
5. **Contención real de los bots:** sin transferir y sin rellamada en 48 h.
6. **Pérdidas en dos cifras:** las que cuelgan en la bienvenida (menos de 40 s) y las que se pierden
   esperando a un agente.
7. **Gestiones que entran por Nueva Reserva:** medir cada mes qué parte son gestiones (39 % en el Excel de
   septiembre; el equipo habla de un 80 %); si
   la IA filtra bien, tiene que bajar.
8. **Cola de control:** comparar la evolución de Gestión con la de Nueva Reserva, que no tiene bot, para
   descontar la temporada.

**La pista:** cuando las horas-agente necesarias de una franja bajen de forma estable al menos 5,6 h al día
(una jornada) y las pérdidas esperando a un agente no suban, se puede quitar un turno en esa franja. Con lo
de hoy, la primera franja candidata es el pico de España (11 h y 17 h).

Para medir la ocupación faltan datos que no salen del registro de llamadas: hay que pedir a RingCentral
Analytics, o al sistema de turnos, el tiempo conectado y disponible de cada agente y el tiempo de
trabajo posterior.

## Limitaciones
- **Pocos días:** un jueves, un sábado y un jueves de referencia. El volumen cambia con la temporada y el
  día de la semana.
- **Tiempo por llamada:** sale de una muestra de 49 llamadas; los 30 s de trabajo posterior y el 30 % de
  merma son supuestos.
- **Objetivo y agrupación:** el objetivo 80/30 y los grupos de agentes por país también son supuestos.
- **Lo que no se descuenta:** que los agentes atienden también correos y otras tareas.
- **Datos de bots:** las llamadas de los bots salen de los informes diarios, no de HappyRobot directamente.
- **Datos de trabajo:** los CSV por cola y día están en el scratchpad de la sesión del 17–18/10; no se
  versionan.
