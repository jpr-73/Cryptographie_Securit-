#Project by Aurélien Santi - Alexandre Raccurt


import socket
import sys

host = "vlbeintrocrypto.hevs.ch"
port = 6000
ip = ""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(host, port)

def connect() :
    print("[+] Connecting to " + host + " : " + str(port))
    try: 
        ip = socket.gethostbyname('vlbelintrocrypto.hevs.ch')
        print("[+] Resolved server IP = " + ip)
    except socket.gaierror: 
        print ("[X] Connection impossible : There was an error resolving the host")
        sys.exit()

    try: 
        s.connect((ip, port))
        print("[V] Connected successfully")
    except socket.gaierror: 
        print ("[X] Connection impossible : Host Unreachable")
        sys.exit()

    return True

def messageType(msg):
    header = b"ISC"

    if msg == "t" or msg == "T" :
        header += "t"
    elif msg =="s" or msg == "S":
        header += "s"

    return header

def sizeOfMsg(b):
    result = b[4:]
    result = result[:2]
    return result

def addMsgSize(n): 
    size = b""
    size += n.to_bytes(2, byteorder="big")

    return size


