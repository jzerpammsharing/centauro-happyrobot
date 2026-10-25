<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v7 (3it0j96ugsqw) · nodos: transfer_to_human_agent (los cinco módulos) y buscar_punto_de_encuentro (Triaje) · copiado: 2026-10-25 -->

# Herramientas que cambian en la v7

Cambian la descripción y el parámetro `cola` de los cinco `transfer_to_human_agent` (D-021) y el parámetro
`aeropuerto` de `buscar_punto_de_encuentro` del Triaje. Se pegó la función entera por API (`function` es un reemplazo
completo): `message`, `hold_music`, `hold_music_asset_id`, `motivo_transferencia` y `resumen_para_agente` siguen igual
que en la v6 (copias en `../v2/herramientas-*.md` y, la de Consultas, en `../v4/herramientas-consultas.md`). En los
textos, «Gestión ahora: …» es la variable `{{e51cd732-f403-4ef7-95d4-490347960a93.gestion_abierta}}`.

## transfer_to_human_agent · Triaje (`01a17350-f4f0-7560-9ba6-d67935537200`, persistent_id `17c682a0-82d2-42f6-88fa-817d8cba0783`)

**Descripción:** Transfiere la llamada a una cola de compañeros. Úsala solo en los casos de TRANSFIERES TÚ y de NO
INSISTAS, o si no puedes seguir al cliente por el idioma. En modo virtual, solo para una avería o un accidente (cola
asistencia). Con gestión cerrada, nunca con la cola gestion: lo importante de su alquiler o su viaje va con la cola
minibus; facturas, reembolsos, cargos y reclamaciones no se transfieren. Prolongar, la web, la contraseña, el minibús,
las oficinas y las dudas del alquiler no se transfieren: tienen su herramienta. Ejecútala en el mismo turno en que
decides transferir, sin decir antes «le paso». Si devuelve gestion_cerrada, no la repitas: sigue COLA DE GESTIÓN
CERRADA.

**`cola`:** Cola de destino. Valores permitidos EXACTOS: "asistencia" (avería o accidente; funciona siempre),
"nueva_reserva" (todavía no tiene reserva y quiere alquilar, o pregunta precios o disponibilidad para un alquiler
nuevo), "minibus" (queja del minibús, persona sin motivo en la línea de Minibús, idioma que no puedes seguir,
conversación atascada o, con gestión cerrada, lo que iría a gestión si es algo importante de su alquiler o su viaje,
como cambiar su reserva o un dato de ella, o una persona sin motivo en la línea de Prolongación), "gestion" (hay que
mirar o cambiar un dato concreto de su reserva, o persona sin motivo en la línea de Prolongación; solo con gestión
abierta). Gestión ahora: … Si es false, nunca uses "gestion".

## transfer_to_human_agent · Consultas del alquiler (`01a17350-f4f0-7d27-bfc7-00b9cfcd174e`, persistent_id `fbe2e40e-4915-4f44-9bac-59c318862e97`)

**Descripción:** Gestión ahora: … Si es false, NO la uses para una factura, un reembolso, un cargo que no reconoce o
una reclamación, aunque el cliente insista o pida una persona: dile el horario de gestión y el formulario de «Atención
al cliente y reclamaciones». Transfiere la llamada a una cola de compañeros. Úsala solo en los casos de ESCALADO, o si
no puedes seguir al cliente por el idioma. Cuando la sección manda transferir en el caso del cliente: si ya ha pedido
que lo mire alguien, ejecútala en ese turno; si no, pregúntale antes si quiere que le pases (puedes decir antes una
frase con la respuesta) y ejecútala cuando acepte. En modo virtual, solo para una avería o un accidente (cola
asistencia). Con gestión cerrada, nunca con la cola gestion: si es algo importante de su alquiler o su viaje (recoger o
devolver, cambiar o cancelar una reserva, un problema con el coche, el servicio de espera de un vuelo o un tren
retrasado) y no lo resuelves o pide una persona, ejecútala con la cola minibus. Prolongar, la web, la contraseña, el
minibús y las oficinas no se transfieren: tienen su herramienta. Ejecútala en el mismo turno en que decides
transferir, sin decir antes «le paso». Si devuelve gestion_cerrada, no la repitas: sigue COLA DE GESTIÓN CERRADA.

(Segunda subida: la excepción de facturas, reembolsos, cargos y reclamaciones pasa al principio, con «aunque el
cliente insista o pida una persona»; sin eso, V7-GC-CARGO transfería a la cola minibus 2 de cada 3 veces.)

**`cola`:** … "minibus" (queja del minibús, idioma que no puedes seguir o, con gestión cerrada, algo importante de su
alquiler o su viaje que no resuelves o en que pide una persona: recoger o devolver, cambiar o cancelar una reserva, un
problema con el coche, el servicio de espera de un vuelo o un tren retrasado; nunca una factura, un reembolso, un cargo
ni una reclamación), "gestion" (sin cambios) …

## transfer_to_human_agent · Prolongación (`01a17350-f4f2-7c5a-b55c-277cad0617a9`, persistent_id `01a150ca-b67d-726a-845b-19c18b2e891e`)

**Descripción:** Gestión ahora: … Si Gestión ahora es false, nunca uses la cola gestion: sigue COLA DE GESTIÓN
CERRADA. Transfiere la llamada a una cola de compañeros. Úsala en los casos de ESCALADO, cuando tus secciones mandan
transferir (por ejemplo, un dato concreto de su reserva) o si no puedes seguir al cliente por el idioma. Si el cliente
ya ha pedido que lo mire alguien, o la sección manda transferir en ese turno, ejecútala en ese turno; si solo ofreces
pasarle, espera a que acepte. En modo virtual, solo para una avería o un accidente (cola asistencia). Con gestión
cerrada, lo importante de su alquiler que no resuelves, o si pide una persona, va con la cola minibus; facturas,
reembolsos, cargos y reclamaciones no se transfieren, ni lo que pida una agencia o una aseguradora. Prolongar,
devolver tarde, la web que no deja, la contraseña y el coche de aseguradora o de empresa no se transfieren por sí
solos: tienes instrucciones para ellos. Ejecútala en el mismo turno en que decides transferir, sin decir antes «le
paso». Si devuelve gestion_cerrada, no la repitas: sigue COLA DE GESTIÓN CERRADA.

(Antes: «Si Gestión ahora es false y el caso es de gestión, no la llames: di que gestión está cerrada y su horario» y
«Con gestión cerrada, nunca con la cola gestion».)

**`cola`:** … "minibus" (idioma que no puedes seguir o, con gestión cerrada, algo importante de su alquiler que no
resuelves o en que pide una persona: prolongar, la web que no le deja, devolver, cambiar su reserva, un problema con
el coche; nunca facturas, reembolsos, cargos ni reclamaciones, ni si llama una agencia o una aseguradora), "gestion"
(sin cambios) …

## transfer_to_human_agent · Punto de encuentro (`01a17350-f4f1-7e5d-8358-d85de62879fe`, persistent_id `00435498-eccf-4110-9cf1-eb17821af3ed`)

**Descripción:** cambian dos frases. «Si Gestión ahora es false y el caso es de gestión, no la llames: di que gestión
está cerrada y su horario» pasa a «Si Gestión ahora es false, nunca uses la cola gestion: sigue COLA DE GESTIÓN
CERRADA (lo importante de su alquiler o su viaje, con la cola minibus)», y sale «Con gestión cerrada, nunca con la cola
gestion» (queda dicho al principio). El resto, igual.

**`cola`:** "minibus" añade al final «; y, con gestión cerrada, lo que iría a gestión si es algo importante de su
reserva o su viaje, como el servicio de espera o devolver con la oficina cerrada».

## transfer_to_human_agent · Información de oficina (`01a17350-f4f1-7f48-8f74-3b67051e4c5f`, persistent_id `62c5b6dd-5dde-4b3a-9a93-adb638c0bd66`)

**Descripción:** como en Punto de encuentro, con «(lo importante de su alquiler o su viaje, con la cola minibus; un
cargo, una factura, un reembolso o una reclamación no se transfieren)», y sale «Con gestión cerrada, nunca con la cola
gestion».

**`cola`:** "minibus" añade al final «; y, con gestión cerrada, lo que iría a gestión si es algo importante de su
reserva o su viaje, pero nunca un cargo, una factura, un reembolso ni una reclamación».

## buscar_punto_de_encuentro · Triaje (`01a17350-f4ef-70f4-bdd8-7f5a4525a7a8`, persistent_id `72261523-5d3f-4830-ac36-67ab187d93ed`)

**`aeropuerto`:** Nombre del aeropuerto donde está el cliente, tal como lo ha dicho (por ejemplo: Valencia, Rodas,
Lisboa, Madrid). Una terminal o un parking solos no son un aeropuerto: si solo dice eso, pregúntale antes en qué
aeropuerto está, salvo la terminal dos A, dos B o dos C, que es Barcelona, y la cuatro, que es Madrid.

(Añadida la segunda frase. `terminal`, `tool_index_id` y `tool_index_hash` siguen igual.)

**Descripción** (segunda subida, tras la pasada de evals: V7-TERM-2 llamaba a la herramienta con «terminal uno»): la
frase «Si todavía no sabes el aeropuerto, pregúntalo antes.» pasa a «Si todavía no sabes el aeropuerto, pregúntalo
antes: si solo ha dicho una terminal o un parking, no lo sabes (la terminal uno, dos o tres está en varios
aeropuertos).» El resto, igual.

## estado_oficina · Punto de encuentro (`01a17350-f4ee-7e66-8be6-708b6a4a6983`, persistent_id `01a1575e-923d-7deb-8a35-da450582d445`)

Segunda subida (V7-TERM-PE deducía Madrid de «terminal uno» y llamaba a la herramienta):

**`aeropuerto`:** El aeropuerto del cliente, tal como lo ha dicho (por ejemplo «Valencia», «Madrid», «Atenas»,
«Milán-Malpensa»). Sin terminal ni datos personales. Una terminal o un parking no son un aeropuerto y la terminal uno,
dos o tres está en varios: si solo tienes eso, no la ejecutes ni deduzcas la ciudad; pregunta antes en qué aeropuerto
está (solo la terminal dos A, dos B o dos C es Barcelona, y la cuatro, Madrid).

**Descripción:** «ejecútala en cuanto sepas el aeropuerto» pasa a «ejecútala en cuanto sepas el aeropuerto (no lo
deduzcas de una terminal)». El resto, igual que en la v2.
