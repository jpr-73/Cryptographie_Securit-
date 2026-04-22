from hashlib import sha256

"""la premiere fonction hach une list d'entier en utilisent sha256
chaque entier est traiter comme un point de code unicode -> utf 8 -> haché
c'est ensuite renvoyer sous forme de liste d'entier en hexdigest 
poui le hexdigest est envoyé au serveur sous forme de message
"""

def hash_int(ints: list[int]) :
    text = "".join(chr(i) for i in ints)
    raw_bytes = text.encode("utf-8")

    digest = sha256(raw_bytes).hexdigest()

    return [ord(c) for c in digest]

"""cette fonction verifie simplement que la list d'entier haché est bien
le hexdigest attendu"""

def verify_hash(ints: list [int], expected_hex: str) :
    text = "".join(chr(i) for i in ints)
    raw_bytes = text.encode("utf-8")
    digest = sha256(raw_bytes).hexdigest()

    return digest == expected_hex

"""
def hash_hex_from_ints(ints: list(int)):
    text = "".join(chr(i)for i in ints)
    return sha256(text.encode("utf-8")).hexdigest()

"""