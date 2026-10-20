<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v1 (veavliy3k6jx) · nodo: Module Change (4) · copiado: 2026-10-18 -->

# Module Change (v1)

Los 4 nodos `module-change` que trae el duplicado de la v25. Cada uno cuelga de una herramienta y devuelve la
conversación a un módulo (prompt) ya abierto. **Los cuatro apuntan a nodos del workflow nuevo** (el duplicado
reasigna `moduleId` y `modulePersistentId`), no a los de Minibús ES.

Salida de cada Module Change: `called` (boolean) y `callCount` (number).

| # | persistent_id | Cuelga de la herramienta | Módulo de origen | Salta a (módulo) | moduleId / modulePersistentId |
|---|---|---|---|---|---|
| 1 | `91b601ad-4782-44fb-955a-5bc42657c191` | `informacion_oficina` (`0be9b6d8-9353-41de-8049-c2e477ed6668`) | Prolongación y consultas | Información de oficina | `0c60218b-8901-47bd-95de-40e0e1af1296` |
| 2 | `081b2d5c-d7cf-49b7-b0a1-70c82ee5aac7` | `buscar_punto_de_encuentro` (`eda4aa10-c99e-4319-b7ae-dbf5dc6db949`) | Prolongación y consultas | Punto de encuentro | `a80fca22-b295-41e3-a735-a3c878af4eee` |
| 3 | `9661e3bd-a18e-477b-8076-96c76caae15b` | `consultas_alquiler` (`6edd13ac-b226-4d1c-87dc-748b46ce5638`) | Información de oficina | Prolongación y consultas | `38378785-0846-4920-b41a-583f7c5773fb` |
| 4 | `7f70daef-fdf6-4f51-86b0-43a61e626efc` | `consultas_alquiler` (`3f1c2be8-8768-455f-895b-047063ea7938`) | Punto de encuentro | Prolongación y consultas | `38378785-0846-4920-b41a-583f7c5773fb` |

Configuración de cada nodo (ejemplo, el nº 1):

```json
{
  "moduleId": "0c60218b-8901-47bd-95de-40e0e1af1296",
  "modulePersistentId": "0c60218b-8901-47bd-95de-40e0e1af1296"
}
```

Las herramientas del Triaje (`buscar_punto_de_encuentro`, `informacion_oficina`, `consultas_alquiler`) no llevan
Module Change: su hijo es directamente el prompt del módulo de destino. «Punto de encuentro» e «Información de
oficina» no se enlazan entre sí en la v25 (solo con «Prolongación y consultas»), y ninguno de los tres módulos
tiene hoy un camino de vuelta al Triaje (queda por comprobar que un Module Change pueda apuntar al Triaje; ver
`docs/pendientes.md`).
