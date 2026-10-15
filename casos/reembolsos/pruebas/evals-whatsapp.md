# Evals automáticos de la conversación por WhatsApp (T4)

> Fecha anonimizada en esta copia (fila 4a3): el eval en HappyRobot usa otra fecha de prueba.
>
> Última ronda: **ronda 2** (10/10 PASS), al final de este fichero. La tabla de arriba es la ronda 1.

Evals personalizados de HappyRobot sobre el nodo de prompt «Reembolsos» (W1 v2, `v2 · v1 + oferta de WhatsApp y lectura de señales`).

- Nodo: `01a12efe-08c3-7d1b-ab66-e951341c25e5`
- Versión probada: `01a12efe-08b0-74e8-acba-f27b76f791eb`
- Variable `whatsapp_posible` = true en todos salvo 4f (false). Datos ficticios: `ER00000000` / `Prueba Prueba`.
- Fecha de la ejecución: 12/10/2026.

## Resultados

| Eval | eval_id | Conversación | Expectativa | Resultado | Run | Motivo del juez |
|---|---|---|---|---|---|---|
| WA · 4a1 oferta inicial | `01a12f07-1062-7583-ac20-d778821f6be6` | Saludo + «no me ha llegado la devolución de la fianza» | Mira la reserva y ofrece WhatsApp; sin herramienta; una pregunta | PASS | `6067fb24-cbe6-4819-b0aa-8056e8ad1efc` | Indica que revisará la reserva y ofrece el WhatsApp con una sola pregunta, sin herramientas. |
| WA · 4a2 acepta → envía | `01a12f08-6122-7cc6-8533-95ff370e405d` | Oferta + «Sí, mándemelo» | `enviar_whatsapp {idioma:"es"}` | PASS | `2bb83cec-fe8f-4532-93f0-3683e4aaa28a` | Solo ejecuta enviar_whatsapp con idioma es. |
| WA · 4a3 señal con fecha ya dada | `01a12f08-6619-710b-9703-38be8649ce54` | Oferta, envío (con tool call), fecha dada, luego señal | `consultar_reembolso` con ER00000000, Prueba Prueba, 03/03/1990; sin leer datos | FAIL | `78780a73-945e-41a5-8a3e-c50691ba1d70` | Consulta bien, pero dice «Un momento…» y repite nombre y fecha en vez de «Me ha llegado, gracias». |
| WA · 4b rechaza | `01a12f07-fd1a-7cba-bce3-23fda28f45e9` | Oferta + «No, prefiero decírselo yo» | Pide el número de reserva; sin enviar_whatsapp | PASS | `d386381e-2f8c-4492-ae91-2d5d4c681c94` | No envía y pregunta solo el número de reserva. |
| WA · 4c señal pegada sin fecha | `01a12f08-0150-7d83-b5b4-ceffa5ef6d5e` | Envío (con tool call), «¿me dice su fecha de nacimiento?», «Vale. » + señal | Acusa recibo y pide la fecha; sin consultar | PASS | `84405be7-02f9-4dd8-9e7c-de5f86f2efa7` | Confirma la recepción sin leer el número y pide la fecha de nacimiento. |
| WA · 4d segunda oferta | `01a12f08-05a2-7659-96b7-7bd52913c221` | Rechazó WhatsApp, dictó datos, consultar_reembolso devuelve `{"encontrada":false}` | Segunda oferta de WhatsApp | FAIL | `d66770c9-ffca-4584-80a5-98ce5af93c87` | Solo pidió repetir el número, sin ofrecer el WhatsApp. |
| WA · 4e no reenviar | `01a12f08-09af-7986-a646-30175e436da2` | Envío (con tool call) + «¿Me lo puede mandar otra vez?» | Sin nuevo enviar_whatsapp; ofrece dictar | PASS | `f88776be-f172-4029-adc4-822d80002750` | No reenvía ni promete otro mensaje; ofrece continuar por voz. |
| WA · 4f sin WhatsApp | `01a12f08-0e5c-7d43-8054-bd9d051771be` | Como 4a1 con `whatsapp_posible=false` | No menciona WhatsApp; pide la reserva | PASS | `87dcda8c-c88d-44f0-ba30-f2bc4064c33f` | Pide el número sin mencionar WhatsApp ni usar herramientas. |
| WA · 4g inglés | `01a12f08-6aaf-7957-953e-8442d702ad2b` | Conversación en inglés, acepta | `enviar_whatsapp {idioma:"en"}` | PASS | `c9d40da5-0c4b-4f3f-bf38-2303cc85652f` | Solo ejecuta enviar_whatsapp con idioma en. |
| WA · 4h señal tardía tras verificar | `01a12f08-17ae-7b80-a6df-eb19f4d1fdda` | Dictado, verificado (resumen en texto), explica fianza, llega señal | Ignora la señal; sin nuevas herramientas | PASS | `94c40035-10b8-495e-9a28-3f4183972020` | Ignora la señal y cierra resumiendo la liberación de la fianza. |

Total: 8 PASS, 2 FAIL.

## Fallos que apuntan al prompt (no se ha cambiado el prompt)

- **4a3:** al llegar la señal con la fecha ya dada, el agente consulta correctamente pero habla de más: repite el nombre y la fecha en voz alta en lugar de decir solo «Me ha llegado, gracias».
- **4d:** tras «no encontrada» el agente no hace la SEGUNDA OFERTA. Puede influir que en el prompt la rama «Verificado false» (releer los datos) y la rama «No encontrada» (segunda oferta) se solapan, y la forma real del resultado de la herramienta no se conoce con certeza (los evals usan `{"encontrada":false}`). Conviene reforzar la segunda oferta en el prompt o repetir esta prueba con una llamada real.

## Notas sobre los evals

- El formato de los evals: `eval_mode` es `custom`, cada mensaje lleva `turn_index`, y `expected_tool_calls` usa `{"name":..., "args":...}`.
- Las llamadas previas a herramientas se incluyen en el historial como mensaje `assistant` con `tool_calls` seguido de un mensaje `role: "tool"`. Sin ellas (solo texto «Se lo acabo de enviar»), el agente no ve que ya envió y vuelve a ejecutar enviar_whatsapp (falso fallo en la primera pasada de 4a3, 4c y 4e; corregido en los evals).
- Cuando la expectativa es una llamada a herramienta, el resultado de la herramienta es simulado (en 4a2 y 4g fue un error), por lo que esos evals solo valoran la llamada, no el texto posterior.
- 4h usa un resumen en texto del resultado verificado, no un tool call real.

## Cómo repetirlos

Con el conector `hr` de HappyRobot, para cada eval:

```
manage_custom_evals action=run eval_id=<eval_id de la tabla> version_id=<versión a probar>
manage_custom_evals action=list_runs eval_id=<eval_id>   # unos segundos después
```

Para probar una versión nueva, usa su `version_id` (el nodo cambia de ID en cada versión, pero los evals cuelgan del workflow y se pueden lanzar contra otra versión). Los evals se listan con `action=list node_id=<node_id>`.

## Ronda 2 (12/10/2026): ajustes de prompt

Versión probada: W1 v2 `01a12efe-08b0-74e8-acba-f27b76f791eb` (slug `pc4zvke3xdjl`), mismo nodo, prompt editado en el sitio (sin publicar). Fichero: `casos/reembolsos/prompts/reembolsos-whatsapp/v2/receive-customer-call.md`.

Cambios: (1) bloque «DATOS QUE LLEGAN POR WHATSAPP»: acuse corto sin repetir número, nombre ni fecha, y consulta en el mismo turno; (2) «No encontrada»: la SEGUNDA OFERTA pasa a ser lo primero de la rama, obligatoria cuando el resultado trae `encontrada false`, `whatsapp_posible` es true y no se ha enviado, y empieza diciendo que no aparece con esos datos.

| Eval | Ronda 1 | Ronda 2 | Run ronda 2 |
|---|---|---|---|
| 4a1 oferta inicial | PASS | PASS | `f8969fe7-5c83-4f40-a3f2-a1b0c43ff5b7` |
| 4a2 acepta → envía | PASS | PASS | `138309db-3dc8-4670-9453-41418c40e98c` |
| 4a3 señal con fecha ya dada | FAIL | PASS | `5d2dc8c6-fd3e-4110-b52d-838110e501a2` |
| 4b rechaza | PASS | PASS | `d6963c33-3f1d-4499-972c-f0929cd78b3c` |
| 4c señal pegada sin fecha | PASS | PASS | `b2d28609-639e-4b17-9801-6a36acd4bc7a` |
| 4d segunda oferta | FAIL | PASS | `ec67914a-9a2c-459e-b2fe-693ed723e61d` |
| 4e no reenviar | PASS | PASS | `b877ebb8-88be-4eb3-94bc-decb0e06b1dc` |
| 4f sin WhatsApp | PASS | PASS | `388661d7-0138-41e9-bbb8-1505e0960fef` |
| 4g inglés | PASS | PASS | `d60d77fa-e7bc-4d46-95c4-b59b002c6b0c` |
| 4h señal tardía tras verificar | PASS | PASS | `8325089a-024c-4b65-a5f0-d18758c3a4af` |

Total ronda 2: 10 PASS, 0 FAIL. Nota: una pasada intermedia con solo el primer ajuste de 4d dejó 4d en FAIL (ofrecía el WhatsApp pero no decía que no aparecía con esos datos); se añadió esa frase y se relanzaron los 10.

## Ronda D-005 (15/10/2026): fallos de la prueba por voz de la tarde

Versiones: W1 v4 `01a13eba-f5cd-7bac-bc47-3e399e60f3a9` (publicada) contra W1 v5
`01a1401c-0965-780f-b482-dd25c59ca603`; W2 v8 `01a13a4e-dba7-7d39-aa38-e958bb2a7ccd` (publicada) contra
W2 v9 `01a1401c-0eaf-7777-a8d7-ab69e20e8a7b`. Datos inventados (`Prueba Prueba`, `prueba@ejemplo.com`,
`ER00000000`, 21/08/1985). Informe de las llamadas: `docs/informes/2026-10-15-pruebas-tarde-w1-v4.md`.

### Evals nuevos de W1 (nodo «Reembolsos»)

| Eval | eval_id | Reproduce | v4 | v5 (final) |
|---|---|---|---|---|
| D5 · «Ya lo he enviado» sin datos: no dice que le ha llegado | `01a14028-c1fc-74ac-ad7c-e435c8ae6325` | «Me ha llegado» sin señal (llamadas 1, 2 y 4) | FAIL | PASS |
| D5 · Sin nombre del cliente: lo pide y no consulta | `01a14028-d094-75b3-9e0b-947d90e04362` | Nombre inventado (llamada 2) | PASS | PASS |
| D5 · Email con guion de la transcripción: no lee «guion» | `01a14028-d5e5-74a7-8200-fc5e1518da53` | «ce, guion, efe…» (llamada 1) | FAIL | PASS |
| D5 · Espera del WhatsApp: no repite la espera ni ofrece voz | `01a14028-dc48-77a4-8111-970880769203` | Espera repetida (llamadas 1 a 4) | PASS | PASS |
| D5 · Datos de WhatsApp tras dos consultas: hace la tercera | `01a14029-7bfd-7ed9-add9-e97e9076bdd8` | Límite de dos consultas (llamada 3) | FAIL | PASS |
| D5 · WhatsApp trae el email como nombre: pide el nombre por voz | `01a14029-8416-7aec-84c7-845641d21436` | Nombre = trozo del email (llamada 2) | FAIL | PASS |
| D5 · No encontrada con datos de WhatsApp: no pide escribir otra vez | `01a14029-8d9a-75f4-881b-5e9fd47b7f36` | Pide escribir el NIE en el WhatsApp (llamada 4) | FAIL | PASS |

Los evals no pueden reproducir los turnos que HappyRobot da al agente cuando hay silencio (el origen de
«Si lo prefiere, seguimos por aquí» a los 6-7 s): el de la espera prueba un «vale, un momento» del
cliente. Eso hay que mirarlo en la prueba por voz.

### Regresión de W1 v5 (18 evals anteriores)

Ronda final con el prompt definitivo: 17/18 a la primera y 18/18 al repetir el que falló («ID ·
Verificado: «Ya he encontrado su reserva»»: el juez pidió el mes en «el siete»; el ejemplo del prompt
tampoco lo lleva). Durante el ajuste:
- con la primera versión del prompt, el email se deletreaba sin guion pero leía el apellido en bloque:
  se añadió el ejemplo de deletreo completo;
- la frase «lo que dices es solo "Me ha llegado"» hizo que, sin fecha de nacimiento, no la pidiera
  (4c, 3 fallos seguidos): se separaron los dos casos («si ya tienes la fecha…» / «si todavía no…»).

### Evals de W2 (nodo «Prompt» de la rama es)

| Eval | eval_id | v8 | v9 |
|---|---|---|---|
| D5 · Solo email: pide el nombre, no el número de reserva | `01a14029-f772-737b-82c1-d294e24a23fa` | PASS | PASS |
| D5 · Repite el email: no repite la pregunta y pide el nombre | `01a14029-fba0-7e9a-aa7d-3dca27cc6f0a` | FAIL (pasa a la llamada con el email como nombre) | PASS |
| D5 · Email y luego nombre: pasa a la llamada con los dos | `01a1402a-016c-7e3f-84a1-996b618cc6d3` | PASS | PASS |
| D5 · Email, nombre y número ER: el número no va en dni | `01a1402a-05c6-7180-a707-fd53cf0cbde4` | FAIL (ER también en `dni`) | PASS |
| WA · Solo email y nombre (W-a) | `01a13bba-88b3-7f3c-b076-edb091234608` | PASS | FAIL (juez: error simulado del POST) → PASS |
| WA · Solo DNI y nombre (W-b) | `01a13bba-8ddb-7568-bb8d-1fc00be85980` | PASS | FAIL (respuesta vacía) → PASS |
| WA · Solo nombre (W-c) | `01a13bba-925a-754f-bfd8-6ba47ce08557` | FAIL | FAIL → PASS |

En W2 v9 los tres evals anteriores fallaron en la primera pasada y pasaron al repetirlos; W-c sigue
siendo inestable (ver pendientes). Los evals de W2 solo cuelgan de la rama es; la rama en tiene el mismo
prompt.
