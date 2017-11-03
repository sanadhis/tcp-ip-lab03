import socket
import datetime
from socket import timeout
from time import sleep

# Set fixed CMU server and message
HOST    = "lab3.iew.epfl.ch"
PORT    = 5004
message = "RESET:20"

# Connet with IPv4 Socket with timeout 3 s
sock_ipv4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_ipv4.connect((HOST,PORT))
sock_ipv4.settimeout(3)

# Connect with IPv6 Socket with timeout 3 s
sock_ipv6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
sock_ipv6.connect((HOST,PORT))
sock_ipv6.settimeout(3)

# Init empty var
reply        = ""
response_msg = ""

# Ask user for the number of acknowledgement of reset request
n_times   = int(input("Enter number of iteration: "))

# For final statistics, compute every number of packets loss before getting actual result
l_packets = []

# Iterate as number of n_times
for i in range(n_times):
    # Init counter as zero, var counter keep track of the number of packets send
    counter = 0
    while True:
        # For each attempt of sending packets, increment counter
        counter += 1
        print("Waiting for reply iteration-"+str(counter))
        print("sending:", message)

        try:
            # Sending Part, try with ipv4        
            sock_ipv4.sendall(message.encode())
            print("try to sent with ipv4")   
            # Wait 1 second for ack                         
            sleep(1)            
            reply = sock_ipv4.recv(10)  
        # catch exception if ipv4 is refused
        except ConnectionRefusedError as err:
            # Sending Part, try with ipv6                    
            sock_ipv6.sendall(message.encode())
            print("try to sent with ipv6")            
            # Wait 1 second for ack        
            sleep(1)            
            reply = sock_ipv6.recv(10)      
        except timeout as err:
            print("Timeout: No response, try sending again!")
            continue
        finally:
            # Check if there is a reply or or not            
            if reply:
                response_msg = reply.decode() 
                break
            else:
                print("Sigh, no response the server is so mean to me!")  

    # Add the number of packets loss per iteration
    l_packets.append(counter)
    # Print response from CMU
    print("\nResponse: ",response_msg)
    # Print the now date and timestamp
    print(str(datetime.datetime.now()).split('.')[0]+"\n")

### Display Summary ###
total_packets    = sum(l_packets)
avg_packets      = total_packets/n_times
loss_probability = (total_packets-n_times)/total_packets

print("############# SUMMARY #################")
print("Avg Packets Before Ack: " + str(avg_packets))
print("Loss Probability: " + str(loss_probability))
