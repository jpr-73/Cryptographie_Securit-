import main
import message
import cliText
import random
import crypto

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
                            p, q = crypto.getRandomPrime(primeSize)
                            n, e, d = crypto.getKeys(p, q)

                            print("[Info] : Your RSA public key (do not use - sended to server) is e=" + str(e))
                            print("[Info] : Your RSA modular is n=" + str(n))
                            print("[Info] : Your RSA private key is d=" + str(d))
                            
                            message1 = message.Message("s", str(n) + "," + str(e))
                                
                            toSend = message1.create_text_message() 
                            main.client1.send(toSend)

                            return True


                        case "dh" :

                            p = crypto.getOneRandomPrime(5000)

                            generators = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
                            generator = 2
                            valid = False

                            for el in generators :
                                if crypto.isPrimitiveRoot(p, el) and not valid:
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
                                shiftedText = crypto.shift_ints(buff1.int_content, " ".join(splitted[2:]))
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
                                vigeneredText = crypto.vigenere_ints(buff1.int_content, " ".join(splitted[2:]))
                                try :

                                    message1 = message.Message("s", "")

                                    message1.ints = vigeneredText
                                    
                                    toSend = message1.create_text_message()
                                    main.client1.send(toSend)
                                except Exception as e:
                                    print(f"Error : {e}")

                            return True
                        
                        case "rsa" | "RSA" :
                            print("rsa mode")
                            if len(splitted[2:]) == 0:
                                print("[Missing key : /encode RSA <n> <e>] ")
                                return True
                            else :
                                rsaedText = crypto.encodeRSA_ints(buff1.int_content, " ".join(splitted[2:3]), " ".join(splitted[3:]))
                                try :

                                    message1 = message.Message("s", "")
                                    message1.ints = rsaedText
                                    
                                    toSend = message1.create_text_message() 
                                    main.client1.send(toSend)
                                except Exception as e:
                                    print(f"Error : {e}")
                                
                                return True
                            
                        case "hash" :

                            digest = crypto.hash_ints(buff1.int_content)
                            print("[Info] : buff1 content " + str(buff1.int_content))
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
                        match splitted[1] :
                            case "shift" :

                                crypto.decode_shift(buff1.int_content)
                                return True
                            
                            case "vigenere" :

                                print("On va pas faire : pas le temps")
                                return True
                            
                            case "rsa" | "RSA" :
                                rsaedText = crypto.decodeRSA_ints(splitted[4:], " ".join(splitted[2:3]), " ".join(splitted[3:4]))
                                print(str(rsaedText))

                                message1 = message.Message("s", "")

                                message1.ints = rsaedText
                                
                                toSend = message1.create_text_message()
                                main.client1.send(toSend)
                                return True
                            
                            case "hash" :
                                try :
                                    verified = crypto.verify_hash(buff1.int_last_content, buff1.content)

                                    #print("[Info] : buff1 last content " + str(buff1.int_last_content))
                                    #print("[Info] : buff1 content " + str(buff1.int_content))
                                    #print("[Info] : Le texte hashé = " + str(digest))
                                    print("[Info] : Le texte hashé correspond ? " + str(verified))

                                    reponse = "true" if verified else "false"

                                    message1 = message.Message("s", reponse)

                                    message1.ints = []

                                    toSend = message1.create_text_message()

                                    main.client1.send(toSend)
                                
                                except Exception as e:
                                    print(f"Error : {e}")
                        
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

