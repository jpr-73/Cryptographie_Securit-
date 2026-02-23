<<<<<<< HEAD
import cliText
import connect
import interpretCommand
=======
#Project by Aurélien Santi - Alexandre Raccurt - Gabriel Zeizer

import socket

host = "vlbeintrocrypto.hevs.ch"
port = 6000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(host, port)




def messageType(msg):
    header = b"ISC"

    if msg == "t" or msg == "T" :
        header += "t"
    elif msg =="s" or msg == "S":
        header += "s"
    elif msg =="i" or msg == "I":
        header += "i"

    return header

def sizeOfMsg(b):
    result = b[4:]
    result = result[:2]
    return result

def addMsgSize(n): 
    size = b""
    size += n.to_bytes(2, byteorder="big")

    return size




# shift a message by a key that has to be a int or a single character
# make sure to convert the shifted message in the right unicode in big-endian order

def shift(msg, key):
    res = b""
    s = int(key)

    for c in msg:
        charInt = int.from_bytes(c.encode("utf-8"), byteorder="big")
        charInt += s
        charByte = charInt.to_bytes(4, byteorder="big")
        res += charByte
    return res
        
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
    

>>>>>>> e201c94 (shift function implemented)

def main():
    cliText.print1stHeader()
    connected = connect.connect()

    if connect :
        cliText.printCommandHeader()
        while True :
            text = input(">")
            interpretCommand.interpret(text)



if __name__ == "__main__":
    main()
