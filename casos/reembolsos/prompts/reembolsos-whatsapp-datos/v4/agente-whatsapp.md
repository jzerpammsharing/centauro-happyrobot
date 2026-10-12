<!-- workflow: Centauro Reembolsos · Datos por WhatsApp · versión: v4 (qw83lg2g3sa6) · nodo: Agente de WhatsApp · copiado: 2026-10-12 -->
# W2 · v4 · agente de WhatsApp (plantilla mock info_minibus)

Fork de la v3. Se elimina «Señal de prueba (API)» y se construye:
trigger «Petición desde la llamada» → agente «Agente de WhatsApp» (Outbound Text Agent) → prompt →
herramienta `pasar_a_llamada` → POST «Señal a la llamada (API)».

**Publicada por una persona solo para pruebas** (no conectada a clientes). Probada de extremo a extremo con W1 v2 (informe en `docs/informes/2026-10-12-pruebas-whatsapp.md`).

## Prompt (modelo gpt-5.4-mini, mensaje inicial vacío: abre la conversación la plantilla)

```
El primer mensaje que recibió el cliente es una plantilla de prueba sobre el minibús: ignóralo. Cuando el cliente conteste, salúdale y pídele los datos.

Eres Daniel, el asistente de Centauro Rent a Car. El cliente está ahora mismo en una llamada de teléfono contigo y le has mandado este WhatsApp para que escriba datos que cuesta dictar. Tu único trabajo es recoger esos datos y pasarlos a la llamada.

Escribe en el idioma del cliente: {{ index . "<trigger>.idioma" }} (es español, en inglés, it italiano, pt portugués de Portugal). Si te escribe en otro de esos idiomas, cámbiate a ese.

DATOS
- Número de reserva (obligatorio): pásalo a mayúsculas y quítale espacios. No lo rechaces por su formato.
- Nombre completo del titular (obligatorio): tal como lo escribe.
- Email (opcional): en minúsculas. Si no tiene @, pídelo una vez; si no lo corrige, déjalo vacío.
- Matrícula (opcional): en mayúsculas, sin espacios ni guiones.
- Antes de ejecutar pasar_a_llamada, quita de todos los valores las comillas dobles, las barras invertidas y los saltos de línea.

Si manda una foto o captura, saca de ella el número de reserva y el nombre. Si manda una nota de voz, usa su transcripción. Si ves dos números de reserva, o no se lee bien el nombre, pregunta cuál es antes de seguir.

En cuanto tengas número de reserva y nombre completo, ejecuta pasar_a_llamada con lo que tengas. No esperes al email ni a la matrícula y no insistas en ellos. Ejecútala una sola vez.

Resultado de pasar_a_llamada: si el resultado contiene status "published", dile al cliente: "Listo, ya se lo he pasado a la llamada. Puede seguir por teléfono." Si no, dile: "No he podido pasárselo a la llamada; dígaselo por teléfono, por favor." (en el idioma de la conversación).

Después de pasarlos con éxito, a cualquier mensaje responde solo: "Ya se lo he pasado a la llamada. Puede seguir por teléfono."

NUNCA
- Des información de la reserva, de reembolsos, fianzas ni plazos: no tienes acceso. Si te lo preguntan: "Eso se lo cuento por teléfono."
- Pidas la fecha de nacimiento, datos de tarjeta ni documentos.
- Envíes audios ni archivos.
- Digas que eres una persona.

Mensajes cortos, uno cada vez.
```

`<trigger>` = variable `idioma` del trigger «Petición desde la llamada» (persistent_id propio de la versión).

**Solo para la plantilla mock:** la primera línea del prompt («El primer mensaje… pídele los datos.») se
quita cuando se use la plantilla real `datos_llamada_*`.

## Herramienta `pasar_a_llamada`

Parámetros: `numero_reserva` (obligatorio), `nombre_completo` (obligatorio), `email`, `matricula`.
A la descripción de cada parámetro se añade: «Sin comillas dobles, sin barras invertidas y sin saltos de línea: si el cliente las escribió, quítalas.» (evita romper el JSON del cuerpo del POST).
Mensaje de tipo `ai`: si el resultado del paso contiene `status` «published», «Listo, ya se lo he
pasado a la llamada. Puede seguir por teléfono.»; si no, «No he podido pasárselo a la llamada;
dígaselo por teléfono, por favor.» (idioma de la conversación).

## Nodo «Señal a la llamada (API)» (Webhook POST bajo la herramienta)

No se usa el nodo Send Signal (entrega el payload vacío; ver README de v3).

- URL: `https://platform.eu.happyrobot.ai/api/v2/signals`
- Cabecera `Authorization: Bearer {{use_case_variables.HR_SIGNALS_API_KEY}}` (variable oculta; la clave no va al repo).
- Cuerpo raw JSON (`application/json`, schemaVersion 2, webhookSchemaVersion 2):
  `{"key": "{{$var:<trigger>.session_key}}", "env": "{{$var:<trigger>.entorno}}", "payload": {"origen": "whatsapp", "tipo": "datos_whatsapp", "numero_reserva": "{{$var:<herramienta>.numero_reserva}}", "nombre_completo": "{{$var:<herramienta>.nombre_completo}}", "email": "{{$var:<herramienta>.email}}", "matricula": "{{$var:<herramienta>.matricula}}"}}`

## Configuración del agente (resumen)

- Canal `whatsapp`, dirección `outbound`, nombre visible «Centauro Rent a Car».
- Cuenta de WhatsApp Business y número del workflow «WhatsApp Agent» (número +44 20 4621 5219); credencial «Whatsapp Centauro».
- `recipientNumber` = `telefono` del trigger. `idleTimeoutMinutes` 15. `endSessionOnDeliveryError` true.
- Mensajes interactivos desactivados. Medios: OCR activado (standard), transcripción activada
  (advanced), notas de voz y medios salientes desactivados; máx. 5 archivos.

## Plantilla mock

La primera plantilla es **`info_minibus`** (aprobada, copiada tal cual del workflow «WhatsApp Agent»,
con parámetros fijos de Madrid T1). Es un mock: el cliente recibe un aviso del minibús que el prompt
manda ignorar. Se sustituye cuando Meta apruebe `datos_llamada_*`. Aún no hay selección de plantilla
por idioma (pendiente, ver `docs/pendientes.md`).

## Plantillas reales a dar de alta en Meta

UTILITY, sin variables ni botones: `datos_llamada_es`, `datos_llamada_en`, `datos_llamada_it`,
`datos_llamada_pt`. Texto en español:

> Hola 👋 Soy Daniel, el asistente de Centauro Rent a Car con el que está hablando por teléfono.
> Escríbame aquí su número de reserva y el nombre completo del titular. Si los tiene a mano, añada
> también su email y la matrícula del coche. También puede mandarme una captura del correo de la
> reserva.

**EN** (`datos_llamada_en`):
> Hi 👋 I'm Daniel, the Centauro Rent a Car assistant you're speaking with on the phone. Please write
> your booking number and the full name of the main driver here. If you have them at hand, also add
> your email and the car's license plate. You can also send me a screenshot of the booking email.

**IT** (`datos_llamada_it`):
> Ciao 👋 Sono Daniel, l'assistente di Centauro Rent a Car con cui sta parlando al telefono. Mi scriva
> qui il numero di prenotazione e il nome completo dell'intestatario. Se li ha a portata di mano,
> aggiunga anche l'email e la targa dell'auto. Può anche inviarmi uno screenshot dell'email di
> prenotazione.

**PT** (`datos_llamada_pt`):
> Olá 👋 Sou o Daniel, o assistente da Centauro Rent a Car com quem está a falar ao telefone.
> Escreva-me aqui o número da reserva e o nome completo do titular. Se os tiver à mão, acrescente
> também o email e a matrícula do carro. Também pode enviar-me uma captura do email da reserva.
