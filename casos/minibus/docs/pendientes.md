# Pendientes

## Incidencias abiertas
- [ ] **Averías enviadas a menús** (2114, 2115 y 2119): ver C-001. Afecta a ES v17, v18 y v19 y a
      IT v2.
- [x] **Llamadas de ES por versiones no publicadas** (v19, v21, v22): 70 de 133 el 10/10.
      Resuelto: la v22 se publicó la noche del 11 al 12/10 y desde entonces entra todo por ella.
  - Desde el 10/10 hacia las 18:40 solo entran la v17 (publicada) y la v22 (no publicada), casi a
    medias: el 11/10, 27 y 28 runs. La v19 y la v21 ya no reciben llamadas.
  - Comparación v17/v22 del fin de semana: `informes/2026-10-11-v17-vs-v22.md`.
- [ ] **v17: transfiere a Gestión en fin de semana y la llamada se pierde.** La Gestión no tiene
      agentes en fin de semana (ver pendientes de Prolongaciones). Del 10/10 18:53 al 11/10 16:47,
      14 llamadas de la v17 a 18057/18061 acabaron en la locución. La v22 no lo hace.
- [ ] **v22: copia «NO DISPONIBLE» como extensión** (f06cc517, 11/10). La regla de «recoger tarde»
      de «Prolongación y consultas» («si acepta… transfiere a GESTIÓN DE RESERVA») choca con la
      sección de Gestión cerrada. El bot pasó el texto como `extension_destino` y la transferencia
      falló con «invalid phone number». Misma causa que en Prolongaciones: «Resolver colas» deja el
      texto donde va la extensión.
- [ ] **v22 no tiene en cuenta los festivos** en `gestion_abierta` (solo mira día de la semana y
      hora). El 12/10 (festivo nacional) la Gestión sí tuvo agentes, así que no hizo daño; falta
      confirmar con Centauro qué festivos cierra Gestión.
- [ ] **v22: dice «le paso con un compañero» dos veces** (por su cuenta y dentro de la herramienta)
      en 4 de 34 llamadas del 12/10 (d1774c82, c21eba56, a3be3ecb, bac77e01).
- [ ] **v22: tutea** («Perdón, continúa.», «Perdón, dime.») en 5 de 37 llamadas (10–11/10).
- [ ] **v22: información inventada** el 11/10: oficina en el aeropuerto de A Coruña (2ff9ad71) y
      «el minibús es amarillo» (a0b9b970).
- [ ] **Palma: posible punto de encuentro de invierno distinto** (4e309ad0 y su rellamada 12c53ac1,
      11/10). El agente dijo que «en invierno tenemos otro punto de encuentro» y el cliente dijo que
      el correo de confirmación le dio un punto equivocado. Confirmar con la oficina.
- [ ] **Agentes de Gestión (18057, 18061) que cogen y no pulsan 1**: 2 llamadas perdidas el
      10/10. En la 18057 las patas duran solo 8 s.
- [ ] **Frecuencias del minibús inventadas** («cada 10-15 minutos»): ver D-006.
- [ ] **Respuestas en un idioma distinto del del cliente** (IT): ver D-006.
- [ ] **La rutina cuenta como Minibús todas las patas a 18056 y 18059**, pero Prolongaciones también
      transfiere a esas colas (minibús o idioma no atendido). Hay que corregir la sección 4 de
      `rutinas/informe-minibus.md` para que cuente solo las patas que casan con un intento de
      Minibús, como ya hace con 18057, 18061, 18001, 18006 y 18034.

- [ ] **v23: probar con llamadas reales** (D-009). Los 4 «Module Change» están enlazados y la batería de evals pasa: 14/14 nuevas y 24/24 de regresión (`informes/2026-10-12-v23-evals.md`). Falta el recorrido completo en una llamada.
  - Probar los recorridos mixtos: minibús → prolongar, prolongar → minibús, oficina → fianza,
    recoger tarde → punto de encuentro, y prolongar → oficina en modo virtual.
  - Revisar que al cambiar de módulo no repite el saludo ni vuelve a preguntar el motivo.
  - Revisar los extracts:
    - Hecho (12/10): «Registrar consultas del alquiler» ya lee también el `tema` y la `pregunta` de
      las dos `consultas_alquiler` nuevas.
    - En «Registrar resultado», `ultima_herramienta` y `fase_transferencia` no conocen la fase de
      consultas.

## Mejoras propuestas
- [ ] Mejoras de prompt de D-006 (estimación: resueltas del 42 % al 54 %).
- [ ] Herramientas nuevas (estimación: hasta el 94 %):
  - localización de la flota y aviso al operador (52 llamadas el 10/10);
  - acceso a reservas (32);
  - enlace de reserva nueva (7);
  - ubicación y foto del punto por WhatsApp (4);
  - parte de asistencia (3);
  - objetos olvidados (3).
- [ ] Guardar en `prompts/` los prompts de las versiones publicadas. Hechos ES v17 y v22 (11/10);
      faltan IT v2 y PT v1.
