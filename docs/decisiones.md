# Decisiones comunes a todos los casos

Decisiones que afectan a más de un caso (colas, extensiones, forma de trabajar). Las de un solo
caso van en `casos/<caso>/docs/decisiones.md`. Numeración `C-NNN`, la más reciente arriba.

Plantilla:

```
## C-NNN · AAAA-MM-DD · Título corto
- **Qué:** …
- **Por qué:** … (datos: run_id, cifras, llamadas de ejemplo)
- **Afecta a:** casos y workflows
- **Quién:** persona(s)
- **Estado:** propuesta | aprobada | aplicada | descartada
```

---

## C-004 · 2026-10-15 · Se permiten tests A/B con dos versiones en producción
- **Qué:** un workflow puede tener dos versiones en producción a la vez para comparar una frente a otra. Cada test lleva una entrada en el `decisiones.md` del caso con: versiones, reparto del tráfico, métricas, umbrales de decisión y fecha de revisión. Al terminar se deja una sola versión.
- **Por qué:** poder medir el efecto de un cambio (primer uso: Minibús ES, v22 frente a v24) en lugar de publicarlo a ciegas.
- **Afecta a:** todos los casos; regla de «una sola versión en producción» en `CLAUDE.md`.
- **Quién:** jzerpa
- **Estado:** aprobada

## C-003 · 2026-10-11 · Un solo repo para todos los casos de HappyRobot, con una carpeta por caso
- **Qué:** el repo `centauro-happyrobot` reúne todos los casos de uso de Centauro en HappyRobot.
  Lo común (colas, reglas de transferencia, scripts, convenciones) está en la raíz; cada caso
  tiene su carpeta en `casos/`. Sustituye a la D-008 de Minibús, que hacía un repo solo para
  Minibús.
- **Por qué:**
  - los casos comparten colas de RingCentral (Minibús España y Prolongaciones usan 18057, 18061,
    18001, 18006 y 18034), la extensión de salida y el workspace de HappyRobot;
  - las decisiones comunes se escriben una sola vez;
  - Claude Code lee el `CLAUDE.md` común y el del caso.
  - Se harían repos separados solo si un caso lo lleva otro equipo con otros permisos, si tiene
    código propio desplegable o si se entrega a un tercero.
- **Afecta a:** todos los casos.
- **Quién:** jzerpa.
- **Estado:** aplicada.

## C-002 · antes del 10/10/2026 · Los análisis de llamadas son de solo lectura
- **Qué:** las rutinas y los análisis no modifican workflows ni runs (no cancelan, marcan ni
  lanzan) y no escriben en RingCentral. Solo escriben en sus propios informes (p. ej. la colección
  `informes` del artefacto de Minibús).
- **Por qué:** evitar cambios en producción sin revisión humana.
- **Afecta a:** todos los casos (definida en Minibús como D-001).
- **Estado:** aplicada.

## C-001 · 2026-10-10 · Las extensiones 2114, 2115 y 2119 no pueden ser destino de transferencia
- **Qué:** ningún workflow debe transferir a 2114, 2115 (asistencia en carretera ES/EN) ni a 2119
  («RA IT-EN-OPCIONES»). Las averías y los accidentes van a la cola de agentes de asistencia (en
  España, 18034).
- **Por qué:** son menús automáticos, no agentes.
  - 09/10: 3 averías de Minibús ES perdidas (v17 y v18).
  - 10/10: una avería a la 2115 (Minibús ES v19, `c6ffa5b5`) y otra a la 2119 (Minibús IT v2,
    `7463c774`).
- **Afecta a:** todos los workflows que transfieren averías. Confirmado en Minibús ES e IT.
  Prolongaciones, revisado el 11/10/2026: la V6 mandaba las averías a 2114/2115; desde la V7 van a
  18034/18035 y la V11 no usa ninguna de las tres. Falta revisar Reembolsos.
- **Quién:** pendiente.
- **Estado:** propuesta (antes era la D-005 de Minibús).
