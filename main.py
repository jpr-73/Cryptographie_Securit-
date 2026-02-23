import cliText
import connect
import interpretCommand

def main():
    cliText.print1stHeader()
    connected = connect.connect()

    if connect :
        cliText.printCommandHeader()
        while True :
            text = input(">")
            interpretCommand.interpret(text)



if __name__ == "__main__":
    main()
