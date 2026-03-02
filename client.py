
import socket
import sys
import time
import fonctions
from fonctions import decode


class Client:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, bytes_per_char = 4) :
        None

    def connect(self, host, port) :
        print("[+] Connecting to " + host + " : " + str(port))
        try:
            ip = socket.gethostbyname('vlbelintrocrypto.hevs.ch')
            print("[+] Resolved server IP = " + ip)
        except socket.gaierror: 
            print ("[X] Connection impossible : There was an error resolving the host")
            sys.exit()

        try: 
            self.sock.connect((ip, port))
            print("[V] Connected successfully")
        except socket.gaierror: 
            print ("[X] Connection impossible : Host Unreachable")
            sys.exit()

        return True

    def send(self, message) :
        print("On essaie d'envoyer un truc")
        self.sock.send(message)
    
    def receive(self, timeout = 10.00) :
        try :
            print("test")
            #self.sock.settimeout(timeout)
            while True :
                answer = self.sock.recv(4)
                if not answer :
                    print("Server disconnected")
                else :
                    print("received = " + str(answer))
        except socket.timeout:
            print("Connection Time out")
        except Exception as e:
            print(f"Error : {e}")

    def close(self) :
        self.s.close()