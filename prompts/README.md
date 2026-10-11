# Prompts versionados

Copia de los prompts de cada versión de los workflows, para tener histórico y poder comparar
versiones con `git diff`.

Estructura: `prompts/<bot>/<versión>/<nodo>.md`, por ejemplo:

```
prompts/minibus-es/v17/receive-customer-call.md
prompts/minibus-es/v17/punto-de-encuentro.md
prompts/minibus-es/v17/registrar-resultado.md
```

Cada fichero empieza con una cabecera:

```
<!-- workflow: 019f7594-… · versión: v17 (i0syf61bujsz) · nodo: Punto de encuentro · copiado: AAAA-MM-DD -->
```

Para copiarlos, pídele a Claude: «guarda en prompts/ los prompts de la versión <slug> del workflow
<nombre>». Usará `get_workflows` con `version_slug` y `get_node_details`, que son de solo lectura.
