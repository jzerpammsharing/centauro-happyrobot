# Colas y extensiones de RingCentral

Todas las patas salientes de los bots salen de la extensión **19236** (id interno `4027457064`).
`to.extensionNumber` y `to.name` del registro de llamadas dan el destino real.

> **Colas compartidas:** una pata hacia una cola compartida puede ser de cualquiera de los bots que la
> usan. Cada informe cuenta solo las patas que casan con un intento de transferencia de su bot (misma
> extensión e inicio cercano).

## Colas de Minibús
| Ext. | Nombre en RingCentral | Uso | También la usa |
|---|---|---|---|
| 18056 | 00. CC ES-ES- Hor.MiniBus | Minibús España, español | **Prolongaciones** (minibús o idioma no atendido, ES); Atención España (v2, sin publicar) |
| 18059 | 00. CC ES-EN-Hor.MiniBus | Minibús España, inglés | **Prolongaciones** (minibús o idioma no atendido, EN); Atención España (v2, sin publicar) |
| 18069 | 00. CC IT-IT-Hor.MiniBus | Minibús Italia, italiano | |
| 18073 | 00. CC IT-EN-Hor.MiniBus | Minibús Italia, inglés | |
| 18063 | 00. CC PT-PT-Hor.MiniBus | Minibús Portugal, portugués | |
| 18066 | 00. CC PT-EN-Hor.MiniBus | Minibús Portugal, inglés | |

## Colas de Prolongaciones

Bloque `COLAS` del nodo «Resolver colas por idioma» (V11). El bot elige la columna por la línea
marcada (español o inglés).

| Ext. | Nombre en RingCentral | Uso en Prolongaciones | Compartida con |
|---|---|---|---|
| 18057 | 00. CC ES-ES -Hor.Gestión | Gestión de reserva, español (cola por defecto) | Minibús ES (v19 y siguientes); Atención España (v2, sin publicar) |
| 18061 | 00. CC ES-EN-Hor. Manage Reservation | Gestión de reserva, inglés | Minibús ES (v19 y siguientes); Atención España (v2, sin publicar) |
| 18001 | Nueva Reserva ES-ES | Reserva nueva, español | Minibús ES (v19 y siguientes); Atención España (v2, sin publicar) |
| 18006 | Nueva Reserva ES-EN | Reserva nueva, inglés | Minibús ES (v19 y siguientes); Atención España (v2, sin publicar) |
| 18034 | 00. RA ES-ES AVERÍAS | Asistencia (avería o accidente), español, desde la V7 | Minibús ES (v19 y siguientes); Atención España (v2, sin publicar) |
| 18035 | RA ES-EN Breakdowns | Asistencia (avería o accidente), inglés, desde la V7 | Prolongaciones, Atención España (v2, sin publicar) |
| 18056 | 00. CC ES-ES- Hor.MiniBus | Minibús, punto de encuentro o idioma no atendido, español | Minibús ES; Atención España (v2, sin publicar) |
| 18059 | 00. CC ES-EN-Hor.MiniBus | Minibús, punto de encuentro o idioma no atendido, inglés | Minibús ES; Atención España (v2, sin publicar) |

En el código de Prolongaciones, 18034 y 18035 se llaman «RA ES-ES-Opciones» y «RA ES-EN-OPCIONES»,
que son los nombres de los menús 2114 y 2115. El destino es correcto y solo el nombre está mal (ver
pendientes de Prolongaciones).

### Horarios (observados en RingCentral y en las llamadas)
- **Gestión (18057 y 18061):**
  - los bots la tratan como abierta de lunes a viernes de 08:00 a 21:00;
  - en RingCentral el horario laboral es de 08:00 a 22:00 los 7 días, pero la regla «FHL - Opción 3
    Fin de Semana» (del viernes a las 21:00 al lunes a las 08:00) solo reproduce un anuncio y no hace
    sonar a ningún agente;
  - en fin de semana no atiende nadie: el sábado 10/10, 0 de 173 patas de bots atendidas;
  - falta que Centauro confirme que es intencionado.
- **Bienvenida en cola:** en la 18057 dura unos 35 s (el primer agente suena hacia los 37 s); en la
  18061, unos 20 s.
- **Nueva reserva, Minibús y Averías** atienden los 7 días.

### IDs internos de RingCentral

| Ext. | Id interno |
|---|---|
| 18001 | 1591780064 |
| 18034 | 3690726064 |
| 18035 | 3690727064 |
| 18056 | 3740185064 |
| 18057 | 3741268064 |
| 18059 | 3741323064 |
| 18061 | 3741335064 |
| 19236 (pata saliente de los bots) | 4027457064 |

## Colas de Reembolsos

Las colas de Centauro Reembolsos (V4) están por documentar (ver pendientes del caso). **Centauro
Reembolsos WhatsApp** (W1, copia de la V4 con la oferta de WhatsApp) usa **las mismas colas que la
V4**: antes de cambiar una cola de Reembolsos, cambia también las dos. «Centauro Reembolsos · Datos
por WhatsApp» (W2) no transfiere llamadas.

## Otras colas a las que transfieren los bots de Minibús

Las colas de Gestión, Nueva reserva y Averías de España están en la tabla de Prolongaciones.

| Ext. | Nombre | Nota |
|---|---|---|
| 18071 / 18074 | IT Mod. Reserva IT-IT / IT-EN | Mismo horario de fin de semana que Gestión ES |
| 18024 / 19042 | IT Nuova Prenotazione IT-IT / IT-EN | |
| 18064 / 18067 | PT Alteração PT-PT / PT Management EN | Mismo horario de fin de semana que Gestión ES |

## ⚠️ Destinos prohibidos (menús automáticos, no agentes)

Una transferencia con resumen a un menú falla siempre a los 54 s, porque nadie pulsa 1.

| Ext. | Nombre | Visto |
|---|---|---|
| 2114 | Menú de asistencia en carretera (ES), «RA ES-ES-Opciones» | Minibús ES 09/10; Prolongaciones V6 (05/10–07/10) |
| 2115 | Menú de asistencia en carretera (EN), «RA ES-EN-OPCIONES» | Minibús ES 09/10 y 10/10 (v19); Prolongaciones V6 (05/10–07/10) |
| 2119 | RA IT-EN-OPCIONES | Minibús IT 10/10 (v2) |
