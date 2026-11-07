# Business case: los bots de Centauro en HappyRobot frente a atenderlo con personas a salario mínimo

Análisis de solo lectura del 26/10/2026. Semana medida: **19/10 a 25/10/2026** (hora de Madrid). No se ha
cambiado nada en HappyRobot ni en RingCentral.

## Resumen

- **La semana costó unos 556 € de HappyRobot** por 1.567 llamadas de los tres bots de voz de Centauro en España: Minibús ES,
  Prolongaciones y Atención España.
  - Son unos 0,35 € por llamada y unos 29.000 € al año, a 0,004 € por crédito.
  - Aparte hay 276 € de evals de Atención España, que es coste de construcción y no de atender.
- **Las mismas llamadas con personas a salario mínimo costarían de 33.000 a 196.000 € al año.** Depende de cómo se
  cubran:

  | Cómo se atendería sin bots | Personas de 40 h | € al año |
  |---|---|---|
  | El equipo actual absorbe solo las que el bot cierra sin transferir | ~1,5 | 33.000 |
  | El equipo actual absorbe todo el trabajo que hace el bot | ~2,1 | 47.000 |
  | **Con Gestión abierta (L–V de 8 a 21 h), el equipo actual; con Gestión cerrada (noches y fines de semana), un turno nuevo** | **~5,9** | **133.000** |
  | Servicio propio 24/7 a 80/30 | ~8,7 | 196.000 |

- **El ahorro está en las horas con Gestión cerrada, no en el minuto.**
  - En horario de Gestión, el bot cuesta casi lo mismo que el minuto de una persona a salario mínimo.
  - Por la noche y el fin de semana evita montar turnos: el 28 % de las llamadas de la semana (444) entró con
    Gestión cerrada.
  - En el escenario realista (el tercero de la tabla), el ahorro es de unos **104.000 € al año**. Si se reparte la
    cuota del contrato, queda en **67.000 €**.
  - **ROI del 357 %**: por cada euro que se paga a HappyRobot se dejan de pagar 4,57 € en personas; se recupera el
    euro y se ahorran 3,57 € más. Con la cuota repartida, el ROI es del **103 %**.
- **Prolongaciones V11 sale más cara que una persona.**
  - Cuesta 0,62 € por llamada y 1,15 € por llamada cerrada sin agente; una persona costaría unos 0,79 €.
  - El motivo es el prompt grande: el LLM es el 79 % de su factura.
  - Minibús ES (0,46 € por llamada cerrada) y Atención España (unos 0,35 €, estimado) sí salen por debajo.
  - Pasar la línea de Prolongación a Atención España (C-004), hecho el 24/10, va en la buena dirección.
- **El 59 % de los minutos facturados son de después de transferir**: el bot sigue en la llamada mientras habla el
  agente. A unos 4 créditos por minuto, son unos 2.600 € al año.

## Cómo leer este informe

**Horarios**
- **Gestión abierta:** de lunes a viernes de 8 a 21 h, salvo festivos nacionales (65 h a la semana). Hay agentes
  conectados que pueden coger llamadas.
- **Gestión cerrada:** de 21 a 8 h entre semana y el fin de semana entero (103 h a la semana). Sin bot, hoy esas
  llamadas solo oyen el anuncio de cerrado y se pierden.

**Escenarios con personas** (cómo se atenderían las llamadas de los bots si no existieran)
- **El equipo actual absorbe las llamadas:** se suman a lo que ya atienden los agentes y solo se paga el tiempo que
  les dedican. Es el escenario más barato, pero supone que siempre hay alguien libre, también de noche.
- **Conservador:** como el anterior, pero contando solo las llamadas que el bot cierra sin transferir. En las
  transferidas se supone que el agente vuelve a preguntar todo, así que el bot no le ahorra nada.
- **Equipo actual + turno con Gestión cerrada (el realista):** con Gestión abierta lo absorbe el equipo actual; con
  Gestión cerrada hay que contratar un turno solo para esas horas.
- **Servicio propio 24/7:** un equipo dedicado solo a estas llamadas, con alguien conectado las 24 h.

**Cómo se cuentan las personas**
- **Personas de 40 h:** puestos a jornada completa (FTE). 2,1 personas equivale, por ejemplo, a dos jornadas
  completas y una parte de otra.
- **Coste por persona:** 22.564 € al año. Es el salario mínimo de 2026 (17.094 € en 14 pagas) más un 32 % de
  cotizaciones de empresa.
- **Merma (16 %):** horas pagadas en las que la persona no puede atender: pausas de pantalla, bajas y ausencias,
  formación y reuniones.
- **Ocupación (70 %):** parte del tiempo conectado que se pasa hablando con clientes. El resto es espera entre
  llamadas; nadie puede estar al 100 %.
- **Minuto atendido (0,357 €):** lo que cuesta un minuto de conversación de un agente, con la merma y la ocupación ya
  descontadas.
- **Trabajo posterior (30 s):** lo que tarda el agente en apuntar y cerrar cada llamada después de colgar.
- **80/30:** el nivel de servicio objetivo, que el 80 % de las llamadas las coja alguien en menos de 30 s.
- **Erlang C:** la fórmula estándar de los call center para calcular cuántos agentes hacen falta cada hora para
  cumplir el 80/30 con las llamadas de esa hora.

**Cómo se cuenta HappyRobot**
- **Crédito:** la unidad con la que factura HappyRobot (voz, LLM, orquestación). Cuesta 0,004 € en el contrato.
- **A 0,004 € por crédito (coste variable):** lo que se paga por cada crédito que gastan los bots. Hoy, con la cuenta
  en exceso, es lo que se paga de verdad.
- **Con la cuota repartida (0,009 €):** la cuota anual de 450.000 € dividida entre los 50 M de créditos que incluye. A
  cada bot se le carga la parte de la cuota que le toca por lo que gasta.
- **Bolsa de 50 M:** los créditos que trae el contrato para el año; lo que se gaste de más se paga aparte.
- **Evals:** pruebas automáticas de un bot mientras se construye. Gastan créditos, pero no atienden a clientes, así
  que se cuentan aparte.

**Llamadas**
- **Sin transferir:** el bot termina la llamada sin pasarla a un agente. Solo cuentan las de 15 s o más; las más
  cortas son cuelgues.
- **Transferida:** el bot pasa la llamada a una cola de agentes.
- **Resolución real:** sin transferir y sin que el cliente vuelva a llamar en 48 h. Es más baja que «sin transferir».
- **Minutos tras transferir:** después de pasar la llamada, el bot sigue en ella escuchando al agente y HappyRobot lo
  sigue cobrando, aunque más barato (unos 4 créditos por minuto frente a 11–16 hablando).
- **Anualizado ×52:** la semana medida multiplicada por las semanas del año.

**Resultado**
- **Ahorro:** lo que costarían las personas menos lo que cuesta HappyRobot.
- **ROI:** el ahorro dividido entre lo que cuesta HappyRobot, en porcentaje.
  - Un 0 % significa que el bot cuesta lo mismo que las personas.
  - Un 100 % significa que las personas costarían el doble: por cada euro pagado al bot, se recupera ese euro y se
    ahorra otro.
  - Por debajo de 0 %, el bot cuesta más que las personas.

## 1. Qué se ha medido

| Bot | Llamadas | Minutos | Sin transferir (≥ 15 s) | Transferidas | Créditos por llamada | € de la semana |
|---|---|---|---|---|---|---|
| Minibús ES | 1.068 | 3.242 | 588 | 461 | 63 | 269 € |
| Prolongaciones V11 (hasta el 24/10 a las 18:14) | 432 | 1.678 | 233 | 195 | 155 | 269 € |
| Atención España (desde el 24/10) | 67 | 141 | 54 | 9 | 70 (estimado) | 19 € |
| **Total** | **1.567** | **5.061** | **875** | **665** | **89** | **556 €** |

- **Llamadas:** listado de sesiones de HappyRobot, cruzado con las tablas de Twin de Minibús y de Prolongaciones.
  - Atención España no tiene tabla de Twin; sus datos salen de los nodos de cada run.
  - Se ha quitado una llamada de prueba por web.
  - Los datos por llamada están en `datos/business-case-2026-10-26/` (fuera del repo, sin teléfonos).
- **Euros de HappyRobot:** la pantalla de uso de HappyRobot, del 18 al 25/10 (UTC).
  - **Prolongaciones:** 323,94 € en 521 runs.
  - **Minibús ES:** 307,26 €, prorrateado a 7 de los 8 días.
    - Sale a 0,25 € por llamada. La media de 30 días es 0,16 €: el coste ha subido en octubre (más LLM).
  - **Atención España:** la pantalla da solo 4,26 € de voz para las 67 llamadas (16 créditos por llamada).
    - Seguramente falta por facturar la voz del 25/10.
    - Se usan los 60–75 créditos que estima el spec (§9) para no abaratar el bot.
- **Moneda:** la pantalla muestra «$0.0040/credit» y el contrato dice 0,004 € por crédito. Se toma la cifra como
  euros.

## 2. Lo que cuesta HappyRobot

**Contrato** (Order Form #2 con Mutuamad Motor Network, borrador del 15/09/2026, en vigor desde el 01/09):
- Cuota de 450.000 € por 12 meses, sin cancelación. Incluye la plataforma, un FDE dedicado y 50 M de créditos:
  - 25 M pagados a 0,004 €;
  - 25 M gratis solo el primer año.
- El crédito de más se paga a 0,004 €, con un tope de gasto de 900.000 € al año.
- La tabla indicativa (Schedule A) da unos 24 créditos por minuto de voz: 6 de LLM, 16 de orquestación de voz y
  2 de telefonía.

**Situación hoy:**
- La cuenta tiene **0 créditos disponibles y 1.708.197 créditos en exceso** (unos 6.800 €).
- El Order Form revisado tiene la firma del cliente «TO BE CONFIRMED».
- Hay que confirmar si la bolsa de 50 M ya está activa. Si no lo está, hoy cada crédito se paga a 0,004 €.

**Tres formas de ponerle precio:**

| Criterio | € por crédito | Semana | Año |
|---|---|---|---|
| Coste variable (lo que se paga por cada crédito, también en exceso) | 0,004 | 556 € | 29.000 € |
| Cuota repartida entre los 50 M de créditos | 0,009 | 1.251 € | 65.000 € |
| Tabla indicativa del contrato (24 créditos por minuto) | 0,004 | 486 € | 25.000 € |

- Los tres bots de Centauro gastan unos **7,25 M de créditos al año, el 14,5 % de la bolsa** de 50 M.
- **El coste de cuota** solo tiene sentido como reparto: los 450.000 € se pagan igual, haya bots o no, si se firma
  el contrato.
- **El gasto de la cuenta lo marca otro caso.** En la semana medida, Aurgi Lunas gastó 2.790 € (el 70 % de
  la cuenta), frente a 912 € de los tres bots de Centauro con sus evals. Conviene revisarlo, porque explica buena
  parte del exceso.

**Lo que no entra:**
- las evals de Atención España: 276 € esta semana, unos 14.000 € al año si se mantuviera el ritmo de construcción;
- el tiempo del equipo propio que construye y mantiene los bots;
- los minutos de RingCentral de las transferencias.

## 3. Lo que costaría con personas

**Coste de una persona a jornada completa con el salario mínimo de 2026:**
- 1.221 € al mes en 14 pagas: 17.094 € al año (Real Decreto 126/2026).
- Con un 32 % de cotizaciones de empresa: **22.564 € al año**.
- Mismo supuesto que en `2026-10-18-carga-agentes-ringcentral.md`.

**Supuestos:**
- **Horas al año:** 1.792 (40 h a la semana, menos 22 días de vacaciones y 14 festivos).
- **Merma del 16 %:** pausas de pantalla, absentismo y formación.
- **Ocupación del 70 %** (escenarios 1 y 2).
- **Coste por minuto atendido: 0,357 €.**
- **Tiempo de la persona por llamada:**
  - lo mismo que habla el bot más 30 s de trabajo posterior;
  - sin trabajo posterior en los cuelgues de menos de 15 s;
  - en las transferidas, solo la parte del bot, porque la del agente se paga en los dos casos.
- **Nivel de servicio:** 80 % de llamadas atendidas en 30 s, con Erlang C hora a hora y al menos una persona en
  cada hora cubierta.
- **Horario de Gestión:** el mismo que usa el bot (`contexto_llamada.gestion_abierta_en`).
- **Sin pluses de nocturnidad ni festivos:** el coste con personas es un mínimo, y el salario real por convenio
  será mayor.

**Escenarios:**
1. **El equipo actual absorbe el trabajo.** Solo se paga el minuto atendido: 898 € a la semana, unos 2,1
   personas, 47.000 € al año.
   - **Versión conservadora:** las transferidas no ahorran nada, porque el agente vuelve a preguntar. Quedan
     633 € a la semana y 33.000 € al año.
   - Supone que hay hueco en el equipo a cualquier hora. No es cierto con Gestión cerrada, y por la tarde ya
     faltan unas 6 personas (informe del 18/10).
2. **Servicio propio 24/7.** Hacen falta 251 h de agente a la semana (8,7 personas) para cubrir cada hora a 80/30:
   3.762 € a la semana y 196.000 € al año.
3. **Lo realista: el equipo actual cuando Gestión está abierta y un turno nuevo cuando está cerrada.**
   - **Gestión abierta** (lunes a viernes de 8 a 21 h, salvo festivos; 65 h a la semana): entran 1.123 de las
     llamadas del bot. Hay agentes conectados, así que las absorben ellos y solo se paga el tiempo que les dedican:
     unos 31.000 € al año (~1,4 personas).
   - **Gestión cerrada** (de 21 a 8 h entre semana y el fin de semana entero; 103 h a la semana): entran 444
     llamadas. Hoy no hay nadie, así que habría que montar un turno solo para ellas.
     - Hace falta al menos una persona conectada en cada una de esas 103 horas, y alguna más en las horas con más
       llamadas (sábado y domingo por la mañana). En total, 129 h de agente a la semana.
     - Con jornadas de 40 h y la merma, son 4,5 personas: unos 102.000 € al año.
     - Lo caro no es el volumen (unas 4 llamadas por hora), sino tener a alguien en cada hora. Es lo que se ahorra
       el bot.
   - En total: **133.000 € al año, unas 5,9 personas**.

## 4. Comparación

| | € al año | Frente a HappyRobot a 0,004 € (29.000 €) | ROI | Frente a HappyRobot con la cuota repartida (65.000 €) | ROI |
|---|---|---|---|---|---|
| Personas, escenario 1 conservador | 33.000 € | ahorra 4.000 € | 14 % | cuesta 32.000 € más | −49 % |
| Personas, escenario 1 | 47.000 € | ahorra 18.000 € | 62 % | cuesta 18.000 € más | −28 % |
| **Personas, escenario 3** | **133.000 €** | **ahorra 104.000 €** | **357 %** | **ahorra 67.000 €** | **103 %** |
| Personas, escenario 2 | 196.000 € | ahorra 167.000 € | 576 % | ahorra 131.000 € | 201 % |

- **ROI = (coste con personas − coste de HappyRobot) / coste de HappyRobot.**
  - Un ROI del 357 % quiere decir que, por cada euro pagado a HappyRobot, se dejan de pagar 4,57 € en personas: se
    recupera el euro y se ahorran 3,57 € más.
  - Un ROI negativo quiere decir que el bot cuesta más que las personas: con −49 %, se pierde la mitad de lo que se
    paga.
- **No incluye las evals de construcción** (unos 14.000 € al año si se mantuviera el ritmo de esta semana). Con ellas,
  el ROI del escenario 3 a 0,004 € pasaría del 357 % al 205 %.

**Por bot, por llamada cerrada sin agente** (coste de la semana / llamadas sin transferir de ≥ 15 s):

| Bot | HappyRobot | Persona (minuto atendido) | |
|---|---|---|---|
| Minibús ES | 0,46 € | 0,69 € | el bot, un 33 % más barato |
| Prolongaciones V11 | 1,15 € | 0,79 € | **el bot, un 46 % más caro** |
| Atención España (estimado) | 0,35 € | 0,80 € | el bot, un 56 % más barato |

- **Las llamadas sin transferir no son llamadas resueltas.** La resolución real, sin rellamada en 48 h, era del
  47 % en Minibús y del 38 % en Prolongaciones (spec de Atención España §1). Con la resolución real, el coste por
  llamada resuelta del bot sube un 15 % en Minibús y un 40 % en Prolongaciones.
- **En la comparación por minuto se compara solo el coste.** No entra que, sin bot, las llamadas con Gestión
  cerrada se pierden: el sábado 10/10 se perdieron las 504 llamadas de Gestión ES y EN (informe del 18/10).

## 5. Qué cambiaría el caso

1. **Confirmar el contrato y la bolsa de créditos.**
   - Con la bolsa activa, los créditos de los bots de Centauro no se pagan aparte hasta agotar los 50 M.
   - Sin la bolsa activa, todo es exceso a 0,004 €.
2. **Prolongación al bot único.** Ya está hecho desde el 24/10. Con 70 créditos por llamada en vez de 155, la línea
   pasa de unos 14.000 € al año a unos 6.300 €. Hay que confirmarlo con la facturación de una semana completa.
3. **Que el bot suelte la llamada al transferir**, como Minibús Italia y Portugal.
   - Hoy el 59–61 % de los minutos de Minibús ES y de Prolongaciones son de después de transferir.
   - Son unos 2.600 € al año de orquestación de voz.
4. **Revisar Aurgi Lunas**, que se lleva el 70 % del gasto de la cuenta. Su business case, aparte, está en
   `2026-10-26-business-case-aurgi-lunas-vs-personas.md`.
5. **Subir la resolución.** Cada punto de llamadas cerradas sin agente abarata la llamada resuelta y acerca el
   escenario de quitar trabajo de día (informe del 18/10: objetivo del 50 % en Gestión).

## 6. Límites

- **Es una semana**, anualizada ×52. En temporada alta habrá más llamadas para los dos lados.
- **Prolongaciones y Atención España no cubren la semana entera** cada uno; juntos sí cubren la línea de
  Prolongación. La línea se movió el 24/10 por la tarde.
- **La parte del bot en las transferidas es una estimación**: el final del último turno antes de transferir. En
  Twin, `transfer_completed_at` marca el final de la llamada, no la transferencia. Solo afecta al escenario 1 sin
  la versión conservadora.
- **En las transferencias de Minibús a colas que no son la de Minibús**, la conexión se deduce de que haya
  transcripción después de transferir.
- **La facturación de Atención España parece incompleta**: se ha usado la estimación del spec.
- **El coste con personas es el mínimo legal:** sin convenio, sin pluses, sin supervisión, sin puesto ni licencias.

## Fuentes y cómo repetirlo

- **Contrato:** Order Form #2 y MSA + DPA (borradores de HappyRobot del 15 y del 24/09/2026), fuera del repo.
- **Facturación:** pantalla de uso de HappyRobot del 18 al 25/10 y del 25/09 al 25/10, por workflow.
- **Cálculo:** `python3 -I scripts/coste_bots_vs_humanos.py datos/business-case-2026-10-26/entrada --json
  datos/business-case-2026-10-26/resultado.json`.
  - Todos los supuestos están en las constantes del script.
  - Pruebas: `python3 -I scripts/test_coste_bots_vs_humanos.py`.
