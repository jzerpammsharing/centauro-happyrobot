# casos/reembolsos/codigo/test_telefono_whatsapp.py
# Ejecutar: python3 -I casos/reembolsos/codigo/test_telefono_whatsapp.py
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from telefono_whatsapp import normalizar_telefono, whatsapp_posible  # noqa: E402

CASOS_NORMALIZAR = [
    ("0034612345678", "+34612345678"),   # formato 00 que llega de la centralita
    ("0039375000000", "+39375000000"),   # extranjero con 00
    ("+34 612 34 56 78", "+34612345678"),
    ("612345678", "+34612345678"),       # nacional sin prefijo
    ("912345678", "+34912345678"),       # fijo nacional
    ("web", ""),                          # llamada web del editor
    ("", ""),
    (None, ""),
    ("anonymous", ""),
]

CASOS_POSIBLE = [
    ("+34612345678", True),    # móvil 6
    ("+34712345678", True),    # móvil 7
    ("+34912345678", False),   # fijo 9
    ("+34812345678", False),   # 8xx
    ("+3461234567", False),    # longitud incorrecta
    ("+39375000000", True),    # extranjero
    ("+447700900000", True),   # extranjero
    ("", False),
]

fallos = 0
for entrada, esperado in CASOS_NORMALIZAR:
    obtenido = normalizar_telefono(entrada)
    if obtenido != esperado:
        fallos += 1
        print("FALLO normalizar_telefono(%r) = %r, esperado %r" % (entrada, obtenido, esperado))
for entrada, esperado in CASOS_POSIBLE:
    obtenido = whatsapp_posible(entrada)
    if obtenido != esperado:
        fallos += 1
        print("FALLO whatsapp_posible(%r) = %r, esperado %r" % (entrada, obtenido, esperado))

print("OK" if fallos == 0 else "%d fallos" % fallos)
sys.exit(1 if fallos else 0)
