<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v1 (veavliy3k6jx) · nodo: Initiate customer connection (hijas de transfer_to_human_agent de Triaje, Punto de encuentro, Información de oficina y Prolongación y consultas) · copiado: 2026-10-18 -->

# Transferencias «Initiate customer connection» (v1)

- Event ID de los cuatro nodos: `01926f25-dacb-710e-a823-4254189111dd` (Transfer, integración Phone calls).
- Los campos de texto enriquecido de Plate (`number`, `fallback_number`, `extension`, `whisper_message`) se han
  aplanado a texto con `{{persistent_id.variable}}`, sin los nodos de texto vacíos que añade el editor.
- Los cuatro llevan el mismo agente (`300ae88d-ccb2-466c-a914-9f9090363a74`, «Receive Customer Call»), `whisper_transfer:
  true` y la misma configuración de transferencia; solo cambian el padre, el `number` (la `extension_destino` de su
  herramienta), el `fallback_number` y la variable `resumen_para_agente` del whisper.
- `number` es la `extension_destino` que elige el modelo (hoy la URI SIP completa de la cola, p. ej. `sip:18056@…`).
- El whisper dice «Llamada del asistente de minibús.» y termina con el teléfono dictado (`telefono_dictado`).

Configuración común (los valores que cambian van marcados con `<…>`):

```json
{
  "agent": {"type": "static", "static": {"id": "300ae88d-ccb2-466c-a914-9f9090363a74", "name": "Receive Customer Call"}},
  "number": "{{<tool_persistent_id>.extension_destino}}",
  "headers": [],
  "extension": "",
  "from_number": "",
  "uui_encoding": "ascii",
  "warm_handoff": false,
  "fallback_number": "{{081e2b5d-b260-41a6-bd2a-6f82b26193d1.<cola_de_respaldo>}}",
  "uui_data_format": "text",
  "whisper_message": "Llamada del asistente de minibús. {{<tool_persistent_id>.resumen_para_agente}} Teléfono del cliente: {{e51cd732-f403-4ef7-95d4-490347960a93.telefono_dictado}}.",
  "skip_digit_press": false,
  "whisper_transfer": true,
  "enableSpokenDigit": false,
  "skip_handoff_message": true,
  "warm_handoff_intro_mode": "default",
  "stop_recording_on_transfer": false,
  "record_transfer_conversation": true
}
```

## 1. Hija del transfer de «Triaje y horario»

- persistent_id: `b4439401-fdae-4a3b-9a42-9a5c2de8f1b2`
- Padre: transfer_to_human_agent `17c682a0-82d2-42f6-88fa-817d8cba0783`
- `<tool_persistent_id>` = `17c682a0-82d2-42f6-88fa-817d8cba0783`
- `<cola_de_respaldo>` = `cola_horario_minibus` (cola de Minibús)

## 2. Hija del transfer de «Punto de encuentro»

- persistent_id: `37fb8053-214e-4357-be80-0fc8f832ecbc`
- Padre: transfer_to_human_agent `00435498-eccf-4110-9cf1-eb17821af3ed`
- `<tool_persistent_id>` = `00435498-eccf-4110-9cf1-eb17821af3ed`
- `<cola_de_respaldo>` = `cola_horario_minibus` (cola de Minibús)

## 3. Hija del transfer de «Información de oficina»

- persistent_id: `faec6a20-257a-4b8c-8c75-8dd336beead7`
- Padre: transfer_to_human_agent `62c5b6dd-5dde-4b3a-9a93-adb638c0bd66`
- `<tool_persistent_id>` = `62c5b6dd-5dde-4b3a-9a93-adb638c0bd66`
- `<cola_de_respaldo>` = `cola_horario_minibus` (cola de Minibús)

## 4. Hija del transfer de «Prolongación y consultas»

- persistent_id: `1dce23f2-c76c-4bfc-afbc-a1675318c082`
- Padre: transfer_to_human_agent `fbe2e40e-4915-4f44-9bac-59c318862e97`
- `<tool_persistent_id>` = `fbe2e40e-4915-4f44-9bac-59c318862e97`
- `<cola_de_respaldo>` = `cola_gestion_reserva` (cola de Gestión; con Gestión cerrada esa variable lleva el aviso de
  «NO DISPONIBLE AHORA» en lugar de la SIP, ver «Resolver colas por idioma»)
