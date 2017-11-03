from websocket import create_connection

# Set websocket server and port
HOST = "tcpip.epfl.ch"
PORT = "5006"

# Init connection
ws = create_connection("ws://"+HOST+":"+PORT)

#d = input("enter d: ")
#message = "CMD_short:"+d
message = "CMD_floodme"

# Send the message
print("sending:", message)
ws.send(message)

# To count how many invocations of recv()
counter=0

# Handle the response
while True:
    try:
        result =  ws.recv().decode()        
        if result:
            counter+=1            
            print ('received:', result)
        else:
            break
    except:
        print("No message received!")

# Show recv() invocations
print("recv() called: ",counter)
print("\nclosing socket")
ws.close()