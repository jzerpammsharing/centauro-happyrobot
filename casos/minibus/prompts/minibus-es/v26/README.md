<!-- workflow: 019f7594-2cce-7eed-b995-dd9ea64a1062 · versión: v26 (fw02geuq54cv) · servicio de espera y avisos de retraso a la cola de Minibús · 2026-10-24 -->

# v26 · v25 + servicio de espera y avisos de retraso a la cola de Minibús

Fork de la v25 (`k2in5n9kk01x`, en producción). Decisión: D-012 (`../../../docs/decisiones.md`).
Evals: `../../../docs/informes/2026-10-24-v26-evals.md`.

Lo que no está en esta carpeta es igual que en v25. Los prompts y el código están en `../v24/`, y lo
que v24 no tocó, en `../v23/` y `../v22/`.

## Nodos que cambian

| Nodo | Cambio |
|---|---|
| Prolongación y consultas (prompt) | RECOGER TARDE: si acepta comprobar el servicio de espera, transfiere a MINIBÚS (`motivo_transferencia` `minibus`), esté Gestión abierta o cerrada. Si solo quiere avisar a la oficina, le dice que no hace falta (la reserva se guarda doce horas), cierra con «¿Puedo ayudarle en algo más?» y no ofrece pasarle con nadie; solo si insiste, transfiere a MINIBÚS. COLA DE GESTIÓN CERRADA y REGLAS DE ESCALADO: el servicio de espera sale de la lista de Gestión y entra en la de Minibús. Copia: `prolongacion-y-consultas.md`. |
| Punto de encuentro (prompt) | COLA DE GESTIÓN CERRADA y REGLAS DE ESCALADO: el servicio de espera o el aviso de retraso pasan de Gestión a Minibús. Copia: `punto-de-encuentro.md`. |
| Información de oficina (prompt) | Igual que Punto de encuentro. Copia: `informacion-de-oficina.md`. |
| `transfer_to_human_agent` de esos tres prompts | En la descripción de `extension_destino`, el servicio de espera pasa de la lista de Gestión a la de Minibús. En la de Prolongación, además, `motivo_transferencia` (`minibus` incluye el retraso) y el punto 12 de la descripción. Copia: `herramientas.md`. |

«Triaje y horario» no cambia: ya manda los retrasos a `consultas_alquiler` (tema `recoger_tarde`).
El modo virtual tampoco cambia: con el centro de atención cerrado no se transfiere.
