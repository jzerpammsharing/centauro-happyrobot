<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v1 (veavliy3k6jx) · nodo: Entrada · copiado: 2026-10-18 -->

# Entrada

- Tipo: Paths (Conditions), event_id `24d80afe-e0b7-438a-93aa-0b5db5149447`
- Persistent ID: `3380d3e5-8e28-4cd1-bc12-66646795e46c`
- Padre: «Resolver colas por idioma»
- Configuración: ninguna (`_No configuration set_`)
- Ramas: «Siempre» (orden 0) y «Fallback» (orden -1, vacía)
- En la v2 se borró «Fallback» (vacía) y se dejó «Entrada» + «Siempre»: borrar un nodo borra todo su subárbol
  y no se puede reenganchar el agente por API (ver `docs/pendientes.md`).

## Rama «Siempre»

- Tipo de condición: conditional · Orden: 0
- Persistent ID: `34d2bf66-5e03-4e89-b1dc-02c4d7f5b3af`
- Hijo: «Receive Customer Call»

```json
[
  {
    "id": "0b73a6ba-8fa1-4fea-93a8-6062da8965a6",
    "ors": [
      {"ands": [{"field": {"group_id": "081e2b5d-b260-41a6-bd2a-6f82b26193d1", "variable_id": "idioma_colas"}, "condition": "is_not_empty"}]},
      {"ands": [{"field": {"group_id": "081e2b5d-b260-41a6-bd2a-6f82b26193d1", "variable_id": "idioma_colas"}, "condition": "is_empty"}]}
    ],
    "title": "Siempre: el horario lo marca la IVR y el modo virtual lo decide el prompt"
  }
]
```

## Rama «Fallback»

- Tipo de condición: fallback · Orden: -1
- Persistent ID: `3128fb5a-0c53-40a4-a40b-2c0c4f4c2d7b`
- Sin hijos.

```json
[
  {
    "id": "dde48e58-85ea-45c1-8729-c26826a37ac0",
    "ors": [{"id": "e581615b-6cc5-4486-9541-0e188a3c7f91", "ands": [{"id": "58dacc7d-48fb-4c69-b783-6631ab6f3059"}]}]
  }
]
```
