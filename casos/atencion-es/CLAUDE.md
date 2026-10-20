# CLAUDE.md — Caso Atención España (bot único)

Contexto propio del caso. Las reglas comunes (forma de trabajar, transferencias, RingCentral, convenciones)
están en el `CLAUDE.md` de la raíz.

## 1. Qué es

El **bot único** de atención de Centauro España: una puerta de entrada corta (Triaje) y módulos especialistas
entre los que el bot salta con Module Change. Va absorbiendo las opciones del menú telefónico una a una.

- **Fase 1 (v2 construida, sin publicar; puerta 0 pendiente; tareas 1–16 de 18, la 17 y la 18 a falta de las partes con personas):** opciones de **Minibús** y de **Prolongación** de España. Hoy las atienden los workflows
  de `casos/minibus/` (Minibús ES) y `casos/prolongaciones/`, que siguen publicados como vuelta atrás.
- **Después, por decidir:** Gestión cuando está cerrada, triaje en Nueva Reserva, Gestión en horario.
- **Spec:** `docs/specs/2026-10-18-bot-unico-arquitectura.md`. Decisiones: C-004 (raíz) y `docs/decisiones.md`.

| Workflow | workflow_id | slug | Estado |
|---|---|---|---|
| Centauro Atención España | `01a14f1b-4ea9-7827-a4f3-4cfb06a896f6` | `rntn68r0a8gh` | Creado el 18/10/2026 duplicando Minibús ES v25. v1 `veavliy3k6jx` (copia de referencia, version_id `01a14f1b-4eee-7f9c-8ec5-19600855e648`) y v2 `x8xd0llbdp3j` (version_id `01a14f1d-0387-70e5-a6ad-2b311a86224c`): **v2 construida, sin publicar; puerta 0 pendiente**. 87 nodos (tras R10 y R42, 20/10/2026), 12 Module Change; sin líneas en el trigger |

**Bloqueos de la puerta 0** (detalle en `docs/pendientes.md`, «Antes de conectar la primera línea», y en el registro
de progreso, «Task 16: parked»): evals en rojo (VIRT-T1, HOR-C1, FDS-02, TEL-C1, DEVOL-03a/03c, CARGO-05,
PISTA-04, PROL-05/06, CORREO-08, resto de Punto de encuentro al 87,3 %); `HORA_PRUEBA` en `ninguna`; correo «coincide» y `pista_correo` sin probar con reserva real; llamadas de
prueba (Tarea 17) y ensayo de líneas (Tarea 18, Paso 2) con personas. Procedimiento de movimiento de líneas:
`docs/procedimiento-lineas.md` (control de la fase 2: Minibús ES v25, R46).

Versiones, flujo de nodos y ids por nodo: `docs/workflows.md`. Qué copió el duplicado y qué falta (evals, líneas,
ajustes, Twin): `docs/pendientes.md`.

## 2. Carpetas del caso

| Ruta | Qué contiene |
|---|---|
| `docs/decisiones.md` | Decisiones del caso (D-NNN) |
| `docs/workflows.md` | Ficha del workflow y tabla de versiones |
| `docs/pendientes.md` | Incidencias abiertas, comprobaciones y mejoras |
| `docs/procedimiento-lineas.md` | Cómo mover las líneas de Prolongación y Minibús ES al bot único y volver atrás |
| `docs/specs/` | Specs (arquitectura del bot único) |
| `docs/planes/` | Plan de construcción (`2026-10-18-bot-unico-construccion.md`) y registro de progreso de los subagentes (`2026-10-18-bot-unico-progreso.md`, copia para retomar en otro equipo) |
| `prompts/atencion-es/<versión>/` | Copias de los prompts y de la configuración de los nodos |
| `codigo/` | Python de los nodos y sus pruebas (al construir) |
| `rutinas/` | Prompt de la rutina diaria de calidad (`informe-atencion-es.md`) y fuente HTML del artefacto «Calidad Atención España» (`calidad-atencion-es.html`) |

## 3. Reglas propias del caso

- **Módulos:** Triaje (gpt-4.1-fast), Punto de encuentro, Información de oficina, Prolongación (gpt-5.4, el único
  que razona) y Consultas del alquiler. Ver la tabla del spec (§5.4).
- **Conocimiento:** las respuestas del alquiler viven en `comun/bloques/consultas-alquiler.md` y llegan al bot por
  la herramienta `buscar_respuesta`, generada desde el bloque. No se copian enteras en ningún prompt. Las reglas
  comunes de los módulos viven en `comun/bloques/reglas-comunes.md`.
- **Transferencias:** el modelo elige la `cola`, no la extensión. Con Gestión cerrada, el código no transfiere
  aunque el modelo lo pida (red de seguridad, spec §5.8).
- **Module Change:** no se pueden crear por API; los crea una persona en el editor.
- **Borrar un nodo por API borra todo su subárbol** y no hay forma de reenganchar un nodo a otro padre: no borrar
  nodos con hijos (comprobado el 18/10/2026; `docs/pendientes.md`).
- **Prompts del duplicado:** el markdown de `get_node_details` conserva los `group_id` antiguos de Minibús ES;
  al actualizar un prompt, escribir `{{persistent_id.variable}}` con los ids de `docs/workflows.md`.
- **MCP de Centauro:** va contra la API real aunque la credencial se llame «Stagin». No hacer refresh de los
  servidores MCP en HappyRobot.
- **Medición:** la misma para este workflow y para los bots actuales (`scripts/medir_bots.py`).
  Resolución real y créditos por llamada resuelta son los indicadores principales (spec §6).

## 4. Rutina diaria de calidad

`rutinas/informe-atencion-es.md` (sin programar; lo decide una persona). Mide el día anterior del bot único, de
Prolongaciones y de Minibús ES con la misma cadena: runs y outputs en HappyRobot (subagentes de ~23 runs, teléfonos
solo en hash) → `scripts/creditos_runs.py` (necesita `HAPPYROBOT_API_KEY` en el entorno; sin ella, créditos null) →
RingCentral (¿llegó a un agente?) → `scripts/normalizar_llamadas.py` → `scripts/medir_bots.py` →
`codigo/informe_diario.py` (documento del día y puertas de §8.4). Los lunes, auditoría de 30 llamadas. D-011.

| Artefacto | La rutina escribe en | Lo escriben personas |
|---|---|---|
| [Calidad Atención España](https://claude.ai/artifact/4YyyT2jrKTe1TjhGdApnh7) (privado; fuente `rutinas/calidad-atencion-es.html`) | `informes` (doc_id = AAAA-MM-DD) | cualquier campo de un documento que no salga de `informe_diario.py` ni de la sección 8 del prompt |
