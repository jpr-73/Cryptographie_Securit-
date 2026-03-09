def vigenere(msg, key):
    res = b""
    length = len(key)

    for i, char in enumerate(msg):
        m = int.from_bytes(char.encode("utf-8"), byteorder="big") #transform the current character into a utf-8 byte in big endian 4
        k = int.from_bytes(key[i % length].encode("utf-8"), byteorder="big") #transform the key and for each character the key will change based on the idx
        c = m + k # apply the key to the caracter to encrypt (E(x) = m + k)
        res += c.to_bytes(4, byteorder="big") 
    
    return res

def decode_vigenere(msg, key):
    res = ""
    length = len(key)
    ky_idx = 0

    for c in range(0, len(msg), 4):
        chunk = msg[c:c+4] # takes the current character of the string based on the index
        charInt = int.from_bytes(chunk, byteorder="big") # reformat it into int
        
        k = key[ky_idx % length] # revert the key 
        m = charInt - ord(k) # D(x) = m - k -> D(E(x)) = x  (basically doing the inverse function)
        
        res += chr(m)
        ky_idx += 1
    return res 

def vigenereByteless(msg, key):
    res = ""
    length = len(key)
    key_idx = 0

    for char in msg:
        if char.isalpha():
            k = key[key_idx % length]
            if char.isupper():
                base = ord('A')
                k_base = ord('A')
            else: 
                base = ord('a')
                k_base = ord('a')

            c = chr((ord(char)- base + ord(k)- k_base) % 26 + base)
            res += c
            key_idx += 1
        else:
            res += char            
    return res


def decodeVigenere(msg, key):
    res= ""
    length = len(key)
    key_idx = 0


    for char in msg:
        if char.isalpha():
            k = key[key_idx %length]
            if char.isupper():
                base = ord('A')
                k_base = ord('A')
            else:
                base = ord('a')
                k_base = ord('a')
            
            c = chr((ord(char)- base -(ord(k)- k_base)) % 26 + base)
            res += c
            key_idx += 1
        else:
            res += char
        
    return res
        
envryp = vigenere("bonjour comment sa va ", "lme")

d = decode_vigenere(envryp, "lme")

print(f"encrypted = {envryp}")

print(f"decrypted = {d}")