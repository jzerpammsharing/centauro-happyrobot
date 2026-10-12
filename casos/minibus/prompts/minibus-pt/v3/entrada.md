<!-- workflow: 01a05977-3a33-76da-acb2-a757f3947cf9 · versión: v3 (2139o3pf25qm) · nodo: Entrada · copiado: 2026-10-12 -->

# Entrada

- Tipo: Paths (Conditions), antes «Horario de atencion».
- Ramas: «Siempre» (antes «En horario») y «Fallback», que se queda sin hijos.
- Igual que «Entrada» de ES v22: la rama «Siempre» se cumple con `idioma_colas` vacío o no vacío; el modo virtual lo decide el prompt.
- Se borra la rama nocturna de la v anterior («Idioma fuera de horario», «Derivacion nocturna ES/EN», `transferir_a_cola_nocturna` y sus transferencias).

```json
[{"title": "Siempre: el horario lo marca la IVR y el modo virtual lo decide el prompt", "ors": [
  {"ands": [{"field": {"group_id": "96b01012-31c0-4328-9bb4-1650bcdbf1dc", "variable_id": "idioma_colas"}, "condition": "is_not_empty"}]},
  {"ands": [{"field": {"group_id": "96b01012-31c0-4328-9bb4-1650bcdbf1dc", "variable_id": "idioma_colas"}, "condition": "is_empty"}]}
]}]
```
