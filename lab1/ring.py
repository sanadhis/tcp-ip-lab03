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
    # ex: python ring.py 10
    nodes = int(sys.argv[1])
    
    "Create an empty network and add nodes to it."
    net = Mininet()
    info( '*** Adding controller\n' )
    net.addController( 'c0' )

    PC = []
    SWITCH = []

    info( '*** Adding first PC\n' )
    firstPC = net.addHost ("PC1")

    info( '*** Adding first switch\n' )    
    firstSwitch = net.addSwitch("s1")

    net.addLink( firstPC, firstSwitch )

    PC.append(firstPC)
    SWITCH.append(firstSwitch)
    
    for i in range(2,nodes+1):
        currPC = "PC" + str(i)
        IP = "10.10." + str(i-1) + ".2/24"      
        info( '*** Adding hosts\n' )
        host = net.addHost( currPC, ip=IP )
        
        info( '*** Adding switch\n')
        currSwitch = "s" + str(i)
        switch = net.addSwitch ( currSwitch )
        
        #getting previous PC
        prevSwitch = SWITCH[-1]

        info( '*** Creating links\n' )
        net.addLink( host, prevSwitch )
        net.addLink( host, switch )

        PC.append(host)
        SWITCH.append(switch)

    lastSwitch = SWITCH[-1]
    net.addLink(PC[0],lastSwitch)

    info( '*** Starting network\n')
    net.start()                
    
    for idx,host in enumerate(PC):
        IPleftInt = "10.10."+str(idx)+".2/24" 
        IPrightInt = "10.10."+str(idx+1)+".1/24"
        defaultForward = "10.10."+str(idx+1)+".2"

        info("*** Assigning Ipv4")
        host.cmd("ip address add "+ IPleftInt +" dev PC"+str(idx+1)+"-eth0")
        host.cmd("ip address add "+ IPrightInt +" dev PC"+str(idx+1)+"-eth1")
        host.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
        host.cmd("ip route add default via "+defaultForward)
    
    firstPC.cmd("ip addr flush dev PC1-eth0")
    firstPC.cmd("ip address add 10.10.1.1/24 dev PC1-eth0")
    firstPC.cmd("ip addr flush dev PC1-eth1")
    firstPC.cmd("ip address add 10.10."+str(nodes)+".2/24 dev PC1-eth1")
    firstPC.cmd("ip route add default via 10.10.1.2")

    "This is used to run commands on the hosts"

    info( '*** Starting xterm on hosts\n' )
    firstPC.cmd('xterm -xrm \'XTerm.vt100.allowTitleOps: false\' -T PC1 &')

    info( '*** Running the command line interface\n' )
    CLI( net )
	
    info( '*** Closing the terminals on the hosts\n' )
    firstPC.cmd("killall xterm")
	
    info( '*** Stopping network' )
    net.stop()

"main Function: This is called when the Python file is run"
if __name__ == '__main__':
    setLogLevel( 'info' )
    firstNetwork()
