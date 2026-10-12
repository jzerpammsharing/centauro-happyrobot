<!-- workflow: 01a03a65-3700-74c1-9c7b-e9c708833c4b · versión: v3 (jgkjecsoaxp4) · nodo: Initiate customer connection (hijas de transfer_to_human_agent de Triaje y horario y Punto de encuentro) · copiado: 2026-10-12 -->

# Transferencias «Initiate customer connection» (v3)

- Event ID: `01926f25-dacb-710e-a823-4254189111dd`. Misma configuración que ES v22; el whisper va en el idioma de las colas del país.

## Hija del transfer de «Triaje y horario»

- persistent_id: `845ab48d-5f29-40b8-870f-8fe93a02ca16`
- Padre: transfer_to_human_agent `7a3776a5-7ee5-4031-81c7-0e3bd02c31c9`

```json
{
  "agent": {
    "type": "static",
    "static": {
      "id": "8156783c-8dd2-4c3d-87ce-d42310d4c2f3",
      "name": "Receive Customer Call"
    }
  },
  "number": "{{7a3776a5-7ee5-4031-81c7-0e3bd02c31c9.extension_destino}}",
  "headers": [],
  "extension": "",
  "from_number": "",
  "uui_encoding": "ascii",
  "warm_handoff": false,
  "fallback_number": "{{4e0b9531-326f-4c5f-8f49-bbe460868570.cola_horario_minibus}}",
  "uui_data_format": "text",
  "whisper_message": "Chiamata dall'assistente del minibus. {{7a3776a5-7ee5-4031-81c7-0e3bd02c31c9.resumen_para_agente}} Telefono del cliente: {{3b1e91ac-f471-47a9-b175-8408c58d826f.telefono_dictado}}.",
  "skip_digit_press": false,
  "whisper_transfer": true,
  "enableSpokenDigit": false,
  "skip_handoff_message": true,
  "warm_handoff_intro_mode": "default",
  "stop_recording_on_transfer": false,
  "record_transfer_conversation": true
}
```

## Hija del transfer de «Punto de encuentro»

- persistent_id: `d034a001-6674-4ca3-bd61-208c329735cc`
- Padre: transfer_to_human_agent `d37cbb84-a6a7-4dc6-928e-03c871087eef`

```json
{
  "agent": {
    "type": "static",
    "static": {
      "id": "8156783c-8dd2-4c3d-87ce-d42310d4c2f3",
      "name": "Receive Customer Call"
    }
  },
  "number": "{{d37cbb84-a6a7-4dc6-928e-03c871087eef.extension_destino}}",
  "headers": [],
  "extension": "",
  "from_number": "",
  "uui_encoding": "ascii",
  "warm_handoff": false,
  "fallback_number": "{{4e0b9531-326f-4c5f-8f49-bbe460868570.cola_horario_minibus}}",
  "uui_data_format": "text",
  "whisper_message": "Chiamata dall'assistente del minibus. {{d37cbb84-a6a7-4dc6-928e-03c871087eef.resumen_para_agente}} Telefono del cliente: {{3b1e91ac-f471-47a9-b175-8408c58d826f.telefono_dictado}}.",
  "skip_digit_press": false,
  "whisper_transfer": true,
  "enableSpokenDigit": false,
  "skip_handoff_message": true,
  "warm_handoff_intro_mode": "default",
  "stop_recording_on_transfer": false,
  "record_transfer_conversation": true
}
```
