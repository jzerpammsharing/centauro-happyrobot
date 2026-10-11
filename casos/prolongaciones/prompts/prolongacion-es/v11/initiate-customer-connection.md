<!-- workflow: 01a0d9de-b1cd-7bc9-bafc-f5117bd57249 · versión: Version 11 (2g1bxzyzazpp) · nodo: Initiate customer connection · copiado: 2026-10-11 -->

Acción «Transfer» (Phone calls), hija de la herramienta `transfer_to_human_agent`. Persistent ID
`01a0da09-043d-70ea-8460-0b0db98c258f`. Variables como `{{persistent_id.variable}}`:
`0f790e71-…` = herramienta transfer_to_human_agent, `01a0da07-411e-…` = Resolver colas por idioma,
`01a0da06-917d-…` = Calcular idioma y saludo.

## Mensaje de susurro (whisper) al agente que coge la llamada

Llamada del asistente de prolongaciones. {{0f790e71-8013-43e1-864b-914666f034b2.resumen_para_agente}} Teléfono del cliente: {{01a0da06-917d-7e9c-9b1c-153df5946a48.telefono_dictado}}.

## Configuración

| Campo | Valor |
|---|---|
| agent | Receive Customer Call (`01a0da07-a2b9-7e69-942f-fca238dc2334`) |
| number | `{{0f790e71-8013-43e1-864b-914666f034b2.extension_destino}}` |
| fallback_number | `{{01a0da07-411e-71c5-84ce-499952b43d8e.cola_gestion_reserva}}` |
| extension | (vacío) |
| from_number | (vacío) |
| whisper_transfer | true |
| skip_digit_press | false (el agente tiene que pulsar 1) |
| skip_handoff_message | true |
| warm_handoff | false |
| warm_handoff_intro_mode | default |
| enableSpokenDigit | false |
| record_transfer_conversation | true |
| stop_recording_on_transfer | false |
| uui_encoding / uui_data_format | ascii / text |
| headers | [] |

No figura un `transfer_timeout` explícito; el corte a los 300 s (`whisper_transfer_timeout`) se ha
observado en los runs.
