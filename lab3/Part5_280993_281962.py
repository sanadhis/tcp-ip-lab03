from websocket import create_connection

HOST = "tcpip.epfl.ch"
PORT = "5006"

ws = create_connection("ws://"+HOST+":"+PORT)

#d = input("enter d: ")
#message = "CMD_short:"+d
message = "CMD_floodme"

print("sending:", message)
ws.send(message)

counter=0

while True:
    try:
        result =  ws.recv()        
        if result:
            print ('received:', result.decode())
            counter+=1
            print('invocation:',counter)
        else:
            break
    except:
        print()

ws.close()