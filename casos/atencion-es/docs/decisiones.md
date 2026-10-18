# Decisiones del caso Atención España

Las decisiones comunes están en `docs/decisiones.md` de la raíz (C-NNN). Aquí van las de este caso (D-NNN), la
más reciente arriba, con la misma plantilla.

Plantilla:

```
## D-NNN · AAAA-MM-DD · Título corto
- **Qué:** …
- **Por qué:** … (datos: run_id, cifras, llamadas de ejemplo)
- **Afecta a:** versión(es)
- **Quién:** persona(s)
- **Estado:** propuesta | aprobada | aplicada en vX | descartada
```

---

## D-001 · 2026-10-18 · Arquitectura del bot único y plan de migración (fase 1: Minibús + Prolongación)
- **Qué:** spec `specs/2026-10-18-bot-unico-arquitectura.md`. Resumen:
  - **Workflow nuevo** «Centauro Atención España», duplicando Minibús ES v25 (ver C-004).
  - **Triaje** corto (gpt-4.1-fast, ≤ 9.000 caracteres) que solo encamina, y cuatro módulos: Punto de encuentro e
    Información de oficina (los de la v25), **Prolongación** (de la v12, gpt-5.4, ≤ 22.000 caracteres) y
    **Consultas del alquiler** (gpt-4.1 o el que digan las evals).
  - **Saltos:** el Triaje es el centro (`volver_al_triaje` en cada módulo) y hay atajos solo entre los pares
    frecuentes. 12 Module Change: 4 ya existen en la v25 y 8 los crea una persona.
  - **Conocimiento:** el bloque común de consultas llega por la herramienta `buscar_respuesta` (Python generado
    desde `comun/bloques/consultas-alquiler.md`), no copiado en los prompts ni en una base de conocimiento de
    HappyRobot.
  - **Transferencias:** `cola` cerrada en vez de extensión; red de seguridad de Gestión cerrada en el código; el
    bot sigue en la llamada (whisper) mientras se afina.
  - **Extract único** para todos los módulos; medición común para los tres workflows (resolución real y créditos
    por llamada resuelta).
  - **Migración:** primero la línea de Prolongación (ES y EN), después la de Minibús ES; dos semanas por línea con
    puertas de calidad y coste. Las líneas actuales se mueven al workflow nuevo al pasar a producción; la vuelta
    atrás es republicar la versión antigua con sus líneas (ensayado antes con la línea de pruebas).
  - **Decidido además el 18/10:** identificar por correo o por número de reserva (con la pista del dominio del
    correo, `pista_correo`) sin cambiar la regla de envío; de 22 a 8 h solo se transfiere a Asistencia, también en
    la línea de Prolongación; Gestión no atiende los festivos nacionales.
- **Por qué:**
  - Coste medido: 118 créditos por llamada en Prolongaciones V11 frente a 64 en Minibús v25; el LLM por respuesta
    va de 2,1 (Triaje) a 12,4 (V11). Estimación del bot único: 60–75 créditos en la línea de Prolongación.
  - Resolución: 38 % hoy en Prolongaciones (transcripciones), 53 % realista con las respuestas nuevas y el MCP.
  - Las respuestas del alquiler están copiadas en dos bots y se contradicen.
- **Afecta a:** workflow nuevo; Minibús ES y Prolongaciones solo como control y vuelta atrás.
- **Quién:** jzerpa (arquitectura y workflow nuevo aprobados el 18/10; el resto del spec, en revisión).
- **Estado:** propuesta.
