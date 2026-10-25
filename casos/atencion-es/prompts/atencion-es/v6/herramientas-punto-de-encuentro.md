<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v6 (lxkt96mlluxz) · nodo: informacion_oficina (Punto de encuentro) · copiado: 2026-10-25 -->

# Herramientas de Punto de encuentro · v6

Solo cambia `informacion_oficina` (nodo de la v6 `01a1726a-a854-7057-99c6-af046a17e6e2`, persistent_id
`01a155d9-5db0-7106-ab47-43027e0f8647`): la descripción y el parámetro `tema` (D-020). Su Module Change
(`01a1726a-a85a-7ae7-a110-27f5f91fca22`) y el resto de herramientas son iguales que en la v2:
`../v2/herramientas-punto-de-encuentro.md`.

**Descripción** (añadido en la v6: la dirección de cualquier oficina; el 25/10, tras la primera subida, «sea para lo que sea»
en lugar de «por ejemplo, porque va en taxi o en su coche»):

Úsala cuando el cliente quiera saber la dirección de una oficina de Centauro, sea para lo que sea y también la de un
aeropuerto (aunque ya le hayas dado el punto de encuentro), o el horario de una oficina que no es de aeropuerto (estación o ciudad), cómo llegar a
ella o dónde se devuelve el coche en ella. Sirve a cualquier hora, también en modo virtual. NO la uses para el minibús,
el punto de encuentro ni el horario o la devolución en un aeropuerto: eso es de aquí. Devolver el coche antes de tiempo
o en otra oficina distinta de la del contrato es una duda del alquiler: consultas_alquiler con el tema devolucion. No
digas nada antes ni después: la herramienta continúa la conversación.

**Parámetros:**
- `motivo` (sin cambios): Por qué cambias de módulo: lo que el cliente pide ahora, en una frase corta, con lo que ya ha
  dicho y sin datos personales (ni nombre, ni reserva, ni matrícula, ni correo, ni teléfono).
- `tema` (añadido el valor "direccion"): Lo que quiere saber el cliente. Valores permitidos EXACTOS: "horario" (horario
  de la oficina), "como_llegar" (cómo llegar a una oficina de estación o de ciudad para recoger el coche), "devolucion"
  (dónde devolver el coche), "direccion" (la dirección de una oficina, también de aeropuerto, sea para lo que sea). Si pregunta por varias cosas, pon la primera que haya pedido.
- `oficina` (sin cambios): La oficina, ciudad, estación o aeropuerto tal como lo ha dicho el cliente (por ejemplo:
  Málaga estación, Atocha, Madrid, Alicante aeropuerto). Si el cliente todavía no lo ha dicho, OMITE este parámetro por
  completo: no lo envíes vacío ni con valores como "desconocida". Nunca lo deduzcas ni lo preguntes solo para
  rellenarlo: la herramienta se encarga de identificar la oficina.
