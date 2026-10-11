# Colas y extensiones de RingCentral

Todas las patas salientes de los bots salen de la extensión **19236** (id interno `4027457064`).
`to.extensionNumber` y `to.name` del registro de llamadas dan el destino real.

## Colas de Minibús
| Ext. | Nombre en RingCentral | Uso |
|---|---|---|
| 18056 | 00. CC ES-ES- Hor.MiniBus | Minibús España, español |
| 18059 | 00. CC ES-EN-Hor.MiniBus | Minibús España, inglés |
| 18069 | 00. CC IT-IT-Hor.MiniBus | Minibús Italia, italiano |
| 18073 | 00. CC IT-EN-Hor.MiniBus | Minibús Italia, inglés |
| 18063 | 00. CC PT-PT-Hor.MiniBus | Minibús Portugal, portugués |
| 18066 | 00. CC PT-EN-Hor.MiniBus | Minibús Portugal, inglés |

## Otras colas a las que transfieren los bots de Minibús

En el informe solo cuentan las patas que casan con un intento de transferencia de Minibús; el
resto son del bot de Prolongaciones.

| Ext. | Nombre | Nota |
|---|---|---|
| 18057 | 00. CC ES-ES -Hor.Gestión | Compartida con el bot de Prolongaciones |
| 18061 | 00. CC ES-EN-Hor. Manage Reservation | Compartida con el bot de Prolongaciones |
| 18001 / 18006 | Nueva Reserva ES-ES / ES-EN | Compartidas con el bot de Prolongaciones |
| 18034 | 00. RA ES-ES AVERÍAS | Cola de agentes de averías (ES); compartida con el bot de Prolongaciones |
| 18071 / 18074 | IT Mod. Reserva IT-IT / IT-EN | |
| 18024 / 19042 | IT Nuova Prenotazione IT-IT / IT-EN | |
| 18064 / 18067 | PT Alteração PT-PT / PT Management EN | |

## ⚠️ Destinos prohibidos (menús automáticos, no agentes)
| Ext. | Nombre | Visto |
|---|---|---|
| 2114 | Menú de asistencia en carretera (ES) | 09/10 |
| 2115 | Menú de asistencia en carretera (EN) | 09/10 y 10/10 (ES v19) |
| 2119 | RA IT-EN-OPCIONES | 10/10 (IT v2) |
