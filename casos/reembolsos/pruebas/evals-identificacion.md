# Evals de identificación por email o DNI/NIE (D-003) · 14/10/2026

Datos inventados. Evals de HappyRobot (modo `custom`) sobre el nodo «Reembolsos» de cada versión; los
casos 1-4 están en V5 y en W1 v3 (con `whatsapp_posible = false`), y los de WhatsApp en W2 v8.

| # | Caso | Esperado |
|---|---|---|
| 1 | Sin número; dicta el email | `consultar_reembolso` con `email`, sin `numero_reserva` ni `dni` |
| 2 | Sin número ni email; da el DNI | `consultar_reembolso` con `dni` |
| 3 | Número y además email | Solo `numero_reserva` |
| 4 | El filtro devuelve `dato_no_interpretado` por DNI | Pide repetirlo cifra a cifra, con la letra al final |
| W-a | W2: nombre y email, sin número | `pasar_a_llamada` con `email` |
| W-b | W2: nombre y DNI | `pasar_a_llamada` con `dni` en mayúsculas y sin guion |
| W-c | W2: solo el nombre | Pide el dato de la reserva y no ejecuta la herramienta |

Resultados: V5 23/23 (19 previas + 4 nuevas; la «03 matrícula en vez del número» falló en la primera
pasada, se ajustó el prompt y pasa). W1 v3: 14/14 (10 previas + 4 nuevas). W2 v8: 2/3; falla W-c.
Código del filtro probado en local con el texto de cada `isError` del MCP (número, email, DNI, fecha,
falta, «no disponible», timeout, otro), en texto plano y en formato de contenido MCP.
