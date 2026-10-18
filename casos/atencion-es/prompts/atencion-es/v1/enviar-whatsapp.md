<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v1 (veavliy3k6jx) · nodo: ¿Enviar WhatsApp? y Enviar WhatsApp del punto de encuentro · copiado: 2026-10-18 -->

# ¿Enviar WhatsApp? (Paths) y Enviar WhatsApp del punto de encuentro

Cadena final de la llamada: «Registrar resultado de la llamada» → «Registrar consultas del alquiler» →
«Preparar WhatsApp minibús» → Paths «¿Enviar WhatsApp?» → rama «Enviar» → «Enviar WhatsApp del punto de encuentro».

En la configuración del nodo «Enviar WhatsApp del punto de encuentro» se han sustituido el número remitente de
WhatsApp por `<TELEFONO_WHATSAPP_NEGOCIO>`, los identificadores de la cuenta y del número de Meta por
`<ID_CUENTA_WHATSAPP>` y `<ID_NUMERO_WHATSAPP>`, y la credencial por `<CREDENCIAL_WHATSAPP>`.

## Paths «¿Enviar WhatsApp?»

- Tipo: Paths (Conditions), event_id `24d80afe-e0b7-438a-93aa-0b5db5149447`
- Persistent ID: `d7bea790-20cc-431d-b696-edd7f09b51e3`
- Padre: «Preparar WhatsApp minibús»
- Configuración: `{"policy": null}`

### Rama «Enviar»

- Tipo de condición: conditional · Orden: 0
- Persistent ID: `09675b8f-685e-43b7-abd9-15ce07f31077`
- Hijo: «Enviar WhatsApp del punto de encuentro»

```json
[
  {
    "id": "enviar-whatsapp",
    "ors": [
      {"ands": [{"field": {"group_id": "4bd059bb-837c-4242-845f-7fc802c0f937", "variable_id": "enviar"}, "condition": "boolean_true"}]}
    ]
  }
]
```

### Rama «Fallback» (por defecto, vacía; añadida en la v25)

- Tipo de condición: fallback · Orden: 1
- Persistent ID: `5b4c35c5-2b47-47f0-b066-22eaf8c3ada3`
- Sin hijos.

## Enviar WhatsApp del punto de encuentro

- Tipo: Send WhatsApp (integración WhatsApp), event_id `eef26438-f118-4680-a43f-d1f1b07485f7`
- Persistent ID: `cbb87a1f-4994-49ea-872b-501640029b45`
- Padre: rama «Enviar»

```json
{
  "to": "{{4bd059bb-837c-4242-845f-7fc802c0f937.telefono}}",
  "business": {"type": "static", "static": {"id": "<ID_CUENTA_WHATSAPP>", "name": "Business <ID_CUENTA_WHATSAPP>"}},
  "credentialId": "<CREDENCIAL_WHATSAPP>",
  "phone_number": {"type": "static", "static": {"id": "<ID_NUMERO_WHATSAPP>", "name": "<TELEFONO_WHATSAPP_NEGOCIO>", "disabled": false}},
  "business_account": {"type": "static", "static": {"id": "<ID_CUENTA_WHATSAPP>", "name": "Business <ID_CUENTA_WHATSAPP>"}},
  "templateConfig": {
    "inputMode": "static",
    "parameters": {
      "body_aeropuerto": "{{4bd059bb-837c-4242-845f-7fc802c0f937.var_aeropuerto}}",
      "body_frecuencia": "{{4bd059bb-837c-4242-845f-7fc802c0f937.var_frecuencia}}",
      "body_indicaciones": "{{4bd059bb-837c-4242-845f-7fc802c0f937.var_indicaciones}}",
      "body_descripcion_minibus": "{{4bd059bb-837c-4242-845f-7fc802c0f937.var_descripcion}}"
    },
    "templateId": "minibus_punto_texto_boton",
    "templateName": "minibus_punto_texto_boton",
    "templateMetadata": {
      "status": "APPROVED",
      "category": "UTILITY",
      "language": "es",
      "components": [
        {"text": "Punto de encuentro del minibús", "type": "HEADER", "format": "TEXT"},
        {
          "text": "Hola, le escribimos de Centauro Rent a Car tras su llamada.\n\nPunto de encuentro del minibús gratuito en {{aeropuerto}}:\n{{indicaciones}}\n\nEl minibús es {{descripcion_minibus}} y pasa cada {{frecuencia}}. Espere en ese punto y le recogerá.",
          "type": "BODY",
          "example": {
            "body_text_named_params": [
              {"example": "Madrid T1", "param_name": "aeropuerto"},
              {"example": "Salga de la terminal, gire a la derecha y camine unos 150 m hasta el cartel verde \"Hotel Bus\", justo enfrente de la Consigna de Equipaje. Ahí espera el minibús.", "param_name": "indicaciones"},
              {"example": "blanco o amarillo, con el logo de Centauro", "param_name": "descripcion_minibus"},
              {"example": "20 minutos", "param_name": "frecuencia"}
            ]
          }
        },
        {"text": "Mensaje automático. Si lo necesita, llámenos.", "type": "FOOTER"},
        {"type": "BUTTONS", "buttons": [{"url": "https://www.buscentauro.com/", "text": "Ver minibús en directo", "type": "URL"}]}
      ]
    }
  }
}
```

Los campos de texto enriquecido de Plate (`to` y los `body_*`) se muestran aplanados a `{{persistent_id.variable}}`.
