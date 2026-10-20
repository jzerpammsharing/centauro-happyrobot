# scripts/test_creditos_runs.py
# Ejecutar: python3 -I scripts/test_creditos_runs.py
# Sin red: el cliente HTTP es una función inyectada.
import io
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import urllib.request  # noqa: E402

from creditos_runs import (BASE_POR_DEFECTO, ErrorHttp, SinRedirecciones, creditos_de_respuesta, leer_ids,  # noqa: E402
                           main, obtener_creditos)

fallos = 0
total = 0


def comprobar(nombre, obtenido, esperado):
    global fallos, total
    total += 1
    if obtenido != esperado:
        fallos += 1
        print("FALLO %s: obtenido %r, esperado %r" % (nombre, obtenido, esperado))


class HttpFalso:
    """Devuelve respuestas fijas por run_id y apunta las peticiones."""

    def __init__(self, respuestas):
        self.respuestas = respuestas
        self.peticiones = []

    def __call__(self, url, cabeceras):
        self.peticiones.append((url, dict(cabeceras)))
        run_id = url.rstrip("/").rsplit("/", 1)[-1]
        r = self.respuestas[run_id]
        if isinstance(r, list):  # varias respuestas seguidas (reintentos)
            r = r.pop(0)
        if isinstance(r, Exception):
            raise r
        return r


# --- creditos_de_respuesta: formas posibles de la respuesta ---
comprobar("total_credits", creditos_de_respuesta({"run_id": "x", "total_credits": 118.4}), 118.4)
comprobar("credits numérico", creditos_de_respuesta({"credits": 64}), 64)
comprobar("credits como texto", creditos_de_respuesta({"credits": "64.5"}), 64.5)
comprobar("credits como objeto con total", creditos_de_respuesta({"credits": {"total": 80, "llm": 50}}), 80)
comprobar("dentro de data", creditos_de_respuesta({"data": {"total_credits": 12}}), 12)
comprobar("suma de partidas", creditos_de_respuesta({"line_items": [{"credits": 10}, {"credits": 2.5}]}), 12.5)
comprobar("lista de partidas suelta", creditos_de_respuesta([{"credits": 1}, {"credits": 2}]), 3)
comprobar("sin dato de créditos", creditos_de_respuesta({"run_id": "x"}), None)
comprobar("créditos no numéricos", creditos_de_respuesta({"credits": "n/d"}), None)
comprobar("cero es un dato", creditos_de_respuesta({"total_credits": 0}), 0)

# --- leer_ids ---
with tempfile.TemporaryDirectory() as d:
    ruta = os.path.join(d, "ids.txt")
    with open(ruta, "w") as f:
        f.write("# comentario\nrun-1\n\n  run-2  \nrun-1\n")
    comprobar("leer_ids sin vacíos, comentarios ni repetidos", leer_ids(ruta), ["run-1", "run-2"])

# --- obtener_creditos ---
http = HttpFalso({"run-1": {"total_credits": 100}, "run-2": {"credits": 50}})
r = obtener_creditos(["run-1", "run-2"], "clave-falsa", http=http, base="https://api.ejemplo")
comprobar("dos runs", r, {"run-1": 100, "run-2": 50})
comprobar("url de facturación", http.peticiones[0][0], "https://api.ejemplo/billing/usage/runs/run-1")
# El run_id se escapa en la URL: un id con «/», «?» o «#» no puede cambiar la ruta
urls = []


def http_urls(url, cabeceras):
    urls.append(url)
    return {"total_credits": 1}


obtener_creditos(["a/b?c#d e"], "k", http=http_urls, base="https://api.ejemplo")
comprobar("run_id escapado en la URL", urls, ["https://api.ejemplo/billing/usage/runs/a%2Fb%3Fc%23d%20e"])
comprobar("cabecera Bearer", http.peticiones[0][1].get("Authorization"), "Bearer clave-falsa")
comprobar("base por defecto", BASE_POR_DEFECTO, "https://platform.happyrobot.ai")

http = HttpFalso({"run-1": ErrorHttp(404, "no encontrado"), "run-2": {"credits": 7}})
comprobar("un 404 deja null y sigue", obtener_creditos(["run-1", "run-2"], "k", http=http, base="b"),
          {"run-1": None, "run-2": 7})

esperas = []
http = HttpFalso({"run-1": [ErrorHttp(429, "límite"), ErrorHttp(429, "límite"), {"credits": 9}]})
comprobar("reintenta tras 429", obtener_creditos(["run-1"], "k", http=http, base="b", dormir=esperas.append), {"run-1": 9})
comprobar("esperas crecientes", esperas, [2, 4])

esperas = []
http = HttpFalso({"run-1": [ErrorHttp(429, "x")] * 10})
comprobar("429 sin fin acaba en null", obtener_creditos(["run-1"], "k", http=http, base="b", dormir=esperas.append),
          {"run-1": None})
comprobar("máximo 4 reintentos", len(esperas), 4)

http = HttpFalso({"run-1": ErrorHttp(401, "no autorizado"), "run-2": {"credits": 1}})
try:
    obtener_creditos(["run-1", "run-2"], "k", http=http, base="b")
    comprobar("401 corta", "sin excepción", "excepción")
except ErrorHttp as e:
    comprobar("401 corta con el código", e.codigo, 401)
comprobar("401 no sigue con más runs", len(http.peticiones), 1)

http = HttpFalso({"run-1": ValueError("json roto")})
comprobar("respuesta ilegible deja null", obtener_creditos(["run-1"], "k", http=http, base="b"), {"run-1": None})

# --- el cliente real no sigue redirecciones (la cabecera Authorization no sale del host) ---
peticion = urllib.request.Request("https://platform.happyrobot.ai/billing/usage/runs/x",
                                  headers={"Authorization": "Bearer k"})
try:
    SinRedirecciones().redirect_request(peticion, None, 302, "Found", {}, "https://otro.ejemplo/x")
    comprobar("redirección rechazada", "seguida", "rechazada")
except ErrorHttp as e:
    comprobar("redirección rechazada con su código", e.codigo, 302)
comprobar("el abridor usa el manejador sin redirecciones",
          any(isinstance(h, SinRedirecciones) for h in __import__("creditos_runs").ABRIDOR.handlers), True)

# --- main ---
with tempfile.TemporaryDirectory() as d:
    ruta = os.path.join(d, "ids.txt")
    with open(ruta, "w") as f:
        f.write("run-1\n")
    err = io.StringIO()
    rc = main([ruta], entorno={}, salida=io.StringIO(), errores=err)
    comprobar("sin clave sale con 2", rc, 2)
    comprobar("sin clave lo dice claro", "HAPPYROBOT_API_KEY" in err.getvalue(), True)
    comprobar("sin clave no imprime la clave", "Bearer" in err.getvalue(), False)

    out = io.StringIO()
    http = HttpFalso({"run-1": {"total_credits": 33}})
    rc = main([ruta], entorno={"HAPPYROBOT_API_KEY": "k", "HAPPYROBOT_API_BASE": "https://otra"}, http=http,
              salida=out, errores=io.StringIO())
    comprobar("con clave sale con 0", rc, 0)
    comprobar("imprime JSON run_id → créditos", json.loads(out.getvalue()), {"run-1": 33})
    comprobar("base desde el entorno", http.peticiones[0][0], "https://otra/billing/usage/runs/run-1")

    out = io.StringIO()
    http = HttpFalso({"run-1": {"total_credits": 33, "detalle": 1}})
    main([ruta, "--crudo"], entorno={"HAPPYROBOT_API_KEY": "k"}, http=http, salida=out, errores=io.StringIO())
    comprobar("--crudo imprime la respuesta tal cual", json.loads(out.getvalue()),
              {"run-1": {"total_credits": 33, "detalle": 1}})

    rc = main([], entorno={"HAPPYROBOT_API_KEY": "k"}, salida=io.StringIO(), errores=io.StringIO())
    comprobar("sin fichero sale con 2", rc, 2)

print("%d/%d casos correctos" % (total - fallos, total))
sys.exit(1 if fallos else 0)
