import main
import client
import message
import buffer

def interpret(line) :
    buff1 = main.buff1
    if len(line) >=1 and line[0] == "/" :
        splitted = line.split(" ")
        if len(splitted) > 0 :
            match splitted[0][1:] :
                case "help" :
                    print("Nobody hears you")
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
                    

                    #if len(splitted) > 1 :
                    #    for el in splitted
                    #        message = splitted[1]
                    return True
                case "set" :
                    None
                case "encode" :
                    match splitted[1] :
                        case "shift" :
                            shifted = shift(" ".join(splitted[2:]), buff1)

                            message1 = message.Message("s", shifted)
                            toSend = message1.create_text_message()
                            print("message = " + toSend.decode())
                            main.client1.send(toSend)

                            return True

                        case "vigenere" :
                            print("will vigenere here")
                            return True

                        case _ : 
                            print("Unknown Command")
                            return True
                case _ : 
                    print("Unknown Command")
                    return True
            
        else :
            print("Unknown Command")
    else :
        print("not a command")




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