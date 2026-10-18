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

### Flujo de nodos de la v2 (18/10/2026)

```
Inbound Call (sin líneas)
 └ Calcular horario nocturno        (Python; idioma, modo virtual, gestion_abierta, telefono_dictado…)
   └ Resolver colas por idioma      (Python; cola_* por idioma, URI SIP)
     └ Entrada (Paths)              ← PENDIENTE DE QUITAR a mano (ver pendientes.md)
       └ Siempre (condición)
         └ Receive Customer Call    (agente de voz «Shuttle Prompt»)
             ├ Triaje y horario     (prompt, raíz del agente)
             │   ├ buscar_punto_de_encuentro → Punto de encuentro
             │   ├ informacion_oficina       → Información de oficina
             │   ├ consultas_alquiler        → Prolongación y consultas
             │   └ transfer_to_human_agent   → Initiate customer connection
             │      Punto de encuentro:  consultas_alquiler (→ Module Change → Prolongación y consultas),
             │                           transfer_to_human_agent → Initiate customer connection
             │      Información de oficina: consultas_alquiler (→ Module Change → Prolongación y consultas),
             │                           transfer_to_human_agent → Initiate customer connection
             │      Prolongación y consultas: buscar_punto_de_encuentro (→ Module Change → Punto de encuentro),
             │                           informacion_oficina (→ Module Change → Información de oficina),
             │                           transfer_to_human_agent → Initiate customer connection
             └ Registrar resultado de la llamada (AI Extract, 29 campos)
               └ Registrar consultas del alquiler (AI Extract, 14 campos)
                 └ Preparar WhatsApp minibús (Python)
                   └ ¿Enviar WhatsApp? (Paths)
                       ├ Enviar → Enviar WhatsApp del punto de encuentro
                       └ Fallback (vacía)
```

La cadena objetivo del plan (Paso 5 de la Tarea 6) es Inbound Call → Calcular horario nocturno → Resolver colas →
Receive Customer Call. **Hoy en la v2 queda «Entrada» + «Siempre» entre «Resolver colas» y «Receive Customer
Call»**: por API no se puede reenganchar el agente (borrar un nodo borra todo su subárbol; ver `pendientes.md`).

Nodos de la v2 (ID de nodo → persistent_id), por nombre:

| Nodo | ID en la v2 | persistent_id |
|---|---|---|
| Inbound Call | `01a14f1d-0391-742b-90a7-7b69d9a953d9` | `33c2681a-9160-413c-8010-e455bd4023c6` |
| Calcular horario nocturno | `01a14f1d-0393-7fb7-9e26-7687ebda282f` | `e51cd732-f403-4ef7-95d4-490347960a93` |
| Resolver colas por idioma | `01a14f1d-0394-7f91-abea-664941d88ad0` | `081e2b5d-b260-41a6-bd2a-6f82b26193d1` |
| Entrada (Paths) | `01a14f1d-0392-7afe-b494-0165acee1a73` | `3380d3e5-8e28-4cd1-bc12-66646795e46c` |
| Siempre (condición de «Entrada») | `01a14f1d-039a-75a0-9197-ac48a7b70c5f` | `34d2bf66-5e03-4e89-b1dc-02c4d7f5b3af` |
| Receive Customer Call | `01a14f1d-0394-725e-8b8f-bdd2b3ee34cc` | `300ae88d-ccb2-466c-a914-9f9090363a74` |
| Triaje y horario | `01a14f1d-0397-7925-af9e-b01d518bd921` | `c5a70932-117c-4360-9be8-adce260fe13e` |
| Punto de encuentro | `01a14f1d-0397-7c91-b2bc-a12efeed5595` | `a80fca22-b295-41e3-a735-a3c878af4eee` |
| Información de oficina | `01a14f1d-0396-717d-8b6f-52f789dbe9a3` | `0c60218b-8901-47bd-95de-40e0e1af1296` |
| Prolongación y consultas | `01a14f1d-0397-7b22-b5ce-bcb398a7605e` | `38378785-0846-4920-b41a-583f7c5773fb` |
| Registrar resultado de la llamada | `01a14f1d-0395-7611-80cf-234e9e9fcf11` | `aea14d45-81de-4a98-aaae-d45c89421f34` |
| Registrar consultas del alquiler | `01a14f1d-0396-7b8c-ac8b-76817e8d62e8` | `15bf240b-4db7-47cc-86c5-963eaf6955b3` |
| Preparar WhatsApp minibús | `01a14f1d-0394-7fed-89b7-f4b8a5e640aa` | `4bd059bb-837c-4242-845f-7fc802c0f937` |
| ¿Enviar WhatsApp? (Paths) | `01a14f1d-0392-7a3a-9987-9e9a6a9ab190` | `d7bea790-20cc-431d-b696-edd7f09b51e3` |
| Enviar WhatsApp del punto de encuentro | `01a14f1d-0395-7934-834b-0382a080f15d` | `cbb87a1f-4994-49ea-872b-501640029b45` |

Modelos de la v1/v2 (heredados de la v25): Triaje, Punto de encuentro `fast-turbo-one` (gpt-4.1-fast); Información de
oficina `fast-gpt-4.1`; Prolongación y consultas `fast-gpt-5.4`; los dos extract `gpt-5.6-luna`.

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
línea es justo lo que no se quiere hasta producción). La tabla línea → opción y los números se ponen al pasar a
producción (`pendientes.md`, puerta 0).
