import random
import socket
import message
import client


host = "vlbelintrocrypto.hevs.ch"  # Le nom du serveur
port = 6000  # Le numéro de port du serveur
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))


"""
def addMsgHeader(msgType):
    header = b"ISC"


    if msgType == "t" or msgType == "T":
        header += b"t"
    elif msgType == "s" or msgType == "S":
        header += b"s"
    elif msgType == "i" or msgType == "I":
        header += b"i"

    return header

def addMsgSize(n):
    size = b""
    size += n.to_bytes(2, byteorder = "big")

    return size

"""



def diffie_hellman(p, g):

    cmd = message.Message("s", "task DifHel")
    client.send(cmd.create_text_message())


    privKey = random.randint(2, p-2)
    pubKey = pow(g, privKey, p)
    pubKeyBytes = pubKey.to_bytes((pubKey.bit_length() + 7) // 8, byteorder="big")
    pubKeySize = len(pubKeyBytes)
    msg = message.Message("s", str(pubKey))
    client.send(msg.create_text_message())


    #message = addMsgHeader("s") + addMsgSize(pubKeySize)+ pubKeyBytes

    s.sendall(message)
    otherPubKey = reception(b"s")
    sharedSecret = pow(otherPubKey, privKey, p)

    return sharedSecret


def reception(type):
    returnRecep= ""
    test = True

    while test: 
        x = s.recv(6)
        l = (int.from_bytes(x[-2:], byteorder='big')) * 4
        msgType = chr(x[3]).encode("utf-8")

        if msgType == type:
            returnRecep += giveOriginalMsg(s.recv(l))
            test = False
        else:
            s.recv(l)

    return returnRecep

def giveOriginalMsg(convertedMsg):
    res = ""
    conM = convertedMsg

    while conM != b"":
        charB = conM[:4]
        conM = conM[4:]
        a = charB.split(b"\x00")
        num = a[len(a)-1]
        res += num.decode("utf-8")

    return res




print(diffie_hellman(1009, 7))

