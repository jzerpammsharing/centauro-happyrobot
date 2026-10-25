# Atención España · v3

`v3 · v2 sin el correo de contraseña + línea de Prolongación ES` (slug `5cu7jiosi6n7`, version_id
`01a16336-eee7-7143-ba65-931217592e78`). Fork de la v2 del 22/10/2026 (D-018). Sin publicar.

Qué cambia respecto a la v2 (el resto de nodos es igual: sus copias siguen en `../v2/`):

| Fichero | Nodo | Cambio |
|---|---|---|
| `prolongacion.md` | Prolongación (prompt) | Sin ENVÍO DEL CORREO DE CONTRASEÑA ni PISTA DEL CORREO; la contraseña como en la V11 de Prolongaciones (18.648 caracteres) |
| `herramientas-prolongacion.md` | herramientas de Prolongación | Borradas `enviar_correo_contrasena` y `pista_correo` con sus cadenas (8 nodos); `transfer_to_human_agent` sin el correo |
| `registrar-resultado.md` | Registrar resultado de la llamada (extract) | Sin las nueve líneas de entrada de esas herramientas; mismos 46 campos |
| `inbound-call.md` | Inbound Call (trigger) | Lleva la línea de Prolongación ES (para la prueba de una hora) |

79 nodos (comprobado con `get_workflows` el 22/10/2026): 5 prompt, 26 action, 24 tool, 12 condition y 12
module-change. Los persistent_id no cambian; los IDs de nodo de la v3 empiezan por `01a16336-`.
