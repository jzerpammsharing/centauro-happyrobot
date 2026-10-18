# Pendientes del caso Atención España

## Antes de construir
- [x] Aprobar el spec (`specs/2026-10-18-bot-unico-arquitectura.md`) (18/10/2026).
- [ ] Revisar el plan de construcción (`planes/2026-10-18-bot-unico-construccion.md`) y elegir cómo se ejecuta.

## Al construir (comprobaciones del spec, §11)
- [ ] Qué copia el duplicado de la v25: Module Change, evals, agente de voz.
- [ ] Que un Module Change pueda volver al Triaje.
- [ ] Que el módulo de destino ve el historial.
- [ ] Cómo cortar la cadena de la transferencia sin transferir con Gestión cerrada, y qué recibe el agente.
- [ ] Que el whisper es lo que mantiene al bot en la llamada tras transferir (confirmar con HappyRobot).
- [ ] Que un nodo Python acepta el código de `buscar_respuesta`.
- [ ] Que la tabla de Twin se crea sola con los campos del extract.
- [ ] Horario real de las colas de Minibús y Nueva Reserva de noche (RingCentral, solo lectura).
- [ ] Cómo se mueve una línea entre workflows (publicar el antiguo sin ella o despublicarlo; números que siguen
      en versiones antiguas y borradores).
- [ ] Calendario de festivos nacionales de 2026 y 2027 en «Contexto de la llamada».

## Antes de conectar la primera línea (puerta 0, spec §8.4)
- [ ] Caso «coincide» del correo de contraseña probado con una reserva real (pendiente heredado de la v12).
- [ ] `pista_correo` probada con una reserva real (verifica y devuelve solo el dominio).
- [ ] Rutina diaria, artefacto y `scripts/medir_bots.py` funcionando.
- [ ] Movimiento de líneas y vuelta atrás ensayados, ida y vuelta, con la línea «Test SIP RingCentral».
- [ ] Cerrar el experimento de Minibús ES v25 antes de la fase 2 (mover las líneas de Minibús).

## Para negocio
- [ ] Los 7 «DECIDIR» de `comun/bloques/consultas-alquiler.md`.
- [ ] Si después se conecta la opción de Gestión cuando está cerrada.
- [ ] Confirmar con Centauro que Gestión no atiende los festivos autonómicos (hoy se tratan como laborables).
