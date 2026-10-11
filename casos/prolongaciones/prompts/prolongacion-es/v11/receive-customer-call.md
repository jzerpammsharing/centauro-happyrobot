<!-- workflow: 01a0d9de-b1cd-7bc9-bafc-f5117bd57249 · versión: Version 11 (2g1bxzyzazpp) · nodo: Receive Customer Call · copiado: 2026-10-11 -->

Inbound Voice Agent (AI Agent). Persistent ID `01a0da07-a2b9-7e69-942f-fca238dc2334`. El prompt está en
su hijo «Prolongacion» (`prolongacion.md`).

## Contexto de transcripción (transcription_context)

Customer calling Centauro Rent A Car to extend (prolongar) an ongoing car rental. Topics include centauro.net customer area, Mi cuenta, password reset, Mis reservas y facturas, Gestionar mi reserva, Prolongar mi reserva, Booking, return date and time, penalties, replacement cars from insurers.

## Configuración

| Campo | Valor |
|---|---|
| call | Inbound Call (`01a0da06-7f3b-7b5a-9af0-e424300d057c`) |
| agent.name | Daniel Prolongaciones |
| voices | Pablo Galvez HR (`gjc70xusrf87`), Pablo HR (`qu8u116mgo20`), Bruno HR (`oducf8l3pytd`) |
| languages | es, en, it, pt |
| language_accents | es, en, it, pt-pt |
| background | Call center (`call-center.8k.wav`) |
| custom_recording_id | `{{01a0da06-917d-7e9c-9b1c-153df5946a48.recording_id}}` (aviso legal grabado) |
| enable_ring_cxiva | true |
| recording_style / recording_language | (vacío) |

En la configuración no aparece `max_call_duration`. El corte de unos 600 s (`max_duration_reached`)
se ha visto en los runs.
