# 拿來建立miniNet環境的腳本
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.term import makeTerm

def setup():
    net = Mininet(controller=RemoteController)

    info("Create controller.\n")
    c0 = net.addController('controller', ip='127.0.0.1', port=6633)

    info("Create switch node.\n")
    s1 = net.addSwitch('s1')

    info("Create host nodes.\n")
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')
    
    info("Create links.\n")
    net.addLink(s1, h1)
    net.addLink(s1, h2)
    net.addLink(s1, h3)
    
    c0.start()
    s1.start([c0])
    
    net.build()
    net.start()

    # net.terms.append(makeTerm(s1))
    CLI(net)

if __name__ == "__main__":
    setLogLevel('info')
    setup()