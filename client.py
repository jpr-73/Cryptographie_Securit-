
import socket
import sys
import time
import fonctions


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
        self.sock.send(message)
    
    def receive(self, timeout = 10.00) :
        try :
            rcvd = ""
            #self.sock.settimeout(timeout)
            while True :
                answer = self.sock.recv(4096)
                if not answer :
                    print("Server disconnected")
                    sys.stdout.flush()
                else :
                    
                    rcvd += (answer).decode()
                    if rcvd[:4] == "ISCt" :
                        sys.stdout.write(f"\r\033[K[Message reçu]: {rcvd[4:]}\n> ")
                        sys.stdout.flush()
                        rcvd = ""
                        
                        


        except socket.timeout:
            print("Connection Time out")
            sys.stdout.flush()
        except Exception as e:
            print(f"Error : {e}")
            sys.stdout.flush()

    def close(self) :
        self.s.close()