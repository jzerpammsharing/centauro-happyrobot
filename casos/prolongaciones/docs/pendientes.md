# Pendientes del caso Prolongaciones

## Incidencias abiertas
- [ ] **Transferencias a Gestión con la cola cerrada (causa sin arreglar).**
  - **Qué pasa:** con Gestión cerrada, «Resolver colas» pone el texto «NO DISPONIBLE AHORA…» en
    `cola_gestion_reserva`. En la V10, el bot copió ese texto en `extension_destino` en 3 de 3 casos
    reales (10/10 a las 21:17 y 21:44, y 11/10 a las 09:50). La transferencia falló con «invalid phone
    number» después de anunciar «le paso con un compañero».
  - **Qué hace la V11:** lo frena solo con el prompt.
  - **Qué sigue fallando:** en las evaluaciones, la prueba FDS-05 (conversación larga con Gestión
    cerrada) todavía transfiere 3 de cada 7 veces.
  - **Arreglo:** cambiar «Resolver colas» para que, con Gestión cerrada, no haya ningún destino de
    gestión. Falta que el negocio decida si no se ofrece ningún destino o si se manda a otra cola
    abierta.
  - **En producción con la V11** (11/10, 36 llamadas con Gestión cerrada): 0 intentos de transferir
    a Gestión. Pero ningún cliente insistió de verdad en hablar con una persona, que es el caso de
    FDS-05, así que sigue sin probarse. Minibús España v22 sí copió el texto el mismo día (f06cc517):
    ver los pendientes de Minibús.
  - **Efecto secundario:** sin poder transferir, el bot repite el horario de Gestión como única
    salida (3 o 4 veces en 431fb6c7 y 340cde9a) y no ofrece Nueva reserva cuando el coche no está
    disponible (38137f1d, 64d28e50).
- [ ] **El destino de reserva de la transferencia es la cola de Gestión.** En «Initiate customer
      connection», `fallback_number` es `cola_gestion_reserva`.
  - Con Gestión cerrada, el destino de reserva es el texto «NO DISPONIBLE…», que no es un número.
  - Con Gestión abierta, una transferencia fallida a Asistencia, Nueva reserva o Minibús podría acabar
    en Gestión.
  - Falta comprobar en HappyRobot cuándo se usa `fallback_number` y decidir qué valor debe tener.
- [ ] **Gestión no atiende en fin de semana.**
  - En RingCentral, el horario de 18057 y 18061 es de 08:00 a 22:00 los 7 días. Pero la regla «FHL -
    Opción 3 Fin de Semana» (del viernes a las 21:00 al lunes a las 08:00) solo reproduce un anuncio.
  - Sábado 10/10: 0 de 173 patas de bots atendidas y 230 llamadas directas perdidas.
  - Falta que Centauro confirme que es intencionado. Este horario es el que codifica `gestion_abierta`.
- [ ] **Festivos: ni `gestion_abierta` ni el prompt los conocen.**
  - El lunes 12/10 es festivo nacional. `gestion_abierta` lo dará como abierto de 08:00 a 21:00; si
    la Gestión no tiene agentes ese día, el bot transferirá a una cola sin nadie.
  - El 11/10 el bot mandó a un cliente sin internet, con el contrato venciendo el 12/10, a llamar «de
    lunes a viernes de 8 a 21» (1aaa05f0 y su rellamada 59fdebe2).
  - Falta confirmar si la Gestión trabaja los festivos y añadir una salida tipo `festivo_hoy` en
    «Calcular idioma y saludo».
- [ ] **La V11 se publicó sin seguir el proceso del repo.** Se publicó el 11/10 sin guardar antes el
      prompt, sin una entrada en decisiones y sin PR, y con el nombre genérico «Version 11» en vez de
      «v11 · v10 + …».
  - El prompt ya está guardado (`prompts/prolongacion-es/v11/`) y la decisión reconstruida (D-006).
  - Falta confirmar quién la publicó y a qué hora.
- [ ] **El aviso legal en inglés es la grabación en español.** En «Calcular idioma y saludo», la
      línea inglesa usa el mismo `recording_id` que la española. El propio código lo marca como
      PENDIENTE.
- [ ] **Prompt del extract desactualizado.**
  - El «FLUJO ESPERADO» dice «Todo lo demás lo transfiere», pero desde la V8 y la V9 Daniel responde
    muchas consultas sin transferir.
  - `dijo_precio_o_penalizacion` e `invento_informacion` marcan como fallo cosas que el prompt del bot
    permite: la penalización de 50 €/día, las tarifas generales y los teléfonos de Benidorm y
    Torrevieja.
  - Además evalúa también al agente humano.
  - Hay que actualizarlo en una versión nueva.

## Mejoras propuestas
- [ ] **Renombrar 18034 y 18035 en «Resolver colas».** Ahora se llaman «RA ES-ES-Opciones» y «RA
      ES-EN-OPCIONES», que son los nombres de los menús 2114 y 2115. Los nombres correctos son «RA ES-ES
      AVERÍAS» y «RA ES-EN Breakdowns». No cambia el destino, pero confunde al revisar el código.
- [ ] **Revisar adónde va un idioma no atendido.**
  - Ahora va a la cola de Minibús (18056 o 18059), una regla copiada del workflow de Minibús.
  - Además, las llamadas en italiano o portugués que se transfieren llegan a colas españolas, porque
    las colas se eligen por la línea marcada, no por el idioma hablado.
- [ ] **Aclarar una contradicción del prompt.** Dice «Nunca das el teléfono de una oficina», pero en
      «TELÉFONOS QUE PUEDES DAR» incluye Benidorm y Torrevieja para el servicio de entrega. Hay que
      dejar la excepción explícita en «QUÉ NO HACES NUNCA».
- [ ] **Dar el horario de las oficinas con los datos de Minibús.**
  - El bot no tiene horarios de oficina (salvo Benidorm y Torrevieja) y transfiere esas preguntas a
    Gestión, que en fin de semana está cerrada.
  - En 127 llamadas analizadas (V8, V10 y V11), 6 preguntaban el horario de una oficina y en unas 6
    más el bot mandaba al cliente a la oficina sin poder decirle cuándo abre.
  - Minibús España tiene la lista de oficinas con horarios y las reglas para darlos
    (`../../minibus/prompts/minibus-es/v22/informacion-de-oficina.md`, sección HORARIO y lista
    OFICINAS). Opción más rápida: copiar la parte de España en el prompt y cambiar la regla de
    «Horario o dirección de una oficina concreta». Hay que decidir quién mantiene las dos copias.
  - El artefacto «Respuestas de Daniel» tiene una tabla de oficinas (`offices`) que conviene cruzar.
- [ ] **Limpiar los borradores Version 1 a 4**, que nunca se publicaron y son de pruebas. La Version 5
      no aparece en HappyRobot.

## Revisado sin incidencias (11/10/2026, V11)
- Variables: todas apuntan a persistent_id que existen; no hay variables rotas.
- Extensiones: ninguna vacía. `extension_destino` es obligatoria y el prompt insiste en rellenarla.
- Extensiones prohibidas: la V11 no transfiere a 2114, 2115 ni 2119. La V6 sí mandaba las averías a
  2114/2115; se corrigió en la V7 (18034/18035).

## Hechas
- [x] Documentar el caso: `CLAUDE.md` y `docs/workflows.md` (11/10/2026).
- [x] Guardar en `prompts/` los prompts de la versión publicada (V11) y el de la V10 para comparar
      (11/10/2026).
- [x] Revisar que no transfiere a 2114, 2115 ni 2119 (C-001) (11/10/2026).
