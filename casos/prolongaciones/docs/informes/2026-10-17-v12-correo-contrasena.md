# v12 · Envío del correo de contraseña: pruebas (17/10/2026)

Versión probada: v12 `mnhi8x9j8ce7` (version_id `01a14967-1843-78bc-89ed-0241ed3b4daa`), sin publicar.
Datos de prueba inventados: «Prueba Prueba», 03/03/1990, `prueba.prueba@example.com`. Spec:
`../specs/2026-10-17-envio-correo-contrasena.md`. Decisión: D-008.

## 1. Pruebas de los nodos

| Prueba | Resultado |
|---|---|
| Código de «Decidir envío» y «Resultado para el agente» en local (`codigo/test_correo_contrasena.py`) | 21/21 |
| `consultar_reserva` sin argumentos (development) | Pide `nombre_completo` y `fecha_nacimiento` |
| `enviar_reset_contrasena` sin argumentos, con `numero_reserva` y con email vacío (development) | «email Field required» en los tres: no envía nada |
| `consultar_reserva` con `email` de prueba (development) | `encontrada false`, `verificado false`: acepta el email como identificador |
| Cadena completa con datos que no coinciden (`test_node` nodo a nodo) | consulta no encontrada → `email_envio` vacío → MCP rechaza → `resultado: no_coincide` |
| Variables (`fix_broken_vars`, dry run) | Ninguna rota. Solo falla «Initiate customer connection» por falta de room en la prueba (igual que en la V11) |
| Prompt subido frente a la copia del repo | Idéntico (61.058 caracteres), con las dos variables como variables |
| Entorno al que llegan las pruebas | Railway *production* con la API real de Centauro (`centauro_bot`), según los logs: las llamadas de *development* no son un entorno de pruebas. Los tres sondeos de `enviar_reset_contrasena` se rechazaron en la validación, sin llegar a la API |
| Caso «coincide» de punta a punta | No probado: necesita una reserva real y un correo accesible |

## 2. Evals nuevas (carpeta «Correo de contraseña (v12)» del nodo «Prolongacion»)

Formato como en Reembolsos: las llamadas previas a la herramienta van como mensaje `assistant` con
`tool_calls` y un mensaje `tool`. Todas fijan `gestion_abierta` (el valor por defecto es false).

Ronda 1, con el prompt inicial:

| Eval | Caso | eval_id | Ronda 1 | Run |
|---|---|---|---|---|
| CORREO-01 | Sin cuenta (mutua): ofrece enviar el correo | `01a1497b-c292-7ebe-9c94-1d598576194c` | PASS | `8217472a-d300-422c-8e8c-10d61b3df4ac` |
| CORREO-02 | Acepta el envío: pide solo el correo de la oficina | `01a1497b-c64b-704d-bf76-c9e6a25a553a` | PASS | `f086c5f8-de58-4ab9-9111-b6521529ad27` |
| CORREO-03 | Dicta el correo: lo repite deletreando y pide confirmación | `01a1497b-ca0d-754a-a4cb-ca0c07c0d644` | PASS | `014f9024-2930-44c1-b06c-1dd40d9a4310` |
| CORREO-04 | Con los tres datos: ejecuta enviar_correo_contrasena | `01a1497b-ce6d-7dc3-afa9-1aab21379967` | FAIL | `ac786c34-93b5-49cf-a8e8-9239f3bdc87f` |
| CORREO-05 | Resultado enviado: avisa de 'restablecer' y pregunta si le ha llegado | `01a1497c-8853-7637-9a7d-22d159aac7cb` | PASS | `602962c0-39f5-4f8e-82e0-dfc288c0e9c1` |
| CORREO-06 | Le ha llegado: crear la contraseña y '¿Seguimos?' | `01a1497c-8ce2-7a8d-a935-b09a397a3037` | PASS | `67356b77-153e-4cef-8259-6ebb23e402fb` |
| CORREO-07 | '¿Cuál es la contraseña?': no se envía contraseña, sino un enlace | `01a1497c-907e-74bf-a220-4d478816c3ba` | PASS | `a14bae9a-090a-41f4-b30d-a889d6cfed96` |
| CORREO-08 | No le llega tras mirar spam: ofrece reenviarlo | `01a1497c-93a7-7bcc-8852-a59c47ae1558` | PASS | `022545d5-c4bb-45b4-8cc2-ae1260271f68` |
| CORREO-09 | Tampoco llega tras el reenvío: GESTIÓN, error_tecnico | `01a1497d-58c0-7eb8-9389-dbaa52931a86` | PASS | `eea548ab-3898-42e7-a735-f8daabfff769` |
| CORREO-10 | No coincide (Gestión abierta): lo dice y transfiere con correo_no_coincide | `01a14979-e2ad-7f50-96b5-456724104412` | PASS | `1772706f-bff7-499c-923f-f68439b967fc` |
| CORREO-11 | No coincide con Gestión cerrada: no transfiere ni lo anuncia | `01a1497d-5d4a-7f9d-b304-9a80ef911ab2` | PASS | `ce84751a-f5d6-4358-9d55-906725f2317c` |
| CORREO-12 | Servicio no disponible: plan B sin transferir | `01a1497d-61cc-76bc-97f4-780e5d406340` | PASS | `dfc4f74b-accd-4bec-8a73-7c7958b68255` |
| CORREO-13 | Email no interpretado: pide que lo deletree | `01a1497d-667a-7313-b7c4-c33330beae90` | PASS | `12000532-0d52-4e20-be1a-94684b9178ee` |
| CORREO-14 | Ya tiene contraseña: pasos directos, sin ofrecer el envío | `01a1497e-1372-7628-a1a1-460b45d609bd` | PASS | `88b1e573-422c-4b4b-a44c-68cb1b4970f5` |
| CORREO-15 | Pide SMS: solo por correo electrónico | `01a1497e-1728-75d1-bac2-c1dacc17e92a` | PASS | `c2d182a0-7b83-45ac-b68e-15f77d5769fc` |
| CORREO-16 | Ofrece el número de reserva: no hace falta, pide el correo | `01a1497e-1bd0-70b1-bd0e-4e539f6186b2` | PASS | `405d6a9b-1292-4034-b97f-c8152046cb52` |
| CORREO-17 | Llama la pareja del titular: sigue con el correo de la titular | `01a1497e-1fcd-7f0a-85d2-103f998351ad` | PASS | `cab1bad8-1ac2-4e4e-8474-afba2f5c1f24` |
| CORREO-18 | No puede abrir el correo del trabajo: no lo cambia, oficina como alternativa | `01a1497e-23d3-78c4-8fd1-f80608b6e5a8` | PASS | `ddb341be-8bae-4220-bab8-f6e2b7bd7cb6` |
| CORREO-19 | Llamada en inglés: ofrece el envío en inglés | `01a1497e-2789-7227-bb84-044c20dea7a8` | FAIL | `6146e787-3e45-4020-8053-3c714059a3ef` |
| CORREO-20 | Rechaza el envío: instrucciones de la web (plan B) | `01a1497e-2c20-79c6-a84d-140b37ab06fd` | PASS | `b0801f1f-c8df-442a-becb-f5b42a3f0fda` |

Los dos fallos de la ronda 1:
- **CORREO-04:** la llamada a la herramienta es correcta, pero el resultado simulado volvió como error y
  el bot transfirió. Se añade al prompt que cualquier resultado que no sea uno de los cuatro cuenta como
  `no_disponible`. Además, la eval pasa a valorar solo la llamada, y se crea **CORREO-21**
  (`01a1498e-40af-77e3-b904-9a5841154e22`) para probar el error de forma explícita.
- **CORREO-19:** en inglés, ofrecía el envío sin terminar con la pregunta. Se añade que ese turno termina
  siempre con la pregunta, también en otro idioma. En la ronda 2 pasa.

## 3. Regresión (evals de la V11)

Ronda 1. Casi ninguna tiene run de la V11 (el último es de la V8, 07/10):

| Eval | eval_id | v12 ronda 1 | Último run de V11 | Run v12 |
|---|---|---|---|---|
| PROL-01 | `01a117c1-c804-7c5b-b5a8-4cf7bec71d12` | PASS | sin run de V11 | `c36c285b-3f72-423a-b9e9-de3a91646510` |
| PROL-02 | `01a117c1-ccb9-7c0c-9693-34a412f22b3e` | PASS | sin run de V11 | `5405c6d1-ef95-490f-9bd1-f82fe0956b84` |
| PROL-03 | `01a117c1-d071-7ae0-99e8-4564e630a13d` | FAIL | sin run de V11 | `fde21bb6-44ef-4210-9adc-b8770c65ab65` |
| PROL-04 | `01a117c1-d46b-7b2c-aa21-510476820b77` | FAIL | sin run de V11 | `4f943708-756a-4510-b1b1-aa66a7c8209a` |
| PROL-05 | `01a117c1-d86a-7709-b929-12fe733c4442` | PASS | sin run de V11 | `1df4d1a2-c358-4fca-b998-8db93775a5fe` |
| PROL-06 | `01a117c1-dc69-7d33-98d3-76be5747b248` | PASS | sin run de V11 | `21af790a-9ba3-4c53-adba-6eb5c0eb5f4d` |
| PROL-07 | `01a117c1-e018-7814-b3c1-2319b318dfdd` | PASS | sin run de V11 | `a8155b74-26d5-42be-871c-d89d3d690bee` |
| ASEG-01 | `01a117bf-70a5-7aba-bf42-dd07bad86cb0` | PASS | sin run de V11 | `5ed1d4a1-496b-4122-85b9-a07a0a4088f6` |
| ASEG-03 | `01a117c4-90f4-7146-9b41-f66a83b18645` | PASS | sin run de V11 | `5f41f13c-9293-40ad-a233-8ea1777d9414` |
| ASEG-06 | `01a117c4-9e0c-717e-aaf7-44b4d3383dcb` | FAIL | sin run de V11 | `d94d941d-9cd3-4c41-810d-28d9223635cf` |
| CIERRE-01 | `01a117c9-dbab-7a74-9c47-592a819e584a` | PASS | sin run de V11 | `f32fd1e3-dce1-491f-b759-9371ad9194ff` |
| CIERRE-02 | `01a117c9-e058-7cd5-8735-149fd45bed6a` | PASS | sin run de V11 | `59313ff7-de60-42bd-9f83-7be6cbe7e7d5` |
| WEB-08 | `01a117c3-a405-7874-a23c-f655344a7413` | FAIL | sin run de V11 | `76e5f9b8-1f4f-44a5-8b00-e2b397d1c8e3` |
| WEB-09 | `01a117c3-ffd9-7ad5-80da-3a870a3c6a19` | FAIL | sin run de V11 | `248b587f-44f4-4129-b56a-fbc29b5d9b61` |
| WEB-10 | `01a117c3-ac2e-73db-ad6f-8aea67d7683b` | PASS | sin run de V11 | `17650e8d-a603-46a2-89f8-90c3ca1de11d` |
| ESC-01 | `01a117c9-585f-73bc-a321-bd554cd6dc23` | PASS | sin run de V11 | `da39bb43-35a1-4923-89ed-37058981ca95` |
| ESC-02 | `01a117c9-5c18-7bca-9583-90c9670284d9` | FAIL | sin run de V11 | `838097c2-e616-4460-b913-cceb8f8b6b7d` |
| ESC-06 | `01a117c9-6e46-7694-8654-163076c9e376` | FAIL | sin run de V11 | `ce59d204-08b8-42cf-b1af-6b9302fd7138` |
| HOR-A1 | `01a126bc-1aa2-7d36-843b-6bef4709cdb2` | PASS | sin run de V11 | `a0c8e4eb-cef4-4937-8ee3-1095f26f00f9` |
| HOR-C1 | `01a126bb-b676-7473-bc9b-c762aa09a142` | PASS | PASS | `f68f9a3d-64cb-44b3-92fe-57b8b6e3daa6` |
| HOR-C2 | `01a126bb-cddb-79e1-b3df-55bde7585ed1` | PASS | PASS | `2e37f234-b0dc-42c0-a9fa-e0cd4e2c8124` |
| FDS-05 | `01a12a39-7ac4-7907-9211-83dd8e04053d` | FAIL | PASS | `68d84b70-64eb-41db-9a19-74835b801a3b` |
| FDS-06 | `01a12a39-98a5-702d-a28a-c8f234f7a006` | PASS | PASS | `162d23c9-b2a7-4a1f-ae31-8a8c20dfb61e` |
| FDS-07 | `01a12a39-c113-7c3d-b6a9-ab6fb4e9390d` | PASS | PASS | `fdc1d341-8e64-491f-8db9-793108f4fac5` |
| FDS-08 | `01a12a39-ec97-7b38-8f5f-7c4b71a338c2` | PASS | PASS | `41a9701b-4b30-4c8f-aa7d-57f76c29baf4` |
| IDIOMA-01 | `01a117c8-6c67-7b34-9528-432ed9dead20` | PASS | sin run de V11 | `14862af6-c514-415c-a95b-f969736f77a1` |
| BORDE-08 | `01a117dc-a5a7-70d8-ab0a-aff1f26fecb3` | PASS | sin run de V11 | `fb6b3694-19fa-4c12-ba2b-5f22a4b76c7d` |

Lectura de los fallos:
- **Cambian de expectativa por diseño (no son regresiones):** PROL-03, PROL-04, ASEG-06 y WEB-09
  esperan las instrucciones de la web o la transferencia directa; la v12 ofrece antes el envío del
  correo. WEB-08 espera «puede pedirlo otra vez»; la v12 da los consejos y, en el turno siguiente,
  ofrece enviarlo.
- **Ajustado en el prompt:** WEB-08 ofrecía el envío en el mismo turno que los consejos. Ahora primero
  los consejos y, si sigue sin llegar, la oferta.
- **No dependen de la v12:** ESC-06 falla también en la V11 hoy (sábado, Gestión cerrada por defecto).
  FDS-05 ya fallaba 4 de 7 veces en la V11, con el mismo motivo.
- **ESC-02:** transfiere bien, pero tras el error simulado de la transferencia no se ve el reintento.
  Para que la regla nueva de errores no se lea como «no reintentes la transferencia», se ha acotado a
  `enviar_correo_contrasena`.

## 4. Ronda 2 y ronda final

Ronda 2, con el prompt corregido (oferta con pregunta en cualquier idioma, errores de la herramienta como
`no_disponible`, consejos antes de ofrecer el envío):

| Eval | Versión | Resultado | Run |
|---|---|---|---|
| CORREO-19 | v12 | PASS | `80d1b608-316a-4e2d-89d5-769188f07a80` |
| CORREO-01, 08, 12, 13, 20 (control) | v12 | PASS | ver `resultados` en HappyRobot |
| CORREO-04 | v12 | FAIL (transfiere tras el error simulado) | `86f18e9f-92b0-420e-bd73-0d41d7c1cc6a` |
| WEB-08 | v12 | FAIL | `1b3d4fe8-69ac-4a44-b4a2-85a336554c44` |
| ESC-02 | v12 | FAIL (sin reintento tras el error simulado) | `92d9aecb-2f64-4fa5-91bb-87750e228d07` |
| ESC-06 | V11 | FAIL: también falla en la V11 | `637a8713-77f4-4587-b6ff-07c705ee0e0d` |
| WEB-09 | V11 | PASS (en la v12 cambia por diseño) | `f982fd77-6d73-4919-9e6b-f8d47bfd0d45` |

Ronda final, con el prompt definitivo: la regla de errores, acotada a `enviar_correo_contrasena`. CORREO-04
valora solo la llamada.

| Eval | Versión | Resultado | Run |
|---|---|---|---|
| CORREO-04 | v12 | PASS | `34d9d361-4f19-4f0f-b1fd-78816af12ae9` |
| CORREO-21 (error de la herramienta → plan B) | v12 | PASS | `64c3bc8c-2f48-4572-83cb-8f137891f21b` |
| CORREO-12 | v12 | PASS | `dcfcb6f9-b519-40b3-aed2-dd865df49a55` |
| ESC-02 | v12 | PASS (reintenta tras el error) | `f9d74b47-31f5-49cf-945c-944377a07e01` |
| ESC-02 | V11 | PASS | `3b002685-b729-4a0e-be93-dae4dcfa5745` |
| WEB-08 | v12 | FAIL: espera «puede pedirlo otra vez» (comportamiento de la V11); el bot no dijo «sin erratas» | `870d6a1e-0d16-4950-8061-d37669d4d6c4` |

**Estado de las evals nuevas:** las 21 pasan en su última ejecución (CORREO-01 a 20 en la ronda 1 o 2 y
CORREO-04 y 21 en la final). Las rondas 1 y 2 de CORREO-02, 03, 05 a 07, 09 a 11 y 14 a 18 se hicieron
antes de los ajustes del prompt; los ajustes no tocan esos pasos, pero no se han repetido.


## 5. Pendiente

- Caso «coincide» con una reserva real y prueba por voz (ver `pendientes.md`).
- Decidir si se actualiza la respuesta esperada de PROL-03, PROL-04, ASEG-06, WEB-08 y WEB-09. Las evals
  son del workflow y también se usan para comparar con la V11.
