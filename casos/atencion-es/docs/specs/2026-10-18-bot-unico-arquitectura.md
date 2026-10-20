# Spec · Bot único de atención de Centauro España (fase 1: Minibús + Prolongaciones)

Fecha: 18/10/2026 · Estado: **propuesta, sin construir** · Decisiones: C-004 (raíz) y D-001 (este caso) ·
Rama: `comun/bot-unico-arquitectura`.

## 1. Qué es y por qué

Un solo bot de voz para la atención de Centauro España: una puerta de entrada corta (Triaje) y módulos
especialistas pequeños entre los que el bot salta con Module Change. Es el primer paso del bot único: junta las
opciones del menú de **Minibús** y de **Prolongación**, que hoy atienden dos workflows distintos, y después irá
absorbiendo, opción por opción, las demás (Gestión, el triaje de Nueva Reserva…).

Por qué ahora:
- **Coste.** Medido con 120 llamadas reales: una llamada media cuesta 118 créditos en Prolongaciones V11 y 64 en
  Minibús v25. La diferencia es el diseño: el prompt de 61.000 caracteres con gpt-5.4 en cada respuesta
  (12,4 créditos por respuesta del bot) frente a un Triaje corto con gpt-4.1-fast (2,1). A escala, unos 95.000 €
  al año en el escenario del 50 % (`docs/informes/2026-10-18-carga-agentes-ringcentral.md`).
- **Resolución.** Prolongaciones resuelve hoy el 38 % (medido en transcripciones; 42–47 % con la regla de la
  rutina) y Minibús el 47 %. Con las respuestas nuevas del equipo y el MCP, el 53 % es realista
  (`docs/informes/2026-10-17-respuestas-daniel-vs-bots.md`). El objetivo de negocio es que la IA resuelva sin
  agente cerca del 50 % de las llamadas de gestión.
- **Un solo conocimiento.** Las respuestas del alquiler están copiadas en dos bots y ya se contradicen
  (`docs/informes/2026-10-17-minibus-v25-vs-prolongaciones.md`).

## 2. Objetivos, no objetivos y antiobjetivos

**Objetivos**
- Un workflow nuevo, «Centauro Atención España», que atienda las líneas de Minibús y de Prolongación de España
  con el mismo bot.
- Créditos por llamada: ≤ 80 en la línea de Prolongación (hoy 118) y ≤ 64 en la de Minibús (hoy 64).
- Resolución real: no peor que los bots actuales y, como objetivo, ≥ 50 % en la línea de Prolongación.
- Medir igual los tres bots (el nuevo y los dos actuales) para poder compararlos.

**No objetivos (fase 1)**
- Crear o modificar reservas. Los agentes tampoco las modifican: mandan a la web y ayudan con la contraseña.
  Las reservas nuevas se quedan en ventas.
- Leer datos de la reserva para responder (hora de devolución, cargos…): es la fase 2 del MCP. En la fase 1 el
  MCP solo se usa para el correo de contraseña (y su pista del dominio, §5.7).
- Italia y Portugal (Minibús IT y PT siguen como están).
- Reembolsos (sigue en su workflow).
- Cambiar los workflows actuales: Minibús ES y Prolongaciones no se tocan; son la vuelta atrás.
- Optimizar Punto de encuentro e Información de oficina (pasar sus datos a herramientas): fase posterior.

**Antiobjetivos (sería un fracaso aunque funcione)**
- Que el coste por llamada no baje, o que suba por los saltos entre módulos.
- Una sola transferencia ejecutada a Gestión cerrada o a los menús 2114, 2115 y 2119.
- Un correo de contraseña enviado a un correo que no ha coincidido.
- Un Triaje que responde preguntas de contenido (y por tanto inventa).
- Bucles entre módulos o un cliente que tiene que repetir lo que ya dijo después de un salto.
- Perder lo que ya funciona en Minibús: el punto de encuentro, el horario nocturno, el WhatsApp.
- Perder la transcripción del agente humano en las transferencias de gestión (se usa para auditar).

## 3. Restricciones

- Reglas del repo (`CLAUDE.md` raíz): nunca editar una versión publicada (siempre fork); **no publicar** (lo
  hace una persona); solo lectura en RingCentral y en el análisis de llamadas; nada de datos personales ni
  condiciones del contrato con HappyRobot en el repo; todo en castellano.
- **Module Change no se puede crear por API**: los crea una persona en el editor. Los prompts, herramientas,
  Python, Transfer y Extract sí se crean por API.
- **«Centauro MCP»** (credencial `01a0e1d8-9c92-7e58-8e25-caf109f1fadb`) va contra la API real de Centauro
  aunque se llame «Stagin»: cualquier envío es real. **No hacer refresh** de los servidores MCP en HappyRobot
  (la API da 500).
- La documentación de HappyRobot pide código de acceso: lo que no está en la configuración real hay que
  comprobarlo construyendo (§11).
- Las 10 líneas SIP de la serie de Centauro están asignadas (Minibús ES, IT y PT, Prolongaciones, Reembolsos
  WhatsApp y pruebas). El workflow nuevo no tiene líneas propias hasta producción: **al pasar a producción se
  mueven las líneas actuales** (§8.1). Hasta entonces, las pruebas son por web.

## 4. Punto de partida

| | Minibús ES v25 (`k2in5n9kk01x`) | Prolongaciones v12 (`mnhi8x9j8ce7`, borrador) |
|---|---|---|
| Estado | Publicada; recibe tráfico real en un experimento desde el 15/10. En producción, la v22 | Sin publicar. En producción, la V11 (`2g1bxzyzazpp`) |
| Estructura | Triaje (gpt-4.1-fast, ~18.000 car.) → Punto de encuentro (gpt-4.1-fast, 36.076), Información de oficina (gpt-4.1, 35.918) y Prolongación y consultas (gpt-5.4, 51.821) | Un prompt (gpt-5.4, 61.059) |
| Saltos | 4 Module Change, todos con Prolongación y consultas. Nadie vuelve al Triaje; Punto de encuentro ↔ Oficina no existe | — |
| Herramientas propias | `buscar_punto_de_encuentro`, `informacion_oficina`, `consultas_alquiler` (cambios de módulo), `transfer_to_human_agent` ×4 | `enviar_correo_contrasena` (4 nodos sobre «Centauro MCP»), `transfer_to_human_agent` |
| Evals | 24 en el Triaje, más carpetas de Oficina y Punto de encuentro | 127 en «Prolongacion» (14 carpetas, incluidas CORREO-01 a 21) |

Fallos que no hay que heredar:
- Con Gestión cerrada, «Resolver colas» pone el texto «NO DISPONIBLE…» en lugar de la extensión de Gestión, y el
  `fallback_number` de la transferencia de Prolongación y consultas (y de la v12) es ese texto.
- El extract principal de la v25 no recibe nada de Prolongación y consultas, y `ultima_herramienta` no admite
  `consultas_alquiler`.
- El Paths «Entrada» tiene un «Fallback» sin hijos y `cola_fuera_horario` no se usa.
- Las herramientas de transferencia del Triaje, Punto de encuentro y Oficina no saben qué hacer si la
  transferencia falla.
- Prolongaciones usa tres voces al azar y la grabación española del aviso legal en la línea inglesa.
- Las contradicciones entre los dos prompts (cancelación 24/48 h, 29/30 días, coche de aseguradora, grúa,
  francés…), recogidas en `comun/bloques/consultas-alquiler.md`.

## 5. Arquitectura

### 5.1 Flujo

```
Inbound Call (líneas de Minibús ES/EN y de Prolongación ES/EN)
 └ Python «Contexto de la llamada»
   └ Python «Resolver colas»
     └ Receive Customer Call (agente de voz)
         TRIAJE ──► PUNTO DE ENCUENTRO ◄──► INFORMACIÓN DE OFICINA
           │   ──► PROLONGACIÓN
           │   ──► CONSULTAS DEL ALQUILER
           └ transferencias directas
         cada módulo: volver_al_triaje + atajos + transfer_to_human_agent
     └ AI Extract «Registrar resultado de la llamada»
       └ rama de WhatsApp del punto de encuentro (como en la v25)
```

Se crea duplicando Minibús ES v25 (`create_workflow` con `source.type = duplicate`) en la carpeta de Centauro
(`019d8144-ce27-7aaf-b9e5-21d006083063`). La versión duplicada se queda como referencia,
`v1 · copia de Minibús ES v25`, sin tocar; el bot único se construye en un fork, `v2 · bot único: Triaje + 4
módulos`. El Paths «Entrada» y su «Fallback» vacío se quitan.

### 5.2 Python «Contexto de la llamada»

Sustituye a «Calcular horario nocturno» (v25) y a «Calcular idioma y saludo» (Prolongaciones). Mantiene todas las
salidas de la v25 y añade:
- `opcion_menu`: `minibus` o `prolongacion`, según la línea marcada (`to_number`). Una tabla línea →
  (opción, idioma) en el código, sin números en el repo. Una línea desconocida da `minibus` y `es`, y lo anota.
- `mensaje_inicial` según la opción:
  - Minibús: los cuatro mensajes de la v25 (español o inglés, normal o modo virtual).
  - Prolongación: «Centauro Rent a Car, {saludo}, le atiende Daniel, su asistente de IA. ¿Quiere prolongar un
    alquiler que tiene en curso?» y su versión en inglés. En modo virtual no se avisa en el saludo: se avisa
    cuando el cliente pide una persona (como hace hoy la V11 con Gestión cerrada).
- `modo_virtual` (22:00–08:00 peninsular, sin compañeros salvo Asistencia) vale para las dos opciones. Hoy la V11
  transfiere de noche a Minibús y a Nueva Reserva como si atendieran; según el registro de RingCentral
  (informe del 18/10) esas colas solo atienden de 8 a 22. **Decidido el 18/10**; el horario real se comprueba en
  RingCentral al construir (§11).
- `festivo_nacional`: calendario de festivos nacionales de España en el código (2026 y 2027). **Gestión no atiende
  los festivos nacionales** (decidido el 18/10): ese día `gestion_abierta` es false todo el día. Los festivos
  autonómicos no cuentan.
- Grabación del aviso legal por idioma: la de la v25 (corrige el fallo de Prolongaciones).

El código va en `casos/atencion-es/codigo/contexto_llamada.py`, con pruebas.

### 5.3 Python «Resolver colas»

El de la v25, con dos cambios:
- **Nunca pone un texto donde va una extensión.** Con Gestión cerrada devuelve la extensión igual y
  `gestion_abierta = false`; quien decide no transferir es «Preparar transferencia» (§5.8).
- Se quita `cola_fuera_horario`.

### 5.4 Módulos

| Módulo | Qué hace | Modelo | Tamaño objetivo | Sale de |
|---|---|---|---|---|
| **Triaje** | Primer módulo. Saluda (mensaje inicial), averigua el motivo en uno o dos turnos y encamina. No responde preguntas de contenido | gpt-4.1-fast | ≤ 9.000 caracteres | Triaje de la v25, sin las listas nocturnas de aeropuertos (pasan a Punto de encuentro) |
| **Punto de encuentro** | Punto de encuentro, horario nocturno de los aeropuertos (el cierre lo resuelve el código: `estado_oficina`, D-012), quejas del minibús, WhatsApp | gpt-4.1-fast | ~36.000 | v25 |
| **Información de oficina** | Horario, cómo llegar y dónde devolver | gpt-4.1 | ~36.000 | v25 |
| **Prolongación** | Explicación, cuenta, correo de contraseña, pasos, «la web no le deja», devolver tarde, aseguradora y empresa | gpt-5.4 (el único módulo que razona: identificación, resultados del MCP, imprevistos) | ≤ 22.000 | v12, sin las consultas frecuentes |
| **Consultas del alquiler** | El resto de dudas del alquiler, con `buscar_respuesta` | gpt-4.1; las evals deciden frente a gpt-5.4 (§7.3) | ≤ 8.000 + la sección consultada | Nodo «Prolongación y consultas» de la v25 reconvertido (conserva sus Module Change) |

Cada módulo lleva al principio el bloque de **reglas comunes** (§5.10) y, al final, sus propias reglas de
escalado. Cada módulo que no es el Triaje empieza con: «La llamada ya ha empezado: no saludes ni te presentes;
contesta a lo último que ha pedido el cliente».

### 5.5 Triaje

- **Arranque por opción.** En la línea de Prolongación, si la respuesta al saludo es que sí quiere prolongar (o
  devolver más tarde), ejecuta `prolongar_alquiler` en ese mismo turno. En la de Minibús, pregunta el motivo como
  en la v25.
- **Encamina** (sin decir nada antes; la herramienta continúa la conversación):

| Motivo | Herramienta |
|---|---|
| Minibús, punto de encuentro, cómo llegar del aeropuerto a la oficina | `buscar_punto_de_encuentro` |
| Horario, dirección o devolución en una oficina | `informacion_oficina` |
| Prolongar, devolver más tarde, la web no le deja prolongar, contraseña del área de cliente, coche de aseguradora o de empresa | `prolongar_alquiler` |
| Cualquier otra duda del alquiler (reserva no iniciada, recoger tarde, devolver antes u en otra oficina, fianza, combustible, cargos, multas, facturas, requisitos, durante el alquiler) | `consultas_alquiler` |

- **Transfiere él mismo** (sin pasar por un módulo):
  - avería o accidente → ASISTENCIA (también en modo virtual y con Gestión cerrada);
  - reserva nueva → NUEVA RESERVA;
  - queja del minibús (salvo menos de 10 minutos esperando) → MINIBÚS;
  - dato concreto de su reserva que hay que mirar o cambiar → GESTIÓN, solo si está abierta;
  - pide una persona: pregunta una vez qué necesita; si insiste sin motivo → en la línea de Prolongación,
    GESTIÓN si está abierta; en la de Minibús, MINIBÚS (**decisión mía**: cada opción conserva su cola de hoy);
  - idioma no atendido → MINIBÚS (como hoy; ver pendientes de Prolongaciones).
- **Vuelta al Triaje.** Si llega desde un módulo (`volver_al_triaje`), no saluda: encamina con el motivo que le
  pasan y lo que ya dijo el cliente.
- Gestión cerrada, modo virtual, idioma, voz y escalado: bloque de reglas comunes.

### 5.6 Saltos entre módulos

- **El Triaje es el centro**: cada módulo tiene `volver_al_triaje(motivo)` para lo que no le toca. Un módulo
  nuevo solo añade una entrada desde el Triaje y una vuelta, no un salto a cada módulo.
- **Atajos directos** solo entre los pares frecuentes:

| Desde \ hacia | Triaje | Punto de encuentro | Oficina | Prolongación | Consultas |
|---|---|---|---|---|---|
| Triaje | — | herramienta (existe) | herramienta (existe) | herramienta (nueva) | herramienta (existe) |
| Punto de encuentro | MC nuevo | — | MC nuevo | por el Triaje | MC (existe) |
| Oficina | MC nuevo | MC nuevo | — | por el Triaje | MC (existe) |
| Prolongación | MC nuevo | por el Triaje | MC nuevo | — | no hace falta: usa `buscar_respuesta` |
| Consultas | MC nuevo | MC (existe) | MC (existe) | MC nuevo | — |

  MC = Module Change. Las entradas desde el Triaje son herramientas cuyo hijo es el prompt del módulo, como en la
  v25 (se crean por API). **12 Module Change: 4 existen en la v25 y 8 los tiene que crear una persona.**
- **Herramientas de salto:** `message: none`; parámetros `motivo` (y `pregunta` o los de la v25: `tema`,
  `oficina`, `aeropuerto`, `terminal`) con lo que el cliente ya ha dicho, sin datos personales. Los nombres de la
  v25 se mantienen (`buscar_punto_de_encuentro`, `informacion_oficina`, `consultas_alquiler`) para reutilizar las
  evals; la nueva entrada es `prolongar_alquiler(situacion)`.
- **Bucles:** si ya ha habido dos cambios de módulo y el cliente sigue sin lo que necesita, se transfiere a la
  cola que corresponda; en modo virtual o con Gestión cerrada, se le da el horario y se cierra. Evals propias.
- **Idioma tras el salto:** sigue en el idioma en que ya se hablaba (regla de la v25).

### 5.7 Herramientas por módulo

| Módulo | Herramientas |
|---|---|
| Triaje | `buscar_punto_de_encuentro`, `informacion_oficina`, `prolongar_alquiler`, `consultas_alquiler`, `transfer_to_human_agent` |
| Punto de encuentro | `estado_oficina` (D-012), `consultas_alquiler`, `informacion_oficina`, `volver_al_triaje`, `transfer_to_human_agent` |
| Información de oficina | `consultas_alquiler`, `buscar_punto_de_encuentro`, `volver_al_triaje`, `transfer_to_human_agent` |
| Prolongación | `enviar_correo_contrasena`, `pista_correo`, `buscar_respuesta`, `informacion_oficina`, `volver_al_triaje`, `transfer_to_human_agent` |
| Consultas del alquiler | `buscar_respuesta`, `prolongar_alquiler`, `informacion_oficina`, `buscar_punto_de_encuentro`, `volver_al_triaje`, `transfer_to_human_agent` |

Las de contenido:
- **`buscar_respuesta(tema, pregunta)`** → Python «Consultas del alquiler» (§5.9).
- **`enviar_correo_contrasena(email, nombre_completo, fecha_nacimiento)`**: la de la v12 sin cambios de regla
  (spec `casos/prolongaciones/docs/specs/2026-10-17-envio-correo-contrasena.md`). Solo se envía si la consulta por
  ese correo encuentra la reserva y verifica nombre y fecha. Como mucho dos envíos por llamada. Mejora: que
  «Enviar correo» no se ejecute cuando no coincide (hoy se ejecuta y lo rechaza la validación del MCP).
  **Solo se ofrece con un alquiler en curso:** con correo, `consultar_reserva` solo encuentra reservas ya
  iniciadas, así que a quien tiene una reserva que aún no ha empezado (y necesita la contraseña para cambiarla o
  cancelarla) no se le ofrece el envío: se le dan las instrucciones de «¿Has olvidado tu contraseña?» (plan B de
  la v12) y no se le transfiere por ese motivo. **Decisión mía.**
- **`estado_oficina(aeropuerto)`** (Punto de encuentro; añadida el 20/10, D-012): Python que reconoce el aeropuerto
  y devuelve `oficina_cerrada` y la hora de apertura. Sustituye a las listas nocturnas del prompt: el modelo no las
  cruzaba de forma fiable (R39). Desde D-014 calcula con la hora del momento en que se ejecuta y el horario concreto
  de cada oficina (el del prompt); la variable de pruebas `HORA_PRUEBA` manda sobre el reloj en las evals.
- **`pista_correo(numero_reserva, nombre_completo, fecha_nacimiento)`** (nueva): para identificar por número de
  reserva, como en Reembolsos, al cliente que no sabe con qué correo está su alquiler. MCP `consultar_reserva`
  con el número → Python que devuelve al agente solo `verificado` y, si verifica, el **dominio** del correo
  (`email_hint`, p. ej. «gmail.com»). Después el cliente dicta el correo y se envía con `enviar_correo_contrasena`,
  que lo comprueba. **Decidido el 18/10** (resuelve el pendiente «identificar como en Reembolsos» y adelanta la
  pista del dominio que el 17/10 se dejó para después): se identifica por correo o por número de reserva, más
  nombre y fecha de nacimiento, y la regla de envío no cambia (el correo dictado tiene que coincidir). Nunca se
  dice nada más de la ficha que el dominio.

### 5.8 Transferencias

- **Una `transfer_to_human_agent` por módulo**, con `cola` cerrada (`gestion`, `asistencia`, `nueva_reserva`,
  `minibus`), `motivo_transferencia` (los 11 valores de la v12, iguales en todos los módulos) y
  `resumen_para_agente` (en español, sin datos personales). El modelo ya no copia extensiones: se acaban las
  extensiones vacías o mal copiadas.
- **Cadena:** herramienta → Python «Preparar transferencia» (cola + idioma → extensión; redes de seguridad de
  Gestión cerrada y del modo virtual) → Transfer «Initiate customer connection».
- **Gestión abierta** = de lunes a viernes de 8:00 a 21:00, hora peninsular, como hoy en los dos bots
  (RingCentral tiene el horario laboral hasta las 22:00, pero los bots no transfieren de 21 a 22).
- **Gestión cerrada, en dos capas:**
  1. La descripción de la herramienta dice en cada llamada si Gestión está abierta o cerrada (variable
     `gestion_abierta`), y el bloque de reglas comunes lleva la regla de máxima prioridad de la V11.
  2. Si aun así el modelo pide `gestion` con Gestión cerrada, «Preparar transferencia» no transfiere y devuelve
     `resultado: gestion_cerrada` y el horario. Puede quedar una frase incómoda («le paso…» y después «ahora no
     está disponible»), que es mejor que dejar al cliente en la locución. Las evals miden que el modelo no lo
     intente. Cómo cortar la cadena sin transferir se comprueba al construir (§11).
     **Aviso (D-013 y D-014, R34 y R45):** el aviso de la herramienta (`message` tipo `ai`) lo escribe el modelo al
     llamarla, antes del resultado. En Prolongación y Consultas depende de la cola: neutro («Un momento, por favor, no
     cuelgue»), sin «le paso», solo si la transferencia puede no salir (`gestion` con Gestión cerrada, o una cola que
     no sea `asistencia` en modo virtual); en los demás casos, y siempre con `asistencia`, el de siempre. El Triaje sigue con el
     de siempre (el cambio hizo que transfiriera en modo virtual). Que el cliente oiga exactamente ese texto se
     comprueba en la llamada de la Tarea 17.
- **Modo virtual, también en dos capas (D-004):** de 22:00 a 8:00, hora peninsular, solo se transfiere a
  Asistencia. El bloque de reglas comunes lo dice (MODO DE ATENCIÓN, variable `modo_virtual`) y, si aun así el modelo
  pide `minibus` o `nueva_reserva`, «Preparar transferencia» no transfiere y devuelve `resultado: modo_virtual` con
  un detalle fijo que remite a MODO DE ATENCIÓN (no hay compañeros a esta hora, volver a llamar a partir de las ocho;
  una avería o un accidente, a la cola asistencia). La hora se calcula al ejecutarse, como la de Gestión. Si piden
  `gestion` de noche, Gestión también está cerrada y gana `gestion_cerrada`: su detalle remite a COLA DE GESTIÓN
  CERRADA, que da el horario real de Gestión («a partir de las ocho» sería falso de viernes a domingo y en vísperas
  de festivo).
- **`fallback_number`:** la misma cola, nunca Gestión.
- **Quedarse en la llamada:** whisper con resumen y teléfono dictado, el agente pulsa 1 y se graba la
  conversación, como hoy en España. Se mantiene en las cuatro colas mientras se afina el bot (cuesta unos
  0,08 € por llamada y da la transcripción del agente). Whisper: «Llamada del asistente de atención.» + resumen
  + teléfono. Música de espera: «holdacent» en todas.
- **Si la transferencia falla:** la sección de la V11 en el bloque común (reintento, segundo fallo, 112 y
  teléfonos de asistencia y de reservas).
- **Colas:** las de `docs/extensiones.md`, sin cambios: Gestión 18057/18061, Nueva Reserva 18001/18006,
  Asistencia 18034/18035, Minibús 18056/18059. Ninguna a 2114, 2115 ni 2119.

### 5.9 Conocimiento: el bloque de consultas como herramienta

- **Fuente única:** `comun/bloques/consultas-alquiler.md`.
- **En el workflow:** `buscar_respuesta(tema, pregunta)` → Python «Consultas del alquiler», que devuelve el texto
  de la sección del tema (2.000–5.000 caracteres) sin las líneas `>` de notas. El código se genera desde el
  bloque con `casos/atencion-es/codigo/generar_consultas.py`; las pruebas comprueban que cada tema devuelve
  texto, que no se cuela ninguna nota ni ningún «DECIDIR» y que el código generado coincide con el bloque.
- **Temas** (uno por subapartado del bloque): `reserva_no_iniciada`, `recoger_tarde`, `devolucion`,
  `cargos_y_reembolsos`, `requisitos`, `durante_el_alquiler`, `otras`, `telefonos`, más `detalles_prolongacion`,
  `la_web_no_le_deja`, `aseguradora_empresa` y `devolver_tarde` (para Consultas, que no tiene esas secciones en
  su prompt). Si la pregunta no encaja en ningún tema: `otras`.
- **Reparto:** Prolongación lleva en su prompt DEVOLVER TARDE, COCHE DE ASEGURADORA O DE EMPRESA, DETALLES QUE
  PUEDES DAR y LA WEB NO LE DEJA (unos 12.000 caracteres, se usan en casi todas sus llamadas); el resto le llega
  por la herramienta.
- **Regla de uso en el prompt:** responder solo con lo que devuelve la herramienta; si no está, decirlo y seguir
  las reglas de escalado. No leer la sección entera: una o dos frases, como siempre.
- **Por qué no la base de conocimiento de HappyRobot:** está fuera de las versiones (cambiarla cambia producción
  al momento, sin fork ni PR), devuelve trozos por parecido que pueden separar una regla de su excepción, y no
  queda claro qué leyó el bot.
- **Los 7 «DECIDIR»** del bloque se construyen con el texto de Prolongaciones mientras negocio no decida (como
  dice el bloque). Las resoluciones del equipo ya incorporadas (aseguradora, fianza, grúa, sillas, francés con
  cuatro idiomas) se aplican.

### 5.10 Bloque de reglas comunes

`comun/bloques/reglas-comunes.md`, unos 4.000 caracteres, copiado al principio de cada módulo:
- identidad (Daniel, agente de IA de Centauro; trato de usted; «Está hablando con un agente de IA»);
- reglas de voz (una pregunta por turno, frases de ≤ 25 palabras, números en palabras, interrupciones, regla de
  longitud);
- idioma (es, en, it, pt; francés: ofrecer los cuatro; cambio sin comentarlo);
- modo virtual (solo se transfiere a ASISTENCIA);
- Gestión cerrada, regla de máxima prioridad de la V11 (con el horario de Gestión, nunca el de una oficina);
- validar el enfado y no pedir datos personales (salvo los del correo de contraseña, en Prolongación);
- teléfonos que se pueden dar (los cuatro de la V11);
- cómo transferir (`cola`, frase dentro de la herramienta, nada después) y si la transferencia falla;
- cambios de módulo (no saludar, no anunciar el salto, límite de dos).

### 5.11 Voz y agente

«Receive Customer Call» de la v25: una sola voz («Pablo Galvez HR»), idiomas es/en/it/pt, fondo de call center.
`transcription_context` ampliado a prolongaciones, contraseña y correo. Sin horario comercial en el nodo: el modo
virtual lo decide el prompt y lo asegura «Preparar transferencia» (§5.8, D-004).

### 5.12 Extract «Registrar resultado de la llamada»

Uno solo (junta los dos de la v25 y el de la v12), con modelo GPT-5.6 Luna como hoy. Recibe la transcripción y
los datos de las herramientas de **todos** los módulos. Evalúa solo los turnos del bot anteriores a la
transferencia, nunca al agente humano.

| Grupo | Campos |
|---|---|
| Copiados de la entrada (no los decide la IA) | `opcion_menu`, `idioma_linea`, `modo_virtual`, `gestion_abierta`, `festivo_nacional` |
| Motivo | `motivo_principal` (punto_encuentro / info_oficina / prolongar / web_no_deja / devolver_tarde / aseguradora_empresa / reserva_no_iniciada / recoger_tarde / devolucion / cargos_reembolsos / requisitos / durante_alquiler / dato_reserva / reserva_nueva / averia / persona_sin_motivo / queja_minibus / otro / desconocido), `motivos_secundarios` |
| Resultado | `resuelto_por_bot` (si / no / parcial), `motivo_no_resuelto` (necesita_cambio_reserva / necesita_dato_reserva / pide_persona / reserva_nueva / averia / cuelga_o_corte / fallo_bot / sin_respuesta_en_catalogo / gestion_cerrada / ninguno) |
| Recorrido | `modulos_visitados`, `saltos`, `modulo_final` |
| Transferencia | `hubo_transferencia`, `cola_destino`, `motivo_transferencia`, `modulo_transferencia`, `intento_gestion_cerrada` |
| Prolongación y correo | `necesitaba_contrasena`, `dio_pasos_prolongacion`, `correo_contrasena_ofrecido`, `correo_contrasena_resultado`, `envios_correo`, `correo_recibido_confirmado`, `motivo_no_envio`, `pista_correo_usada` |
| Consultas | `temas_consultados`, `pregunta_sin_respuesta` (una frase sin datos personales, para «Respuestas de Daniel») |
| Minibús y oficinas | `aeropuerto_detectado`, `terminal_detectada`, `punto_encuentro_entregado`, `aeropuerto_sin_datos`, `oficina_consultada`, `informacion_oficina_entregada` |
| WhatsApp (los lee la rama de envío) | `whatsapp_ofrecido`, `whatsapp_aceptado`, `punto_whatsapp`, `idioma_cliente` |
| Calidad (solo turnos del bot) | `invento_informacion`, `pregunta_repetida`, `valido_antes_de_informar`, `cliente_molesto`, `verbalizacion_acciones_internas`, `tuteo` |
| Otros | `resumen` (≤ 25 palabras), `turnos_agente` |

La penalización de 50 €/día, las tarifas generales y los teléfonos de Benidorm y Torrevieja no son fallos
(pendiente del extract de Prolongaciones).

## 6. Medición

**Una misma medición para los tres workflows** (el nuevo, Prolongaciones y Minibús ES), con un script nuevo de
solo lectura, `scripts/medir_bots.py`, que parte de los runs de HappyRobot, sus outputs, la facturación y
RingCentral. Las cifras del extract solo se usan para repartir por motivo.

| Indicador | Definición | Fuente |
|---|---|---|
| Llamadas reales | Runs completados con al menos un turno del cliente, sin llamadas web ni de prueba | Runs |
| **Resolución real** | Sin intento de transferencia, sin rellamada del mismo número en 48 h (a cualquiera de los bots) y sin corte antes de que el bot conteste (≥ 2 turnos del cliente) | Outputs de «Initiate customer connection», `from_number` en hash, transcripción |
| Transferencias | % de llamadas con intento; % que llega a un agente; perdidas por no pulsar 1, por colgar esperando o a los 300 s | Outputs + `scripts/emparejar_ringcentral.py` |
| Gestión cerrada | Intentos de transferir a Gestión cerrada (los devuelve «Preparar transferencia»). Transferencias ejecutadas: tienen que ser 0 | Outputs |
| **Coste** | Créditos por llamada (`GET /billing/usage/runs/{run_id}`), separados en LLM por módulo y voz (bot hablando / escuchando al agente). **Créditos por llamada resuelta** = créditos totales / llamadas resueltas | API de facturación |
| Saltos | Cambios de módulo por llamada; % con 3 o más | Outputs de las herramientas de salto |
| Duración | Media y cortes a 600 s | Runs |
| Calidad | Auditoría semanal de 30 llamadas al azar (estratificada: resueltas y transferidas), mirando solo los turnos del bot; misma auditoría de los bots actuales para comparar | Transcripciones |

- Todo por opción del menú y por franja (Gestión abierta, Gestión cerrada, modo virtual).
- Rutina diaria y artefacto propios del workflow nuevo (`casos/atencion-es/rutinas/`), listos antes de conectar
  la primera línea. Las rutinas de Minibús y Prolongaciones siguen midiendo los bots actuales.

## 7. Evals

### 7.1 Reutilizadas (se copian por API a los nodos nuevos y se adaptan)
- **Triaje:** las 24 de la v25. Cambian las que esperan `extension_destino` (ahora `cola`).
- **Punto de encuentro e Información de oficina:** las de sus nodos en la v25.
- **Las 127 de Prolongaciones**, repartidas:
  - a **Prolongación**: Prolongación base, Devolver tarde y precio, La web no le deja, Aseguradora y empresa,
    Correo de contraseña (v12), Cierre, y las de escalado, bordes, idiomas, HOR y FDS que traten de prolongar;
  - a **Consultas**: Reserva no iniciada, Recoger tarde y oficinas, Devolver antes u otra oficina, Fianza,
    combustible y cargos, Requisitos y durante el alquiler, NOINI y el resto de FDS;
  - cambian de expectativa las que hoy transfieren a MINIBÚS o a GESTIÓN por algo que ahora tiene módulo (p. ej.
    ESC-04 punto de encuentro → `buscar_punto_de_encuentro`; RECOG-04 horario de oficina → `informacion_oficina`)
    y las cinco de la V11 que ya cambiaban con la v12 (PROL-03, PROL-04, ASEG-06, WEB-08 y WEB-09).

### 7.2 Nuevas
- **SALTOS:** cada dirección de la matriz (§5.6) al menos dos veces; vuelta al Triaje sin saludar y sin repetir
  preguntas; ping-pong (tercer salto → transfiere); idioma tras el salto.
- **GESTIÓN CERRADA en cada módulo:** pide una persona, dato de su reserva, «la web no deja» y no coincide el
  correo; y el resultado `gestion_cerrada` de «Preparar transferencia».
- **TRIAJE POR LÍNEA:** en la línea de Prolongación «sí, quiero prolongar» → `prolongar_alquiler` sin más
  preguntas; dudas y minibús desde la línea de Prolongación; prolongar desde la línea de Minibús.
- **MODO VIRTUAL** en cada módulo (solo ASISTENCIA).
- **`buscar_respuesta`:** elige bien el tema; con la sección devuelta responde en una o dos frases; si no está en
  la sección, no inventa.
- **`cola` correcta** en cada transferencia y **`pista_correo`** (verifica y da solo el dominio).
- Las evals no ejecutan el MCP: el resultado de las herramientas va como mensaje `tool`, como en la v12.

### 7.3 Criterio
- Cada eval se corre 3 veces. **Críticas** (Gestión cerrada, avería, correo que no coincide, no inventar
  teléfonos, `cola` correcta): 3 de 3. **Resto:** ≥ 90 % de las ejecuciones.
- **Modelo de Consultas:** el mismo juego con gpt-4.1, gpt-4.1-fast y gpt-5.4. Se elige el más barato que quede a
  ≤ 3 puntos del mejor y sin fallos críticos.

## 8. Plan de migración por opciones del menú

### 8.1 Cómo se conecta una opción
- **Se mueven las líneas actuales** (decidido el 18/10): las dos de Prolongación (ES y EN) en la fase 1 y las dos
  de Minibús ES en la fase 2. RingCentral no cambia: la opción del menú sigue llamando al mismo número.
- **Conectar una opción** (lo hace una persona al pasar a producción):
  1. publicar en el workflow antiguo una versión igual a la de producción pero sin esas líneas (p. ej.
     `V13 · V11 sin las líneas de Prolongación`), o despublicarlo, según lo que permita HappyRobot (§11);
  2. publicar la versión del workflow nuevo con esas líneas en su trigger.
- **Volver atrás** = lo contrario: republicar la versión antigua con sus líneas (V11, o la de Minibús que esté en
  producción) y quitar las líneas del workflow nuevo. Las versiones antiguas no se editan: siguen bloqueadas tal
  como están.
- **Ensayo:** antes de la fase 1 se ensaya el movimiento completo, ida y vuelta, con la línea de pruebas «Test SIP
  RingCentral» y un workflow de pruebas. Objetivo: vuelta atrás en menos de 30 minutos, en horario de oficina.
  Por eso la fase 1 empieza un martes a las 10:00.
- La tabla línea → (opción, idioma) de «Contexto de la llamada» usa los números de esas líneas desde el principio.
- Cada cambio se apunta con fecha y hora en los pendientes del caso.
- **Module Change:** los 8 nuevos los crea en el editor el responsable del caso (jzerpa), cuando el plan de
  construcción lo pida.
- **Llamadas de prueba de la puerta 0:** por web, como en Reembolsos (`from_number` = `web`). Si para eso hay que
  publicar la versión en *development*, lo hace una persona.

### 8.2 Fases

| Fase | Qué se conecta | Cuándo | Control |
|---|---|---|---|
| 0 | Nada: construcción, evals y llamadas de prueba | — | — |
| **1** | **Prolongación ES y EN** | Un martes a las 10:00, con la puerta 0 superada | Prolongaciones V11, mismas semanas anteriores |
| 2 | Minibús ES y EN | Tras superar la puerta 1 (unas 2–3 semanas después). Antes hay que cerrar el experimento de la v25 | Minibús ES v25 (y v22) |
| Después (por decidir) | Gestión cuando está cerrada (fines de semana y de 21 a 8: hoy solo suena la locución; el sábado 10/10 se perdieron 504 llamadas); triaje en Nueva Reserva (soltando la llamada); Gestión en horario | Una por una, cada una con su puerta | Lo de hoy |

**Por qué Prolongación primero:** es donde está el ahorro (118 créditos por llamada frente a 64) y la mejora de
resolución (respuestas nuevas, correo de contraseña); su línea base está medida a diario desde el 05/10; y los
módulos nuevos (Prolongación, Consultas, `buscar_respuesta`) son justo lo que hay que validar. En Minibús el
cambio es pequeño (la v25 ya es modular).

### 8.3 Cómo se compara
- **Antes y después por semanas completas:** las dos semanas de la línea con el bot nuevo frente a las dos
  semanas anteriores con el bot actual, medidas con el mismo script, por día de la semana y por franja.
- **Muestra:** unas 600 llamadas a la semana en Prolongación y unas 1.000 en Minibús ES. Con dos semanas por lado,
  una diferencia de 4–5 puntos en la resolución ya es real; si sale entre −2 y +4 puntos, decide el coste.
- **Si queda dudoso** (diferencia pequeña o el volumen cambia mucho), una semana de vuelta al bot actual para
  descartar la temporada.

### 8.4 Puertas

**Puerta 0 · antes de conectar la primera línea**
1. Evals: críticas 3 de 3 y resto ≥ 90 %.
2. 25 llamadas de prueba por voz con guion: prolongar con y sin cuenta, correo (enviado y no coincide), pista del
   dominio, saltos de ida y vuelta, Gestión cerrada (llamando fuera de horario), modo virtual, avería, reserva
   nueva, inglés, italiano y francés. Ningún fallo crítico.
3. Caso «coincide» del correo probado con una reserva real (pendiente de la v12). Si no se ha podido probar, se
   conecta con `enviar_correo_contrasena` desactivada y el plan B de la web.
4. Créditos por llamada en las pruebas ≤ 80 en llamadas de prolongación.
5. Medición, rutina y artefacto funcionando con los runs de prueba.
6. Movimiento de líneas y vuelta atrás escritos y ensayados con la línea de pruebas (§8.1).

**Puerta 1 · Prolongación, tras dos semanas** (tienen que cumplirse todas)
- Resolución real no peor que la de la V11 (diferencia ≥ −2 puntos); objetivo ≥ 50 %.
- Créditos por llamada ≤ 80 y créditos por llamada resuelta ≤ 70 % de los de la V11.
- % de transferencias ≤ V11 + 2 puntos; % que llega a un agente ≥ V11; 0 transferencias ejecutadas a Gestión
  cerrada y 0 a 2114, 2115 o 2119.
- Rellamadas en 48 h y cortes a 600 s no peores que en la V11.
- Auditoría: fallos del bot no peores que en la V11 y ningún fallo crítico (dato inventado que perjudique al
  cliente, correo enviado sin coincidir, cliente dejado en la locución de Gestión).
- ≤ 2 % de llamadas con 3 o más saltos.

**Puerta 2 · Minibús, tras dos semanas:** lo mismo frente a la v25 (resolución ≥ 47 %, ≤ 64 créditos por
llamada) y además punto de encuentro entregado y WhatsApp enviados no peores que en la v25.

**Vuelta atrás inmediata (cualquier día):** dos fallos críticos en un día; errores de herramientas en más del 5 %
de las llamadas de un día; o resolución real 10 puntos por debajo del control dos días seguidos.

## 9. Coste esperado (estimación, a confirmar)

Supuestos: créditos por respuesta medidos (Triaje 2,1; Punto de encuentro 3,6–3,9; Oficina 4,8–5,4); un prompt de
gpt-5.4 de ~22.000 caracteres a 4–5 créditos por respuesta; Consultas con gpt-4.1 a 2–2,5; voz a 16 créditos por
minuto hablando el bot y 3,6 escuchando al agente.

| Línea | Hoy | Bot único |
|---|---|---|
| Prolongación | 118 (≈ 89 de LLM + 29 de voz) | 60–75 (LLM 30–45 con los turnos del correo y la identificación) |
| Minibús ES | 64 | 55–60 (las dudas del alquiler pasan de gpt-5.4 a Consultas) |

El extract también gasta créditos en cada llamada: se mide aparte.

## 10. Repo

- Caso nuevo `casos/atencion-es/`: `CLAUDE.md`, `docs/decisiones.md`, `docs/workflows.md`, `docs/pendientes.md`,
  `docs/specs/`, `prompts/atencion-es/<versión>/`, `codigo/` (Python de los nodos y sus pruebas) y `rutinas/`.
- Bloques comunes: `comun/bloques/consultas-alquiler.md` (existe) y `comun/bloques/reglas-comunes.md` (nuevo).
- Script de medición: `scripts/medir_bots.py`.
- Al construir: `docs/extensiones.md` anota que el workflow nuevo usa las mismas colas.

## 11. Qué hay que comprobar al construir

1. Qué copia el duplicado: Module Change (con sus destinos), evals y la configuración del agente de voz. Si no
   copia los Module Change, la persona crea los 12.
2. Que un Module Change pueda volver al Triaje (el primer módulo del agente).
3. Que el módulo de destino ve el historial (la v25 funciona como si sí).
4. Cómo cortar la cadena de la transferencia sin transferir (Transfer sin número o Paths dentro de la herramienta)
   y qué recibe el agente.
5. Que el whisper es lo que mantiene al bot en la llamada y que sin whisper la suelta (Italia: 0,7 min tras
   transferir), para la futura entrada de Nueva Reserva. Confirmarlo con HappyRobot.
6. Que un nodo Python acepta el código de `buscar_respuesta` (unos 35.000 caracteres de texto).
7. Que la tabla de Twin del workflow nuevo se crea sola con los campos del extract.
8. Horario real de Minibús y Nueva Reserva de noche (modo virtual para la línea de Prolongación, §5.2).
9. Cómo se mueve una línea entre workflows: si basta con publicar el antiguo sin ella o hay que despublicarlo; si
   molesta que el número siga en versiones antiguas o borradores (aparece en muchas versiones de Minibús ES y de
   Prolongaciones); cuánto tarda en entrar la primera llamada por el workflow nuevo.

## 12. Decidido, mis decisiones y preguntas abiertas

**Decidido con el responsable (18/10):**
- workflow nuevo duplicando la v25; Triaje + 4 módulos; gpt-5.4 solo en Prolongación; consultas como
  herramienta versionada; un extract único; seguir en la llamada tras transferir en gestión;
- conectar moviendo las líneas actuales al pasar a producción (§8.1);
- identificar por correo o por número de reserva, con la pista del dominio y sin cambiar la regla de envío (§5.7);
- de 22 a 8 h, en las dos líneas, solo se transfiere a Asistencia (§5.2);
- Gestión no atiende los festivos nacionales (§5.2).

**Decisiones mías (revisar):**
- Nombre del workflow y del caso («Centauro Atención España», `casos/atencion-es/`).
- En la línea de Prolongación, el modo virtual se avisa solo cuando el cliente pide una persona (§5.2).
- «Persona sin motivo»: cada línea conserva su cola de hoy (§5.5).
- Correo de contraseña solo con un alquiler en curso; con una reserva que aún no ha empezado, plan B (§5.7).
- Prolongación primero y antes-después por semanas (§8).
- Umbrales de las puertas (§8.4).

**Para negocio (no bloquean la construcción):**
- Los 7 «DECIDIR» del bloque de consultas.
- Si se conecta después la opción de Gestión cuando está cerrada.

**Queda al constructor:** el texto de los prompts dentro de lo que dice este spec, la forma de cortar la cadena de
la transferencia (§11.4), los nombres de los nodos Python y el orden de los pasos de construcción (plan aparte).
