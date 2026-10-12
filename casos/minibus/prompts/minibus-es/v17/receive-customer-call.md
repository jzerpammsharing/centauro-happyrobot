<!-- workflow: 019f7594-2cce-7eed-b995-dd9ea64a1062 · versión: v17 (i0syf61bujsz) · nodo: Receive Customer Call · copiado: 2026-10-11 -->

# Receive Customer Call

- Tipo: Inbound Voice Agent (integración AI Agent)
- Persistent ID: 019f8045-5a02-7105-9e51-23b284430c73
- Padre: condición «Siempre»
- Hijos: prompt «Triaje y horario» (modelo gpt-4.1-fast) y extract «Registrar resultado de la llamada»

El nodo no guarda prompt, mensaje inicial ni modelo: el prompt y el modelo están en el nodo hijo «Triaje y horario» (ver `triaje-y-horario.md`). Los campos que no aparecen abajo (interrupciones, timeouts, keywords, velocidad, temperatura…) no están definidos en el nodo y usan los valores por defecto de la plataforma.

## Configuración

```json
{
  "call": {
    "type": "static",
    "static": {
      "id": "019f7594-d64b-778e-bc23-1d0b6d94d240",
      "name": "Inbound Call"
    }
  },
  "agent": {
    "name": [
      {
        "type": "paragraph",
        "children": [
          {
            "text": "Shuttle Prompt"
          }
        ]
      }
    ],
    "voices": [
      {
        "type": "static",
        "static": {
          "id": "gjc70xusrf87",
          "name": "Pablo Galvez HR"
        }
      }
    ],
    "languages": [
      {
        "type": "static",
        "static": {
          "id": "es",
          "name": "Spanish"
        }
      },
      {
        "type": "static",
        "static": {
          "id": "en",
          "name": "English"
        }
      },
      {
        "type": "static",
        "static": {
          "id": "it",
          "name": "Italian"
        }
      },
      {
        "type": "static",
        "static": {
          "id": "pt",
          "name": "Portuguese"
        }
      }
    ],
    "language_accents": [
      {
        "type": "static",
        "static": {
          "id": "es",
          "name": "Spanish"
        }
      },
      {
        "type": "static",
        "static": {
          "id": "en",
          "name": "English"
        }
      },
      {
        "type": "static",
        "static": {
          "id": "it",
          "name": "Italian"
        }
      },
      {
        "type": "static",
        "static": {
          "id": "pt-pt",
          "name": "Portuguese (Portugal)"
        }
      }
    ]
  },
  "background": {
    "type": "static",
    "static": {
      "id": "https://storage.googleapis.com/happyrobot-public/backgrounds/call-center.8k.wav",
      "name": "Call center",
      "description": "https://storage.googleapis.com/happyrobot-public/backgrounds/call-center.8k.wav"
    }
  },
  "recording_style": "",
  "enable_ring_cxiva": true,
  "recording_language": "",
  "custom_recording_id": {
    "type": "dynamic",
    "static": {
      "id": "019feaea-eea1-7139-a9ae-07e639c52456",
      "media_url": "https://storage.googleapis.com/happyrobot-audio-assets-eu/019d1ff1-108b-7b48-b8d0-a7011f552bfc/audio-assets/41982936-8119-4b2f-a211-d1ca08a354da.wav?[REDACTADO: URL firmada]",
      "duration_ms": 23771
    },
    "dynamic": [
      {
        "type": "paragraph",
        "children": [
          {
            "text": ""
          },
          {
            "type": "variable",
            "children": [
              {
                "text": ""
              }
            ],
            "group_id": "019fd418-5a5d-7bd4-93f8-eae309f8dc7a",
            "variable_id": "recording_id"
          },
          {
            "text": ""
          }
        ]
      }
    ]
  },
  "transcription_context": [
    {
      "type": "paragraph",
      "children": [
        {
          "text": "Customer calling about Centauro Rent A Car courtesy shuttle and airport meeting points. Topics include booking numbers, airport terminals, and shuttle pickup locations."
        }
      ]
    },
    {
      "type": "paragraph",
      "children": [
        {
          "text": ""
        }
      ]
    },
    {
      "type": "paragraph",
      "children": [
        {
          "text": ""
        }
      ]
    }
  ],
  "business_hours_setting_name": "default"
}
```
