import base64
import random
from math import gcd
import math
import sys


'''
This file is a test file to make the RSA encryption method

 Step 1 select two prime Numbers (p and q) => 7 et 19
    calculate their product (p * q) N => 7 * 19 = 133
    calculate then the Totient (p-1)*(q-1)T => 6 * 18 = 108
    select a Public Key (E) => E = 5
    must be Prime
    must be less than Totient
    must not be a factor to the Totient
    
    select a private key D
    (D * E) % T = 1
 
    Message ^E % N = Cipher
    Cipher ^D % N = Message
'''

#Prime check and generator for the first two primes

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
# extended Euclid gives x such that e * x + phi * y = 1
# taking mod phi drops the phi*y term leaving e* x = 1 mod phi
# the % phi at the end ensure that the result is positive


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






# convert a txt string into a single large int one byte per char
def encodeMessage(msg):
    encodedMsg = 0
    for char in msg:
        encodedMsg = encodedMsg << 8
        encodedMsg = encodedMsg ^ ord(char)
    return encodedMsg


#reverse encodeMessage extracts characters one byte at a time
def decodeMessage(encodedMsg):
    decodedMsg = ""
    while encodedMsg > 0:
        char = chr(encodedMsg & 0xFF)
        decodedMsg = char + decodedMsg
        encodedMsg = encodedMsg >> 8
    return decodedMsg

#read mod size from cmdline default to 1024 bits if not provided
try:
    modulusSize = int(sys.argv[1])
except:
    modulusSize = 1024

msg = "Hello how Դ are öÖé you ד ݜ ࠅ ݜ doing વ"


#key gen
primeSize = 2 ** modulusSize // 2
p, q = getRandomPrime(primeSize)
n, e, d = getKeys(p, q)

# rsa encrypt decrypt 
encodedMsg = encodeMessage(msg)
encryptedMsg = pow(encodedMsg, e, n)
decryptedMsg = pow(encryptedMsg, d, n)
decodedMsg = decodeMessage(decryptedMsg)

# Convert encrypted message to bytes and then to UTF-8 string
encrypted_bytes = encryptedMsg.to_bytes((encryptedMsg.bit_length() + 7) // 8, byteorder='big')

# Direct UTF-8 representation (may contain unprintable characters)
encrypted_utf8 = encrypted_bytes.decode('utf-8', errors='replace')

# For a safer UTF-8 representation, use base64 (still valid UTF-8)
encrypted_base64 = base64.b64encode(encrypted_bytes).decode('utf-8')

print("\nEncrypted message (UTF-8):\n\t", encrypted_utf8)
print("\nEncrypted message (Base64 for reliable transport):\n\t", encrypted_base64)
print("Public key (e, n):")
print("\te = ", e)
print("\tn = ", n)
print("\nPrivate key (d, n):")
print("\td = ", d)
print("\tn = ", n)
print("\nOriginal message string:\n\t", msg)
print("\nInteger encoded message:\n\t", encodedMsg)
print("\nEncrypted message( C(M) = M^e % n ):\n\t", encryptedMsg)
print("\nDecrypted message( M(C) = C^d % n ):\n\t", decryptedMsg)
print("\nDecoded message string:\n\t", decodedMsg)
print("\nEncrypted message (UTF-8):\n\t", encrypted_utf8)
if encodedMsg == decryptedMsg:
    print("\nThe decrypted message and the original encoded message match.")