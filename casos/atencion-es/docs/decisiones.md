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

## D-004 · 2026-10-18 · Red de seguridad del modo virtual en «Preparar transferencia»
- **Qué:** de 22:00 a 8:00 (hora peninsular, calculada al ejecutarse el nodo, como la de Gestión), «Preparar
  transferencia» solo transfiere a `asistencia`. Si el modelo pide `minibus` o `nueva_reserva`, no transfiere y
  devuelve `resultado: modo_virtual` con un detalle fijo: no hay compañeros en esa cola a esta hora, no lo vuelvas a
  intentar con ella; si es una avería o un accidente, a la cola asistencia; si no, sigue MODO DE ATENCIÓN (volver a
  llamar a partir de las ocho) sin decir que le pasas con nadie. Si pide `gestion` de noche, gana `gestion_cerrada`
  (Gestión cierra a las 21:00, así que de noche siempre está cerrada). Cambia el spec §5.8 y §5.11. El prompt no
  cambia: el detalle remite a lo que ya dice el bloque de reglas comunes.
- **Por qué:**
  - en modo virtual el modelo a veces transfería igualmente a minibus (ADV-2 de Consultas 1/3 en la ronda 3;
    «VIRTUAL · pide persona» del Triaje 2/3), y una transferencia nocturna deja al cliente en una cola vacía;
  - la excepción del modo virtual en la descripción de `buscar_punto_de_encuentro` del Triaje no sirve: con ella
    VIRT-T1 cae a 0/3 (ronda de arreglos 1 de la Tarea 9). Se queda fuera del Triaje; la de Consultas se mantiene;
  - gana `gestion_cerrada` sobre `modo_virtual` porque COLA DE GESTIÓN CERRADA da el horario real de Gestión y el
    bloque de reglas comunes ya manda seguirla en un caso de gestión, también en modo virtual; con `modo_virtual`
    el bot diría «a partir de las ocho», falso de viernes a domingo y en vísperas de festivo. Así además Gestión se
    transfiere exactamente cuando `gestion_abierta_en` dice que está abierta (lo comprueba la prueba de equivalencia).
- **Afecta a:** v2 (los dos «Preparar transferencia», Triaje y Consultas; los de Prolongación y los demás módulos
  copiarán el mismo código). Código y pruebas: `codigo/preparar_transferencia.py` y
  `codigo/test_preparar_transferencia.py` (71 casos).
- **Quién:** jzerpa (responsable), 18/10/2026, a propuesta de la revisión de la Tarea 9 (R24).
- **Estado:** aplicada en v2 (Tarea 9b).

## D-003 · 2026-10-18 · Consultas: ofrecer la transferencia que manda la sección y transferir al sí
- **Qué:** cuando la sección de `buscar_respuesta` manda transferir («Transfiere a GESTIÓN DE RESERVA…») y el cliente
  no ha pedido hablar con nadie, el bot de Consultas le pregunta si quiere que le pase y transfiere cuando acepta; si
  el cliente ya lo ha pedido, transfiere en ese turno. Cambia el prompt («CÓMO LEER LA SECCIÓN») y la descripción de
  `transfer_to_human_agent`. DEVOL-03 se parte en tres evals críticas: 03a (ofrece o transfiere; valen las dos), 03b
  (acepta la oferta → cola gestion, motivo otro) y 03c (Gestión cerrada: ni ofrece ni transfiere, da el horario).
  REQ-09 (objeto olvidado) pasa a aceptar también la oferta.
- **Por qué:** con «ejecútala en ese mismo turno, sin preguntarle si quiere», los modelos seguían ofreciendo en vez
  de transferir (DEVOL-03: gpt-4.1 0/9 en las rondas 1 a 3; gpt-4.1-fast 0/3). Ofrecer antes es aceptable para el cliente y
  no salta a una cola que no ha pedido (R21 de la revisión de la Tarea 9).
- **Afecta a:** v2 (nodo «Consultas del alquiler» y su `transfer_to_human_agent`).
- **Quién:** el responsable de la construcción, a propuesta de la revisión de la Tarea 9.
- **Estado:** aplicada en v2 (ronda de arreglos 1 de la Tarea 9; resultado en `docs/informes/evals-v2.md`).

## D-002 · 2026-10-18 · Consultas del alquiler con gpt-4.1 hasta comparar modelos
- **Qué:** el módulo «Consultas del alquiler» de la v2 queda con `fast-gpt-4.1`. La comparación del spec §7.3
  (gpt-4.1, gpt-4.1-fast y gpt-5.4; el más barato a ≤ 3 puntos del mejor y sin fallos críticos) se hace en una sesión
  posterior, antes de la Tarea 16.
- **Por qué:** acabar antes la Tarea 9. Lo que se llegó a ver, con el mismo prompt (vuelta 2): gpt-4.1 86,9 % (153
  ejecuciones) y gpt-4.1-fast 89,0 % (136); los dos fallan la crítica DEVOL-03 (`docs/informes/evals-v2.md`).
- **Afecta a:** v2 (nodo «Consultas del alquiler»).
- **Quién:** el responsable de la construcción, a través del controlador de la Tarea 9.
- **Estado:** aplicada en v2 (provisional; pendiente en `pendientes.md`).

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
