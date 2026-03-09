import cliText
import interpretCommand
import client
import buffer
#Project by Aurélien Santi - Alexandre Raccurt - Gabriel Zeizer

import socket
import threading

host = "vlbeintrocrypto.hevs.ch"
port = 6000
ip = ""
help
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(host, port)

client1 = client.Client()
buff1 = buffer.Buffer()

def main():
    working = True
    cliText.print1stHeader()

    connected = client1.connect(host, port)

    iListen = threading.Thread(target=client1.receive)
    iListen.start()

    cliText.printCommandHeader()
    while working :
        print()
        text = input(">")
        working = interpretCommand.interpret(text)





        
# decode the shifted message from byte and big-endian order to a string to be readable 
# for the user

def decode_shift(msg, key):
    res = ""
    s = int(key)

    for c in range(0, len(msg), 4):
        chunk = msg[c:c+4]
        charInt = int.from_bytes(chunk, byteorder="big")
        charInt -= s
        res += chr(charInt)
    return res

def vigenere(msg, key):
    res = b""
    length = len(key)

    for i, char in enumerate(msg):
        m = int.from_bytes(char.encode("utf-8"), byteorder="big") #transform the current character into a utf-8 byte in big endian 
        k = int.from_bytes(key[i % length].encode("utf-8"), byteorder="big") #transform the key and for each character do a different mod with the current index we are in
        c = m + k # apply the key to the caracter to encrypt (E(x) = m + k)
        res += c.to_bytes(4, byteorder="big") 
    
    return res

def decode_vigenere(msg, key):
    res = ""
    length = len(key)
    ky_idx = 0

    for c in range(0, len(msg), 4):
        chunk = msg[c:c+4] 
        charInt = int.from_bytes(chunk, byteorder="big")
        
        k = key[ky_idx % length] 
        m = charInt - ord(k) # D(x) = m - k -> D(E(x)) = x
        
        res += chr(m)
        ky_idx += 1
    return res 
    




if __name__ == "__main__":
    main()
