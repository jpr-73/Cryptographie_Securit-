#Project by Aurélien Santi - Alexandre Raccurt

'''
def connect() :
    

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
'''

