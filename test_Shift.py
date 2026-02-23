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



test_shift = shift("hello", "123")
print("shifted message ->", shift("hello", "123"))
print("decoded shifted message ->", decode_shift(test_shift, "123"))