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
