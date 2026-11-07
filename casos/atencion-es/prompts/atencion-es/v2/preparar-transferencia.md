<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v2 (x8xd0llbdp3j) · nodos: Preparar transferencia (Triaje y Consultas del alquiler) · copiado: 2026-10-18 (Tarea 9b) -->

# Preparar transferencia (código Python) · Triaje y Consultas del alquiler

- Tipo: action (Python Sandbox), event_id `019dde7b-3500-7a3c-8f5e-1c2d4e6a8b9c`, execution_profile `standard`
- Triaje: ID = persistent_id en la v2 `01a14f64-277b-7226-8e39-a8ef0274949f` (creado en la Tarea 8); padre, la
  herramienta `transfer_to_human_agent` del Triaje (`17c682a0-82d2-42f6-88fa-817d8cba0783`)
- Consultas del alquiler: ID = persistent_id en la v2 `01a14fa7-1147-724b-af62-e10108d91bce` (Tarea 9); padre, la
  herramienta `transfer_to_human_agent` de Consultas (`fbe2e40e-4915-4f44-9bac-59c318862e97`)
- Hijo: Paths «¿Transferir?» (ver `transfer.md`)
- Código: `casos/atencion-es/codigo/preparar_transferencia.py` tal cual. Las Tareas 9 a 11 crean un nodo igual en la
  herramienta de transferencia de cada módulo (cambia solo el persistent_id de la herramienta en `cola`).
- Tarea 9b (18/10/2026, D-004): red de seguridad del modo virtual (resultado `modo_virtual`). Pegado el mismo código en
  los dos nodos «Preparar transferencia» de la v2: Triaje (`01a14f64-277b-…`, `cola` de `17c682a0-…`) y Consultas del
  alquiler (`01a14fa7-1147-724b-af62-e10108d91bce`, `cola` de `fbe2e40e-4915-4f44-9bac-59c318862e97`).

## Entradas (input_data)

```json
[
  {"key": "cola", "value": "{{17c682a0-82d2-42f6-88fa-817d8cba0783.cola}}"},
  {"key": "cola_gestion_reserva", "value": "{{081e2b5d-b260-41a6-bd2a-6f82b26193d1.cola_gestion_reserva}}"},
  {"key": "cola_asistencia", "value": "{{081e2b5d-b260-41a6-bd2a-6f82b26193d1.cola_asistencia}}"},
  {"key": "cola_nueva_reserva", "value": "{{081e2b5d-b260-41a6-bd2a-6f82b26193d1.cola_nueva_reserva}}"},
  {"key": "cola_horario_minibus", "value": "{{081e2b5d-b260-41a6-bd2a-6f82b26193d1.cola_horario_minibus}}"}
]
```

## Pruebas con `test_node` (Paso 3; 18/10/2026, domingo, Gestión cerrada)

`test_node` no usa la salida fijada de una herramienta (los argumentos llegan vacíos y sale `cola_no_valida`), así
que para la prueba se puso `cola` como texto fijo y después se volvió a dejar la variable de la herramienta:

| cola | transferir | numero | resultado | detalle |
|---|---|---|---|---|
| (argumento vacío) | false | «» | cola_no_valida | «No se ha transferido: la cola no es válida…» |
| `gestion` | false | «» | gestion_cerrada | el de `DETALLE_GESTION_CERRADA` |
| `asistencia` | true | URI SIP de Asistencia (español) | transferir | «» |

### Tarea 9b (18/10/2026, domingo, nodo de Consultas)

Mismo método (`cola` fija y después otra vez la variable de la herramienta). El reloj es el real: a las 20:06 y
20:07 todavía no era modo virtual.

| Hora (Madrid) | cola | transferir | numero | resultado |
|---|---|---|---|---|
| 20:06 | `minibus` | true | URI SIP de Minibús (español) | transferir |
| 20:07 | `gestion` | false | «» | gestion_cerrada (domingo) |

`modo_virtual` no se pudo ver con `test_node` antes de las 22:00; lo cubren las pruebas locales
(`test_preparar_transferencia.py`, 71/71).

## Código

```python
# ===============================================================
# PREPARAR TRANSFERENCIA - bot único de Atención España
# ---------------------------------------------------------------
# Se pega tal cual en el nodo Python «Preparar transferencia» de la herramienta transfer_to_human_agent de cada
# módulo, entre la herramienta y el Transfer «Initiate customer connection» (spec §5.8).
#
# Entradas (input_data):
#   cola                  la cola que elige el modelo: gestion | asistencia | nueva_reserva | minibus (argumento de
#                         la herramienta)
#   cola_gestion_reserva, cola_asistencia, cola_nueva_reserva, cola_horario_minibus
#                         las URI SIP de «Resolver colas» (sip:<ext>@hrpbx.buscentauro.com)
#
# Salidas: transferir (bool), numero (URI de la cola, o «» si no se transfiere), resultado (transferir |
# gestion_cerrada | modo_virtual | cola_no_valida) y detalle (instrucción para el agente cuando no se transfiere;
# vacío si se transfiere). El Transfer lleva en number y en fallback_number {{<este nodo>.numero}}.
#
# - Red de seguridad de Gestión cerrada: si piden «gestion» fuera de su horario (lunes a viernes de 08:00 a 21:00,
#   hora peninsular, y no en festivos nacionales), no se transfiere. La hora es la del momento en que se ejecuta
#   el nodo, no la del principio de la llamada: este nodo NO usa gestion_abierta, aunque llegue en la entrada.
#   Una llamada que empieza a las 20:55 y pide Gestión a las 21:02 no se transfiere.
# - Red de seguridad del modo virtual (D-004): de 22:00 a 08:00, hora peninsular y calculada al ejecutarse, solo se
#   transfiere a asistencia; si piden minibus o nueva_reserva, no se transfiere y el resultado es modo_virtual, con
#   un detalle que remite a MODO DE ATENCIÓN del bloque de reglas comunes.
# - Si piden gestion en modo virtual, Gestión también está cerrada (cierra a las 21:00): gana gestion_cerrada,
#   porque COLA DE GESTIÓN CERRADA da el horario real de Gestión («a partir de las ocho» sería falso de viernes a
#   domingo y en vísperas de festivo) y el bloque de reglas comunes ya manda seguirla en un caso de gestión.
# - Nunca se devuelve transferir = true con un número vacío: si la URI de la cola pedida no llega, el resultado es
#   cola_no_valida.
# - hora_madrid, gestion_abierta_en, modo_virtual_en y FESTIVOS_NACIONALES son una copia de contexto_llamada.py (un
#   nodo de HappyRobot no puede importar otro fichero): si cambian allí, cambian aquí. La prueba
#   test_preparar_transferencia.py comprueba que las dos copias dan lo mismo.
# ===============================================================
from datetime import date, datetime, timedelta, timezone

# cola del modelo -> clave de la entrada con la URI que dio «Resolver colas»
COLAS = {
    "gestion": "cola_gestion_reserva",
    "asistencia": "cola_asistencia",
    "nueva_reserva": "cola_nueva_reserva",
    "minibus": "cola_horario_minibus",
}

DETALLE_GESTION_CERRADA = (
    "No se ha transferido: el equipo de gestión de reservas atiende de lunes a viernes de ocho de la mañana a "
    "nueve de la noche, salvo festivos. Díselo al cliente con calma, no digas que le pasas con nadie y sigue con "
    "COLA DE GESTIÓN CERRADA."
)
DETALLE_MODO_VIRTUAL = (
    "No se ha transferido: de diez de la noche a ocho de la mañana no hay compañeros en esa cola. No lo vuelvas a "
    "intentar con ella; si es una avería o un accidente, transfiere a la cola asistencia. Si no, sigue MODO DE "
    "ATENCIÓN: dile que a esta hora no hay compañeros y que puede volver a llamar a partir de las ocho de la "
    "mañana, y no digas que le pasas con nadie."
)
DETALLE_COLA_NO_VALIDA = (
    "No se ha transferido: la cola no es válida. Usa gestion, asistencia, nueva_reserva o minibus."
)

# ---------------------------------------------------------------
# Copia de contexto_llamada.py (mantener igual)
# ---------------------------------------------------------------
# Festivos de ámbito nacional (resolución de la Dirección General de Trabajo publicada en el BOE). Los
# autonómicos y locales no cuentan. Hay que añadir el año siguiente antes de que acabe 2027.
FESTIVOS_NACIONALES = {
    # 2026
    date(2026, 1, 1),    # Año Nuevo
    date(2026, 1, 6),    # Epifanía
    date(2026, 4, 3),    # Viernes Santo
    date(2026, 5, 1),    # Fiesta del Trabajo
    date(2026, 8, 15),   # Asunción
    date(2026, 10, 12),  # Fiesta Nacional de España
    date(2026, 12, 8),   # Inmaculada Concepción
    date(2026, 12, 25),  # Navidad
    # 2027
    date(2027, 1, 1),    # Año Nuevo
    date(2027, 1, 6),    # Epifanía
    date(2027, 3, 26),   # Viernes Santo
    date(2027, 5, 1),    # Fiesta del Trabajo
    date(2027, 8, 15),   # Asunción (domingo)
    date(2027, 10, 12),  # Fiesta Nacional de España
    date(2027, 11, 1),   # Todos los Santos
    date(2027, 12, 6),   # Día de la Constitución
    date(2027, 12, 8),   # Inmaculada Concepción
    date(2027, 12, 25),  # Navidad
}

# Cola de GESTION DE RESERVA: solo de lunes a viernes de 08:00 a 21:00 (hora peninsular) y no en festivos
# nacionales. Fuera de ese horario la cola reproduce una locución de cerrado y nadie atiende.
GESTION_INICIO = 8
GESTION_FIN = 21

# Centro de atención con operadores: de 08:00 a 22:00 (hora peninsular).
# Fuera de esa franja el agente atiende en modo virtual, sin transferencias (salvo Asistencia).
CALLCENTER_INICIO = 8
CALLCENTER_FIN = 22

# Desfase base respecto a UTC en horario de invierno (solo la zona peninsular; el original tiene también wet y eet)
BASE = {
    "cet": 1,  # España peninsular, Baleares e Italia
}


def _en_utc(t):
    if t.tzinfo is None:
        return t.replace(tzinfo=timezone.utc)
    return t.astimezone(timezone.utc)


def ultimo_domingo(anio, mes):
    # Primer día del mes siguiente, retrocediendo al domingo anterior
    if mes == 12:
        d = datetime(anio + 1, 1, 1, tzinfo=timezone.utc)
    else:
        d = datetime(anio, mes + 1, 1, tzinfo=timezone.utc)
    d = d - timedelta(days=1)
    while d.weekday() != 6:  # 6 = domingo
        d = d - timedelta(days=1)
    return d


def en_horario_verano_ue(t):
    # Reglas UE: empieza el último domingo de marzo a las 01:00 UTC
    # y termina el último domingo de octubre a las 01:00 UTC
    t = _en_utc(t)
    inicio = ultimo_domingo(t.year, 3).replace(hour=1)
    fin = ultimo_domingo(t.year, 10).replace(hour=1)
    return inicio <= t < fin


def hora_local(ahora_utc, base):
    """Hora local de una zona con `base` horas de desfase en invierno (una más en horario de verano)."""
    t = _en_utc(ahora_utc)
    desfase = base + (1 if en_horario_verano_ue(t) else 0)
    return t.astimezone(timezone(timedelta(hours=desfase)))


def hora_madrid(ahora_utc):
    return hora_local(ahora_utc, BASE["cet"])


def callcenter_abierto_en(ahora_utc):
    return CALLCENTER_INICIO <= hora_madrid(ahora_utc).hour < CALLCENTER_FIN


def modo_virtual_en(ahora_utc):
    return not callcenter_abierto_en(ahora_utc)


def gestion_abierta_en(ahora_utc):
    local = hora_madrid(ahora_utc)
    return (local.weekday() < 5
            and local.date() not in FESTIVOS_NACIONALES
            and GESTION_INICIO <= local.hour < GESTION_FIN)


# ---------------------------------------------------------------
# Salida del nodo
# ---------------------------------------------------------------
def cola_de(valor):
    """La cola del modelo normalizada (sin espacios y en minúsculas), o «» si no es una de las cuatro."""
    cola = str(valor or "").strip().lower()
    return cola if cola in COLAS else ""


def salida(transferir, numero, resultado, detalle):
    return {"transferir": transferir, "numero": numero, "resultado": resultado, "detalle": detalle}


def preparar(input_data, ahora_utc=None):
    cola = cola_de(input_data.get("cola"))
    if not cola:
        return salida(False, "", "cola_no_valida", DETALLE_COLA_NO_VALIDA)

    # Gestión cerrada: se decide con la hora de ahora, nunca con gestion_abierta del principio de la llamada
    ahora = _en_utc(ahora_utc or datetime.now(timezone.utc))
    if cola == "gestion" and not gestion_abierta_en(ahora):
        return salida(False, "", "gestion_cerrada", DETALLE_GESTION_CERRADA)

    # Modo virtual: de noche solo hay compañeros en asistencia (gestion ya ha salido arriba como gestion_cerrada)
    if cola != "asistencia" and modo_virtual_en(ahora):
        return salida(False, "", "modo_virtual", DETALLE_MODO_VIRTUAL)

    # Sin URI no se transfiere: un Transfer con el número vacío falla
    numero = str(input_data.get(COLAS[cola]) or "").strip()
    if not numero:
        return salida(False, "", "cola_no_valida", DETALLE_COLA_NO_VALIDA)

    return salida(True, numero, "transferir", "")


try:
    _entrada = input_data  # noqa: F821 (lo inyecta el nodo Python de HappyRobot)
except NameError:  # importado desde las pruebas locales
    _entrada = None
if _entrada is not None:
    output = preparar(_entrada)
```
