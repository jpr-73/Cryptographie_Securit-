# ===========================================
# Constants
# ===========================================

ISC_HEADER = b'ISC'

# ===========================================
# Int <-> Bytes Conversion
# ===========================================

def int_to_bytes(value:int, num_bytes:int) -> bytes:
    return value.to_bytes(num_bytes, 'big')

def bytes_to_int(data:bytes) -> int:
    return int.from_bytes(data, 'big')


# ===========================================
# String <-> Integer List Conversion
# ===========================================

def string_to_ints(text):
    t = text.encode("utf-8")
    out : list = list()
    for i in range(len(t)):
        out.append(int(t[i]))
    return out

def ints_to_string(int_list):
    out = ""
    for i in range(len(int_list)):
        out += chr(int_list[i])
    return out

# ===========================================
# Network Encoding
# ===========================================

def encode_ints(int_list, bytes_per_int = 4):
    lsBytes : list = list()
    for i in range(len(int_list)):
        lsBytes.append(int_list[i].to_bytes(bytes_per_int, 'big'))
    return lsBytes

def decode_ints(data, bytes_per_int = 4):
    out : list = list()
    for i in range(len(data)):
        out.append(int.from_bytes(data[i], 'big'))
    return out

def decode (data, bytes_per_int = 4):
    out : str = ""
    for i in range(len(data)):
        out += data[i].decode("utf-32-be")
    return out

# ===========================================
# ISC Message Creation
# ===========================================

def create_text_message(text, bytes_per_char = 4, isServer = False):
    string = f"[ISC][t][{len(text)}][{encode_ints(string_to_ints(text), bytes_per_char)}]"
    return string

def create_image_message(width, hight, image_data):
    string = f"[ISC][i][{width}][{hight}][{encode_ints(image_data)}]"
    return string

# ===========================================
# Message Reception
# ===========================================