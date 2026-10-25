<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v3 (5cu7jiosi6n7) · nodo: Inbound Call · actualizado: 2026-10-22 (D-018) -->

# Inbound Call (trigger) · v3

- Tipo: trigger «Inbound to number», event_id `0192a20c-cb70-7bf2-977a-b7edc14dcd66`. ID de nodo en la v3
  `01a16336-eef9-7832-be88-f82fde4331cd` · persistent_id `33c2681a-9160-413c-8010-e455bd4023c6`.
- En la v1 y la v2, sin números (a propósito). En la v3, una línea, para la prueba de una hora en producción con la
  línea de Prolongación en español (D-018, `docs/procedimiento-lineas.md`, apartado 8):

```json
{
  "numbers": [
    {"id": "<id de la línea en HappyRobot>", "name": "<LINEA_PROLONGACION_ES>", "type": "sip", "number": "<LINEA_PROLONGACION_ES>"}
  ]
}
```

- Es la misma línea que la V11 de Prolongaciones tiene en su trigger; el número real se lee de ese trigger o de
  `manage_phone_numbers` (no se copia aquí).
- Comprobado el 22/10/2026 con `manage_phone_numbers action=usage`: HappyRobot deja tener la línea en el borrador de
  la v3 mientras la V11 la tiene publicada. **Por comprobar al publicar:** si deja publicar la v3 con la línea mientras
  la V11 siga publicada con ella (por eso el orden del apartado 8 publica antes la V13, que no la lleva).
- En «Contexto de la llamada», `LINEAS` ya reconoce esta línea como `("prolongacion", "es")`.
