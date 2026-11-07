# Copia exacta de las funciones que van en el nodo «Calcular idioma y saludo» de
# «Centauro Reembolsos WhatsApp». Si se cambian aquí, se cambian también allí.


def normalizar_telefono(numero):
    """Devuelve el número en E.164 (+ y dígitos) o "" si no es un teléfono."""
    texto = str(numero or "").strip()
    digitos = "".join(c for c in texto if c.isdigit())
    if not digitos:
        return ""
    if texto.startswith("+"):
        return "+" + digitos
    if digitos.startswith("00"):
        return "+" + digitos[2:]
    if len(digitos) == 9:
        return "+34" + digitos
    return "+" + digitos


def whatsapp_posible(e164):
    """True si tiene sentido ofrecer WhatsApp a ese número."""
    if not e164 or not e164.startswith("+"):
        return False
    if e164.startswith("+34"):
        return len(e164) == 12 and e164[3] in "67"
    return len(e164) >= 9


def telefono_para_consulta(numero_cliente, telefono_prueba=""):
    """Teléfono (E.164) que va al MCP para buscar la reserva sin pedir datos, o "" si no hay.

    Es el número desde el que llama el cliente. En las llamadas web del editor (from_number =
    "web") es TELEFONO_PRUEBA, para poder probar la búsqueda por teléfono con una reserva
    propia. Con menos de 9 cifras (extensión interna, oculto) no se puede buscar: "".
    """
    numero = telefono_prueba if str(numero_cliente or "").strip() == "web" else numero_cliente
    e164 = normalizar_telefono(numero)
    return e164 if len(e164) - 1 >= 9 else ""
