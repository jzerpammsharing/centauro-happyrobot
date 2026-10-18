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

## D-008 · 2026-10-17 · v12: Daniel envía el correo de contraseña si el correo coincide (fase 1)
- **Qué:** versión nueva `v12 · V11 + envío del correo de contraseña (fase 1)` (`mnhi8x9j8ce7`), fork
  de la V11. Spec: `specs/2026-10-17-envio-correo-contrasena.md`.
  - **Herramienta nueva `enviar_correo_contrasena`** (email, nombre completo, fecha de nacimiento), con
    cuatro nodos en cadena sobre «Centauro MCP»: `consultar_reserva` buscando por el email dictado →
    Python «Decidir envío» → `enviar_reset_contrasena` → Python «Resultado para el agente».
  - **Regla de negocio:** el agente pide el correo que el cliente dio en la oficina; si coincide con el
    de su alquiler (la consulta por ese email lo encuentra y verifica nombre y fecha), se llama a la API
    actual y se envía; si no coincide, no se envía nada, se le dice que no coincide (sin decir qué dato
    falla) y se le pasa con un agente (motivo nuevo `correo_no_coincide`). Con Gestión cerrada no
    transfiere: plan B de la web y horario.
  - **El «no se envía» no depende del modelo:** si no coincide, el email llega vacío al MCP de envío y
    este lo rechaza por validación.
  - **Prompt:** sección nueva «ENVÍO DEL CORREO DE CONTRASEÑA» con el guion y los imprevistos del
    análisis de 21 llamadas reales de septiembre (decir que la cuenta ya existe, avisar de que el correo
    dice «restablecer» pero sirve para crearla, esperar a que confirme que le ha llegado, «no le envío
    una contraseña, sino un enlace»…). Las instrucciones de «¿Has olvidado tu contraseña?» quedan como
    plan B. Se levanta la prohibición de pedir el correo, el nombre y la fecha solo para este envío;
    nunca reserva, matrícula ni DNI. Como mucho dos envíos por llamada.
  - **`transfer_to_human_agent`:** motivo `correo_no_coincide` y casos del correo en Gestión.
  - **Extract:** 5 campos nuevos (`correo_contrasena_ofrecido`, `correo_contrasena_resultado`,
    `envios_correo`, `correo_recibido_confirmado`, `motivo_no_envio`), `correo_no_coincide` en
    `motivo_transferencia` y `pidio_dato_personal` sin contar los datos del envío aceptado. No se quita
    ningún campo (los usa la rutina diaria).
- **Por qué:**
  - En septiembre, antes del bot, los agentes de Gestión enviaron este correo en 21 de 66 llamadas de
    prolongación (11 a clientes de mutua que nunca habían entrado en centauro.net). La V11 solo puede
    explicarlo y, si el correo no llega, transfiere a Gestión, que en fin de semana está cerrada.
  - El MCP de envío (`enviar_reset_contrasena`) solo acepta `email` y no comprueba nada: sin la
    comprobación previa, el bot enviaría a cualquier correo dictado y no sabría si es el de la cuenta.
- **Descartado:** confirmar el correo con una pista enmascarada («el que empieza por jota eme»), como
  proponía el brief: la API nunca devuelve el correo al agente virtual (solo el dominio, `email_hint`).
- **Afecta a:** v12 (sin publicar).
- **Quién:** jzerpa.
- **Estado:** construida en el fork, sin publicar. Evals nuevas CORREO-01 a 21 en verde en su última
  ejecución; la regresión solo falla en evals que cambian de expectativa por diseño o que ya fallaban en
  la V11 (informe `informes/2026-10-17-v12-correo-contrasena.md`). Faltan la prueba del caso «coincide»
  con una reserva real y la prueba por voz (ver pendientes).

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
