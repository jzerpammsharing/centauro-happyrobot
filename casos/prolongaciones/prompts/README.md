# Prompts versionados

Copia de la configuración de cada versión del workflow «Centauro Prolongacion Spain», para tener
histórico y comparar versiones con `git diff`.

Estructura: `casos/prolongaciones/prompts/prolongacion-es/<versión>/<nodo>.md`. El nombre del fichero
es el nombre del nodo en minúsculas y con guiones.

| Versión | Qué hay |
|---|---|
| `v12/` | v12 (`mnhi8x9j8ce7`), borrador sin publicar (D-008). Solo los nodos que cambian: el prompt de «Prolongacion», la herramienta nueva `enviar_correo_contrasena` con su cadena de nodos, `transfer_to_human_agent` y el extract. El resto es igual que en la V11. |
| `v11/` | Version 11 (`2g1bxzyzazpp`), en producción desde el 11/10/2026. Están 7 de los 8 nodos: el prompt de «Prolongacion», la herramienta, el nodo de transferencia, el extract, el agente de voz y los dos nodos de código. Falta «Inbound Call», que solo contiene los dos números de entrada. |
| `v10/` | V10 (`fg6e9yqdgwok`). Solo el prompt de «Prolongacion», para compararlo con la V11. «Resolver colas», la herramienta y el nodo de transferencia se han comprobado y son iguales en las dos versiones. |

Cada fichero empieza con una cabecera:

```
<!-- workflow: 01a0d9de-… · versión: <nombre> (<slug>) · nodo: <nombre del nodo> · copiado: AAAA-MM-DD -->
```

- **Prompts** (`prolongacion.md`): copia literal del markdown que devuelve `get_node_details`. Las
  variables aparecen como `{{ index . "<persistent_id>.<variable>" }}`, que es como las muestra
  HappyRobot; no están rotas.
- **Resto de nodos:** las variables se escriben como `{{persistent_id.variable}}`.
- **Teléfonos:** el prompt incluye los teléfonos públicos de Centauro que el bot puede dar
  (asistencia, reservas y las oficinas de Benidorm y Torrevieja). El número de entrada de la línea
  en inglés no se copia.

Para copiar una versión nueva, pídele a Claude: «guarda en casos/prolongaciones/prompts/ los prompts
de la versión <slug>». Usará `get_workflows` con `version_slug` y `get_node_details`, que son de
solo lectura.
