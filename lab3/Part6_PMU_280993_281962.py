import socket
import ssl
from time import sleep
import string
from random import randint, choice

# Socket properties
HOST       = ""
PORT       = 5069
max_client = 5

# TLS Identities
cert_file = "280993_cert.pem"
key_file  = "280993_key.pem"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST,PORT))
sock.listen(max_client)

allchar = string.ascii_letters + string.punctuation + string.digits

def response_short(ssl_sock, d):
    for i in range(8):
        msg = "PMU data "+ str(i)
        ssl_sock.send(msg.encode())
        sleep(d)

def response_flood(ssl_sock):
    msg = "".join(choice(allchar) for x in range(20000))
    print(msg)
    ssl_sock.send(msg.encode())

if __name__ == "__main__":
    while True:
        newsocket, source_addr = sock.accept()
        ssl_socket             = ssl.wrap_socket(newsocket, 
                                                server_side=True, 
                                                certfile=cert_file,
                                                ssl_version=ssl.PROTOCOL_SSLv23,
                                                keyfile=key_file)
        try:
            # blocking socket
            data    = ssl_socket.recv().decode()
            data    = data.split(":")            
            command = data[0]

            if(command == "CMD_short"):
                response_short(ssl_socket, int(data[1]))
            elif (command == "CMD_floodme"):
                response_flood(ssl_socket)
            
            print(data)
        except KeyboardInterrupt:
            break
        except:
            print("")
        finally:
            ssl_socket.shutdown(socket.SHUT_RDWR)
            ssl_socket.close()
