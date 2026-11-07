# Spec · Prolongaciones: Daniel envía el correo de contraseña (fase 1)

Fecha: 17/10/2026 · Versión: v12 (`mnhi8x9j8ce7`), fork de la V11 · Decisión: D-008 · Estado: construida, sin publicar.

## Objetivo

Que el cliente que no tiene o no recuerda la contraseña de centauro.net pueda recibir, durante la
llamada, el correo para crearla, y así prolongar él mismo desde su área de cliente sin pasar a un agente.

Fuente del guion: análisis de 705 llamadas de la cola de Gestión (18057), del 1 al 25/09/2026, en las que
los agentes enviaron este correo en 21 de 66 prolongaciones. El análisis está fuera del repo (contiene
horas de llamadas y nombres de agentes); de él se toman las frases y los imprevistos.

## Alcance

Entra:
- Ofrecer el envío cuando el cliente necesita entrar en su cuenta (no tiene, no recuerda la contraseña,
  reservó por mutua, agencia o Booking). Si recuerda la contraseña, no se envía nada.
- Pedir el correo que dio en la oficina, repetirlo deletreando lo de antes de la arroba, y pedir nombre
  completo y fecha de nacimiento, en turnos separados.
- Comprobar que el correo coincide con el de su alquiler y, solo entonces, enviar el correo con la API
  actual.
- Si no coincide: no se envía nada, se le dice que no coincide y se le pasa con un agente.
- Esperar a que confirme que le ha llegado y seguir con los pasos de prolongación de la V11.
- Plan B (instrucciones de la web de la V11) si no quiere el envío o la herramienta falla.

Queda fuera (fase 2 o siguientes):
- Leer datos del alquiler (hora de devolución, oficina, estado): se mantiene «No confirmes cuál es su
  hora de devolución». Pedido por el negocio para una fase posterior.
- Identificar por número de reserva, DNI o matrícula.
- Añadir o cambiar el correo de una reserva (transferencia).
- SMS o WhatsApp.

## Contrato del MCP «Centauro MCP» (credencial `01a0e1d8-9c92-7e58-8e25-caf109f1fadb`)

Comprobado el 17/10/2026 con llamadas que fallan en la validación (no envían nada) y leyendo el código
del servidor (repo `jzerpammsharing/centauro-mcp`, desplegado en Railway, proyecto `centauro-mcp`):
- **Dónde va la credencial:** aunque se llama «Centauro MCP Credential Stagin», las llamadas desde
  HappyRobot (también las de prueba en *development*) llegan al entorno **production** de Railway, que
  usa la API real de Centauro (`DATA_PROVIDER=centauro_bot`, `bot-api.centauro.net`). Visto en los logs
  de Railway del 17/10. No hay entorno de pruebas: cualquier envío desde HappyRobot es real.
- `consultar_reserva(numero_reserva | email | dni, nombre_completo, fecha_nacimiento)`: si no verifica,
  solo `encontrada`, `verificado` y `motivo_no_verificado`. Si verifica: `estado`,
  `fecha_hora_recogida`, `fecha_hora_devolucion`, `oficina_recogida`, `oficina_devolucion`,
  `duracion_dias`, `canal` y `email_hint`, que es **solo el dominio** del correo (p. ej. `gmail.com`).
  Con email devuelve la reserva más reciente ya iniciada de ese cliente (D-003 de Reembolsos).
- **Ningún endpoint devuelve el correo completo.** La API de Centauro (`POST /api/v1/Booking/Search`)
  devuelve del titular solo nombre, apellidos y `email_dominio`; es lo pactado en el contrato
  («nunca devuelve la fecha ni el email completo»). `Contract/Refund`, `BookingLine` y `PaymentLine`
  no tienen correo. Si la API enviara más campos, el MCP los descartaría (`extra="ignore"`).
- **No hay verificador de email.** La verificación es la fecha de nacimiento (la compara Centauro) y
  el nombre (lo compara el MCP, con tolerancia). El email solo es clave de búsqueda, con prioridad
  número > email > DNI: si llegan número y email, el MCP descarta el email. Por eso la v12 comprueba
  el correo buscando por él.
- `enviar_reset_contrasena(email)`: único parámetro obligatorio. Llama a
  `POST /api/v1/Customer/ResetPassword` (el README del MCP aún lo llama «stub», pero ya está
  implementado). Responde `{"ok": true}` exista o no la cuenta. Errores: email no interpretado,
  `timeout`, `servicio_no_disponible`.

## Diseño

### Herramienta `enviar_correo_contrasena`

Una sola herramienta para el agente, con cuatro nodos en cadena:

1. **Comprobar correo (`consultar_reserva`)** con el email dictado, el nombre y la fecha.
2. **Decidir envío** (Python, `codigo/decidir_envio.py`): `coincide` = encontrada y verificada.
   `email_envio` = el email si coincide; vacío si no.
3. **Enviar correo (`enviar_reset_contrasena`)** con `email_envio`. Vacío → HappyRobot omite el
   argumento → el MCP rechaza la llamada. El «no se envía» no depende del modelo.
4. **Resultado para el agente** (Python, `codigo/resultado_envio.py`): `resultado` = enviado /
   no_coincide / dato_no_interpretado / no_disponible, `enviado` y `detalle`. El agente nunca ve el
   correo de la ficha ni datos de la reserva.

Se descartó usar un nodo de ramas dentro de la herramienta porque la documentación de HappyRobot no
aclara qué salida recibe el agente cuando hay ramas.

### Conversación

| Paso | Daniel |
|---|---|
| Oferta | «No se preocupe: su cuenta ya existe con el correo que dio al recoger el coche, aunque reservara por la mutua o por una agencia. Si quiere, le envío ahora un correo para que cree su contraseña. ¿Se lo envío?» |
| Correo | «¿Me dice el correo que dio en la oficina al recoger el coche?» → lo repite deletreando y pregunta si es correcto |
| Nombre y fecha | Un turno cada uno |
| Enviado | «Ya se lo he enviado. Le llegará un correo de Centauro que dice "restablecer contraseña"; aunque nunca haya tenido una, sirve para crearla. ¿Le ha llegado?» |
| Le ha llegado | «Pulse el enlace del correo y escriba la contraseña que usted quiera…» → «¿Seguimos con los pasos para prolongar?» |
| No coincide | «Con esos datos no me coincide, así que no puedo enviárselo. Le paso con un compañero…» → Gestión, `correo_no_coincide`. Con Gestión cerrada: sin transferir, plan B y horario |
| No disponible | «Ahora mismo no puedo enviárselo.» → plan B |

Imprevistos (del análisis): «¿cuál es la contraseña?», no le llega (esperar, spam y promociones, un
reenvío y, si sigue sin llegar, transferencia con `error_tecnico`), el enlace falla, no puede abrir ese
correo (solo al de su alquiler; prolongar en oficina), llama otra persona (al correo del titular), pide
SMS, ofrece el número de reserva (no hace falta).

Límites: como mucho dos ejecuciones de la herramienta por llamada; nunca dice el correo de la reserva
ni si un correo está dado de alta; nunca pide reserva, matrícula ni DNI.

### Extract

Campos nuevos: `correo_contrasena_ofrecido`, `correo_contrasena_resultado`, `envios_correo`,
`correo_recibido_confirmado`, `motivo_no_envio`. Se mantienen todos los de la V11.

## Riesgos y preguntas abiertas

- **¿Qué correo compara `consultar_reserva`?** Se asume que el correo de la reserva es el mismo con el
  que se creó la cuenta del área de cliente (el de la oficina). Si en reservas de Booking o mutua la
  ficha guarda otro correo, saldrá «no coincide» aunque el cliente dé el correo correcto de su cuenta.
- **Reservas que no han empezado:** con email, la consulta solo devuelve reservas ya iniciadas; un
  cliente con una reserva futura saldrá «no coincide».
- **Sin entorno de pruebas:** la credencial va a la API real, así que el caso «coincide» solo se puede
  probar con una reserva real y enviará un correo de verdad.
- **Pista del dominio (posible mejora):** con la identidad verificada por número de reserva o DNI,
  `email_hint` permitiría decir «el correo de su reserva es de gmail» para ayudar a recordar cuál dio
  en la oficina. No está en la v12.
- **Caso «coincide» sin probar de punta a punta:** necesita una reserva real y un correo accesible.
- **Tiempo:** el envío añade unos cuatro turnos; la llamada tiene un límite de unos 600 s.

## Fase 2 (esbozo, sin diseñar)

Leer datos del alquiler con la identidad verificada (por ejemplo, oficina y fecha y hora de devolución)
para responder sin transferir las preguntas de `pregunta_reserva_concreta`. Falta el contrato de lo que
devuelve `consultar_reserva` con una reserva verificada y decidir qué datos puede decir Daniel.
