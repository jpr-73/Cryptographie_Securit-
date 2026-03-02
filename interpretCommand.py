import main
import client
import message

def interpret(line) :
    if len(line) >=1 and line[0] == "/" :
        splitted = line.split(" ")
        #print(splitted)
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

                    message1 = message.Message("t", "CoucouAll")
                    message1.build()
                    print(message1.build())

                    #toSend += addMsgSize(message)
                    toSend = message1.build() ##len(message).to_bytes(2, big)
                    toSend = len(message1.build()).to_bytes(2, 'big')
                    print("toSend = " + toSend.decode())
                    #print("tosend = " + toSend)

                    main.client1.send(toSend)
                    main.client1.receive(100)

                    #if len(splitted) > 1 :
                    #    for el in splitted
                    #        message = splitted[1]
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