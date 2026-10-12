# Evals automáticos de la conversación por WhatsApp (T4)

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
| WA · 4a3 señal con fecha ya dada | `01a12f08-6619-710b-9703-38be8649ce54` | Oferta, envío (con tool call), fecha dada, luego señal | `consultar_reembolso` con ER00000000, Prueba Prueba, 21/08/1985; sin leer datos | FAIL | `78780a73-945e-41a5-8a3e-c50691ba1d70` | Consulta bien, pero dice «Un momento…» y repite nombre y fecha en vez de «Me ha llegado, gracias». |
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
