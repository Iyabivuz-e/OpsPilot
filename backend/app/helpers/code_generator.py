import os

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
    
    code = os.urandom(3).hex().upper()

    if mode == None:
        return "Kindly put something"

    return f"CORTORA-{prefix}-{code}"

