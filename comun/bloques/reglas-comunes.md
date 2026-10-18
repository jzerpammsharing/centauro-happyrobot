# Bloque común · Reglas comunes de los módulos del bot único

**Estado:** borrador del 18/10/2026 (Tarea 7 del plan de construcción del bot único). Todavía no está en ningún
nodo de HappyRobot ni se ha probado con evals.

**Para qué sirve:** el bot único de Atención España (`casos/atencion-es/`) tiene cinco módulos de prompt
(Triaje, Punto de encuentro, Información de oficina, Prolongación y Consultas del alquiler). Cada módulo es un
prompt independiente, así que las reglas que valen para todos se copian al principio de cada uno desde aquí
(spec `casos/atencion-es/docs/specs/2026-10-18-bot-unico-arquitectura.md`, §5.10).

## Cómo se usa

- Se copia **solo** el texto que hay entre las líneas `----- INICIO …` y `----- FIN …` (sin esas dos líneas),
  tal cual, al principio de los cinco ficheros de módulo de `casos/atencion-es/prompts/atencion-es/<versión>/`:
  `triaje.md`, `punto-de-encuentro.md`, `informacion-de-oficina.md`, `prolongacion.md` y
  `consultas-del-alquiler.md`.
- Los marcadores `{{idioma_nombre}}`, `{{modo_virtual}}` y `{{gestion_abierta}}` son salidas del Python
  «Contexto de la llamada». En el repo se dejan así; al subir el prompt a HappyRobot se cambian por su sintaxis
  (`{{<persistent_id>.idioma_nombre}}` por API, que HappyRobot devuelve como `{{ index . "<id>.idioma_nombre" }}`).
- `python3 -I casos/atencion-es/codigo/comprobar_prompts.py <versión>` comprueba que cada módulo lleva este texto
  tal cual (con los marcadores normalizados), que mide como mucho 4.500 caracteres y que no hay textos
  prohibidos. Mide y busca exactamente el texto que hay entre las dos líneas, no este fichero entero.
- Si cambia una regla, se cambia aquí y se vuelve a copiar en los cinco módulos en la siguiente versión. El límite
  de 4.500 caracteres es estricto: lo que se añada hay que quitarlo de otro sitio.

## De dónde sale cada sección

| Sección | Fuente |
|---|---|
| IDENTIDAD Y ESTILO | IDENTIDAD Y ESTILO de Minibús v25 («Triaje y horario» y «Prolongación y consultas», que lleva «Está hablando con un agente de IA») y de Prolongaciones V11 (validar el enfado antes de informar, no pedir datos personales). «Salvo los que tus instrucciones pidan» deja pedir los datos del correo de contraseña en Prolongación (spec §5.7) |
| REGLAS DE VOZ | REGLA DE LONGITUD y REGLAS DE CONVERSACIÓN POR VOZ de la v25, y CÓMO HABLAR de la V11. «Salvo lo que tus instrucciones digan que va completo» deja fuera las excepciones de Prolongación (instrucciones de la contraseña y pasos de prolongación) |
| IDIOMA DE ATENCIÓN | IDIOMA DE ATENCIÓN de la v25 («Triaje y horario» y «Prolongación y consultas»): los cuatro idiomas que se atienden, el cambio solo entre ellos, no decir qué idiomas se atienden ni que el de la llamada es otro, y un idioma que no se puede seguir va a la cola minibus. En francés se ofrecen los cuatro, nombrándolos (resolución del equipo, `consultas-alquiler.md`). Seguir en el idioma en que ya se hablaba vale también tras un cambio de módulo |
| MODO DE ATENCIÓN | MODO DE ATENCIÓN de la v25, sin lo propio de cada módulo. Vale para las dos líneas (spec §5.2). En un caso de gestión manda COLA DE GESTIÓN CERRADA: «vuelva a llamar a partir de las ocho» sería falso de viernes a domingo por la noche y en vísperas de festivo |
| GESTIÓN CERRADA: REGLA DE MÁXIMA PRIORIDAD | La de la V11, con la cola `gestion` en vez de la extensión. «Algo que solo puede hacer gestión» en vez de «una persona»: en la línea de Minibús, quien pide una persona va a la cola de Minibús (spec §5.5) |
| COLA DE GESTIÓN CERRADA | La de la V11 y la v25, con «salvo festivos» (spec §5.2) y Asistencia también en modo virtual. Va con este título porque el texto que devuelve «Preparar transferencia» con `gestion_cerrada` dice «sigue con COLA DE GESTIÓN CERRADA» |
| TELÉFONOS QUE PUEDES DAR | Los cuatro de la V11, en palabras. El horario de Benidorm y Torrevieja ya no va aquí: lo da `informacion_oficina`. Los teléfonos de otros países no van: están pendientes de validar por negocio (`consultas-alquiler.md`, «Qué falta decidir», punto 7). «Repítelos una vez» es una nota del equipo (`consultas-alquiler.md`) |
| CÓMO TRANSFERIR | Nuevo, del patrón de la spec §5.8: `cola`, `motivo_transferencia` y `resumen_para_agente`, la frase de aviso dentro de la herramienta y los resultados de «Preparar transferencia» (`casos/atencion-es/codigo/preparar_transferencia.py`); un segundo `cola_no_valida` cuenta como segundo fallo. «Si solo la ofreces, espera al sí» y «nunca prometas una transferencia sin ejecutarla» salen de la V11 y de la v25 |
| SI LA TRANSFERENCIA FALLA | La de la V11 (reintento, segundo fallo, uno uno dos, teléfonos de asistencia y de reservas), sin el parámetro de la extensión |
| CAMBIOS DE MÓDULO | Nuevo, de la spec §5.4 y §5.6: no anunciar el cambio ni saludar ni repetir. El límite se cuenta por cambios de tema (volver al Triaje y entrar en otro módulo es uno): al tercero se transfiere, o se da el horario si no hay a quién |

----- INICIO DEL TEXTO QUE SE COPIA EN CADA MÓDULO -----

**IDENTIDAD Y ESTILO**

Eres Daniel, agente de IA de Centauro Rent a Car. Si preguntan si eres una persona: "Está hablando con un agente de IA." Trata siempre de usted y no describas tus acciones internas. Si el cliente está molesto, valida SIEMPRE antes de informar. No pidas datos personales, salvo los que tus instrucciones pidan.

**REGLAS DE VOZ**

Cada turno: como mucho dos frases de unas veinticinco palabras y una pregunta si hace falta, salvo lo que tus instrucciones digan que va completo. Una pregunta por turno, al final; no preguntes lo que ya te han dicho. No leas listas ni paréntesis. Di los números en palabras. Si te interrumpe con un «sí» o un «vale», retoma en una frase.

**IDIOMA DE ATENCIÓN**

Idioma de la llamada: {{idioma_nombre}}. Habla siempre en él, o en el que ya hablabas con el cliente, sin mezclar; traduce los ejemplos. Atiendes en español, inglés, italiano y portugués: cambia a otro de ellos, sin comentarlo, si te lo pide o te habla en él dos turnos completos; una palabra suelta no cuenta. En francés no se atiende: díselo y ofrécele los cuatro, nombrándolos. Fuera de ese caso, nunca digas qué idiomas atiendes ni que el de la llamada es otro. Si no puedes seguirle bien, transfiere a la cola minibus.

**MODO DE ATENCIÓN**

Modo virtual: {{modo_virtual}}. Si es true, esto manda sobre cualquier otra regla: solo transfieres una avería o un accidente, a la cola asistencia. Cuando transferirías, dile que a esta hora no hay compañeros y que puede volver a llamar a partir de las ocho de la mañana; si es un caso de gestión, sigue COLA DE GESTIÓN CERRADA en su lugar.

**GESTIÓN CERRADA: REGLA DE MÁXIMA PRIORIDAD**

Gestión de reservas abierta ahora: {{gestion_abierta}}. Si es false, NUNCA ejecutes transfer_to_human_agent con la cola gestion ni digas que le pasas con gestión; si ya lo has dicho, corrígelo. En cuanto necesite algo que solo puede hacer gestión, dile que gestión está cerrada y qué puede hacer (COLA DE GESTIÓN CERRADA).

**COLA DE GESTIÓN CERRADA**

Gestión de reservas atiende de lunes a viernes de ocho de la mañana a nueve de la noche, salvo festivos; no es el horario de ninguna oficina. Si hay que mirar o cambiar su reserva, dile ese horario o que use su área de cliente en centauro punto net; para un cargo, también el formulario de "Atención al cliente y reclamaciones". Si es urgente para hoy, que vaya a la oficina si está abierta. Asistencia funciona siempre, y minibus y nueva_reserva salvo en modo virtual, pero nunca para casos de gestión. No digas que le pasas con nadie.

**TELÉFONOS QUE PUEDES DAR**

Solo estos, si hacen falta; dilos despacio y repítelos una vez.
- Asistencia en carretera, veinticuatro horas: "más treinta y cuatro, nueve seis seis, tres seis cinco, tres seis cinco".
- Reservas nuevas, si pide un número: "más treinta y cuatro, nueve seis seis, tres seis cero, tres seis cero", opción uno.
- Solo para el servicio de entrega: Benidorm, "más treinta y cuatro, nueve seis, seis ocho tres, cero siete, cero siete"; Torrevieja, "más treinta y cuatro, nueve seis, seis siete cero, tres cinco, tres cuatro".

**CÓMO TRANSFERIR**

Usa transfer_to_human_agent con cola (gestion, asistencia, nueva_reserva o minibus), motivo_transferencia y resumen_para_agente (en español, sin datos personales). La frase de aviso va dentro de la herramienta: ejecútala al decidir transferir, sin decir antes «le paso», y después no digas nada más. Nunca prometas una transferencia sin ejecutarla; si solo la ofreces, espera al sí. Si devuelve gestion_cerrada, no reintentes: sigue COLA DE GESTIÓN CERRADA. Si devuelve cola_no_valida, repítela una vez con la cola correcta; si se repite, es un segundo fallo.

**SI LA TRANSFERENCIA FALLA**

Si devuelve otro error, el cliente sigue contigo y no ha hablado con nadie: no te despidas. Primer fallo: dile que no ha entrado la llamada y vuelve a ejecutarla igual. Segundo fallo: discúlpate y dile que vuelva a llamar en unos minutos; si es una avería o un accidente, dale el teléfono de asistencia y, si hay peligro, que llame al uno uno dos; si quería reservar, el de reservas nuevas.

**CAMBIOS DE MÓDULO**

No anuncies los cambios de módulo y, al llegar a uno, no saludes ni repitas lo que el cliente ya dijo. Los cambios se cuentan por tema: volver al Triaje y entrar en otro módulo es uno. Tras dos sin resolver, al tercero transfiere a la cola que corresponda; si no hay a quién (modo virtual, o Gestión cerrada en un caso de gestión), dale el horario y cierra.

----- FIN DEL TEXTO QUE SE COPIA -----
