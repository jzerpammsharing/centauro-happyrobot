# Workflows del caso Prolongaciones

## Centauro Prolongacion Spain (`01a0d9de-b1cd-7bc9-bafc-f5117bd57249`, slug `tiz1bci7y0dh`)

Voicebot de la opción PROLONGACIÓN del menú telefónico de Centauro España. El agente se llama
«Daniel Prolongaciones». Está en la carpeta de Centauro (`019d8144-ce27-7aaf-b9e5-21d006083063`).
Copia de la configuración: `../prompts/prolongacion-es/`.

### Flujo (Version 11)

Son 8 nodos en línea. No hay condiciones, horario nocturno ni derivación fuera de horario: el agente
atiende siempre. Lo único con horario es la cola de Gestión.

| # | Nodo | Tipo | Persistent ID | Qué hace |
|---|---|---|---|---|
| 1 | Inbound Call | Trigger «Inbound to number» | `01a0da06-7f3b-7b5a-9af0-e424300d057c` | Dos líneas SIP de entrada: una para español (por defecto) y otra para inglés. Da `from_number` y `to_number`. |
| 2 | Calcular idioma y saludo | Python Sandbox | `01a0da06-917d-7e9c-9b1c-153df5946a48` | Ver «Calcular idioma y saludo» más abajo. |
| 3 | Resolver colas por idioma | Python Sandbox | `01a0da07-411e-71c5-84ce-499952b43d8e` | Ver «Resolver colas por idioma» más abajo. |
| 4 | Receive Customer Call | Inbound Voice Agent | `01a0da07-a2b9-7e69-942f-fca238dc2334` | Agente «Daniel Prolongaciones». Voces Pablo Galvez HR, Pablo HR y Bruno HR. Idiomas es, en, it y pt. Aviso legal grabado y fondo de call center. |
| 4.1 | Prolongacion | Prompt (único módulo) | `01a0da07-a2b9-7e69-942f-fca354afa1db` | Prompt de unos 54 KB. Modelo `gpt-5.4` (fast). Usa las variables `idioma_nombre` y `gestion_abierta`. |
| 4.2 | transfer_to_human_agent | Tool | `0f790e71-8013-43e1-864b-914666f034b2` | Ver «transfer_to_human_agent» más abajo. |
| 4.3 | Initiate customer connection | Transfer (hijo de la tool) | `01a0da09-043d-70ea-8460-0b0db98c258f` | Ver «Initiate customer connection» más abajo. |
| 5 | Registrar resultado de la llamada | AI Extract | `01a0da09-35ef-7743-964e-73d51ceb1a22` | Modelo GPT-5.6 Luna. Campos más abajo. |

**Calcular idioma y saludo** (nodo 2):
- **Idioma:** sale del número marcado. La línea inglesa da `en`; cualquier otra, `es`.
- **Saludo:** «buenos días» de 06:00 a 13:00 y «buenas tardes» el resto.
- **Otras salidas:**
  - `mensaje_inicial`: el saludo con la pregunta de si quiere prolongar;
  - `recording_id`: el aviso legal;
  - `telefono_dictado`: el número del cliente cifra a cifra, para el whisper;
  - `hora_cet`.
- **`gestion_abierta`:** true de lunes a viernes de 08:00 a 21:00, hora peninsular.

**Resolver colas por idioma** (nodo 3):
- Elige las cuatro colas según el idioma (es o en; cualquier otro idioma cae en es).
- Las devuelve como `sip:<ext>@hrpbx.buscentauro.com`.
- Si `gestion_abierta` es false, sustituye `cola_gestion_reserva` por el texto «NO DISPONIBLE AHORA…».

**transfer_to_human_agent** (nodo 4.2): parámetros obligatorios:
- `extension_destino`: copia literal de una de las cuatro colas;
- `motivo_transferencia`;
- `resumen_para_agente`: en español y sin datos personales.

**Initiate customer connection** (nodo 4.3):
- **Destino:** `number` = `extension_destino`.
- **Destino de reserva:** `fallback_number` = `cola_gestion_reserva`.
- **Whisper:** «Llamada del asistente de prolongaciones. <resumen> Teléfono del cliente: <teléfono dictado>».
- El agente tiene que pulsar 1.
- Se graba la conversación transferida.

Notas:
- **Sin fases.** El agente tiene un solo módulo y una sola herramienta.
- **Sin herramientas de consulta.** No hay ninguna que devuelva vacío a propósito, como pasa en Minibús.
- **Saludo.** Lo dice el agente como mensaje inicial (`mensaje_inicial`). El prompt le prohíbe
  repetirlo.
- **Límites de tiempo.** No figuran en la configuración, pero se han visto en los runs: unos 600 s
  por llamada (`max_duration_reached`) y 300 s esperando a un agente (`whisper_transfer_timeout`).

### Colas a las que transfiere

| Uso | Español | Inglés | Horario |
|---|---|---|---|
| Gestión de reserva (cola por defecto) | 18057 | 18061 | L–V 08:00–21:00 según el bot. En RingCentral no atiende nadie el fin de semana (ver pendientes). |
| Nueva reserva | 18001 | 18006 | 7 días |
| Asistencia (avería o accidente) | 18034 | 18035 | 7 días |
| Minibús, punto de encuentro o idioma no atendido | 18056 | 18059 | 7 días |

- En el código, 18034 y 18035 se llaman «RA ES-ES-Opciones» y «RA ES-EN-OPCIONES». Esos nombres vienen
  de los menús 2114 y 2115, que usaba la V6. Las colas reales son de agentes: «RA ES-ES AVERÍAS» y
  «RA ES-EN Breakdowns».
- La V11 no transfiere a 2114, 2115 ni 2119 (C-001).
- Detalle y colas compartidas con Minibús: `../../../docs/extensiones.md`.

### Comportamiento esperado de Daniel (prompt de la V11)

1. **Arranque.** El saludo automático pregunta si quiere prolongar un alquiler en curso. El menú se
   marca mal a menudo, así que Daniel decide el motivo en silencio con la respuesta. Ruido, restos del
   menú o frases sueltas no son un motivo: pregunta «¿en qué puedo ayudarle?». Si tras dos intentos
   sigue sin entender, transfiere a Gestión.
2. **Prolongar** (el caso principal), en este orden:
   1. Explica en dos frases que la prolongación la hace el cliente desde su área de cliente en
      centauro punto net o en la app, que depende de la disponibilidad y que verá el precio antes de
      pagar.
   2. Pregunta si ha entrado alguna vez en su cuenta.
   3. Si no ha entrado, le explica cómo crear la contraseña con «¿Has olvidado tu contraseña?» y el
      correo que dio en la oficina.
   4. Le da los pasos: «Mis reservas y facturas» > «Gestionar mi reserva» > «Prolongar mi reserva».
   5. Cierra con el recordatorio y el aviso fijo: si la web no le deja, tiene que devolver el coche en
      la fecha y hora del contrato.
   - Nunca da los pasos sin saber antes si el cliente ha entrado en su cuenta.
   - Nunca se despide sin haber dado los pasos.
3. **Devolver tarde.** No hay cortesía y el alquiler se cuenta por periodos de 24 h. Devolver tarde
   cuesta el tiempo extra más 50 € por día; esa cifra solo la da si se la piden. Nunca transfiere por
   esta pregunta.
4. **Coche de aseguradora, mutua o empresa.**
   - Si llama el cliente, no se transfiere por ese motivo: se prolonga igual que cualquier alquiler.
   - Si llama la propia aseguradora, una agencia o un gestor de empresa, transfiere a Gestión con el
     motivo `aseguradora`.
5. **La web no le deja.**
   - Pregunta una vez qué le dice la web.
   - Si el coche no está disponible, el cliente tiene que devolverlo en fecha. Si acepta, le pasa a
     Nueva reserva para hacer otra.
   - Si falla el pago, le propone alternativas, una por turno, antes de transferir.
6. **Consultas frecuentes** que responde sin transferir:
   - reserva que aún no ha empezado (hay que cancelarla y hacer otra);
   - recoger antes o después de la hora: la reserva se guarda 12 h; servicio de espera por vuelo o tren;
   - devolver antes, en otra oficina o con la oficina cerrada;
   - fianza, combustible, cargos, multas y facturas;
   - requisitos y conductores;
   - incidencias durante el alquiler, sillas, cadenas, mascotas y salir de España.
7. **Qué no hace nunca:**
   - dar el precio de la prolongación;
   - confirmar datos de la reserva del cliente;
   - pedir datos personales;
   - prometer disponibilidad;
   - decir que hay cortesía al devolver;
   - dar el teléfono de una oficina. Excepción: las oficinas de Benidorm y Torrevieja, solo para el
     servicio de entrega.
8. **Estilo.**
   - Como mucho dos frases y una pregunta por turno.
   - Cada pregunta se hace una sola vez y nunca más de dos.
   - Los números se dicen en palabras.
   - Si el cliente está molesto, valida su emoción antes de informar.
9. **Gestión cerrada** (nuevo en la V11, con máxima prioridad):
   - no transfiere casos de gestión ni anuncia transferencias;
   - avisa del cierre en el primer turno en que el cliente pide una persona;
   - el horario L–V 8–21 es el del equipo de gestión, nunca el de una oficina;
   - Asistencia, Nueva reserva y Minibús siguen funcionando con normalidad.
10. **Escalado:**

    | Motivo | Cola | `motivo_transferencia` |
    |---|---|---|
    | Dato de su reserva concreta, contrato vencido que quiere explicar, no ve la reserva | Gestión | `pregunta_reserva_concreta` |
    | Error de la web tras probar alternativas, correo de contraseña que no llega, no encuentra la opción tras dos intentos | Gestión | `error_tecnico` |
    | Coche no disponible y quiere que alguien lo revise | Gestión | `web_no_disponible` |
    | Reserva no iniciada que prefiere que gestione un compañero | Gestión | `no_iniciada` |
    | Aseguradora, mutua, agencia, partner o gestor de empresa (no el cliente) | Gestión | `aseguradora` |
    | Cliente enfadado o reclamación hablada | Gestión | `enfado` |
    | Servicio de espera hoy, horario u oficina, objetos olvidados, grúa, cargo concreto, persona sin motivo | Gestión | `otro` |
    | Pide reserva nueva o acepta que se la preparen | Nueva reserva | `nueva_reserva` |
    | Avería, accidente o aviso de batería (si acepta) | Asistencia | `asistencia` |
    | Minibús, punto de encuentro, idioma no atendido | Minibús | `minibus` |

    El anuncio de la transferencia y la llamada a la herramienta van en el mismo turno.
11. **Si la transferencia falla:**
    - al primer fallo, lo reintenta una vez;
    - al segundo, pide al cliente que vuelva a llamar en unos minutos;
    - si es una avería, le da el teléfono de asistencia y le recuerda el 112;
    - si quería una reserva nueva, le da el teléfono de reservas.
12. **Idiomas.**
    - Atiende él mismo en español, inglés, italiano y portugués.
    - En francés dice que no hay atención y ofrece seguir en español o en inglés.
    - Si no puede seguir al cliente en ninguno de esos idiomas, le pasa a Minibús.
    - Un saludo suelto en otro idioma no cuenta como cambio de idioma.

### Campos del extract («Registrar resultado de la llamada»)

Se leen con el prefijo `response.`. Valores permitidos:

| Campo | Valores |
|---|---|
| hubo_transferencia | si / no |
| resuelto_sin_transferencia | si / no |
| cola_destino | gestion_reserva / nueva_reserva / asistencia / minibus / ninguna |
| motivo_transferencia | no_iniciada / web_no_disponible / pregunta_reserva_concreta / aseguradora / enfado / error_tecnico / minibus / asistencia / nueva_reserva / otro / ninguno |
| rellamada | si / no |
| tipo_consulta | prolongacion / devolver_tarde / web_no_deja / precio / reserva_concreta / otra_gestion / fuera_de_alcance |
| necesitaba_contrasena | si / no |
| cliente_molesto | si / no |
| valido_antes_de_informar | si / no / no_aplica |
| pidio_dato_personal | si / no |
| dijo_precio_o_penalizacion | si / no |
| dedujo_datos_reserva | si / no |
| invento_informacion | si / no |
| extension_vacia | si / no |
| pregunta_repetida | si / no |
| llamada_fuera_de_alcance | si / no |
| duracion_segundos | número |
| turnos_agente | número |
| resumen | una frase de 25 palabras como máximo |

El extract no es fiable: ver las reglas de análisis del `CLAUDE.md` del caso.

### Versiones

`is_version_locked` = la versión se ha publicado alguna vez. Las fechas de producción (hora de Madrid)
salen del análisis de llamadas del 5 al 11 de octubre, no de HappyRobot.

| Versión | Slug | Nombre / cambio | Estado (11/10/2026) | En producción |
|---|---|---|---|---|
| Version 1–4 | dsjp09sfqce4, f9klk5afdrt6, q02iy6m5ucm7, jsfzlajc7ht0 | pruebas | nunca publicadas | — |
| (Version 5) | — | no aparece en HappyRobot | — | — |
| Version 6 | raj41i941z54 | primera en producción; averías a los menús 2114/2115 | publicada antes | 05/10 13:59 → 07/10 |
| Version 7 | fftgzxcuqdkj | V6 con averías a 18034/18035 | publicada antes | 07/10 |
| V8 | 5qzsupu4v4w8 | Daniel con todas las respuestas (aseguradoras fase 1) | publicada antes | 07/10 22:48 → 09/10 13:54 |
| V9 | xn2gx6zswa5h | Daniel: responder más sin transferir (caso 1) | publicada antes | 09/10 13:54 → 10/10 20:16 |
| V10 | fg6e9yqdgwok | V9 + horario de la cola de Gestión | publicada antes | 10/10 20:16 → 11/10 11:31 |
| **Version 11** | **2g1bxzyzazpp** | V10 + regla de Gestión cerrada, «no pudo recoger a su hora» y «recoger antes» | **publicada (live)** | desde el 11/10 entre 11:31 y 11:52 (primer run a las 11:52) |
| v12 | mnhi8x9j8ce7 | v12 · V11 + envío del correo de contraseña (fase 1) | sin publicar (borrador del 17/10) | — |

version_id de las versiones publicadas:
- V6 `01a0fc08-5131-7307-959c-4b5508c11fad`
- V7 `01a1156a-f585-7546-b066-78447d146052`
- V8 `01a1179d-e2bc-7093-81e1-b0ed111a6802`
- V9 `01a11f73-b616-7083-8913-ebef21017aa0`
- V10 `01a126ac-ec56-787a-9b03-641a0e218fd6`
- V11 `01a12a23-10e9-7575-bf06-6c77472ca128`
- v12 (sin publicar) `01a14967-1843-78bc-89ed-0241ed3b4daa`

### Cambios de la V10 a la V11

Solo cambia el prompt de «Prolongacion». Para ver el diff, desde la raíz del repo:
`git diff --no-index casos/prolongaciones/prompts/prolongacion-es/v10/prolongacion.md casos/prolongaciones/prompts/prolongacion-es/v11/prolongacion.md`.
1. **Nuevo bloque «GESTIÓN CERRADA: REGLA DE MÁXIMA PRIORIDAD»**, al principio del prompt.
   - Además, el arranque, «No insistas», «Cola de Gestión cerrada» y la regla de la cola por defecto
     añaden «solo si está abierta».
2. **«NO PUDO RECOGER A SU HORA».** La reserva se guarda 12 h desde la hora de recogida, dentro del
   horario de la oficina. Nunca hay que decirle que cancele y haga otra.
3. **Recoger antes de la hora.** No se le puede garantizar; puede preguntar en la oficina al llegar.
   Para asegurarse la hora, tiene que cancelar y hacer otra reserva.

«Resolver colas», `transfer_to_human_agent` e «Initiate customer connection» no cambian. Por eso, con
Gestión cerrada, el aviso «NO DISPONIBLE AHORA…» sigue llegando al bot como si fuera un destino (ver
pendientes).

### Cambios de la V11 a la v12 (sin publicar, D-008)

Spec: `specs/2026-10-17-envio-correo-contrasena.md`. Copias: `../prompts/prolongacion-es/v12/`.

1. **Herramienta nueva `enviar_correo_contrasena`** (persistent ID `01a14967-92fa-78e2-b3ef-a2f1d8ec570b`),
   hija del prompt, con cuatro nodos en cadena sobre «Centauro MCP»:
   - «Comprobar correo (consultar_reserva)» `01a14967-9302-788f-974c-9e48f2817298`;
   - «Decidir envío» (Python) `01a1496e-6988-7395-be53-09c5dca06973`;
   - «Enviar correo (enviar_reset_contrasena)» `01a1496e-699c-7bd0-af43-cba069b66bf8`;
   - «Resultado para el agente» (Python) `01a1496e-69ad-7004-b3b8-8c6ef64afc58`.
   Solo se envía si el correo coincide; si no, el email llega vacío al MCP de envío y este lo rechaza.
   El código de los dos Python está en `../codigo/` con sus pruebas.
2. **Prompt «Prolongacion»:** sección nueva «ENVÍO DEL CORREO DE CONTRASEÑA»; el párrafo «Si dice que
   no…» ofrece el envío y deja «¿Has olvidado tu contraseña?» como plan B; excepción a «NO pidas…» solo
   para el correo, el nombre y la fecha del envío; cómo deletrear un correo; motivo
   `correo_no_coincide` en el escalado. Para ver el diff, desde la raíz del repo:
   `git diff --no-index casos/prolongaciones/prompts/prolongacion-es/v11/prolongacion.md casos/prolongaciones/prompts/prolongacion-es/v12/prolongacion.md`.
3. **`transfer_to_human_agent`:** motivo `correo_no_coincide` y casos del correo de contraseña en la cola
   de Gestión.
4. **Extract:** cinco campos nuevos y `correo_no_coincide` en `motivo_transferencia` (ver la copia).

«Calcular idioma y saludo», «Resolver colas», «Initiate customer connection» y el agente de voz no
cambian. Evals nuevas: carpeta «Correo de contraseña (v12)» del nodo «Prolongacion» (CORREO-01 a 21);
resultados en `informes/2026-10-17-v12-correo-contrasena.md`.
