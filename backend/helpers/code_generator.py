import os

def generate_id_code(mode: str) -> str:
    match mode:
         case "payment":
             mode = "PAY"
         case "order":
             mode = "ORD"
         case "refund":
             mode = "REF"
         case "return":
             mode = "RET"
         case "case":
             mode = "CASE"
             
    code = os.urandom(3).hex().upper()
    
    if mode == None:
        return "Kindly put something"
    
    full_code = f"CORTORA-{mode}-{code}"
    
    return f"Code: {full_code}"
    
