# Bloques comunes

Textos de prompt que repiten varios bots. Cada bloque es la versión de referencia: cuando un bot cambia
una de esas respuestas, se cambia aquí y se copia a los demás bots en su siguiente versión.

**Estado (17/10/2026):** borrador. Ningún workflow se ha construido todavía a partir de un bloque, y falta
decidir si se adopta esta forma de trabajar (entonces irá a `docs/decisiones.md`).

| Bloque | Lo usan hoy (copiado a mano) | Notas |
|---|---|---|
| `consultas-alquiler.md` | Prolongaciones (V11, de DEVOLVER TARDE a TELÉFONOS) y Minibús España (módulo «Prolongación y consultas») | Base: Prolongaciones V11. Marca lo que solo tiene Minibús, lo nuevo del artefacto «Respuestas de Daniel» y lo que falta decidir |
| `reglas-comunes.md` | Nadie todavía. Va al principio de los cinco módulos del bot único de Atención España (v2, Tareas 8 a 11) | Identidad, voz, idioma, modo virtual, Gestión cerrada, teléfonos, transferencias y cambios de módulo. Sin notas `>`: las fuentes van en la cabecera y solo se copia el texto entre las líneas INICIO y FIN (4.500 caracteres como mucho). Lo comprueba `casos/atencion-es/codigo/comprobar_prompts.py` |

## Reglas
- Las líneas que empiezan por `>` son notas (origen, contradicciones, lo que falta decidir) y **no van al
  prompt**.
- Lo que depende de un bot (sus herramientas, sus variables, sus colas propias) no va en el bloque: se
  marca como «Se queda en cada bot» o «Enganche por bot».
- Un bloque no se publica solo: entra en un bot con una versión nueva de ese bot, siguiendo el proceso de
  siempre (fork, prompt guardado en el caso, decisión y PR).
