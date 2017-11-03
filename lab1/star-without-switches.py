#!/usr/bin/python

"""
This example shows how to create a Mininet object and add nodes to it manually.
"""
"Importing Libraries"
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import sys

"Function definition: This is called from the main function"
def firstNetwork():
    # takes input param to dynamically create the topology with desired N nodes
    # ex: python star-without-switches.py 2
    nodes = int(sys.argv[1])
    
    "Create an empty network and add nodes to it."
    net = Mininet()
    info( '*** Adding controller\n' )
    net.addController( 'c0' )

    PC = []

    info( '*** Adding center PC\n' )
    center_router = net.addHost ("PC0",ip="10.10.1.2/24")
    
    for i in range(1,nodes+1):
        currPC = "PC" + str(i)
        IP = "10.10." + str(i) + ".1/24"      
        
        info( '*** Adding hosts\n' )
        host = net.addHost( currPC, ip=IP )

        info( '*** Creating links\n' )
        net.addLink( center_router, host )

        PC.append(host)

    info( '*** Starting network\n')
    net.start()                

    center_router.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")    
    
    for idx,pc in enumerate(PC):
        IP_router_interface = "10.10."+str(idx+1)+".2/24"
        IP_default = "10.10."+str(idx+1)+".2"        

        info("*** Assigning Ipv4")
        info("ip address add "+ IP_router_interface +" dev PC0-eth"+str(idx))
        center_router.cmd("ip address add "+ IP_router_interface +" dev PC0-eth"+str(idx))

        info("*** Assigning Default Route")
        pc.cmd("ip route add default via "+ IP_default)
    
    "This is used to run commands on the hosts"

    info( '*** Starting xterm on hosts\n' )
    center_router.cmd('xterm -xrm \'XTerm.vt100.allowTitleOps: false\' -T PC0 &')

    info( '*** Running the command line interface\n' )
    CLI( net )
	
    info( '*** Closing the terminals on the hosts\n' )
    center_router.cmd("killall xterm")
	
    info( '*** Stopping network' )
    net.stop()

"main Function: This is called when the Python file is run"
if __name__ == '__main__':
    setLogLevel( 'info' )
    firstNetwork()
