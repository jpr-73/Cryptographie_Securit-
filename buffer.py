
class Buffer:
    content = ""
    int_content = []

    def __init__(self) : None

    def errase(self) :
        self.content = ""
    
    def set_content(self, text):
        self.content = text
        self.int_content = []

        for c in text :
            utf8_bytes = c.encode('utf-8')
            num = int.from_bytes(utf8_bytes, byteorder='little')
            self.int_content.append(num)