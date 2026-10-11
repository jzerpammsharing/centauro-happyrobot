# Pendientes

## Incidencias abiertas
- [ ] **Averías enviadas a menús** (2114, 2115 y 2119): ver C-001. Afecta a ES v17, v18 y v19 y a
      IT v2.
- [ ] **Llamadas de ES por versiones no publicadas** (v19, v21, v22): 70 de 133 el 10/10.
      Revisar qué números de teléfono apuntan a cada versión.
- [ ] **Agentes de Gestión (18057, 18061) que cogen y no pulsan 1**: 2 llamadas perdidas el
      10/10. En la 18057 las patas duran solo 8 s.
- [ ] **Frecuencias del minibús inventadas** («cada 10-15 minutos»): ver D-006.
- [ ] **Respuestas en un idioma distinto del del cliente** (IT): ver D-006.
- [ ] **La rutina cuenta como Minibús todas las patas a 18056 y 18059**, pero Prolongaciones también
      transfiere a esas colas (minibús o idioma no atendido). Hay que corregir la sección 4 de
      `rutinas/informe-minibus.md` para que cuente solo las patas que casan con un intento de
      Minibús, como ya hace con 18057, 18061, 18001, 18006 y 18034.

## Mejoras propuestas
- [ ] Mejoras de prompt de D-006 (estimación: resueltas del 42 % al 54 %).
- [ ] Herramientas nuevas (estimación: hasta el 94 %):
  - localización de la flota y aviso al operador (52 llamadas el 10/10);
  - acceso a reservas (32);
  - enlace de reserva nueva (7);
  - ubicación y foto del punto por WhatsApp (4);
  - parte de asistencia (3);
  - objetos olvidados (3).
- [ ] Guardar en `prompts/` los prompts de las versiones publicadas (ES v17, IT v2, PT v1).
