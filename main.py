#Project by Aurélien Santi - Alexandre Raccurt - Gabriel Zeizer
import cliText
import interpretCommand
import client
import buffer
import gui
import socket
import threading
import os

host = "vlbeintrocrypto.hevs.ch"
port = 6000
ip = ""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#print(host, port)

client1 = client.Client()
buff1 = buffer.Buffer()

def setup_cli():
    working = True
    cliText.print1stHeader()

    connected = client1.connect(host, port)

    iListen = threading.Thread(target=client1.receive, daemon=True)
    iListen.start()

    cliText.printCommandHeader()
    while working:
        try :
            print()
            text = input(">")
            working = interpretCommand.interpret(text)
        except Exception as e:
            print(f"\n[!] Erreur : {e}")
            working = True
        

def main():
    # Run the console input loop in a background thread
    cli_thread = threading.Thread(target=setup_cli, daemon=True)
    cli_thread.start()

    # The Tkinter GUI must run on the main thread
    try:
        gui.root.mainloop()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear') #clear console
    main()