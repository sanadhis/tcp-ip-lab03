import socket
import ssl
import sys

# PMU Target Hostname and port
HOST = "localhost"
PORT = 5069

# Bind socket and establish the TLS connection with PMU
sock       = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_socket = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_SSLv23)
ssl_socket.connect((HOST,PORT))

# To count how many invocations of recv()
counter = 0

# Take input from command-line
message = str(sys.argv[1])

# We set msg_size = 18 to handle lines easily for short message
if message.startswith("CMD_short"):
    msg_size = 18
# For flood scenario we want the application to receive up to 1024 bytes at once from the socket
elif message.startswith("CMD_floodme"):
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
print("\nclosing socket")
ssl_socket.close()