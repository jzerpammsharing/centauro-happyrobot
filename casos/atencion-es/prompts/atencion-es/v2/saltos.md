<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v2 (x8xd0llbdp3j) · nodo: herramientas de salto y Module Change · copiado: 2026-10-19 -->

# Saltos entre módulos (v2, Tarea 12)

Spec §5.6 y §5.7. Las 8 herramientas nuevas se crearon por API el 19/10/2026 a las 22:27; sus 8 Module Change los
creó el responsable en el editor (los Module Change no se pueden crear por API) y el controlador comprobó por API que
hay 12 y que apuntan al destino de la tabla. Los persistent_id de los Module Change nuevos son iguales a su ID de nodo.

Todas llevan `message: {"type": "none"}` y el parámetro obligatorio `motivo`; las que entran en un módulo que ya tenía
entrada desde el Triaje llevan además los parámetros de la v25 (`tema`/`oficina`, `aeropuerto`/`terminal`, `situacion`).
En HappyRobot el persistent_id de cada herramienta nueva es igual a su ID de nodo.

## Las 12 filas

| # | Herramienta | Módulo de origen (ID de nodo) | Herramienta: ID de nodo | Destino (ID de nodo · persistent_id) | Hijo |
|---|---|---|---|---|---|
| 1 | `volver_al_triaje` | Punto de encuentro (`01a14f1d-0397-7c91-b2bc-a12efeed5595`) | `01a155d9-5d9b-7fd6-bfaa-6b87ccd6ac42` | Triaje (`01a14f1d-0397-7925-af9e-b01d518bd921` · `c5a70932-117c-4360-9be8-adce260fe13e`) | Module Change `01a155e8-f3f3-7d25-a6cf-f788cbfee0b4` (creado en el editor el 19/10/2026) |
| 2 | `volver_al_triaje` | Información de oficina (`01a14f1d-0396-717d-8b6f-52f789dbe9a3`) | `01a155d9-5da4-74b3-a7c4-3bb6257242d6` | Triaje (`01a14f1d-0397-7925-af9e-b01d518bd921` · `c5a70932-117c-4360-9be8-adce260fe13e`) | Module Change `01a155ec-a9e8-733d-a286-a38da5f0b411` (creado en el editor el 19/10/2026) |
| 3 | `volver_al_triaje` | Prolongación (`01a14f69-b09d-7689-ad9e-8e8de0fd6fb4`) | `01a155d9-5da8-738a-8af4-ada5f82ebdd7` | Triaje (`01a14f1d-0397-7925-af9e-b01d518bd921` · `c5a70932-117c-4360-9be8-adce260fe13e`) | Module Change `01a155ec-37d2-7d99-b8b8-d4e83069c3ba` (creado en el editor el 19/10/2026) |
| 4 | `volver_al_triaje` | Consultas del alquiler (`01a14f1d-0397-7b22-b5ce-bcb398a7605e`) | `01a155d9-5dac-7449-b143-4392c795602f` | Triaje (`01a14f1d-0397-7925-af9e-b01d518bd921` · `c5a70932-117c-4360-9be8-adce260fe13e`) | Module Change `01a155ed-9634-753f-b55c-de35edd40c1d` (creado en el editor el 19/10/2026) |
| 5 | `informacion_oficina` | Punto de encuentro (`01a14f1d-0397-7c91-b2bc-a12efeed5595`) | `01a155d9-5db0-7106-ab47-43027e0f8647` | Información de oficina (`01a14f1d-0396-717d-8b6f-52f789dbe9a3` · `0c60218b-8901-47bd-95de-40e0e1af1296`) | Module Change `01a155e8-59fa-7a49-ba5b-ca96f22b2050` (creado en el editor el 19/10/2026) |
| 6 | `buscar_punto_de_encuentro` | Información de oficina (`01a14f1d-0396-717d-8b6f-52f789dbe9a3`) | `01a155d9-5db4-757d-ac17-fc1adb754b0f` | Punto de encuentro (`01a14f1d-0397-7c91-b2bc-a12efeed5595` · `a80fca22-b295-41e3-a735-a3c878af4eee`) | Module Change `01a155ec-dcfc-730e-9c8c-daa3bfbc19ae` (creado en el editor el 19/10/2026) |
| 7 | `prolongar_alquiler` | Consultas del alquiler (`01a14f1d-0397-7b22-b5ce-bcb398a7605e`) | `01a155d9-5db8-7b78-8ecd-d52451c7ed84` | Prolongación (`01a14f69-b09d-7689-ad9e-8e8de0fd6fb4` · `01a14f69-b09d-7689-ad9e-8e8de0fd6fb4`) | Module Change `01a155ee-138f-7765-954f-20ec0b421975` (creado en el editor el 19/10/2026) |
| 8 | `informacion_oficina` | Prolongación (`01a14f69-b09d-7689-ad9e-8e8de0fd6fb4`) | `01a155d9-5dbb-704a-b119-2db7b00a6fa2` | Información de oficina (`01a14f1d-0396-717d-8b6f-52f789dbe9a3` · `0c60218b-8901-47bd-95de-40e0e1af1296`) | Module Change `01a155ec-665d-7f0f-86b1-c070b229aa53` (creado en el editor el 19/10/2026) |
| a | `consultas_alquiler` | Punto de encuentro (`01a14f1d-0397-7c91-b2bc-a12efeed5595`) | `01a14f1d-0398-7a4b-84e7-313e054df714` | Consultas del alquiler (`01a14f1d-0397-7b22-b5ce-bcb398a7605e` · `38378785-0846-4920-b41a-583f7c5773fb`) | Module Change `01a14f1d-039b-7e6e-91ee-a0401da2c7e3` (existe, del duplicado; no se toca) |
| b | `consultas_alquiler` | Información de oficina (`01a14f1d-0396-717d-8b6f-52f789dbe9a3`) | `01a14f1d-0398-71cd-be10-a50ab91d1f5d` | Consultas del alquiler (`01a14f1d-0397-7b22-b5ce-bcb398a7605e` · `38378785-0846-4920-b41a-583f7c5773fb`) | Module Change `01a14f1d-039b-7e2a-90f5-a43135ba4453` (existe, del duplicado; no se toca) |
| c | `buscar_punto_de_encuentro` | Consultas del alquiler (`01a14f1d-0397-7b22-b5ce-bcb398a7605e`) | `01a14f1d-0398-793a-a4f6-4cc4ed3a45c4` | Punto de encuentro (`01a14f1d-0397-7c91-b2bc-a12efeed5595` · `a80fca22-b295-41e3-a735-a3c878af4eee`) | Module Change `01a14f1d-039a-76cb-8e2c-fd908a63d1af` (existe, del duplicado; no se toca) |
| d | `informacion_oficina` | Consultas del alquiler (`01a14f1d-0397-7b22-b5ce-bcb398a7605e`) | `01a14f1d-0398-78ce-93ed-6d599a4dcad6` | Información de oficina (`01a14f1d-0396-717d-8b6f-52f789dbe9a3` · `0c60218b-8901-47bd-95de-40e0e1af1296`) | Module Change `01a14f1d-039a-7490-9015-e42727f49b17` (existe, del duplicado; no se toca) |

Los destinos de las 12 filas se comprobaron (filas a–d por el agente; 1–8 por el controlador) con `get_node_details` (`moduleId`/`modulePersistentId`) el 19/10/2026.

## Lista que se dio al responsable (Paso 2, hecho)

En el editor de la v2 (`https://platform.eu.happyrobot.ai/mutuamobility/workflows/rntn68r0a8gh/editor/x8xd0llbdp3j`):

1. Bajo la herramienta `volver_al_triaje` (`01a155d9-5d9b-7fd6-bfaa-6b87ccd6ac42`) del módulo Punto de encuentro, crear un Module Change que apunte a **Triaje** (`01a14f1d-0397-7925-af9e-b01d518bd921`).
2. Bajo la herramienta `volver_al_triaje` (`01a155d9-5da4-74b3-a7c4-3bb6257242d6`) del módulo Información de oficina, crear un Module Change que apunte a **Triaje** (`01a14f1d-0397-7925-af9e-b01d518bd921`).
3. Bajo la herramienta `volver_al_triaje` (`01a155d9-5da8-738a-8af4-ada5f82ebdd7`) del módulo Prolongación, crear un Module Change que apunte a **Triaje** (`01a14f1d-0397-7925-af9e-b01d518bd921`).
4. Bajo la herramienta `volver_al_triaje` (`01a155d9-5dac-7449-b143-4392c795602f`) del módulo Consultas del alquiler, crear un Module Change que apunte a **Triaje** (`01a14f1d-0397-7925-af9e-b01d518bd921`).
5. Bajo la herramienta `informacion_oficina` (`01a155d9-5db0-7106-ab47-43027e0f8647`) del módulo Punto de encuentro, crear un Module Change que apunte a **Información de oficina** (`01a14f1d-0396-717d-8b6f-52f789dbe9a3`).
6. Bajo la herramienta `buscar_punto_de_encuentro` (`01a155d9-5db4-757d-ac17-fc1adb754b0f`) del módulo Información de oficina, crear un Module Change que apunte a **Punto de encuentro** (`01a14f1d-0397-7c91-b2bc-a12efeed5595`).
7. Bajo la herramienta `prolongar_alquiler` (`01a155d9-5db8-7b78-8ecd-d52451c7ed84`) del módulo Consultas del alquiler, crear un Module Change que apunte a **Prolongación** (`01a14f69-b09d-7689-ad9e-8e8de0fd6fb4`).
8. Bajo la herramienta `informacion_oficina` (`01a155d9-5dbb-704a-b119-2db7b00a6fa2`) del módulo Prolongación, crear un Module Change que apunte a **Información de oficina** (`01a14f1d-0396-717d-8b6f-52f789dbe9a3`).

Tras crearlos, `get_workflows` debe dar 12 nodos `module-change` (Paso 3).

## Definición de las herramientas (fuente)

### 1. `volver_al_triaje` en Punto de encuentro

**Descripción:** Úsala cuando el cliente pide otra gestión que no es del minibús ni del punto de encuentro, ni una duda del alquiler, ni el horario o la dirección de una oficina. Te lleva al triaje, que encamina la llamada con lo que el cliente ya ha dicho, sin saludar ni repetir preguntas. NO la uses si en el mismo turno se queja del minibús (eso es ESCALADO), para una duda del alquiler (consultas_alquiler), para una oficina que no es de aeropuerto (informacion_oficina) ni para transferir (transfer_to_human_agent). Sirve a cualquier hora, también en modo virtual y con gestión cerrada. No digas nada antes ni después: la herramienta continúa la conversación.

**Parámetros:**
- `motivo` (obligatorio): Por qué cambias de módulo: lo que el cliente pide ahora, en una frase corta, con lo que ya ha dicho y sin datos personales (ni nombre, ni reserva, ni matrícula, ni correo, ni teléfono).

### 2. `volver_al_triaje` en Información de oficina

**Descripción:** Úsala cuando el cliente pide otra gestión que no es de oficinas, ni una duda del alquiler, ni el minibús. Te lleva al triaje, que encamina la llamada con lo que el cliente ya ha dicho, sin saludar ni repetir preguntas. NO la uses para una duda del alquiler (consultas_alquiler), para el minibús o el punto de encuentro de un aeropuerto (buscar_punto_de_encuentro) ni para transferir (transfer_to_human_agent). Sirve a cualquier hora, también en modo virtual y con gestión cerrada. No digas nada antes ni después: la herramienta continúa la conversación.

**Parámetros:**
- `motivo` (obligatorio): Por qué cambias de módulo: lo que el cliente pide ahora, en una frase corta, con lo que ya ha dicho y sin datos personales (ni nombre, ni reserva, ni matrícula, ni correo, ni teléfono).

### 3. `volver_al_triaje` en Prolongación

**Descripción:** Úsala cuando el cliente pide el minibús o el punto de encuentro de un aeropuerto, u otra gestión que no es de su alquiler. Te lleva al triaje, que encamina la llamada con lo que el cliente ya ha dicho, sin saludar ni repetir preguntas. NO la uses para prolongar o para una duda del alquiler (eso es de aquí: buscar_respuesta), para el horario o la dirección de una oficina (informacion_oficina) ni para transferir (transfer_to_human_agent). Sirve a cualquier hora, también en modo virtual y con gestión cerrada. No digas nada antes ni después: la herramienta continúa la conversación.

**Parámetros:**
- `motivo` (obligatorio): Por qué cambias de módulo: lo que el cliente pide ahora, en una frase corta, con lo que ya ha dicho y sin datos personales (ni nombre, ni reserva, ni matrícula, ni correo, ni teléfono).

### 4. `volver_al_triaje` en Consultas del alquiler

**Descripción:** Úsala cuando el cliente pide otra gestión que no es una duda del alquiler. Te lleva al triaje, que encamina la llamada con lo que el cliente ya ha dicho, sin saludar ni repetir preguntas. NO la uses para una duda del alquiler (buscar_respuesta), para prolongar (prolongar_alquiler), para una oficina (informacion_oficina), para el minibús o el punto de encuentro (buscar_punto_de_encuentro) ni para transferir (transfer_to_human_agent). Sirve a cualquier hora, también en modo virtual y con gestión cerrada. No digas nada antes ni después: la herramienta continúa la conversación.

**Parámetros:**
- `motivo` (obligatorio): Por qué cambias de módulo: lo que el cliente pide ahora, en una frase corta, con lo que ya ha dicho y sin datos personales (ni nombre, ni reserva, ni matrícula, ni correo, ni teléfono).

### 5. `informacion_oficina` en Punto de encuentro

**Descripción:** Úsala cuando el cliente quiera saber el horario o la dirección de una oficina de Centauro que no es de aeropuerto (estación o ciudad), cómo llegar a ella o dónde se devuelve el coche en ella. Sirve a cualquier hora, también en modo virtual. NO la uses para el minibús, el punto de encuentro ni el horario o la devolución en un aeropuerto: eso es de aquí. Devolver el coche antes de tiempo o en otra oficina distinta de la del contrato es una duda del alquiler: consultas_alquiler con el tema devolucion. No digas nada antes ni después: la herramienta continúa la conversación.

**Parámetros:**
- `motivo` (obligatorio): Por qué cambias de módulo: lo que el cliente pide ahora, en una frase corta, con lo que ya ha dicho y sin datos personales (ni nombre, ni reserva, ni matrícula, ni correo, ni teléfono).
- `tema` (obligatorio): Lo que quiere saber el cliente. Valores permitidos EXACTOS: "horario" (horario de la oficina), "como_llegar" (cómo llegar a una oficina de estación o de ciudad para recoger el coche), "devolucion" (dónde devolver el coche). Si pregunta por varias cosas, pon la primera que haya pedido.
- `oficina` (opcional): La oficina, ciudad, estación o aeropuerto tal como lo ha dicho el cliente (por ejemplo: Málaga estación, Atocha, Madrid, Alicante aeropuerto). Si el cliente todavía no lo ha dicho, OMITE este parámetro por completo: no lo envíes vacío ni con valores como "desconocida". Nunca lo deduzcas ni lo preguntes solo para rellenarlo: la herramienta se encarga de identificar la oficina.

### 6. `buscar_punto_de_encuentro` en Información de oficina

**Descripción:** Úsala cuando el cliente pregunta por el minibús, por el punto de encuentro (también el de vuelta) o por cómo llegar del aeropuerto a la oficina de Centauro, y ya sabes en qué aeropuerto está. También si pregunta a qué hora pasa el minibús, si hay minibús a una hora concreta o por el de vuelta: no lo contestes tú, aunque sea fuera del horario de la oficina. La herramienta continúa la conversación: da el punto de encuentro o avisa de que la oficina de ese aeropuerto ya ha cerrado. Sirve a cualquier hora, también en modo virtual. NO la uses si se queja de que el minibús no llega, se ha ido sin él o lleva tiempo esperando (salvo que lleve menos de diez minutos): eso se transfiere a la cola minibus, salvo en modo virtual: entonces no transfieras; dile que a esta hora no hay compañeros y que puede volver a llamar a partir de las ocho de la mañana. NO la uses para el horario, la dirección o la devolución en una oficina: eso es de aquí. Si todavía no sabes el aeropuerto, pregúntalo antes. Nunca preguntes la terminal solo para poder llamarla: es opcional. No digas nada antes ni después.

**Parámetros:**
- `motivo` (obligatorio): Por qué cambias de módulo: lo que el cliente pide ahora, en una frase corta, con lo que ya ha dicho y sin datos personales (ni nombre, ni reserva, ni matrícula, ni correo, ni teléfono).
- `aeropuerto` (obligatorio): Nombre del aeropuerto donde se encuentra el cliente, tal como lo ha dicho (por ejemplo: Valencia, Rodas, Lisboa, Madrid).
- `terminal` (opcional): Terminal o puerta de salida, SOLO si el cliente la ha mencionado espontáneamente. Si el cliente no ha dicho la terminal, OMITE este parámetro por completo: no lo incluyas en la llamada y no lo envíes como texto vacío, ni con guiones, ni con valores como "no indicada" o "desconocida". Nunca deduzcas ni inventes una terminal, y nunca se la preguntes al cliente solo para rellenar este campo.

### 7. `prolongar_alquiler` en Consultas del alquiler

**Descripción:** Úsala cuando el cliente quiere prolongar el alquiler que tiene en curso o devolver el coche más tarde, cuando la web no le deja prolongar, cuando no recuerda o no tiene la contraseña de su área de cliente en la web, o cuando su coche es de una aseguradora, de un taller o de su empresa. Si solo pregunta una condición (la penalización, si hay margen), no la uses: respóndela con buscar_respuesta. Sirve a cualquier hora, también en modo virtual y con gestión cerrada. No digas nada antes: la herramienta continúa la conversación.

**Parámetros:**
- `motivo` (obligatorio): Por qué cambias de módulo: lo que el cliente pide ahora, en una frase corta, con lo que ya ha dicho y sin datos personales (ni nombre, ni reserva, ni matrícula, ni correo, ni teléfono).
- `situacion` (obligatorio): Lo que necesita el cliente. Valores permitidos EXACTOS: "prolongar" (quedarse el coche más días), "devolver_tarde" (devolverlo más tarde el mismo día), "web_no_deja" (la web no le deja prolongar), "contrasena" (no recuerda o no tiene la contraseña del área de cliente), "aseguradora_empresa" (coche de aseguradora, de taller o de empresa). Si dice varias cosas, pon la primera.

### 8. `informacion_oficina` en Prolongación

**Descripción:** Úsala cuando el cliente quiera saber el horario de una oficina de Centauro, cómo llegar a una oficina de estación o de ciudad, o dónde se devuelve el coche en una oficina. Sirve a cualquier hora, también en modo virtual. NO la uses para el minibús ni para el punto de encuentro de un aeropuerto (volver_al_triaje). Devolver el coche antes de tiempo o en otra oficina distinta de la del contrato es una duda del alquiler: buscar_respuesta con el tema devolucion. No digas nada antes ni después: la herramienta continúa la conversación.

**Parámetros:**
- `motivo` (obligatorio): Por qué cambias de módulo: lo que el cliente pide ahora, en una frase corta, con lo que ya ha dicho y sin datos personales (ni nombre, ni reserva, ni matrícula, ni correo, ni teléfono).
- `tema` (obligatorio): Lo que quiere saber el cliente. Valores permitidos EXACTOS: "horario" (horario de la oficina), "como_llegar" (cómo llegar a una oficina de estación o de ciudad para recoger el coche), "devolucion" (dónde devolver el coche). Si pregunta por varias cosas, pon la primera que haya pedido.
- `oficina` (opcional): La oficina, ciudad, estación o aeropuerto tal como lo ha dicho el cliente (por ejemplo: Málaga estación, Atocha, Madrid, Alicante aeropuerto). Si el cliente todavía no lo ha dicho, OMITE este parámetro por completo: no lo envíes vacío ni con valores como "desconocida". Nunca lo deduzcas ni lo preguntes solo para rellenarlo: la herramienta se encarga de identificar la oficina.

La frase «También si pregunta a qué hora pasa el minibús…» de la herramienta 6 se añadió el 19/10/2026 a las 23:06, en
la vuelta de arreglos de los Pasos 3 a 5 (ADV-12).

## Evals (Pasos 4 y 5)

Carpeta «Bot único · Saltos» (`01a155f0-c997-7c47-9d1e-6aceb2c7b093`), 31 evals, en el módulo de origen de cada salto
(las SALTO-ENTRADA, en el de destino). `create` no guarda `folder_id` ni devuelve el id: se archivan después con
`update` y los ids salen de `list`.

| Eval | Nodo | id | Espera |
|---|---|---|---|
| SALTO-01a | Punto de encuentro | `01a155f2-2063-7a8c-aefa-d5564684ec2a` | `volver_al_triaje` |
| SALTO-01b | Punto de encuentro | `01a155f2-84e9-7359-b0c7-4002a7bb4ef9` | `volver_al_triaje` |
| SALTO-02a | Información de oficina | `01a155f2-877f-7292-829f-ef5736e62b4f` | `volver_al_triaje` |
| SALTO-02b | Información de oficina | `01a155f2-8ad6-7ea2-9c4e-e3ea53afaf04` | `volver_al_triaje` |
| SALTO-03a | Prolongación | `01a155f3-2db3-7595-b348-adfdb7364c38` | `volver_al_triaje` |
| SALTO-03b | Prolongación | `01a155f3-3075-7093-9a3c-8eff01f84cec` | `volver_al_triaje` |
| SALTO-04a | Consultas del alquiler | `01a155f3-32e5-78a4-a530-dcd7f1f072e3` | `volver_al_triaje` |
| SALTO-04b | Consultas del alquiler | `01a155f3-3638-7807-99db-89b02d7701f5` | `volver_al_triaje` |
| SALTO-05a | Punto de encuentro | `01a155f3-389f-71a5-a5a6-0d1dbec3e8a1` | `informacion_oficina` tema=horario |
| SALTO-05b | Punto de encuentro | `01a155f3-3b1f-73a8-83ff-ed9ca832185a` | `informacion_oficina` tema=como_llegar |
| SALTO-06a | Información de oficina | `01a155f3-f200-7390-b7e7-92efbf49eb6a` | `buscar_punto_de_encuentro` aeropuerto=Sevilla |
| SALTO-06b | Información de oficina | `01a155f3-f47f-7c75-bd0e-0e8048cde4fe` | `buscar_punto_de_encuentro` aeropuerto=Bilbao |
| SALTO-07a | Consultas del alquiler | `01a155f3-f6c6-78c0-9b74-e6a2e668d7dd` | `prolongar_alquiler` situacion=prolongar |
| SALTO-07b | Consultas del alquiler | `01a155f3-f916-71d0-a63e-d1ca486807aa` | `prolongar_alquiler` situacion=web_no_deja |
| SALTO-08a | Prolongación | `01a155f3-fbfc-75e5-83b6-f68e272fb175` | `informacion_oficina` tema=horario |
| SALTO-08b | Prolongación | `01a155f3-fef6-7da2-af65-aef146368f06` | `informacion_oficina` tema=devolucion |
| SALTO-09a | Punto de encuentro | `01a155f4-0232-7afc-8cf6-dc2c175b90c9` | `consultas_alquiler` tema=cargos_y_reembolsos |
| SALTO-09b | Punto de encuentro | `01a155f4-b0f8-7a59-9dc8-a997e90c5365` | `consultas_alquiler` tema=durante_el_alquiler |
| SALTO-10a | Información de oficina | `01a155f4-b34c-72d4-8d51-c37bcd4dd6e0` | `consultas_alquiler` tema=requisitos |
| SALTO-10b | Información de oficina | `01a155f4-b5c4-72ec-a4d1-0460ae051646` | `consultas_alquiler` tema=reserva_no_iniciada |
| SALTO-11a | Consultas del alquiler | `01a155f4-b84d-71b9-881e-d39805e94a13` | `buscar_punto_de_encuentro` aeropuerto=Málaga |
| SALTO-11b | Consultas del alquiler | `01a155f4-ba8d-74b3-a747-1d656210cc02` | `buscar_punto_de_encuentro` aeropuerto=Valencia |
| SALTO-12a | Consultas del alquiler | `01a155f4-bde5-7725-bbb9-33d92773eb89` | `informacion_oficina` tema=horario |
| SALTO-12b | Consultas del alquiler | `01a155f4-c0c5-76b3-9f2b-97a2d3d46614` | `informacion_oficina` tema=como_llegar |
| SALTO-ENTRADA-TR | Triaje | `01a155f5-8806-7b44-8540-8d1d3970cb07` | `transfer_to_human_agent` cola=nueva_reserva, motivo_transferencia=nueva_reserva |
| SALTO-ENTRADA-PE | Punto de encuentro | `01a155f5-8a4a-7745-8851-d885ddf7238a` | sin herramienta |
| SALTO-ENTRADA-IO | Información de oficina | `01a155f5-8d8a-7790-a40e-892646d1085b` | sin herramienta |
| SALTO-ENTRADA-PR | Prolongación | `01a155f5-90b6-73a1-b529-48a7e0672776` | sin herramienta |
| SALTO-ENTRADA-CO | Consultas del alquiler | `01a155f5-92f7-7607-81cd-17c70ce1fded` | `buscar_respuesta` tema=cargos_y_reembolsos |
| SALTO-PING (crítica) | Consultas del alquiler | `01a155f5-953e-747a-897e-e527995decbf` | `transfer_to_human_agent` cola=minibus |
| SALTO-IDIOMA | Prolongación | `01a155f5-977f-7518-8ea2-6204ee41f9b9` | sin herramienta |

SALTO-01a, SALTO-02a y SALTO-03b se crearon con «quiero que borren mis datos de la cuenta de cliente» y se cambiaron en la
vuelta de arreglos por «tengo otra consulta distinta» (los módulos lo trataban, con razón, como gestión o como duda del
alquiler). Las transferencias (SALTO-ENTRADA-TR, SALTO-PING) llevan las cuatro `cola_*` y la nota del reintento.
