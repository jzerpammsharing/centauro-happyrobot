# Plan de implementación · Datos por WhatsApp durante la llamada de Reembolsos

> **Para agentes:** SUB-SKILL OBLIGATORIA: usa superpowers:subagent-driven-development (recomendada) o
> superpowers:executing-plans para ejecutar este plan tarea a tarea. Los pasos usan casillas (`- [ ]`).

**Objetivo:** que el bot de voz de Reembolsos pueda mandar un WhatsApp al cliente, que este escriba
reserva, nombre, email y matrícula, y que esos datos lleguen a la llamada en curso con Signals.

**Arquitectura:** dos workflows nuevos en HappyRobot.
- **W1 «Centauro Reembolsos WhatsApp»** (voz): copia de la V4 con Signals activado y una herramienta
  `enviar_whatsapp` que llama por webhook a W2.
- **W2 «Centauro Reembolsos · Datos por WhatsApp»**: un agente de texto de WhatsApp recoge los datos
  y los publica con **Send Signal** en `session.<session_id>` de la llamada.

**Herramientas:** MCP de HappyRobot (`hr`), Python 3.11 para la lógica del teléfono, git.

**Spec:** `casos/reembolsos/docs/specs/2026-10-12-datos-por-whatsapp.md` (léelo antes de empezar).

## Restricciones globales

- **Nunca** editar ni publicar la V4 (`m87e6xzgo405`) ni ninguna versión publicada. Todo se hace en
  workflows nuevos y en versiones sin publicar.
- **Publicar** lo hace una persona. El agente no ejecuta `manage_versions action=publish`.
- Todas las escrituras en HappyRobot piden confirmación (`.claude/settings.json`); no se esquivan.
- En el repo **no** se guardan teléfonos, nombres, emails, números de reserva, matrículas, API keys
  ni URLs de webhook con secretos. El teléfono de prueba y la API key van como variables del
  workflow en HappyRobot, nunca en el repo.
- Variables en actualizaciones: `{{persistent_id.variable}}`, nunca índices numéricos. Las salidas
  de AI Extract llevan `response.`.
- Después de cambios en bloque: `fix_broken_vars` con `dry_run: true` y, si todo cuadra, sin él.
- Los nodos se localizan por **nombre**: los IDs cambian entre versiones y workflows.
- Idioma de docs, commits y nombres de versión: castellano. Commits con
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- Payload de la señal (fijo en todo el plan):
  `{"origen":"whatsapp","tipo":"datos_whatsapp","numero_reserva":"…","nombre_completo":"…","email":"…","matricula":"…"}`.
- En la transcripción, una señal aparece como turno `user` con
  `<Signal Received>{"key": …, "payload": …}</Signal Received>`, a veces pegada al texto del cliente
  (visto en el workflow «Web agent 2», run `e1995983-6c79-42eb-b17e-ea18cb6936c4`).

## Ajustes al spec que introduce este plan

1. **Idioma de la plantilla:** «Calcular idioma y saludo» siempre devuelve `es` (su tabla
   `NUMEROS_IDIOMA` está vacía) y el agente cambia de idioma durante la llamada. Por eso
   `enviar_whatsapp` recibe un parámetro `idioma` (`es` | `en` | `it` | `pt`) que elige el agente
   según el idioma en que está hablando.
2. **Email y matrícula en la transferencia:** la transferencia usa un susurro (`whisper_transfer`)
   que ahora está vacío, y leer un email en voz alta al agente humano no sirve. En esta versión se
   guardan en el extract (campos `email_whatsapp` y `matricula_whatsapp`) y la forma de enseñarlos al
   agente humano queda en pendientes.
3. **Fase 0:** el tótem ya demuestra que `session_id` tiene valor durante la llamada, que la señal
   despierta al agente y cómo se ve en la transcripción. La única duda que queda (publicar con el
   nodo Send Signal desde otro workflow) se prueba en la Tarea 2 con el propio W2 en modo prueba, sin
   workflows desechables.

La Tarea 8 refleja estos ajustes en el spec.

## Revisión: casos que ninguna prueba cubre del todo

1. **Señal tardía después de dictar y verificar:** el agente debe ignorarla y no volver a consultar.
   Se fija en la Tarea 4 (caso 4.d).
2. **Señal pegada a lo que dice el cliente** (`"Vale. <Signal Received>…"`): el agente debe atender
   las dos cosas. Se fija en la Tarea 4 (caso 4.c).
3. **Reserva con espacios, guiones o minúsculas en WhatsApp:** el agente de texto normaliza antes de
   enviar. Se fija en la Tarea 5 (caso 5.b).
4. **Número español sin prefijo o fijo `9xx`:** `whatsapp_posible` debe ser `false` para fijos y
   `true` para móviles en formato nacional. Se fija en la Tarea 1 (pruebas unitarias).
5. **El agente llama dos veces a `enviar_whatsapp`:** el cliente recibiría dos plantillas. El prompt
   lo prohíbe y la herramienta devuelve `ya_enviado` la segunda vez. Se fija en la Tarea 4
   (caso 4.e).

---

### Tarea 1: Lógica del teléfono (Python, con pruebas)

Decide a qué número se manda el WhatsApp y si tiene sentido ofrecerlo. Es la única pieza con código
propio, así que se prueba en local antes de pegarla en HappyRobot.

**Ficheros:**
- Crear: `casos/reembolsos/codigo/telefono_whatsapp.py`
- Crear: `casos/reembolsos/codigo/test_telefono_whatsapp.py`

**Interfaces:**
- Produce: `normalizar_telefono(numero: str) -> str` (E.164 con `+`, o `""`) y
  `whatsapp_posible(e164: str) -> bool`. La Tarea 3 pega estas dos funciones en el nodo
  «Calcular idioma y saludo».

- [ ] **Paso 1: escribir las pruebas**

```python
# casos/reembolsos/codigo/test_telefono_whatsapp.py
# Ejecutar: python3 -I casos/reembolsos/codigo/test_telefono_whatsapp.py
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from telefono_whatsapp import normalizar_telefono, whatsapp_posible  # noqa: E402

CASOS_NORMALIZAR = [
    ("0034612345678", "+34612345678"),   # formato 00 que llega de la centralita
    ("0039375000000", "+39375000000"),   # extranjero con 00
    ("+34 612 34 56 78", "+34612345678"),
    ("612345678", "+34612345678"),       # nacional sin prefijo
    ("912345678", "+34912345678"),       # fijo nacional
    ("web", ""),                          # llamada web del editor
    ("", ""),
    (None, ""),
    ("anonymous", ""),
]

CASOS_POSIBLE = [
    ("+34612345678", True),    # móvil 6
    ("+34712345678", True),    # móvil 7
    ("+34912345678", False),   # fijo 9
    ("+34812345678", False),   # 8xx
    ("+3461234567", False),    # longitud incorrecta
    ("+39375000000", True),    # extranjero
    ("+447700900000", True),   # extranjero
    ("", False),
]

fallos = 0
for entrada, esperado in CASOS_NORMALIZAR:
    obtenido = normalizar_telefono(entrada)
    if obtenido != esperado:
        fallos += 1
        print("FALLO normalizar_telefono(%r) = %r, esperado %r" % (entrada, obtenido, esperado))
for entrada, esperado in CASOS_POSIBLE:
    obtenido = whatsapp_posible(entrada)
    if obtenido != esperado:
        fallos += 1
        print("FALLO whatsapp_posible(%r) = %r, esperado %r" % (entrada, obtenido, esperado))

print("OK" if fallos == 0 else "%d fallos" % fallos)
sys.exit(1 if fallos else 0)
```

- [ ] **Paso 2: comprobar que fallan**

Ejecutar: `python3 -I casos/reembolsos/codigo/test_telefono_whatsapp.py`
Esperado: `ModuleNotFoundError: No module named 'telefono_whatsapp'`.

- [ ] **Paso 3: escribir las funciones**

```python
# casos/reembolsos/codigo/telefono_whatsapp.py
# Copia exacta de las funciones que van en el nodo «Calcular idioma y saludo» de
# «Centauro Reembolsos WhatsApp». Si se cambian aquí, se cambian también allí.


def normalizar_telefono(numero):
    """Devuelve el número en E.164 (+ y dígitos) o "" si no es un teléfono."""
    texto = str(numero or "").strip()
    digitos = "".join(c for c in texto if c.isdigit())
    if not digitos:
        return ""
    if texto.startswith("+"):
        return "+" + digitos
    if digitos.startswith("00"):
        return "+" + digitos[2:]
    if len(digitos) == 9:
        return "+34" + digitos
    return "+" + digitos


def whatsapp_posible(e164):
    """True si tiene sentido ofrecer WhatsApp a ese número."""
    if not e164 or not e164.startswith("+"):
        return False
    if e164.startswith("+34"):
        return len(e164) == 12 and e164[3] in "67"
    return len(e164) >= 9
```

- [ ] **Paso 4: comprobar que pasan**

Ejecutar: `python3 -I casos/reembolsos/codigo/test_telefono_whatsapp.py`
Esperado: `OK` y código de salida 0.

- [ ] **Paso 5: commit**

```bash
git add casos/reembolsos/codigo/
git commit -m "Reembolsos WhatsApp: lógica del teléfono con pruebas

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Tarea 2: W2 en modo prueba (solo Send Signal, sin WhatsApp)

Crea W2 con su trigger y un Send Signal que manda datos fijos de prueba. Sirve para probar el camino
completo de la señal antes de tener la cuenta de WhatsApp. En la Tarea 5 el Send Signal de prueba se
sustituye por el agente de texto.

**Ficheros:**
- Crear: `casos/reembolsos/prompts/reembolsos-whatsapp-datos/v1/README.md`

**Interfaces:**
- Produce: W2 con un trigger «Predefined request» llamado «Petición desde la llamada» que acepta
  `telefono`, `session_key`, `idioma` y `entorno` (todos string), con autenticación por API key. Su
  URL y su API key se guardan como variables de W1 en la Tarea 3.
- Produce: nodo «Señal de prueba» (Send Signal) que publica el payload fijo en `session_key`.

- [ ] **Paso 1: crear el workflow vacío**

`create_workflow` con:
```json
{"name": "Centauro Reembolsos · Datos por WhatsApp",
 "folder_id": "019d8144-ce27-7aaf-b9e5-21d006083063",
 "icon": "message",
 "source": {"type": "blank"}}
```
Después, `get_workflows` con el `workflow_id` devuelto para obtener el `version_id` editable.

- [ ] **Paso 2: añadir el trigger y la señal de prueba**

`update_workflow_nodes action=add` en esa versión:
```json
[
  {"type": "trigger", "event_id": "b329e750-2e0e-4618-ba65-e04bb6a93c5f",
   "name": "Petición desde la llamada",
   "configuration": {
     "auth_type": "api_key",
     "params": [
       {"name": "telefono", "type": "string", "required": true},
       {"name": "session_key", "type": "string", "required": true},
       {"name": "idioma", "type": "string", "required": true},
       {"name": "entorno", "type": "string", "required": true}
     ]}},
  {"type": "action", "event_id": "019e4c31-7b2a-7f10-9e3d-2f4a6b8c0d1e",
   "name": "Señal de prueba", "parent_node_index": 0,
   "configuration": {
     "deliveryMode": "signal_keys",
     "key": "{{0.session_key}}",
     "body": {"contentType": "application/json",
              "raw": "{\"origen\":\"whatsapp\",\"tipo\":\"datos_whatsapp\",\"numero_reserva\":\"ER00000000\",\"nombre_completo\":\"Prueba Prueba\",\"email\":\"\",\"matricula\":\"\"}"}}}
]
```
Antes de enviarlo, ejecuta `get_node_config_schema` con `event_id` `b329e750-…` y
`019e4c31-…` y ajusta los nombres de campo de `params`, `body` y `key` a lo que devuelva. No
inventes campos.

- [ ] **Paso 3: comprobar la configuración**

`get_node_config_schema` en modo nodo (`version_id` + `node_id`) para los dos nodos.
Esperado: `Validation: PASSED`. Si Send Signal pide `apiKeyId`, para y pide a la persona que cree
una API key de la organización en HappyRobot y te diga su id; no la crees tú.

- [ ] **Paso 4: obtener la URL y la API key del trigger**

`get_node_details` del trigger. Si no muestra la URL ni la API key, pide a la persona que las copie
del editor. **No** las escribas en el repo ni en el chat: la persona las mete directamente como
variables de W1 en la Tarea 3, paso 1.

- [ ] **Paso 5: guardar el README de la versión**

```markdown
<!-- workflow: Centauro Reembolsos · Datos por WhatsApp · versión: v1 (modo prueba) · copiado: AAAA-MM-DD -->
# W2 · v1 (modo prueba)

- Trigger «Petición desde la llamada» (Predefined request, API key): telefono, session_key,
  idioma, entorno.
- «Señal de prueba» (Send Signal): publica en `session_key` el payload fijo
  `{"origen":"whatsapp","tipo":"datos_whatsapp","numero_reserva":"ER00000000","nombre_completo":"Prueba Prueba","email":"","matricula":""}`.
- Sin WhatsApp. Se sustituye en la v2 por el agente de texto.
```
Sustituye `AAAA-MM-DD` por la fecha del día.

- [ ] **Paso 6: commit**

```bash
git add casos/reembolsos/prompts/reembolsos-whatsapp-datos/
git commit -m "Reembolsos WhatsApp: W2 en modo prueba (solo Send Signal)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Tarea 3: W1, copia de la V4 con Signals y la herramienta `enviar_whatsapp`

**Ficheros:**
- Crear: `casos/reembolsos/prompts/reembolsos-whatsapp/v1/calcular-idioma-y-saludo.md`
- Crear: `casos/reembolsos/prompts/reembolsos-whatsapp/v1/herramientas.md`

**Interfaces:**
- Consume: `normalizar_telefono` y `whatsapp_posible` (Tarea 1); la URL y la API key de W2
  (Tarea 2).
- Produce: en «Calcular idioma y saludo», las salidas `telefono_e164` (string) y `whatsapp_posible`
  (bool); la herramienta `enviar_whatsapp(idioma)`, que devuelve `enviado`, `ya_enviado` o `error`.

- [ ] **Paso 1: duplicar la V4**

`create_workflow`:
```json
{"name": "Centauro Reembolsos WhatsApp",
 "folder_id": "019d8144-ce27-7aaf-b9e5-21d006083063",
 "source": {"type": "duplicate", "workflow_id": "01a0defb-9c46-7f81-b966-69ca9d211709",
            "version_id": "01a118af-4989-7a7e-8207-3c6af957f54e"}}
```
Devuelve `creation_pending`: repite `get_workflows` con el nuevo `workflow_id` hasta que la versión
exista; no lo vuelvas a crear. Renombra la versión con `manage_versions action=update`:
`v1 · V4 + datos por WhatsApp`.

Pide a la persona que cree en W1 (ajustes del workflow → variables) tres variables:
`WA_DATOS_URL` (URL del trigger de W2), `WA_DATOS_API_KEY` (su API key) y
`TELEFONO_PRUEBA` (un móvil del equipo, solo para las llamadas web). Ninguna va al repo.

- [ ] **Paso 2: anotar los persistent_id de W1**

`get_workflows` con el `version_slug` nuevo y `get_available_variables` sobre el nodo
«Check Reimbursement Status». Anota en tu contexto (no en el repo) el persistent_id de:
«Calcular idioma y saludo», «Receive Customer Call», «Reembolsos» (el prompt) y «Registrar resultado
de la llamada». Las tareas siguientes los llaman `<PID_IDIOMA>`, `<PID_AGENTE>`, `<PID_PROMPT>` y
`<PID_EXTRACT>`.

- [ ] **Paso 3: añadir la lógica del teléfono a «Calcular idioma y saludo»**

`get_node_details` del nodo para leer el código actual. Añade al final del código, justo antes de
`output = {`, las dos funciones de `casos/reembolsos/codigo/telefono_whatsapp.py` (copia literal) y
estas líneas:

```python
# WhatsApp: numero de destino y si tiene sentido ofrecerlo.
# TELEFONO_PRUEBA solo se usa en llamadas web del editor (from_number = "web").
telefono_prueba = str(input_data.get("telefono_prueba") or "")
if numero_cliente == "web" and telefono_prueba:
    telefono_e164 = normalizar_telefono(telefono_prueba)
else:
    telefono_e164 = normalizar_telefono(numero_cliente)
puede_whatsapp = whatsapp_posible(telefono_e164)
```

Añade a `output` las claves `"telefono_e164": telefono_e164` y
`"whatsapp_posible": puede_whatsapp`. Añade a `input_data` la clave `telefono_prueba` con el valor
`{{use_case_variables.TELEFONO_PRUEBA}}`. Envía la **configuración completa** (es un reemplazo
total) con `update_workflow_nodes action=update`.

- [ ] **Paso 4: probar el nodo**

`test_workflow action=test_node` sobre «Calcular idioma y saludo».
Esperado: salida con `telefono_e164` y `whatsapp_posible`. Con `from_number` = `web` y
`TELEFONO_PRUEBA` vacío: `telefono_e164` = `""` y `whatsapp_posible` = `false`.

- [ ] **Paso 5: activar Signals en el agente de voz**

`get_node_details` de «Receive Customer Call» y `update_workflow_nodes action=update` con la
configuración completa más:
```json
"agentSignalsConfig": {"enabled": true, "shouldRespondOnSignal": true, "customTopics": []}
```
Comprueba con `get_node_config_schema` en modo nodo que aparece en «Current Values».

- [ ] **Paso 6: añadir la herramienta `enviar_whatsapp` y su webhook**

`update_workflow_nodes action=add` con `parent_node_id` = id del nodo prompt «Reembolsos»:
```json
[
  {"type": "tool", "name": "enviar_whatsapp",
   "function": {
     "description": "Envía al móvil del cliente un WhatsApp para que escriba ahí su número de reserva, su nombre completo, su email y la matrícula. Úsala solo si el cliente ha aceptado y solo una vez por llamada.",
     "parameters": [
       {"name": "idioma", "required": true,
        "description": "Idioma en que estás hablando con el cliente ahora mismo. Exactamente uno de: es, en, it, pt."}
     ],
     "message": {"type": "ai", "example": "Un momento, se lo envío.",
                 "description": "Di en pocas palabras, en el idioma del cliente, que le envías el WhatsApp."}}},
  {"type": "action", "event_id": "01926f2b-2973-7ebf-ada1-e984251e27ec",
   "name": "POST petición de datos", "parent_node_index": 0,
   "configuration": {
     "url": "{{use_case_variables.WA_DATOS_URL}}",
     "contentType": "application/json",
     "headers": [{"key": "x-api-key", "value": "{{use_case_variables.WA_DATOS_API_KEY}}"}],
     "bodyMode": "raw",
     "rawBody": "{\"telefono\": \"{{<PID_IDIOMA>.telefono_e164}}\", \"session_key\": \"session.{{<PID_AGENTE>.session_id}}\", \"idioma\": \"{{0.idioma}}\", \"entorno\": \"{{current.execution_environment}}\"}",
     "ignore5XX": false}}
]
```
Sustituye `<PID_IDIOMA>` y `<PID_AGENTE>` por los del paso 2. Comprueba con
`get_node_config_schema` (event `01926f2b-…`) el nombre real de los campos del cuerpo y de la
cabecera de la API key (el nodo del tótem usa `body.raw` con tokens `{{$var:pid.var}}`); usa ese
formato si `rawBody` no valida. La cabecera de autenticación es la que diga el trigger de W2.

- [ ] **Paso 7: comprobar variables**

`fix_broken_vars` con `dry_run: true`. Esperado: sin referencias rotas. Si las hay, corrígelas a
mano con los persistent_id del paso 2 y repite.

- [ ] **Paso 8: prueba de la señal de punta a punta** *(persona + Claude)*

La persona hace una llamada web a W1 desde el editor, con `TELEFONO_PRUEBA` relleno, y dice:
«Llamo por la fianza. ¿Me puede mandar un WhatsApp para escribirle la reserva?». El prompt aún no
tiene las reglas de WhatsApp, así que si el agente no usa la herramienta, la persona le pide
explícitamente «use la herramienta de enviar WhatsApp».

Claude comprueba con `monitor_runs`:
- en el run de W1: `enviar_whatsapp` ejecutada y el POST con `status_code` 200;
- en el run de W2: el trigger recibió `session_key` = `session.<session_id de W1>` y «Señal de
  prueba» terminó sin error;
- en la transcripción de W1: un turno con `<Signal Received>` y `"tipo": "datos_whatsapp"`.

Si la señal no llega, prueba en este orden: `deliveryMode` `combined`; mover el JSON al campo
`message`; revisar si Send Signal necesita `apiKeyId`; revisar el entorno (la llamada del editor
corre en `development`). Si nada funciona, **para**: el diseño pasa a la alternativa con Twin y hay
que volver al spec.

- [ ] **Paso 9: guardar la configuración y commit**

Guarda en `casos/reembolsos/prompts/reembolsos-whatsapp/v1/calcular-idioma-y-saludo.md` el código
completo del nodo y en `herramientas.md` la definición de `enviar_whatsapp` y la configuración del
POST, sin URL ni API key (pon `{{use_case_variables.WA_DATOS_URL}}` tal cual). Cabecera:
`<!-- workflow: Centauro Reembolsos WhatsApp · versión: v1 (<slug>) · nodo: <nombre> · copiado: <fecha> -->`.

```bash
git add casos/reembolsos/prompts/reembolsos-whatsapp/
git commit -m "Reembolsos WhatsApp: W1 con Signals y enviar_whatsapp; señal probada de punta a punta

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Tarea 4: prompt del agente de voz

**Ficheros:**
- Crear: `casos/reembolsos/prompts/reembolsos-v4/receive-customer-call.md` (copia de la V4, base del
  diff)
- Crear: `casos/reembolsos/prompts/reembolsos-whatsapp/v1/receive-customer-call.md`

**Interfaces:**
- Consume: `whatsapp_posible` (Tarea 3), la herramienta `enviar_whatsapp` (Tarea 3), el payload fijo
  de las restricciones globales.

- [ ] **Paso 1: guardar el prompt de la V4**

`get_node_details` del nodo «Reembolsos» en la versión `01a118af-4989-7a7e-8207-3c6af957f54e` y
guarda `prompt_md` en `casos/reembolsos/prompts/reembolsos-v4/receive-customer-call.md` con la
cabecera `<!-- workflow: 01a0defb-… · versión: Version 4 (m87e6xzgo405) · nodo: Reembolsos · copiado: <fecha> -->`.
Esto cierra también el pendiente «guardar en prompts/ los prompts de la versión publicada».

- [ ] **Paso 2: escribir el prompt nuevo**

Copia ese fichero a `casos/reembolsos/prompts/reembolsos-whatsapp/v1/receive-customer-call.md`
y aplica estos cuatro cambios.

**2.a** Debajo de la línea `Fecha de hoy: …`, añade:
```
WhatsApp disponible en esta llamada: {{ index . "<PID_IDIOMA>.whatsapp_posible" }}.
```

**2.b** En IDENTIFICACIÓN, sustituye la frase
`Dile en una frase que vas a mirar su reserva. Pide los datos en tres turnos separados, en este orden:`
por:
```
Dile en una frase que vas a mirar su reserva.

DATOS POR WHATSAPP (solo si "WhatsApp disponible en esta llamada" es true; si es false, ignora este bloque y nunca menciones WhatsApp):
En ese mismo turno, ofrécelo una vez: "Para que no tenga que dictarlo, ¿le mando un WhatsApp a este número y me escribe ahí el número de reserva y su nombre?".
- Si acepta: ejecuta enviar_whatsapp con el idioma en que estáis hablando. Si devuelve enviado, di en ese mismo turno "Se lo acabo de enviar. Mientras le llega, ¿me dice su fecha de nacimiento?" y pasa directamente al punto 3 (fecha de nacimiento). Si devuelve error, di "No he podido enviárselo, lo hacemos por aquí" y sigue con el punto 1.
- Si no acepta, o dice que no tiene WhatsApp en este número: sigue con el punto 1 y no vuelvas a ofrecerlo salvo en la SEGUNDA OFERTA.
- Nunca ejecutes enviar_whatsapp más de una vez por llamada. Si devuelve ya_enviado, no digas nada sobre un segundo mensaje.
- Mientras esperas los datos, no ejecutes consultar_reembolso. Si el cliente dice que no le llega, o pasan dos turnos suyos después de la fecha de nacimiento sin que lleguen, ofrécele una vez dictarlo y, si acepta, sigue con el punto 1.
- Si el cliente pregunta qué tiene que escribir: el número de reserva y el nombre completo del titular; si los tiene a mano, también el email y la matrícula. Puede mandar una captura del correo de la reserva.

Si no se usa WhatsApp, pide los datos en tres turnos separados, en este orden:
```

**2.c** En «No encontrada», justo antes de `Si no, pide que te repita el número de reserva despacio, carácter a carácter, y vuelve a ejecutar.`, añade:
```
SEGUNDA OFERTA: si "WhatsApp disponible en esta llamada" es true y todavía no has ejecutado enviar_whatsapp, en vez de pedir que lo repita despacio, ofrece una vez el WhatsApp con la misma frase de DATOS POR WHATSAPP.
```
Y en «Verificado false», al final de la frase que termina en `Vuelve a ejecutar con los datos corregidos.`, añade:
```
Si el cliente no sabe qué corregir y todavía no has ejecutado enviar_whatsapp, aplica la SEGUNDA OFERTA antes de volver a consultar. Las correcciones de datos que llegaron por WhatsApp se hacen por voz: nunca mandes un segundo WhatsApp.
```

**2.d** Justo antes de `CIERRE`, añade una sección nueva:
```
DATOS QUE LLEGAN POR WHATSAPP

Durante la llamada te puede llegar un mensaje que empieza por <Signal Received>. No lo ha dicho el cliente: es el sistema que te pasa lo que ha escrito por WhatsApp. Puede llegar solo o pegado detrás de una frase del cliente; atiende las dos cosas.

Solo cuenta si el payload trae "tipo": "datos_whatsapp". Cualquier otra señal, ignórala sin comentarla.

Con datos_whatsapp:
- Di "Me ha llegado, gracias." (o equivalente en su idioma). No leas el número de reserva dígito a dígito ni el nombre: lo ha escrito el propio cliente.
- Usa numero_reserva y nombre_completo del payload como los datos 1 y 2 de IDENTIFICACIÓN.
- Si ya tienes la fecha de nacimiento, ejecuta consultar_reembolso en ese mismo turno. Si no, pídela y consulta cuando la tengas.
- No digas en voz alta el email ni la matrícula.
- Si ya habías verificado con datos dictados, o el cliente ya está dictando porque lo eligió, ignora la señal.
- La señal nunca sustituye a la fecha de nacimiento.

Nunca digas "señal", "payload", "herramienta" ni "sistema".
```

Sustituye `<PID_IDIOMA>` por el persistent_id del paso 2 de la Tarea 3.

- [ ] **Paso 3: aplicar el prompt**

`update_workflow_nodes action=update` sobre el nodo prompt «Reembolsos» de W1 con
`{"prompt_md": <contenido del fichero nuevo sin la cabecera>}`. Después `get_node_details` y
comprueba que el texto guardado coincide con el fichero (los cuatro bloques presentes).

- [ ] **Paso 4: añadir `ya_enviado` a la herramienta**

Para que una segunda llamada no mande otra plantilla: añade debajo de `enviar_whatsapp`, antes del
POST, una condición con el contador de llamadas a la herramienta, si HappyRobot lo expone
(`get_available_variables` sobre el POST: busca un campo tipo `callCount` o `called` del propio
tool). Si existe, la rama `callCount > 1` devuelve `ya_enviado` sin llamar a W2. Si no existe,
apúntalo en `docs/pendientes.md` y confía en la regla del prompt.

- [ ] **Paso 5: pruebas con W2 en modo prueba** *(persona + Claude)*

La «Señal de prueba» manda `ER00000000` y `Prueba Prueba`, así que la consulta dará «no encontrada»:
lo que se prueba es la conversación, no la verificación. La persona hace una llamada web por caso y
Claude revisa la transcripción con `monitor_runs`.

| Caso | La persona dice / hace | Esperado en los turnos `assistant` |
|---|---|---|
| 4.a | Acepta el WhatsApp. | Ofrece una vez, envía, pide la fecha de nacimiento en el mismo turno; al llegar la señal dice «Me ha llegado» sin leer el número y consulta con la fecha. |
| 4.b | Rechaza el WhatsApp. | Dictado normal de la V4. No vuelve a ofrecerlo salvo en la segunda oferta. |
| 4.c | Acepta y, justo cuando llega la señal, dice «Vale». | Atiende la señal aunque venga pegada a «Vale». |
| 4.d | Rechaza, dicta y verifica (usar una reserva de prueba que exista, si la hay; si no, simular con la persona leyendo la señal tardía). | Ignora la señal tardía y no vuelve a consultar. |
| 4.e | Acepta y, después, pide «mándemelo otra vez». | No ejecuta `enviar_whatsapp` por segunda vez (o devuelve `ya_enviado`). |
| 4.f | `TELEFONO_PRUEBA` vacío. | Nunca menciona WhatsApp. |
| 4.g | Habla en inglés desde el principio y acepta. | `enviar_whatsapp` con `idioma` = `en`. |

Si un caso falla, ajusta el bloque del prompt que corresponda, vuelve al paso 3 y repite **solo**
los casos afectados.

- [ ] **Paso 6: commit**

```bash
git add casos/reembolsos/prompts/
git commit -m "Reembolsos WhatsApp: prompt de voz con oferta de WhatsApp y lectura de señales

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Tarea 5: agente de texto de WhatsApp en W2

**Bloqueada** hasta que la credencial «Whatsapp Centauro» (`01a0df2b-c1bf-7da3-ab60-dc684d8004c2`)
muestre cuenta de WhatsApp Business, número y las plantillas aprobadas. Comprobación:
`list_integrations integration_slug=whatsapp resource=business-accounts business_id=970312032038916 credential_id=01a0df2b-…`
y después `resource=phone-numbers` y `resource=message-templates`. Si alguna sale vacía, para y avisa.

**Ficheros:**
- Crear: `casos/reembolsos/prompts/reembolsos-whatsapp-datos/v2/agente-whatsapp.md`

**Interfaces:**
- Consume: los cuatro campos del trigger (Tarea 2).
- Produce: la herramienta `pasar_a_llamada(numero_reserva, nombre_completo, email, matricula)`, que
  publica el payload fijo en `session_key`.

- [ ] **Paso 1: plantillas que tiene que dar de alta Centauro en Meta**

UTILITY, sin variables ni botones, nombres `datos_llamada_es`, `datos_llamada_en`,
`datos_llamada_it` y `datos_llamada_pt`. Texto en español (spec, apartado 6):
> Hola 👋 Soy Daniel, el asistente de Centauro Rent a Car con el que está hablando por teléfono.
> Escríbame aquí su número de reserva y el nombre completo del titular. Si los tiene a mano, añada
> también su email y la matrícula del coche. También puede mandarme una captura del correo de la
> reserva.

Las otras tres son traducciones de este texto, con el mismo contenido.

- [ ] **Paso 2: nueva versión de W2 y quitar la señal de prueba**

`manage_versions action=fork` de la v1 de W2, renombrada `v2 · agente de WhatsApp`. En la v2,
`update_workflow_nodes action=delete` de «Señal de prueba».

- [ ] **Paso 3: añadir el agente de texto, la herramienta y el Send Signal**

`update_workflow_nodes action=add` con `parent_node_id` = trigger «Petición desde la llamada»:
```json
[
  {"type": "agent", "event_id": "d2e3f4a5-c6d7-5e8f-9a0b-1c2d3e4f5a6b",
   "name": "Agente de WhatsApp",
   "configuration": {
     "name": "Daniel",
     "channel": "whatsapp",
     "credentialId": "01a0df2b-c1bf-7da3-ab60-dc684d8004c2",
     "recipientNumber": "{{<PID_TRIGGER>.telefono}}",
     "idleTimeoutMinutes": "15",
     "interactiveMessages": {"enabled": false},
     "endSessionOnDeliveryError": true,
     "mediaConfig": {
       "ocr": {"enabled": true, "providerTier": "standard"},
       "transcription": {"enabled": true, "providerTier": "advanced"},
       "voiceNotes": {"enabled": false, "mode": "always"},
       "outboundMedia": {"enabled": false},
       "limits": {"maxFiles": 5, "maxFileSizeBytes": 52428800, "maxTotalSizeBytes": 104857600,
                  "processingTimeoutSeconds": 240, "maxAttempts": 2}}}},
  {"type": "tool", "name": "pasar_a_llamada", "parent_node_index": 0,
   "function": {
     "description": "Pasa a la llamada de teléfono los datos que ha escrito el cliente. Úsala una sola vez, en cuanto tengas el número de reserva y el nombre completo.",
     "parameters": [
       {"name": "numero_reserva", "required": true, "description": "Número de reserva en mayúsculas y sin espacios."},
       {"name": "nombre_completo", "required": true, "description": "Nombre completo del titular, tal como lo escribió."},
       {"name": "email", "required": false, "description": "Email en minúsculas, o vacío si no lo dio."},
       {"name": "matricula", "required": false, "description": "Matrícula en mayúsculas sin espacios ni guiones, o vacía si no la dio."}
     ],
     "message": {"type": "fixed", "example": "Listo, ya se lo he pasado a la llamada. Puede seguir por teléfono."}}},
  {"type": "action", "event_id": "019e4c31-7b2a-7f10-9e3d-2f4a6b8c0d1e",
   "name": "Señal a la llamada", "parent_node_index": 1,
   "configuration": {
     "deliveryMode": "signal_keys",
     "key": "{{<PID_TRIGGER>.session_key}}",
     "body": {"contentType": "application/json",
              "raw": "{\"origen\":\"whatsapp\",\"tipo\":\"datos_whatsapp\",\"numero_reserva\":\"{{$var:1.numero_reserva}}\",\"nombre_completo\":\"{{$var:1.nombre_completo}}\",\"email\":\"{{$var:1.email}}\",\"matricula\":\"{{$var:1.matricula}}\"}"}}}
]
```
Antes de enviarlo: usa en Send Signal exactamente los campos que funcionaron en la Tarea 3, paso 8;
completa `business`, `business_account` y `phone_number` con los valores de los `list_integrations`
del bloqueo; y configura `whatsappTemplateConfig.initialOutboundTemplate` según el esquema
(`get_node_config_schema` del event `d2e3f4a5-…`), con la plantilla elegida por `idioma` (si el
nodo no admite plantilla dinámica, crea una rama por idioma con un nodo de condiciones antes del
agente). `<PID_TRIGGER>` es el persistent_id del trigger.

- [ ] **Paso 4: prompt del agente de texto**

Actualiza el prompt raíz del agente (`update_workflow_nodes action=update`, `prompt_md`) con:
```
Eres Daniel, el asistente de Centauro Rent a Car. El cliente está ahora mismo en una llamada de teléfono contigo y le has mandado este WhatsApp para que escriba datos que cuesta dictar. Tu único trabajo es recoger esos datos y pasarlos a la llamada.

Escribe en el idioma del cliente: {{ index . "<PID_TRIGGER>.idioma" }} (es español, en inglés, it italiano, pt portugués de Portugal). Si te escribe en otro de esos idiomas, cámbiate a ese.

DATOS
- Número de reserva (obligatorio): pásalo a mayúsculas y quítale espacios. No lo rechaces por su formato.
- Nombre completo del titular (obligatorio): tal como lo escribe.
- Email (opcional): en minúsculas. Si no tiene @, pídelo una vez; si no lo corrige, déjalo vacío.
- Matrícula (opcional): en mayúsculas, sin espacios ni guiones.

Si manda una foto o captura, saca de ella el número de reserva y el nombre. Si manda una nota de voz, usa su transcripción. Si ves dos números de reserva, o no se lee bien el nombre, pregunta cuál es antes de seguir.

En cuanto tengas número de reserva y nombre completo, ejecuta pasar_a_llamada con lo que tengas. No esperes al email ni a la matrícula y no insistas en ellos. Ejecútala una sola vez.

Después de pasarlos, a cualquier mensaje responde solo: "Ya se lo he pasado a la llamada. Puede seguir por teléfono."

NUNCA
- Des información de la reserva, de reembolsos, fianzas ni plazos: no tienes acceso. Si te lo preguntan: "Eso se lo cuento por teléfono."
- Pidas la fecha de nacimiento, datos de tarjeta ni documentos.
- Envíes audios ni archivos.
- Digas que eres una persona.

Mensajes cortos, uno cada vez.
```

- [ ] **Paso 5: probar y comprobar variables**

`fix_broken_vars` (`dry_run: true` y luego sin él si hay arreglos). `test_workflow action=test_all`
sobre la v2. Esperado: sin errores de validación (el agente puede salir «skipped»).

- [ ] **Paso 6: pruebas reales** *(persona con el móvil de `TELEFONO_PRUEBA` + Claude)*

Llamada web a W1 aceptando el WhatsApp. Claude revisa los runs de W1 y W2.

| Caso | La persona escribe en WhatsApp | Esperado |
|---|---|---|
| 5.a | Reserva y nombre en un solo mensaje. | Una señal con los dos campos, email y matrícula vacíos; despedida fija. |
| 5.b | `er 1234 5678` y el nombre en minúsculas. | `numero_reserva` = `ER12345678`; nombre tal cual. |
| 5.c | Captura del correo de reserva. | El OCR saca el número; si hay dos, pregunta. |
| 5.d | Nota de voz con los datos. | Usa la transcripción. |
| 5.e | «¿Cuándo me devuelven la fianza?» | «Eso se lo cuento por teléfono.» Sin señal. |
| 5.f | Escribe otra vez después de enviar. | Respuesta fija; sin segunda señal. |

- [ ] **Paso 7: guardar y commit**

Guarda el prompt y la configuración (sin IDs de cuenta ni secretos) en
`casos/reembolsos/prompts/reembolsos-whatsapp-datos/v2/agente-whatsapp.md`.

```bash
git add casos/reembolsos/prompts/reembolsos-whatsapp-datos/
git commit -m "Reembolsos WhatsApp: agente de texto de WhatsApp en W2

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Tarea 6: extract de W1

**Ficheros:**
- Crear: `casos/reembolsos/prompts/reembolsos-whatsapp/v1/registrar-resultado.md`

- [ ] **Paso 1: leer la configuración actual**

`get_node_details` de «Registrar resultado de la llamada» en W1. La actualización es un reemplazo
total: parte de esa configuración.

- [ ] **Paso 2: cambiar el texto**

En el párrafo `FLUJO ESPERADO`, sustituye `lo identifica en tres turnos (número de reserva, nombre completo, fecha de nacimiento; nunca pide la matrícula)` por:
`lo identifica con número de reserva, nombre completo y fecha de nacimiento; puede ofrecer un WhatsApp para que el cliente escriba la reserva y el nombre (y, si quiere, email y matrícula), y esos datos llegan a la llamada como un mensaje <Signal Received>; la fecha de nacimiento siempre es por voz`.

Añade una regla 6 a `REGLAS OBLIGATORIAS`:
`6. Los mensajes que empiezan por <Signal Received> no los dice el cliente: son datos que llegan por WhatsApp. No cuentan como turnos del cliente ni como petición del agente. Que la plantilla de WhatsApp pida email o matrícula no cuenta como que el agente los pidió.`

En la descripción de `incumplio_restriccion` y de `pidio_matricula`, añade al final:
`Pedirlos en el WhatsApp no cuenta; solo cuenta si el agente de voz los pide hablando.`

- [ ] **Paso 3: añadir los campos nuevos**

Añade a `parameters`, con el mismo formato que los existentes:

| name | type | example | description |
|---|---|---|---|
| `whatsapp_ofrecido` | string | `si` | Valores EXACTOS: "si", "no". "si" si el agente ofreció mandar un WhatsApp. |
| `whatsapp_aceptado` | string | `si` | Valores EXACTOS: "si", "no", "no_aplica". "no_aplica" si no se ofreció. |
| `whatsapp_datos_recibidos` | string | `si` | Valores EXACTOS: "si", "no", "no_aplica". "si" si hay un <Signal Received> con "tipo": "datos_whatsapp". |
| `identificacion_via` | string | `whatsapp` | Valores EXACTOS: "whatsapp", "dictado", "ninguna". Por dónde llegaron la reserva y el nombre de la última consulta. |
| `email_whatsapp` | string | `ninguno` | El email del payload de datos_whatsapp, o "ninguno". |
| `matricula_whatsapp` | string | `ninguna` | La matrícula del payload de datos_whatsapp, o "ninguna". |

Cambia también la regla 5: `Los únicos identificadores permitidos son numero_cliente, numero_reserva_verificado, email_whatsapp y matricula_whatsapp.`

- [ ] **Paso 4: aplicar y probar**

`update_workflow_nodes action=update` con la configuración completa. `test_workflow action=test_node`
sobre el extract con la salida de un run de la Tarea 4 o 5. Esperado: los seis campos nuevos con
valores permitidos (`whatsapp_datos_recibidos` = `si` en un run con señal).

- [ ] **Paso 5: guardar y commit**

```bash
git add casos/reembolsos/prompts/reembolsos-whatsapp/v1/registrar-resultado.md
git commit -m "Reembolsos WhatsApp: extract con campos de WhatsApp y regla de señales

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Tarea 7: pruebas completas *(persona + Claude)*

Requiere la Tarea 5 terminada. Son los 12 casos del spec (apartado 7, fase 2), con llamadas web a
W1, `TELEFONO_PRUEBA` relleno y, cuando haga falta, una reserva de prueba que exista en el MCP
(pídela a la persona; no la escribas en el repo).

**Ficheros:**
- Crear: `casos/reembolsos/docs/informes/AAAA-MM-DD-pruebas-whatsapp.md`

- [ ] **Paso 1: ejecutar los 12 casos**

Por cada caso, la persona hace la llamada y Claude revisa los runs de W1 y W2 con `monitor_runs`:
`outputs` del agente (transcripción), del POST, de la señal y del extract. El veredicto sale de los
turnos `assistant` y de los `<Signal Received>`, no del extract.

- [ ] **Paso 2: escribir el informe**

Tabla con caso, run_id de W1, run_id de W2, resultado (OK / FALLO) y, si falla, el turno exacto.
Sin teléfonos, nombres ni reservas.

- [ ] **Paso 3: corregir y repetir**

Por cada fallo: corrige el prompt o el nodo, guarda el cambio en `prompts/`, repite solo ese caso y
actualiza el informe.

- [ ] **Paso 4: commit**

```bash
git add casos/reembolsos/docs/informes/ casos/reembolsos/prompts/
git commit -m "Reembolsos WhatsApp: informe de pruebas completas

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Tarea 8: documentación y PR

**Ficheros:**
- Modificar: `casos/reembolsos/docs/specs/2026-10-12-datos-por-whatsapp.md` (los tres ajustes de este plan)
- Modificar: `casos/reembolsos/docs/decisiones.md` (D-001)
- Modificar: `casos/reembolsos/docs/workflows.md`
- Modificar: `casos/reembolsos/docs/pendientes.md`
- Modificar: `casos/reembolsos/CLAUDE.md`
- Modificar: `CLAUDE.md` (tabla de casos)
- Modificar: `docs/extensiones.md`

- [ ] **Paso 1: spec**

Aplica los tres «Ajustes al spec» de este plan en los apartados 4.1 (parámetro `idioma` de
`enviar_whatsapp`; email y matrícula al extract), 2 (decisión 5) y 7 (fase 0 cubierta por el tótem y
por la Tarea 3, paso 8).

- [ ] **Paso 2: D-001**

```markdown
## D-001 · <fecha> · Datos por WhatsApp durante la llamada, con Signals
- **Qué:** workflows nuevos «Centauro Reembolsos WhatsApp» (voz, copia de la V4) y «Centauro
  Reembolsos · Datos por WhatsApp». El agente de voz ofrece un WhatsApp; el cliente escribe reserva,
  nombre, email y matrícula; los datos vuelven a la llamada con Send Signal a `session.<id>`. La
  fecha de nacimiento sigue siendo por voz.
- **Por qué:** el número de reserva y el nombre son lo que más falla al dictar. Signals evita Twin y
  las consultas periódicas; un tema por teléfono se descartó porque los temas personalizados no
  admiten variables.
- **Afecta a:** Reembolsos. La V4 no cambia.
- **Quién:** jzerpa.
- **Estado:** aplicada en versiones sin publicar; pendiente de publicar y de conectar a un número.
```

- [ ] **Paso 3: workflows, pendientes y CLAUDE.md**

- `workflows.md`: una sección por workflow nuevo con su `workflow_id`, slug, flujo (nodos por
  nombre) y tabla de versiones.
- `pendientes.md`: cuenta y plantillas de WhatsApp de Centauro; a qué número se conecta W1; cómo ve
  el agente humano el email y la matrícula; `ya_enviado` si no se pudo hacer en la Tarea 4 paso 4;
  vaciar `TELEFONO_PRUEBA` antes de publicar.
- `casos/reembolsos/CLAUDE.md`: tabla de workflows con los dos nuevos y, en reglas propias, que los
  turnos `<Signal Received>` no son del cliente al analizar llamadas.
- `CLAUDE.md` raíz: en la tabla de casos, Reembolsos pasa a «Centauro Reembolsos, Centauro
  Reembolsos WhatsApp y Datos por WhatsApp».
- `docs/extensiones.md`: W1 usa las mismas colas que Reembolsos V4.

- [ ] **Paso 4: comprobar que no hay datos personales**

```bash
git diff main --stat
git diff main | grep -nE '\+?[0-9]{9,}|@[a-z0-9-]+\.[a-z]{2,}|ER[0-9]{6,}' || echo "limpio"
```
Esperado: `limpio`, o solo coincidencias de ejemplo (`ER00000000`, `ER12345678`, números de prueba
de las pruebas unitarias).

- [ ] **Paso 5: commit y PR**

```bash
git add -A casos/reembolsos CLAUDE.md docs/extensiones.md
git commit -m "Reembolsos WhatsApp: documentación, decisión D-001 y pendientes

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
git push -u origin reembolsos/docs-whatsapp-spec
```
PR con: ticket, resumen del comportamiento y riesgos, impacto (dos workflows nuevos, la V4 sin
cambios), pruebas (informe de la Tarea 7) y la lista de lo que falta para publicar. Termina la
descripción con `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
