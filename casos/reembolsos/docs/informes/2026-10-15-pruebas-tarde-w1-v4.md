# Pruebas por voz de W1 v4 · 15/10/2026 (tarde)

Cuatro llamadas de prueba a la línea de W1 («Centauro Reembolsos Llamada + w», v4 `n9k51iiu8ehw`, ya
publicada) entre las 16:06 y las 16:57 (hora de Madrid), con su WhatsApp en W2 v8 (`fm6g5527v6lw`).
Misma persona de prueba en las cuatro, sin número de reserva a mano (email o NIE). Datos personales
omitidos: solo se citan run_id y el comportamiento del bot.

| # | Run W1 | Run W2 | Identificador | Final |
|---|---|---|---|---|
| 1 | `bb8f0252-6c31-4540-94d9-1bf0d3ab2086` | `9aa5c161-c167-4de2-b8a4-f78d50023a0b` | Email | Transferencia `reserva_no_encontrada` |
| 2 | `0480816e-35ac-4aed-9aa3-c464c35543bf` | `56a93701-858f-4c4d-b134-bab7174b3df8` | Email | Transferencia `no_identificado` |
| 3 | `72107c25-3fcd-4d27-a6b2-802d7d2257a8` | `5d5410b3-4d26-4272-90e4-a064281b86b8` | NIE y número | Transferencia `reserva_no_encontrada` (el cliente no quería) |
| 4 | `caab162e-a1dc-43b7-9176-05c45185791c` | `df471ff7-8d79-4a3c-a15a-58e243a3abeb` | Email | Transferencia `dificultad_agente` |

## Lo que se vio (y la causa)

1. **Se inventa el nombre** (llamada 2). El cliente dijo «Incorrecto» en el turno en que Daniel
   repetía el email y pedía el nombre; el nombre nunca se dijo. Al decir el cliente «ya te lo he
   enviado por WhatsApp», Daniel contestó «Me ha llegado, gracias» **sin que hubiera llegado nada**
   (la señal llegó 20 s después) y consultó con un nombre sacado del email. Causa: el prompt no
   prohibía deducir el nombre ni decía qué hacer si el cliente afirma haber escrito y no hay señal.
   Lo mismo pasó en las llamadas 1 y 4: «Me ha llegado» sin señal (en la 1 W2 nunca llegó a pasar los
   datos).
2. **W2 no pide el nombre** (llamadas 1, 2 y 4). Con solo el email escrito, el agente de WhatsApp
   respondía «¿Tiene el número de reserva? Si no, dígame el email…» (la única frase literal del
   prompt), aunque ya tenía el email, y la repetía tal cual. En la 2 acabó pasando a la llamada el
   trozo del email antes de la @ como nombre; en la 1 no pasó nada. Además, en la 3 puso el número
   de reserva también en `dni`.
3. **Guion en el email** (llamada 1). La transcripción escribió «C-…» por la letra dictada y Daniel
   deletreó «ce, guion, efe…» y consultó con el guion. En la 4 leyó el apellido en bloque en vez de
   deletrearlo.
4. **No insiste con el WhatsApp / repite la espera** (llamadas 1 a 4). A los 6-7 s de decir «Se lo
   acabo de enviar», sin que el cliente hablara, Daniel ofrecía seguir por voz («Si lo prefiere,
   seguimos por aquí», «¿Me dicta el email despacio?») o decía «Aquí sigo»; en la 4, cuatro mensajes de
   espera. HappyRobot le da turno al agente cuando hay silencio y el prompt («pasan dos turnos suyos
   sin que lleguen») no frenaba esos turnos.
5. **Límite de dos consultas** (llamada 3). La primera consulta (NIE) encontró otra reserva y la
   segunda (número mal transcrito) no apareció; el WhatsApp llegó con el número bien escrito, pero
   Daniel ya no podía consultar y transfirió. Es el pendiente del «máximo de dos consultas».
6. **Pide escribir otra vez en el WhatsApp** (llamada 4). Tras «no encontrada» con datos de WhatsApp,
   Daniel pidió escribir el NIE «ahí»; W2 ya había pasado los datos y no pasa más, así que no llegó
   nada, y volvió a pedir la fecha de nacimiento que ya tenía.

Observaciones sin cambio en esta versión:
- En las llamadas 1 y 3 el cliente ofreció el DNI/NIE y Daniel insistió en el email (orden de D-003).
  El email por voz falló en las tres llamadas en que se dictó; el DNI/NIE se entendió a la primera.
- En la llamada 3 Daniel aceptó un número de reserva con nueve cifras tras ER sin preguntar.
- La voz del agente («más despacio»): la v4 no fija `voice_speed`; se puede bajar por voz en el editor
  (0,7-1,2). No se cambia sin decisión.

## Cambios (D-005)

- **W1 v5** (`ok9wpis1yhs3`): prompt y herramienta `consultar_reembolso`. Copia en
  `prompts/reembolsos-whatsapp/v5/`.
- **W2 v9** (`n1ij39vr42xd`): prompt y `pasar_a_llamada` en las dos ramas. Copia en
  `prompts/reembolsos-whatsapp-datos/v9/`.

Resultados de los evals en `pruebas/evals-whatsapp.md` (ronda D-005).
