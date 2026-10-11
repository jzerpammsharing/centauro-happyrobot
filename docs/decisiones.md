# Registro de decisiones

Una entrada por decisión, la más reciente arriba. Cada una dice qué se decidió, por qué, a qué
afecta y quién la tomó. Si una decisión sustituye a otra, enlázala ("sustituye a D-003").

Plantilla:

```
## D-NNN · AAAA-MM-DD · Título corto
- **Qué:** …
- **Por qué:** … (datos: run_id, cifras del informe, llamadas de ejemplo)
- **Afecta a:** bot(s) y versión(es)
- **Quién:** persona(s)
- **Estado:** propuesta | aprobada | aplicada en vX | descartada
```

> Las entradas D-001 a D-004 se reconstruyeron el 11/10/2026 a partir de los nombres de las
> versiones y del análisis de calidad. Faltan fechas exactas y responsables: complétalos quien lo
> sepa.

---

## D-007 · 2026-10-11 · Rutina diaria: corrección del prompt
- **Qué:**
  - Las transferencias de Minibús ES a 18057, 18061, 18001, 18006 y 18034 cuentan en el informe;
    se ignoran solo las patas de esas colas que no casan con un intento de Minibús.
  - La 2119 se añade a los menús prohibidos.
  - La 18066 (PT-EN) se añade a las colas de Minibús.
  - `consultas_alquiler` e `informacion_oficina` vacías no son error.
  - El listado de runs se extrae con python, no copiado a mano.
  - Los teléfonos se guardan solo como hash.
  - Se tolera el retraso de RingCentral en los últimos 15 minutos del periodo.
  - Se reintenta ante el límite de peticiones del conector.
- **Por qué:** en el informe del 10/10, las versiones v19 y siguientes de ES transfirieron 21 veces
  a Gestión (18057 y 18061) y ahí se perdieron 2 llamadas porque el agente no pulsó 1. Con el
  prompt anterior esas transferencias se habrían ignorado. También hubo una avería a la 2119 en
  Italia.
- **Afecta a:** `rutinas/informe-minibus.md`.
- **Quién:** pendiente de aplicar en la rutina programada.
- **Estado:** aplicada en el repo; falta pegarla en la rutina.

## D-006 · 2026-10-11 · Mejoras de prompt para Minibús (propuesta)
- **Qué:**
  - preguntas frecuentes con respuestas validadas (recogida tarde, devoluciones, oficinas,
    políticas);
  - dar el punto de encuentro en una frase y repetirlo si el cliente interrumpe;
  - transferir tras 2 preguntas sin respuesta;
  - no dar frecuencias del minibús que no estén en la ficha;
  - responder en el idioma del cliente;
  - permitir dar la dirección de la oficina al cliente que está en el aeropuerto.
- **Por qué:** el 10/10, 31 de 252 llamadas se podrían haber resuelto sin herramientas nuevas.
  La tasa de resueltas pasaría del 42 % al 54 % aproximadamente. Ejemplos: `4673ac2f`
  (frecuencia inventada), `a625edab` (idioma), `c6ffa5b5` (pregunta repetida 4 veces).
- **Afecta a:** Minibús ES, IT y PT.
- **Quién:** pendiente.
- **Estado:** propuesta.

## D-005 · 2026-10-10 · Las extensiones 2114, 2115 y 2119 no pueden ser destino de transferencia
- **Qué:** quitar 2114, 2115 (España) y 2119 (Italia, «RA IT-EN-OPCIONES») de los destinos de
  avería y accidente, y transferir a la cola de agentes de asistencia.
- **Por qué:** son menús automáticos, no agentes. El 09/10 hubo 3 averías perdidas (v17 y v18).
  El 10/10 hubo una a la 2115 (v19, `c6ffa5b5`) y otra a la 2119 (`7463c774`).
- **Afecta a:** Minibús ES (v17 a v19, como mínimo) y Minibús IT (v2).
- **Quién:** pendiente.
- **Estado:** propuesta.

## D-004 · antes del 10/10/2026 · Nuevas versiones de ES con prolongaciones y consultas (v19, v21, v22)
- **Qué:** se añaden el módulo «Prolongación y consultas» (herramientas `consultas_alquiler` e
  `informacion_oficina`), los ajustes de voz y de Palma, las respuestas validadas y el horario de
  la cola de Gestión.
- **Por qué:** resolver consultas del alquiler sin transferir.
- **Nota:** el 10/10, 70 de 133 llamadas de ES entraron por estas versiones aunque la publicada
  es la v17. Hay que decidir cuál es la buena y dejar una sola en producción.
- **Estado:** en prueba (sin publicar).

## D-003 · antes del 10/10/2026 · Horario 08:00–23:00 y modo virtual (ES v17, publicada)
- **Qué:** amplía el horario de atención y añade el modo virtual.
- **Estado:** aplicada en ES v17.

## D-002 · antes del 10/10/2026 · `buscar_punto_de_encuentro` es un cambio de módulo, no una consulta
- **Qué:** la herramienta devuelve siempre vacío (Data null, SUCCESS). La lista de puntos de
  encuentro vive en el prompt del nodo «Punto de encuentro».
- **Por qué:** comprobado en 7 transcripciones: el bot da el punto correcto.
- **Consecuencia:** los campos del extract `herramientas_con_error=buscar_punto_de_encuentro` e
  `invento_informacion=si` son falsos positivos del analizador (el 08/10 salieron en 129 y 115 de
  278 llamadas).
- **Estado:** aplicada.

## D-001 · antes del 10/10/2026 · El analista de calidad es de solo lectura
- **Qué:** la rutina diaria no modifica workflows ni runs ni escribe en RingCentral. Solo escribe
  en la colección `informes` del artefacto de Minibús.
- **Por qué:** evitar cambios en producción sin revisión humana.
- **Estado:** aplicada.
