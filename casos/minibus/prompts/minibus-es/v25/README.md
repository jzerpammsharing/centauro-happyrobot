<!-- workflow: 019f7594-2cce-7eed-b995-dd9ea64a1062 · versión: v25 (k2in5n9kk01x) · solo cambia el nodo de rutas «¿Enviar WhatsApp?» · 2026-10-15 -->

# v25 · v24 + rama por defecto en ¿Enviar WhatsApp?

Fork de la v24 (`5g6422lgdcem`). **Los prompts, el Python y la plantilla son los de v24** y no se
copian aquí. Están en `../v24/`, y lo que v24 no tocó, en `../v23/` y `../v22/`.

## Único cambio

| Nodo | v24 | v25 |
|---|---|---|
| ¿Enviar WhatsApp? (Paths) | Una rama: «Enviar» (`enviar` es true) → «Enviar WhatsApp del punto de encuentro» | Igual, más la rama «Fallback» (tipo `fallback`) sin ninguna acción detrás |

Con `enviar` false, el run debe terminar en «completed» en lugar de «failed». El motivo y el estado
están en D-011 (`../../../docs/decisiones.md`).
