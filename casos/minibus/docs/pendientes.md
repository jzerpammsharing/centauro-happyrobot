# Pendientes

## Incidencias abiertas
- [ ] **Averías enviadas a menús** (2114, 2115 y 2119): ver C-001. Afecta a ES v17, v18 y v19 y a
      IT v2.
- [ ] **Llamadas de ES por versiones no publicadas** (v19, v21, v22): 70 de 133 el 10/10.
      Revisar qué números de teléfono apuntan a cada versión.
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

- [ ] **IT v3 y PT v3 (D-010): confirmar antes de publicar.**
  - Que 19048/19049 (IT) y 19035/19036 (PT) son las colas de averías con agentes y atienden los 7
    días, como la 18034.
  - Horario del centro de atención para IT y PT: se ha supuesto el de España, de 08:00 a 22:00
    peninsular (en Portugal, de 07:00 a 21:00).
  - Horario de Mod. Reserva (18071/18074) y Alteração (18064/18067): se ha supuesto el de Gestión
    ES, de lunes a viernes de 08:00 a 21:00 peninsular.
  - Que la IVR de IT y PT filtra el horario como en España: sin la rama nocturna, a cualquier hora
    entra el bot en modo virtual.
  - El idioma del whisper y de `resumen_para_agente` (italiano / portugués) para los agentes de
    cada cola.
  - Probar con llamadas de test las dos líneas (local e inglés) de cada país, de día y en modo
    virtual.
- [ ] **IT y PT sin información de oficinas ni prolongaciones**: hacen falta los datos de oficinas
      y las condiciones de alquiler de Italia y Portugal para portar esos módulos de ES v22.

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
      faltan IT v2 y PT v1 (sí están IT v3 y PT v3).
