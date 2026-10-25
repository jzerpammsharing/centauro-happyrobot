<!-- workflow: 01a14f1b-4ea9-7827-a4f3-4cfb06a896f6 · versión: v7 (3it0j96ugsqw) · nodos: Preparar transferencia (los cinco módulos) · copiado: 2026-10-25 -->

# Preparar transferencia (código Python) · los cinco módulos

- Los cinco nodos Python «Preparar transferencia» de la v7 llevan este código, `casos/atencion-es/codigo/preparar_transferencia.py`
  (pruebas: `python3 -I casos/atencion-es/codigo/test_preparar_transferencia.py`, 72/72). Pegado por API el 25/10/2026
  (D-021); `cola` sale de la herramienta `transfer_to_human_agent` de cada módulo y las cuatro URI de «Resolver colas»
  (`081e2b5d-b260-41a6-bd2a-6f82b26193d1`):

  | Módulo | Nodo de la v7 | `cola` |
  |---|---|---|
  | Triaje | `01a17350-f4e8-753f-b25e-7415f9167714` | `{{17c682a0-82d2-42f6-88fa-817d8cba0783.cola}}` |
  | Consultas del alquiler | `01a17350-f4e8-7e63-af66-ae63b19315f1` | `{{fbe2e40e-4915-4f44-9bac-59c318862e97.cola}}` |
  | Prolongación | `01a17350-f4e8-75d3-a6b9-89f1c8a20f0a` | `{{01a150ca-b67d-726a-845b-19c18b2e891e.cola}}` |
  | Punto de encuentro | `01a17350-f4e9-7dbe-a4b4-a8a310ae0bec` | `{{00435498-eccf-4110-9cf1-eb17821af3ed.cola}}` |
  | Información de oficina | `01a17350-f4e9-78ba-9808-c461e2db8a8f` | `{{62c5b6dd-5dde-4b3a-9a93-adb638c0bd66.cola}}` |

- Cambia respecto a la v2: el detalle de `gestion_cerrada`. De 8:00 a 22:00 manda seguir COLA DE GESTIÓN CERRADA (lo
  importante, a la cola minibus; facturas, reembolsos, cargos y reclamaciones, el horario de Gestión). De 22:00 a 8:00
  (modo virtual) hay otro detalle, sin la cola minibus, que de noche tampoco atiende. La lógica de transferir o no es
  la misma. Entradas, `execution_profile` standard e hijo «¿Transferir?»: `../v2/preparar-transferencia.md`.

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
#   El detalle manda seguir COLA DE GESTIÓN CERRADA: lo importante va a la cola minibus y las facturas, los
#   reembolsos, los cargos y las reclamaciones esperan a Gestión (D-021).
# - Red de seguridad del modo virtual (D-004): de 22:00 a 08:00, hora peninsular y calculada al ejecutarse, solo se
#   transfiere a asistencia; si piden minibus o nueva_reserva, no se transfiere y el resultado es modo_virtual, con
#   un detalle que remite a MODO DE ATENCIÓN del bloque de reglas comunes.
# - Si piden gestion en modo virtual, Gestión también está cerrada (cierra a las 21:00): gana gestion_cerrada,
#   porque COLA DE GESTIÓN CERRADA da el horario real de Gestión («a partir de las ocho» sería falso de viernes a
#   domingo y en vísperas de festivo) y el bloque de reglas comunes ya manda seguirla en un caso de gestión. Su
#   detalle es otro, sin la cola minibus, que de noche tampoco atiende (D-021).
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
    "No se ha transferido: gestión de reservas está cerrada (atiende de lunes a viernes de ocho de la mañana a "
    "nueve de la noche, salvo festivos). No uses la cola gestion: sigue COLA DE GESTIÓN CERRADA. Si es algo "
    "importante de su alquiler o su viaje, la cola minibus; si es una factura, un reembolso, un cargo o una "
    "reclamación, dile ese horario sin decir que le pasas con nadie."
)
DETALLE_GESTION_CERRADA_VIRTUAL = (
    "No se ha transferido: gestión de reservas está cerrada (atiende de lunes a viernes de ocho de la mañana a "
    "nueve de la noche, salvo festivos) y a esta hora solo hay compañeros en asistencia. No uses la cola gestion "
    "ni la minibus: dile ese horario con calma, sin decir que le pasas con nadie. Si es una avería o un accidente, "
    "transfiere a la cola asistencia."
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
        detalle = DETALLE_GESTION_CERRADA_VIRTUAL if modo_virtual_en(ahora) else DETALLE_GESTION_CERRADA
        return salida(False, "", "gestion_cerrada", detalle)

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
