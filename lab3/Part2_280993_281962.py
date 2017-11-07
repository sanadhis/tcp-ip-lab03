import socket
import sys

# Bind socket and establish the TCP connection to given server
HOST = "tcpip.epfl.ch"
PORT = 5003
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))

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
sock.sendall(message.encode())

# Handle the response
while True:
    try:
        data = sock.recv(msg_size).decode()
        if data:
            counter +=1
            print ('received:', data)
        else:
            break
    except:
        print("No message received!")
        
# Show recv() invocations
print("recv() called: ",counter)
print("\nclosing socket")
sock.close()