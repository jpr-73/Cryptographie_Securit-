import random
import socket
import message
import client
import main


def diffie_hellman_ints(p: int, g: int):
    priv_key = random.randint(2, p-2)
    pub_key = pow(g, priv_key, p)

    msg_out = message.Message("s", str(pub_key))
    main.client1.send(msg_out.create_text_message())
    print(f"[DH] sent a public key: {pub_key}")

    return priv_key, pub_key


def compute_shared_sec(server_pub_int: list[int], priv_key:int, p:int):
    server_pub_str = "".join(chr(i) for i in server_pub_int)
    server_pub = int(server_pub_str.strip())

    shared_secret = pow(server_pub, priv_key, p)
    print(f"[DH] server public key: {server_pub}")
    print(f"[DH] Shared secret : {shared_secret}")

    return shared_secret

def shared_secret_ints(shared_secret: int):
    return [ord(c) for c in str(shared_secret)]
