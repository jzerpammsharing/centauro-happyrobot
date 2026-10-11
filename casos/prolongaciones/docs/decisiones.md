# Decisiones del caso Prolongaciones

Las decisiones comunes están en `docs/decisiones.md` de la raíz (C-NNN). Aquí van las de este
caso (D-NNN), la más reciente arriba, con la misma plantilla.

Plantilla:

```
## D-NNN · AAAA-MM-DD · Título corto
- **Qué:** …
- **Por qué:** … (datos: run_id, cifras, llamadas de ejemplo)
- **Afecta a:** versión(es)
- **Quién:** persona(s)
- **Estado:** propuesta | aprobada | aplicada en vX | descartada
```

> Las entradas D-001 a D-006 se reconstruyeron el 11/10/2026 a partir de la configuración de
> HappyRobot, los nombres de las versiones y el análisis de llamadas del 5 al 11 de octubre. Faltan
> los responsables: complétalos quien lo sepa. Lo que solo se apoya en el nombre de la versión está
> indicado.

---

## D-007 · 2026-10-11 · Rutina diaria: prompt en el repo, actualizado a la V11 y sin la comparación V8/V7
- **Qué:** el prompt de la rutina diaria de calidad pasa al repo
  (`rutinas/informe-prolongaciones.md`), con estos cambios respecto al de la nube (del 09/10):
  - **Versión:** la V11 sustituye a la V8 como versión en producción.
  - **Comparación diaria V8/V7:** se quita (sección 5b y campo `v8_vs_v7`). En su lugar, cada
    informe guarda una entrada por versión en `versiones`, que es lo que usa la tabla «versión a
    versión» de la página.
  - **Gestión cerrada:** se cuentan los intentos de transferir a Gestión cerrada (error «NO
    DISPONIBLE») y se guarda el campo nuevo `perdidas_gestion_cerrada`.
  - **Fallos de la V11:** se añaden a los fallos del bot que hay que buscar.
  - **Teléfonos y colas:** sin teléfonos en cifras. Se protege la colección `rev` de los revisores
    y, al reescribir un informe, se conservan los campos que se escriben a mano.
- **Por qué:** la comparación V8/V7 ya no tiene sentido y el prompt de la nube no conoce la V9, la V10
  ni la V11. La memoria de Claude no viaja entre cuentas, así que el prompt tiene que estar en el repo.
- **Afecta a:** la rutina «Centauro Prolongaciones - informe diario» (`trig_01BTNdfZukdFBe6PpMrEAj5T`).
- **Quién:** jzerpa.
- **Estado:** aplicada en el repo. La rutina programada no se cambia por ahora.

## D-006 · 2026-10-11 · V11: Gestión cerrada como regla de máxima prioridad, «no pudo recoger a su hora» y «recoger antes»
- **Qué:** solo cambia el prompt de «Prolongacion».
  - **Bloque «GESTIÓN CERRADA» al principio:**
    - con Gestión cerrada, no transfiere casos de gestión ni anuncia transferencias;
    - avisa del cierre en el primer turno en que el cliente pide una persona;
    - el horario L–V 8–21 es el del equipo de gestión, no el de una oficina.
  - **«NO PUDO RECOGER A SU HORA»:** la reserva se guarda 12 h desde la hora de recogida, dentro del
    horario de la oficina, y nunca se le dice que cancele y haga otra.
  - **«Recoger antes»:** no se le puede garantizar; puede preguntar en la oficina al llegar.
- **Por qué:**
  - Con Gestión cerrada, la V10 copió el aviso «NO DISPONIBLE…» en `extension_destino` en 3 de 3
    casos reales (10/10 a las 21:17 y 21:44, y 11/10 a las 09:50). Además daba el horario de Gestión
    como si fuera el de la oficina.
  - En las evaluaciones de texto, fin de semana con la cola cerrada: la V10 aprobó 15 de 40 con 13
    transferencias o promesas; la V11, 30 de 40 con 2. La prueba de las 12 horas (FDS-08) pasa de 0/5
    a 5/5. Las de recoger antes (NOINI-05, 08 y 09) dan 5/5 cada una, y la regresión no rompe nada.
  - La respuesta de recoger antes coincide con lo que hicieron los agentes humanos y con lo que pidió
    el equipo.
- **Límite:** FDS-05 (conversación larga con Gestión cerrada) sigue transfiriendo 3 de cada 7 veces.
  El arreglo fiable está en «Resolver colas» (ver pendientes).
- **Afecta a:** Version 11 (`2g1bxzyzazpp`).
- **Quién:** pendiente.
- **Estado:** aplicada en V11 (publicada el 11/10/2026, sin pasar por PR).

## D-005 · 2026-10-10 · V10: horario de la cola de Gestión
- **Qué:**
  - «Calcular idioma y saludo» calcula `gestion_abierta` (L–V 08:00–21:00, hora peninsular).
  - Con Gestión cerrada, «Resolver colas» sustituye `cola_gestion_reserva` por un aviso de texto.
  - El prompt añade la sección «COLA DE GESTIÓN CERRADA».
- **Por qué:** en fin de semana, Gestión (18057 y 18061) solo reproduce una locución de cerrado. El
  sábado 10/10, 0 de 173 patas de bots fueron atendidas.
- **Afecta a:** V10 y siguientes.
- **Quién:** pendiente.
- **Estado:** aplicada en V10. La parte del aviso de texto causó el fallo que intenta frenar la D-006.

## D-004 · 2026-10-09 · V9: responder más sin transferir
- **Qué:** según el nombre de la versión («Daniel: responder más sin transferir (caso 1)»), Daniel
  responde más consultas sin pasarlas a una persona. El detalle no se ha reconstruido.
- **Afecta a:** V9 y siguientes.
- **Quién:** pendiente.
- **Estado:** aplicada en V9.

## D-003 · 2026-10-07 · V8: todas las respuestas y aseguradoras (fase 1)
- **Qué:** según el nombre de la versión («Daniel con todas las respuestas (aseguradoras fase 1)»), se
  añaden respuestas validadas y el tratamiento de los coches de aseguradora. El detalle no se ha
  reconstruido.
- **Afecta a:** V8 y siguientes.
- **Quién:** pendiente.
- **Estado:** aplicada en V8.

## D-002 · 2026-10-07 · V7: las averías van a las colas de agentes 18034/18035, no a los menús 2114/2115
- **Qué:** en «Resolver colas», la cola de asistencia pasa de 2114 (ES) y 2115 (EN) a 18034 y 18035.
  Comprobado en la configuración de la V6 y de la V7.
- **Por qué:** 2114 y 2115 son menús automáticos. Una transferencia con resumen a un menú siempre
  falla a los 54 s, porque nadie pulsa 1 (C-001).
- **Afecta a:** V7 y siguientes.
- **Quién:** pendiente.
- **Estado:** aplicada en V7.

## D-001 · 2026-10-05 · Puesta en producción con la V6
- **Qué:** el workflow entra en producción el 05/10 a las 13:59 (Madrid) con la Version 6. Las
  versiones 1 a 4 eran pruebas y nunca se publicaron.
- **Afecta a:** Version 6.
- **Quién:** pendiente.
- **Estado:** aplicada.
