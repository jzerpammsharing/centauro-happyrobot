# CLAUDE.md — centauro-happyrobot

Repositorio de **todos los casos de uso de Centauro Rent a Car en HappyRobot**. Esta guía es
común a todos los casos. Cada caso tiene su propio `casos/<caso>/CLAUDE.md` con su contexto
(workflows, flujo, versiones y reglas propias), que Claude Code lee al trabajar en esa carpeta.

**El histórico y el porqué de cada cambio** está en dos sitios:
- decisiones comunes a todos los casos: `docs/decisiones.md`;
- decisiones de un caso: `casos/<caso>/docs/decisiones.md`.

Si algo cambia (versiones, colas, decisiones), actualiza el CLAUDE.md que corresponda y su
registro de decisiones en el mismo commit.

> **Datos personales y secretos:** este repo NO contiene teléfonos, nombres de clientes o agentes,
> emails, números de reserva, matrículas ni credenciales. El run_id de HappyRobot sí se puede
> usar. Los conectores (HappyRobot, RingCentral) se autentican por OAuth en cada cuenta.

---

## 0. Arrancar en una cuenta o equipo nuevo

1. **Clonar** el repo. Rama `main`; un cambio = una rama + PR.
2. **Conectar los conectores MCP** en tu cuenta de Claude:
   - `hr` → HappyRobot (OAuth, workspace de Centauro).
   - `phone` → RingCentral (OAuth; solo lectura).
3. **Permisos:** `.claude/settings.json` pide confirmación antes de cualquier herramienta de
   HappyRobot que escriba (editar nodos, publicar versiones, lanzar o cancelar runs…) y bloquea el
   envío de SMS por RingCentral.
4. **La memoria y los chats de Claude no viajan entre cuentas**: todo lo relevante tiene que estar
   en este repo.

## 1. Casos

Workflows de la carpeta de Centauro en HappyRobot (folder `019d8144-ce27-7aaf-b9e5-21d006083063`):

| Caso | Carpeta | Workflows | Estado de la documentación |
|---|---|---|---|
| Minibús | `casos/minibus/` | Centauro Minibus SPAIN, ITALY y Portugal | Completa |
| Prolongaciones | `casos/prolongaciones/` | Centauro Prolongacion Spain | Completa (V11; v12 en borrador, D-008) |
| Reembolsos | `casos/reembolsos/` | Centauro Reembolsos, Centauro Reembolsos WhatsApp y Centauro Reembolsos · Datos por WhatsApp | Parcial: WhatsApp documentado (spec, D-001, pruebas); faltan el detalle del bot V4 y sus colas |
| Atención España (bot único) | `casos/atencion-es/` | Centauro Atención España (creado el 18/10/2026, sin publicar; absorberá Minibús ES y Prolongación, C-004) | Spec aprobado (D-001); en construcción: tareas 1–15 de 18 hechas (registro en `docs/planes/2026-10-18-bot-unico-progreso.md`) |

Para añadir un caso:
1. Crea `casos/<caso>/` con `CLAUDE.md`, `docs/decisiones.md`, `docs/workflows.md`,
   `docs/pendientes.md` y `prompts/`.
2. Añade el caso a esta tabla.

## 2. Estructura del repo

| Ruta | Qué contiene |
|---|---|
| `CLAUDE.md` | Esta guía común |
| `docs/decisiones.md` | Decisiones que afectan a todos los casos |
| `docs/extensiones.md` | Todas las colas y extensiones de RingCentral (una sola vez para todos) |
| `docs/informes/` | Análisis que comparan varios casos |
| `comun/bloques/` | Bloques de prompt comunes a varios bots (borrador; ver su README) |
| `scripts/` | Utilidades de análisis reutilizables (Python, solo lectura). `medir_bots.py`: resolución real y créditos por llamada resuelta de los tres bots; `normalizar_llamadas.py`: registros por run → `llamadas.json`; `creditos_runs.py`: créditos por run con la API de facturación (clave en `HAPPYROBOT_API_KEY`, nunca en el repo). Pruebas en `scripts/test_*.py` (`python3 -I`) |
| `casos/<caso>/CLAUDE.md` | Contexto del caso |
| `casos/<caso>/docs/` | `decisiones.md`, `workflows.md`, `pendientes.md`, `informes/` |
| `casos/<caso>/prompts/<workflow>/<versión>/` | Copia de los prompts de cada versión, para tener histórico y diff |
| `casos/<caso>/rutinas/` | Prompts de las rutinas programadas del caso |

## 3. Cómo se trabaja con los workflows (todos los casos)

- **Nunca editar una versión publicada.** Se hace `manage_versions action=fork` y se trabaja en
  la copia. El nombre de la versión dice qué cambia: `v22 · v21 + horario de la cola de Gestión`.
- **Antes de publicar:**
  1. Guarda el prompt nuevo en `casos/<caso>/prompts/`.
  2. Añade una entrada al `decisiones.md` del caso.
  3. Actualiza la tabla de versiones de `workflows.md`.
  4. Abre un PR para que otra persona lo revise.
- **Publicar** lo hace una persona, no el agente, salvo que se pida de forma explícita en ese
  momento.
- **Una sola versión en producción por workflow.** Si entran llamadas por versiones no
  publicadas, apúntalo en los pendientes del caso.
- **Variables:** en actualizaciones se usan `{{persistent_id.variable}}`, nunca índices
  numéricos. Las salidas de AI Extract llevan el prefijo `response.`. Después de cambios en
  bloque, ejecuta `fix_broken_vars`.
- **Los IDs de nodo cambian con cada versión**: en los análisis, localiza los nodos por NOMBRE.
- **Antes de cambiar una cola o extensión de transferencia**, mira en `docs/extensiones.md` qué
  otros casos la usan.

## 4. Análisis de llamadas (todos los casos)

- **Solo lectura** en HappyRobot y RingCentral (ver C-002 en `docs/decisiones.md`).
- **Resultado de un intento de transferencia** (nodo «Initiate customer connection»):
  - `error` vacío o `transfer_result_timeout`: conectado.
  - `whisper_transfer_no_bridge`: el agente cogió y no pulsó 1.
  - «user disconnected before rep connected»: el cliente colgó esperando.
  - `whisper_transfer_timeout`: corte a 300 s sin agente.
- Las extensiones **2114, 2115 y 2119** son menús automáticos, no agentes (C-001).
- **RingCentral:** las patas de todos los bots salen de la extensión 19236 (id interno
  4027457064). Se emparejan con cada intento de transferencia por extensión e inicio a ±10 s
  (`scripts/emparejar_ringcentral.py`).
  - El registro va con unos minutos de retraso.
  - El conector a veces da límite de peticiones: espera y reintenta.
- **El extract de IA no es fiable:** un fallo del bot solo cuenta si se ve en turnos `assistant`
  de la transcripción.
- **Volumen grande:**
  1. Listado con `monitor_runs action=list` (todas las páginas; IDs extraídos con python, nunca
     copiados a mano).
  2. `outputs` por run, repartido en subagentes de unos 23 runs.
  3. Cada subagente escribe un JSON; los teléfonos se guardan solo como hash.
  4. Los datos de trabajo van a `datos/`, que no se versiona.

## 5. Convenciones

- **Idioma:** todo en castellano (docs, commits, nombres de versión).
- **Commits:** asunto descriptivo + línea `Co-Authored-By: Claude …`.
- **Ramas:** `<caso>/prompt-…`, `<caso>/docs-…`, `comun/…`. Merge a `main` por PR.
- **Fechas en hora de Madrid** (UTC+2 hasta el 25/10/2026, UTC+1 después).
- No cerrar cada respuesta con menús de «¿siguiente paso?».
