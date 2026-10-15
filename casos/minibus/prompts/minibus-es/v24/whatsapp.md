<!-- workflow: 019f7594-2cce-7eed-b995-dd9ea64a1062 · versión: v24 (5g6422lgdcem) · cambios de WhatsApp fuera del prompt de Punto de encuentro · 2026-10-15 -->

# WhatsApp del punto de encuentro (v24)

Fork de la v23. Solo se envía WhatsApp si el punto de encuentro es de un aeropuerto con seguimiento
en directo en buscentauro.com: **Madrid (T1, T2, T4), Sevilla y Málaga**.

## Nodos tocados o nuevos

| Nodo | Cambio |
|---|---|
| Calcular horario nocturno | Añade `whatsapp_disponible` (llamada en español y número móvil). El código está en el nodo; la parte nueva es el bloque final «WhatsApp (v24)». |
| Punto de encuentro (prompt) | Nueva sección INDICACIONES POR WHATSAPP: el agente ofrece el WhatsApp una vez, solo en MAD (T1, T2, T4), SVQ y AGP. Ver `punto-de-encuentro.md`. |
| Registrar consultas del alquiler (Extract) | Nuevos campos `whatsapp_ofrecido`, `whatsapp_aceptado`, `punto_whatsapp` (MAD-T1, MAD-T2, MAD-T4, SVQ, AGP, ninguno) e `idioma_cliente`. Nuevos datos técnicos: `whatsapp_disponible`, aeropuerto y terminal de `buscar_punto_de_encuentro`. |
| Preparar WhatsApp minibús (Python, nuevo) | Decide si se envía y prepara las variables. Código en `preparar-whatsapp-minibus.py`. |
| ¿Enviar WhatsApp? → Enviar (Paths, nuevo) | Envía solo si `enviar` es true. |
| Enviar WhatsApp del punto de encuentro (nuevo) | Plantilla `minibus_punto_texto_boton` (español), credencial «Whatsapp Centauro». |

## Regla de envío (`Preparar WhatsApp minibús`)

Se envía solo si, por este orden, el cliente aceptó, hay punto de encuentro, el aeropuerto está en
`TRACKING`, la llamada fue en español y el número es un móvil válido. Si no, `motivo_no_envio` toma
uno de estos valores: `no_aceptado`, `sin_punto`, `sin_geolocalizacion`, `idioma_no_es`,
`telefono_no_valido`.

## Plantilla `minibus_punto_texto_boton`

Variables nombradas: `aeropuerto`, `indicaciones`, `descripcion_minibus` y `frecuencia`. Botón «Ver
minibús en directo» con URL fija (sin parte variable). Valores fijos: `descripcion_minibus` =
«amarillo, con el logo de Centauro» y `frecuencia` = «15 o 20 minutos» para los tres aeropuertos.

## Dar de alta un aeropuerto nuevo con seguimiento

1. Añadir su IATA a `TRACKING` y sus puntos a `PUNTOS` en «Preparar WhatsApp minibús».
2. Añadir el código del punto a los valores permitidos de `punto_whatsapp` en el Extract.
3. Añadir el aeropuerto a la lista de la sección INDICACIONES POR WHATSAPP del prompt.
