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

| Versión | Slug | version_id | Nombre / cambio | Estado (18/10/2026) |
|---|---|---|---|---|
| v1 | `veavliy3k6jx` | `01a14f1b-4eee-7f9c-8ec5-19600855e648` | `v1 · copia de Minibús ES v25` | Borrador, sin tocar (referencia). Sin bloquear. Sin números en el trigger |
| v2 | `x8xd0llbdp3j` | `01a14f1d-0387-70e5-a6ad-2b311a86224c` | `v2 · bot único: Triaje + 4 módulos` | Borrador en construcción (fork de la v1). Sin publicar |

Copia de los nodos de la v1 en `prompts/atencion-es/v1/` (un fichero por nodo; herramientas, transferencias y
Module Change agrupados). La v2 empieza igual que la v1 salvo la rama «Fallback» de «Entrada», que se borró.

Los **persistent_id** son iguales en la v1 y la v2 (y son los que van en las variables `{{persistent_id.variable}}`);
los **IDs de nodo** cambian de una versión a otra: localizar siempre por nombre.

### Flujo de nodos de la v2 (18/10/2026, tras la Tarea 10)

```
Inbound Call (sin líneas)
 └ Contexto de la llamada           (Python; opcion_menu, idioma, modo virtual, gestion_abierta, festivo_nacional…)
   └ Resolver colas                 (Python; cola_* por idioma, URI SIP; Gestión siempre con su extensión)
     └ Entrada (Paths)              ← PENDIENTE DE QUITAR a mano (ver pendientes.md)
       └ Siempre (condición)
         └ Receive Customer Call    (agente de voz «Shuttle Prompt»)
             ├ Triaje               (prompt, raíz del agente; antes «Triaje y horario»)
             │   ├ buscar_punto_de_encuentro → Punto de encuentro
             │   ├ informacion_oficina       → Información de oficina
             │   ├ consultas_alquiler        → Consultas del alquiler
             │   ├ prolongar_alquiler        → Prolongación (Tarea 10)
             │   └ transfer_to_human_agent   → Preparar transferencia (Python) → ¿Transferir? (Paths)
             │                                   ├ Transferir → Initiate customer connection
             │                                   └ Fallback (vacía: no se transfiere)
             │      Punto de encuentro:  consultas_alquiler (→ Module Change → Consultas del alquiler),
             │                           transfer_to_human_agent → Initiate customer connection  (patrón v25)
             │      Información de oficina: consultas_alquiler (→ Module Change → Consultas del alquiler),
             │                           transfer_to_human_agent → Initiate customer connection  (patrón v25)
             │      Prolongación (Tarea 10, fast-gpt-5.4):
             │                           enviar_correo_contrasena → Comprobar correo (MCP consultar_reserva)
             │                                   → Decidir envío (Python) → Enviar correo (MCP enviar_reset_contrasena)
             │                                   → Resultado para el agente (Python)
             │                           pista_correo → Identificar al cliente (MCP consultar_reserva)
             │                                   → Pista del correo (Python, pista_correo.py)
             │                           buscar_respuesta → Buscar respuesta (Python, consultas_alquiler.py)
             │                           transfer_to_human_agent → Preparar transferencia → ¿Transferir?
             │                                   ├ Transferir → Initiate customer connection
             │                                   └ Fallback (vacía)
             │      Consultas del alquiler (antes «Prolongación y consultas»; Tarea 9):
             │                           buscar_respuesta → Buscar respuesta (Python, consultas_alquiler.py)
             │                           buscar_punto_de_encuentro (→ Module Change → Punto de encuentro)
             │                           informacion_oficina (→ Module Change → Información de oficina)
             │                           transfer_to_human_agent → Preparar transferencia → ¿Transferir?
             │                                   ├ Transferir → Initiate customer connection
             │                                   └ Fallback (vacía)
             └ Registrar resultado de la llamada (AI Extract, 29 campos)
               └ Registrar consultas del alquiler (AI Extract, 14 campos)
                 └ Preparar WhatsApp minibús (Python)
                   └ ¿Enviar WhatsApp? (Paths)
                       ├ Enviar → Enviar WhatsApp del punto de encuentro
                       └ Fallback (vacía)
```

Variable del workflow: `OPCION_PRUEBA` (id `01a14f5f-012a-7715-b762-8f7d4acf1724`), `ninguna` en los tres entornos
(HappyRobot no admite valores vacíos); con `prolongacion` en *development* una llamada web entra por la línea de
Prolongación.

La cadena objetivo del plan (Paso 5 de la Tarea 6) es Inbound Call → Contexto de la llamada → Resolver colas →
Receive Customer Call. **Hoy en la v2 queda «Entrada» + «Siempre» entre «Resolver colas» y «Receive Customer
Call»**: por API no se puede reenganchar el agente (borrar un nodo borra todo su subárbol; ver `pendientes.md`).

Nodos de la v2 (ID de nodo → persistent_id), por nombre:

| Nodo | ID en la v2 | persistent_id |
|---|---|---|
| Inbound Call | `01a14f1d-0391-742b-90a7-7b69d9a953d9` | `33c2681a-9160-413c-8010-e455bd4023c6` |
| Contexto de la llamada (antes «Calcular horario nocturno») | `01a14f1d-0393-7fb7-9e26-7687ebda282f` | `e51cd732-f403-4ef7-95d4-490347960a93` |
| Resolver colas (antes «Resolver colas por idioma») | `01a14f1d-0394-7f91-abea-664941d88ad0` | `081e2b5d-b260-41a6-bd2a-6f82b26193d1` |
| Entrada (Paths) | `01a14f1d-0392-7afe-b494-0165acee1a73` | `3380d3e5-8e28-4cd1-bc12-66646795e46c` |
| Siempre (condición de «Entrada») | `01a14f1d-039a-75a0-9197-ac48a7b70c5f` | `34d2bf66-5e03-4e89-b1dc-02c4d7f5b3af` |
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
| Consultas del alquiler (antes «Prolongación y consultas») | `01a14f1d-0397-7b22-b5ce-bcb398a7605e` | `38378785-0846-4920-b41a-583f7c5773fb` |
| buscar_respuesta (Consultas, Tarea 9) | `01a14fa1-5c34-7bff-9366-aa7e9e4e448a` | `01a14fa1-5c34-7bff-9366-aa7e9e4e448a` |
| Buscar respuesta (Python, Consultas) | `01a14fa1-5c44-7c37-821c-1d01c0bd41eb` | `01a14fa1-5c44-7c37-821c-1d01c0bd41eb` |
| transfer_to_human_agent (Consultas) | `01a14f1d-0399-7dbf-9f55-4977771a298f` | `fbe2e40e-4915-4f44-9bac-59c318862e97` |
| Preparar transferencia (Consultas) | `01a14fa7-1147-724b-af62-e10108d91bce` | `01a14fa7-1147-724b-af62-e10108d91bce` |
| ¿Transferir? (Paths, Consultas) | `01a14fa7-420e-78db-a46a-1afc6823c0ac` | `01a14fa7-420e-78db-a46a-1afc6823c0ac` |
| Transferir (condición, Consultas) | `01a14fa7-421d-7c4b-ab14-17edc7ed95df` | `01a14fa7-421d-7c4b-ab14-17edc7ed95df` |
| Initiate customer connection (Consultas; sustituye a `01a14f1d-0396-7a17-…`, borrado) | `01a14fa7-4228-7812-a6b7-aa42c035b190` | `01a14fa7-4228-7812-a6b7-aa42c035b190` |
| Registrar resultado de la llamada | `01a14f1d-0395-7611-80cf-234e9e9fcf11` | `aea14d45-81de-4a98-aaae-d45c89421f34` |
| Registrar consultas del alquiler | `01a14f1d-0396-7b8c-ac8b-76817e8d62e8` | `15bf240b-4db7-47cc-86c5-963eaf6955b3` |
| Preparar WhatsApp minibús | `01a14f1d-0394-7fed-89b7-f4b8a5e640aa` | `4bd059bb-837c-4242-845f-7fc802c0f937` |
| ¿Enviar WhatsApp? (Paths) | `01a14f1d-0392-7a3a-9987-9e9a6a9ab190` | `d7bea790-20cc-431d-b696-edd7f09b51e3` |
| Enviar WhatsApp del punto de encuentro | `01a14f1d-0395-7934-834b-0382a080f15d` | `cbb87a1f-4994-49ea-872b-501640029b45` |

**Tarea 9b (18/10/2026):** los dos «Preparar transferencia» (Triaje y Consultas) llevan la red de seguridad del modo
virtual (resultado `modo_virtual`, D-004) y «Buscar respuesta» el código regenerado tras C-005 (sin los teléfonos de
asistencia de otros países; «No digas que no está permitido» en la oficina cerrada). Los ids no cambian.

El Python de `buscar_respuesta` se llama **«Buscar respuesta»** (no «Consultas del alquiler», para no repetir el nombre
del prompt). **Aviso para la Tarea 10:** el nodo igual que se cree en Prolongación debe llevar el mismo nombre.

Modelos de la v1/v2 (heredados de la v25): Triaje, Punto de encuentro `fast-turbo-one` (gpt-4.1-fast); Información de
oficina `fast-gpt-4.1`; Prolongación y consultas `fast-gpt-5.4`; los dos extract `gpt-5.6-luna`. En la v2, Consultas
del alquiler pasa a `fast-gpt-4.1` (Tarea 9) y se confirma tras la comparación del spec §7.3 (Tarea 9c, D-005).
Prolongación (Tarea 10) usa `fast-gpt-5.4`, sin `initial_message`.

**Tarea 10 (18/10/2026):** el prompt «Prolongación» deja de ser provisional (21.978 caracteres; 21.580 tras la ronda de arreglos 1 del 19/10; copia en
`prompts/atencion-es/v2/prolongacion.md`) y lleva sus cuatro herramientas, creadas por API: la cadena del correo de
contraseña de Prolongaciones v12 (misma credencial «Centauro MCP» y mismo código), `pista_correo` (nueva, spec §5.7),
`buscar_respuesta` (Python «Buscar respuesta», el mismo código que Consultas) y la transferencia con el patrón de
Consultas. Detalle: `herramientas-prolongacion.md`, `enviar-correo-contrasena.md` y `pista-correo.md`.

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
