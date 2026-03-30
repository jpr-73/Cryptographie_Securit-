
import socket
import sys
import time
import fonctions
import main


class Client:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, bytes_per_char = 4) :
        self.buffer_bytes = b""

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
            while True :
                answer = self.sock.recv(4096)
                if not answer :
                    print("Server disconnected")
                    sys.stdout.flush()
                    break
                

                self.buffer_bytes += answer
                stream = self.buffer_bytes.decode("latin-1", errors="replace")

                

                if "ISCs" in stream:
                    start_index = self.buffer_bytes.find(b"ISCs")
                    if len(self.buffer_bytes) < start_index + 6:
                        continue
                    
                    len_bytes = self.buffer_bytes[start_index+4 : start_index+6]
                    msg_len = int.from_bytes(len_bytes, byteorder='big')
                    data_len = start_index + 6 + (msg_len * 4)

                    if len(self.buffer_bytes) < data_len:
                        continue
                    
                    data = self.buffer_bytes[start_index + 6 : data_len]

                    raw_octets = bytes([data[i+3] for i in range(0, len(data), 4)])

                    try :
                        clean_text = raw_octets.decode('utf-8')
                    except :
                        clean_text = raw_octets.decode('latin-1')

                    int_text = []
                    for i in range(0, len(data), 4):
                        valeur_complete = int.from_bytes(data[i:i+4], byteorder='big')
                        int_text.append(valeur_complete)

                    clean_text = "".join([chr(x) for x in int_text])

                    sys.stdout.write(f"\r\033[K[SERVER]: {clean_text}\n> ")
                    sys.stdout.write(f"\r\033[K[SERVER]: {int_text}\n> ")
                    
                    buff1 = main.buff1
                    buff1.content = clean_text
                    buff1.int_content = int_text
                    sys.stdout.flush()
                    self.buffer_bytes = self.buffer_bytes[data_len:]


                elif "ISCt" in stream :
                    sys.stdout.write(f"\r\033[K[MSG]: {stream}\n> ")
                    sys.stdout.flush()
                    self.buffer_bytes = b""
                    

        except socket.timeout:
            print("Connection Time out")
            sys.stdout.flush()
        except Exception as e:
            print(f"Error : {e}")
            sys.stdout.flush()

    def close(self) :
        self.s.close()