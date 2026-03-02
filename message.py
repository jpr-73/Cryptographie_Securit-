class Message():
    def __init__(self, type, message):
        self.type = type
        self.message = message
        None

    def build(self):
        buildedMessage = b""
        header = self.messageType(self.type)
        buildedMessage += header
        buildedMessage += b"06"
        buildedMessage += (self.message).encode("utf-32-be")
        #toSend += addMsgSize(message)
        ##len(message).to_bytes(2, big)

        return buildedMessage
    
    def messageType(self, msg):
        header = b"ISC"

        if msg == "t" or msg == "T" :
            header += b"t"
        elif msg =="s" or msg == "S":
            header += b"s"
        elif msg =="i" or msg == "I":
            header += b"i"

        return header

    def sizeOfMsg(self, b):
        result = b[4:]
        result = result[:2]
        return result

    def addMsgSize(self, n): 
        size = b""
        size += n.to_bytes(2, byteorder="big")

        return size