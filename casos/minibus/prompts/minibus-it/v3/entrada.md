<!-- workflow: 01a03a65-3700-74c1-9c7b-e9c708833c4b · versión: v3 (jgkjecsoaxp4) · nodo: Entrada · copiado: 2026-10-12 -->

# Entrada

- Tipo: Paths (Conditions), antes «Horario de atencion».
- Ramas: «Siempre» (antes «En horario») y «Fallback», que se queda sin hijos.
- Igual que «Entrada» de ES v22: la rama «Siempre» se cumple con `idioma_colas` vacío o no vacío; el modo virtual lo decide el prompt.
- Se borra la rama nocturna de la v anterior («Idioma fuera de horario», «Derivacion nocturna ES/EN», `transferir_a_cola_nocturna` y sus transferencias).

```json
[{"title": "Siempre: el horario lo marca la IVR y el modo virtual lo decide el prompt", "ors": [
  {"ands": [{"field": {"group_id": "4e0b9531-326f-4c5f-8f49-bbe460868570", "variable_id": "idioma_colas"}, "condition": "is_not_empty"}]},
  {"ands": [{"field": {"group_id": "4e0b9531-326f-4c5f-8f49-bbe460868570", "variable_id": "idioma_colas"}, "condition": "is_empty"}]}
]}]
```
