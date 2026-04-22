import main
import message
import cliText
import base64
import random
from math import gcd
from hashlib import sha256
import math
import sys

def interpret(line) :
    buff1 = main.buff1
    if len(line) >=1 and line[0] == "/" :
        splitted = line.split(" ")
        if len(splitted) > 0 :
            match splitted[0][1:] :
                case "help" :
                    print("Nobody hears you")
                    cliText.printCommandHeader()
                    return True
                case "exit" :
                    print("Good Bye")
                    main.client1.close()
                    return False
                case "send" :
                    if splitted[1] == "-s" :
                        message1 = message.Message("s", " ".join(splitted[2:]))
                    else :
                        message1 = message.Message("t", " ".join(splitted[1:]))
                        
                    toSend = message1.create_text_message() 
                    main.client1.send(toSend)
                    
                    return True
                
                case "task" :
                    splitted[0] = "task"
                    message1 = message.Message("s", " ".join(splitted[0:]))
                    toSend = message1.create_text_message() 
                    
                    main.client1.send(toSend)
                    return True

                
                case "set" :
                    buff1.set_content(" ".join(splitted[1:]))
                    print(f"[Buffer setted to :] {buff1.content} ")
                    print(f"[Buffer Int setted to :] {buff1.int_content} ")
                    return True
                
                case "clear" :
                    buff1.errase
                    print("[Buffer errased :] " + buff1.content)
                    return True
                
                case "show" :
                    print("[Buffer :] " + buff1.content)
                    print("[Buffer ints :] " + str(buff1.int_content))
                    return True
                
                case "generate" :

                    match splitted[1] :
                        case "rsa" :
                            primeSize = 2 ** 16 // 2
                            p, q = getRandomPrime(primeSize)
                            n, e, d = getKeys(p, q)

                            print("[Info] : Your RSA public key (do not use - sended to server) is e=" + str(e))
                            print("[Info] : Your RSA modular is n=" + str(n))
                            print("[Info] : Your RSA private key is d=" + str(d))

                            
                            message1 = message.Message("s", str(n) + "," + str(e))
                                
                            toSend = message1.create_text_message() 
                            main.client1.send(toSend)

                            return True


                        case "dh" :

                            p = getOneRandomPrime(5000)

                            generators = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
                            generator = 2
                            valid = False

                            for el in generators :
                                if isPrimitiveRoot(p, el) and not valid:
                                    generator = el
                                    valid = True

                            print("[Info] : Your DH modular world is p=" + str(p))
                            print("[Info] : Your DH generator world is g=" + str(generator))
                            
                            message1 = message.Message("s", str(p) + "," + str(generator))
                            main.client1.send(message1.create_text_message())

                            return True
                        
                        case "dh-hk" :
                            #print("g=" + str(splitted[1]) + " p=" + str(splitted[2]))
                            p = int(splitted[2])
                            g = int(splitted[3])

                            privKey = random.randint(2, p-2)
                            pubKey = pow(g, privKey, p)

                            print("[Info] : Your DH modular is g=" + str(g))
                            print("[Info] : Your DH private key is p1=" + str(privKey))
                            print("[Info] : Your DH public key is p2=" + str(pubKey))
                            
                            message1 = message.Message("s", str(pubKey))
                            main.client1.send(message1.create_text_message())

                            return True
                        
                        case "dh-secret" :
                            p = int(splitted[2])
                            privKey = int(splitted[3])
                            pubKey = int(splitted[4])
                            sharedSecret = pow(pubKey, privKey, p)

                            print("[Info] : Your DH secret is " + str(sharedSecret))
                            
                            message1 = message.Message("s", str(sharedSecret))
                            main.client1.send(message1.create_text_message())

                            return True
                        
                        case _ :
                            print("Unknown Command")
                            return True

                    
                
                case "encode" :
                    if buff1.content == "" : 
                        print("You have to set the buffer before to encode it")
                        return True
                    match splitted[1] :
                        case "shift" :
                            if len(splitted[2:]) == 0:
                                print("[Missing key : /encode shift <key>] ")
                                return True
                            
                            else :
                                shiftedText = shift_ints(buff1.int_content, " ".join(splitted[2:]))
                                try :
                                    #print("shifted message = ", shiftedText)

                                    message1 = message.Message("s", "")

                                    message1.ints = shiftedText
                                    
                                    toSend = message1.create_text_message() 
                                    main.client1.send(toSend)
                                except Exception as e:
                                    print(f"Error : {e}")


                                try :
                                    print(type(shiftedText))

                                except Exception as e:
                                    print(f"Error : {e}")
                        

                            return True

                        case "vigenere" :
                            if len(splitted[2:]) == 0:
                                print("[Missing key : /encode vigenere <key>] ")
                                return True
                            
                            else :
                                vigeneredText = vigenere_ints(buff1.int_content, " ".join(splitted[2:]))
                                try :

                                    message1 = message.Message("s", "")

                                    message1.ints = vigeneredText
                                    
                                    toSend = message1.create_text_message()
                                    main.client1.send(toSend)
                                except Exception as e:
                                    print(f"Error : {e}")


                                try :
                                    print(type(vigeneredText))

                                except Exception as e:
                                    print(f"Error : {e}")

                            return True
                        
                        case "rsa" | "RSA" :
                            print("rsa mode")
                            if len(splitted[2:]) == 0:
                                print("[Missing key : /encode RSA <n> <e>] ")
                                return True
                            else :
                                rsaedText = encodeRSA_ints(buff1.int_content, " ".join(splitted[2:3]), " ".join(splitted[3:]))
                                try :

                                    message1 = message.Message("s", "")
                                    message1.ints = rsaedText
                                    
                                    toSend = message1.create_text_message() 
                                    main.client1.send(toSend)
                                except Exception as e:
                                    print(f"Error : {e}")
                                
                                return True
                            
                        case "hash" :

                            digest = hash_ints(buff1.int_content)

                            print("[Info] : Le texte hashé = " + str(digest))

                            message1 = message.Message("s", "")
                            message1.ints = digest

                            toSend = message1.create_text_message() 

                            main.client1.send(toSend)
                        
                            return True

                                

                        case _ : 
                            print("Unknown Command")
                            return True

                case "decode" :    
                    #if buff1.content == "" : 
                    #    print("You have to set the buffer before to encode it")
                    #    return True
                    #else :
                        match splitted[1] :
                            case "shift" :

                                decode_shift(buff1.content)
                                return True
                            
                            case "vigenere" :

                                print("On va pas faire : pas le temps")
                                return True
                            
                            case "rsa" | "RSA" :
                                rsaedText = decodeRSA_ints(splitted[4:], " ".join(splitted[2:3]), " ".join(splitted[3:4]))
                                print(str(rsaedText))

                                message1 = message.Message("s", "")

                                message1.ints = rsaedText
                                
                                toSend = message1.create_text_message()
                                main.client1.send(toSend)
                                return True
                            
                            case "hash" :

                                verified = verify_hash(buff1.int_last_content, " ".join(splitted[2:3]))

                                #print("[Info] : Le texte hashé = " + str(digest))
                                print("[Info] : Le texte hashé correspond ? " + str(verified))

                                reponse = "true" if verified else "false"

                                message1 = message.Message("s", reponse)

                                message1.ints = []

                                toSend = message1.create_text_message()

                                main.client1.send(toSend)
                        
                                return True
                            
                            case _ :
                                print("Unknown Command")
                                return True
                
                case _ : 
                    print("Unknown Command")
                    return True
            
        else :
            print("Unknown Command")
            return True
    else :
        print("not a command")
        return True




def messageType(msg):
    header = b"ISC"

    if msg == "t" or msg == "T" :
        header += b"t"
    elif msg =="s" or msg == "S":
        header += b"s"
    elif msg =="i" or msg == "I":
        header += b"i"

    return header

def sizeOfMsg(b):
    result = b[4:]
    result = result[:2]
    return result

def addMsgSize(n): 
    size = b""
    size += n.to_bytes(2, byteorder="big")

    return size

def shift_ints(ints, key):
    s = int(key)
    return [x + s for x in ints]


def decode_shift(msg):

    for i in range(1, 27) :
        res = ""

        for c in msg:
            res += chr(ord(c) - i)
        print("Key " + str(i) + " : " + res)


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
    text = "".join(chr(i) for i in ints)
    raw_bytes = text.encode("utf-8")

    digest = sha256(raw_bytes).hexdigest()

    return [ord(c) for c in digest]

"""cette fonction verifie simplement que la list d'entier haché est bien
le hexdigest attendu"""

def verify_hash(ints: list [int], expected_hex: str) :
    text = "".join(chr(i) for i in ints)
    raw_bytes = text.encode("utf-8")
    digest = sha256(raw_bytes).hexdigest()

    return digest == expected_hex