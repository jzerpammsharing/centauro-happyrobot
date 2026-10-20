<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v2 (x8xd0llbdp3j) · nodo: Receive Customer Call · copiado: 2026-10-19 (Tarea 13) -->

# Receive Customer Call (agente de voz)

- Tipo: Inbound Voice Agent, event_id `0192e5dc-08df-78bf-a549-f43c6bf9f087`. ID de nodo en la v2
  `01a14f1d-0394-725e-8b8f-bdd2b3ee34cc` · persistent_id `300ae88d-ccb2-466c-a914-9f9090363a74`.
- Padre: «Resolver colas» (el Paths «Entrada» y su condición «Siempre» se quitaron en el editor el 20/10/2026, R10). Hijos: prompt «Triaje» y extract
  «Registrar resultado de la llamada».
- Spec §5.11: una sola voz, idiomas es/en/it/pt, fondo de call center, `transcription_context` ampliado y sin horario
  comercial en el nodo (el modo virtual lo decide el prompt y lo asegura «Preparar transferencia», D-004).

## Cambios de la Tarea 13 (19/10/2026)

| Campo | Antes (copia de la v25) | Ahora |
|---|---|---|
| `agent.voices` | una sola voz, «Pablo Galvez HR» (`gjc70xusrf87`) | sin cambios: ya era la única |
| `transcription_context` | minibús, puntos de encuentro, terminales y números de reserva (en inglés) | además oficinas, prolongaciones, contraseña, correos deletreados, número de reserva, nombre y fecha de nacimiento, fianza, combustible y cargos |
| `business_hours_setting_name` | `"default"` (no existe en este workflow; R12) | `""` (vacío) |

El resto no cambia: `agent.name` «Shuttle Prompt», idiomas es/en/it/pt y acentos es/en/it/pt-pt, fondo «Call center»,
`enable_ring_cxiva` true, grabación del aviso legal `custom_recording_id` dinámica con
`{{e51cd732-f403-4ef7-95d4-490347960a93.recording_id}}` (la URL firmada del valor estático no se copia: `<URL_FIRMADA>`).
`respect_business_hours` no está definido (falso por defecto).

## Configuración

```json
{
  "call": {"type": "static", "static": {"id": "33c2681a-9160-413c-8010-e455bd4023c6", "name": "Inbound Call"}},
  "agent": {
    "name": "Shuttle Prompt",
    "voices": [{"type": "static", "static": {"id": "gjc70xusrf87", "name": "Pablo Galvez HR"}}],
    "languages": ["es Spanish", "en English", "it Italian", "pt Portuguese"],
    "language_accents": ["es Spanish", "en English", "it Italian", "pt-pt Portuguese (Portugal)"]
  },
  "background": "Call center (call-center.8k.wav)",
  "recording_style": "",
  "enable_ring_cxiva": true,
  "recording_language": "",
  "custom_recording_id": {"type": "dynamic", "static": {"id": "019feaea-eea1-7139-a9ae-07e639c52456", "media_url": "<URL_FIRMADA>", "duration_ms": 23771},
                          "dynamic": "{{e51cd732-f403-4ef7-95d4-490347960a93.recording_id}}"},
  "transcription_context": "Customer calling Centauro Rent A Car (car rental in Spain). Topics: courtesy shuttle (minibús) and airport meeting points, airport terminals and shuttle pickup locations; office opening hours, addresses and where to return the car; extending a rental (prolongar, prolongación, alargar el alquiler, devolver más tarde); the customer area password (contraseña, área de cliente, «¿Has olvidado tu contraseña?»); email addresses spelled out letter by letter (arroba, punto, guion, guion bajo, gmail, hotmail, outlook, yahoo); booking numbers (número de reserva: letters and digits, for example ER followed by eight digits); full name and date of birth; deposit, fuel, charges and refunds.",
  "business_hours_setting_name": ""
}
```

(`agent.name`, los idiomas, el fondo y `transcription_context` van en HappyRobot como Plate o `templated_value`; aquí
se resumen.)
