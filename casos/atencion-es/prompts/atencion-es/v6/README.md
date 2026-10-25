# Atención España · v6

`v6 · v4 + dirección de las oficinas de aeropuerto` (slug `lxkt96mlluxz`, version_id
`01a1726a-a839-7e93-886c-7831a100a674`). Fork de la v4 del 25/10/2026 (D-020), hecho desde la sesión de Minibús
(mismo arreglo que Minibús v28, D-014 de Minibús). Sin publicar. No hay v5: la que se creó el 24/10 salía de la v3 y se
borró el 25/10.

Qué cambia respecto a la v4 (el resto de nodos es igual: sus copias siguen en `../v4/`, `../v3/` y `../v2/`):

| Fichero | Nodo | Cambio |
|---|---|---|
| `herramientas-punto-de-encuentro.md` | informacion_oficina de Punto de encuentro | La descripción incluye la dirección de cualquier oficina, también de aeropuerto; `tema` gana "direccion" |
| `punto-de-encuentro.md` | Punto de encuentro (prompt) | Fuera «busque en el navegador»: si pide la dirección, `informacion_oficina` con el tema `direccion`; OTRAS HERRAMIENTAS separa la dirección del resto |
| `informacion-de-oficina.md` | Información de oficina (prompt) | Sección nueva DIRECCIÓN (la de la ficha tal cual); taxi o coche propio en un aeropuerto sigue DIRECCIÓN; DÓNDE DEVOLVER, regla 3, da la dirección de la ficha |

79 nodos, como la v4 (comprobado con `get_workflows` el 25/10/2026). Los IDs de nodo de la v6 empiezan por `01a1726a-`.
Segunda subida (25/10/2026, a petición de jzerpa): la dirección se da siempre que la pidan, sea para lo que sea; ya no
depende de que vaya en taxi o en su coche. En un aeropuerto, si busca cómo llegar, punto de encuentro, y si pide la
dirección, también se le da. Cambian cinco frases de los mismos tres nodos (D-020).

Comprobado también que conserva lo de la v4: el `transfer_to_human_agent` de Consultas lleva la excepción de la cola
minibus. `comprobar_prompts.py v6` sin fallos.
