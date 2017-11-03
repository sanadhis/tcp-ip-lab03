from websocket import create_connection

# Set websocket server and port
HOST = "tcpip.epfl.ch"
PORT = "5006"

# Init connection
ws = create_connection("ws://"+HOST+":"+PORT)

# Make sure user can choose scenarios
option      = int(input("Enter 1 for CMD_short and 2 for CMD_floodme: "))

# For scenario 1, ask user to input d
# We set msg_size = 18 to handle lines easily
if option == 1:
    d        = input("enter d: ")
    message  = "CMD_short:"+d
# For scenario we want the application to receive up to 1024 bytes at once from the socket
else:
    message  = "CMD_floodme"

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