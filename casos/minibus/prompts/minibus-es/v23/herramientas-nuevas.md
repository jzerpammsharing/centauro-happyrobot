<!-- workflow: 019f7594-2cce-7eed-b995-dd9ea64a1062 · versión: v23 (3o04zrwgfj0g) · nodo: herramientas de cambio de módulo añadidas · copiado: 2026-10-12 -->

# Herramientas añadidas en la v23

Las cuatro son copias de las herramientas de «Triaje y horario». Cambia solo la descripción, adaptada
al módulo donde están; los parámetros son los mismos. Su mensaje es `none`: no dicen nada y sirven
para cambiar de módulo.

| Herramienta | Node ID | Está en el módulo | Debe llevar a |
|---|---|---|---|
| `consultas_alquiler` | `01a1305c-93e2-753f-9318-debd132bf553` | Punto de encuentro | Prolongación y consultas |
| `consultas_alquiler` | `01a1305c-fd17-7fe2-9ed6-d04b2ba552b0` | Información de oficina | Prolongación y consultas |
| `buscar_punto_de_encuentro` | `01a1305c-fd20-776b-90b9-47289c4fceca` | Prolongación y consultas | Punto de encuentro |
| `informacion_oficina` | `01a1305c-fd27-7db0-b620-5cbbc488e387` | Prolongación y consultas | Información de oficina |

## Diferencias con las originales

- **`consultas_alquiler`** (en las dos copias): la descripción ya no remite a
  `buscar_punto_de_encuentro` ni a `informacion_oficina`. Dice que el minibús o los datos de oficina
  los resuelve el propio módulo.
- **`buscar_punto_de_encuentro`** (en Prolongación): solo se usa con el modo virtual en false. Ya no
  habla de «el valor de su lista», porque ese módulo no tiene las listas de aeropuertos cerrados. De
  08:00 a 22:00 todas las oficinas de aeropuerto están abiertas, así que no hace falta comprobarlo.
- **`informacion_oficina`** (en Prolongación): igual que la original, más «No digas nada especial
  antes».

## Enlaces de cambio de módulo (hechos en el editor el 12/10/2026)

La API no permite crear el nodo «Module Change» (en el editor está en Agent Utilities). Se añadieron a
mano y se comprobó por la API que cada uno cuelga de la herramienta correcta y apunta al módulo correcto:

| Module Change | Cuelga de | `moduleId` (módulo destino) |
|---|---|---|
| `01a13064-e348-7628-842d-4f7344089913` | `consultas_alquiler` de Punto de encuentro | `01a13059-cc5e-7370-…` Prolongación y consultas |
| `01a13066-469c-7a3e-b2b4-1d56b67ba704` | `consultas_alquiler` de Información de oficina | `01a13059-cc5e-7370-…` Prolongación y consultas |
| `01a13066-adbd-781b-afbf-fae656b7e31e` | `buscar_punto_de_encuentro` de Prolongación | `01a13059-cc5c-74ea-…` Punto de encuentro |
| `01a13067-80c7-70f6-87a1-2f6bde93f7e0` | `informacion_oficina` de Prolongación | `01a13059-cc5c-77d0-…` Información de oficina |

Sin contexto añadido: el historial de la conversación se conserva al cambiar de módulo.
