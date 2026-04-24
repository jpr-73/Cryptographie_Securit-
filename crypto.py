'''File with all the crypto logic'''


from hashlib import sha256
from math import gcd
import random


def shift_ints(ints, key):
    s = int(key)
    return [x + s for x in ints]



def decode_shift(msg):

    for i in range(1, 27) :

        raw_bytes2 = bytearray()
        for val in msg:
            shifted_val = (val - i) % 256

            raw_bytes2.append(shifted_val)

        try :
            print("Key " + str(i) + " = " + raw_bytes2.decode("utf-8", errors="replace") + " \n")

        except :
            print("Key " + str(i) + " = " + raw_bytes2.decode("latin-1") + " \n")
            print("problem with utf-8")



#implemented vigenere
def vigenere_ints(msg, key):
    res = []
    
    if isinstance(key, str):
        key = [ord(k) for k in key]
        
    length = len(key)

    for i in range(len(msg)):
        m = msg[i]          
        k = key[i % length]
        
        res.append(m + k)   
        
    return res


#implemented encode RSA :

def encodeRSA_ints(msg, n, e):
    res = []
    
    for i in range(len(msg)):
        res.append(pow(msg[i], int(e), int(n)))   

    return res

#implemented decode RSA
'''returns how many times the number was 
divided and what the odd remainder is'''
def decompose(n):
    i = 0
    while n &( 1 << i) == 0:
        i += 1
    return i, n >> i

'''Miller-Rabin compositeness test with witness a
Returns True if n is composite, false if n might be prime  '''
def iscomposite(a, n):
    t, d = decompose(n-1)
    x = pow(a, d, n)
    if x == 1 or x == n-1: # if x is already 1 or n-1 then this witness can't prove compositeness
        return False
    #square x repeatedly looking for a non-trivial square root of 1
    for i in range(1, t):
        x0 = x
        x = pow(x0, 2, n)
        if x == 1 and x0 != 1 and x0 != n -1:
            return True
    if x != 1: # if we never reached 1 by the end of the loop n fails to check if its prime
        return True
    return False

'''Using probability test 40 times if the number is composite
return true if x is very likely to be prime else false (probability
that the answer is wrong is less than 1 in 2^80)'''
def isPrime(x):
    if x % 2 == 0:# even number are never prime 
        return False
    for i in range(1, 40):# run 40 rounds with random witnesses more rounds = more certainty
        a = random.randint(1, x-1)
        if iscomposite(a, x):
            return False# 1 witness is enought to rule out the prime condition
    return True 


'''use the function isPrime and random to generate two random
prime numbers that aren't equal between 3 and the bounds given '''
def getRandomPrime(bound):
    p =random.randint(3, bound)
    q =random.randint(3, bound)
    while not isPrime(p):
        p =random.randint(3, bound)
    while not isPrime(q):
        q =random.randint(3, bound)
    if p == q:
        while not isPrime(q):
            q =random.randint(3, bound) 
    return p, q

'''For DH'''
def getOneRandomPrime(bound):
    p =random.randint(3, bound)
    while not isPrime(p):
        p =random.randint(3, bound)
    return p

def isPrimitiveRoot(p, generator):
    checked = []

    for i in range(1, p):
        result = pow(generator, i, p)

        if result not in checked :
            checked.append(result)
        else :
            return False
    return len(checked) == p-1
        



''' using the extended Euclid algorithm we find (d, x, y) such that 
a *x + b *y = d  and d = GCD(a, b)  '''
def extendedEuclid(a, b):
    if b == 0:
        return a, 1, 0
    else:
        d2, x2, y2 = extendedEuclid(b, a % b)# Recurse with (b, a mod b) — Euclid's classic remainder trick

        ''' Unwind: recalculate x and y for 
        the current level from the result below
        New x is the previous y
        New y is derived from the quotient (a // b) and previous coefficients'''
        d, x, y = d2, y2, x2 - (a // b) * y2
        return d, x, y


''' find the multiplicative inverse of e mod phi
returns x such that e * x = 1 mod phi and they require 
to not share any common factors  '''
def multiplicativeInverse(e, phi):
    return extendedEuclid(e, phi)[1] % phi


''' use the values p and q given by the function getRandomPrime
to get the values N, selecting E using the Totient 
And the private generated using the multiplicativeInverse function  '''
def getKeys(p, q):
    n = p * q #calculate N
    phi = (p -1) * (q-1) #calculate the Totient

    for i in range(2, phi):# find E such as 1 < E < Totient and gcd(e, Totient) = 1
        if gcd(phi, i) == 1: 
            e = i
            break
    d = multiplicativeInverse(e, phi)
    return n, e, d


def decodeRSA_ints(msg_ints, n, d):
    res = []
    text_message = ""

    print("[info] : n = " + n)
    print("[info] : d = " + d)

    for one_int in msg_ints:
        decrypted_int = pow(int(one_int), int(d), int(n))
        res.append(decrypted_int)
        text_message += chr(decrypted_int) 

    print("[info] : decrypted message = " + text_message)

    return res


"""la premiere fonction hach une list d'entier en utilisent sha256
chaque entier est traiter comme un point de code unicode -> utf 8 -> haché
c'est ensuite renvoyer sous forme de liste d'entier en hexdigest 
poui le hexdigest est envoyé au serveur sous forme de message
"""

def hash_ints(ints: list[int]) :
    #text = "".join(chr(i) for i in ints)
    #raw_bytes = text.encode("utf-8")

    #digest = sha256(raw_bytes).hexdigest()

    raw_bytes2 = b""
    for i in ints:
        quatre_octets = i.to_bytes(4, byteorder="little")

        raw_bytes2 += quatre_octets.replace(b'\x00', b'')
    
    digest = sha256(raw_bytes2).hexdigest()

    return [ord(c) for c in digest]

"""cette fonction verifie simplement que la list d'entier haché est bien
le hexdigest attendu"""

def verify_hash(ints: list [int], expected_hex: str) :

    #text = "".join(chr(i) for i in ints)
    #raw_bytes = text.encode("utf-8")

    #Le fait de passer par un chr coromps les caractères sur plusieurs bytes comme les é, je les ai donc récupérés sur des quadrioctets et les inteprêter correctement
    raw_bytes2 = b""
    for i in ints:
        quatre_octets = i.to_bytes(4, byteorder="little")

        raw_bytes2 += quatre_octets.replace(b'\x00', b'')

    digest = sha256(raw_bytes2).hexdigest()

    print("digest = " + str(digest))
    print("expected = " + str(expected_hex))


    return digest == expected_hex