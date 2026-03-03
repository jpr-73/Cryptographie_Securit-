import main
import client
import message

def interpret(line) :
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
                    message1 = message.Message("t", " ".join(splitted[1:]))
                    toSend = message1.create_text_message()
                    main.client1.send(toSend)

                    #if len(splitted) > 1 :
                    #    for el in splitted
                    #        message = splitted[1]
                    return True
                case _ : print("Unknown Command")
            
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