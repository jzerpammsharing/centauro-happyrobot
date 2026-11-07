<!-- workflow: Centauro Reembolsos · Datos por WhatsApp · versión: v7 (63eqtfk9nrdl) · nodos: Elegir plantilla, Idioma de la plantilla, Agente de WhatsApp (es) y (en) · copiado: 2026-10-14 -->
# W2 · v7 · v4 + plantilla datos_reserva (rama es / en)

Decisión D-002. Sustituye la plantilla mock `info_minibus` por la real `datos_reserva`, con una rama
por idioma. **Provisional:** cuando Meta apruebe `datos_reserva_es` y `datos_reserva_en` (nombres
distintos) se puede volver a un solo agente con plantilla dinámica por nombre.

**Sin publicar en producción.**

## Flujo

```
Petición desde la llamada (trigger)
└─ Elegir plantilla (Python Sandbox) → idioma_plantilla
   └─ Idioma de la plantilla (rutas)
      ├─ Español (idioma_plantilla == "es")
      │  └─ Agente de WhatsApp (es) → Prompt → pasar_a_llamada → Señal a la llamada (API) (es)
      └─ Fallback
         └─ Agente de WhatsApp (en) → Prompt → pasar_a_llamada → Señal a la llamada (API) (en)
```

Las dos ramas son iguales salvo la plantilla: misma configuración del agente que la v4 (credencial
«Whatsapp Centauro», número +34 914 83 13 55, inactividad 15 min, OCR y transcripción…), mismo
prompt, misma herramienta y mismo POST (cada POST apunta a la herramienta de su rama). **Un cambio
en el prompt, la herramienta o el POST hay que hacerlo en las dos ramas.**

Al analizar runs, el agente se llama ahora «Agente de WhatsApp (es)» o «(en)», y el POST «Señal a la
llamada (API) (es)» o «(en)».

## Por qué una rama por idioma

- `datos_reserva` tiene el mismo nombre en `es` y `en`. El desplegable del editor solo distingue por
  nombre: al elegir la española guardó la inglesa (`language: "en"`).
- Modo dinámico (v5): el campo «Template ID or name» busca por **nombre**. Con el ID de Meta
  (`1615023370215020`) el agente falla con `whatsapp error 132001: template_not_found` (run
  `5e1fac1f-b7f8-41f5-8773-67c5f7a98481`).
- Modo estático con `templateMetadata.language = "es"` fijado por la API (v6): HappyRobot envía la
  española (run `b4dc7352-0070-4fef-a3fb-3162b80756fd`, comprobado en el móvil del equipo).

**No editar la plantilla desde el desplegable del editor:** volvería a guardar la inglesa en la rama
española. Si hay que tocarla, por la API (`update_workflow_nodes`) con la configuración de abajo.

## Plantillas de Meta

`datos_reserva`, UTILITY, cuenta de WhatsApp Business `970312032038916`, sin variables ni botones.
No hay `it` ni `pt`: esos idiomas van por la rama inglesa.

| Idioma | ID de Meta (no lo usa HappyRobot) |
|---|---|
| `es` | `1615023370215020` |
| `en` | `1468397315203244` |

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

## Plantilla inicial de cada agente

`whatsappTemplateConfig.initialOutboundTemplate.config`:
- `inputMode`: `static`; `parameters`: vacío; `templateId` y `templateName`: `datos_reserva`.
- `templateMetadata`: `status` APPROVED, `category` UTILITY, `language` `es` o `en`, y `components`
  con el texto de arriba (en `en`, además el HEADER de texto «Centauro Rent a Car»).

## Nodo «Elegir plantilla» (Python Sandbox)

Entrada `idioma` = variable `idioma` del trigger «Petición desde la llamada».

```python
# ===============================================================
# ELEGIR PLANTILLA - idioma de la plantilla inicial de WhatsApp
# ---------------------------------------------------------------
# datos_reserva solo esta aprobada en es y en: it, pt y cualquier
# otro idioma reciben la inglesa. El nodo de rutas «Idioma de la
# plantilla» manda es al agente con la plantilla espanola y el resto
# al de la inglesa.
# ===============================================================

IDIOMAS_CON_PLANTILLA = ("es", "en")
IDIOMA_POR_DEFECTO = "en"

idioma = str(input_data.get("idioma") or "").strip().lower()[:2]

output = {
    "idioma_plantilla": idioma if idioma in IDIOMAS_CON_PLANTILLA else IDIOMA_POR_DEFECTO,
}
```

## Nodo de rutas «Idioma de la plantilla»

- «Español»: `idioma_plantilla` (de «Elegir plantilla») `text_equals` `es`.
- «Fallback»: todo lo demás (en la práctica `en`).

## Prompt (igual en las dos ramas; modelo gpt-5.4-mini, mensaje inicial vacío)

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

Respecto a la v4 se quita la primera línea («El primer mensaje que recibió el cliente es una
plantilla de prueba sobre el minibús…»), que solo valía para la plantilla mock.

## Herramienta `pasar_a_llamada` y POST «Señal a la llamada (API)»

Iguales que en la v4 (`../v4/agente-whatsapp.md`), una copia por rama. El cuerpo de cada POST usa
las variables de la herramienta de su rama.
