import random
import string


def generate_pnr(length: int = 6) -> str:
    prefix = "FB"
    chars = string.ascii_uppercase + string.digits
    code = "".join(random.choices(chars, k=length))
    return f"{prefix}{code}"
