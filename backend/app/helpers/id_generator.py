import os
from datetime import datetime


def generate_id_code(mode: str) -> str:
    prefixes = {
        "payment": "PAY",
        "order": "ORD",
        "refund": "REF",
        "return": "RET",
        "case": "CASE",
    }
    prefix = prefixes.get(mode)

    if prefix is None:
        raise ValueError(f"Unknown mode")

    now = datetime.now().year
    code = os.urandom(8).hex().upper()  ## We shall be checking the 1st 4 digits

    if mode == None:
        return "Kindly put something"

    return f"CT-{prefix}-{now}-{code}"
