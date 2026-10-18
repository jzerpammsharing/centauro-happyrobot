# Prompts versionados

Copia de los prompts y de la configuración de los nodos de cada versión de «Centauro Atención España», para tener
histórico y poder comparar versiones con `git diff`.

Estructura: `casos/atencion-es/prompts/atencion-es/<versión>/<nodo>.md`. Cada fichero empieza con una cabecera:

```
<!-- workflow: … · versión: v2 (slug) · nodo: Triaje · copiado: AAAA-MM-DD -->
```

Los bloques comunes que se copian en los módulos (`comun/bloques/reglas-comunes.md` y, por herramienta,
`comun/bloques/consultas-alquiler.md`) se guardan aquí tal como quedan en cada nodo, para que el diff muestre lo
que de verdad lee el bot.
