<!-- workflow: 01a0d9de-b1cd-7bc9-bafc-f5117bd57249 · versión: v12 · V11 + envío del correo de contraseña (fase 1) (mnhi8x9j8ce7) · nodo: enviar_correo_contrasena · copiado: 2026-10-17 -->

Herramienta (tool) nueva en la v12, hija del prompt «Prolongacion». Persistent ID
`01a14967-92fa-78e2-b3ef-a2f1d8ec570b`. Es una tool normal (no MCP directa): sus cuatro nodos hijos van
en cadena y el agente solo ve la salida del último.

| # | Nodo | Tipo | Persistent ID | Qué hace |
|---|---|---|---|---|
| 1 | Comprobar correo (consultar_reserva) | MCP Call, credencial «Centauro MCP» (`01a0e1d8-9c92-7e58-8e25-caf109f1fadb`) | `01a14967-9302-788f-974c-9e48f2817298` | `consultar_reserva` con `email`, `nombre_completo` y `fecha_nacimiento` de la tool. Busca por el email que dictó el cliente. |
| 2 | Decidir envío | Python Sandbox | `01a1496e-6988-7395-be53-09c5dca06973` | Código: `../../../codigo/decidir_envio.py`. `coincide` = encontrada y verificada. Solo entonces `email_envio` lleva el email; si no, va vacío. |
| 3 | Enviar correo (enviar_reset_contrasena) | MCP Call, «Centauro MCP» | `01a1496e-699c-7bd0-af43-cba069b66bf8` | `enviar_reset_contrasena` con `email` = `{{01a1496e-6988-7395-be53-09c5dca06973.email_envio}}`. Con el email vacío HappyRobot no manda el argumento y el MCP lo rechaza («email Field required»): **no sale ningún correo si no coincide**. |
| 4 | Resultado para el agente | Python Sandbox | `01a1496e-69ad-7004-b3b8-8c6ef64afc58` | Código: `../../../codigo/resultado_envio.py`. Devuelve `resultado` (enviado / no_coincide / dato_no_interpretado / no_disponible), `enviado` y `detalle`. Nunca el correo ni datos de la reserva. |

Entradas de los nodos Python:
- «Decidir envío»: `email` = `{{01a14967-92fa-78e2-b3ef-a2f1d8ec570b.email}}`, `result` e `is_error` del nodo 1.
- «Resultado para el agente»: `estado` y `detalle` del nodo 2; `reset_result` y `reset_is_error` del nodo 3.

Contrato del MCP comprobado el 17/10/2026 (validación de pydantic, sin enviar nada) y en el código del servidor (`jzerpammsharing/centauro-mcp`):
- `consultar_reserva`: obligatorios `nombre_completo` y `fecha_nacimiento`; acepta `email` como
  identificador. Con datos de prueba que no existen devuelve `{"encontrada": false, "verificado": false, "motivo_no_verificado": null}`.
- `enviar_reset_contrasena`: único obligatorio `email`. Un `numero_reserva` no lo sustituye.
- Las llamadas desde HappyRobot, también en *development*, llegan a Railway *production* con la API real de Centauro.
- `consultar_reserva` verificada devuelve `email_hint` (solo el dominio); ningún endpoint devuelve el correo completo.

## Descripción de la herramienta

Comprueba que el correo que te ha dicho el cliente coincide con el de su alquiler (busca por ese correo con el nombre completo y la fecha de nacimiento del titular) y, SOLO si coincide, le envía el correo para crear o restablecer la contraseña de su área de cliente. Si no coincide, no se envía nada. Ejecútala solo cuando el cliente haya aceptado el envío y tengas los tres datos dichos por él: el correo que dio en la oficina al recoger el coche (ya repetido y confirmado por el cliente), su nombre completo y su fecha de nacimiento. Nunca la ejecutes con un dato a medio dictar ni con datos que no haya dicho el cliente. MÁXIMO DOS LLAMADAS POR CONVERSACIÓN. Devuelve resultado: enviado (correo enviado), no_coincide (no se ha enviado nada), dato_no_interpretado (pide que repita el dato que indica detalle) o no_disponible (no se ha podido enviar ahora). Nunca devuelve el correo que consta ni ningún dato de la reserva.

## Mensaje al cliente (tipo `ai`)

**Descripción:** Una sola frase corta, en el idioma en que se está desarrollando la llamada, diciendo que lo compruebas. Ejemplos: español "Un momento, lo compruebo."; inglés "One moment, let me check."; portugués "Um momento, vou verificar."; italiano "Un attimo, controllo."

**Ejemplo:** Un momento, lo compruebo.

## Parámetros (los tres obligatorios)

### email

Correo que el cliente dio en la oficina al recoger el coche, escrito con letras y símbolos: 'laura punto gomez arroba gmail punto com' -> 'laura.gomez@gmail.com'. Pon guion, punto o guion bajo solo si el cliente los dijo; la transcripción a veces mete guiones que no dijo ('L-Gomez' cuando dijo 'ele gomez' -> 'lgomez'). Si el cliente lo deletreó o lo corrigió, usa su versión. Nunca lo inventes ni lo completes.

Ejemplo: `prueba.prueba@example.com`

### nombre_completo

Nombre y apellidos del titular del alquiler, tal como los dice el cliente. Si corrigió o deletreó algún apellido, usa la versión corregida. Nunca lo inventes ni lo saques del correo: si el cliente no te lo ha dicho, pídeselo antes.

Ejemplo: `Prueba Prueba`

### fecha_nacimiento

Fecha de nacimiento del titular SIEMPRE en formato DD/MM/AAAA, sea cual sea el idioma en que la diga el cliente. Convierte tú la fecha dicha: 'cinco de abril del noventa y siete' -> 05/04/1997; 'três de março de mil novecentos e oitenta' -> 03/03/1980; 'ventiquattro dicembre novantacinque' -> 24/12/1995.

Ejemplo: `01/01/1990`
