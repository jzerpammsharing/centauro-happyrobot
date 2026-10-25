<!-- workflow: 019f7594-2cce-7eed-b995-dd9ea64a1062 · versión: v28 (arjyj8ufclwz) · dirección de las oficinas desde Punto de encuentro · 2026-10-25 -->

# v28 · v27 + dirección de las oficinas desde Punto de encuentro

Fork de la v27 (`e4qv98cib2dm`, en producción). Decisión: D-014 (`../../../docs/decisiones.md`).
Análisis y evals: `../../../docs/informes/2026-10-25-v28-direccion.md`.

Lo que no está en esta carpeta es igual que en v27 (`../v27/`) y, para «Información de oficina»,
que en v26 (`../v26/`).

**Sin publicar y no se puede publicar todavía:** falta el «Module Change» debajo de la herramienta
nueva (ver `herramienta-informacion-oficina.md`).

## Nodos que cambian

| Nodo | Cambio |
|---|---|
| `informacion_oficina` (herramienta nueva en Punto de encuentro) | Copia: `herramienta-informacion-oficina.md`. Lleva a «Información de oficina» cuando el cliente pide la dirección de una oficina (también la de su aeropuerto) o datos de una oficina que no es de aeropuerto. Nuevo `tema`: `direccion`. |
| Punto de encuentro (prompt) | Copia: `punto-de-encuentro.md`. Detalle debajo. |
| Información de oficina (prompt) | Copia: `informacion-de-oficina.md`. Detalle debajo. |

## Cambios en «Punto de encuentro»

- **QUÉ HACER AHORA:** si pide la dirección de una oficina, también la de su aeropuerto (para el
  taxi, para ir en su coche o para el navegador), o datos de una oficina que no es de aeropuerto,
  ejecuta `informacion_oficina` en ese mismo turno, sin anunciarlo. Antes, los datos de una oficina
  que no es de aeropuerto se transferían a la cola de MINIBÚS. Solo se transfiere ya lo que no está
  ni en esta sección ni en «Información de oficina».
- **Devolución en aeropuertos:** quita «Dile que busque en el navegador "Centauro Rent a Car" y el
  nombre del aeropuerto». Si pide la dirección, no se le manda a buscarla: se ejecuta
  `informacion_oficina` con el tema `direccion` y su aeropuerto.
- **Modo virtual:** la dirección o los datos de una oficina se dan también con
  `informacion_oficina` (antes: «puede volver a llamar ahora y pedir esa información al principio de
  la llamada»).
- **Escalado a MINIBÚS:** se quita «Pide datos de una oficina que no es de aeropuerto (estación o
  ciudad)».

## Cambios en «Información de oficina»

- **Identidad:** la información de una oficina incluye «su dirección».
- **DIRECCIÓN** (sección nueva, después de HORARIO): da la «Dirección» de la ficha tal cual, también
  si es de aeropuerto; si va en su coche y la ficha trae «Para llegar en coche», también. Si la ficha
  no tiene dirección o dice que la busque en el navegador, se le dice eso una sola vez. Nunca se
  inventa ni se cambia una dirección.
- **CÓMO LLEGAR en un aeropuerto:** quien está allí buscando la oficina o el minibús sigue yendo a la
  cola de MINIBÚS; quien va por su cuenta (en taxi o en su coche) y pide la dirección sigue
  DIRECCIÓN.
- **DÓNDE DEVOLVER, regla 3:** se da la dirección de la ficha; el navegador solo si la ficha no la
  tiene o lo dice.

## Comprobaciones hechas

- Los dos prompts se releyeron tras subirlos: el mismo texto que el preparado y las mismas variables
  (4 en «Punto de encuentro»). En «Información de oficina» solo cambia el salto de línea final.
- `fix_broken_vars` (simulación) en los tres nodos: sin referencias rotas. Los únicos fallos de
  «test-all» son los de siempre en «Initiate customer connection» («room name is required»).
