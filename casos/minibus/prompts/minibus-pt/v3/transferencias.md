<!-- workflow: 01a05977-3a33-76da-acb2-a757f3947cf9 · versión: v3 (2139o3pf25qm) · nodo: Initiate customer connection (hijas de transfer_to_human_agent de Triaje y horario y Punto de encuentro) · copiado: 2026-10-12 -->

# Transferencias «Initiate customer connection» (v3)

- Event ID: `01926f25-dacb-710e-a823-4254189111dd`. Misma configuración que ES v22; el whisper va en el idioma de las colas del país.

## Hija del transfer de «Triaje y horario»

- persistent_id: `39a2aa34-5703-4f2f-9e0b-8d318198b78a`
- Padre: transfer_to_human_agent `302bc6a5-b38f-4baf-9b2c-c62e533e3b2c`

```json
{
  "agent": {
    "type": "static",
    "static": {
      "id": "af5a7237-13fe-4b86-b7f5-4f96b1d61c5b",
      "name": "Receive Customer Call"
    }
  },
  "number": "{{302bc6a5-b38f-4baf-9b2c-c62e533e3b2c.extension_destino}}",
  "headers": [],
  "extension": "",
  "from_number": "",
  "uui_encoding": "ascii",
  "warm_handoff": false,
  "fallback_number": "{{96b01012-31c0-4328-9bb4-1650bcdbf1dc.cola_horario_minibus}}",
  "uui_data_format": "text",
  "whisper_message": "Chamada do assistente do minibus. {{302bc6a5-b38f-4baf-9b2c-c62e533e3b2c.resumen_para_agente}} Telefone do cliente: {{0f85067a-078e-4a21-9b45-0d5bfb92dd8e.telefono_dictado}}.",
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

- persistent_id: `1e31ce4b-83c5-46b4-84e5-a26dc2d3bc42`
- Padre: transfer_to_human_agent `9e8601c0-cab7-49de-9590-785d03341d87`

```json
{
  "agent": {
    "type": "static",
    "static": {
      "id": "af5a7237-13fe-4b86-b7f5-4f96b1d61c5b",
      "name": "Receive Customer Call"
    }
  },
  "number": "{{9e8601c0-cab7-49de-9590-785d03341d87.extension_destino}}",
  "headers": [],
  "extension": "",
  "from_number": "",
  "uui_encoding": "ascii",
  "warm_handoff": false,
  "fallback_number": "{{96b01012-31c0-4328-9bb4-1650bcdbf1dc.cola_horario_minibus}}",
  "uui_data_format": "text",
  "whisper_message": "Chamada do assistente do minibus. {{9e8601c0-cab7-49de-9590-785d03341d87.resumen_para_agente}} Telefone do cliente: {{0f85067a-078e-4a21-9b45-0d5bfb92dd8e.telefono_dictado}}.",
  "skip_digit_press": false,
  "whisper_transfer": true,
  "enableSpokenDigit": false,
  "skip_handoff_message": true,
  "warm_handoff_intro_mode": "default",
  "stop_recording_on_transfer": false,
  "record_transfer_conversation": true
}
```
