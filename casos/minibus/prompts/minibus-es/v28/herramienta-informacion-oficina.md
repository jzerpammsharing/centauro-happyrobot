<!-- workflow: 019f7594-2cce-7eed-b995-dd9ea64a1062 · versión: v28 (arjyj8ufclwz) · nodo: informacion_oficina de Punto de encuentro · copiado: 2026-10-25 -->

# Herramienta `informacion_oficina` en «Punto de encuentro» (v28)

Herramienta nueva de la v28 (D-014), añadida por API debajo del prompt «Punto de encuentro». Su
mensaje es `none`: no dice nada y sirve para cambiar de módulo.

| Herramienta | Node ID | Está en el módulo | Debe llevar a |
|---|---|---|---|
| `informacion_oficina` | `01a17263-9058-7c9d-ba62-895569b1ce06` | Punto de encuentro (`01a17262-140a-7670-b746-32485aaf9c54`) | Información de oficina (`01a17262-1409-7c6a-a58b-7bcdf2db7c14`, persistent_id `01a103fb-1a38-7793-9a90-2bed30a37fcb`) |

**Falta el «Module Change».** La API no permite crearlo. Hasta que una persona lo añada en el
editor (Agent Utilities → Module Change, debajo de esta herramienta, apuntando a «Información de
oficina»), la herramienta devuelve vacío y el bot puede inventarse la respuesta (eval DIR-2). La v28
no se puede publicar sin él.

## Descripción

> Úsala cuando el cliente quiera la dirección de una oficina de Centauro, también la de su aeropuerto (por ejemplo, porque va en taxi o en su coche), o el horario, cómo llegar o dónde devolver el coche en una oficina que no es de aeropuerto (estación o ciudad). Sirve a cualquier hora, también en modo virtual. NO la uses para el minibús, el punto de encuentro ni el horario o la devolución en un aeropuerto: eso lo contestas tú. No digas nada especial antes: la herramienta continúa la conversación.

## Parámetros

- **tema** (obligatorio): Lo que quiere saber el cliente. Valores permitidos EXACTOS: "direccion" (la dirección de una oficina, también de aeropuerto, para ir en taxi o en coche), "horario" (horario de una oficina que no es de aeropuerto), "como_llegar" (cómo llegar a una oficina de estación o de ciudad para recoger el coche), "devolucion" (dónde devolver el coche en una oficina que no es de aeropuerto). Si pregunta por varias cosas, pon la primera que haya pedido.
- **oficina** (opcional): La oficina, ciudad, estación o aeropuerto tal como lo ha dicho el cliente o como ya se sabe en la llamada (por ejemplo: Málaga aeropuerto, Atocha, Madrid, Alicante estación). Si no se sabe todavía, OMITE este parámetro por completo: no lo envíes vacío ni con valores como "desconocida". Nunca lo preguntes solo para rellenarlo: la herramienta se encarga de identificar la oficina.
