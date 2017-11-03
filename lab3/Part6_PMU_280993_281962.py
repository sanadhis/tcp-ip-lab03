import socket
import ssl

# Socket properties
HOST = ""
PORT = 5069
max_client = 5

# TLS Identities
cert_file = "280993_cert.pem"
key_file  = "280993_key.pem"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST,PORT))
sock.listen(max_client)

while True:
    newsocket, source_addr = sock.accept()
    ssl_socket             = ssl.wrap_socket(newsocket, 
                                             server_side=True, 
                                             certfile=cert_file,
                                             keyfile=key_file)
    try:
        data = ssl_socket.recv()
        while data:
            try:
                data = ssl_socket.recv()
                print(data)
            except:
                break
    except:
        print()
    finally:
        ssl_socket.shutdown(socket.SHUT_RDWR)
        ssl_socket.close()
    
    print(source_addr)