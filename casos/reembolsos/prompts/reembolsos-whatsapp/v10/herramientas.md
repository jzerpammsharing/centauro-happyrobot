<!-- workflow: Centauro Reembolsos Llamada + w · versión: v10 (2y93xxzzph11, 01a1607d-d367-7a80-9528-5eb548080d83), borrador · copiado: 2026-10-22 · base: v9 + búsqueda v2 del MCP (D-006) -->
# W1 v10 · Herramientas y nodos que cambian respecto a la v9

Solo lo que cambia. El resto de nodos (Inbound Call, Resolver colas por idioma, Receive Customer Call,
`enviar_whatsapp`, POST petición de datos, `transfer_to_human_agent`, Initiate customer connection y Registrar
resultado de la llamada) son los de la v9, sin tocar.

## «Calcular idioma y saludo» (Python, persistent_id `494e2f1a-e656-48a2-b08c-37fc660594e9`)

Código completo en `calcular-idioma-y-saludo.py` (esta carpeta). Lo nuevo:

- `telefono_para_consulta(numero_cliente, telefono_prueba)`. Devuelve el número en E.164 desde el que llama el
  cliente, o «» si no tiene al menos 9 cifras (extensión interna, oculto, `web`). En las llamadas web del editor
  (`from_number = web`) usa `TELEFONO_PRUEBA`. Así, quien prueba puede probar la búsqueda por teléfono con una reserva
  suya. En producción nunca hay llamadas web. La misma función está, con sus pruebas, en
  `codigo/telefono_whatsapp.py`.
- Salidas nuevas:
  - `telefono_consulta`: va al MCP como `telefono`;
  - `telefono_consultable`: lo lee el prompt como «Teléfono del cliente consultable».

## Herramienta `consultar_reembolso` (persistent_id `d78a66ae-4751-4f9d-97f7-b1b74b7e31e5`)

- Parámetros: siguen igual (`numero_reserva`, `email` y `dni` opcionales; `nombre_completo` y `fecha_nacimiento`
  obligatorios). **No lleva `telefono`:** el modelo nunca lo rellena.
- Descripción: explica el PRIMER INTENTO (solo con nombre y fecha, con los tres identificadores vacíos) y
  `otras_reservas`. El límite pasa a dos consultas, o tres si la primera fue sin identificador, y la falta de
  identificador del primer intento no cuenta.
- Ejemplos: los números de reserva de los ejemplos de las descripciones se sustituyen por otros inventados
  (`ER12345678`, `123456-654321`; pendiente de los «posibles números reales»).
- Los `example` de `numero_reserva`, `email` y `dni` se dejan vacíos para que el modelo no rellene con un ejemplo.
  Además, `test_node` toma de ahí los valores de prueba. Los de `nombre_completo` y `fecha_nacimiento` siguen como en
  la v9.
- `nombre_completo` y `fecha_nacimiento`: el texto de la v9, más «la fecha, solo la que el cliente dijo al
  preguntársela».

## MCP Call «Check Reimbursement Status» (persistent_id `0bd838d1-cf77-4ce1-8557-ca5551283e50`)

`tool_args` de la v9 (`numero_reserva`, `email`, `dni`, `nombre_completo` y `fecha_nacimiento`, todos desde la
herramienta), más:

| Clave | Valor |
|---|---|
| `telefono` | `{{494e2f1a-e656-48a2-b08c-37fc660594e9.telefono_consulta}}`: la variable del sistema, nunca la del modelo |

Credencial «Centauro MCP» (`01a0e1d8-9c92-7e58-8e25-caf109f1fadb`), sin cambios. **Sin confirmar que el teléfono llega
al MCP** (ver `docs/pendientes.md`, D-006).

## Python «Filtrar respuesta verificada» (persistent_id `c51fe669-1c44-4afb-b58a-15f4fef92f0b`)

Código completo y pruebas en `codigo/filtrar_respuesta_verificada.py` y `codigo/test_filtrar_respuesta_verificada.py`.
Lo nuevo:

- `CAMPOS_VERIFICADOS` añade `numero_reserva`, `tiene_cuenta` y `otras_reservas`. De cada reserva de
  `otras_reservas` solo pasan seis campos: `numero_reserva`, `estado`, `oficina_recogida`, `oficina_devolucion`,
  `fecha_recogida` y `fecha_devolucion`.
- Entradas nuevas: `email_solicitado` y `dni_solicitado`, de la herramienta.
- Salidas nuevas:
  - `consulta_por_telefono`: la consulta no llevaba número de reserva, email ni DNI;
  - `cuenta_en_limite`: false si el primer intento por teléfono vuelve con «falta el identificador».
- Las ramas de error de email, DNI y «falta», y la de búsqueda no disponible, ya estaban desde la v3 (D-003).
- El código está pasado a una función, `filtrar`, con el bloque `try: input_data … except NameError` al final, para
  poder probarlo en local.
