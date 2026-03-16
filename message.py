class Message():
    def __init__(self, type, message):
        self.type = type
        self.message = message
        None

    
    def create_text_message(self, bytes_per_char = 4, isServer = False):
        #int_list = self.string_to_ints(self.message)
        int_list = [ord(c) for c in self.message]
        real_length = len(int_list)

        header = ("ISC" + self.type).encode("ASCII")
        size_field = real_length.to_bytes(2, byteorder="big")
        #payload = b"".join(self.encode_ints(int_list, bytes_per_char))
        payload = b""
        for val in int_list:
            payload += val.to_bytes(4, byteorder="big")
        bytesMessage = header + size_field + payload
        #bytesMessage = ("ISC" + self.type).encode("ASCII") + (len(self.message).to_bytes(2, byteorder="big")) + (b"".join(self.encode_ints(self.string_to_ints(self.message), bytes_per_char)))
        return bytesMessage
    
    def string_to_ints(self, text):
        #t = text.encode("utf-8")
        #out : list = list()
        #for i in range(len(t)):
        #    out.append(int(t[i]))
        #return out
        return [ord(c) for c in text]
    
    def encode_ints(self, int_list, bytes_per_int = 4):
        lsBytes : list = list()
        for i in range(len(int_list)):
            lsBytes.append(int_list[i].to_bytes(bytes_per_int, 'big'))
        return lsBytes
    

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