# Pendientes

## Incidencias abiertas
- [ ] **Averías enviadas a menús** (2114, 2115 y 2119): ver C-001. Afecta a ES v17, v18 y v19 y a
      IT v2.
- [x] **Llamadas de ES por versiones no publicadas** (v19, v21, v22): 70 de 133 el 10/10.
      Resuelto: la v22 se publicó la noche del 11 al 12/10 y desde entonces entra todo por ella.
  - Desde el 10/10 hacia las 18:40 solo entran la v17 (publicada) y la v22 (no publicada), casi a
    medias: el 11/10, 27 y 28 runs. La v19 y la v21 ya no reciben llamadas.
  - Comparación v17/v22 del fin de semana: `informes/2026-10-11-v17-vs-v22.md`.
- [ ] **v17: transfiere a Gestión en fin de semana y la llamada se pierde.** La Gestión no tiene
      agentes en fin de semana (ver pendientes de Prolongaciones). Del 10/10 18:53 al 11/10 16:47,
      14 llamadas de la v17 a 18057/18061 acabaron en la locución. La v22 no lo hace.
- [ ] **v22: copia «NO DISPONIBLE» como extensión** (f06cc517, 11/10). La regla de «recoger tarde»
      de «Prolongación y consultas» («si acepta… transfiere a GESTIÓN DE RESERVA») choca con la
      sección de Gestión cerrada. El bot pasó el texto como `extension_destino` y la transferencia
      falló con «invalid phone number». Misma causa que en Prolongaciones: «Resolver colas» deja el
      texto donde va la extensión.
- [ ] **v22 no tiene en cuenta los festivos** en `gestion_abierta` (solo mira día de la semana y
      hora). El 12/10 (festivo nacional) la Gestión sí tuvo agentes, así que no hizo daño; falta
      confirmar con Centauro qué festivos cierra Gestión.
- [ ] **v22: dice «le paso con un compañero» dos veces** (por su cuenta y dentro de la herramienta)
      en 4 de 34 llamadas del 12/10 (d1774c82, c21eba56, a3be3ecb, bac77e01).
- [ ] **v22: tutea** («Perdón, continúa.», «Perdón, dime.») en 5 de 37 llamadas (10–11/10).
- [ ] **v22: información inventada** el 11/10: oficina en el aeropuerto de A Coruña (2ff9ad71) y
      «el minibús es amarillo» (a0b9b970).
- [ ] **Palma: posible punto de encuentro de invierno distinto** (4e309ad0 y su rellamada 12c53ac1,
      11/10). El agente dijo que «en invierno tenemos otro punto de encuentro» y el cliente dijo que
      el correo de confirmación le dio un punto equivocado. Confirmar con la oficina.
- [ ] **Agentes de Gestión (18057, 18061) que cogen y no pulsan 1**: 2 llamadas perdidas el
      10/10. En la 18057 las patas duran solo 8 s.
- [ ] **Frecuencias del minibús inventadas** («cada 10-15 minutos»): ver D-006.
- [ ] **Respuestas en un idioma distinto del del cliente** (IT): ver D-006.
- [ ] **La rutina cuenta como Minibús todas las patas a 18056 y 18059**, pero Prolongaciones también
      transfiere a esas colas (minibús o idioma no atendido). Hay que corregir la sección 4 de
      `rutinas/informe-minibus.md` para que cuente solo las patas que casan con un intento de
      Minibús, como ya hace con 18057, 18061, 18001, 18006 y 18034.

- [ ] **v23: probar con llamadas reales** (D-009). Los 4 «Module Change» están enlazados y la batería de evals pasa: 14/14 nuevas y 24/24 de regresión (`informes/2026-10-12-v23-evals.md`). Falta el recorrido completo en una llamada.
  - Probar los recorridos mixtos: minibús → prolongar, prolongar → minibús, oficina → fianza,
    recoger tarde → punto de encuentro, y prolongar → oficina en modo virtual.
  - Revisar que al cambiar de módulo no repite el saludo ni vuelve a preguntar el motivo.
  - Revisar los extracts:
    - Hecho (12/10): «Registrar consultas del alquiler» ya lee también el `tema` y la `pregunta` de
      las dos `consultas_alquiler` nuevas.
    - En «Registrar resultado», `ultima_herramienta` y `fase_transferencia` no conocen la fase de
      consultas.

- [ ] **v24: WhatsApp con geolocalización** (D-010). Borrador sin probar ni publicar.
  - Reseleccionar la plantilla `minibus_punto_texto_boton` en el nodo «Enviar WhatsApp del punto de encuentro» y comprobar las cuatro variables (no se pudo leer la plantilla desde la API).
  - Probar una llamada real desde un móvil en Madrid, Sevilla y Málaga, y una en otro aeropuerto (no debe ofrecer el WhatsApp).
  - Cuando se apruebe la plantilla en inglés, enviar también en llamadas en inglés.
  - Revisar si v24 debe heredar los cambios de v23 antes de publicar (v23 sigue sin probar).
  - [x] **15/10/2026 · runs «failed» en v24:** el nodo de rutas «¿Enviar WhatsApp?» no tiene rama por defecto. Cuando `enviar` es false, el run termina en «failed» («has no matching condition and no fallback branch»), aunque la llamada fue bien (primer caso: run 52019f08-6f67-4055-8537-db12c2c7cd57, Murcia, inglés, transferida y conectada a 18059; otro: 4ca09060-423f-4b37-b45d-9fe7f5ee6172). Arreglo: añadir una rama por defecto sin acción, en una versión nueva (fork de v24).
    **Resuelto en v25 (`k2in5n9kk01x`, D-011)**, que ya está en producción (24/10/2026).

- [ ] **v26: servicio de espera y avisos de retraso a la cola de Minibús** (D-012). Publicada el 24/10/2026; desde el 25/10 sigue en producción dentro de la v27.
  - 25/10, de 08:01 a 09:01: un cliente avisó de que llegaba un poco tarde a recoger; el bot le explicó que la reserva se guarda doce horas y no transfirió, que es lo correcto con la oficina abierta. Ninguna llamada fue a Gestión.
  - Según jzerpa, ya ha pasado bien algunas llamadas reales. Falta comprobar con datos, mejor un fin de semana o después de las 21 h (Gestión cerrada), que estas llamadas entran en la 18056 (o en la 18059 si son en inglés).
  - Avisar al call center de que la cola de Minibús recibirá estas llamadas todos los días, también entre semana con Gestión abierta.
  - Tras publicar: en el informe diario, contar las transferencias a 18056/18059 por retraso y comprobar que no aumentan las de «solo quiere avisar».
  - **El mismo cambio falta en Prolongaciones (V11) y en el bot único de Atención España**: los dos mandan todavía el servicio de espera a Gestión, incluso con Gestión cerrada.

- [ ] **v27: WhatsApp del punto de encuentro como cierre normal y para el cliente que ya espera** (D-013). Publicada; en producción el 25/10/2026.
  - Primera hora del 25/10 (08:01 a 09:01, 9 llamadas): una sola llamada apta (Málaga, 08:19), que
    cerró con la pregunta del WhatsApp; el cliente dijo que no y no se envió nada. Hay que seguir
    midiendo durante la semana.
  - Las llamadas de prueba previstas antes de publicar no constan como hechas:
    - Sevilla: debe cerrar con la pregunta del WhatsApp, y con un «sí» debe llegar el mensaje;
    - un cliente que ya espera en Madrid T1, T2 o T4 y pregunta cada cuánto pasa: debe ofrecerlo, y con un «sí» el extract debe poner `punto_whatsapp` con su terminal y debe llegar el mensaje;
    - una llamada en inglés y una de Bilbao: no debe mencionar el WhatsApp.
  - Tras publicar, medir en el informe diario el porcentaje de oferta en las llamadas aptas: con v25, 42 de 93; Sevilla, 0 de 16.
  - En Madrid T2, al cliente que ya espera, una de dos veces le dio la indicación entera en lugar de solo la referencia, aunque sí ofreció el WhatsApp (WA-6). Vigilarlo en llamadas reales.
  - Al cliente que ya espera en Málaga (WA-5), el 25/10 no siempre mencionó el enlace para ver el minibús en directo, aunque sí ofreció el WhatsApp: v27, 1 de 2; v28, 1 de 3. El 24/10, v27 pasó 2 de 2. Vigilarlo en llamadas reales.
- [ ] **v28: dirección de las oficinas desde «Punto de encuentro»** (D-014). Sin publicar y **no se sigue** (25/10, jzerpa): la línea de Minibús ES pasará pronto al bot único de Atención España, que ya lo hace.
  - Mientras la línea siga en este workflow quedan dos huecos que el bot único no tiene:
    - «Punto de encuentro» manda al navegador a quien pide la dirección de la oficina (run `f7b98d60`, Málaga, 25/10);
    - «Información de oficina» transfiere a la cola de MINIBÚS solo para dar el punto de encuentro: unas 19 de 2.336 llamadas del 07 al 25/10, una al día (`informes/2026-10-25-v28-direccion.md`, sección 6). Ejemplo: `cad2c98e` (Valencia, 25/10).
  - Al pasar la línea al bot único, comprobar en sus primeras llamadas que ninguno de los dos casos se repite.
  - Si la migración se retrasa y se retoma la v28, faltan los pasos de abajo y, además, igualarla con la v6 del bot único (la dirección por cualquier motivo, no solo en taxi o en su coche) y añadir el salto de «Información de oficina» a «Punto de encuentro».
  - **Antes de publicar (si se retomara):** una persona tiene que crear en el editor el Module Change debajo de la herramienta `informacion_oficina` de «Punto de encuentro» (node `01a17263-9058-7c9d-ba62-895569b1ce06`) hacia «Información de oficina» (`01a17262-1409-7c6a-a58b-7bcdf2db7c14`). Sin él no se puede publicar: la herramienta devuelve vacío y el bot puede inventarse la respuesta (DIR-2).
  - Después: comprobar por la API que el enlace apunta al módulo correcto y repetir DIR-1 y DIR-2.
  - Llamada de prueba real: Málaga, ir en taxi y pedir la dirección de la oficina. Debe dar «calle Pascal, cuarenta y dos, polígono Villa Rosa».
  - Al publicar, vigilar que la cola de MINIBÚS no reciba ya preguntas de horario de oficinas de estación o de ciudad hechas desde «Punto de encuentro».
- [ ] **«Assistance» en inglés se toma como avería** (run `78624427`, 24/10). Un cliente que llegaba tarde dijo «I want to contact with assistance» y el bot le pasó a la 18035 (averías) en vez de a Minibús (18059). En inglés, «assistance» o «help» a secas no deberían contar como avería, solo si el cliente habla de una avería o un accidente. Caso aislado: vigilar si se repite antes de cambiar el prompt.
- [ ] **Palma, 25/10: el minibús no llegaba.** El mismo cliente llamó a las 08:07 (llevaba 20 minutos esperando) y a las 08:30 (ya una hora). Las dos veces se pasó a Minibús y conectó con un agente. Es un problema de operación, no del bot. Avisar a la oficina de Palma si se repite. Es una suposición que tenga que ver con el cambio de hora de esa noche.
- [ ] **«Punto de encuentro» salta a `consultas_alquiler` ante «¿puedo devolver el coche en Alicante a las tres de la madrugada?»** (ADV-10). Debería responder él: Alicante admite devoluciones las 24 horas. La respuesta final es correcta, pero cambia de módulo sin necesidad. Ya pasaba en v26: con todas las variables fijadas, como en una llamada real, v26 pasa 0 de 4 y v27, 3 de 5 (`informes/2026-10-24-v27-whatsapp.md`).

## Mejoras propuestas
- [ ] Mejoras de prompt de D-006 (estimación: resueltas del 42 % al 54 %).
- [ ] Herramientas nuevas (estimación: hasta el 94 %):
  - localización de la flota y aviso al operador (52 llamadas el 10/10);
  - acceso a reservas (32);
  - enlace de reserva nueva (7);
  - ubicación y foto del punto por WhatsApp (4);
  - parte de asistencia (3);
  - objetos olvidados (3).
- [ ] Guardar en `prompts/` los prompts de las versiones publicadas. Hechos ES v17 y v22 (11/10);
      faltan IT v2 y PT v1.
