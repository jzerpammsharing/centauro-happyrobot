# CLAUDE.md — Caso Atención España (bot único)

Contexto propio del caso. Las reglas comunes (forma de trabajar, transferencias, RingCentral, convenciones)
están en el `CLAUDE.md` de la raíz.

## 1. Qué es

El **bot único** de atención de Centauro España: una puerta de entrada corta (Triaje) y módulos especialistas
entre los que el bot salta con Module Change. Va absorbiendo las opciones del menú telefónico una a una.

- **Fase 1 (en diseño):** opciones de **Minibús** y de **Prolongación** de España. Hoy las atienden los workflows
  de `casos/minibus/` (Minibús ES) y `casos/prolongaciones/`, que siguen publicados como vuelta atrás.
- **Después, por decidir:** Gestión cuando está cerrada, triaje en Nueva Reserva, Gestión en horario.
- **Spec:** `docs/specs/2026-10-18-bot-unico-arquitectura.md`. Decisiones: C-004 (raíz) y `docs/decisiones.md`.

| Workflow | workflow_id | slug | Estado (18/10/2026) |
|---|---|---|---|
| Centauro Atención España | por crear (duplicando Minibús ES v25, `k2in5n9kk01x`) | — | Spec en borrador, sin construir |

## 2. Carpetas del caso

| Ruta | Qué contiene |
|---|---|
| `docs/decisiones.md` | Decisiones del caso (D-NNN) |
| `docs/workflows.md` | Ficha del workflow y tabla de versiones |
| `docs/pendientes.md` | Incidencias abiertas, comprobaciones y mejoras |
| `docs/specs/` | Specs (arquitectura del bot único) |
| `prompts/atencion-es/<versión>/` | Copias de los prompts y de la configuración de los nodos |
| `codigo/` | Python de los nodos y sus pruebas (al construir) |
| `rutinas/` | Prompt de la rutina diaria de calidad (al construir) |

## 3. Reglas propias del caso

- **Módulos:** Triaje (gpt-4.1-fast), Punto de encuentro, Información de oficina, Prolongación (gpt-5.4, el único
  que razona) y Consultas del alquiler. Ver la tabla del spec (§5.4).
- **Conocimiento:** las respuestas del alquiler viven en `comun/bloques/consultas-alquiler.md` y llegan al bot por
  la herramienta `buscar_respuesta`, generada desde el bloque. No se copian enteras en ningún prompt. Las reglas
  comunes de los módulos viven en `comun/bloques/reglas-comunes.md`.
- **Transferencias:** el modelo elige la `cola`, no la extensión. Con Gestión cerrada, el código no transfiere
  aunque el modelo lo pida (red de seguridad, spec §5.8).
- **Module Change:** no se pueden crear por API; los crea una persona en el editor.
- **MCP de Centauro:** va contra la API real aunque la credencial se llame «Stagin». No hacer refresh de los
  servidores MCP en HappyRobot.
- **Medición:** la misma para este workflow y para los bots actuales (`scripts/medir_bots.py`, al construir).
  Resolución real y créditos por llamada resuelta son los indicadores principales (spec §6).
