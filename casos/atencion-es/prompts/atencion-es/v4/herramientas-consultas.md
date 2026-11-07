<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v4 (02qakmz6tbk0) · nodo: transfer_to_human_agent (Consultas del alquiler) · copiado: 2026-10-24 -->

# Herramientas de Consultas del alquiler · v4

Solo cambia `transfer_to_human_agent` (nodo de la v4 `01a16ed5-c646-7a86-ad16-1c2df93fd016`, persistent_id
`fbe2e40e-4915-4f44-9bac-59c318862e97`), en la descripción y en el parámetro `cola` (D-019). El resto (message,
hold_music, `motivo_transferencia`, `resumen_para_agente` y las otras herramientas) es igual que en la v2:
`../v2/herramientas-consultas.md`. `{{gestion_abierta}}` va como nodo de variable de Plate con `group_id`
`e51cd732-f403-4ef7-95d4-490347960a93`.

Subido con `update_workflow_nodes` (campo `function` entero) el 24/10/2026. Motivo: con la sección nueva de
`recoger_tarde` en la conversación, V4-RT2 (acepta que le pasen con Gestión cerrada) daba 0/3: el bot le daba el
horario de Gestión. Con este cambio, 1/3; con el del prompt (`consultas-del-alquiler.md`), ver `pendientes.md`.

**Descripción** (añadido: «pero si acepta que le pases… no es un caso de gestión»):

Transfiere la llamada a una cola de compañeros. Úsala solo en los casos de ESCALADO, o si no puedes seguir al cliente
por el idioma. Cuando la sección manda transferir en el caso del cliente: si ya ha pedido que lo mire alguien,
ejecútala en ese turno; si no, pregúntale antes si quiere que le pases (puedes decir antes una frase con la respuesta)
y ejecútala cuando acepte. En modo virtual, solo para una avería o un accidente (cola asistencia). Con gestión
cerrada, nunca con la cola gestion; pero si acepta que le pases para comprobar el servicio de espera de un vuelo o un
tren retrasado, ejecútala con la cola minibus: no es un caso de gestión. Prolongar, la web, la contraseña, el minibús
y las oficinas no se transfieren: tienen su herramienta. Ejecútala en el mismo turno en que decides transferir, sin
decir antes «le paso». Si devuelve gestion_cerrada, no la repitas: sigue COLA DE GESTIÓN CERRADA.

**`cola`** (añadido en «minibus»: «o, con gestión cerrada, acepta que le pases para comprobar el servicio de espera
de un vuelo o un tren retrasado»):

Cola de destino. Valores permitidos EXACTOS: "asistencia" (avería o accidente, o acepta que le pases por un aviso
del coche o por la grúa; funciona siempre), "nueva_reserva" (quiere hacer una reserva nueva o acepta que un compañero
se la prepare), "minibus" (queja del minibús, idioma que no puedes seguir o, con gestión cerrada, acepta que le pases
para comprobar el servicio de espera de un vuelo o un tren retrasado), "gestion" (lo que la sección manda a GESTIÓN
DE RESERVA, un dato concreto de su reserva, o una persona sin motivo; solo con gestión abierta). Gestión ahora:
{{gestion_abierta}}. Si es false, nunca uses "gestion".
