import socket
import threading
import time

# change to match number of potential connections from cyberstorm students
ABSOLUTE_MAX_NUMBER_OF_CONNECTIONS = 5

# start with 0 because we are in computer science class :)
ITERATION = 0
 
# change to actual assigned IP on day of cyberstorm
bind_ip = "127.0.0.1"
# initial starting port
bind_port = 9991
# number of seconds before control to PI toggles
TIME_INTERVAL = 30

class Server(object):
    def __init__(self, bind_ip, bind_port):
        self.ip = bind_ip
        self.port = bind_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        
    # server will listen to incoming connections
    def listen(self, maxNumberofConnections):
        self.socket.listen(maxNumberofConnections)
    
    # server will bind itself to its ip and port numbers
    def bind(self):
        self.socket.bind((self.ip, self.port))
    
    # server will change port 
    def changePort(self, bind_port):
        # change server's port number
        self.port = bind_port
        # rebind the server to a new port
        self.bind()
        # allow server to resetup it's listening functionality
        self.listen(ABSOLUTE_MAX_NUMBER_OF_CONNECTIONS)
        
        

    # server can accept connections
    def acceptConnection(self):
        self.socket.accept()

    # client-handling thread
    def handle_client(self, client_socket):
        # print out what the client sends
        request = client_socket.recv(1024)
        print "[*] Received: %s" % request
        
        # send back a packet with the correct iteration number
        client_socket.send("iteration " + str(ITERATION))
        # close the connection 
        client_socket.close()
    

    def mainloop(self):
        # user friendly information (will have issues with two server threads printing at same time... look into boundedSemaphores)
        print "[*] Listening on %s:%d" % (self.ip, self.port)
        # bind the server to its port and ip address 
        self.bind()
        # allow server to listen to connections
        self.listen(ABSOLUTE_MAX_NUMBER_OF_CONNECTIONS)
        while True:
            # return value is a tuple(client is a socket object, address is the address of the client socket)
            client, addr  = self.socket.accept()
            # fails to work... NOT SURE WHY!
            #client, addr = self.acceptConnection()
            
            # show us where the connection came from 
            print "[*] Accepted connection from %s:%d" % (addr[0], addr[1])
            
            # spin up our client thread to handle incoming data
            client_handler = threading.Thread(target=self.handle_client, args=(client,))
            
            # start the thread
            client_handler.start()
            

server1 = Server(bind_ip, bind_port)
#server1.mainloop()     # test case to see if just one server works
client_handler1 = threading.Thread(target=server1.mainloop)
client_handler1.start()

server2 = Server(bind_ip, 1501)
client_handler2 = threading.Thread(target=server2.mainloop)
client_handler2.start()

# NOTE port numbers must be greater than 1023 if not using sudo privileges

starttime=time.time()

# runs every 'time_interval' seconds
    # option 1) destroy the thread and recreate the thread every Z seconds
    # option 2) 
if ((time.time() - starttime) % TIME_INTERVAL):
    # change the port on the server
    
    # change message of the server
    
    # increment the global variable 
    ITERATION += 1
    # transfer control of the LEDs
        # option 1) switch control every k*TIME_INTERVAL
        # option 2) switch control depending on the message --> more secure and reliable
    # set startime to current time (essentially back to zero)
    starttime = time.time()