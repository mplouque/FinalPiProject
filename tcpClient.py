# code acts as a cyberstorm hacker trying to connect to the raspberry pis

import socket

target_host = "127.0.0.1"         # raspberry pi 1
target_port = 9991              # raspberry pi 1 port

class Client(object):
    def __init__(self):
        # not useful instance variables right now (may use later?)
        #self.tgtHost = None
        #self.tgtPort = None
        # assign a socket to each client instance
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connectTo(self, target_host, target_port):
        # target host or target port is undefined
        if not(target_host or target_port) :
            print "You forget to enter a valid target_host IP address and Port number"
        else:
            self.socket.connect((target_host, target_port))
            print "connection Success"
            
    # send data to the server
    def send(self, data):
        self.socket.send(data)
    
    # receive data from the server
    def receive(self, numberOfBytes):
        print self.socket.recv(numberOfBytes)


client1 = Client()
client1.connectTo(target_host, 9051)
client1.send("test1")
client1.receive(1024)


client2 = Client()
client2.connectTo(target_host, 9489)
client2.send("hello universe")
client2.receive(1024)