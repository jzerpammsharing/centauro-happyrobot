# Pendientes del caso Atención España

## Antes de construir
- [x] Aprobar el spec (`specs/2026-10-18-bot-unico-arquitectura.md`) (18/10/2026).
- [ ] Revisar el plan de construcción (`planes/2026-10-18-bot-unico-construccion.md`) y elegir cómo se ejecuta.

## Al construir (comprobaciones del spec, §11)
- [x] Qué copia el duplicado de la v25: Module Change, evals, agente de voz (18/10/2026; detalle en «Comprobaciones de
      la Tarea 6»). Copia los 4 Module Change, el agente de voz y los 37 nodos; **no** copia evals, líneas del trigger,
      ajustes del workflow ni tabla de Twin.
- [ ] Que un Module Change pueda volver al Triaje.
- [ ] Que el módulo de destino ve el historial.
- [ ] Cómo cortar la cadena de la transferencia sin transferir con Gestión cerrada, y qué recibe el agente.
- [ ] Que el whisper es lo que mantiene al bot en la llamada tras transferir (confirmar con HappyRobot).
- [ ] Que un nodo Python acepta el código de `buscar_respuesta`.
- [ ] Que la tabla de Twin se crea sola con los campos del extract (18/10/2026: aún no existe la tabla del workflow
      nuevo, solo las de los workflows que ya tienen runs; se verá con la primera ejecución o al publicar).
- [ ] Horario real de las colas de Minibús y Nueva Reserva de noche (RingCentral, solo lectura).
- [ ] Cómo se mueve una línea entre workflows (publicar el antiguo sin ella o despublicarlo; números que siguen
      en versiones antiguas y borradores).
- [ ] Calendario de festivos nacionales de 2026 y 2027 en «Contexto de la llamada».

## Comprobaciones de la Tarea 6 (18/10/2026)

Duplicado de Minibús ES v25 → workflow `01a14f1b-4ea9-7827-a4f3-4cfb06a896f6` (ver `workflows.md`). Resultado de
las comprobaciones de los apartados 11.1 y 11.7 del spec:

- **Module Change: se copian los 4**, con 37 nodos en total (4 prompt, 14 action, 11 tool, 4 module-change,
  4 condition). Cada uno apunta a un nodo **del workflow nuevo**, no a los de Minibús ES:
  `informacion_oficina` (en Prolongación y consultas) → Información de oficina; `buscar_punto_de_encuentro` (en
  Prolongación y consultas) → Punto de encuentro; `consultas_alquiler` (en Información de oficina) y
  `consultas_alquiler` (en Punto de encuentro) → Prolongación y consultas. Detalle en
  `prompts/atencion-es/v1/module-change.md`.
- **Evals: no se copian.** 0 en los 4 prompts del workflow nuevo, frente a 24 (Triaje), 17 (Información de oficina),
  21 (Punto de encuentro) y 12 (Prolongación y consultas) en la v25, 74 en total. Tampoco hay carpetas de evals.
  Hay que crearlas por API en los nodos nuevos (spec §7.1).
- **Trigger «Inbound Call»: no se copian las líneas** de Minibús (sin configuración, `numbers` vacío), así que no
  hizo falta quitar nada. Tampoco copia `require_webcall_auth: false`: por defecto es `true`, y una prueba por
  llamada web necesitará ponerlo en `false` (decisión de la persona) antes de usar `OPCION_PRUEBA`.
- **Ajustes del workflow: no se copian.** En el workflow nuevo `out_of_office_hours` está vacío (Minibús ES tenía
  `default` con un día de excepción y `horariominibus`), las auditorías no están activadas (Minibús ES: activadas,
  muestreo del 10 %) y el nodo «Receive Customer Call» sigue apuntando a `business_hours_setting_name: "default"`,
  que no existe en el workflow nuevo. Comprobar antes de las primeras llamadas de prueba que el agente no depende de
  ese horario, y decidir si se activan las auditorías.
- **Tabla de Twin:** no existe todavía una para el workflow nuevo (solo `centauro_minibus_spain_runs`,
  `centauro_minibus_italy_runs`, `centauro_minibus_portugal_runs`, `centauro_prolongacion_spain_runs` y
  `centauro_reembolsos_runs`). Revisar su creación y sus columnas tras la primera ejecución o la publicación.
- **Variables en el duplicado:** el JSON de Plate de los nodos apunta bien a los persistent_id nuevos
  (p. ej. «Calcular horario nocturno» pasa de `019fd418-…` a `e51cd732-…`). Pero el **markdown** que devuelve
  `get_node_details` para los prompts conserva los ids antiguos; no pegarlo tal cual al actualizar un prompt.
  `fix_broken_vars` en simulación no encontró referencias rotas.
- **`fix_broken_vars` / test-all:** aunque se acotó con `node_ids`, recorrió la versión entera (12 nodos: 4 bien,
  4 con error, 4 saltados). Los 4 «Initiate customer connection» fallan con «room name is required for inbound voice
  agents», que es lo esperado sin una llamada en curso; no se transfirió nada ni se envió ningún WhatsApp. No es
  una prueba de que las transferencias funcionen.
- **`delete` de `update_workflow_nodes` borra el nodo con todo su subárbol.** Comprobado con nodos desechables
  (un Paths de prueba con una condición y un hijo: desaparecieron los tres; los nodos de prueba ya no están en la
  v2). No hay forma por API de reenganchar un nodo a otro padre (`parent_id` no se puede cambiar con `update`;
  `add` solo inserta un nodo nuevo entre un padre y sus hijos). **Para las tareas siguientes: no borrar nunca un
  nodo con hijos esperando que se reenganchen.**

## Para la persona (editor de HappyRobot)

- [ ] **Quitar el Paths «Entrada» y su condición «Siempre» de la v2** y dejar «Receive Customer Call» colgando
      directamente de «Resolver colas por idioma» (Paso 5 de la Tarea 6, no hecho por API). Hay que hacerlo en el
      editor **sin borrar el agente** (mover «Receive Customer Call» con todo lo que cuelga y después borrar
      «Entrada»/«Siempre»). La v2 ya no tiene la rama «Fallback» (vacía) de «Entrada». Después, comprobar con
      `get_workflows` que la cadena es Inbound Call → Calcular horario nocturno → Resolver colas → Receive Customer
      Call. Las tareas siguientes pueden construirse sobre la v2 tal como está (el Paths no estorba), pero no hay
      que publicarla con él.
- [ ] **Líneas telefónicas:** la v1 y la v2 no tienen números en el trigger. La tabla línea → opción del menú y los
      números se ponen al pasar a producción (puerta 0 del spec §8.4); ahora mismo no entra ninguna llamada por
      este workflow. Los números van como `<LINEA_PROLONGACION_ES>`, `<LINEA_PROLONGACION_EN>`,
      `<LINEA_MINIBUS_ES>` y `<LINEA_MINIBUS_EN>` en el repo.
- [ ] **Bloquear la v1** (`manage_versions action=lock`) si se quiere proteger la referencia: el fork no la bloquea.
      No se hizo por no estar pedido.

## Antes de conectar la primera línea (puerta 0, spec §8.4)
- [ ] Caso «coincide» del correo de contraseña probado con una reserva real (pendiente heredado de la v12).
- [ ] `pista_correo` probada con una reserva real (verifica y devuelve solo el dominio).
- [ ] Rutina diaria, artefacto y `scripts/medir_bots.py` funcionando.
- [ ] Movimiento de líneas y vuelta atrás ensayados, ida y vuelta, con la línea «Test SIP RingCentral».
- [ ] Cerrar el experimento de Minibús ES v25 antes de la fase 2 (mover las líneas de Minibús).

## Para negocio
- [ ] Los 7 «DECIDIR» de `comun/bloques/consultas-alquiler.md`.
- [ ] Si después se conecta la opción de Gestión cuando está cerrada.
- [ ] Confirmar con Centauro que Gestión no atiende los festivos autonómicos (hoy se tratan como laborables).
