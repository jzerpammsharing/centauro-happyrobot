# CLAUDE.md — Caso Minibús

Contexto propio del caso Minibús. Las reglas comunes (forma de trabajar, transferencias,
RingCentral, convenciones) están en el `CLAUDE.md` de la raíz.

## 1. Qué es

Tres voicebots de HappyRobot, uno por país, cada uno con su agente «Daniel». Atienden a clientes
que normalmente están **en el aeropuerto esperando el minibús** de Centauro. Les dan el punto de
encuentro o les transfieren a las colas del call center en RingCentral.

| Workflow | País | workflow_id | slug | Producción (12/10/2026) |
|---|---|---|---|---|
| Centauro Minibus SPAIN | ES | `019f7594-2cce-7eed-b995-dd9ea64a1062` | `t2vkrtiqj3ve` | v22 (`2l6skwt8wphb`) |
| Centauro Minibus ITALY | IT | `01a03a65-3700-74c1-9c7b-e9c708833c4b` | `w13gsdcqkq9b` | Version 2 (`v9c38tkjwxae`) |
| Centauro Minibus Portugal | PT | `01a05977-3a33-76da-acb2-a757f3947cf9` | `i8kjlnu1m3zp` | v1 (`ql6fasoxl1ql`) |

- **Fichas de los workflows** (flujo, comportamiento esperado, campos del extract, versiones):
  `docs/workflows.md`.
- **Colas:** `../../docs/extensiones.md`. Minibús España (desde la v19) comparte con
  Prolongaciones las colas 18057, 18061, 18001, 18006 y 18034. Además, Prolongaciones transfiere a
  las colas de Minibús España, 18056 y 18059.

## 2. Carpetas del caso

| Ruta | Qué contiene |
|---|---|
| `docs/decisiones.md` | Decisiones de Minibús (D-NNN) |
| `docs/workflows.md` | Ficha de los tres workflows y tabla de versiones |
| `docs/pendientes.md` | Incidencias abiertas y mejoras propuestas |
| `docs/informes/` | Resumen mensual de los informes diarios |
| `prompts/minibus-<es\|it\|pt>/<versión>/` | Copias de los prompts |
| `rutinas/informe-minibus.md` | Prompt de la rutina diaria de calidad |

## 3. Reglas propias de Minibús

- `buscar_punto_de_encuentro` devuelve vacío **a propósito**: es un cambio de módulo y los puntos
  están en el prompt de «Punto de encuentro» (D-002). Lo mismo pasa con `consultas_alquiler` e
  `informacion_oficina` (ES v19 y siguientes). Por eso `herramientas_con_error` e
  `invento_informacion` del extract son casi siempre falsos positivos.
- `aeropuerto_detectado` hay que normalizarlo (Napoli/Nápoles, Venezia/Venecia, Bologna/Bolonia,
  Malpensa/Milano-Malpensa…).
- España: la v22 se publicó entre el 11/10 a las 21:53 y el 12/10 a las 08:02. Desde entonces todas
  las llamadas entran por ella; antes convivían varias versiones (ver `docs/pendientes.md`).

## 4. Rutina diaria de calidad

`rutinas/informe-minibus.md` se ejecuta a diario y hace tres cosas:
- analiza las llamadas de los tres países en HappyRobot y RingCentral;
- escribe las cifras en el artefacto de Minibús (colección `informes`,
  https://claude.ai/artifact/GmKgXeUN1kGKkNtv4yPB3y; doc_id = AAAA-MM-DD);
- envía una notificación.

Las claves del documento del artefacto y su significado están en la sección 8 del prompt de la
rutina. Cada día se añade una línea al resumen mensual de `docs/informes/`.
