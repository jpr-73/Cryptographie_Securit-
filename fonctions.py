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

def ints_to_string(int_list):
    out = ""
    for i in range(len(int_list)):
        out += chr(int_list[i])
    return out

# ===========================================
# Network Encoding
# ===========================================



def decode_ints(data, bytes_per_int = 4):
    out : list = list()
    for i in range(len(data)):
        out.append(int.from_bytes(data[i], 'big'))
    return out

def decody (data, bytes_per_int = 4):
    print(type(data))
    out : str = ""
    for i in range(len(data)):
        out += data.decode()
    return out

# ===========================================
# ISC Message Creation
# ===========================================



def create_image_message(width, hight, image_data):
    string = f"[ISC][i][{width}][{hight}][{encode_ints(image_data)}]"
    return string

# ===========================================
# Message Reception
# ===========================================