import socket
import struct

# Bind socket for UDP connection with ipv4
HOST = ''  
PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

# Multicast address, convert to 32 bit binary format
MCAST_GRP  = "224.1.1.1"
group      = socket.inet_aton(MCAST_GRP)

# set option socket.INADDR_ANY, so any given interface in machine will listen to this multicast address
mreq = struct.pack('4sL', group, socket.INADDR_ANY)

# set IP_ADD_MEMBERSHIP option to make OS chose the default interface to join multicast group
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Handle the receiving process
while True:
    try:
        data = sock.recv(1024)
        if data:
            # Skip first 6 bytes
            print(data[6:].decode())
    except KeyboardInterrupt:
        break
    except:
        print("No message received!")

print("\nclosing socket")
sock.close()