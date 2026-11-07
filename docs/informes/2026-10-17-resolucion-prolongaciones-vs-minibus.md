<!-- 17/10/2026, solo lectura. Llamadas del 15/10 18:36 (Madrid) al 17/10: Prolongaciones V11 (182) frente al módulo «Prolongación y consultas» de Minibús ES v22/v25. Fuente: listado de runs de HappyRobot + tabla Twin de cada workflow. Cifras del extract de IA, sin contrastar con transcripciones. -->

# Prolongaciones (V11) vs. módulo «Prolongación y consultas» de Minibús (v22/v25)

Periodo: desde 2026-10-15 16:36 UTC (18:36 Madrid) hasta el 2026-10-17 (último run 17:30 UTC).
Fuente: listado `monitor_runs` (IDs extraídos con script) + Twin (`centauro_prolongacion_spain_runs`,
`centauro_minibus_spain_runs`), solo runs COMPLETED. Todas las métricas salen del extract de IA,
que no es del todo fiable (ver notas al final).

## 1. Prolongaciones – Centauro Prolongacion Spain

Runs listados: 184, todos en V11 (`01a12a23…`); 182 COMPLETED + 2 RUNNING. En Twin cruzan los 182.

### a) Totales (n = 182)

| Métrica | n | % |
|---|---|---|
| resuelto_sin_transferencia = si | 48 | 26 % |
| hubo_transferencia = si | 64 | 35 % |
| hubo_transferencia = no | 118 | 65 % |
| llamada_fuera_de_alcance = si | 9 | 5 % |
| Duración media | 201,9 s | |

### b) Por tipo_consulta

| tipo_consulta | n | Sin transferencia | % sin transf. | Transferidas | Resuelto sin transf. (extract) |
|---|---|---|---|---|---|
| otra_gestion | 70 | 35 | 50 % | 35 | 5 (7 %) |
| prolongacion | 55 | 48 | 87 % | 7 | 28 (51 %) |
| web_no_deja | 23 | 13 | 57 % | 10 | 4 (17 %) |
| devolver_tarde | 18 | 11 | 61 % | 7 | 9 (50 %) |
| fuera_de_alcance | 9 | 8 | 89 % | 1 | 0 |
| reserva_concreta | 4 | 0 | 0 % | 4 | 0 |
| precio | 3 | 3 | 100 % | 0 | 2 |

### c) Transferencias (n = 64)

| cola_destino | n |
|---|---|
| gestion_reserva | 39 |
| nueva_reserva | 13 |
| minibus | 8 |
| asistencia | 4 |

| motivo_transferencia | n |
|---|---|
| otro | 25 |
| pregunta_reserva_concreta | 12 |
| nueva_reserva | 8 |
| minibus | 6 |
| asistencia | 4 |
| no_iniciada | 4 |
| error_tecnico | 3 |
| web_no_disponible | 1 |
| enfado | 1 |

### d) Contraseña

| necesitaba_contrasena | n | Sin transferencia | Transferidas | Resuelto sin transf. |
|---|---|---|---|---|
| si | 51 | 38 | 13 | 26 |
| no | 131 | 80 | 51 | 22 |

## 2. Minibús – subconjunto «Prolongación y consultas» (tools_result contiene `consultas_alquiler`)

Base: runs COMPLETED desde 2026-10-15 16:36 UTC de `minibus_runs_15_17.csv`: v22 = 121, v25 = 155 (todos cruzan en Twin).

| Versión | Runs | Entran en PyC | % PyC | PyC sin transferencia | PyC transferidas |
|---|---|---|---|---|---|
| v22 | 121 | 25 | 21 % | 14 (56 %) | 11 |
| v25 | 155 | 33 | 21 % | 19 (58 %) | 14 |
| Total | 276 | 58 | 21 % | 33 (57 %) | 25 |

### Por motivo_llamada (PyC)

| motivo_llamada | v22 n | v22 sin transf. | v25 n | v25 sin transf. |
|---|---|---|---|---|
| gestion_reserva | 19 | 10 | 21 | 10 |
| devolucion | 3 | 2 | 4 | 3 |
| otro | 0 | – | 3 | 3 |
| minibus | 0 | – | 2 | 1 |
| retraso_llegada | 1 | 0 | 1 | 1 |
| averia | 1 | 1 | 1 | 0 |
| nueva_reserva | 1 | 1 | 0 | – |
| horario | 0 | – | 1 | 1 |

### Transferencias PyC por cola_destino

| cola_destino | v22 | v25 |
|---|---|---|
| minibus | 10 | 7 |
| gestion_reserva | 1 | 5 |
| nueva_reserva | 0 | 1 |
| ninguna (incoherente con hubo_transferencia = si) | 0 | 1 |

### Ejemplos de temas en PyC (paráfrasis de response_resumen, sin datos personales)

| # | Versión | Tema | ¿Transferida? |
|---|---|---|---|
| 1 | v22 | Arañazo en coche recién recogido | No |
| 2 | v22 | Fianza con tarjeta al devolver | No (cliente insatisfecho) |
| 3 | v22 | Restricciones de tráfico en ciudad | No (falló la transferencia) |
| 4 | v22 | Ampliar reserva y devolver con retraso | No |
| 5 | v22 | Cobertura para viajar a Portugal | No |
| 6 | v22 | Alquilar con débito y seguro premium | No |
| 7 | v22 | Recogida tardía por vuelo retrasado | Sí, a minibús (mal enrutada) |
| 8 | v25 | Devolver antes de abrir la oficina | No |
| 9 | v25 | Multa y cargo de gestión | No |
| 10 | v25 | Cancelar una reserva | Sí, a gestión de reservas |
| 11 | v25 | Cambiar oficina de devolución | Sí, a gestión de reservas |
| 12 | v25 | Vehículos adaptados | Atendida por compañero (extract dice «no») |

## Notas de fiabilidad

- Todo sale del extract de IA (incluido `response_resumen`); no se ha verificado contra turnos `assistant` ni RingCentral.
- «Sin transferencia» no es «resuelto»: en Prolongaciones 118 sin transferencia pero solo 48 resueltas según el extract.
- En Minibús PyC, `extension_destino` está vacío en las 58 filas, así que no hay dato no-IA en Twin para contrastar las transferencias.
- Incoherencias vistas: 1 fila v25 con hubo_transferencia = si y cola = ninguna; 1 con hubo_transferencia = no y cola = gestion_reserva cuyo resumen dice que la atendió un compañero.
- Muestras pequeñas por tema (n ≤ 21 en Minibús PyC), los porcentajes son orientativos.
