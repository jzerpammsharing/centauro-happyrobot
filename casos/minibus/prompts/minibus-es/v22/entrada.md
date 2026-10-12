<!-- workflow: 019f7594-2cce-7eed-b995-dd9ea64a1062 · versión: v22 (2l6skwt8wphb) · nodo: Entrada · copiado: 2026-10-11 -->

# Entrada

- Tipo: Paths (Conditions)
- Persistent ID: 019ffd30-5d6a-78f7-9575-82afe132e5c3
- Padre: «Resolver colas por idioma»
- Configuración: ninguna (_No configuration set_)
- Ramas: «Siempre» (orden 0) y «Fallback» (orden -1)

## Rama «Siempre»

- Tipo de condición: conditional · Orden: 0
- Persistent ID: 019ffd30-5d6a-78f7-9575-82b034d74fb6
- Hijo: «Receive Customer Call»

```json
[
  {
    "id": "0b73a6ba-8fa1-4fea-93a8-6062da8965a6",
    "ors": [
      {
        "ands": [
          {
            "field": {
              "group_id": "019feb2c-0554-7b99-a980-42f896779230",
              "variable_id": "idioma_colas"
            },
            "condition": "is_not_empty"
          }
        ]
      },
      {
        "ands": [
          {
            "field": {
              "group_id": "019feb2c-0554-7b99-a980-42f896779230",
              "variable_id": "idioma_colas"
            },
            "condition": "is_empty"
          }
        ]
      }
    ],
    "title": "Siempre: el horario lo marca la IVR y el modo virtual lo decide el prompt"
  }
]
```

## Rama «Fallback»

- Tipo de condición: fallback · Orden: -1
- Persistent ID: 019ffd30-5d6b-7ab8-9db0-6e41a2fff93e
- Hijos: ninguno

```json
[
  {
    "id": "dde48e58-85ea-45c1-8729-c26826a37ac0",
    "ors": [
      {
        "id": "e581615b-6cc5-4486-9541-0e188a3c7f91",
        "ands": [
          {
            "id": "58dacc7d-48fb-4c69-b783-6631ab6f3059"
          }
        ]
      }
    ]
  }
]
```
