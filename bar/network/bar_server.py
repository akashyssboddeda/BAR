import os
import time
import socket
import sys
import urllib2
import sqlite3 as lite
from twisted.internet import defer, reactor
from twisted.internet.protocol import ServerFactory, ClientFactory, Protocol
from twisted.protocols.basic import LineReceiver, NetstringReceiver
from twisted.protocols import basic

clients = []

class BARServerProtocol(NetstringReceiver):

    def connectionMade(self):
        clients.append(self)
        self.sendString("=== BAR Server ===")

    def stringReceived(self, data):
        if data[:9] == "BROADCAST":
            self.broadcast(data)
        elif data[:4] == "QUIT":    
            self.close_connection()
        else:
            self.sendString("I can break rules too.")

    def broadcast(self, data):
        if len(data) <= 11:
            self.sendString("Ok, but where's the message to broadcast?")
        else:
            message = data[10:]
	    print "Starting broadcast from: " + self.transport.getPeer().host
            for client in clients:
		if self.transport.getPeer().host != client.transport.getPeer().host:
                	client.sendString(message)
            self.sendString("OK")

    def close_connection(self):
        self.transport.loseConnection()
 
    def connectionLost(self, reason):
        clients.remove(self)

class BARServerFactory(ServerFactory):
    protocol = BARServerProtocol

def server_main():
    factory = BARServerFactory()
    port = reactor.listenTCP(231, factory,
                             #interface=socket.gethostbyaddr(socket.gethostbyname(socket.gethostname()))[2][0])
                            interface=urllib2.urlopen('http://ip.42.pl/raw').read())
    print 'Serving on %s.' % (port.getHost())
    reactor.run()

if __name__ == '__main__':
    server_main()
