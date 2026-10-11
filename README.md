# centauro-happyrobot

Todos los casos de uso de **Centauro Rent a Car en HappyRobot**: documentación, histórico de
decisiones, prompts versionados y rutinas de análisis.

| Caso | Carpeta | Estado |
|---|---|---|
| Minibús (ES · IT · PT) | `casos/minibus/` | Documentado; rutina diaria de calidad activa |
| Prolongaciones (ES) | `casos/prolongaciones/` | Por documentar |
| Reembolsos | `casos/reembolsos/` | Por documentar |

- Empieza por **`CLAUDE.md`** (común) y luego por el `CLAUDE.md` del caso.
- **Colas y extensiones de RingCentral** (compartidas) → `docs/extensiones.md`
- **Decisiones comunes** → `docs/decisiones.md`; las de cada caso → `casos/<caso>/docs/decisiones.md`

## Trabajar con Claude Code
1. Clona el repo y ábrelo con Claude Code (terminal, escritorio o claude.ai/code).
2. Conecta en tu cuenta los conectores de HappyRobot y RingCentral.
3. Claude lee `CLAUDE.md` al empezar. Pide confirmación antes de cambiar nada en HappyRobot.
