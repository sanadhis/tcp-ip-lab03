import socket
import struct

HOST = ''  
PORT = 5005

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))

MCAST_GRP  = "224.1.1.1"
group      = socket.inet_aton(MCAST_GRP)

# socket.INADDR_ANY = For any given interface
mreq = struct.pack('4sL', group, socket.INADDR_ANY)

# Option to make OS chose default interface to join multicast group
s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
    data = s.recv(1024)
    if data:
        print(data[6:].decode())