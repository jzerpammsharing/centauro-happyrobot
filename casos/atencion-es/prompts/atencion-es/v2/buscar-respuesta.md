<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v2 (x8xd0llbdp3j) · nodo: Buscar respuesta (Consultas del alquiler) · copiado: 2026-10-18 (Tarea 9b) -->

# Buscar respuesta (código Python) · Consultas del alquiler

- Herramienta `buscar_respuesta` (tool): ID = persistent_id en la v2 `01a14fa1-5c34-7bff-9366-aa7e9e4e448a`; padre, el
  prompt «Consultas del alquiler» (`01a14f1d-0397-7b22-b5ce-bcb398a7605e`, persistent_id
  `38378785-0846-4920-b41a-583f7c5773fb`). `message`: `{"type": "none"}`. Descripción y parámetros:
  `herramientas-consultas.md` (§1).
- Hijo: action (Python Sandbox) «Buscar respuesta», event_id `019dde7b-3500-7a3c-8f5e-1c2d4e6a8b9c`,
  execution_profile `standard`; ID = persistent_id en la v2 `01a14fa1-5c44-7c37-821c-1d01c0bd41eb` (creado en la
  Tarea 9). No tiene hijos: el agente recibe su salida como resultado de la herramienta.
- Código: `casos/atencion-es/codigo/consultas_alquiler.py` tal cual (39.162 caracteres; regenerado y pegado en la
  Tarea 9b, 18/10/2026, tras C-005: sin los teléfonos de asistencia de otros países, con «no tienes esos
  teléfonos» en su lugar y con «No digas que no está permitido…» en la oficina cerrada). El nodo lo aceptó entero: no hizo falta partir `SECCIONES`
  (spec §11.6).
- La Tarea 10 crea una herramienta igual en Prolongación (mismo código; cambia el persistent_id de la herramienta en
  las entradas).

## Entradas (input_data)

```json
[
  {"key": "tema", "value": "{{01a14fa1-5c34-7bff-9366-aa7e9e4e448a.tema}}"},
  {"key": "pregunta", "value": "{{01a14fa1-5c34-7bff-9366-aa7e9e4e448a.pregunta}}"}
]
```

## Salida

`tema` (el tema que se ha usado), `texto` (la sección de ese tema) y `encontrado` (false si el tema no era válido o
llegó vacío; entonces devuelve la sección `otras`).

## Pruebas con `test_node` (Paso 3; 18/10/2026)

`test_node` no usa los argumentos de la herramienta (llegan vacíos), así que para la prueba se puso `tema` como texto
fijo y después se volvió a dejar la variable de la herramienta:

| tema | encontrado | tema devuelto | texto |
|---|---|---|---|
| (argumento vacío) | false | otras | sección «otras» |
| `requisitos` | true | requisitos | sección «requisitos» (carnet, documentos, tarjeta…) |

En las evals la herramienta se ejecuta de verdad: las que llaman a `buscar_respuesta` reciben la sección real.

## Código

```python
# ===============================================================
# CONSULTAS DEL ALQUILER - bot único de Atención España
# ---------------------------------------------------------------
# GENERADO: este fichero no se edita a mano. Sale de comun/bloques/consultas-alquiler.md (solo la parte «## Bloque»,
# sin las notas, que son las líneas que empiezan por «>») con:
#
#     python3 -I casos/atencion-es/codigo/generar_consultas.py
#
# Para cambiar una respuesta se edita el bloque, se vuelve a generar y se pega el fichero entero en HappyRobot.
#
# Se pega tal cual en el nodo Python de la herramienta «buscar_respuesta». Entradas (input_data): tema (una de las
# claves de SECCIONES) y pregunta (la duda del cliente; el nodo no la usa). Salidas: tema (el usado), texto (la
# sección de ese tema) y encontrado (False si el tema no existía y se ha devuelto la sección «otras»).
# ===============================================================

# Una sección por tema, en el orden del bloque. Cada texto va troceado por párrafos para que los cambios del
# bloque se vean párrafo a párrafo en git.
SECCIONES = {
    'devolver_tarde': (
        'Si el cliente pretende devolver después de la hora sin prolongar, aunque sean pocas horas, o pregunta si hay margen: explica, en dos turnos si hace falta, que no hay periodo de cortesía y que el alquiler se cuenta en periodos de veinticuatro horas, así que aunque sea una hora más se paga un periodo completo (por eso la web le muestra un día entero). Devolverlo fuera de la fecha y hora del contrato sin prolongar supone el cobro del tiempo adicional más una penalización, así que lo mejor es prolongar antes de la hora, desde la web, la app o en una oficina. Ejemplo de primer turno: "No hay periodo de cortesía: el alquiler se cuenta por periodos de veinticuatro horas, y devolverlo más tarde sin prolongar supone el cobro del tiempo extra más una penalización. Lo mejor es prolongarlo antes de la hora. ¿Ha entrado alguna vez en su cuenta de Centauro?" Después sigue con EXPLICACIÓN. No confirmes cuál es su hora de devolución: no lo sabes. Si pregunta cuánto es la penalización, dale la cifra de DETALLES QUE PUEDES DAR.'
    ),
    'aseguradora_empresa': (
        'Coche de sustitución de su aseguradora o de su mutua: si el cliente quiere quedárselo más días, NO transfieras por ese motivo. Primero dile, en un turno: "La prolongación de un coche de sustitución tiene que pedírsela a su aseguradora." Si te dice que ya lo ha hecho y su aseguradora le ha remitido a Centauro, dile que puede prolongarlo él mismo desde su área de cliente en centauro punto net o en la app, o en una oficina, siempre que el coche siga disponible, y sigue con EXPLICACIÓN. Si pregunta el precio, por teléfono no tienes acceso a la tarifa: lo verá en pantalla antes de pagar.\n\n'
        'Si pregunta si su seguro le cubre los días extra o quién lo paga, di: "Eso depende de su póliza; se lo confirma su aseguradora. Si lo prolonga usted desde la web, el importe se paga allí al confirmar." Nunca digas que el seguro se lo cubre ni que no se lo cubre: no lo sabes.\n\n'
        'Si pregunta cuántos días puede alargarlo, dile que eso también se lo confirma su aseguradora; si su aseguradora ya le ha remitido a Centauro, aplica "Cuánto se puede prolongar" de DETALLES QUE PUEDES DAR. Si pregunta por su caso concreto, transfiere a GESTIÓN DE RESERVA.\n\n'
        'Coche de empresa (su empresa tiene acuerdo con Centauro): la prolongación la hace el gestor de su empresa, que gestiona sus alquileres con Centauro desde el portal de empresas. Si no hay disponibilidad, tienen que contactar con el comercial de Centauro de su zona. No transfieras por este motivo.\n\n'
        'Si quien llama no es el cliente sino la propia aseguradora, una mutua, un club de asistencia o el gestor de una empresa, transfiere a GESTIÓN DE RESERVA con motivo_transferencia aseguradora. Un cliente que dice "es el coche de mi aseguradora" o "es de sustitución" es un CLIENTE: sigue este apartado y NO uses el motivo aseguradora. Si no queda claro quién llama, pregunta UNA vez "¿Llama usted como cliente del coche o en nombre de la aseguradora?" antes de transferir.'
    ),
    'detalles_prolongacion': (
        'Precio: empieza SIEMPRE respondiendo directamente que por teléfono no tienes acceso a la tarifa y que lo verá al consultar el importe, antes de pagar. Solo después, si hace falta, sigue con la explicación. Es la tarifa vigente para las nuevas fechas, así que puede ser distinta de la que pagó por el alquiler original. Por teléfono no hay acceso a la tarifa. No añadas motivos sobre cómo se calcula (demanda, tipo de coche, temporada, disponibilidad): di solo que es la tarifa vigente para las nuevas fechas.\n\n'
        'Si pregunta si el importe que le muestra la web o la app es correcto: es la tarifa vigente que calcula el sistema y tú no puedes comprobarlo. Si le sorprende que le cobre un día entero por pocas horas, recuérdale que se cuenta en periodos de veinticuatro horas.\n\n'
        'Condiciones: la prolongación mantiene las mismas coberturas y extras que tiene contratados; lo que cambia es la tarifa, que se calcula para las nuevas fechas.\n\n'
        'Penalización por devolver tarde: si pregunta cuánto le van a cobrar por devolverlo tarde, di: "De acuerdo con las condiciones actuales, la penalización es de cincuenta euros por día de demora, más el coste de los días adicionales a la tarifa vigente." No calcules el total de su caso. Preguntar el importe NO es motivo para transferir. Solo si después sigue insistiendo en ese punto (el total exacto, su caso concreto, que se lo quiten), transfiere a GESTIÓN DE RESERVA con motivo_transferencia otro.\n\n'
        'Prolongar en una oficina: si pregunta si puede hacerlo en persona, di que sí, que también puede gestionar la prolongación en una oficina de forma presencial, siempre que el coche esté disponible. No transfieras por esta pregunta. Si dice que prefiere ir a la oficina porque no se maneja con la web, no le preguntes por la cuenta ni le des los pasos de la web: recuérdale que lo haga antes de la hora de devolución y pregunta si puede ayudarle en algo más.\n\n'
        'Pagar la prolongación: se paga en el momento de hacerla, en la oficina o en la web.\n\n'
        'Prolongar el mismo día de la devolución: es mejor hacerlo con antelación, pero se puede el mismo día desde el área de cliente si hay disponibilidad. Si no puede, tiene que devolverlo en fecha y hora.\n\n'
        '¿Está bien hecha mi prolongación?: si al pagar le llegó el correo de confirmación y en "Mis reservas y facturas" aparece la nueva fecha de devolución, está hecha.\n\n'
        'Contrato ya vencido: el contrato no se prorroga solo. Si no lo prolonga en la web, en la app o en una oficina, se cobra el tiempo extra más cincuenta euros por cada día; lo mejor es prolongarlo o devolver el coche cuanto antes. Si pregunta si le pueden denunciar: si no prolonga ni devuelve el coche, pasados unos días Centauro puede presentar una denuncia por apropiación indebida. Si ya lleva días de retraso y quiere explicar su situación, transfiere a GESTIÓN DE RESERVA con motivo_transferencia pregunta_reserva_concreta.\n\n'
        'Contrato vencido y la web no le deja prolongar, ni siquiera unas horas: puede que el coche esté reservado para otro alquiler. Que vaya cuanto antes a la oficina donde tiene que devolverlo para ver qué opciones tiene. Recuérdale que se cobra el tiempo extra más cincuenta euros por día.\n\n'
        'Devolver antes de la nueva fecha: aplica "Si lo devuelve antes" de CONSULTAS FRECUENTES.\n\n'
        'Le falta parte del depósito o de la fianza después de prolongar: los reembolsos se hacen al terminar el contrato, no al prolongar.\n\n'
        'Precio caro: si se queja de que la prolongación le parece muy cara, valida ("lo entiendo") y explica en una frase que el precio depende de la tarifa vigente en ese momento y que por eso puede variar. En ese mismo turno ofrece que un compañero lo revise con él ("¿Quiere que le pase con un compañero para ver si hay alguna alternativa?"); si acepta, transfiere a GESTIÓN DE RESERVA con motivo_transferencia otro.\n\n'
        'Cuánto se puede prolongar: los alquileres de menos de veintinueve días, hasta veintinueve días en total; los de entre treinta y sesenta, hasta sesenta. Si pregunta cuánto le queda a él en concreto, transfiere a GESTIÓN DE RESERVA.\n\n'
        'Cambiar de coche: si quiere prolongar pero con otro coche (más grande, distinto), explica que la prolongación es siempre del mismo coche y pregunta si quiere que un compañero le prepare una reserva nueva para el otro coche. Es una oferta, no una petición de reserva nueva: transfiere a NUEVA RESERVA solo si dice que sí.\n\n'
        'Cambiar a un coche más grande con el alquiler en curso: tiene que ir a una oficina, que comprueba si hay disponibilidad, y paga la diferencia.\n\n'
        'Otra reserva para esas fechas: si tiene otra reserva confirmada que empieza cuando acaba este alquiler y pregunta si, cancelándola, puede quedarse este coche más días, dile que puede ayudar, porque no se pueden tener dos reservas confirmadas para las mismas fechas, pero que no está garantizado: depende de que el coche que lleva siga disponible.\n\n'
        'Cualquier otra pregunta sobre condiciones que no esté en estas instrucciones, o sobre qué pasa en su caso concreto: remite a los términos y condiciones de centauro punto net o transfiere a GESTIÓN DE RESERVA. No lo deduzcas.'
    ),
    'la_web_no_le_deja': (
        'Pregunta UNA sola vez qué le indica la web.\n\n'
        'Si es que la fecha u hora no es válida: pídele que pruebe con una hora posterior a la de devolución actual.\n\n'
        'Si es que el coche no está disponible o no le deja prolongar: NO transfieras. Valida ("entiendo que le complica") y explica que, si la web no le ofrece prolongar, es que no hay disponibilidad, y que tiene que devolver el coche en la fecha y hora del contrato, en la misma oficina donde lo recogió. En el turno siguiente, si viene al caso, dale la alternativa: puede hacer una reserva nueva a partir de ese día, en la web o en el mostrador cuando devuelva el coche, si hay disponibilidad, y hacer el cambio en la oficina; si prefiere, un compañero se la prepara. Solo si acepta que se la prepare un compañero, transfiere a NUEVA RESERVA. Si pregunta qué pasa si no lo devuelve a tiempo, explica DEVOLVER TARDE (y la cifra de la penalización si la pide).\n\n'
        'Si pregunta por esa reserva nueva: su hora de recogida tiene que ser posterior a la devolución de este coche; no puede caer dentro del alquiler actual.\n\n'
        'Si ya lo prolongó antes y ahora no le deja alargarlo más: puede ser que haya llegado al máximo de días (ver "Cuánto se puede prolongar") o que no haya disponibilidad. En los dos casos, las opciones son las mismas: devolverlo en la fecha del contrato o hacer una reserva nueva.\n\n'
        'Si no le deja pagar, el pago da error, la web sale en blanco o no carga: antes de transferir, sugiere alternativas, una por turno: probar desde otro dispositivo, desde la app, o con otro método de pago; también puede prolongar en una oficina. Si pregunta qué tarjetas o métodos de pago se aceptan para pagar en la web (marcas de tarjeta, Bizum, PayPal...), no tienes ese dato confirmado: dilo así, no nombres ninguno y sugiere que pruebe con otra tarjeta. En ese turno NO transfieras ni ofrezcas transferir. Solo si después insiste en que necesita confirmarlo, transfiere a GESTIÓN DE RESERVA con motivo_transferencia error_tecnico. Si dice que ya lo ha probado todo y sigue fallando, recuérdale en una frase que, si no consigue prolongar, tiene que devolver el coche en fecha y hora, y transfiere a GESTIÓN DE RESERVA con motivo_transferencia error_tecnico.\n\n'
        'Si le han cobrado y la prolongación no se ha confirmado: la web reembolsa automáticamente cualquier cobro que no corresponda a una reserva o prolongación confirmada. Puede tardar hasta doce días en verlo en su cuenta, según su banco.\n\n'
        'Si no le llega el correo de la contraseña: dile que puede tardar unos minutos, que compruebe que el correo es exactamente el que dio en la oficina, sin erratas, y que revise todas las carpetas, también la de correo no deseado. Si no le llega, puede pedirlo otra vez. Solo si después de eso sigue sin llegarle, transfiere a GESTIÓN DE RESERVA con motivo_transferencia error_tecnico. No le guíes pantalla a pantalla.\n\n'
        'Si entra en su cuenta pero no ve la reserva: en ese turno NO transfieras. Dile que la reserva está asociada al correo que dio al recoger el coche y pregúntale si ha entrado con ese correo. Solo si con ese correo tampoco la ve, transfiere a GESTIÓN DE RESERVA con motivo_transferencia pregunta_reserva_concreta.\n\n'
        '¿Necesita el número de reserva para prolongar?: no. Entrando en su área de cliente con el correo que dio al recoger el coche verá su alquiler y su número de reserva.\n\n'
        'Usuario bloqueado: que compruebe que entra con el correo que dio al recoger el coche. Si sigue bloqueado, puede prolongar en una oficina, si hay disponibilidad, o devolver el coche en fecha y hora. Para recuperar la cuenta, el formulario de "Atención al cliente y reclamaciones" de centauro punto net.'
    ),
    'reserva_no_iniciada': (
        'Son preguntas que no son de prolongación, pero que puedes responder tú. Responde solo con lo que pone aquí, en una o dos frases por turno, y no añadas nada que no esté escrito. Si el cliente necesita después que alguien mire o cambie su reserva, transfiere a GESTIÓN DE RESERVA.\n\n'
        'REGLA: cambiar o cancelar una reserva que aún no ha empezado, recoger antes, cambiar la hora, añadir horas o un día, cambiar de coche, y el cupón o el reembolso de una cancelación NO se transfieren: respóndelo tú con lo de abajo. Solo transfieres a GESTIÓN DE RESERVA (motivo_transferencia no_iniciada) si, DESPUÉS de tu respuesta, el cliente dice que prefiere que lo haga un compañero. Que el cliente diga "quiero modificar mi reserva" no es una petición de compañero. Si ya has dado la respuesta y el cliente lo entiende, no la repitas ni transfieras.\n\n'
        'Cambiar fechas, hora, oficina o coche, o añadir un día: dilo así: "Antes de recoger el coche la reserva no se puede modificar: hay que cancelarla y hacer una nueva, si hay disponibilidad, y el precio puede cambiar porque se aplica la tarifa de ese momento."\n\n'
        'Cambiar el titular: no se puede cambiar en la reserva; hay que cancelarla y hacer una nueva a nombre del nuevo conductor, si hay disponibilidad. Si reservó con una agencia, se hace con ellos.\n\n'
        'Recoger antes de la hora de la reserva: no se le puede garantizar; puede preguntar en la oficina al llegar si el coche ya está disponible. Si necesita asegurarse esa hora, o quiere recogerlo un día antes, hay que cancelar y hacer una reserva nueva, si hay disponibilidad, y el precio puede cambiar. Nunca le prometas que se lo darán antes.\n\n'
        'Si no pudo recoger el coche a su hora y pregunta si puede recogerlo ahora u hoy, no es un cambio de reserva: sigue NO PUDO RECOGER A SU HORA, en RECOGER TARDE.\n\n'
        'Un día más al final: también puede preguntar en la oficina, al recoger el coche, si se puede prolongar, según la disponibilidad de ese momento. Pero si ya sabe que lo va a necesitar, es mejor no arriesgarse y cambiar la reserva antes.\n\n'
        'Cancelar: es gratis hasta veinticuatro horas antes de la recogida, desde su área de cliente en centauro punto net. Si pagó por adelantado, recibe un cupón por el importe, que puede usar en la nueva reserva, en el último paso, en la casilla del cupón de descuento.\n\n'
        'No le aparece el botón de cancelar: la web solo deja cancelar sin coste dentro del plazo de arriba; pasado ese plazo, la reserva no se reembolsa.\n\n'
        'Si prefiere el dinero en vez del cupón: en "Mis reservas y facturas", en la reserva cancelada, pulse "Reembolso Cupón". Tiene tres meses desde la cancelación para pedirlo; el cupón vale dos años para reservas en el mismo país.\n\n'
        'Plazo del reembolso: una vez pedido el "Reembolso Cupón", el dinero llega en unos doce días naturales, según su banco.\n\n'
        'El precio cambia según el día en que reserva: los precios son dinámicos y dependen de la disponibilidad y de la demanda. Si ya tiene una reserva y ve una tarifa mejor, puede cancelarla y hacer otra con ese precio, si hay disponibilidad; si pagó por adelantado, recibe un cupón.\n\n'
        'Reservó con Booking u otra agencia: los cambios y cancelaciones se hacen con ellos. Si quiere adelantar el inicio de una reserva de Booking, con Centauro no se puede: puede cancelarla con Booking y hacer otra, o hacer un alquiler directo con Centauro por los días que necesita adelantar y luego, en la oficina, cerrar ese contrato y empezar la reserva que ya tenía.\n\n'
        'Añadir un extra, el número de vuelo o pagar por adelantado: desde su área de cliente en centauro punto net.\n\n'
        'Fast Key o recogida rápida (a veces lo llaman "fast track"): sirve para recoger el coche sin pasar por el mostrador. No siempre está disponible; si lo está, se añade desde su área de cliente, en su reserva, con "Modificar servicios". Con reservas de agencia no se puede. Hace falta digitalizar la documentación en centauro punto net y pagar por adelantado la reserva y el combustible. Solo funciona en el horario de la oficina.\n\n'
        'Smart Key: en las oficinas sin personal (Madrid Plaza de España, Madrid Recoletos y Barcelona Glòries) la recogida es siempre con Smart Key. En el resto, solo si lo activó al reservar o después en su área de cliente, cuando está disponible.\n\n'
        'Cancelar la cobertura Smart Cover: Centauro no vende seguros sino coberturas. Si aún no ha recogido el coche, puede cancelarla en la oficina el día de la recogida; con el coche ya recogido, no se puede cancelar.\n\n'
        'Si prefiere que un compañero le haga la cancelación o el cambio, transfiere a GESTIÓN DE RESERVA con motivo_transferencia no_iniciada.'
    ),
    'recoger_tarde': (
        'Son preguntas que no son de prolongación, pero que puedes responder tú. Responde solo con lo que pone aquí, en una o dos frases por turno, y no añadas nada que no esté escrito. Si el cliente necesita después que alguien mire o cambie su reserva, transfiere a GESTIÓN DE RESERVA.\n\n'
        'Va a llegar tarde a recoger: no pierde la reserva. Se guarda hasta doce horas desde la hora de recogida, siempre dentro del horario de la oficina; no tiene que cambiar nada y la hora de devolución sigue igual. Si viene en avión, el número de vuelo tiene que estar en la reserva; lo puede añadir en su área de cliente.\n\n'
        'NO PUDO RECOGER A SU HORA: si no llegó a recoger el coche (por ejemplo, ayer por la noche) y pregunta si puede recogerlo ahora u hoy, dile que la reserva se guarda hasta doce horas desde la hora de recogida, dentro del horario de la oficina: si todavía no han pasado doce horas, puede ir a recogerlo hoy a la oficina en su horario. Si ya han pasado o no está seguro, que pase por la oficina donde tenía la recogida para que le den una solución. Nunca le confirmes que el coche le está esperando ni cuántas horas le quedan, y no le digas que tiene que cancelar ni hacer una reserva nueva. Esto vale también con Gestión cerrada.\n\n'
        'Llega de noche o con la oficina cerrada: no se puede recoger el coche fuera del horario de la oficina, tampoco con el servicio sin llaves. Puede recogerlo cuando abra la oficina, dentro de las doce horas que se guarda la reserva.\n\n'
        'Su vuelo llega cuando la oficina ya ha cerrado: explícale primero el servicio, sin prometer nada: "En algunas oficinas de aeropuerto hay un servicio de espera por vuelo retrasado, que cuesta cuarenta euros y llega como mucho hasta la una de la madrugada, pero no siempre está disponible: hay que comprobarlo el mismo día de la recogida, antes de las diez de la noche." Si la recogida es hoy, termina ese turno con "¿Quiere que le pase con un compañero para comprobarlo?". Si no es hoy, recuérdale que la reserva se guarda doce horas dentro del horario de la oficina.\n\n'
        'Su tren llega tarde: explícale primero el servicio, sin prometer nada: "En algunas estaciones hay un servicio de espera de cuarenta euros, de como mucho sesenta minutos, pero hay que comprobarlo el mismo día de la recogida, antes de las diez de la noche." Si la recogida es hoy, termina ese turno con "¿Quiere que le pase con un compañero para comprobarlo?". Las estaciones son Sevilla Santa Justa, Málaga María Zambrano, Valencia Joaquín Sorolla, Alicante, Madrid Atocha, Madrid Chamartín, Santiago, Bilbao Abando, Zaragoza Delicias y Barcelona Sants; dilas solo si te pregunta por una.\n\n'
        'Si acepta que le pases para comprobar el servicio de espera, transfiere a GESTIÓN DE RESERVA con motivo_transferencia otro. Nunca prometas que le van a esperar.'
    ),
    'devolucion': (
        'Son preguntas que no son de prolongación, pero que puedes responder tú. Responde solo con lo que pone aquí, en una o dos frases por turno, y no añadas nada que no esté escrito. Si el cliente necesita después que alguien mire o cambie su reserva, transfiere a GESTIÓN DE RESERVA.\n\n'
        'Si lo devuelve antes: en reservas hechas directamente con Centauro de menos de veintinueve días, el sistema devuelve los periodos completos de veinticuatro horas que no use. Con veintinueve días o más no se devuelve nada. Si reservó con una agencia o intermediario, Centauro no hace ese reembolso: tiene que consultarlo con la agencia.\n\n'
        'En otra oficina: se puede devolver en otra oficina de Centauro si se indicó al hacer la reserva. Si la web no deja reservar ese trayecto, no está permitido. El precio depende del trayecto; con el alquiler ya en curso, el recargo se paga en la oficina de devolución.\n\n'
        'Devolver en una ciudad y recoger otro coche en otra el mismo día: sí se puede; no hay ninguna restricción.\n\n'
        'Con la oficina cerrada: depende de la oficina; algunas tienen buzón de llaves y otras no lo permiten. Se acuerda al recoger el coche, y allí le dan las instrucciones. No digas que no está permitido ni que solo se puede si lo acordó: depende de la oficina. Si deja el coche fuera de las instalaciones de Centauro, responde de los gastos y daños. Si no lo acordó al recoger, transfiere a GESTIÓN DE RESERVA con motivo_transferencia otro.\n\n'
        'Volver desde la oficina de devolución: no tienes información del transporte público. Si la oficina tiene minibús de cortesía, puede usarlo gratis para volver al aeropuerto, dentro del horario de la oficina.'
    ),
    'cargos_y_reembolsos': (
        'Son preguntas que no son de prolongación, pero que puedes responder tú. Responde solo con lo que pone aquí, en una o dos frases por turno, y no añadas nada que no esté escrito. Si el cliente necesita después que alguien mire o cambie su reserva, transfiere a GESTIÓN DE RESERVA.\n\n'
        'Fianza: es una retención si es tarjeta de crédito y un cargo real si es de débito. Suele volver a estar disponible en un plazo de hasta diez días hábiles; según el banco puede tardar más, a veces varias semanas, así que para más detalle lo mejor es consultar con su banco.\n\n'
        'Combustible: al recoger se paga el combustible que lleva el coche y al devolverlo se reembolsa el que no se ha gastado; si lo devuelve con el mismo nivel, se le devuelve entero. No hace falta repostar. Centauro ordena el reembolso al cerrar el contrato; según su banco, puede tardar hasta doce días en verlo en su cuenta.\n\n'
        'Si lo devuelve con más combustible del que tenía: se le reembolsa como mucho lo que pagó al recogerlo; el combustible de más no se compensa.\n\n'
        'Reembolso del combustible en dos pagos: a veces el sistema lo devuelve en dos pagos distintos. Que revise los movimientos con su banco para comprobar que ha recibido el total.\n\n'
        '¿Se ha cerrado bien mi alquiler?: cuando se cierra el contrato le llega un correo con una encuesta y un enlace a su área de cliente, donde puede descargar el contrato y las facturas. La fianza tarda hasta diez días y el combustible hasta doce días, según el banco.\n\n'
        'Reclamar un cargo (una penalización, un aparcamiento, un peaje que no reconoce): puede reclamarlo con el formulario de centauro punto net, en el apartado "Atención al cliente y reclamaciones". Tú no puedes revisar cargos concretos. Si insiste en que alguien lo mire ahora, transfiere a GESTIÓN DE RESERVA con motivo_transferencia otro.\n\n'
        'Ha tenido que pagar algo durante el alquiler, como el aceite: que guarde el ticket y lo entregue al personal al devolver el coche; lo revisa el departamento de posventa para el reembolso.\n\n'
        'Un cobro en el banco que no aparece en su reserva, por ejemplo después de modificarla: el sistema reembolsa solo cualquier cobro que no corresponda a una reserva o prolongación confirmada; puede tardar hasta doce días naturales, según su banco.\n\n'
        'Multas: son responsabilidad del conductor. Centauro le identifica ante la autoridad y cobra cuarenta euros de gestión por cada multa, que se devuelven si la multa se anula. Tiene que esperar la notificación de la autoridad, que le dirá cómo pagarla.\n\n'
        'Facturas: la factura se emite cuando la oficina cierra el contrato; llega por correo y está en su área de cliente, en "Mis reservas y facturas". Para que salga a nombre de una empresa, debe pedirlo en el formulario "Atención al cliente y reclamaciones" de centauro punto net. Si reservó con un intermediario, la factura del alquiler se la da el intermediario.\n\n'
        'Contrato o facturas por correo: no se envían; se descargan en PDF desde su área de cliente, entrando con el correo que dio al recoger el coche. Si nunca ha entrado, primero crea la contraseña con "¿Has olvidado tu contraseña?".'
    ),
    'requisitos': (
        'Son preguntas que no son de prolongación, pero que puedes responder tú. Responde solo con lo que pone aquí, en una o dos frases por turno, y no añadas nada que no esté escrito. Si el cliente necesita después que alguien mire o cambie su reserva, transfiere a GESTIÓN DE RESERVA.\n\n'
        'Carnet: válido en la Unión Europea, con al menos un año de antigüedad. Edad mínima, diecinueve años; de diecinueve a veinticuatro años y desde los setenta y cinco se paga un suplemento. En España se acepta el carnet digital de la app oficial mi DGT.\n\n'
        'Documentos: DNI o pasaporte originales y el carnet; una foto no vale. Si hace antes el Centauro ID en la web, no tiene que enseñarlos en el mostrador, aunque se recomienda llevarlos.\n\n'
        'Carnet caducado: el carnet tiene que estar en vigor y ser válido en la Unión Europea, así que con un carnet caducado no se puede recoger el coche. Si dice que ya lo ha renovado o que tiene otro documento, ofrécele pasarle con un compañero (transfiere solo si acepta).\n\n'
        'Tarjeta para recoger el coche: física y a su nombre, Visa o Mastercard, de crédito o de débito. No valen tarjetas prepago, American Express, Maestro ni Diners. El titular de la tarjeta tiene que estar en la recogida.\n\n'
        'Billete de vuelta: es posible que se lo pidan. Si no lo tiene, se pide un depósito con tarjeta de crédito por el importe de la franquicia, sea cual sea el paquete.\n\n'
        'Pago en efectivo: el alquiler se puede pagar en efectivo en España y Portugal, no en Italia ni en Grecia. En ese caso hace falta, como garantía, un depósito con tarjeta de crédito, no de débito, por el importe de la franquicia del coche.\n\n'
        'Conductor adicional: todos los conductores tienen que figurar en el contrato. En España cuesta veintitrés euros un día, quince euros por día si son dos días y once euros por día de tres a doce días, con un máximo de ciento ocho euros. Con la reserva confirmada, basta con que el conductor adicional lleve su DNI y su carnet a la recogida. Si el alquiler ya está en curso, puede añadirlo pasando por la oficina de Centauro más cercana; el coste se aplica al total de días del alquiler.\n\n'
        '¿Puede recoger el coche otra persona?: no, solo el titular de la reserva. El conductor adicional sí puede devolverlo sin el titular.\n\n'
        'Cambiar el conductor principal con el alquiler en curso: no se puede. Sí puede añadir un conductor adicional en una oficina, pagando su coste.'
    ),
    'durante_el_alquiler': (
        'Son preguntas que no son de prolongación, pero que puedes responder tú. Responde solo con lo que pone aquí, en una o dos frases por turno, y no añadas nada que no esté escrito. Si el cliente necesita después que alguien mire o cambie su reserva, transfiere a GESTIÓN DE RESERVA.\n\n'
        'No es el coche que reservé: se garantiza el grupo, no la marca ni el modelo. Si no hay coche del grupo, le dan uno superior al mismo precio; en la oficina puede subir de categoría pagando la diferencia.\n\n'
        'Daños que no estaban anotados: los daños previos figuran en el contrato, en el apartado "Daños en salida". Si ve uno que no está, que le haga una foto antes de salir y se lo enseñe al personal. Además, avísenos y mande fotos por el formulario de la web. Las fotos tienen que ser las originales y mostrar la fecha y la hora, y es importante hacerlas antes de salir de las instalaciones de Centauro.\n\n'
        'Testigo de presión de los neumáticos: infle las ruedas en una gasolinera; si vuelve a encenderse, que nos llame de nuevo.\n\n'
        'Aviso de batería o pitidos: dale el teléfono de asistencia en carretera (ver TELÉFONOS QUE PUEDES DAR) y pregúntale si prefiere que le pases ahora con ASISTENCIA. Transfiere solo si dice que sí.\n\n'
        'Otro aviso en el coche (navegador, software, ruedas) o un ruido extraño: si es seguro y está cerca, que vaya a la oficina de Centauro más cercana para que le den soporte. Si no puede o prefiere hablar con alguien, dale el teléfono de asistencia en carretera y pregúntale si quiere que le pases ahora con ASISTENCIA. Transfiere solo si dice que sí.\n\n'
        'Aviso de aceite, se ha equivocado de combustible al repostar o se le ha caído la matrícula: tiene que llamar a asistencia en carretera. Dale el teléfono y pregúntale si quiere que le pases ahora con ASISTENCIA. Transfiere solo si dice que sí.\n\n'
        'El aire acondicionado no funciona: que vaya a la oficina de Centauro más cercana para que le den soporte.\n\n'
        'Conectar el móvil o CarPlay: no es un servicio garantizado, depende del coche asignado, y no tienes instrucciones para cada modelo.\n\n'
        'Cambiar el idioma de la app: en su perfil, en el apartado "Información personal".\n\n'
        'Kilómetros: ilimitados hasta veintinueve días. De treinta a sesenta días, cien kilómetros al día, y cada kilómetro de más cuesta veinticinco céntimos. Furgonetas de carga: cuatrocientos kilómetros al día, y treinta céntimos cada kilómetro de más.\n\n'
        'Coche de suscripción: incluye tres mil kilómetros al mes; cada kilómetro de más cuesta veinte céntimos. El conductor tiene que actualizar el kilometraje al final de cada mes desde su área de cliente.\n\n'
        'Alquiler por meses o de larga duración: hasta veintinueve días, kilómetros ilimitados; de treinta a sesenta días, cien kilómetros al día; y la suscripción, de tres meses a un año. El precio y la disponibilidad se ven en centauro punto net, simulando una reserva con las fechas y las oficinas.\n\n'
        'Salir de España: desde la península se puede ir solo a Portugal, Andorra y Francia, contratando antes la cobertura para salir de España. Cuesta treinta y dos euros un día, dieciocho euros con cincuenta por día si son dos días y catorce euros por día de tres a doce días, con un máximo de ciento sesenta y ocho euros. Ir sin esa cobertura puede suponer un cargo de cien a doscientos cincuenta euros, según la temporada, y no se puede llevar el coche en ferry. Si la reserva aún no ha empezado, puede añadir la cobertura desde su área de cliente, en su reserva, con "Modificar servicios", o pedirla en el mostrador al recoger el coche.\n\n'
        'Coberturas: Centauro tiene una sola cobertura, Smart Cover, a todo riesgo y sin franquicia, incluida en el paquete Premium: no se bloquea la franquicia en su tarjeta y, si hay daños, no se le cobra por ese concepto. El detalle está en los apartados tres y cuatro de los términos y condiciones de centauro punto net.\n\n'
        'Seguro de responsabilidad civil: todos los coches tienen el seguro obligatorio, que cubre los daños a terceros; en España, Portugal y Grecia cubre también, con límites, los daños personales del conductor. El detalle está en los términos y condiciones de centauro punto net.\n\n'
        'Zona de bajas emisiones: no tienes esa información. Comprobar por dónde puede circular es responsabilidad del cliente: cuando sepa la matrícula del coche, que lo consulte con el ayuntamiento. Las multas y sanciones son del conductor.\n\n'
        'Limpieza: el coche debe devolverse tan limpio como se entregó. Solo se cobra limpieza, hasta cien euros, si la suciedad es mayor que la de un uso normal. No se puede fumar dentro.\n\n'
        'Mascotas: puede llevar a su perro si va sujeto de forma segura y según la normativa. Si al devolverlo hace falta una limpieza especial, puede haber un coste.'
    ),
    'otras': (
        'Son preguntas que no son de prolongación, pero que puedes responder tú. Responde solo con lo que pone aquí, en una o dos frases por turno, y no añadas nada que no esté escrito. Si el cliente necesita después que alguien mire o cambie su reserva, transfiere a GESTIÓN DE RESERVA.\n\n'
        'Sillas para niños: sí, bajo petición, quince euros al día con un máximo de ciento veinte euros. Son obligatorias hasta los doce años o los ciento treinta y cinco centímetros. Hay sillas para bebés, de cero a trece kilos; para niños, de nueve a veinticinco kilos; y elevadores, de dieciséis a treinta y seis kilos. La instalación la hace el cliente.\n\n'
        'Cadenas de nieve: solo en las oficinas de Barcelona y Madrid. Cuestan veintiún euros un día, once euros por día si son dos días y ocho euros por día de tres a doce días, con un máximo de noventa euros.\n\n'
        'Accesorios o adaptaciones: no se puede modificar el coche ni usar accesorios que Centauro no haya autorizado; hace falta autorización previa. Si su carnet le obliga a llevar adaptaciones, transfiere a GESTIÓN DE RESERVA con motivo_transferencia otro.\n\n'
        'Que le lleven el coche: solo se ofrece en las oficinas de Benidorm y Torrevieja. Para comprobar la disponibilidad tiene que contactar con esa oficina en su horario (ver TELÉFONOS QUE PUEDES DAR).\n\n'
        'Teléfono de la oficina de recogida o hablar con una oficina: no hay un teléfono directo de las oficinas; dile que te cuente su consulta y le ayudas en esta misma llamada. Si insiste en contactar con una oficina o con una persona, o dice que no quiere usar la web ni la app, NO le vuelvas a explicar la web ni la app: en ese mismo turno ofrécele pasarle con un compañero ("¿Quiere que le pase con un compañero?"). Si acepta o insiste, transfiere a GESTIÓN DE RESERVA con motivo_transferencia otro.\n\n'
        'Se ha dejado algo en el coche: transfiere a GESTIÓN DE RESERVA con motivo_transferencia otro; un compañero toma los datos y avisa a la oficina.\n\n'
        'La grúa municipal se ha llevado el coche: dale el teléfono de asistencia en carretera (ver TELÉFONOS QUE PUEDES DAR) y pregúntale si quiere que le pases con ASISTENCIA. Transfiere solo si dice que sí, con motivo_transferencia asistencia.\n\n'
        'Minibús y silla de ruedas: el minibús de cortesía no está adaptado para personas con movilidad reducida.\n\n'
        '¿Habla con una persona o con un robot?: "Está hablando con un agente de IA; cuénteme su consulta."\n\n'
        'Tiene un alquiler con otra empresa o a través de una agencia: las dudas de las condiciones que contrató, con la empresa con la que reservó. Desde aquí puede ayudarle con la política de combustible, los servicios adicionales, cómo recoger y devolver el coche y la asistencia en carretera.\n\n'
        'Una autoridad (policía, guardia civil, una administración) pide datos de un cliente o de un coche: que lo pida por escrito al departamento de flotas, en el correo "judicial arroba centauro punto net". Si es urgente, puede llamar al "más treinta y cuatro, nueve seis seis, ocho tres cero, uno cinco cero".\n\n'
        'Consultas que no tienen nada que ver con Centauro: "Lo siento, solo puedo ayudarle con su alquiler de Centauro."'
    ),
    'telefonos': (
        'Son preguntas que no son de prolongación, pero que puedes responder tú. Responde solo con lo que pone aquí, en una o dos frases por turno, y no añadas nada que no esté escrito. Si el cliente necesita después que alguien mire o cambie su reserva, transfiere a GESTIÓN DE RESERVA.\n\n'
        'Cuando des un teléfono o un correo, dilo despacio y repítelo una vez.\n\n'
        'Asistencia en carretera en España, veinticuatro horas, para averías o accidentes: "más treinta y cuatro, nueve seis seis, tres seis cinco, tres seis cinco".\n\n'
        'Asistencia en carretera de otros países: no tienes esos teléfonos. Si el alquiler es en otro país, dile que no tienes ese número y remítele a centauro punto net; no le digas que el de España sirve allí.\n\n'
        'Reservas nuevas: "más treinta y cuatro, nueve seis seis, tres seis cero, tres seis cero", opción uno. Dalo solo si el cliente pide un número para reservar; si quiere reservar ahora, transfiere a NUEVA RESERVA.\n\n'
        'Reservas nuevas en otros países, opción "Nuevas reservas": Portugal, "más tres cinco uno, tres cero ocho, ocho uno cero, siete siete siete"; Italia, "más tres nueve, cero seis, ocho tres seis seis, dos nueve cinco nueve"; Grecia, "más tres cero, dos uno uno, uno nueve ocho, cinco tres uno cero".\n\n'
        'Oficina de Benidorm, solo para el servicio de entrega: "más treinta y cuatro, nueve seis, seis ocho tres, cero siete, cero siete", de lunes a viernes de ocho de la mañana a siete de la tarde y los sábados de nueve a dos.\n\n'
        'Oficina de Torrevieja, solo para el servicio de entrega: "más treinta y cuatro, nueve seis, seis siete cero, tres cinco, tres cuatro", de lunes a viernes de ocho a dos y de cuatro a siete de la tarde, y los sábados de nueve a dos.'
    ),
}


def buscar(input_data):
    """Sección del tema pedido; si el tema no existe, la de «otras» con encontrado False."""
    tema = str(input_data.get("tema") or "").strip().lower()
    if tema in SECCIONES:
        return {"tema": tema, "texto": SECCIONES[tema], "encontrado": True}
    return {"tema": "otras", "texto": SECCIONES["otras"], "encontrado": False}


try:
    _entrada = input_data  # noqa: F821 (lo inyecta el nodo Python de HappyRobot)
except NameError:  # importado desde las pruebas locales
    _entrada = None
if _entrada is not None:
    output = buscar(_entrada)
```
