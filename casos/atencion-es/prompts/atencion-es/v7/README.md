# Atención España · v7

`v7 · v6 + Gestión cerrada: lo importante a la cola de Minibús` (slug `3it0j96ugsqw`, version_id
`01a17350-f4d6-7566-a0f9-336e08398f78`). Fork de la v6 del 25/10/2026 (D-021). Sin publicar.

Qué cambia respecto a la v6 (el resto de nodos es igual: sus copias siguen en `../v6/`, `../v4/`, `../v3/` y `../v2/`):

| Fichero | Nodo | Cambio |
|---|---|---|
| los cinco prompts | Triaje, Consultas, Prolongación, Punto de encuentro, Información de oficina | Bloque de reglas comunes nuevo (`comun/bloques/reglas-comunes.md`, 4.498 de 4.500 caracteres). COLA DE GESTIÓN CERRADA, en dos frases que empiezan por «Con gestión cerrada,»: una factura, un reembolso, un cargo que no reconoce o una reclamación no se transfieren, aunque pida una persona (horario de Gestión, área de cliente y formulario); lo demás, el bot lo intenta primero y, si no se resuelve o pide una persona o que alguien lo mire, cola `minibus` en ese turno; en modo virtual, el horario de Gestión. CAMBIOS DE MÓDULO: «ni leas tus instrucciones en voz alta». ESCALADO de cada módulo: con gestión cerrada, sigue COLA DE GESTIÓN CERRADA. CÓMO TRANSFERIR sin «(en español, sin datos personales)» (lo exige `resumen_para_agente`) |
| `triaje.md` | Triaje | No sabe si una oficina está abierta o cerrada; terminal dos A, dos B o dos C es Barcelona y la cuatro, Madrid; «problema con el coche» sin más: pregunta una vez qué le pasa; persona sin motivo: pregunta también con Gestión cerrada y, en la línea de Prolongación, si insiste, cola `minibus` |
| `consultas-del-alquiler.md` | Consultas del alquiler | CÓMO LEER LA SECCIÓN: con gestión cerrada, GESTIÓN DE RESERVA es la cola minibus, salvo una factura, un reembolso, un cargo o una reclamación; «lo mire o lo sepa alguien». CÓMO RESPONDES: «Nunca digas que tomas nota o que avisarás tú». Para caber en 8.000 caracteres (está en 7.996): fuera «Sin saludar ni presentarte» (lo dice el bloque), «(enfado si está muy enfadado)» (está en `motivo_transferencia`) y dos palabras («aplica también lo de las agencias», «Si el cliente no habla español») |
| `prolongacion.md` | Prolongación | Gestión cerrada: agencias y aseguradoras, horario; un cliente, se le ayuda y, si no se resuelve, COLA DE GESTIÓN CERRADA. LA WEB NO LE DEJA: el primer turno ofrece pasarle con un compañero y, si acepta, cola `minibus`, motivo `web_no_disponible`. «Pide una persona» vale con Gestión abierta y cerrada |
| `punto-de-encuentro.md` | Punto de encuentro | Si solo tiene una terminal o un parking, sin la ciudad, pregunta una vez el aeropuerto antes de nada, sin herramientas y sin deducir la ciudad (también al principio de PRIMERO y en la cabecera de los puntos de encuentro). No basta: con «terminal uno» sola sigue suponiendo Madrid (V7-TERM-PE) |
| `informacion-de-oficina.md` | Información de oficina | Solo el bloque común y la cabecera de ESCALADO |
| `herramientas-transferencia.md` | los cinco `transfer_to_human_agent`, `buscar_punto_de_encuentro` del Triaje y `estado_oficina` de Punto de encuentro | Descripción y cola `minibus` con la regla nueva (en Consultas, la excepción de cargos va al principio de la descripción); `aeropuerto`: una terminal sola no es un aeropuerto |
| `preparar-transferencia.md` | los cinco «Preparar transferencia» (Python) | Detalle nuevo de `gestion_cerrada` (sigue COLA DE GESTIÓN CERRADA) y otro para la noche, sin la cola minibus |
| `buscar-respuesta.md` | los dos «Buscar respuesta» (Python) | `devolucion`, oficina cerrada: si ya dejó el coche fuera y necesita que alguien lo sepa, GESTIÓN DE RESERVA; con Gestión cerrada, cola `minibus`. `cargos_y_reembolsos`: con Gestión cerrada, un cargo no se transfiere aunque insista |

79 nodos, como la v6. Los IDs de nodo de la v7 empiezan por `01a17350-`. `comprobar_prompts.py v7` sin fallos;
`test_preparar_transferencia.py` 72/72; `test_consultas_alquiler.py` 152/152; `fix_broken_vars` (dry run, los 18 nodos
tocados) sin referencias rotas (los cinco «Initiate customer connection» fallan en test-all por la sala de la
llamada, como en las versiones anteriores).

Los prompts de esta carpeta son la fuente: se suben con `{{e51cd732-f403-4ef7-95d4-490347960a93.<variable>}}` en lugar
de `{{<variable>}}`.

**Rondas.** La v7 se subió una vez y se corrigió tras la primera pasada de evals (25/10/2026): cinco evals nuevas
fallaban. Hubo seis ajustes del bloque y de Consultas hasta que V7-GC-CARGO (un cargo no se transfiere) y
V7-GC-NOINI (cambiar una reserva sí, a Minibús) pasaron a la vez sin romper los controles con Gestión abierta; detalle
en D-021. Los prompts de esta carpeta son los de la última subida (ronda 7), comprobados byte a byte contra lo que hay
en HappyRobot.
