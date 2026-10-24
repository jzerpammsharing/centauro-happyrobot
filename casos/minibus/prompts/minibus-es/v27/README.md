<!-- workflow: 019f7594-2cce-7eed-b995-dd9ea64a1062 · versión: v27 (e4qv98cib2dm) · WhatsApp como cierre normal y para el cliente que ya espera · 2026-10-24 -->

# v27 · v26 + WhatsApp como cierre normal y para el cliente que ya espera

Fork de la v26 (`fw02geuq54cv`, en producción). Decisión: D-013 (`../../../docs/decisiones.md`).
Análisis y evals: `../../../docs/informes/2026-10-24-v27-whatsapp.md`.

Lo que no está en esta carpeta es igual que en v26 (`../v26/`). El Python «Preparar WhatsApp
minibús», la plantilla de Meta y el nodo de rutas son los de v24 y v25 (`../v24/`, `../v25/`).

## Nodos que cambian

| Nodo | Cambio |
|---|---|
| Punto de encuentro (prompt) | Copia: `punto-de-encuentro.md`. Detalle debajo. |
| Registrar consultas del alquiler (AI Extract) | Párrafo WHATSAPP del prompt: el WhatsApp también se ofrece al cliente que ya espera. `punto_whatsapp`: es el punto al que se refieren las indicaciones (el que dio el agente o, si el cliente ya esperaba, aquel en el que espera), no solo «el punto cuya indicación dio el agente». Sin este cambio, al cliente que ya espera y acepta no le llegaría el WhatsApp, porque «Preparar WhatsApp minibús» no envía nada con `punto_whatsapp` = `ninguno`. Copia: `registrar-consultas-alquiler.md`. |

## Cambios en «Punto de encuentro»

- **Cierre:** en Madrid (T1, T2 y T4), Sevilla y Málaga, si se cumplen las condiciones, la pregunta
  del WhatsApp **sustituye** a «¿Puedo ayudarle en algo más?» (en v26 era una excepción entre
  paréntesis y el bot solía quedarse con el cierre por defecto). Nunca las dos en el mismo turno.
- **Nota interna** detrás de cada uno de esos cinco puntos de encuentro: si se cumplen las
  condiciones, ahí el cierre es la pregunta del WhatsApp.
- **INDICACIONES POR WHATSAPP:**
  - las condiciones van primero y se comprueban antes de ofrecerlo: WhatsApp disponible = true,
    conversación en español en ese momento (aunque la línea sea española, en inglés no se ofrece),
    punto de esos cinco y cliente sin queja ni transferencia;
  - si falla una, no se menciona el WhatsApp en toda la llamada;
  - se ofrece una sola vez, en el primero de dos momentos: al cerrar tras dar el punto (también si
    el cliente interrumpe la indicación) o cuando el cliente **ya espera** en el punto y pregunta
    cada cuánto pasa, sin quejarse;
  - al que ya espera se le dice la frecuencia y la referencia de su punto (lista de referencias de
    los cinco puntos) y se le ofrece el WhatsApp «con un enlace para ver el minibús en directo»;
    en Madrid hace falta la terminal.
- **«Si lleva MENOS que la frecuencia»** y la pregunta frecuente «¿Cada cuánto pasa?» recuerdan
  ofrecerlo en esos cinco puntos si se cumplen las condiciones.
- La variable `whatsapp_disponible` se presenta como «WhatsApp disponible para este número (true o
  false)».

Se sigue preguntando: no se envía nada sin el «sí» del cliente (opt-in de Meta).
