# Guion de las 25 llamadas de prueba (Tarea 17, puerta 0 de §8.4)

Workflow «Centauro Atención España», v2 (`x8xd0llbdp3j`) publicada en *development*. Las llamadas las hace una persona;
el agente analiza los runs después. Spec: §8.4, §11.2 a §11.5 y §11.8 (`docs/specs/2026-10-18-bot-unico-arquitectura.md`).

## Antes de empezar (lo prepara la persona)

1. Publicar la v2 en *development* y decidir `require_webcall_auth` (por defecto es `true`; una prueba web necesita
   `false`: pendientes, Tarea 6).
2. **Llamada web:** `from_number` = `to_number` = `web`. Sin línea, el código da Minibús en español (`origen_opcion`
   `por_defecto`) y `telefono_dictado` «número oculto». Por eso la variable `OPCION_PRUEBA` (en *development*):
   - `minibus` (o `ninguna`): las llamadas de Minibús;
   - `prolongacion`: las de Prolongación.
   Cambiarla entre llamadas cuando el guion lo pida y anotarlo. Valores: `ninguna`, `minibus`, `prolongacion`.
3. **Las transferencias son reales:** suenan en las colas de producción (`gestion` 18057, `asistencia` 18034,
   `nueva_reserva` 18001, `minibus` 18056). Avisar antes a quien atienda esas colas («llamadas de prueba del asistente»).
   Llamadas con transferencia esperada: 2, 16, 21 y 22. Si no se puede avisar, colgar al oír el mensaje de transferencia
   (se pierde la comprobación del whisper de la 22).
4. **Datos inventados, siempre los mismos:** nombre «Prueba Prueba», nacimiento 03/03/1990, correo
   `prueba.prueba@example.com`, reserva `ER00000000`. No usar nunca datos reales: «Centauro MCP» va contra la API real.
5. **Horarios (hora peninsular, UTC+2 hasta el 25/10/2026, UTC+1 después):** Gestión abierta de lunes a viernes de 8:00 a
   21:00, salvo festivos nacionales; modo virtual de 22:00 a 8:00. Las llamadas 1 a 16 y 21 a 25 van en laborable de 8:00
   a 20:30. La 17 en sábado, domingo o festivo; la 18 cruzando las 21:00 un laborable; la 19 y la 20 de 22:00 a 8:00.
6. **Por cada llamada, anotar:** run_id (solo el id, nunca el teléfono), `OPCION_PRUEBA`, hora, resultado
   (correcto / fallo / fallo crítico), qué falló y créditos (`scripts/creditos_runs.py`, con `HAPPYROBOT_API_KEY`).

## Qué se mira en todas (en el run, no solo de oído)

- Solo cuentan los fallos vistos en turnos `assistant` de la transcripción (el extract de IA no es fiable, CLAUDE.md §4).
- Nunca sale a 2114, 2115 o 2119. La cola es la de la tabla de colas, no una extensión inventada.
- Créditos por llamada de prolongación ≤ 80 (puerta 0, punto 4).
- `saltos` del extract = suma de los `callCount` de los 12 Module Change (D-010).
- Fallo crítico: dato inventado que perjudique al cliente, correo enviado sin coincidir, cliente dejado en la locución de
  Gestión, transferencia ejecutada con Gestión cerrada.

## Llamadas 1 a 4 · Prolongación (`OPCION_PRUEBA` = `prolongacion`, laborable de 8:00 a 20:30)

| # | Qué hace el que llama | Esperado | Comprobar en el run |
|---|---|---|---|
| 1 | Quiere prolongar el alquiler en curso. Cuando le preguntan por su cuenta, dice que sí entra. | Explica los pasos de la web sin precio ni garantías; no transfiere. | Sin saltos: `callCount` de los 12 Module Change vacío o 0 y el extract sin error (`callCount` vacío). Créditos ≤ 80. |
| 2 | Prolongar, sin cuenta ni contraseña. Acepta el correo. Da `prueba.prueba@example.com`, «Prueba Prueba», 03/03/1990, y confirma el deletreo. | Ejecuta `enviar_correo_contrasena`: el MCP no encuentra nada y sale `no_coincide`. Dice «con esos datos no me coincide», sin decir qué dato falla, y transfiere a `gestion` con `correo_no_coincide`. **Ningún correo sale** (no puede salir con datos inventados). | Resultado de la herramienta; una pata a 18057 en RingCentral; whisper con el resumen y «número oculto» (ver §whisper). |
| 3 | Prolongar, sin cuenta. Rechaza el correo. | Plan B completo y solo («Mi cuenta», «¿Has olvidado tu contraseña?»), sin los pasos en ese turno; luego pregunta si seguimos. | No llama a `enviar_correo_contrasena`. |
| 4 | Prolongar; no sabe con qué correo está su alquiler. Da `ER00000000`, «Prueba Prueba» y 03/03/1990, un dato por turno. | `pista_correo` da `no_verificado`; no dice qué dato falla; ofrece repetir una vez o el plan B. No dice dominio alguno. | Máximo 2 ejecuciones de `pista_correo`. Pista: el caso `verificado` no se puede ver con datos inventados. |

**Hueco para la persona (Paso 3 de la Tarea 17), no se hace con datos inventados.** Caso «coincide» y pista del dominio
`verificado`, con una reserva real en curso y un correo que alguien del equipo pueda abrir. Anotar aquí solo el resultado,
sin datos de la reserva ni del correo:

| # | Caso | Esperado | Resultado (rellena la persona) |
|---|---|---|---|
| H1 | Pista del dominio: `pista_correo` con los datos de la reserva real | `verificado`; el bot dice solo «es una dirección de <dominio>» y pide el correo | _pendiente_ |
| H2 | `enviar_correo_contrasena` con el correo correcto | `enviado`; llega el correo; qué trae el correo (confirmar) | _pendiente_ |
| H3 | Correo del cliente distinto del del alquiler | `no_coincide`, sin correo | _pendiente_ |

## Llamadas 5 a 16 · Un salto por llamada, ida y vuelta

Tabla de `prompts/atencion-es/v2/saltos.md` (filas 1 a 8 nuevas, a a d heredadas de la v25). Cada llamada hace el salto
(ida) y vuelve al módulo de origen (vuelta) por el camino que dice la tabla. Texto de ejemplo del cliente entre comillas.

**En cada salto comprobar** (pendientes, «Que un Module Change pueda volver al Triaje» y «Que el módulo de destino ve
el historial»):
- el salto ocurre de verdad (herramienta ejecutada, Module Change `called` true, `callCount` +1);
- el destino **no saluda, no se presenta ni repite** lo que el cliente ya dijo; contesta a lo último que se pidió;
- si se hablaba en inglés (solo en la llamada 7), el destino sigue en inglés;
- qué historial recibe el módulo en una llamada real (mirar el primer turno del destino en la transcripción);
- el bot no dice «le paso con…» ni anuncia el cambio.

| # | Fila | `OPCION_PRUEBA` | Origen → destino (ida) | Vuelta | Cliente |
|---|---|---|---|---|---|
| 5 | 1 `volver_al_triaje` | `minibus` | Punto de encuentro → Triaje | Triaje → Punto de encuentro (pide otra vez el minibús de Valencia) | Pide el punto de encuentro de un aeropuerto; luego: «tengo otra consulta distinta» y, al encaminarle el Triaje, «quiero saber el horario de la oficina de Atocha». Vuelve: «perdona, vuelvo al minibús». **Además:** web = `whatsapp_disponible` false: el bot no debe ofrecer el WhatsApp del punto de encuentro. |
| 6 | 2 `volver_al_triaje` | `minibus` | Información de oficina → Triaje | Triaje → Información de oficina | Pregunta el horario de Madrid; luego «tengo otra consulta distinta»; luego vuelve a preguntar por una oficina. |
| 7 | 3 `volver_al_triaje` | `prolongacion` | Prolongación → Triaje | Triaje → Prolongación | **En inglés:** «I want to extend my rental»; luego «I have another question» (sin decir cuál: el Triaje pregunta); luego «actually, back to extending». El Triaje y el destino siguen en inglés. |
| 8 | 4 `volver_al_triaje` | `minibus` | Consultas del alquiler → Triaje | Triaje → Consultas | Duda del alquiler (por ejemplo, requisitos del conductor); luego «tengo otra consulta distinta»; luego otra duda del alquiler. |
| 9 | 5 `informacion_oficina` | `minibus` | Punto de encuentro → Información de oficina | Información de oficina → Punto de encuentro (fila 6) | Minibús de un aeropuerto; luego «¿y el horario de la oficina de Málaga estación?»; luego «¿y el minibús de Sevilla aeropuerto?». |
| 10 | 6 `buscar_punto_de_encuentro` | `minibus` | Información de oficina → Punto de encuentro | Punto de encuentro → Información de oficina (fila 5) | Horario de una oficina; luego «¿dónde cojo el minibús en Bilbao?»; luego «¿y cómo llego a la oficina de Madrid?». |
| 11 | 7 `prolongar_alquiler` | `minibus` | Consultas del alquiler → Prolongación | Prolongación → Triaje (fila 3) → Consultas | Duda del alquiler; luego «quiero prolongar mi alquiler»; luego «y otra duda: ¿qué se cobra por devolver tarde?» (vuelta). |
| 12 | 8 `informacion_oficina` | `prolongacion` | Prolongación → Información de oficina | Información de oficina → Triaje (fila 2) → Prolongación | Quiere prolongar; luego «¿hasta qué hora está abierta la oficina de Atocha?»; luego «vuelvo a lo de prolongar». |
| 13 | a `consultas_alquiler` | `minibus` | Punto de encuentro → Consultas | Consultas → Punto de encuentro (fila c) | Minibús; luego «¿qué cargos pueden hacerme al devolver?»; luego «volviendo al minibús…». |
| 14 | b `consultas_alquiler` | `minibus` | Información de oficina → Consultas | Consultas → Información de oficina (fila d) | Horario de una oficina; luego «¿qué documentos necesito?»; luego otra pregunta de oficina. |
| 15 | c `buscar_punto_de_encuentro` | `minibus` | Consultas → Punto de encuentro | Punto de encuentro → Consultas (fila a) | Duda del alquiler; luego «¿dónde está el minibús en Málaga?»; luego otra duda del alquiler. |
| 16 | d `informacion_oficina` | `minibus` | Consultas → Información de oficina | Información de oficina → Consultas (fila b) | Duda del alquiler; luego «¿cuál es el horario de la oficina de Valencia?»; luego otra duda del alquiler. **Extra (SALTO-PING):** a continuación, un tercer cambio de tema («ahora quiero el minibús del aeropuerto»): al tercer salto se transfiere a `minibus` (18056) en horario; ver «Extra» de `saltos.md`. Ésta es la 4.ª llamada con transferencia. |

Anotar también en qué turno decidió el modelo
el salto y con qué `motivo`/`tema`/`aeropuerto`/`situacion`, y que no mande datos personales en `motivo`.

## Llamadas 17 a 20 · Gestión cerrada y modo virtual

| # | Condición | `OPCION_PRUEBA` | Qué hace el que llama | Esperado | Comprobar |
|---|---|---|---|---|---|
| 17 | **Sábado, domingo o festivo nacional** a media mañana (Gestión cerrada, no es modo virtual) | `prolongacion` | Prolongar; luego «quiero hablar con una persona de mi reserva». | «Preparar transferencia» da `gestion_cerrada`; el bot **no transfiere**, da el horario de Gestión y el plan B; **sigue hablando**. | Corte de la cadena: el agente recibe `resultado: gestion_cerrada` (nodo «¿Transferir?» rama «Fallback»); **ninguna pata nueva** en RingCentral hacia 18057 ni 18061; el cliente no se queda en silencio ni en una locución. Pendientes: «Cómo cortar la cadena de la transferencia sin transferir con Gestión cerrada». |
| 18 | **Laborable cruzando las 21:00**: empezar a las 20:55 y pedir la persona a las 21:02 | `prolongacion` | Hablar de la prolongación sin pedir persona hasta pasadas las 21:00; entonces «necesito hablar con alguien». | No se transfiere: «Preparar transferencia» calcula la hora al ejecutarse, no se fía de `gestion_abierta` del principio (caso `21:02 con gestion_abierta true`). | `gestion_abierta` de «Contexto de la llamada» true y `resultado: gestion_cerrada` en la transferencia. Ninguna pata a 18057. |
| 19 | **22:00 a 8:00** (modo virtual) | `minibus` | «Mi minibús no llega, quiero hablar con alguien.» | `modo_virtual`: no transfiere a `minibus` ni a `nueva_reserva`; dice que a esta hora no hay compañeros y que vuelva a llamar a partir de las 8:00. | Sin patas a 18056 ni 18001. Ver §11.8 (informe): de noche esas colas solo reproducen un anuncio. |
| 20 | **22:00 a 8:00** (modo virtual) | `prolongacion` | Prolongar; luego pide una persona de su reserva. | El modo virtual se avisa **solo cuando pide una persona** (no en el saludo); no transfiere a Gestión (cerrada); da el horario. | El saludo no menciona el modo virtual; `gestion_cerrada` o `modo_virtual` (en la noche, gana `gestion_cerrada`). Sin patas. |

## Llamadas 21 a 25 · Avería, reserva nueva e idiomas

| # | Condición | `OPCION_PRUEBA` | Qué hace el que llama | Esperado | Comprobar |
|---|---|---|---|---|---|
| 21 | Laborable de día (también valdría de noche: Asistencia atiende siempre) | `minibus` | «Se me ha averiado el coche» (o accidente). | Triaje → transfiere a la cola `asistencia` (18034), `motivo_transferencia` `asistencia`; el modo virtual no la bloquea. | Pata a 18034 (no a 2114 ni 2115). Whisper. |
| 22 | Laborable de día | `minibus` | «Quiero hacer una reserva nueva.» | Triaje → `nueva_reserva` (18001), motivo `nueva_reserva` (SALTO-ENTRADA-TR). Una persona del equipo coge la llamada. | **Whisper (§11.5, Tarea 17):** sonó con el resumen y el teléfono; con la persona que pulsa 1, el bot queda **callado** mientras habla con el agente y no vuelve a hablar tras conectar; repetir sin pulsar 1 (`whisper_transfer_no_bridge`) y anotar qué hace el bot. Anotar la duración del run y la de la pata en RingCentral. |
| 23 | Laborable de día | `prolongacion` | Habla en **inglés** desde el primer turno: «I want to extend my rental», y sigue en inglés todo el rato. | Todo en inglés (también tras un salto, ver llamada 7). Sin mezcla. | Nota: con web el idioma de partida es `es`; el inglés se prueba cambiando de idioma hablando (dos turnos completos). La línea en inglés real (`<LINEA_PROLONGACION_EN>`) se prueba en el ensayo de la Tarea 18. |
| 24 | Laborable de día | `minibus` | Habla en **italiano**: «Buongiorno, vorrei sapere dove prendere il minibus all'aeroporto». | Cambia a italiano sin comentarlo tras dos turnos completos (el prompt atiende español, inglés, italiano y portugués); no cambia por una palabra suelta. | El bot contesta en italiano, el saludo y el aviso legal siguen en el idioma de la llamada. |
| 25 | Laborable de día | `minibus` | Habla en **francés**: «Bonjour, je voudrais savoir où prendre la navette». | En francés no se atiende: se lo dice y le ofrece los cuatro idiomas nombrándolos (español, inglés, italiano y portugués). No dice qué otros idiomas «hay» fuera de este caso. | No transfiere salvo que no pueda seguirle (entonces cola `minibus`, motivo `otro`). |

## Resumen de cobertura

| Comprobación (spec §8.4 punto 2 y pendientes) | Llamadas |
|---|---|
| Prolongar con y sin cuenta | 1, 2, 3 |
| Correo: enviado | H2 (hueco, reserva real) |
| Correo: no coincide | 2 |
| Pista del dominio | 4 (no verificado), H1 (verificado, hueco) |
| Saltos de la tabla de 12, ida y vuelta | 5 a 16 |
| Salto real y qué recibe el módulo de destino | 5 a 16 |
| Triaje sin saludar tras `volver_al_triaje`; inglés tras salto | 5 a 8, 7 |
| Tercer salto transfiere (SALTO-PING) | 16 |
| Gestión cerrada, no transfiere y el bot sigue | 17, 18 |
| Modo virtual | 19, 20 |
| Avería | 21 |
| Reserva nueva | 22 |
| Whisper y bot callado tras transferir | 2, 21, 22 (sobre todo la 22) |
| `callCount` vacío | 1, 3, 4 (sin saltos) |
| WhatsApp con `whatsapp_disponible` false | 5 (web) |
| `require_webcall_auth` | Antes de empezar (punto 1) |
| Inglés, italiano, francés | 23, 24, 25 (y 7) |
| Créditos de prolongación ≤ 80 | 1 a 4, 7, 12, 17, 18, 20 (`creditos_runs.py`) |

## Registro de resultados (rellena la persona; el agente lo analiza)

| # | run_id | OPCION_PRUEBA | Hora (Madrid) | Resultado | Fallos | Créditos |
|---|---|---|---|---|---|---|
| 1 a 25 | _pendiente_ | | | | | |
