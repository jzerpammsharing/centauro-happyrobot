# Workflows del caso Atención España

## Centauro Atención España

- **workflow_id:** `01a14f1b-4ea9-7827-a4f3-4cfb06a896f6`
- **slug del workflow:** `rntn68r0a8gh`
- **Carpeta:** Centauro (`019d8144-ce27-7aaf-b9e5-21d006083063`)
- **Origen:** duplicado de Minibús ES (`019f7594-2cce-7eed-b995-dd9ea64a1062`), versión v25 (`k2in5n9kk01x`,
  version_id `01a14054-0eaf-73b5-af31-1fc40bfcd3cc`, 37 nodos). Creado el 18/10/2026.
- **Editor de la v2:** `https://platform.eu.happyrobot.ai/mutuamobility/workflows/rntn68r0a8gh/editor/x8xd0llbdp3j`
- Flujo, módulos, herramientas y extract: spec `specs/2026-10-18-bot-unico-arquitectura.md` (§5). Qué copió el
  duplicado y qué no: `pendientes.md` (sección «Comprobaciones de la Tarea 6»).

### Versiones

| Versión | Slug | version_id | Nombre / cambio | Estado |
|---|---|---|---|---|
| v1 | `veavliy3k6jx` | `01a14f1b-4eee-7f9c-8ec5-19600855e648` | `v1 · copia de Minibús ES v25` | Borrador, sin tocar (referencia). Sin bloquear. Sin números en el trigger |
| v2 | `x8xd0llbdp3j` | `01a14f1d-0387-70e5-a6ad-2b311a86224c` | `v2 · bot único: Triaje + 4 módulos` | Construida (Tareas 8 a 16 y R35); sin publicar; puerta 0 pendiente. 87 nodos (comprobado con `get_workflows` el 20/10/2026 tras R10 y R42; con R35 eran 90: 5 prompt, 34 action, 13 condition, 26 tool, 12 module-change, menos «Entrada», «Siempre» y «Registrar consultas del alquiler») |

Copia de los nodos de la v1 en `prompts/atencion-es/v1/` (un fichero por nodo; herramientas, transferencias y
Module Change agrupados). La v2 empieza igual que la v1 salvo que no tiene el Paths «Entrada» (con «Siempre» y «Fallback») ni «Registrar consultas del alquiler» (R10 y R42, 20/10/2026).

Los **persistent_id** son iguales en la v1 y la v2 (y son los que van en las variables `{{persistent_id.variable}}`);
los **IDs de nodo** cambian de una versión a otra: localizar siempre por nombre.

**Estado de la v2 (20/10/2026): construida, sin publicar; puerta 0 pendiente.** Comprobada contra
`get_workflows` (87 nodos tras R10 y R42): todos están en el árbol, en la tabla o en `saltos.md`.

### Flujo de nodos de la v2

```
Inbound Call (sin líneas)
 └ Contexto de la llamada           (Python; opcion_menu, idioma, modo virtual, gestion_abierta, festivo_nacional…)
   └ Resolver colas                 (Python; cola_* por idioma, URI SIP; Gestión siempre con su extensión)
     └ Receive Customer Call    (agente de voz «Shuttle Prompt»)
         ├ Triaje               (prompt, raíz del agente; antes «Triaje y horario»)
         │   ├ buscar_punto_de_encuentro → Punto de encuentro
         │   ├ informacion_oficina       → Información de oficina
         │   ├ consultas_alquiler        → Consultas del alquiler
         │   ├ prolongar_alquiler        → Prolongación (Tarea 10)
         │   └ transfer_to_human_agent   → Preparar transferencia (Python) → ¿Transferir? (Paths)
         │                                   ├ Transferir → Initiate customer connection
         │                                   └ Fallback (vacía: no se transfiere)
         │      Punto de encuentro (Tarea 11, fast-turbo-one; aviso de oficina cerrada por código, D-012):
         │                           estado_oficina → Estado de la oficina (Python, estado_oficina.py; Tarea 15b)
         │                           consultas_alquiler (→ Module Change → Consultas del alquiler),
         │                           informacion_oficina, volver_al_triaje (Tarea 12; → Module Change, saltos.md),
         │                           transfer_to_human_agent → Preparar transferencia → ¿Transferir? (Tarea R35)
         │                                   ├ Transferir → Initiate customer connection
         │                                   └ Fallback (vacía)
         │      Información de oficina (Tarea 11, fast-gpt-4.1):
         │                           consultas_alquiler (→ Module Change → Consultas del alquiler),
         │                           buscar_punto_de_encuentro, volver_al_triaje (Tarea 12; → Module Change),
         │                           transfer_to_human_agent → Preparar transferencia → ¿Transferir? (Tarea R35)
         │                                   ├ Transferir → Initiate customer connection
         │                                   └ Fallback (vacía)
         │      Prolongación (Tarea 10, fast-gpt-5.4):
         │                           enviar_correo_contrasena → Comprobar correo (MCP consultar_reserva)
         │                                   → Decidir envío (Python) → Enviar correo (MCP enviar_reset_contrasena)
         │                                   → Resultado para el agente (Python)
         │                           pista_correo → Identificar al cliente (MCP consultar_reserva)
         │                                   → Pista del correo (Python, pista_correo.py)
         │                           buscar_respuesta → Buscar respuesta (Python, consultas_alquiler.py)
         │                           informacion_oficina, volver_al_triaje (Tarea 12; → Module Change)
         │                           transfer_to_human_agent → Preparar transferencia → ¿Transferir?
         │                                   ├ Transferir → Initiate customer connection
         │                                   └ Fallback (vacía)
         │      Consultas del alquiler (antes «Prolongación y consultas»; Tarea 9):
         │                           buscar_respuesta → Buscar respuesta (Python, consultas_alquiler.py)
         │                           buscar_punto_de_encuentro (→ Module Change → Punto de encuentro)
         │                           informacion_oficina (→ Module Change → Información de oficina)
         │                           prolongar_alquiler, volver_al_triaje (Tarea 12; → Module Change)
         │                           transfer_to_human_agent → Preparar transferencia → ¿Transferir?
         │                                   ├ Transferir → Initiate customer connection
         │                                   └ Fallback (vacía)
         └ Registrar resultado de la llamada (AI Extract único, 46 campos; Tarea 13)
           └ Preparar WhatsApp minibús (Python; cuelga de aquí desde R42, 20/10/2026)
             └ ¿Enviar WhatsApp? (Paths)
                 ├ Enviar → Enviar WhatsApp del punto de encuentro
                 └ Fallback (vacía)
```

Variable del workflow: `OPCION_PRUEBA` (id `01a14f5f-012a-7715-b762-8f7d4acf1724`), `ninguna` en los tres entornos
(HappyRobot no admite valores vacíos); con `prolongacion` en *development* una llamada web entra por la línea de
Prolongación. `HORA_PRUEBA` (id `01a15787-36ac-782d-9f54-1353c934de58`, Tarea 16, D-014), `ninguna` en los tres
entornos: solo la lee «Estado de la oficina»; las evals la ponen a `HH:MM` para no depender del reloj.

La cadena de la v2 es Inbound Call → Contexto de la llamada → Resolver colas → Receive Customer Call. **R10 hecho el
20/10/2026:** el responsable quitó en el editor el Paths «Entrada» y su condición «Siempre»; «Receive Customer Call» cuelga
directamente de «Resolver colas» (por API no se podía: borrar un nodo borra su subárbol; ver `pendientes.md`).

Nodos de la v2 (ID de nodo → persistent_id), por nombre:

| Nodo | ID en la v2 | persistent_id |
|---|---|---|
| Inbound Call | `01a14f1d-0391-742b-90a7-7b69d9a953d9` | `33c2681a-9160-413c-8010-e455bd4023c6` |
| Contexto de la llamada (antes «Calcular horario nocturno») | `01a14f1d-0393-7fb7-9e26-7687ebda282f` | `e51cd732-f403-4ef7-95d4-490347960a93` |
| Resolver colas (antes «Resolver colas por idioma») | `01a14f1d-0394-7f91-abea-664941d88ad0` | `081e2b5d-b260-41a6-bd2a-6f82b26193d1` |
| Receive Customer Call | `01a14f1d-0394-725e-8b8f-bdd2b3ee34cc` | `300ae88d-ccb2-466c-a914-9f9090363a74` |
| Triaje (antes «Triaje y horario») | `01a14f1d-0397-7925-af9e-b01d518bd921` | `c5a70932-117c-4360-9be8-adce260fe13e` |
| prolongar_alquiler (herramienta del Triaje, Tarea 8) | `01a14f69-b092-7e6d-9203-c968520c1670` | `01a14f69-b092-7e6d-9203-c968520c1670` |
| Prolongación (prompt; creado provisional en la Tarea 8, completo en la Tarea 10) | `01a14f69-b09d-7689-ad9e-8e8de0fd6fb4` | `01a14f69-b09d-7689-ad9e-8e8de0fd6fb4` |
| enviar_correo_contrasena (Prolongación, Tarea 10) | `01a150c7-08df-73fd-abac-19c873b9533d` | `01a150c7-08df-73fd-abac-19c873b9533d` |
| Comprobar correo (consultar_reserva) | `01a150c7-08ea-725d-a22c-f6dd3d5161d4` | `01a150c7-08ea-725d-a22c-f6dd3d5161d4` |
| Decidir envío | `01a150c7-08fd-7f91-9dc8-5b5d5290896e` | `01a150c7-08fd-7f91-9dc8-5b5d5290896e` |
| Enviar correo (enviar_reset_contrasena) | `01a150c7-090c-7f7b-b5f7-38aa1b1614d9` | `01a150c7-090c-7f7b-b5f7-38aa1b1614d9` |
| Resultado para el agente | `01a150c7-091b-7abf-a101-539b1b7ec049` | `01a150c7-091b-7abf-a101-539b1b7ec049` |
| pista_correo (Prolongación, Tarea 10) | `01a150c7-0928-79dc-a21c-4d9348ca038d` | `01a150c7-0928-79dc-a21c-4d9348ca038d` |
| Identificar al cliente (consultar_reserva) | `01a150c7-0930-723c-89d9-eaeb76a0599e` | `01a150c7-0930-723c-89d9-eaeb76a0599e` |
| Pista del correo | `01a150c7-0940-76a7-8129-f132e4373895` | `01a150c7-0940-76a7-8129-f132e4373895` |
| buscar_respuesta (Prolongación) | `01a150c9-677e-791b-8f74-957f60586f02` | `01a150c9-677e-791b-8f74-957f60586f02` |
| Buscar respuesta (Python, Prolongación) | `01a150c9-6786-7e05-95c4-8007aa1e06d4` | `01a150c9-6786-7e05-95c4-8007aa1e06d4` |
| transfer_to_human_agent (Prolongación) | `01a150ca-b67d-726a-845b-19c18b2e891e` | `01a150ca-b67d-726a-845b-19c18b2e891e` |
| Preparar transferencia (Prolongación) | `01a150ca-b684-7698-a2ff-ccdefe784483` | `01a150ca-b684-7698-a2ff-ccdefe784483` |
| ¿Transferir? (Paths, Prolongación) | `01a150ca-dc54-7efe-8af0-9eab480b758a` | `01a150ca-dc54-7efe-8af0-9eab480b758a` |
| Transferir (condición, Prolongación) | `01a150ca-dc5d-7979-b66d-fa2f4033c5b6` | `01a150ca-dc5d-7979-b66d-fa2f4033c5b6` |
| Initiate customer connection (Prolongación; `outside_agent_transfer` false) | `01a150ca-dc8b-73ca-84c2-08eca941b971` | `01a150ca-dc8b-73ca-84c2-08eca941b971` |
| transfer_to_human_agent (Triaje) | `01a14f1d-0397-721d-9dab-ad0e44f6e642` | `17c682a0-82d2-42f6-88fa-817d8cba0783` |
| Preparar transferencia (Triaje) | `01a14f64-277b-7226-8e39-a8ef0274949f` | `01a14f64-277b-7226-8e39-a8ef0274949f` |
| ¿Transferir? (Paths, Triaje) | `01a14f66-5245-7cb6-9718-59dd25ecc3f5` | `01a14f66-5245-7cb6-9718-59dd25ecc3f5` |
| Transferir (condición) | `01a14f66-524e-78a8-a01b-fd9c184bbe1d` | `01a14f66-524e-78a8-a01b-fd9c184bbe1d` |
| Initiate customer connection (Triaje; sustituye a `b4439401-…`, borrado) | `01a14f66-5252-70a4-81ad-fa8d1cc6b438` | `01a14f66-5252-70a4-81ad-fa8d1cc6b438` |
| Punto de encuentro | `01a14f1d-0397-7c91-b2bc-a12efeed5595` | `a80fca22-b295-41e3-a735-a3c878af4eee` |
| Información de oficina | `01a14f1d-0396-717d-8b6f-52f789dbe9a3` | `0c60218b-8901-47bd-95de-40e0e1af1296` |
| estado_oficina (Punto de encuentro, Tarea 15b) | `01a1575e-923d-7deb-8a35-da450582d445` | = ID de nodo |
| → Estado de la oficina (Python) | `01a1575e-9248-71bc-ac3d-1dc0666e3a92` | = ID de nodo |
| consultas_alquiler (Punto de encuentro) | `01a14f1d-0398-7a4b-84e7-313e054df714` | `3f1c2be8-8768-455f-895b-047063ea7938` |
| transfer_to_human_agent (Punto de encuentro; parámetros nuevos en la Tarea 11, `message` de D-014 en la Tarea R35) | `01a14f1d-0398-75cb-939a-e2f512c94a01` | `00435498-eccf-4110-9cf1-eb17821af3ed` |
| Preparar transferencia (Punto de encuentro, Tarea R35) | `01a15973-c0e4-7eb3-8c1e-3931e73efcb1` | = ID de nodo |
| ¿Transferir? (Paths, Punto de encuentro) | `01a15974-0bf6-75fe-8fb3-391b0f2c7095` | = ID de nodo |
| Transferir (condición, Punto de encuentro) | `01a15974-0c05-701a-9d1e-8b1779473893` | = ID de nodo |
| Initiate customer connection (Punto de encuentro; sustituye al de la v25 `01a14f1d-0396-7961-…`, que borró el responsable; `outside_agent_transfer` false) | `01a15974-0c0d-722c-94ca-38fb6aad6ae1` | = ID de nodo |
| consultas_alquiler (Información de oficina) | `01a14f1d-0398-71cd-be10-a50ab91d1f5d` | `6edd13ac-b226-4d1c-87dc-748b46ce5638` |
| transfer_to_human_agent (Información de oficina; parámetros nuevos en la Tarea 11, `message` de D-014 en la Tarea R35) | `01a14f1d-0399-7faf-a630-5c199b3e3efc` | `62c5b6dd-5dde-4b3a-9a93-adb638c0bd66` |
| Preparar transferencia (Información de oficina, Tarea R35) | `01a15973-c373-7e08-9265-75a323398201` | = ID de nodo |
| ¿Transferir? (Paths, Información de oficina) | `01a15974-0f1c-7db1-8128-1182eab1eb18` | = ID de nodo |
| Transferir (condición, Información de oficina) | `01a15974-0f2b-7f09-9657-cc6934a0a05c` | = ID de nodo |
| Initiate customer connection (Información de oficina; sustituye al de la v25 `01a14f1d-0396-788f-…`, que borró el responsable; `outside_agent_transfer` false) | `01a15974-0f32-7195-bc20-40ffed8c52da` | = ID de nodo |
| Consultas del alquiler (antes «Prolongación y consultas») | `01a14f1d-0397-7b22-b5ce-bcb398a7605e` | `38378785-0846-4920-b41a-583f7c5773fb` |
| buscar_respuesta (Consultas, Tarea 9) | `01a14fa1-5c34-7bff-9366-aa7e9e4e448a` | `01a14fa1-5c34-7bff-9366-aa7e9e4e448a` |
| Buscar respuesta (Python, Consultas) | `01a14fa1-5c44-7c37-821c-1d01c0bd41eb` | `01a14fa1-5c44-7c37-821c-1d01c0bd41eb` |
| transfer_to_human_agent (Consultas) | `01a14f1d-0399-7dbf-9f55-4977771a298f` | `fbe2e40e-4915-4f44-9bac-59c318862e97` |
| Preparar transferencia (Consultas) | `01a14fa7-1147-724b-af62-e10108d91bce` | `01a14fa7-1147-724b-af62-e10108d91bce` |
| ¿Transferir? (Paths, Consultas) | `01a14fa7-420e-78db-a46a-1afc6823c0ac` | `01a14fa7-420e-78db-a46a-1afc6823c0ac` |
| Transferir (condición, Consultas) | `01a14fa7-421d-7c4b-ab14-17edc7ed95df` | `01a14fa7-421d-7c4b-ab14-17edc7ed95df` |
| Initiate customer connection (Consultas; sustituye a `01a14f1d-0396-7a17-…`, borrado) | `01a14fa7-4228-7812-a6b7-aa42c035b190` | `01a14fa7-4228-7812-a6b7-aa42c035b190` |
| volver_al_triaje (Punto de encuentro, Tarea 12) | `01a155d9-5d9b-7fd6-bfaa-6b87ccd6ac42` | = ID de nodo |
| volver_al_triaje (Información de oficina, Tarea 12) | `01a155d9-5da4-74b3-a7c4-3bb6257242d6` | = ID de nodo |
| volver_al_triaje (Prolongación, Tarea 12) | `01a155d9-5da8-738a-8af4-ada5f82ebdd7` | = ID de nodo |
| volver_al_triaje (Consultas, Tarea 12) | `01a155d9-5dac-7449-b143-4392c795602f` | = ID de nodo |
| informacion_oficina (Punto de encuentro, Tarea 12) | `01a155d9-5db0-7106-ab47-43027e0f8647` | = ID de nodo |
| buscar_punto_de_encuentro (Información de oficina, Tarea 12) | `01a155d9-5db4-757d-ac17-fc1adb754b0f` | = ID de nodo |
| prolongar_alquiler (Consultas, Tarea 12) | `01a155d9-5db8-7b78-8ecd-d52451c7ed84` | = ID de nodo |
| informacion_oficina (Prolongación, Tarea 12) | `01a155d9-5dbb-704a-b119-2db7b00a6fa2` | = ID de nodo |
| Module Change (volver_al_triaje de Punto de encuentro → Triaje; creado en el editor) | `01a155e8-f3f3-7d25-a6cf-f788cbfee0b4` | = ID de nodo |
| Module Change (volver_al_triaje de Información de oficina → Triaje; creado en el editor) | `01a155ec-a9e8-733d-a286-a38da5f0b411` | = ID de nodo |
| Module Change (volver_al_triaje de Prolongación → Triaje; creado en el editor) | `01a155ec-37d2-7d99-b8b8-d4e83069c3ba` | = ID de nodo |
| Module Change (volver_al_triaje de Consultas → Triaje; creado en el editor) | `01a155ed-9634-753f-b55c-de35edd40c1d` | = ID de nodo |
| Module Change (informacion_oficina de Punto de encuentro → Información de oficina; creado en el editor) | `01a155e8-59fa-7a49-ba5b-ca96f22b2050` | = ID de nodo |
| Module Change (buscar_punto_de_encuentro de Información de oficina → Punto de encuentro; creado en el editor) | `01a155ec-dcfc-730e-9c8c-daa3bfbc19ae` | = ID de nodo |
| Module Change (prolongar_alquiler de Consultas → Prolongación; creado en el editor) | `01a155ee-138f-7765-954f-20ec0b421975` | = ID de nodo |
| Module Change (informacion_oficina de Prolongación → Información de oficina; creado en el editor) | `01a155ec-665d-7f0f-86b1-c070b229aa53` | = ID de nodo |
| Registrar resultado de la llamada | `01a14f1d-0395-7611-80cf-234e9e9fcf11` | `aea14d45-81de-4a98-aaae-d45c89421f34` |
| Preparar WhatsApp minibús | `01a14f1d-0394-7fed-89b7-f4b8a5e640aa` | `4bd059bb-837c-4242-845f-7fc802c0f937` |
| ¿Enviar WhatsApp? (Paths) | `01a14f1d-0392-7a3a-9987-9e9a6a9ab190` | `d7bea790-20cc-431d-b696-edd7f09b51e3` |
| Enviar WhatsApp del punto de encuentro | `01a14f1d-0395-7934-834b-0382a080f15d` | `cbb87a1f-4994-49ea-872b-501640029b45` |

**Nodos heredados de la v25 que la tabla anterior no recogía** (ID y persistent_id leídos con `get_node_details`, solo lectura, el 20/10/2026). Los Module Change a–d y las herramientas
de salto de las filas 1 a 8 están en `prompts/atencion-es/v2/saltos.md` (tabla de los 12 saltos):

| Nodo | ID en la v2 | persistent_id |
|---|---|---|
| informacion_oficina (herramienta del Triaje) | `01a14f1d-0399-7f31-a5b5-1d49d3808d0e` | `414b964d-bb29-428a-b9a1-92b1a3a8d6be` |
| buscar_punto_de_encuentro (herramienta del Triaje) | `01a14f1d-0397-715b-ab9d-56f6a46a9f60` | `72261523-5d3f-4830-ac36-67ab187d93ed` |
| consultas_alquiler (herramienta del Triaje) | `01a14f1d-0399-770c-9155-7167deaf5c99` | `414bdc8c-aacc-4125-b323-acc6a2ae3373` |
| consultas_alquiler (Información de oficina) | `01a14f1d-0398-71cd-be10-a50ab91d1f5d` | `6edd13ac-b226-4d1c-87dc-748b46ce5638` (Module Change `01a14f1d-039b-7e2a-90f5-a43135ba4453`: `9661e3bd-a18e-477b-8076-96c76caae15b`) |
| buscar_punto_de_encuentro (Consultas) | `01a14f1d-0398-793a-a4f6-4cc4ed3a45c4` | `eda4aa10-c99e-4319-b7ae-dbf5dc6db949` (Module Change `01a14f1d-039a-76cb-8e2c-fd908a63d1af`: `081b2d5c-d7cf-49b7-b0a1-70c82ee5aac7`) |
| informacion_oficina (Consultas) | `01a14f1d-0398-78ce-93ed-6d599a4dcad6` | `0be9b6d8-9353-41de-8049-c2e477ed6668` (Module Change `01a14f1d-039a-7490-9015-e42727f49b17`: `91b601ad-4782-44fb-955a-5bc42657c191`) |
| Module Change de consultas_alquiler (Punto de encuentro) | `01a14f1d-039b-7e6e-91ee-a0401da2c7e3` | `7f70daef-fdf6-4f51-86b0-43a61e626efc` |
| Enviar (condición de «¿Enviar WhatsApp?») | `01a14f1d-039a-7a17-8c7a-148dca107199` | `09675b8f-685e-43b7-abd9-15ce07f31077` |
| Fallback (vacía) de «¿Enviar WhatsApp?» | `01a14f1d-0399-703f-9f49-3f7e3137917e` | `5b4c35c5-2b47-47f0-b066-22eaf8c3ada3` |
| Fallback (vacía) de «¿Transferir?» del Triaje | `01a14f66-5245-7cb6-9718-59de12c52f87` | = ID de nodo |
| Fallback (vacía) de «¿Transferir?» de Consultas | `01a14fa7-420f-76f4-b6af-ab7cbfd553da` | = ID de nodo |
| Fallback (vacía) de «¿Transferir?» de Prolongación | `01a150ca-dc54-7efe-8af0-9eac1640d219` | = ID de nodo |
| Fallback (vacía) de «¿Transferir?» de Punto de encuentro (Tarea R35) | `01a15974-0bf6-75fe-8fb3-391c36751004` | = ID de nodo |
| Fallback (vacía) de «¿Transferir?» de Información de oficina (Tarea R35) | `01a15974-0f1c-7db1-8128-118349d27177` | = ID de nodo |

**Herramientas por módulo (26 tool):**
- Triaje (5): `buscar_punto_de_encuentro`, `informacion_oficina`, `consultas_alquiler`, `prolongar_alquiler`,
  `transfer_to_human_agent`.
- Punto de encuentro (5): `estado_oficina`, `consultas_alquiler`, `informacion_oficina`, `volver_al_triaje`,
  `transfer_to_human_agent`.
- Información de oficina (4): `consultas_alquiler`, `buscar_punto_de_encuentro`, `volver_al_triaje`,
  `transfer_to_human_agent`.
- Prolongación (6): `enviar_correo_contrasena`, `pista_correo`, `buscar_respuesta`, `informacion_oficina`,
  `volver_al_triaje`, `transfer_to_human_agent`.
- Consultas del alquiler (6): `buscar_respuesta`, `buscar_punto_de_encuentro`, `informacion_oficina`,
  `prolongar_alquiler`, `volver_al_triaje`, `transfer_to_human_agent`.

**Estado de la transferencia a 20/10/2026 (tras la Tarea R35):** los cinco módulos tienen la cadena «Preparar
transferencia» → «¿Transferir?» → «Initiate customer connection» (con su Fallback vacío), así que en todos actúan la
red de seguridad de Gestión cerrada y la del modo virtual. En Punto de encuentro e Información de oficina el
responsable borró en el editor los dos Transfer de la v25 y la cadena se creó por API el 20/10/2026 (R35 cerrado,
`pendientes.md`).

**Extract:** «Registrar resultado de la llamada» (`aea14d45-…`) es el único en uso (46 campos, D-010; desde la Tarea R35 lee el
`resultado` y el `transfer_succeeded` de las cinco cadenas de transferencia; detalle en
`prompts/atencion-es/v2/registrar-resultado.md`). «Registrar consultas del alquiler» se borró en el editor el
20/10/2026 (R42); «Preparar WhatsApp minibús» cuelga ahora de este extract.

**Module Change:** 12 (los 4 de la v25 y los 8 del editor), todos comprobados contra la tabla de `saltos.md`.

**Tarea 9b (18/10/2026):** los dos «Preparar transferencia» (Triaje y Consultas) llevan la red de seguridad del modo
virtual (resultado `modo_virtual`, D-004) y «Buscar respuesta» el código regenerado tras C-005 (sin los teléfonos de
asistencia de otros países; «No digas que no está permitido» en la oficina cerrada). Los ids no cambian.

El Python de `buscar_respuesta` se llama **«Buscar respuesta»** (no «Consultas del alquiler», para no repetir el nombre
del prompt). **Aviso para la Tarea 10:** el nodo igual que se cree en Prolongación debe llevar el mismo nombre.

Modelos de la v1/v2 (heredados de la v25): Triaje, Punto de encuentro `fast-turbo-one` (gpt-4.1-fast); Información de
oficina `fast-gpt-4.1`; Prolongación y consultas `fast-gpt-5.4`; los dos extract `gpt-5.6-luna`. En la v2, Consultas
del alquiler pasa a `fast-gpt-4.1` (Tarea 9) y se confirma tras la comparación del spec §7.3 (Tarea 9c, D-005).
Prolongación (Tarea 10) usa `fast-gpt-5.4`, sin `initial_message`.

**Tarea 10 (18/10/2026):** el prompt «Prolongación» deja de ser provisional (21.978 caracteres; 21.946 tras la ronda de arreglos 3 y 21.998 tras la ronda de arreglos 4 y 21.994 tras la 5, del 19/10; copia en
`prompts/atencion-es/v2/prolongacion.md`) y lleva sus cuatro herramientas, creadas por API: la cadena del correo de
contraseña de Prolongaciones v12 (misma credencial «Centauro MCP» y mismo código), `pista_correo` (nueva, spec §5.7),
`buscar_respuesta` (Python «Buscar respuesta», el mismo código que Consultas) y la transferencia con el patrón de
Consultas. Detalle: `herramientas-prolongacion.md`, `enviar-correo-contrasena.md` y `pista-correo.md`.

**Tarea 11 (19/10/2026):** «Punto de encuentro» (34.595 caracteres; 35.073 tras la ronda de arreglos 1, 35.489 tras la 2, 35.801 tras la 3, 36.159 tras la 4, 36.250 tras la 5 y 36.382 en la Tarea 12) e «Información de oficina» (33.210; 33.379; 33.571; 33.727; sin cambios en la 4 ni en la 5) llevan el
bloque de reglas comunes; Punto de encuentro, además, las LISTAS 1 a 4 de `nocturno_*` (aviso de oficina de
aeropuerto cerrada) y la sección de interrupciones de la v25. Modelos sin cambios. Copias en
`prompts/atencion-es/v2/punto-de-encuentro.md`, `informacion-de-oficina.md` y sus `herramientas-*.md`. Las dos
`transfer_to_human_agent` tienen ya `cola`, `motivo_transferencia` y `resumen_para_agente`, pero la cadena «Preparar
transferencia» → «¿Transferir?» → Transfer **no se creó entonces**: el borrado de los Transfer de la v25 lo rechazó el
sistema de permisos (`pendientes.md`, «Comprobaciones de la Tarea 11»); se creó en la Tarea R35. D-008.

**Tarea 12, Paso 1 (19/10/2026):** las 8 herramientas de salto (spec §5.6) creadas por API a las 22:27, sin hijo
(`message: none`, `motivo` obligatorio y los parámetros de la v25). Sus 8 Module Change los creó el responsable en el
editor el mismo día (12 en total, comprobados por API); tabla de los 12 saltos y lista exacta en `prompts/atencion-es/v2/saltos.md`. En Punto de encuentro, la queja y
el «enfadado o puede perder una conexión» llevan la excepción de PRIMERO (36.382 caracteres).

**Tarea 12, Pasos 3 a 5 (19/10/2026):** 12 Module Change comprobados por API. La descripción de
`buscar_punto_de_encuentro` de Información de oficina añade «a qué hora pasa el minibús… no lo contestes tú» (ADV-12).
31 evals en «Bot único · Saltos» (`saltos.md`, `informes/evals-v2.md`). La comprobación en una llamada queda para la
Tarea 17 (`pendientes.md`). Ronda de arreglos 2: viñeta de ESCALADO de Información de oficina y descripción de su
`consultas_alquiler` (D-009); el prompt pasa a 33.871 caracteres.

**Tarea 13 (19/10/2026):** «Registrar resultado de la llamada» pasa a ser el extract único del spec §5.12 (46 campos:
los 45 de la tabla y `origen_opcion`; GPT-5.6 Luna). Lee la transcripción, «Contexto de la llamada», los parámetros y
salidas de las herramientas de los cinco módulos (`cola`, `motivo_transferencia`, `resultado` de «Preparar
transferencia», `transfer_succeeded` de los cinco Transfer, `buscar_respuesta`, `enviar_correo_contrasena`,
`pista_correo` y las de salto) y el `callCount` de los 12 Module Change. «Preparar WhatsApp minibús» lee
`whatsapp_aceptado`, `punto_whatsapp` e `idioma_cliente` de este extract (`aea14d45-…`), y cuelga de él desde
el 20/10/2026 (R42 hecho en el editor; `pendientes.md`). En «Receive Customer Call»,
`transcription_context` ampliado y `business_hours_setting_name` vacío; la voz ya era solo «Pablo Galvez HR». Copias en
`prompts/atencion-es/v2/registrar-resultado.md` y `receive-customer-call.md`.

**Tarea 15b, Parte A (20/10/2026, R39, D-012):** Punto de encuentro tiene la herramienta `estado_oficina` con el
Python «Estado de la oficina» (`codigo/estado_oficina.py`). Las LISTAS 1 a 4 y las `nocturno_*` salen del prompt, que
pasa a 36.026 caracteres (36.382 antes). Copias en `punto-de-encuentro.md`, `herramientas-punto-de-encuentro.md` y
`estado-oficina.md`.

**Tarea 15b, Parte B (20/10/2026, R34, D-013):** en `transfer_to_human_agent` de Prolongación
(`01a150ca-b67d-…`) y de Consultas (`01a14f1d-0399-7dbf-…`), la descripción del `message` `ai` pide un aviso neutro con
Gestión cerrada. La del Triaje (`01a14f1d-0397-721d-…`) se probó y se dejó como estaba. Copias en
`herramientas-prolongacion.md`, `herramientas-consultas.md` y `herramientas-triaje.md`.

**Tarea 16, arreglos previos (20/10/2026, R45, D-014):** «Estado de la oficina» calcula con la hora del momento y el
horario concreto de cada oficina; sus entradas son `aeropuerto` y `hora_prueba` (`{{use_case_variables.HORA_PRUEBA}}`).
El aviso de `transfer_to_human_agent` de Prolongación y Consultas depende de la cola (neutro solo si la transferencia
puede no salir; con `asistencia`, el de siempre); lleva `gestion_abierta` y `modo_virtual`. Copias en
`estado-oficina.md`, `herramientas-punto-de-encuentro.md`, `herramientas-prolongacion.md` y `herramientas-consultas.md`.

**Tarea 16, pasada completa y ronda de arreglos (20/10/2026, D-015):** 285 evals ×3; la puerta 0 sigue pendiente
(bloqueos en `informes/evals-v2.md`). Cambiados en la v2: los dos nodos «Buscar respuesta» (código regenerado del
bloque de consultas), la descripción de `pista_correo` y los prompts de Punto de encuentro e Información de oficina.

**Tarea R35 (20/10/2026):** en Punto de encuentro e Información de oficina, bajo `transfer_to_human_agent`, se
crearon por API «Preparar transferencia» (código de `codigo/preparar_transferencia.py`), el Paths «¿Transferir?» con
«Transferir» y «Fallback», y el Transfer «Initiate customer connection» (`outside_agent_transfer: false`, whisper
«Llamada del asistente de atención.»). Los dos Transfer nuevos llevan `set_custom_output` (`transfer_succeeded`,
`error`, `transfer_completed_at`, `warm_handoff_pressed_one`, `warm_handoff_rep_picked_up`), igual que el de
Prolongación, para que el extract vea `transfer_succeeded` (su `test_node` falla sin llamada). El `message` de las dos herramientas pasa al aviso según la cola de D-014. El
extract lee las dos cadenas nuevas. Copias en `herramientas-punto-de-encuentro.md`,
`herramientas-informacion-de-oficina.md` y `registrar-resultado.md`.

### Cuidado al editar por API (duplicado)

- **El markdown que devuelve `get_node_details` en un prompt del duplicado conserva los `group_id` antiguos de
  Minibús ES** (`019fd418-…` en lugar de `e51cd732-…` para «Calcular horario nocturno»), aunque el JSON de Plate, que
  es lo que ejecuta el bot, apunta bien a los nodos nuevos. `fix_broken_vars` (simulación) no encontró referencias
  rotas. Al escribir un prompt con `prompt_md`, usar siempre `{{persistent_id.variable}}` con los persistent_id de
  esta tabla; **no pegar el markdown tal como sale** del nodo del duplicado.
- Las copias de `prompts/atencion-es/v1/` llevan los ids corregidos a los del workflow nuevo.

### Líneas conectadas

| Opción del menú | Idioma | Desde | Vuelta atrás |
|---|---|---|---|
| — | — | — | — |

Ninguna: la v1 y la v2 tienen el trigger «Inbound Call» sin números, a propósito (dos workflows con la misma
línea es justo lo que no se quiere hasta producción). Los números se ponen en el trigger al pasar a producción
(`pendientes.md`, puerta 0). La tabla línea → opción (`LINEAS` de «Contexto de la llamada») ya lleva en la v2 los
números reales de las cuatro líneas actuales (Tarea 8; en el repo siguen como marcadores).
