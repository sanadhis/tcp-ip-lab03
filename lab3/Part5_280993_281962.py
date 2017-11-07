from websocket import create_connection
import sys

# Set websocket server and port
HOST = "tcpip.epfl.ch"
PORT = "5006"

# Init connection
ws = create_connection("ws://"+HOST+":"+PORT)

# Take input from command-line
message = str(sys.argv[1])

# We set msg_size = 18 to handle lines easily for short message
if message.startswith("CMD_short"):
    msg_size = 18
# For flood scenario we want the application to receive up to 1024 bytes at once from the socket
elif message.startswith("CMD_floodme"):
    msg_size = 1024   

# Send the message
print("sending:", message)
ws.send(message)

# To count how many invocations of recv()
counter=0

# Handle the response
while True:
    try:
        result =  ws.recv()        
        if result:
            counter+=1            
            print ('received:', result.decode())
        else:
            break
    except:
        print("No message received!")

# Show recv() invocations
print("recv() called: ",counter)
print("\nclosing socket")
ws.close()