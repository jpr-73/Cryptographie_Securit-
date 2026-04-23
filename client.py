
import socket
import sys
import main

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
            rcvd = b""
            #self.sock.settimeout(timeout)
            while True :
                answer = self.sock.recv(4096)
                if not answer :
                    print("Server disconnected")
                    sys.stdout.flush()
                    break
                else :
                    rcvd += answer
                    while len(rcvd) >= 6 :
                        if rcvd[:3] != b"ISC":
                            rcvd = rcvd[1:]
                            continue

                        length = int.from_bytes(rcvd[4:6], byteorder="big")

                        byte_length = length * 4
                        msg_length = byte_length + 6

                        if len(rcvd) < msg_length :
                            break

                        data = rcvd[6:msg_length]
                        value = []
                        clean_text = ""

                        for i in range(0, len(data), 4):
                            value.append(int.from_bytes(data[i:i+4], byteorder="big"))
                            #clean_text += chr(data[i+3])

                        raw_bytes2 = bytearray()
                        for val in value:
                            quatre_octets = val.to_bytes(4, byteorder="little")

                            raw_bytes2 += quatre_octets.replace(b'\x00', b'')

                        try :
                            #clean_text = bytes(value).decode("utf-8")
                            clean_text = raw_bytes2.decode("utf-8", errors="replace")

                        except :
                            print("problem with utf-8")
                            clean_text = "".join(chr(v) for v in value)

                        
                        type = "ISC" + rcvd[3:4].decode("latin-1", errors="replace")
                        
                        if type == "ISCt" :
                            sys.stdout.write(f"\r\033[K[MSG]: {clean_text}\n> ")
                        elif type == "ISCs" :
                            sys.stdout.write(f"\r\033[K[SERVER]: {clean_text}\n> ")
                            buff1 = main.buff1
                            buff1.set_content(clean_text)
                            buff1.set_ints(value)
                        else :
                            sys.stdout.write(f"\r\033[K[Bizarrerie]: {rcvd}\n> ")
                        
                        sys.stdout.flush()

                        rcvd = rcvd[msg_length:]

        except socket.timeout:
            print("Connection Time out")
            sys.stdout.flush()
        except Exception as e:
            print(f"Error : {e}")
            sys.stdout.flush()

    def close(self) :
        self.s.close()