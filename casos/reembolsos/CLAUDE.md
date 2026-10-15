# CLAUDE.md — Caso Reembolsos

Contexto propio del caso Reembolsos. Las reglas comunes (forma de trabajar, transferencias,
RingCentral, convenciones) están en el `CLAUDE.md` de la raíz.

> **Documentación parcial.** Está documentado el trabajo de «datos por WhatsApp». Falta describir
> con detalle el bot de la V4 (colas, herramientas, comportamiento esperado, falsos positivos del
> análisis). Toma el caso Minibús (`casos/minibus/`) como ejemplo.

## 1. Qué es

Voicebot de **reembolsos y fianzas** de Centauro Rent a Car. Identifica al cliente con número de
reserva (o, si no lo tiene, email o DNI/NIE desde la V5, D-003), nombre completo y fecha de nacimiento, consulta la reserva con `consultar_reembolso` y,
solo con la identidad verificada, informa del estado del reembolso y de los plazos; lo que exige
emitir, anular o decidir lo transfiere a una persona.

Hay una variante que ofrece al cliente escribir los datos difíciles de dictar por WhatsApp durante la
llamada (spec en `docs/specs/2026-10-12-datos-por-whatsapp.md`, decisión D-001).

| Workflow | workflow_id | slug | Producción / actual (15/10/2026) |
|---|---|---|---|
| Centauro Reembolsos (congelado, D-004) | `01a0defb-9c46-7f81-b966-69ca9d211709` | `ey9623r10ly2` | No se toca: el único bot de voz es W1. V5 (`gwe1rc4d1po6`) sin publicar |
| Centauro Reembolsos WhatsApp (W1, voz) | `01a12d4e-7c03-7494-8e0c-194e1256f8fb` | `j2cgq0sfra2q` | v4 (`n9k51iiu8ehw`, WhatsApp solo con dificultad) live desde el 15/10/2026; v5 (`ok9wpis1yhs3`, nombre sin inventar, email sin guiones y espera del WhatsApp, D-005) sin publicar; recibe la línea +34 911 200 3002 desde el 12/10/2026 |
| Centauro Reembolsos · Datos por WhatsApp (W2, texto) | `01a12d4c-5fe2-76d7-a233-3d5a16972ffd` | `p45rx5hlsber` | v8 (`fm6g5527v6lw`, email/DNI) live desde el 15/10/2026; envía desde +34 914 83 13 55 con la plantilla `datos_reserva`. v9 (`n1ij39vr42xd`, pide el nombre y no repite la pregunta, D-005) sin publicar |

- **Ficha de los workflows** (flujo y versiones): `docs/workflows.md`. Antes de publicar a clientes,
  sigue la checklist «Antes de publicar a clientes» de ese fichero.
- **Colas:** `../../docs/extensiones.md`. W1 usa las mismas colas que la V4.

## 2. Carpetas del caso

| Ruta | Qué contiene |
|---|---|
| `docs/decisiones.md` | Decisiones de Reembolsos (D-NNN) |
| `docs/workflows.md` | Ficha de los workflows y tablas de versiones |
| `docs/pendientes.md` | Incidencias abiertas y mejoras |
| `docs/specs/`, `docs/planes/` | Spec y plan de «datos por WhatsApp» |
| `docs/informes/` | Informes de pruebas |
| `pruebas/` | Evals de HappyRobot (`evals-whatsapp.md`, `evals-identificacion.md`) |
| `codigo/` | Lógica del teléfono (`telefono_whatsapp.py` y sus pruebas), que se pega en «Calcular idioma y saludo» |
| `prompts/reembolsos-v4/`, `reembolsos-v5/` | Prompt de la V4 y de la V5 (identificación por email o DNI/NIE) |
| `prompts/reembolsos-whatsapp/<versión>/` | Copias de W1 (v1 a v5) |
| `prompts/reembolsos-whatsapp-datos/<versión>/` | Copias de W2 |

## 3. Reglas propias del caso

- **Señales de WhatsApp.** En la transcripción de W1 los turnos `user` que empiezan por
  `<Signal Received>{…}</Signal Received>` **no son del cliente**: son los datos que llegan por
  WhatsApp (a veces pegados a lo que dice el cliente). Al analizar llamadas no cuentan como turnos
  del cliente ni como petición del agente.
- **Outputs de W2.** Los outputs del trigger de W2 guardan cabeceras (incluida la API key) y el
  teléfono del cliente. No copiarlos al repo.
- **Señal.** Se publica con un Webhook POST a la API de signals, no con el nodo Send Signal (que
  entrega el payload vacío). El nodo POST sale «succeeded» aunque la API devuelva un 4xx: mira la
  respuesta (`status == "published"`).
- **Plantilla mock.** W2 v4 usa la plantilla `info_minibus`; nunca publicar a clientes con el mock.
- **Plantilla real.** `datos_reserva` (`es` y `en`, mismo nombre). W2 v7 tiene una rama y un agente
  por idioma, cada uno con la plantilla estática y el idioma fijado **por la API** (D-002). No
  editar la plantilla desde el desplegable del editor (guarda la inglesa) ni usar el ID de Meta en
  modo dinámico (busca por nombre: `template_not_found`). `it` y `pt` reciben la inglesa. Los
  cambios de prompt, herramienta o POST van en las dos ramas.
- **Destino del WhatsApp.** Solo el número desde el que llama el cliente (o `TELEFONO_PRUEBA` en
  llamadas web), y solo si es un móvil. No añadir nunca un parámetro de teléfono a `enviar_whatsapp` ni
  enviar a un número dictado (D-004).
- **Pruebas web.** En llamadas web `from_number` es `web` y W1 usa la variable `TELEFONO_PRUEBA`.
- **Datos de prueba.** Reserva `ER00000000` o `ER12345678` y «Prueba Prueba». Nunca datos reales en
  el repo.
- **Ejemplo de «Verificado false».** El prompt de la V4 y de W1 en HappyRobot trae un nombre y una
  fecha reales de ejemplo; las copias del repo llevan uno inventado (ver pendientes).
- **El extract no es fiable** por sí solo (regla común): contrasta con los turnos `assistant` y las
  señales de la transcripción.
