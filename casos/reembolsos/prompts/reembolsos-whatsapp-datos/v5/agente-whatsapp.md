<!-- workflow: Centauro Reembolsos · Datos por WhatsApp · versión: v5 (0urzqrnn4yfr) · nodos: Elegir plantilla y Agente de WhatsApp · copiado: 2026-10-14 -->
# W2 · v5 · v4 + plantilla datos_reserva (es/en por ID)

Fork de la v4 (decisión D-002). Cambia solo:
1. Nodo nuevo **«Elegir plantilla»** (Python Sandbox) entre el trigger y el agente.
2. Plantilla inicial del agente en modo **dinámico**: el campo «Template ID or name» toma
   `plantilla_id` de «Elegir plantilla». Sin parámetros de plantilla (se quitan los de `info_minibus`).
3. Prompt: se quita la primera línea, que solo valía para la plantilla mock.

Flujo: trigger «Petición desde la llamada» → «Elegir plantilla» → «Agente de WhatsApp» → prompt →
herramienta `pasar_a_llamada` → POST «Señal a la llamada (API)». La herramienta y el POST no cambian
respecto a la v4 (ver `../v4/agente-whatsapp.md`).

**Resultado: no funciona.** Publicada por una persona en development y lanzada desde el editor (run
`5e1fac1f-b7f8-41f5-8773-67c5f7a98481`): «Elegir plantilla» dio bien el ID español, pero el agente
falló con `failed to fetch template from Meta API: whatsapp error 132001: template_not_found`. El
campo dinámico busca la plantilla por **nombre**, no por ID de Meta. Superada por la v7 (`../v7/`).

## Plantillas de Meta

`datos_reserva`, UTILITY, aprobadas en la cuenta de WhatsApp Business `970312032038916`. Mismo nombre
en los dos idiomas, sin variables ni botones. No hay `it` ni `pt`: esos idiomas reciben la inglesa.

| Idioma | ID de Meta |
|---|---|
| `es` | `1615023370215020` |
| `en` | `1468397315203244` |

En el editor, el desplegable de plantillas en modo estático identifica la plantilla solo por el
nombre: al elegir `datos_reserva` español guardó la inglesa (`language: "en"`). Por eso se usa el
modo dinámico con el ID.

**EN** (cabecera «Centauro Rent a Car»):
> Hello. This is Centauro Rent a Car. We are writing because you are on the phone with our assistant
> right now.
>
> So you don't have to spell them out, please reply to this message with:
> - Your booking number
> - The first name and surname of the main driver on the booking
>
> If you have them handy, please also add your email address and the car's licence plate. You can
> also send a screenshot of your booking confirmation email.

**ES**:
> Hola. Le escribimos desde Centauro Rent a Car porque está hablando ahora mismo por teléfono con
> nuestro asistente.
>
> Para no tener que dictarlos, responda a este mensaje con:
> - Su número de reserva
> - El nombre y apellidos completo del titular de la reserva
>
> Si los tiene a mano, añada también su email y la matrícula del coche. También puede enviar una
> captura del correo de confirmación de la reserva.

## Nodo «Elegir plantilla» (Python Sandbox)

Entrada `idioma` = variable `idioma` del trigger «Petición desde la llamada».

```python
# ===============================================================
# ELEGIR PLANTILLA - plantilla inicial de WhatsApp por idioma
# ---------------------------------------------------------------
# datos_reserva tiene el mismo nombre en todos los idiomas, asi que
# se elige por el ID de Meta de cada idioma.
# Solo hay es y en aprobadas: it, pt y cualquier otro idioma usan en.
# ===============================================================

PLANTILLAS = {
    "es": "1615023370215020",
    "en": "1468397315203244",
}
IDIOMA_POR_DEFECTO = "en"

idioma = str(input_data.get("idioma") or "").strip().lower()[:2]
idioma_plantilla = idioma if idioma in PLANTILLAS else IDIOMA_POR_DEFECTO

output = {
    "plantilla_id": PLANTILLAS[idioma_plantilla],
    "idioma_plantilla": idioma_plantilla,
}
```

Si Meta aprueba `it` o `pt`, se añade su ID a `PLANTILLAS` (versión nueva).

## Plantilla inicial del agente

`whatsappTemplateConfig.initialOutboundTemplate.config`:
- `inputMode`: `dynamic`
- `templateNameVariable`: `{{<Elegir plantilla>.plantilla_id}}`
- `parameters`: vacío; `templateId` y `templateName` vacíos.

El resto de la configuración del agente es igual que en la v4.

## Prompt (modelo gpt-5.4-mini, mensaje inicial vacío: abre la conversación la plantilla)

```
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
