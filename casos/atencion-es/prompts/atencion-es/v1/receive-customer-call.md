<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v1 (veavliy3k6jx) · nodo: Receive Customer Call · copiado: 2026-10-18 -->

# Receive Customer Call

- Tipo: Inbound Voice Agent (integración AI Agent), event_id `0192e5dc-08df-78bf-a549-f43c6bf9f087`
- Persistent ID: `300ae88d-ccb2-466c-a914-9f9090363a74`
- Padre: condición «Siempre» del Paths «Entrada»
- Hijos: prompt «Triaje y horario» y extract «Registrar resultado de la llamada»

El nodo no guarda prompt, mensaje inicial ni modelo: el prompt y el modelo están en el nodo hijo «Triaje y
horario» (ver `triaje-y-horario.md`). Los campos que no aparecen abajo (interrupciones, timeouts, keywords,
velocidad, temperatura…) no están definidos en el nodo y usan los valores por defecto de la plataforma.
La URL firmada de la grabación del aviso legal se ha sustituido por `<URL_FIRMADA>`.

Dos cosas que dependen del workflow y **no** se han copiado con el duplicado (ver `docs/pendientes.md`):
`business_hours_setting_name` apunta a `"default"`, y los ajustes del workflow (`out_of_office_hours`,
auditorías) vienen vacíos en el workflow nuevo.

## Configuración

```json
{
  "call": {
    "type": "static",
    "static": {
      "id": "33c2681a-9160-413c-8010-e455bd4023c6",
      "name": "Inbound Call"
    }
  },
  "agent": {
    "name": [{"type": "paragraph", "children": [{"text": "Shuttle Prompt"}]}],
    "voices": [
      {"type": "static", "static": {"id": "gjc70xusrf87", "name": "Pablo Galvez HR"}}
    ],
    "languages": [
      {"type": "static", "static": {"id": "es", "name": "Spanish"}},
      {"type": "static", "static": {"id": "en", "name": "English"}},
      {"type": "static", "static": {"id": "it", "name": "Italian"}},
      {"type": "static", "static": {"id": "pt", "name": "Portuguese"}}
    ],
    "language_accents": [
      {"type": "static", "static": {"id": "es", "name": "Spanish"}},
      {"type": "static", "static": {"id": "en", "name": "English"}},
      {"type": "static", "static": {"id": "it", "name": "Italian"}},
      {"type": "static", "static": {"id": "pt-pt", "name": "Portuguese (Portugal)"}}
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
      "media_url": "<URL_FIRMADA>",
      "duration_ms": 23771
    },
    "dynamic": "{{e51cd732-f403-4ef7-95d4-490347960a93.recording_id}}"
  },
  "transcription_context": "Customer calling about Centauro Rent A Car courtesy shuttle and airport meeting points. Topics include booking numbers, airport terminals, and shuttle pickup locations.",
  "business_hours_setting_name": "default"
}
```

`dynamic` y `transcription_context` se muestran aplanados (en el nodo son campos de texto enriquecido de
Plate). El `custom_recording_id` dinámico elige el aviso legal en español o en inglés según el idioma
(`recording_id` de «Calcular horario nocturno»).
