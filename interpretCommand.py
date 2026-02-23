

def interpret(line) :
    splitted = line.split(" ")
    #print(splitted)
    if len(splitted) > 0 :
        if splitted[0][1:] == "help" :
            print("Heeeeelp meeeeeee")
        else :
            print("Unknown Command")
    else :
        print("Unknown Command")
