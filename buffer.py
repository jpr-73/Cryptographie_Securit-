
class Buffer:
    content = ""
    int_content = []
    int_last_content = []

    def __init__(self) : None

    def errase(self) :
        self.content = ""
        self.int_content = []
        self.int_last_content = []
    
    def set_content(self, text):
        self.int_last_content = self.int_content.copy() # Ajout pour recup l'avant dernier message pour le task hash verify
        self.content = text
        self.int_content = []

        for c in text :
            utf8_bytes = c.encode('utf-8')
            num = int.from_bytes(utf8_bytes, byteorder='little')
            self.int_content.append(num)

    def set_ints(self, ints):
        self.int_last_content = self.int_content.copy()
        self.int_content =[]

        for i in ints :
            self.int_content.append(i)