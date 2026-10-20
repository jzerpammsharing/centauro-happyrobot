# «Respuestas de Daniel» frente a los prompts de Prolongaciones y Minibús

Análisis de solo lectura del 17/10/2026. No se ha escrito nada en el artefacto ni en HappyRobot.

## Fuentes
- **Artefacto [Respuestas de Daniel](https://claude.ai/artifact/L4cpA1DVsHPdT3ELCQJY2Y):**
  - 220 revisiones del equipo (colecciones `rev` y `reviews`), de 4 revisores. No hay ninguna anterior al
    06/10, así que la semana del 28/09 al 04/10 no tiene respuestas.
    - Semana pasada (del 6 al 9/10): 179 revisiones.
    - Esta semana (del 12 al 16/10): 43 revisiones, casi todas de preguntas nuevas.
  - 95 preguntas que la rutina detectó en llamadas de Prolongaciones (`detectadas`, 271 llamadas en total).
    El equipo ha respondido 93; quedan 2 sin respuesta.
  - Contradicciones (`contra`), lo que falta (`miss`) y la tabla de oficinas (`offices`).
- **Prolongaciones:** V11 (en producción) y v12 (borrador, D-008).
- **Minibús España v25** (en experimento desde el 15/10), sus cuatro módulos: Triaje y horario, Punto de
  encuentro, Información de oficina y Prolongación y consultas.

En las tablas, «llamadas» es el número de llamadas de Prolongaciones en las que salió la pregunta, según la
rutina (desde el 05/10). Una pregunta de la ficha del artefacto no tiene ese dato (—).

## Resumen
- **Casi todo lo que el equipo contestó ya está en algún bot.** Prolongaciones V11 cubre la mayoría de las
  preguntas, y Minibús v25 copió buena parte de las respuestas del 7 al 9/10.
- **35 respuestas del equipo no están en ningún bot** (tabla 1). Las que más salen son la recogida de noche
  o sin llaves (9 llamadas), los avisos y ruidos del coche (5), el aceite, el combustible equivocado o la
  matrícula caída (4) y el contrato vencido que la web no deja alargar (3).
- **Prolongaciones no tiene 12 respuestas que sí tiene Minibús** (tabla 2), sobre todo de oficinas: horario
  (12 llamadas), dónde está (13) y punto de encuentro (6).
- **El equipo resolvió 6 contradicciones que los bots aún no aplican** (tabla 3), y quedan 5 sin decidir.
- **Hay 6 errores en las respuestas del equipo** (tabla 4): respuestas pegadas en otra pregunta, una errata
  en el teléfono de Grecia y revisiones marcadas «hay que cambiarla» sin texto.

Todo esto está ya en el bloque común `comun/bloques/consultas-alquiler.md`, redactado para voz y marcado
como «Nuevo», «Resuelto por el equipo» o «DECIDIR».

## 1. Lo que el equipo respondió y no está en ningún bot

| Pregunta | Llamadas | Respuesta | Respuesta del equipo (resumen) |
|---|---|---|---|
| ¿Puedo recoger de noche, con el servicio nocturno o sin llaves? | 9 | 12/10 | No se puede fuera del horario de la oficina; puede recogerlo cuando abra, dentro de las 12 horas |
| Avisos del coche (navegador, software, ruedas) o un ruido extraño | 5 | 09/10 y 14/10 | Si es seguro, a la oficina más cercana; si no, teléfono de asistencia y ofrecer pasarle |
| Aviso de aceite, combustible equivocado o matrícula caída | 4 | 12, 13 y 16/10 | Llamar a asistencia en carretera |
| Contrato vencido y la web no deja alargar ni unas horas | 3 | 12/10 | Puede que el coche esté reservado; ir cuanto antes a la oficina de devolución; tiempo extra más 50 € por día |
| Teléfonos de asistencia y de reservas de Portugal, Italia y Grecia | — | 09/10 | Lista de números (ver tabla 4: el de Grecia tiene una errata) |
| Plazo del «Reembolso Cupón» | 2 | 14/10 | Unos 12 días naturales (la ficha del artefacto decía 72 horas) |
| Alquiler por meses o de larga duración | 2 | 15/10 | Hasta 29 días, km ilimitados; de 30 a 60, 100 km al día; suscripción de 3 meses a 1 año; precio en la web |
| Alquiler con otra empresa (el ejemplo era VoltioRent) | 2 | 12/10 | Condiciones, con esa empresa; combustible, extras, recogida, devolución y asistencia, desde aquí |
| Transporte público o shuttle al volver de la oficina | 2 | 12/10 | Sin datos de transporte público; el minibús de la oficina es gratis, en horario (Minibús ya lo dice) |
| ¿Está abierta la oficina en festivo? | 1 | 12/10 | Todos los días del año, también festivos; en Navidad puede cambiar (Minibús dice que no lo sabe) |
| ¿Qué es el fast track? | 1 | 08 y 09/10 | Fast Key: sin mostrador; se añade en «Modificar servicios»; no con agencia; requisitos; solo en horario |
| ¿Cómo sé si mi reserva es con Smart Key? | 1 | 14/10 | Obligatoria en Plaza de España, Recoletos y Glòries; en el resto, si lo activó |
| Coberturas: diferencia entre la total y la premium | 1 | 09/10 | Solo hay una, Smart Cover, incluida en el paquete Premium; sin franquicia |
| Cancelar un seguro adicional | 1 | 12/10 | Smart Cover se cancela en la oficina el día de la recogida; después, no |
| ¿Qué cubre el seguro de responsabilidad civil? | 1 | 13/10 | Texto legal completo; en el bloque va resumido |
| Pago en efectivo | 1 | 09/10 | Sí en España y Portugal, con depósito de la franquicia con tarjeta de crédito. Prolongaciones dice que no tiene el dato |
| Cambiar el titular de una reserva no iniciada | 1 | 09/10 | Cancelar y hacer otra a nombre del nuevo conductor |
| Cambiar el conductor principal con el alquiler en curso | 1 | 12/10 | No se puede; sí añadir un conductor adicional en una oficina |
| ¿Por qué cambia tanto el precio según el día? | 1 | 12/10 | Precios dinámicos; se puede cancelar y rehacer con la tarifa mejor |
| Me falta parte del depósito tras prolongar | 1 | 12/10 | Los reembolsos se hacen al terminar el contrato |
| ¿Anulo mi otra reserva y prolongo esta? | 1 | 13/10 | Puede ayudar, pero no está garantizado |
| Usuario de la web bloqueado | 1 | 09/10 | Comprobar el correo; si sigue, oficina o devolver a tiempo; formulario |
| ¿Necesito el número de reserva para prolongar? | 1 | 12/10 | No (la v12 de Prolongaciones ya lo dice) |
| No me aparece el botón de cancelar | 1 | 16/10 | Fuera del plazo de cancelación gratis ya no se reembolsa |
| Devolver en una ciudad y recoger otro coche en otra el mismo día | 1 | 12/10 | Sí, sin restricciones |
| Reembolso de un gasto (aceite) | 1 | 12/10 | Guardar el ticket y entregarlo al devolver; lo revisa posventa |
| Un cobro que no aparece en la reserva tras modificarla | 1 | 16/10 | Se reembolsa solo; hasta 12 días naturales |
| ¿Me envían el contrato por correo? | 1 | 12/10 | Se descarga en PDF desde el área de cliente |
| Cambiar el idioma de la app | 1 | 13/10 | En el perfil, «Información personal» |
| Zona de bajas emisiones de Madrid | 1 | 08 y 09/10 | Sin datos; lo comprueba el cliente con la matrícula; las multas son suyas |
| ¿El minibús es accesible en silla de ruedas? | 1 | 13/10 | No está adaptado (tampoco lo dice Punto de encuentro) |
| Una autoridad pide documentación de un coche | 1 | 08 y 09/10 | Por escrito al correo del departamento de flotas; teléfono si es urgente |
| ¿Qué oficina abierta me queda cerca para prolongar? | 1 | 13/10 | Google Maps; horarios en la web; según disponibilidad |
| Devolverlo con más combustible del que tenía | — | 09/10 | El reembolso tiene como máximo lo que pagó |
| Nota de estilo: repetir teléfonos y correos | — | 08/10 | «Estaría bien que se repitan dos veces» |

Además, el equipo añadió matices a respuestas que los bots ya tienen: extras y conductor adicional solo en
reservas directas, devolver en otra oficina avisando al recoger, MiDNI y permiso internacional, carnets de
otros países, la reserva nueva cuando no se puede prolongar (su recogida tiene que ser posterior a la
devolución), multas (Centauro no interviene después de identificar), facturas de extras con reserva de
intermediario, salir del país desde Portugal, Italia y Grecia, y espera por tren en Navidad. Van como notas
«Propuesta» en el bloque.

## 2. Lo que tiene Minibús v25 y le falta a Prolongaciones

| Pregunta | Llamadas | Dónde lo tiene Minibús |
|---|---|---|
| ¿Dónde está la oficina y cómo llego? | 13 | Información de oficina (lista de oficinas) |
| ¿A qué hora cierra la oficina? | 12 | Información de oficina, y Punto de encuentro para aeropuertos |
| ¿Se ha cerrado bien mi alquiler? (fianza y combustible) | 11 | Prolongación y consultas |
| ¿Dónde está el punto de encuentro? | 6 | Punto de encuentro |
| ¿Hablo con una persona o con un robot? | 4 | Prolongación y consultas (identidad y estilo) |
| ¿Puedo pagar la prolongación por teléfono o en la oficina? | 4 | Prolongación y consultas |
| La grúa se llevó el coche | 4 | Prolongación y consultas (teléfono de asistencia, como decidió el equipo) |
| Cambiar a un coche más grande con el alquiler en curso | 3 | Prolongación y consultas |
| ¿Cuánto tarda y cómo es el minibús? | 3 (sin respuesta del equipo) | Punto de encuentro (frecuencia y color) |
| ¿Puede recogerlo otra persona? | 2 | Prolongación y consultas |
| ¿Se puede ampliar el mismo día de la devolución? | 2 | Prolongación y consultas |
| Billete de vuelta y daños en salida | — | Prolongación y consultas |

Las de oficinas y punto de encuentro dependen de los datos de cada oficina, que en Minibús están en sus
módulos propios. Para Prolongaciones, la salida más corta es la que dio el equipo: remitir a la web
(«Oficinas») o al correo de confirmación, en lugar de transferir a Gestión.

## 3. Contradicciones

**Resueltas por el equipo y sin aplicar:**

| Tema | Qué decidió el equipo | Prolongaciones V11 | Minibús v25 |
|---|---|---|---|
| Coche de aseguradora (15/10) | Primero la aseguradora; si le remite a Centauro, oficina o web | «Prolónguelo usted mismo» | Solo «consúltelo con su aseguradora» |
| Plazo de la fianza (15/10) | Hasta 10 días hábiles; a veces semanas | «A los diez días» | Igual que Prolongaciones |
| Penalización de 50 € (15/10) | Daniel la puede decir | La dice | La dice |
| Grúa (09/10) | Teléfono de asistencia y ofrecer pasarle | Transfiere a Gestión | Como el equipo |
| Sillas para niños (09/10) | Tres tipos por peso; la instala el cliente | «Distintos tamaños» | Igual que Prolongaciones |
| Francés (09/10) | Ofrecer seguir en español, inglés, portugués o italiano | Ofrece español o inglés | Prolongación y consultas ofrece los cuatro; los otros tres módulos, dos |

En la penalización, lo que falta es quitarla de los fallos del extract de calidad (ya está en los
pendientes de Prolongaciones).

**Sin decidir (negocio):**
- Cancelar gratis: 24 horas (Prolongaciones, ficha del artefacto) o 48 (Minibús, y el equipo dos veces).
- Devolver antes: menos de 29 días (Prolongaciones, un revisor) o menos de 30 (Minibús, otro revisor y la
  ficha).
- Devolver con la oficina cerrada: según el equipo, Madrid aeropuerto también lo admite; Minibús dice que
  solo Alicante aeropuerto.
- Festivos: el equipo dice que las oficinas abren; Información de oficina de Minibús dice que no lo sabe.
- Cadenas de nieve: un revisor añade Grecia e Italia; otro dio por buena la ficha (solo Barcelona y Madrid).
- Adelantar una reserva de Booking: un revisor quita la alternativa del alquiler directo que dan los bots.

## 4. Errores en las respuestas del equipo

| Pregunta | Problema |
|---|---|
| Me han retenido la fianza por daños y necesito un justificante (12/10) | La respuesta es la del transporte público: se pegó en otra pregunta. Sigue sin respuesta |
| Mi reserva aún no ha empezado y quiero un día más (07/10, una de las dos) | Responde sobre el contrato vencido |
| ¿Me van a pedir el billete de vuelta? (07/10, una de las dos) | Responde sobre los documentos |
| Teléfono de asistencia de Grecia | Sale en tres formatos; uno (12/10) empieza por +31, el prefijo de Países Bajos |
| Aire acondicionado, aviso de batería y CarPlay (09/10) | Marcadas «hay que cambiarla» sin escribir otra respuesta |
| Adelantar la recogida de una reserva no iniciada (08/10) | Dice «contactar con Booking» aunque la pregunta no es de Booking |

## 5. Preguntas sin respuesta del equipo
- «Me han retenido dinero de combustible aunque mi contrato es lleno-lleno, ¿cómo lo reclamo?» (2 llamadas,
  16/10).
- «Estoy esperando el minibús de cortesía, ¿cuánto tarda en llegar y cómo es?» (3 llamadas, 16/10). Punto de
  encuentro de Minibús ya lo responde.

## 6. Cuánto subiría la resolución (estimación)

Muestra: las 182 llamadas de Prolongaciones V11 del 15/10 a las 18:36 al 17/10 a las 19:30 (hora de Madrid),
las mismas del informe `2026-10-17-resolucion-prolongaciones-vs-minibus.md`. Se leyó la transcripción de cada
una (8 subagentes, solo lectura en Twin). Una llamada cuenta como resuelta si el bot cubrió todo lo que pedía
el cliente sin transferir. Es más estricto que la «resolución real» de la rutina, que fue del 42 % el 15/10 y
del 47 % el 16/10, y aquí no se descuentan las rellamadas.

| Escenario | Resueltas | % |
|---|---|---|
| Hoy (V11) | 70 | 38 % |
| + respuestas del equipo, casos claros | 73 | 40 % |
| + respuestas del equipo, contando los dudosos | 90 | 49 % |
| + respuestas del equipo y de Minibús, casos claros | 77 | 42 % |
| + respuestas del equipo y de Minibús, contando los dudosos | 99 | 54 % |

- Lo que más suma: horario y dirección de oficinas de Minibús (8 llamadas), usuario web bloqueado (5),
  recogida de noche o con Fast Key (5), contrato vencido que la web no deja alargar (3), avisos y aceite (3),
  punto de encuentro y espera del minibús (3) y «¿hablo con una persona?» (3).
- Los dudosos (22) son llamadas en las que la respuesta nueva cubre la duda, pero el cliente insistía en una
  persona o tenía otra necesidad.
- Lo que sigue sin resolver aunque se añadan todas: 37 llamadas necesitan mirar o cambiar la reserva (20 %),
  12 cuelgan o se corta el audio, 11 son fallos del bot con la información que ya tiene, 9 piden una persona
  sin motivo y 8 son reservas nuevas (transferencia correcta).
- Fuera del catálogo: objetos olvidados (2), puntos de fidelidad para pagar (1), teléfono de una oficina de
  aeropuerto (1) y 3 clientes que preguntan con qué correo está registrado su alquiler.
- Datos de trabajo (por llamada, sin datos personales): `scratchpad/resolucion_nuevas/lote_0N.json` de la
  sesión del 17/10; no se versionan.

## 7. Y si además el bot tuviera el MCP de reembolsos y el de contraseña

Mismas 182 llamadas. Herramientas del MCP de Centauro (solo lectura salvo el envío del correo), todas con la
identidad verificada (número de reserva, correo o DNI, más nombre y fecha de nacimiento):
- `consultar_reserva`: estado, fecha y hora de recogida y devolución, oficinas, canal y dominio del correo;
- `consultar_reembolso`: fianza, combustible (niveles y reembolso), cancelación, cargos posteriores,
  reclamación abierta y factura;
- `enviar_reset_contrasena`: el correo para crear la contraseña.

Las 112 llamadas sin resolver se revisaron con los resúmenes de los subagentes; dos se contrastaron con la
transcripción.

| Escenario | Claros | Realista (dudosos a medias) | Techo |
|---|---|---|---|
| Hoy (V11) | 70 (38 %) | 38 % | 38 % |
| Solo el MCP | 72 (40 %) | 43 % | 84 (46 %) |
| Solo las respuestas nuevas (equipo y Minibús) | 77 (42 %) | 48 % | 99 (54 %) |
| Respuestas nuevas + MCP | 79 (43 %) | 53 % | 113 (62 %) |

- **Lo que añade el MCP** (14 llamadas que las respuestas no cubren):
  - 6 clientes que no ven su reserva porque no saben con qué correo está (`consultar_reserva` da el dominio
    y luego se envía la contraseña);
  - 5 dudas sobre un cobro, la fianza o el combustible (`consultar_reembolso`);
  - 3 que quieren confirmar su reserva o su hora de devolución.
- **El envío de la contraseña casi no suma por sí solo:** en las llamadas que terminan resueltas, el bot ya
  da los pasos de «¿Has olvidado tu contraseña?», y los que cuelgan mientras los oyen (4) no aguantarían la
  identificación, que alarga la llamada. Donde ayuda es con la reserva asociada a otro correo y con las
  cuentas bloqueadas (4 llamadas, que siguen como dudosas).
- **Lo que queda fuera aunque se añada todo** (69 llamadas):
  - 23 piden un cambio: cancelar, cambiar la oficina o la hora, añadir un conductor o comprobar el servicio
    de espera con la oficina (9 por vuelos retrasados). El MCP es de lectura;
  - 12 cuelgan o se corta el audio;
  - 9 fallos del bot con información que ya tiene (se arreglan en el prompt);
  - 8 reservas nuevas, 8 que piden una persona sin motivo y 2 averías, que tienen que ir a un agente;
  - 6 preguntas sin respuesta en ningún sitio (objetos olvidados, puntos de fidelidad…).
- Clasificación por llamada: `scratchpad/resolucion_nuevas/mcp_clasificacion.json` de la sesión del 17/10.
