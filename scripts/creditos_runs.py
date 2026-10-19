"""Créditos de HappyRobot por run, con la API de facturación (solo lectura).

Uso: python3 -I scripts/creditos_runs.py <run_ids.txt> [--crudo]
- run_ids.txt: un run_id por línea (las vacías y las que empiezan por # se ignoran).
- Imprime un JSON {run_id: créditos} (número, o null si la API no dio el dato para ese run).
- --crudo: imprime {run_id: respuesta tal cual} para ver la forma de la respuesta (primera prueba con la API).

Petición: GET <base>/billing/usage/runs/{run_id} con la cabecera `Authorization: Bearer <clave>` (documentación de
HappyRobot: SDK, apartado Billing, `getRunCredits`; la cabecera es la del resto de la API pública).
- La clave se lee SOLO de la variable de entorno HAPPYROBOT_API_KEY. Nunca va en el repo ni en la salida.
- La base es https://platform.happyrobot.ai; se puede cambiar con HAPPYROBOT_API_BASE.
- No sigue redirecciones (un 3xx deja el run en null): la clave no sale nunca hacia otro host.
- Un 429 se reintenta hasta 4 veces (esperas de 2, 4, 8 y 16 s). Un 401/403 corta todo (clave mal). Cualquier otro
  error deja ese run en null y sigue.
Sin la clave, sale con código 2 y un mensaje claro: la rutina pone entonces `creditos` = null en todas las llamadas.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE_POR_DEFECTO = "https://platform.happyrobot.ai"
RUTA = "/billing/usage/runs/%s"
REINTENTOS_429 = 4
CLAVES_TOTAL = ("total_credits", "credits_total", "total", "credits", "credit", "amount")
CLAVES_ANIDADAS = ("data", "usage", "result")
CLAVES_PARTIDAS = ("line_items", "items", "breakdown")


class ErrorHttp(Exception):
    def __init__(self, codigo, texto=""):
        super().__init__("HTTP %s %s" % (codigo, texto))
        self.codigo = codigo


class SinRedirecciones(urllib.request.HTTPRedirectHandler):
    """No sigue redirecciones: así la cabecera Authorization nunca viaja a otro host."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ErrorHttp(code, "redirección no seguida")


ABRIDOR = urllib.request.build_opener(SinRedirecciones)


def http_urllib(url, cabeceras):
    """Cliente HTTP real (urllib, sin seguir redirecciones). Devuelve el JSON decodificado o lanza ErrorHttp."""
    peticion = urllib.request.Request(url, headers=cabeceras, method="GET")
    try:
        with ABRIDOR.open(peticion, timeout=30) as respuesta:
            return json.loads(respuesta.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise ErrorHttp(e.code, e.reason)


def _numero(valor):
    if isinstance(valor, bool):
        return None
    if isinstance(valor, (int, float)):
        return valor
    if isinstance(valor, str):
        try:
            return float(valor)
        except ValueError:
            return None
    return None


def creditos_de_respuesta(datos):
    """Créditos totales de un run a partir de la respuesta de la API, sea cual sea su forma; None si no hay dato."""
    if isinstance(datos, list):
        valores = [creditos_de_respuesta(x) for x in datos]
        valores = [v for v in valores if v is not None]
        return sum(valores) if valores else None
    if not isinstance(datos, dict):
        return _numero(datos)
    for clave in CLAVES_TOTAL:
        if clave in datos:
            valor = datos[clave]
            if isinstance(valor, dict):
                valor = creditos_de_respuesta(valor)
            numero = _numero(valor)
            if numero is not None:
                return numero
    for clave in CLAVES_ANIDADAS:
        if isinstance(datos.get(clave), (dict, list)):
            numero = creditos_de_respuesta(datos[clave])
            if numero is not None:
                return numero
    for clave in CLAVES_PARTIDAS:
        if isinstance(datos.get(clave), list):
            return creditos_de_respuesta(datos[clave])
    return None


def leer_ids(ruta):
    ids = []
    with open(ruta) as f:
        for linea in f:
            linea = linea.strip()
            if linea and not linea.startswith("#") and linea not in ids:
                ids.append(linea)
    return ids


def _pedir(run_id, clave, http, base, dormir):
    url = base.rstrip("/") + RUTA % run_id
    cabeceras = {"Authorization": "Bearer %s" % clave, "Accept": "application/json"}
    espera = 2
    for intento in range(REINTENTOS_429 + 1):
        try:
            return http(url, cabeceras)
        except ErrorHttp as e:
            if e.codigo == 429 and intento < REINTENTOS_429:
                dormir(espera)
                espera *= 2
                continue
            raise


def obtener_creditos(run_ids, clave, http=http_urllib, base=BASE_POR_DEFECTO, dormir=time.sleep, crudo=False,
                     errores=sys.stderr):
    """{run_id: créditos o None}. Con crudo=True, {run_id: respuesta tal cual}. 401/403 lanza ErrorHttp."""
    resultado = {}
    for run_id in run_ids:
        try:
            datos = _pedir(run_id, clave, http, base, dormir)
        except ErrorHttp as e:
            if e.codigo in (401, 403):
                raise
            print("Aviso: %s sin créditos (%s)" % (run_id, e), file=errores)
            resultado[run_id] = None
            continue
        except Exception as e:  # red caída, JSON ilegible...
            print("Aviso: %s sin créditos (%s)" % (run_id, type(e).__name__), file=errores)
            resultado[run_id] = None
            continue
        resultado[run_id] = datos if crudo else creditos_de_respuesta(datos)
    return resultado


def main(argv, entorno=None, http=http_urllib, salida=sys.stdout, errores=sys.stderr):
    entorno = os.environ if entorno is None else entorno
    args = list(argv)
    crudo = "--crudo" in args
    if crudo:
        args.remove("--crudo")
    if len(args) != 1:
        print("Uso: python3 -I creditos_runs.py <run_ids.txt> [--crudo]", file=errores)
        return 2
    clave = entorno.get("HAPPYROBOT_API_KEY", "").strip()
    if not clave:
        print("Error: falta la variable de entorno HAPPYROBOT_API_KEY (clave de la API de HappyRobot). "
              "Sin ella no hay créditos por run: pon `creditos` = null y sigue con el resto de la medición.",
              file=errores)
        return 2
    base = entorno.get("HAPPYROBOT_API_BASE", "").strip() or BASE_POR_DEFECTO
    try:
        resultado = obtener_creditos(leer_ids(args[0]), clave, http=http, base=base, crudo=crudo, errores=errores)
    except ErrorHttp as e:
        print("Error: la API rechazó la clave (%s). Revisa HAPPYROBOT_API_KEY y HAPPYROBOT_API_BASE." % e.codigo,
              file=errores)
        return 3
    json.dump(resultado, salida, indent=2, ensure_ascii=False)
    salida.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
