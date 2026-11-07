# Atención España · v4

`v4 · v3 + retraso de vuelo o tren a la cola de Minibús con Gestión cerrada` (slug `02qakmz6tbk0`, version_id
`01a16ed5-c62b-7965-b592-091ca135c78c`). Fork de la v3 del 24/10/2026 (D-019). Sin publicar.

Qué cambia respecto a la v3 (el resto de nodos es igual: sus copias siguen en `../v3/` y `../v2/`):

| Fichero | Nodo | Cambio |
|---|---|---|
| `buscar-respuesta.md` | Buscar respuesta (Python), en Consultas y en Prolongación | Sección `recoger_tarde` regenerada del bloque: con Gestión cerrada y fuera del modo virtual se ofrece comprobar el servicio de espera y, si acepta, se transfiere a la cola `minibus` (motivo `otro`); pregunta la hora de llegada si no la dice; «llega de noche» explica antes el servicio de espera si es por un retraso |
| `herramientas-consultas.md` | transfer_to_human_agent de Consultas | Descripción y cola `minibus`: con gestión cerrada, el servicio de espera de un vuelo o un tren retrasado va a la cola minibus |
| `consultas-del-alquiler.md` | Consultas del alquiler (prompt) | CÓMO LEER LA SECCIÓN: «a la cola minibus» es una transferencia de la sección; con gestión cerrada «no uses gestion» en vez de «no transfieras». 7.999 caracteres (máximo 8.000; `comprobar_prompts.py v4` sin fallos). El bloque de reglas comunes no cambia |

79 nodos, como la v3 (comprobado con `get_workflows` el 24/10/2026). Los IDs de nodo de la v4 empiezan por
`01a16ed5-`; los persistent_id no cambian.
