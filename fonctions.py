# ===========================================
# Constants
# ===========================================
from operator import index

ISC_HEADER = b'ISC'

# ===========================================
# Int <-> Bytes Conversion
# ===========================================

def int_to_bytes(value, num_bytes):
    return value.to_bytes(num_bytes)

def bytes_to_int(data):
    return int.from_bytes(data)

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

# def encode_ints(int_list, bytes_per_int):

