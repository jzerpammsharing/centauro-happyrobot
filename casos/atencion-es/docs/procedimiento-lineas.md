# Procedimiento: mover las líneas al bot único y volver atrás

Borrador del Paso 1 de la Tarea 18 (spec §8.1 a §8.4 y §11.9). **No está ensayado.** Lo que no está comprobado va
marcado «por comprobar en el ensayo (Paso 2)». En el repo las líneas van como `<LINEA_PROLONGACION_ES>`,
`<LINEA_PROLONGACION_EN>`, `<LINEA_MINIBUS_ES>` y `<LINEA_MINIBUS_EN>`; los números reales se leen de los triggers en
HappyRobot, nunca se copian aquí.

## 0. Datos de partida

| Qué | Dónde |
|---|---|
| Workflow nuevo: Centauro Atención España | `01a14f1b-4ea9-7827-a4f3-4cfb06a896f6` (versión v2, sin publicar; sin números en el trigger) |
| Prolongaciones (producción: V11) | `01a0d9de-b1cd-7bc9-bafc-f5117bd57249`, ver `casos/prolongaciones/docs/workflows.md` |
| Minibús ES (producción: v25) | `019f7594-2cce-7eed-b995-dd9ea64a1062`, ver `casos/minibus/docs/workflows.md` |
| Línea de pruebas | «Test SIP RingCentral» (no es de producción) |
| Tabla línea → opción | `LINEAS` en «Contexto de la llamada» de la v2: ya lleva los números reales |

Quién hace qué:
- **Responsable del caso (jzerpa):** el editor, publicar, despublicar y las pruebas.
- **Suplente del responsable:** <nombre, lo rellena la persona antes de la fase 1>. Puede publicar y volver atrás si el responsable no está.
- **Segunda persona:** revisa el PR, mira RingCentral y cronometra.
- **El agente (Claude):** solo lectura (`monitor_runs`, RingCentral). Publicar lo hace una persona (CLAUDE.md, §3).

## 1. Requisitos previos (todos, antes de la fase 1)

### 1.1 Puerta 0 (spec §8.4)
1. Evals: críticas 3 de 3 y resto >= 90 %.
2. 25 llamadas de prueba por voz con guion (`casos/atencion-es/pruebas/guion-llamadas.md`), sin fallo crítico.
3. Caso «coincide» del correo probado con una reserva real; si no, se conecta con `enviar_correo_contrasena`
   desactivada y el plan B de la web.
4. Créditos por llamada en las pruebas <= 80 en prolongación.
5. Medición, rutina y artefacto funcionando con runs de prueba.
6. Este procedimiento escrito y ensayado (Paso 2, tabla del apartado 6).

### 1.2 Pasos del editor (para la persona; `pendientes.md`, «Para la persona»). R10, R35 y R42 eran requisitos para publicar y están hechos
- [x] **R10 (hecho el 20/10/2026 en el editor, con Frontal; 87 nodos):** quitar el Paths «Entrada» y su condición «Siempre»; «Receive Customer Call» debe colgar de «Resolver
      colas por idioma» sin borrar el agente. Comprobar con `get_workflows`: Inbound Call -> Contexto de la llamada
      -> Resolver colas -> Receive Customer Call.
- [x] **R35 (hecho el 20/10/2026: el responsable borró los Transfer de la v25 y la cadena se creó por API; 90 nodos):** crear la cadena de transferencia en Punto de encuentro e Información de oficina («Preparar
      transferencia» → «¿Transferir?» → «Initiate customer connection»). Hasta entonces conservaban el Transfer de la v25
      colgando de `transfer_to_human_agent`, sin la red de seguridad de Gestión cerrada ni la del modo virtual. **Requisito
      para publicar** (workflows.md, «Estado de la transferencia»). Comprobar con `get_workflows`.
- [x] **R42 (hecho el 20/10/2026 en el editor, con Frontal; 87 nodos):** mover «Preparar WhatsApp minibús» (con «¿Enviar WhatsApp?» y lo que cuelga) para que cuelgue de
      «Registrar resultado de la llamada» y borrar «Registrar consultas del alquiler»
      (`01a14f1d-0396-7b8c-ac8b-76817e8d62e8`). Comprobar con `get_workflows` que el padre de «Preparar WhatsApp
      minibús» es `01a14f1d-0395-7611-80cf-234e9e9fcf11`.
- [ ] `OPCION_PRUEBA` en `ninguna` en producción (con otro valor, el bot ignora la línea y fuerza la opción).
- [ ] `HORA_PRUEBA` en `ninguna` en producción (con otro valor, `estado_oficina` usa esa hora en lugar del reloj y las
      oficinas salen abiertas o cerradas a una hora falsa).
- [ ] `require_webcall_auth` en el valor que decida la persona para producción.
- [ ] Ajustes del workflow nuevo revisados (no se copian del duplicado): `out_of_office_hours`, auditorías, y que el
      nodo «Receive Customer Call» no dependa de `business_hours_setting_name: "default"` (no existe en el nuevo).
- [ ] Versión nueva (v3 o la que salga) con estos cambios, nombrada por lo que cambia, guardada en
      `casos/atencion-es/prompts/`, con entrada en `decisiones.md`, tabla de `workflows.md` y PR revisado.
- [ ] **Por comprobar en el ensayo (Paso 2):** si HappyRobot deja publicar un workflow con el trigger sin números y
      cómo se añaden las líneas (en el trigger de la versión antes de publicar, por entorno production).

### 1.3 Otros
- Elegir un **martes a las 10:00** (hora de Madrid), con la oficina abierta, y avisar a las colas y a Gestión.
- Fase 2: la puerta 1 superada (unas 2-3 semanas de la fase 1) y el experimento de Minibús ES v25 cerrado.
- Abrir un cuaderno de registro (apartado 7) antes de empezar y apuntar cada paso con la hora.
- Tener a mano: los números reales de las cuatro líneas (de los triggers), el enlace del editor de cada workflow,
  y la consulta de `monitor_runs` y de RingCentral preparada.

## 2. Qué es lo que no se sabe todavía (§11.9)

La documentación de HappyRobot solo dice que los números se asignan **por entorno** y que existen `publish` y
`unpublish`. No dice qué pasa si un número está en dos workflows, si basta con publicar el antiguo sin él o hay que
despublicarlo, si molesta que el número siga en versiones antiguas o borradores (aparece en muchas versiones de
Minibús ES y de Prolongaciones) ni cuánto tarda en entrar la primera llamada. Por eso el orden de abajo tiene dos
variantes y la persona elige la que el ensayo confirme:

- **Variante A (preferida):** republicar el antiguo **sin** las líneas (`V13 · V11 sin las líneas de Prolongación`)
  y publicar el nuevo con ellas.
- **Variante B:** despublicar el antiguo y publicar el nuevo con las líneas. Solo si la A no libera el número. Ojo:
  despublicar un workflow quita **todas** sus líneas, también las que no se mueven. En Minibús ES quitaría además
  la línea que usa Reembolsos, así que **casi seguro se descarta para la fase 2** (y solo serviría en la fase 1 si
  el trigger de Prolongaciones no tiene más líneas: comprobarlo antes).

Por comprobar en el ensayo (Paso 2): cuál de las dos variantes libera el número; si HappyRobot rechaza el número
duplicado y con qué mensaje; si las versiones antiguas y borradores que lo conservan molestan; si cambiar de
workflow corta una llamada que esté en curso.

## 3. Fase 1: Prolongación ES y EN

Duración prevista: por medir en el ensayo. Objetivo de vuelta atrás: < 30 minutos.

Orden pensado para que no se pierdan llamadas: **primero se deja listo todo en el workflow nuevo y en la versión
antigua sin líneas (borrador, sin publicar), y solo entonces se hacen las dos publicaciones seguidas**. La ventana
entre publicar una y otra es lo que se cronometra.

| # | Quién | Paso | Notas |
|---|---|---|---|
| 1 | Responsable | Comprobar los requisitos del apartado 1 y apuntar la hora de inicio | |
| 2 | Responsable | En el workflow nuevo, preparar la versión con `<LINEA_PROLONGACION_ES>` y `<LINEA_PROLONGACION_EN>` en el trigger «Inbound Call», entorno production, **sin publicar** | Los números reales se leen del trigger de V11 |
| 3 | Responsable | En Prolongaciones, `manage_versions action=fork` de V11 y quitar las dos líneas del trigger: `V13 · V11 sin las líneas de Prolongación` (**sin publicar**). Las versiones antiguas no se editan | Nombre según el siguiente número libre de versión |
| 3b | Responsable | En el workflow nuevo, dejar en borrador la **versión «nuevo sin las líneas»** (fork de la que se va a publicar, sin las líneas de Prolongación; p. ej. `v3 · v2 sin líneas`), igual que V13. Así la vuelta atrás es solo publicar | Sin publicar. Se usa en el paso 2 del apartado 5 |
| 4 | Segunda persona | Anotar la hora y el último run entrante de Prolongaciones (`monitor_runs action=list`) para tener el punto de corte | |
| 5 | Responsable | Publicar `V13` (variante A). Si en el ensayo la A no libera el número: despublicar Prolongaciones (variante B) | Entre este paso y el 6, las llamadas a esas líneas pueden caer. Hacerlos seguidos |
| 6 | Responsable | Publicar la versión del workflow nuevo con las líneas | |
| 7 | Responsable | Llamar a `<LINEA_PROLONGACION_ES>` desde un móvil conocido y decir la frase del guion | La llamada de comprobación. Y otra a `<LINEA_PROLONGACION_EN>` |
| 8 | Segunda persona | Comprobar la entrada (apartado 3.1) | |
| 9 | Responsable | Apuntar en `pendientes.md` fecha y hora de cada paso (apartado 7) | |
| 10 | Ambos | Vigilar la primera hora: `monitor_runs` cada 10 min y RingCentral; sin fallos críticos | Criterio de vuelta atrás inmediata: apartado 5 |

### 3.1 Cómo se comprueba que la primera llamada entra por el workflow nuevo
- **HappyRobot:** `monitor_runs action=list` del workflow nuevo: aparece un run con `to_number` = la línea movida
  y `from_number` = el móvil de prueba, posterior a la hora del paso 6. En V13 no debe entrar ningún run nuevo
  tras el corte. El nodo «Contexto de la llamada» debe dar `opcion = prolongacion` y el idioma de la línea.
- **RingCentral (solo lectura):** la pata de la llamada sale de la extensión 19236 hacia el SIP de la línea; se
  empareja con el run por hora (±10 s). Comprobar que la llamada de prueba aparece y que no hay llamadas
  entrantes sin run (llamadas perdidas) desde el paso 5.
- **Si en 5 minutos de llamadas de prueba no entra ningún run** en el nuevo ni en V13: vuelta atrás (apartado 5).
- Por comprobar en el ensayo (Paso 2): cuánto tarda en entrar la primera llamada tras publicar (cronometrar con la
  tabla del apartado 6) y si la propagación es por llamada o hay un retraso fijo.

## 4. Fase 2: Minibús ES (y EN)

Mismo esquema, con estas diferencias:
- **Quién:** igual. Un martes a las 10:00 tras superar la puerta 1 y cerrar el experimento de la v25.
- **Control de la fase 2 (decisión del responsable, R46):** Minibús ES **v25**. No se usa la v22.
- **Qué se republica sin las líneas:** una versión nueva de Minibús ES hecha desde la que esté en producción (v25)
  sin `<LINEA_MINIBUS_ES>` ni `<LINEA_MINIBUS_EN>` (p. ej. `v26 · v25 sin las líneas de Minibús ES`). **Antes de
  forkear, comprobar que la versión en producción sigue siendo la v25** (control decidido en R46).
- **Qué se publica en el nuevo:** la versión de Atención España vigente tras la fase 1, con las dos líneas de
  Minibús añadidas al trigger (las de Prolongación se quedan).
- **Cuidado:** el workflow de Minibús ES tiene más líneas que las de la fase 2 (hoy Reembolsos usa una línea
  española que antes era de Minibús, ver `pendientes.md`, Tarea 8). Quitar solo las dos líneas movidas y comprobar
  el trigger antes de publicar.
  **Pregunta abierta para el responsable:** ¿qué líneas quedan en Minibús ES al quitar las dos movidas? Hay que
  listar el trigger de la v25 y decidir qué hacer con las que no son de Minibús (la de Reembolsos, que usa una
  antigua línea española); `pendientes.md`, «Preguntas abiertas de la Tarea 18».
- **Comprobación de la primera llamada:** igual que el apartado 3.1, con `opcion = minibus` en «Contexto de la
  llamada»; además, en la oficina, probar una llamada de avería o de reserva nueva para ver que la transferencia
  sale por la cola correcta (extensiones de `docs/extensiones.md`) y que en horario nocturno no transfiere a las
  colas que solo ponen un anuncio (modo virtual).
- **Qué mirar en las primeras llamadas reales de Minibús** (aviso de la sesión de Minibús, 25/10/2026; informe
  `casos/minibus/docs/informes/2026-10-25-v28-direccion.md`, sección 6, en la rama del PR 11):
  - Que «Información de oficina» no transfiera a la cola minibus solo para dar el punto de encuentro. En Minibús ES
    pasó en 19 de 2.336 llamadas (07/10 a 25/10, una al día): el cliente, ya en el aeropuerto, pregunta cómo llegar a la
    oficina y el triaje lo manda a «Información de oficina». En el bot único lo resuelve el salto a
    `buscar_punto_de_encuentro` (SALTO-06a y SALTO-06b pasan en la v6).
  - Que la dirección de una oficina, también de aeropuerto, se dé y no se mande a buscar en el navegador (caso de Málaga,
    run `f7b98d60`, 25/10; arreglado en la v6, D-020).
- **Vuelta atrás preparada:** como en la fase 1 (paso 3b), dejar en borrador la versión «nuevo sin las líneas de
  Minibús» antes de publicar, para que volver atrás sea solo publicar.
- Minibús Italia y Portugal no se tocan.

## 5. Vuelta atrás (objetivo < 30 minutos, en horario de oficina)

**Cuándo:** dos fallos críticos en un día; errores de herramientas en más del 5 % de las llamadas de un día;
resolución real 10 puntos por debajo del control dos días seguidos; o la comprobación de entrada falla (3.1). La
decide el responsable; cualquiera de los dos puede pedirla.

**Lo hace el responsable en el editor** (el agente no publica). Las versiones antiguas **no se editan**:

| # | Quién | Paso | Hora |
|---|---|---|---|
| 1 | Responsable | Apuntar la hora y el motivo | |
| 2 | Responsable | Quitar las líneas movidas del workflow nuevo: **publicar la versión «nuevo sin las líneas» que se dejó en borrador en el paso 3b de la fase 1** (variante A; si no existe, fork de la de producción sin las líneas). Si el ensayo dice que hace falta, despublicar el nuevo | |
| 3 | Responsable | Republicar la versión antigua **con sus líneas**: V11 de Prolongaciones (o v25 de Minibús ES, o la que fuera la de producción antes del corte). Si se despublicó, publicarla de nuevo | |
| 4 | Segunda persona | Comprobar con una llamada a cada línea que el run entra en el workflow antiguo (3.1 al revés) y que no hay llamadas sin run en RingCentral | |
| 5 | Responsable | Apuntar en `pendientes.md` la hora de cierre y el motivo, y abrir el análisis | |

Si el orden 2 -> 3 se hace al revés (publicar el antiguo primero) puede fallar por número duplicado: **por comprobar
en el ensayo (Paso 2)**.

Si la vuelta atrás tarda más de 30 min en el ensayo, no se hace la fase 1: se reduce el procedimiento (menos
pasos manuales, versiones preparadas de antemano) y se vuelve a ensayar.

## 6. Ensayo (Paso 2, con el responsable)

**Antes de publicar nada del ensayo (seguridad):**
1. Abrir el trigger «Inbound Call» del workflow de pruebas y comprobar que lleva **solo** la línea «Test SIP
   RingCentral» y **ningún número de producción**: una copia de Prolongaciones o de Minibús ES puede arrastrar
   las líneas de producción.
2. Comprobar que la línea «Test SIP RingCentral» no está asignada a otro workflow (buscar en los triggers y en
   `manage_phone_numbers`, solo lectura).
3. Quien cronometra firma la comprobación en el cuaderno de registro con la hora. Sin esto no se publica.

Con la línea «Test SIP RingCentral» y un **workflow de pruebas** (una copia mínima de Prolongaciones o un workflow
vacío con un agente de una frase). **Nunca con las líneas de producción.** Hacer ida y vuelta completos, dos
veces, siguiendo este procedimiento y las dos variantes (A y B) si la A no libera el número.

Qué se mide y qué se resuelve (cronometrar cada fila):

| Quién | Medida | Resultado | Hora inicio | Hora fin | Duración | Observaciones |
|---|---|---|---|---|---|---|
| Responsable | Publicar el workflow de pruebas sin la línea |  |  |  |  |  |
| Responsable | Asignar la línea al workflow nuevo (publicar con la línea) |  |  |  |  |  |
| Responsable | ¿Rechaza HappyRobot la línea si sigue en el otro workflow? Mensaje |  |  |  |  |  |
| Responsable | Variante A: republicar el antiguo sin línea. ¿Libera el número? |  |  |  |  |  |
| Responsable | Variante B: despublicar el antiguo. ¿Libera el número? |  |  |  |  |  |
| Responsable | ¿Molesta que la línea siga en versiones antiguas y borradores? |  |  |  |  |  |
| Segunda persona | Hueco entre quitar la línea del antiguo y entrar la llamada por el nuevo |  |  |  |  |  |
| Segunda persona | Primera llamada por el nuevo tras publicar (segundos desde la publicación) |  |  |  |  |  |
| Segunda persona | ¿Se corta una llamada en curso al publicar? |  |  |  |  |  |
| Ambos | Ida completa (de preparar a primera llamada comprobada) |  |  |  |  |  |
| Ambos | **Vuelta atrás completa (objetivo < 30 min)** |  |  |  |  |  |
| Segunda persona | Primera llamada por el antiguo tras la vuelta (segundos) |  |  |  |  |  |
| Segunda persona | Llamadas perdidas en RingCentral durante el hueco |  |  |  |  |  |

Al terminar:
- Rellenar el apartado 2 con lo comprobado y borrar las marcas «por comprobar» que se resuelvan.
- Elegir la variante (A o B) y dejarla como única en los apartados 3 a 5.
- Marcar en `pendientes.md` «Movimiento de líneas y vuelta atrás ensayados» (puerta 0, punto 6) con la fecha y la
  duración de la vuelta.

## 7. Registro de cambios

Cada cambio, en la producción o en el ensayo, se apunta **con fecha y hora de Madrid** en
`casos/atencion-es/docs/pendientes.md` (y, para el cambio de las líneas, también en los pendientes de Minibús y de
Prolongaciones). Plantilla:

```
- [dd/mm/aaaa hh:mm] Fase N: <qué se hizo> (workflow, versión, líneas) · hecho por <persona> · comprobación: <run_id de la primera llamada>
```

Apuntar siempre: publicación del antiguo sin líneas, publicación del nuevo, primera llamada comprobada (run_id,
que sí se puede guardar), vuelta atrás si la hay y su motivo. No poner números de teléfono ni datos de clientes.

## 8. Prueba de una hora con la línea de Prolongación ES (preparada el 22/10/2026, D-018)

Una prueba corta en producción, antes de la fase 1: **solo la línea `<LINEA_PROLONGACION_ES>`**, una hora, con vuelta
atrás al terminar. La puerta 0 **no** está superada: hacerla así es decisión del responsable (D-018). La línea EN se
queda en Prolongaciones.

Versiones preparadas (borradores, sin publicar):

| Workflow | Versión | Qué lleva en el trigger |
|---|---|---|
| Centauro Atención España | `v3 · v2 sin el correo de contraseña + línea de Prolongación ES` (`5cu7jiosi6n7`, `01a16336-eee7-7143-ba65-931217592e78`) | solo `<LINEA_PROLONGACION_ES>` |
| Centauro Prolongacion Spain | `V13 · V11 sin la línea de Prolongación ES` (`om1srste88es`, `01a16343-9aba-7562-b923-866dac1933c9`) | solo `<LINEA_PROLONGACION_EN>`; el resto, igual que la V11 |

| # | Quién | Paso | Notas |
|---|---|---|---|
| 1 | Responsable | Elegir una mañana de lunes a viernes, con Gestión abierta, y avisar a las colas; abrir el registro (apartado 7) | Dos personas: una publica y otra mira runs y RingCentral |
| 2 | Segunda persona | Apuntar la hora y el último run de Prolongaciones (`monitor_runs action=list`) | Punto de corte |
| 3 | Responsable | Publicar la **V13** en lugar de la V11 | Desde aquí la línea ES no la atiende nadie hasta el paso 4: hacerlos seguidos |
| 4 | Responsable | Publicar la **v3** de Atención España en production | Si HappyRobot la rechaza por la línea, apuntar el mensaje y hacer la vuelta atrás (paso 7) |
| 5 | Responsable | Llamar a la línea ES desde un móvil conocido | Comprobar (3.1): run en Atención España con `opcion_menu = prolongacion`, `idioma = es`, `origen_opcion = linea`. Llamar también a la línea EN: debe entrar en la V13. Si en 5 minutos no entra ningún run, vuelta atrás |
| 6 | Ambos | Vigilar la hora: `monitor_runs` cada 10 minutos y RingCentral (que no haya llamadas sin run) | Vuelta atrás inmediata con un fallo crítico o llamadas perdidas |
| 7 | Responsable | **Vuelta atrás** al acabar la hora: despublicar Atención España (no tiene más líneas) y publicar la **V11** (con sus dos líneas) | En este orden, para no tener la línea en dos workflows publicados |
| 8 | Segunda persona | Llamar a la línea ES: el run debe entrar en la V11 | |
| 9 | Responsable | Apuntar en el registro cada paso con su hora, el run_id de la primera llamada y lo comprobado del apartado 2 | Esta prueba resuelve parte del ensayo (Paso 2): qué variante libera el número y cuánto tarda |

