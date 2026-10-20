<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v1 (veavliy3k6jx) · nodo: Inbound Call · copiado: 2026-10-18 -->

# Inbound Call

- Tipo: Inbound to number (Phone calls), nodo raíz
- Persistent ID: `33c2681a-9160-413c-8010-e455bd4023c6`

## Configuración

Sin configuración (`_No configuration set_`). **El duplicado no copia las líneas telefónicas de Minibús ES**: el
trigger se queda sin números, que es lo que se quiere hasta pasar a producción (las líneas y la tabla línea →
opción se ponen entonces; ver `docs/pendientes.md`). Tampoco copia `require_webcall_auth: false`: por defecto
es `true`, así que una llamada por web necesita autenticación hasta que se cambie.

Los parámetros de salida que usan los nodos siguientes son `from_number` y `to_number`.
