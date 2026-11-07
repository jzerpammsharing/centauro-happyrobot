# Evals de la búsqueda v2 del MCP en W1 v10 (D-006) · 22/10/2026

Datos inventados: reservas `ER00000000`–`ER00000002` y «Prueba Prueba». Evals de HappyRobot (modo `custom`) sobre el
nodo «Reembolsos» de W1 v10 (`2y93xxzzph11`, version_id `01a1607d-d367-7a80-9528-5eb548080d83`). Las evals se comparten
entre versiones: las 37 de antes valen para la v9 y la v10. Las 9 nuevas están en la carpeta «v10 · Búsqueda v2
(teléfono, otras reservas)».

Variables por defecto de las evals: `telefono_consultable` false y `whatsapp_posible` true (salida de prueba de
«Calcular idioma y saludo»). Las evals de teléfono ponen `telefono_consultable` = true en sus variables.

## Evals nuevas

| Eval | Caso | Esperado |
|---|---|---|
| TEL-0 | Teléfono consultable; el cliente da el motivo | Pide el nombre completo, no el número de reserva |
| TEL-1 | Teléfono consultable; da el nombre y la fecha | `consultar_reembolso` con nombre y fecha y los tres identificadores vacíos |
| TEL-2 | El primer intento vuelve «no encontrada» | Dice que no la encuentra con este teléfono y pide el número, sin decir que no existe ni ofrecer el WhatsApp |
| TEL-3 | Tras el primer intento, sin número, da el email | Consulta con el email, sin volver a pedir el nombre ni la fecha |
| TEL-4 | Ni número ni email: da el DNI | Consulta con el DNI |
| TEL-5 | DNI ilegible tras el primer intento | Pide repetirlo cifra a cifra, con la letra al final |
| TEL-6 | El primer intento vuelve «falta el identificador» | Pide el número sin hablar del error |
| OTRA-1 | Verificada una reserva; el cliente habla de otra que está en `otras_reservas` | Consulta con el número de esa reserva, sin pedírselo ni leérselo |
| CTA-1 | `tiene_cuenta` false y pide la factura | Primero crear la contraseña con «¿Has olvidado tu contraseña?», después la ruta |

Las evals TEL-1, TEL-3, TEL-4 y OTRA-1 dicen «Solo se valora hasta la llamada a la herramienta»: el juez valoraba lo
que la simulación inventaba después del resultado.

## Cambios en evals de antes

- «D16 · No es esa reserva: explica el límite y pide el número»: el texto esperado decía «con el DNI o el email solo
  le aparece su reserva más reciente». Con la v2 vienen hasta 5 reservas. Ahora espera que no pregunte por oficinas ni
  fechas (la eval no trae `otras_reservas`), que diga que solo le aparece esa y que pida el número.

## Qué se encontró y se corrigió durante las pruebas

| Problema en la v10 | Causa | Arreglo |
|---|---|---|
| «WA 4a1» pedía el nombre en vez del número (0 de 3) | El bloque PRIMER INTENTO se aplicaba con el teléfono no consultable | El bloque empieza con «Mira antes "Teléfono del cliente consultable": si es false, este bloque no existe para ti» |
| «WA 5a» y «WA 5b»: contestaba «Sí.» al ER12345678 dictado (0 de 2) | La regla nueva «Nunca rellenes un campo con un valor de ejemplo»; ER12345678 es el número de los ejemplos y de las pruebas | Regla quitada (los `example` de la herramienta ya van vacíos). 5b pasa en las 4 corridas siguientes |
| «D16 No es esa reserva» preguntaba por la oficina (0 de 2) | La regla nueva de `otras_reservas` sin caso para cuando no viene | «Si `otras_reservas` no viene, está vacía o ninguna encaja, no le preguntes por oficinas ni por fechas» y expectativa actualizada. Pasa en las 4 corridas siguientes |
| «D16 No da la fecha a la primera» transfiere | Sin identificar (la API no enseña los mensajes de la eval) | **Sin resolver**: ver abajo |

## «D16 No da la fecha a la primera»: la regresión que queda

El cliente no da la fecha de nacimiento cuando se le pide. La v9 la vuelve a pedir: 7 de 7. La v10 a menudo transfiere
y dice que le pasa con un compañero.

| Prompt de la v10 | Resultado |
|---|---|
| Primeras versiones de la noche | 5 de 16 |
| Con «Que el cliente no dé un dato a la primera (por ejemplo, la fecha de nacimiento) no es una consulta ni un intento, y nunca es motivo para transferir» en el párrafo del límite | 5 de 6, pero «WA 5a», «WA 4a1» y «D5 No encontrada con datos de WhatsApp» bajan a 0 de 3 cada una (en la v9, a la vez, 3 de 3) |
| Sin esa frase | 0 de 4 |
| **Final**: frase acotada en «Si el cliente se resiste»: «que no te dé la fecha de nacimiento a la primera no cuenta como consulta ni como intento de identificación» | 1 de 4 |

Se queda la versión final: la frase general arreglaba esta eval pero rompía otras tres de forma estable. Hay que
probarlo por voz y mirar la eval en el editor (qué dice el cliente) antes de publicar.

## Pasada final (prompt definitivo, 56.262 caracteres)

Corrida el 22/10 entre las 01:29 y las 01:35 (hora de Madrid) sobre el prompt definitivo. «Pasa» es pasadas / corridas
con ese prompt; las que fallaron se repitieron.

**41 de 46 pasan siempre. 5 fallan alguna vez:**

| Eval | Pasa | Qué hace mal | v9 |
|---|---|---|---|
| D16 · No da la fecha a la primera | 1 de 4 | Transfiere en vez de volver a pedir la fecha (ver arriba) | 7 de 7 |
| OTRA-1 · otra reserva de `otras_reservas` | 0 de 2 | La consulta con el número de la otra reserva es correcta; después del resultado simulado transfiere. El juez lo cuenta aunque la eval dice que solo se valora hasta la llamada. Con los prompts anteriores de la noche pasó 4 de 4 | No aplica |
| WA · 5a corrige el número repetido | 1 de 2 | Pide que repita el número en vez de ofrecer el WhatsApp | 2 de 2 |
| ID · Verificado: «Ya he encontrado su reserva» | 1 de 2 | Dijo «el siete» sin el mes | Pasaba |
| WA · 4h señal tardía tras verificar | 1 de 2 | Dijo «Me ha llegado» a la señal y volvió a consultar | 1 de 1 |

Pasan siempre:

| Grupo | Evals |
|---|---|
| Nuevas (8) | TEL-0, TEL-1, TEL-2, TEL-3, TEL-4, TEL-5, TEL-6, CTA-1 |
| WhatsApp (11) | 4a1 (2 de 2), 4a2, 4a3, 4b, 4c, 4d, 4e, 4f, 4g, 5b, 5c |
| Identificación (4) | Email, DNI, Número y email, DNI ilegible |
| D5 (7) | No encontrada con datos de WhatsApp (2 de 2), Email como nombre, Tras dos consultas, Espera, Email con guion, Sin nombre, «Ya lo he enviado» |
| D16 (11) | Fecha tras WhatsApp, «De acuerdo», ER con siete cifras, Inglés, Ofrece el DNI, Reserva no iniciada, No es esa reserva, Confirmación ambigua, Verificado false confirma, Verificado false deletrea, «Do you speak English?» |

Notas:
- «D5 Email con guion» y «D16 Verificado false confirma» fallaban también en la v9; esta vez pasan, pero son
  inestables.
- Antes de los arreglos de la noche, la regresión daba 33 de 37.
- Cada corrida es una conversación simulada: la misma eval puede pasar y fallar con el mismo prompt. Una pasada no
  sustituye a la prueba por voz.

## Sin probar

- Que el `telefono` llegue de verdad al MCP: `test_node` del MCP Call devuelve «falta el identificador» (ver
  `docs/pendientes.md`).
- El extract «Registrar resultado de la llamada»: no cambia en la v10 (no distingue la identificación por teléfono).
- Los silencios y los turnos largos solo se ven por voz.
