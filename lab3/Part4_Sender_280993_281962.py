import socket
import struct

# Set the target multicast address and port
multicast_group = ("224.1.1.1", 5005)

# Get Scipher Number and 300 bytes message by input
msg_prefix = input('Enter your Scipher Number: ')
text       = (input("Enter your message(300 char only): "))[:300]

# Convert the message with schiper number to bytes
text_b     = (msg_prefix+text).encode()

# Create the datagram socket with timeout 1s
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(1)

# Configure socket multicast TTL to 1 in order to make packets stay in local network segment
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

try:
    print("sending:", text_b)
    sent = sock.sendto(text_b, multicast_group)

    # Look for responses from all recipients
    while True:
        print('waiting to receive')
        try:
            data, server = sock.recvfrom(16)
        except socket.timeout:
            print('timed out, no more responses')
            break
        else:
            print('received "%s" from %s' % (data, server))

finally:
    print("\nclosing socket")
    sock.close()