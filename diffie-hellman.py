import random

def diffie_hellman(p, g):
    privKey = random.randint(2, p-2)
    pubKey = pow(g, privKey, p)
    pubKeyBytes = pubKey.to_bytes((pubKey.bit_length() + 7)//8, byteorder="big")
    pubKeySize = len(pubKeyBytes)

    




