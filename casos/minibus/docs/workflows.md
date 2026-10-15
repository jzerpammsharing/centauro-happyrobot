# Workflows de Minibús (ES · IT · PT)

Atienden a clientes que normalmente están en el aeropuerto esperando el minibús de Centauro. Los
tres tienen la misma estructura y cada uno tiene su propio agente «Daniel».

## Flujo
1. **Inbound Call** (`from_number`) → Calcular horario nocturno e idioma → Resolver colas por
   idioma → Horario de atención.
2. **Dentro de horario:** Receive Customer Call (Daniel, fase «Triaje y horario»).
   - Si el cliente busca el minibús: `buscar_punto_de_encuentro` cambia a la fase «Punto de
     encuentro».
   - Si hay que pasarle a una persona: `transfer_to_human_agent` (nodo «Initiate customer
     connection»; cada intento es un output).
   - Al final de la llamada: «Registrar resultado de la llamada» (AI Extract).
3. **Fuera de horario:** «Derivacion nocturna ES/EN» → `transferir_a_cola_nocturna`.
4. **ES v19 y siguientes:** añaden la fase «Prolongación y consultas» (`consultas_alquiler`,
   `informacion_oficina`) y el nodo «Registrar consultas del alquiler».

## Comportamiento esperado de Daniel
1. Identificar el MOTIVO antes de preguntar el aeropuerto.
2. Transferir de inmediato si es gestión de reserva, avería, reserva nueva o si piden hablar con
   una persona.
3. Si es por el minibús, preguntar el aeropuerto.
4. Si es horario nocturno, transferir sin dar indicaciones; si no, ejecutar
   `buscar_punto_de_encuentro`.
5. Dar el punto de encuentro una sola vez y cerrar sin pedir confirmación.

## Campos del extract
resumen, flujo_correcto, aeropuerto_detectado, aeropuerto_sin_datos, punto_encuentro_entregado,
ultima_herramienta, herramientas_con_error, reintentos_herramienta, hubo_transferencia,
cola_destino, motivo_transferencia, fase_transferencia, motivo_no_resuelto, extension_vacia,
pregunta_repetida, preguntas_innecesarias, invento_informacion, verbalizacion_acciones_internas,
cliente_molesto, llamada_fuera_de_alcance, turnos_agente.

Desde ES v19 también: motivo_llamada, modo_virtual, oficina_consultada, terminal_detectada,
informacion_oficina_entregada, valido_antes_de_informar, muletillas, tono_agente.

## Versiones

### España (`019f7594-2cce-7eed-b995-dd9ea64a1062`)
| Versión | Slug | Nombre / cambio | Estado (12/10/2026) |
|---|---|---|---|
| v16 | dlcl04sr1x8s | borrador: información de oficinas | — |
| v17 | i0syf61bujsz | horario 08-23 y modo virtual | publicada hasta el 11/10 |
| v18 | 21atxbf5mw1n | puntos de encuentro + idioma | recibió llamadas el 09/10 |
| v19 | viuq0asx7ggf | v17 + prolongaciones y consultas + mejoras del análisis | recibió llamadas sin estar publicada (hasta el 10/10) |
| v20 | 4onx46ig1kz4 | v19 + WhatsApp del punto de encuentro | — |
| v21 | djfjfsx8zq2f | v19 + voz, Palma y respuestas validadas | recibió llamadas sin estar publicada (hasta el 10/10) |
| **v22** | 2l6skwt8wphb | v21 + horario de la cola de Gestión | **publicada** (desde la noche del 11 al 12/10) |
| v23 | 3o04zrwgfj0g | v22 + saltos entre módulos | borrador completo, sin probar |
| v24 | 5g6422lgdcem | v23 + WhatsApp del punto de encuentro con geolocalización (MAD, SVQ, AGP) | borrador, sin probar (D-010) |
| v25 | k2in5n9kk01x | v24 + rama por defecto en ¿Enviar WhatsApp? | pendiente de publicar; sustituirá a v24 en el test A/B (D-011) |

### Italia (`01a03a65-3700-74c1-9c7b-e9c708833c4b`)
| Versión | Slug | Estado |
|---|---|---|
| v1 | yqq5wmz4g4x8 | — |
| **Version 2** | v9c38tkjwxae | **publicada** |

### Portugal (`01a05977-3a33-76da-acb2-a757f3947cf9`)
| Versión | Slug | Estado |
|---|---|---|
| **v1** | ql6fasoxl1ql | **publicada** |
| Version 2 | jaiwiyqhjvo0 | borrador |
