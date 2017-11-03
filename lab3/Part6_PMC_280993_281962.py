import socket
import ssl

# Socket properties
HOST = "localhost"
PORT = 5069

# TLS Identities
cert_file = "280993_cert.pem"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ssl_socket = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_SSLv23)

ssl_socket.connect((HOST,PORT))

# To count how many invocations of recv()
counter = 0

# Make sure user can choose scenarios
option      = int(input("Enter 1 for CMD_short and 2 for CMD_floodme: "))

# For scenario 1, ask user to input d
# We set msg_size = 18 to handle lines easily
if option == 1:
    d        = input("enter d: ")
    message  = "CMD_short:"+d
    msg_size = 18
# For scenario we want the application to receive up to 1024 bytes at once from the socket
else:
    message  = "CMD_floodme"
    msg_size = 1024    

# sending the message
print("sending:", message)
ssl_socket.send(message.encode())

# Handle the response
while True:
    data = ssl_socket.recv(msg_size).decode()
    if data:
        counter +=1
        print ('received:', data)
    else:
        break

# Show recv() invocations
print("recv() called: ",counter)