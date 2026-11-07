# Business case: Aurgi Lunas en HappyRobot frente a atenderlo con personas a salario mínimo

Análisis de solo lectura del 26/10/2026. Semana medida: **19/10 a 25/10/2026** (hora de Madrid). Misma lógica y
supuestos que `2026-10-26-business-case-centauro-vs-personas.md`. No se ha cambiado nada en HappyRobot.

## Qué hace el bot

- En HappyRobot es el workflow «testEnrique» (`019d2033-a82d-7c0f-999b-6b43661abc66`), en producción con la
  Version 72. En este informe se llama Aurgi Lunas.
- Es una línea de Mutua para lunas de parabrisas: 146.411 llamadas en total desde marzo.
- **Triaje.** Antes lo hacían personas. Si no es luna, si es robo o colisión, si la póliza no cubre o si está fuera de
  zona, el bot pasa la llamada a una persona con `transfer_to_human`, de dos formas:
  - **Puente** («Connect to call»): HappyRobot sigue en la llamada mientras habla la persona.
  - **Directa** («Connect to mutua»): HappyRobot suelta la llamada.
- **Parte y cita.** Si es luna, el bot abre el parte y da cita en taller (`complete_booking`).
- **Clasificación.** Al final, dos clasificadores con GPT-5 Mini leen la transcripción entera: uno da el desenlace y
  el otro, qué hizo la persona.

## Resumen

- **La semana costó 2.790 € de HappyRobot** por 5.118 llamadas: 0,55 € por llamada (136 créditos).
  - Al año son unos **145.000 €** a 0,004 € por crédito.
  - Son 36,4 M de créditos al año, **el 73 % de la bolsa de 50 M** del contrato.
- **El bot pasa a una persona el 85 % de las llamadas.**
  - Solo cierra sin persona un 15 %.
  - Las citas creadas sin persona son un 8 %, unas 430 a la semana.
  - Lo que de verdad quita es el triaje: unos 2 minutos al principio de cada llamada.
- **Las mismas llamadas con personas costarían de 56.000 a 219.000 € al año**, según lo rápido que sea su triaje:

  | Cómo se atendería sin bot | Personas de 40 h | € al año | Frente a HappyRobot (145.000 €) | ROI |
  |---|---|---|---|---|
  | Triaje y citas con personas, tan largos como los del bot | ~9,7 | 219.000 | el bot ahorra 74.000 € | 51 % |
  | Triaje de 60 s (la mediana del bot) y citas como las del bot | ~6,1 | 137.000 | el bot cuesta 8.000 € más | −6 % |
  | Solo las llamadas que el bot cierra sin persona | ~2,5 | 56.000 | el bot cuesta 89.000 € más | −61 % |

  - Si se reparte la cuota del contrato (0,009 € por crédito), el bot pasa a costar unos 327.000 € al año y es
    más caro en los tres escenarios.
  - **ROI según cómo se cuente HappyRobot:**

    | Escenario con personas | A 0,004 € (145.000 €) | Con transferencia directa (116.000 €) | Con la cuota repartida (327.000 €) |
    |---|---|---|---|
    | Triaje tan largo como el del bot | 51 % | 89 % | −33 % |
    | Triaje de 60 s | −6 % | 18 % | −58 % |
    | Solo las que el bot cierra | −61 % | −52 % | −83 % |

    Con transferencia directa, el ROI pasa a positivo en los dos primeros escenarios.
- **Una cita creada sin persona cuesta unos 6,50 € de HappyRobot.** La misma cita con una persona a salario mínimo
  costaría unos 2,30 €.
- **El 77 % del tiempo de sesión es la persona hablando**, con HappyRobot en la llamada por la transferencia en
  puente. Esa escucha cuesta unos **29.000 € al año** (el 20 % de la factura). Unos 15.000 € más se van en clasificar
  la transcripción entera, con la parte de la persona incluida.
- **No hay ahorro por horario.**
  - El 86,5 % de las llamadas entra de lunes a viernes de 9 a 18 h.
  - Fuera de ese horario el bot también transfiere (el 88 %) y hay personas que cogen la llamada.
  - A diferencia de los bots de Centauro, aquí el bot no evita montar turnos de noche ni de fin de semana.

## Cómo leer este informe

Los términos comunes (personas de 40 h, merma, ocupación, minuto atendido, crédito, cuota repartida, bolsa de 50 M…)
están explicados en «Cómo leer este informe» de `2026-10-26-business-case-centauro-vs-personas.md`. Lo propio de
este bot:

- **Triaje:** las primeras preguntas para saber qué necesita el cliente (si es luna, si la póliza la cubre, si está
  en zona) y a dónde mandarlo. Antes lo hacía una persona; ahora lo hace el bot.
- **Transferencia en puente** («Connect to call»): el bot pasa la llamada a una persona, pero HappyRobot sigue en la
  llamada hasta que cuelgan, y la sigue cobrando.
- **Transferencia directa** («Connect to mutua»): el bot pasa la llamada y HappyRobot sale de ella. Deja de cobrar.
- **Cita creada sin persona:** el bot abre el parte y da cita en taller sin pasar la llamada a nadie. Es lo único que
  el bot hace de principio a fin.
- **Clasificador:** un paso del bot que, al colgar, lee la transcripción y etiqueta cómo acabó la llamada. Lo hace
  una IA, así que puede equivocarse.
- **Escenarios con personas:**
  - **Triaje tan largo como el del bot:** la persona tarda lo mismo que el bot en el triaje y en la cita.
  - **Triaje de 60 s:** una persona con experiencia pregunta lo justo; 60 s es lo que tarda el bot en la mitad de
    las llamadas.
  - **Solo las que el bot cierra:** el bot no ahorra nada en las transferidas, porque la persona vuelve a
    preguntar todo.
- **ROI:** (coste con personas − coste de HappyRobot) / coste de HappyRobot, en porcentaje.
  - Un 51 % quiere decir que, por cada euro pagado a HappyRobot, se dejan de pagar 1,51 € en personas: se recupera
    el euro y se ahorran 51 céntimos más.
  - Un ROI negativo quiere decir que el bot cuesta más que las personas: con −61 %, se pierden 61 céntimos de cada
    euro pagado.
- **Muestra:** parte de las llamadas que se ha leído una a una. Los porcentajes de desenlace salen de 119 llamadas,
  con un margen de unos ±6 puntos.

## 1. Qué se ha medido

- **Volumen exacto:** 5.118 llamadas, todas de la Version 72. Se han contado con los límites de página del listado de
  sesiones.

  | Día | L 19 | M 20 | X 21 | J 22 | V 23 | S 24 | D 25 |
  |---|---|---|---|---|---|---|---|
  | Llamadas | 1.389 | 1.056 | 936 | 903 | 730 | 104 | 0 |

  - Pico de unas 35 llamadas a la vez el lunes entre las 9:20 y las 9:50.
- **Duraciones:** muestra de 1.100 sesiones (11 páginas de días y horas distintos).
  - Media de 10,3 minutos, mediana de 9,8.
  - El 4,5 % llega al tope de 25 minutos.
  - En total, unos 52.800 minutos a la semana.
- **Desenlace:** muestra de 119 llamadas con sus nodos, de las 11 páginas.
  - Transferidas: 101 (85 %). Conectadas: 98.
  - Transferencias en puente: 76. Directas: 25.
  - Parte del bot antes de transferir: 121 s de media (mediana 59 s). En las no transferidas, 212 s.
  - Con la muestra, el bot es el 23 % del tiempo de sesión: unos 11.500 minutos a la semana. La persona después de
    transferir son unos 39.000.
- **Facturación:** pantalla de uso de HappyRobot del 18 al 25/10 (UTC).
  - 697.488 créditos (2.789,95 €) en 5.118 runs.
  - Orquestación de voz: 47,5 %. LLM de la conversación: 41,3 %. LLM de los clasificadores: 10,3 %. Sin evals.
- **Comprobación cruzada:** con 16 créditos por minuto de bot y 3,6 por minuto escuchando, los minutos de la muestra
  dan 325.000 créditos de orquestación de voz. La factura dice 331.000.

**Clasificación del desenlace en la muestra** (el clasificador de la llamada):

| Desenlace | % | | Desenlace | % |
|---|---|---|---|---|
| Pide hablar con una persona | 25 % | | Fuera de zona | 10 % |
| Redirigida en el triaje (no luna, robo, colisión…) | 23 % | | Póliza | 3 % |
| Cita creada | 18 % | | Abandono | 3 % |
| Otra redirección | 16 % | | Error técnico o daño no claro | 2 % |

- **«Cita creada» no es fiable.** De las 22 citas, 12 son llamadas transferidas: la cita la cerró la persona.
  - De las 10 sin transferir, 2 duran 37 y 85 s; no parece que dé tiempo a dar una cita.
  - En las 25 transferencias directas, el clasificador de la persona se inventa el destino, porque no tiene su
    transcripción.
- **Qué hace la persona después:** en la mitad de los casos deriva a un especialista de lunas (CristalBox 26 %,
  Ralarsa 15 %, GlassDrive 5 %) o a la red propia (Aurgi y Motortown 8 %). Es decir, la persona hace lo que el bot no
  sabe hacer: elegir taller fuera de las citas que ofrece el bot.

## 2. Coste

**HappyRobot:**

| Criterio | Semana | Año |
|---|---|---|
| A 0,004 € por crédito | 2.790 € | 145.000 € |
| Cuota repartida (0,009 €) | 6.277 € | 327.000 € |
| Sin la escucha tras transferir (si toda transferencia fuera directa) | 2.226 € | 116.000 € |

**Con personas** (salario mínimo de 2026: 22.564 € al año por persona; 0,357 € por minuto atendido, con las mismas
mermas y ocupación del informe de Centauro):
- **Tiempo de la persona:**
  - Lo mismo que habla el bot más 30 s de trabajo posterior en las que el bot cierra.
  - En las transferidas, solo la parte del bot, porque la de la persona se paga en los dos casos.
- **Tres escenarios:**
  - **Triaje y citas tan largos como los del bot:** 11.776 min a la semana, unas 9,7 personas, 219.000 € al año.
  - **Triaje de 60 s:** una persona experta pregunta lo justo para derivar. 7.361 min, 6,1 personas,
    137.000 €.
  - **Conservador:** la persona vuelve a preguntar todo tras la transferencia, así que el bot solo ahorra las llamadas
    que cierra. 3.017 min, 2,5 personas, 56.000 €.
- **Sin Erlang a 80/30.** Con este volumen y el 86 % de las llamadas en horario de oficina, el 70 % de ocupación del
  minuto atendido ya es realista, salvo en el pico del lunes.

## 3. Qué cambiaría el caso

1. **Transferir sin puente.** El 75 % de las transferencias son en puente, y escuchar a la persona cuesta unos 29.000 €
   al año. Con la transferencia directa («Connect to mutua»), el bot baja a unos 116.000 € y queda por debajo de los
   escenarios 1 y 2 con personas.
2. **Clasificar solo la parte del bot.** Los dos clasificadores leen la transcripción entera, de 10 minutos de media,
   con la parte de la persona. Cuestan unos 15.000 € al año, y el segundo no sirve en las transferencias directas.
3. **Resolver más sin persona.** Hoy solo cierra el 8 % con cita.
   - Las causas más frecuentes de transferir son pedir una persona (25 %), el triaje (23 %) y «otra» (16 %).
   - Lo que hace la persona después es, sobre todo, mandar al cliente a un especialista de lunas concreto.
   - Si el bot pudiera derivar a CristalBox, Ralarsa o GlassDrive, podría quitar hasta la mitad de las
     transferencias. Este clasificador es poco fiable, así que hay que comprobarlo antes en las transcripciones.
4. **Repartir la cuota.** Este bot gasta el 73 % de la bolsa de 50 M.
   - Con los bots de Centauro (14,5 %) y el resto de la cuenta, el ritmo de la semana medida es de unos 50 M de créditos
     al año: la bolsa entera.
   - El contrato es de Mutuamad Motor Network. Hay que decidir a quién se imputa el coste de este caso.
5. **Cambiar el nombre del workflow.** Un workflow en producción con 146.000 llamadas no debería llamarse
   «testEnrique» en HappyRobot.

## 4. Límites

- **Duración y desenlace salen de muestras** (1.100 y 119 llamadas), no de todas las llamadas. Con 119 llamadas, el
  margen de error de un 15 % es de unos ±6 puntos.
- **«Conectada»** se ha deducido por la duración en la mayoría de las transferencias en puente.
- **No se sabe cómo era el triaje con personas antes del bot** (cuánto duraba ni cuántas personas lo hacían). Por eso
  hay tres escenarios.
- **Una semana anualizada ×52.** Esta semana cae el volumen de lunes a viernes (de 1.389 a 730 llamadas al día).
- **El coste con personas es el mínimo legal:** sin convenio, sin pluses, sin supervisión, sin puesto ni licencias.

## Fuentes

- **Llamadas:** listado de sesiones y nodos de cada run en HappyRobot. Datos de trabajo en
  `datos/business-case-2026-10-26/test_enrique/` (fuera del repo, sin datos personales).
- **Facturación:** pantalla de uso del workflow «testEnrique» del 18 al 25/10.
- **Contrato y supuestos de personas:** como en el informe de Centauro; las constantes están en
  `scripts/coste_bots_vs_humanos.py`.
