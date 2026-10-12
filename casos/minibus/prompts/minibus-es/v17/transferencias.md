<!-- workflow: 019f7594-2cce-7eed-b995-dd9ea64a1062 · versión: v17 (i0syf61bujsz) · nodo: Initiate customer connection (hijas de transfer_to_human_agent de Triaje y horario, Punto de encuentro e Información de oficina) · copiado: 2026-10-11 -->

# Transferencias «Initiate customer connection» (v17)

- Event ID de los tres nodos: `01926f25-dacb-710e-a823-4254189111dd`.
- Los campos Plate (`number`, `fallback_number`, `extension`, `whisper_message`, `transfer_timeout`) se han aplanado a texto con `{{persistent_id.variable}}`, sin los nodos de texto vacíos que añade el editor. Los persistent_id son los mismos en v17 y v22.
- Se mantiene el orden de claves de la API.

## 1. Hija del transfer de «Triaje y horario»

- persistent_id: `019f8463-09df-7f93-bb39-83985f3097a4`
- Padre: transfer_to_human_agent `019f8461-4b58-75df-9ea4-7569ab2dc75b`

```json
{
  "agent": {
    "type": "static",
    "static": {
      "id": "019f8045-5a02-7105-9e51-23b284430c73",
      "name": "Receive Customer Call"
    }
  },
  "number": "{{019f8461-4b58-75df-9ea4-7569ab2dc75b.extension_destino}}",
  "fallback_number": "{{019feb2c-0554-7b99-a980-42f896779230.cola_horario_minibus}}"
}
```

## 2. Hija del transfer de «Punto de encuentro»

- persistent_id: `019fd42c-c2e5-7940-b44c-d2ab6ddbb8fb`
- Padre: transfer_to_human_agent `09353184-6e92-450d-a8b2-94f556b356ae`

```json
{
  "agent": {
    "type": "static",
    "static": {
      "id": "019f8045-5a02-7105-9e51-23b284430c73",
      "name": "Receive Customer Call"
    }
  },
  "number": "{{09353184-6e92-450d-a8b2-94f556b356ae.extension_destino}}",
  "headers": [],
  "fallback_number": "{{019feb2c-0554-7b99-a980-42f896779230.cola_horario_minibus}}"
}
```

## 3. Hija del transfer de «Información de oficina»

- persistent_id: `01a103fb-1a5d-7024-8833-b57401e93937`
- Padre: transfer_to_human_agent `01a103fb-1a54-7564-a74e-03cdc4d4a656`

```json
{
  "agent": {
    "type": "static",
    "static": {
      "id": "019f8045-5a02-7105-9e51-23b284430c73",
      "name": "Receive Customer Call"
    }
  },
  "number": "{{01a103fb-1a54-7564-a74e-03cdc4d4a656.extension_destino}}",
  "headers": [],
  "fallback_number": "{{019feb2c-0554-7b99-a980-42f896779230.cola_horario_minibus}}",
  "transfer_timeout": "300",
  "enableSpokenDigit": false,
  "outside_agent_transfer": true,
  "stop_recording_on_transfer": false,
  "record_transfer_conversation": true
}
```
