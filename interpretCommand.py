import main
import message
import cliText

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
                                    print("shifted message = ", shiftedText)

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

                                

                        case _ : 
                            print("Unknown Command")
                            return True

                case "decode" :    
                    if buff1.content == "" : 
                        print("You have to set the buffer before to encode it")
                        return True
                    else :
                        match splitted[1] :
                            case "shift" :

                                decode_shift(buff1.content)
                                return True
                            
                            case "vigenere" :

                                print("On va pas faire : pas le temps")
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
# convert a txt string into a single large int one byte per char
'''def encodeMessage(msg):
    encodedMsg = 0
    for char in msg:
        encodedMsg = encodedMsg << 8
        encodedMsg = encodedMsg ^ ord(char)
    return encodedMsg


encodedMsg = encodeMessage(msg)
encryptedMsg = pow(encodedMsg, e, n)'''

def encodeRSA_ints(msg, n, e):
    res = []
    
    for i in range(len(msg)):
        res.append(pow(msg[i], int(e), int(n)))   

    return res
    