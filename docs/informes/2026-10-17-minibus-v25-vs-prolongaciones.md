<!-- Comparación hecha el 17/10/2026 (solo lectura): Minibús ES v25 (k2in5n9kk01x) frente a Prolongaciones V11 (live) y v12 (borrador). En HappyRobot la versión de producción es la v22, pero la v25 recibe parte del tráfico real de España desde el 15/10 (experimento: 80 de 142 llamadas el 16/10, según el artefacto «Calidad Minibús»). -->

# Prolongaciones (V11 / V12) frente a Minibús España v25: conocimiento y reglas

Análisis de solo lectura del 17/10/2026. No se ha cambiado nada en HappyRobot.

**Fuentes**
- **Prolongaciones**:
  - `casos/prolongaciones/prompts/prolongacion-es/v11/prolongacion.md` (V11, en producción);
  - `v12/prolongacion.md` (borrador; añade ENVÍO DEL CORREO DE CONTRASEÑA);
  - `v11/transfer-to-human-agent.md`.
- **Minibús ES v25** («v25 · v24 + rama por defecto en ¿Enviar WhatsApp?», slug `k2in5n9kk01x`):
  - **Ojo:** en HappyRobot la de producción es la v22 (`2l6skwt8wphb`), pero la v25 recibe parte del tráfico real desde el 15/10 (experimento).
  - Cuatro módulos de prompt:
    - **T** = «Triaje y horario»;
    - **PE** = «Punto de encuentro»;
    - **IO** = «Información de oficina»;
    - **PyC** = «Prolongación y consultas».
  - Se han leído también:
    - las cuatro herramientas `transfer_to_human_agent`;
    - `consultas_alquiler` de T;
    - los nodos Python «Resolver colas por idioma» y «Calcular horario nocturno».
- PyC parte de una copia del prompt V11 de Prolongaciones: unos 40 párrafos son literales. Las diferencias de abajo son
  las que importan.

Estados:
- **IGUAL**: texto o regla idénticos.
- **PARECIDO**: cambia la redacción, o un lado tiene algún dato más, sin contradicción.
- **DISTINTO**: la regla, la cifra o la cola se contradicen.
- **FALTA**: no está en ningún módulo de Minibús.

---

## 1. Tema por tema

| Tema de Prolongaciones | Minibús v25 (módulo) | Estado | Nota |
|---|---|---|---|
| REGLA DE LONGITUD | PyC | IGUAL | Texto idéntico, ejemplos incluidos. Solo está en PyC. T, PE e IO usan «REGLAS DE CONVERSACIÓN POR VOZ»: frases de unas 25 palabras como máximo y las indicaciones en 2 o 3 frases. |
| GESTIÓN CERRADA: REGLA DE MÁXIMA PRIORIDAD | ninguno | FALTA | No está en ningún módulo, y en Minibús el riesgo es el mismo: «Resolver colas» también pone en `cola_gestion_reserva` el texto «NO DISPONIBLE AHORA…» cuando Gestión está cerrada, y ningún prompt advierte de que ese texto no es un destino. El punto 4 de Prolongaciones (si piden el horario de una oficina, decir que no se tiene) lo contradice Minibús: «Si te pregunta el horario de esa oficina, dáselo con tus datos». |
| IDIOMA DE ATENCIÓN | T, PE, IO, PyC | PARECIDO; DISTINTO en el francés (PyC) | En francés, Prolongaciones ofrece seguir «en español o en inglés, nombrando los dos». PyC ofrece «español, inglés, portugués o italiano, nombrando los cuatro». T, PE e IO siguen con los dos. Minibús añade que el cambio de idioma se hace «sin comentarlo», «nunca le digas qué idiomas atiendes», que un nombre propio o una frase mal transcrita no es un cambio y que, si el cliente ya hablaba otro idioma antes del módulo, se sigue en ese. A Minibús le falta «repite brevemente la pregunta de arranque». |
| IDENTIDAD Y ESTILO (extra) | los cuatro, adaptado | PARECIDO | PyC añade el trato de usted y la respuesta «Está hablando con un agente de IA». A PyC le falta la regla de reformular una sola vez la pregunta de la cuenta («¿Tiene usuario y contraseña…?») y, si sigue sin respuesta clara, tratarlo como un «no». |
| ARRANQUE / PUNTO DE PARTIDA (extra) | PyC; T hace el triaje | PARECIDO, con puntos DISTINTOS | PyC no saluda (lo hace T). Difiere en tres casos. Minibús o punto de encuentro: PyC usa `buscar_punto_de_encuentro` y Prolongaciones transfiere a MINIBÚS. Horario o dirección de una oficina: PyC usa `informacion_oficina`. Persona sin motivo: PyC transfiere a GESTIÓN sin la salvedad «solo si está abierta». En PyC faltan la rama «no pudo recoger a su hora», las ramas explícitas de devolver antes o en otra oficina y la de fianza y combustible (caen en «cualquier otra pregunta»), y la regla del ruido al empezar la llamada. |
| CÓMO HABLAR (extra) | PyC | IGUAL | PE e IO tienen su propia versión: siglas, códigos de parking y direcciones. |
| QUÉ NO HACES NUNCA (extra) | PyC | PARECIDO | Añade «servicio de espera» a las cifras permitidas y prohíbe prometer llamar «al conductor del minibús». |
| EXPLICACIÓN (contraseña y pasos) | PyC | IGUAL que la V11; DISTINTO de la V12 | Mismo texto que la V11: explicación, pregunta de la cuenta, instrucciones de la web, «¿Seguimos con los pasos para prolongar?», pasos y «¿Alguna duda?». No tiene la oferta de enviar el correo que añade la V12. |
| ENVÍO DEL CORREO DE CONTRASEÑA (solo V12) | ninguno | FALTA | La v25 no tiene la herramienta `enviar_correo_contrasena`. PyC mantiene «NO pidas … correo» y «no puedes … enviar correos». Tampoco tiene el motivo `correo_no_coincide` ni el deletreo de correos. |
| DEVOLVER TARDE | PyC | IGUAL | Sin cortesía, periodos de 24 horas, tiempo extra más penalización. |
| COCHE DE ASEGURADORA O DE EMPRESA | PyC | **DISTINTO** | Prolongaciones: «Puede prolongarlo usted mismo … o pedírselo a su aseguradora», y después cuenta, pasos y cierre. Minibús: «no le digas que puede prolongarlo él mismo» y «Tendrá que consultar directamente con su aseguradora si es posible», sin pasos ni aviso. Días que se puede alargar: Prolongaciones aplica la regla de 29/60; Minibús lo remite a la aseguradora. A Minibús le falta la pregunta «¿Llama usted como cliente del coche o en nombre de la aseguradora?». El coche de empresa es IGUAL. |
| DETALLES QUE PUEDES DAR | PyC | PARECIDO | Las cifras son iguales: 50 € por día de demora y 29/60 días. Minibús añade tres respuestas: se paga al hacer la prolongación (en la oficina o en la web), se puede prolongar el mismo día de la devolución, y para cambiar a un coche más grande en curso hay que ir a una oficina y pagar la diferencia. |
| LA WEB NO LE DEJA | PyC | PARECIDO | Igual, salvo que falta el párrafo de Gestión cerrada: el primer turno fijo, con el horario de Gestión y sin transferir. También falta el cambio de la V12 para «no le llega el correo»: ofrecer el envío. |
| CF: reserva que aún no ha empezado | PyC | **DISTINTO** | Cancelación gratis: Prolongaciones «hasta veinticuatro horas antes», Minibús «hasta cuarenta y ocho horas antes». A Minibús le falta la «REGLA» de no transferir salvo que el cliente prefiera, después de la respuesta, que lo haga un compañero. «Recoger antes» está redactado distinto, con el mismo sentido. El cupón (3 meses / 2 años), Booking y extras son IGUALES. |
| CF: recoger tarde / no pudo recoger | PyC | PARECIDO + FALTA | IGUALES: las 12 horas, el servicio de espera de 40 € (vuelo hasta la una de la madrugada, tren 60 minutos, comprobar antes de las 22:00), la lista de estaciones y la transferencia a GESTIÓN. FALTA el apartado «NO PUDO RECOGER A SU HORA». Horario o dirección de una oficina: Minibús usa `informacion_oficina`; Prolongaciones pregunta qué oficina y transfiere a GESTIÓN con motivo «otro». |
| CF: devolver antes / en otra oficina / con la oficina cerrada | PyC; también PE e IO | **DISTINTO** | Devolver antes: Prolongaciones devuelve los periodos si el alquiler es «de menos de veintinueve días» y nada «con veintinueve días o más»; Minibús pone el corte en 30 días. Con 29 días exactos se contradicen. En otra oficina: IGUAL. Con la oficina cerrada: Prolongaciones dice «depende de la oficina»; Minibús, «por norma» no se puede, salvo en Alicante aeropuerto (24 horas), y con buzón solo si se acordó al recoger. |
| CF: combustible / fianza / cargos / multas / facturas | PyC | PARECIDO | Cifras iguales: fianza a los 10 días, combustible hasta 12 días y 40 € de gestión por multa. Minibús añade «¿Se ha cerrado bien mi alquiler?» (encuesta, contrato y facturas). |
| CF: requisitos y conductores | PyC | PARECIDO | IGUALES: carnet, edad, documentos, tarjeta y conductor adicional (23/15/11 €, máximo 108 €). A Minibús le faltan el carnet caducado y el pago en efectivo. Minibús añade el billete de vuelta (si no lo tiene, depósito con tarjeta de crédito por la franquicia) y quién puede recoger o devolver el coche. |
| CF: durante el alquiler | PyC | PARECIDO | Todo IGUAL: kilómetros, suscripción, salir de España (32 / 18,50 / 14 €, máximo 168 €), limpieza hasta 100 €, mascotas, testigos y CarPlay. Minibús añade «Daños en salida» del contrato y enseñar la foto al personal antes de salir. |
| CF: otras preguntas | PyC | **DISTINTO** | IGUALES: sillas (15 €/día, máximo 120 €), cadenas (21/11/8 €, máximo 90 €), accesorios, entrega en Benidorm y Torrevieja, y objetos olvidados. Grúa municipal: Prolongaciones transfiere a GESTIÓN con motivo «otro»; Minibús da el teléfono de asistencia y ofrece ASISTENCIA. Teléfono de la oficina: a Minibús le falta la parte «si insiste … ofrécele pasarle con un compañero». |
| TELÉFONOS QUE PUEDES DAR | PyC | IGUAL | Los mismos cuatro: teléfono de asistencia en carretera, de reservas nuevas, y de las oficinas de Benidorm y Torrevieja (solo para el servicio de entrega), con los mismos horarios. Esos horarios coinciden con las fichas de IO. En modo virtual, Minibús también permite dar el de reservas nuevas y el de asistencia. |
| CIERRE | PyC | PARECIDO | Idéntico, salvo que falta «"¿Puedo ayudarle en algo más?" se pregunta UNA sola vez…». PE e IO cierran con «¿Puedo ayudarle en algo más?». T no tiene cierre. |
| NO INSISTAS | PyC; versión propia en T, PE e IO | PARECIDO | PyC transfiere a GESTIÓN sin «solo si está abierta» y añade el modo virtual. T, PE e IO transfieren a MINIBÚS. |
| COLA DE GESTIÓN CERRADA | T, PE, IO y PyC, con el mismo texto | PARECIDO (versión reducida) | Mismo horario de Gestión: de lunes a viernes de 8:00 a 21:00, hora peninsular. Faltan cuatro viñetas: avisar en el primer turno sin anunciar ninguna transferencia; si la web no deja prolongar, devolver en fecha o prolongar en la oficina; si llama una aseguradora, mutua o partner, darle el horario de Gestión; y «ni cuelgues antes…». Añade: «Si te pregunta el horario de esa oficina, dáselo con tus datos». |
| REGLAS DE ESCALADO | PyC; versión propia en T, PE e IO | PARECIDO, con diferencias | IGUALES: `extension_destino` obligatorio y los mismos 10 valores de `motivo_transferencia` en PyC. Cola por defecto: en Prolongaciones, GESTIÓN solo si está abierta; en PyC, GESTIÓN sin comprobarlo; en T, PE e IO, MINIBÚS. Cola de MINIBÚS: Prolongaciones la usa para cualquier pregunta del minibús; PyC, solo para quejas o si no encuentra el punto. ASISTENCIA: PyC añade la grúa. GESTIÓN: PyC quita el horario o la dirección de una oficina y la grúa. En modo virtual solo se transfiere a ASISTENCIA. |
| SI LA TRANSFERENCIA FALLA | solo PyC | PARECIDO; DISTINTO en un dato | Mismo procedimiento: reintento, segundo fallo, 112, teléfono de asistencia y de reservas nuevas. Prolongaciones dice que el cliente «oye música de espera»; PyC, «Mientras espera no oye nada». Las cuatro herramientas de la v25 tienen música de espera configurada. T, PE e IO no tienen esta sección. |
| `motivo_transferencia` (herramienta) | herramienta de PyC | IGUAL que la V11 | Los mismos 10 valores. La V12 añade `correo_no_coincide`. Las herramientas de T, PE e IO no tienen `motivo_transferencia`: solo `extension_destino` y `resumen_para_agente`. |

---

## 2. Qué tiene Minibús que Prolongaciones no tiene

- **Modo virtual** (los cuatro módulos):
  - fuera de 08:00 a 22:00 peninsular, el centro de atención está cerrado;
  - el saludo ya avisa de que no hay compañeros;
  - no se transfiere salvo una avería o un accidente;
  - el resto se remite a «a partir de las ocho»;
  - Prolongaciones no tiene nada equivalente: atiende y transfiere a cualquier hora.
- **Horario nocturno por aeropuerto** (T):
  - cuatro listas con las variables `nocturno_cet`, `nocturno_wet`, `nocturno_eet` y `nocturno_murcia`;
  - si la oficina ya ha cerrado, no da el punto de encuentro y dice a qué hora abre: 7:00, salvo Murcia, Bari, Florencia, Nápoles y Venecia (8:00).
- **Triaje con herramientas** (T):
  - «Primero el motivo, no el aeropuerto»;
  - quejas del minibús (transferencia inmediata, salvo que lleve menos de 10 minutos esperando);
  - herramientas `consultas_alquiler` (temas: prolongar, recoger_tarde, reserva_no_iniciada, devolucion, cargos_y_reembolsos, requisitos, durante_el_alquiler, otro), `informacion_oficina` y `buscar_punto_de_encuentro`.
- **Puntos de encuentro** (PE):
  - indicaciones por aeropuerto en España, Portugal, Italia y Grecia;
  - color del minibús, servicio gratuito, frecuencias y trayecto de 5 a 10 minutos;
  - aeropuertos sin minibús (Alicante con mostrador; Almería, Gran Canaria, Menorca y Tenerife Sur sin datos);
  - representante en Atenas y Corfú, y a pie en Catania, Cefalonia y Olbia;
  - qué hacer si «el bus tarda demasiado» o el cliente está perdido (con las referencias de Sevilla y el caso de Palma);
  - WhatsApp con el seguimiento en directo (Madrid T1, T2 y T4, Sevilla y Málaga).
- **Horario y devolución en aeropuertos** (PE):
  - de 7:00 a 23:00;
  - Murcia, de 8:00 a 22:00;
  - Alicante, de 7:00 a 23:30, con devolución las 24 horas;
  - Bari, Florencia, Nápoles y Venecia, de 8:00 a 23:00.
- **Fichas de oficinas** (IO):
  - unas 60 oficinas de España, Portugal, Italia y Grecia;
  - horario, dirección, cómo llegar para recoger y «DEVOLUCIÓN ESPECIAL»;
  - Smartkey (Plaza de España, Recoletos, Glòries);
  - ciudades con varias oficinas;
  - si preguntan por el código de un parking o hay problemas con Smartkey, a GESTIÓN;
  - no tiene horarios de festivos.
- **Respuestas que solo están en PyC:**
  - «Está hablando con un agente de IA»;
  - pagar la prolongación;
  - prolongar el mismo día de la devolución;
  - cambiar a un coche más grande en curso;
  - «¿Se ha cerrado bien mi alquiler?»;
  - billete de vuelta;
  - quién puede recoger o devolver el coche;
  - «Daños en salida»;
  - devolver con la oficina cerrada: por norma no se puede, salvo en Alicante (24 horas).
- **Reglas de voz comunes** (los cuatro módulos):
  - trato de usted;
  - frases de unas 25 palabras como máximo;
  - qué hacer si el cliente interrumpe una indicación.

---

## 3. Contradicciones de cifras y reglas

1. **Cancelación gratuita de una reserva que aún no ha empezado.**
   - Prolongaciones: «hasta veinticuatro horas antes».
   - Minibús (PyC): «hasta cuarenta y ocho horas antes».
2. **Coche de sustitución de una aseguradora o mutua.**
   - Prolongaciones: el cliente puede prolongarlo él mismo, y se le dan los pasos.
   - Minibús: «no le digas que puede prolongarlo él mismo».
   - La V12 va más allá en el sentido de Prolongaciones: ofrece el correo de contraseña «aunque reservara por la mutua».
3. **Devolver antes: dónde está el corte.**
   - Prolongaciones: 29 días. Minibús: 30 días.
   - Además, PyC no cuadra con sus propios 29 días: para prolongar, «menos de veintinueve»; para los kilómetros, «hasta veintinueve».
4. **Colas atendidas de noche.**
   - Minibús calcula el modo virtual: no hay compañeros de 22:00 a 08:00, hora peninsular.
   - Prolongaciones transfiere a MINIBÚS y a NUEVA RESERVA a cualquier hora («siguen funcionando»).
   - Una de las dos está mal. Hay que comprobar el horario real de esas colas.
5. **Horario de una oficina.**
   - Prolongaciones: «di que no lo tienes» y transfiere a GESTIÓN con motivo «otro».
   - Minibús: lo da con IO.
   - T dice «tú NO conoces … los horarios de las oficinas», pero copia la viñeta «dáselo con tus datos».
6. **Minibús y punto de encuentro.**
   - Prolongaciones transfiere a la cola de MINIBÚS (motivo `minibus`).
   - Minibús lo responde con herramienta y solo transfiere las quejas.
   - La herramienta de transferencia de PyC sigue mandando a la cola de MINIBÚS los «datos de una oficina concreta», aunque el prompt usa `informacion_oficina`.
7. **Grúa municipal.**
   - Prolongaciones: GESTIÓN (motivo «otro»).
   - Minibús: teléfono de asistencia y ASISTENCIA si el cliente acepta (motivo `asistencia`).
8. **Francés.**
   - Prolongaciones (y T, PE e IO) ofrecen dos idiomas.
   - PyC ofrece cuatro.
9. **Música de espera.**
   - Prolongaciones: el cliente «oye música de espera».
   - PyC: «no oye nada», aunque la herramienta tiene música configurada.
10. **Cola por defecto y «quiero hablar con una persona».**
    - Prolongaciones: GESTIÓN, solo si está abierta.
    - PyC: GESTIÓN sin comprobarlo.
    - T, PE e IO: MINIBÚS.
11. **Devolver con la oficina cerrada.**
    - Prolongaciones: «depende de la oficina».
    - Minibús: «por norma» no se puede, salvo en Alicante (24 horas).

**Coinciden en los dos bots:**
- la penalización de 50 € por día de demora;
- las 12 horas, que valen solo para recoger;
- que al devolver no hay periodo de cortesía (también en PE e IO);
- el servicio de espera de 40 €, con sus límites;
- los cuatro teléfonos y sus horarios;
- el horario de Gestión, de lunes a viernes de 8:00 a 21:00;
- los 10 valores de `motivo_transferencia` (V11 frente a PyC);
- las tarifas de conductor adicional, salida de España, sillas, cadenas, multas, limpieza y kilómetros;
- los plazos de la fianza (10 días) y del combustible (12 días);
- 29/60 días como máximo para prolongar.

---

## 4. Reglas globales: ¿se repiten en cada módulo o solo están en el Triaje?

Están **copiadas en cada módulo**, no centralizadas en T. Cada módulo es un prompt independiente tras el cambio de
módulo. Algunas solo están en PyC y una no está en ninguno.

| Regla | T | PE | IO | PyC |
|---|---|---|---|---|
| IDIOMA DE ATENCIÓN | sí (versión base) | sí (+ sigue el idioma anterior) | sí (+ sigue el idioma anterior) | sí, con variante (francés con 4 idiomas) |
| REGLAS DE CONVERSACIÓN POR VOZ (trato de usted, 25 palabras) | sí | sí (idéntica) | sí (idéntica) | sí (idéntica) |
| MODO DE ATENCIÓN (modo virtual) | sí | sí (adaptada) | sí (adaptada) | sí (adaptada) |
| «Gestión de reservas abierta ahora» + COLA DE GESTIÓN CERRADA | sí | sí (texto idéntico) | sí (texto idéntico) | sí (texto idéntico) |
| GESTIÓN CERRADA: REGLA DE MÁXIMA PRIORIDAD | no | no | no | no |
| Validar el enfado y no pedir datos personales | sí | sí | sí | sí |
| REGLA DE LONGITUD | no | no | no | sí |
| CÓMO HABLAR (texto a voz) | no | sí (propia) | sí (propia) | sí |
| NO INSISTAS | sí (a MINIBÚS) | sí (a MINIBÚS) | sí (a MINIBÚS) | sí (a GESTIÓN) |
| REGLAS DE ESCALADO + `extension_destino` obligatorio | sí (por defecto, MINIBÚS) | sí (por defecto, MINIBÚS) | sí (por defecto, MINIBÚS) | sí (por defecto, GESTIÓN) |
| «Después de ejecutarla no digas nada más» | sí | sí | sí | no |
| SI LA TRANSFERENCIA FALLA | **no** | **no** | **no** | sí |
| CIERRE | no (solo «Cierra la llamada con normalidad» en Gestión cerrada) | «¿Puedo ayudarle en algo más?» | «¿Puedo ayudarle en algo más?» | sí (completo, como Prolongaciones) |
| Sin cortesía al devolver / las 12 horas solo para recoger | no | sí | sí | sí |
| TELÉFONOS QUE PUEDES DAR | no | no | no | sí |
| «Agente de IA» | no | no | no | sí |

Conclusiones:
- **Fallo de transferencia.** T, el módulo que más transfiere (quejas del minibús, reservas nuevas, asistencia, Gestión), no sabe qué hacer si la transferencia falla.
- **Gestión cerrada.** El bloque «máxima prioridad» no está en ningún módulo, aunque el texto «NO DISPONIBLE AHORA…» sí se inyecta.

---

## 5. Incoherencias dentro de Minibús v25

- La herramienta de transferencia de PyC manda a la cola de MINIBÚS los «datos de una oficina concreta», pero el prompt de PyC dice que se use `informacion_oficina`.
- T dice que no conoce los horarios de las oficinas, pero su COLA DE GESTIÓN CERRADA dice «dáselo con tus datos». PyC tampoco tiene horarios en su prompt: tendría que usar IO.
- PyC usa 30 días para devolver antes y 29 días para prolongar y para los kilómetros.
- El francés se trata con cuatro idiomas en PyC y con dos en T, PE e IO.
- PyC dice que en espera no se oye nada, pero las herramientas tienen música de espera (T usa «Acoustic»; PE, IO y PyC, «holdacent»).

---

## Nota sobre los ficheros

- `prolongacion_y_consultas.md` se extrajo con `python3 -I` del resultado guardado en disco. Es el único que la herramienta guardó en fichero.
- Los prompts de T, PE e IO se devolvieron en línea, y se leyeron enteros desde ahí. No se han guardado como `.md`.
- `diff_prol_v11_v12.txt`: diff por párrafos entre la V11 y la V12 de Prolongaciones.
