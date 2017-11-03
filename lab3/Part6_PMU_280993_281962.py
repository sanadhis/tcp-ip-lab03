import socket
import ssl
from time import sleep
import string
from random import randint, choice

# TLS Server properties
HOST       = ""
PORT       = 5069
max_client = 5

# TLS Identities
cert_file = "280993_cert.pem"
key_file  = "280993_key.pem"

# Create TCP socket over ipv4 and bind it to given port and address. Set maximum number of concurrent connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST,PORT))
sock.listen(max_client)

# To give random response
allchar = string.ascii_letters + string.digits

# To give short response with delay of d s
def response_short(ssl_sock, d):
    for i in range(8):
        msg = "PMU data "+ str(i)
        ssl_sock.send(msg.encode())
        sleep(d)

# To give flood response
def response_flood(ssl_sock):
    # method to create random string of 20000 bytes
    msg = "".join(choice(allchar) for x in range(20000))
    print(msg)
    ssl_sock.send(msg.encode())

# Main Function goes here
if __name__ == "__main__":
    # Loop forever until keyboard interrupt
    while True:
        # Accept a connection
        newsocket, source_addr = sock.accept()
        # form a ssl socket for the connection with version of SSLv23
        ssl_socket             = ssl.wrap_socket(newsocket, 
                                                server_side=True, 
                                                certfile=cert_file,
                                                ssl_version=ssl.PROTOCOL_SSLv23,
                                                keyfile=key_file)
        try:
            # handle request based on given keyword
            data    = ssl_socket.recv().decode()
            data    = data.split(":")            
            command = data[0]

            # give appropriate responses
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
            # Close SSL connection after handling request and send response
            ssl_socket.shutdown(socket.SHUT_RDWR)
            ssl_socket.close()
