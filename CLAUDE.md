# CLAUDE.md — Voicebots Centauro en HappyRobot

Guía para trabajar en este proyecto con Claude Code, desde cualquier cuenta o equipo. Resume qué
hay, cómo se trabaja y dónde está cada cosa. **El histórico y el porqué de cada cambio** están en
`docs/decisiones.md`. Si algo cambia (versiones, extensiones, colas, decisiones), **actualiza este
fichero y el registro de decisiones en el mismo commit**.

> **Datos personales y secretos:** este repo NO contiene teléfonos, nombres de clientes o agentes,
> emails, números de reserva, matrículas ni credenciales. El run_id de HappyRobot sí se puede
> usar. Los conectores (HappyRobot, RingCentral) se autentican por OAuth en cada cuenta.

---

## 0. Arrancar en una cuenta o equipo nuevo

1. **Clonar** el repo (ver `README.md`). Rama `main`; un cambio = una rama + PR.
2. **Conectar los conectores MCP** en tu cuenta de Claude:
   - `hr` → HappyRobot (OAuth, workspace de Centauro).
   - `phone` → RingCentral (OAuth; solo lectura en este proyecto).
3. **Permisos:** `.claude/settings.json` pide confirmación antes de cualquier herramienta de
   HappyRobot que escriba (editar nodos, publicar versiones, lanzar o cancelar runs…).
4. **La memoria y los chats de Claude no viajan entre cuentas**: todo lo relevante tiene que estar
   aquí, en `docs/` o en `prompts/`.

## 1. Qué es

Voicebots de atención telefónica de **Centauro Rent a Car** construidos en **HappyRobot**, que
transfieren a las colas del call center en **RingCentral**.

| Bot | País | workflow_id | slug | Producción |
|---|---|---|---|---|
| Centauro Minibus SPAIN | ES | `019f7594-2cce-7eed-b995-dd9ea64a1062` | `t2vkrtiqj3ve` | v17 (`i0syf61bujsz`) |
| Centauro Minibus ITALY | IT | `01a03a65-3700-74c1-9c7b-e9c708833c4b` | `w13gsdcqkq9b` | Version 2 (`v9c38tkjwxae`) |
| Centauro Minibus Portugal | PT | `01a05977-3a33-76da-acb2-a757f3947cf9` | `i8kjlnu1m3zp` | v1 (`ql6fasoxl1ql`) |

Hay además un bot de **Prolongaciones**, que comparte colas con Minibús; está pendiente de
documentar aquí.

Detalle de cada workflow (flujo, nodos, versiones): `docs/workflows/minibus.md`.
Colas y extensiones de RingCentral: `docs/extensiones.md`.

## 2. Estructura del repo

| Ruta | Qué contiene |
|---|---|
| `CLAUDE.md` | Esta guía (contexto para Claude y para personas) |
| `docs/decisiones.md` | Registro de decisiones: fecha, qué, por qué, quién, versión afectada |
| `docs/workflows/` | Una ficha por workflow: flujo, nodos, versiones y cambios |
| `docs/extensiones.md` | Colas de RingCentral, menús y extensiones prohibidas |
| `docs/informes/` | Resumen mensual de los informes diarios de calidad |
| `docs/pendientes.md` | Incidencias abiertas y mejoras propuestas |
| `prompts/<bot>/<versión>/` | Copia de los prompts de cada versión publicada, para tener histórico y diff en git |
| `rutinas/` | Prompts de las rutinas programadas (p. ej. el informe diario) |
| `scripts/` | Utilidades de análisis (Python, solo lectura) |

## 3. Cómo se trabaja con los workflows

- **Nunca editar una versión publicada.** Se hace `manage_versions action=fork` y se trabaja en
  la copia. El nombre de la versión dice qué cambia: `v22 · v21 + horario de la cola de Gestión`.
- **Antes de publicar:**
  1. Guarda el prompt nuevo en `prompts/<bot>/<versión>/` (un fichero por nodo con prompt).
  2. Añade una entrada a `docs/decisiones.md`.
  3. Actualiza la tabla de versiones de `docs/workflows/minibus.md`.
  4. Abre un PR para que otra persona lo revise.
- **Publicar** lo hace una persona, no el agente, salvo que se pida de forma explícita en ese
  momento.
- **Una sola versión en producción por bot.** Si hay llamadas entrando por versiones no
  publicadas (números de teléfono apuntando a otra versión), apúntalo en `docs/pendientes.md`.
- **Variables:** en actualizaciones se usan `{{persistent_id.variable}}`, nunca índices
  numéricos. Las salidas de AI Extract llevan el prefijo `response.`. Después de cambios en
  bloque, ejecuta `fix_broken_vars`.
- **Los IDs de nodo cambian con cada versión**: en los análisis, localiza los nodos por NOMBRE.

## 4. Análisis de calidad (rutina diaria)

La rutina `rutinas/informe-minibus.md` se ejecuta cada día y hace tres cosas:
- analiza las llamadas en HappyRobot y RingCentral;
- escribe las cifras en el artefacto de Minibús (colección `informes`,
  https://claude.ai/artifact/GmKgXeUN1kGKkNtv4yPB3y);
- envía una notificación.

Es de **solo lectura** en HappyRobot y RingCentral.

Reglas aprendidas (detalle en `docs/decisiones.md`):
- **Resultado de un intento de transferencia:**
  - `error` vacío o `transfer_result_timeout`: conectado.
  - `whisper_transfer_no_bridge`: el agente cogió y no pulsó 1.
  - «user disconnected before rep connected»: el cliente colgó esperando.
  - `whisper_transfer_timeout`: corte a 300 s sin agente.
- Las extensiones **2114, 2115 y 2119** son menús automáticos de asistencia, no agentes.
- `buscar_punto_de_encuentro` devuelve vacío **a propósito** (es un cambio de módulo). Por eso
  `herramientas_con_error` e `invento_informacion` del extract son casi siempre falsos positivos.
- El extract no es fiable: un fallo del bot solo cuenta si se ve en turnos `assistant` de la
  transcripción.
- **RingCentral:** las patas de todos los bots salen de la extensión 19236 (id interno
  4027457064). Se emparejan con cada intento de transferencia por extensión e inicio a ±10 s.
- **Cómo trocear el trabajo:**
  1. Listado de runs con `monitor_runs action=list`, todas las páginas.
  2. `outputs` por run, repartido en subagentes de unos 23 runs.
  3. Cada subagente escribe un JSON; los teléfonos se guardan solo como hash.

## 5. Convenciones

- **Idioma:** todo en castellano (docs, commits, nombres de versión).
- **Commits:** asunto descriptivo + línea `Co-Authored-By: Claude …`.
- **Ramas:** `prompt/…` para cambios de prompt, `docs/…` para documentación y `fix/…` para
  correcciones. Merge a `main` por PR.
- **Fechas en hora de Madrid** (UTC+2 hasta el 25/10/2026, UTC+1 después).
- No cerrar cada respuesta con menús de «¿siguiente paso?».
