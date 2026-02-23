import cliText
import connect

def main():
    cliText.print1stHeader()
    connected = connect.connect()

    if connect :
        cliText.printCommandHeader()
        text = input(">")
        


if __name__ == "__main__":
    main()
