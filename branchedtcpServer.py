import socket
import threading
import time
import csv
# need to come up with a way to definitively determine who won the competition(see line 70 (may try writing to a file for permanent solution))


# change to match number of potential connections from cyberstorm students
ABSOLUTE_MAX_NUMBER_OF_CONNECTIONS = 5

# start with 1 because the header row of the CSV file is index 0
ITERATION = 1
 
# change to actual assigned IP on day of cyberstorm
bind_ip = "127.0.0.1"
# initial starting port
bind_port = 9991
# number of seconds before control to PI toggles
TIME_INTERVAL = 10.0


# will need to store csv files into an array and use the matching index of iteration with the matching row in the csv file
# read the file and interact with it as an object
fileObject = open('schedule.csv', 'r')
# change the file structure to csv so we can interact with it more easily
csvReader = csv.reader(fileObject)
# create an array of all the rows in the file
ARRAY = [ row for row in csvReader ]
#print ARRAY

class Server(object):
    def __init__(self, bind_ip, bind_port):
        self.ip = bind_ip
        self.port = bind_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message = 'Good morning'
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
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
        
        # self.socket.close()           # another error
        # or try
        # self.socket.shutdown(socket.SHUT_RDWR)  # no help
        
        # rebind the server to a new port
        self.bind()
        # allow server to resetup it's listening functionality
        self.listen(ABSOLUTE_MAX_NUMBER_OF_CONNECTIONS)
        
    # server can accept connections
    def acceptConnection(self):
        self.socket.accept()

    # client-handling thread
    def handle_client(self, client_socket, address):
        # print out what the client sends
        request = client_socket.recv(1024)
        print "[*] Received: %s" % request
        
        if str(request).lower() == self.message.lower():
            # send back congratulations message!
            client_socket.send("Sayanora!")
            # show us where the winning connection came from 
            print "[*****] Winning connection from %s:%d" % (address[0], address[1])
            # turn on led for the associated pi
            
        else:
            # send back a packet with the correct iteration number
            client_socket.send("iteration " + str(ITERATION))
            
        # close the connection 
        client_socket.close()
    
    def specialmainloop(self):
        # user friendly information (will have issues with two server threads printing at same time... look into boundedSemaphores)
        print "[*] Listening on %s:%d" % (self.ip, self.port)
        # bind the server to its port and ip address 
        self.bind()
        # allow server to listen to connections
        self.listen(ABSOLUTE_MAX_NUMBER_OF_CONNECTIONS)


        global startime
        # TRY TO TAKE OUT, BUT CODE FAILS...
        starttime= time.time()
        while True:
            
            if ( (time.time() - starttime) % TIME_INTERVAL) == 0:
                # change the port on the server(takes care of rebinding and re-listening)
                # self.changePort(6987)
                
                # change message of the server (example of the final code)
                self.message = 'changed code'
                #self.message= ARRAY[ITERATION][2]
                
                # increment the global variable 
                global ITERATION
                ITERATION += 1
                
                # indicate the changed portS!
                print "NEW PORT [*] Listening on %s:%d" % (self.ip, self.port)
                # transfer control of the LEDs
                    # option 1) switch control every k*TIME_INTERVAL
                    # option 2) switch control depending on the message --> more secure and reliable
                    
                # set startime to current time (essentially back to zero)
                starttime = time.time()
            else:
                
                # return value is a tuple(client is a socket object, address is the address of the client socket)
                client, addr  = self.socket.accept()
                # fails to work... NOT SURE WHY!
                #client, addr = self.acceptConnection()
                
                # show us where the connection came from 
                print "[*] Accepted connection from %s:%d" % (addr[0], addr[1])
                
                # spin up our client thread to handle incoming data
                client_handler = threading.Thread(target=self.handle_client, args=(client,addr))
                
                # start the thread
                client_handler.start()
    
    
    def mainloop(self):
        # user friendly information (will have issues with two server threads printing at same time... look into boundedSemaphores)
        print "[*] Listening on %s:%d" % (self.ip, self.port)
        # bind the server to its port and ip address 
        self.bind()
        # allow server to listen to connections
        self.listen(ABSOLUTE_MAX_NUMBER_OF_CONNECTIONS)


        global startime
        # TRY TO TAKE OUT, BUT CODE FAILS...
        starttime= time.time()
        while True:
            
            if ( (time.time() - starttime) % TIME_INTERVAL) == 0:
                # change the port on the server(takes care of rebinding and re-listening)
                # self.changePort(6987)
                
                # change message of the server (example of the final code)
                self.message = 'changed code'
                #self.message= ARRAY[ITERATION][2]

                
                # indicate the changed portS!
                print "NEW PORT [*] Listening on %s:%d" % (self.ip, self.port)
                # transfer control of the LEDs
                    # option 1) switch control every k*TIME_INTERVAL
                    # option 2) switch control depending on the message --> more secure and reliable
                    
                # set startime to current time (essentially back to zero)
                starttime = time.time()
            else:
                
                # return value is a tuple(client is a socket object, address is the address of the client socket)
                client, addr  = self.socket.accept()
                # fails to work... NOT SURE WHY!
                #client, addr = self.acceptConnection()
                
                # show us where the connection came from 
                print "[*] Accepted connection from %s:%d" % (addr[0], addr[1])
                
                # spin up our client thread to handle incoming data
                client_handler = threading.Thread(target=self.handle_client, args=(client,addr))
                
                # start the thread
                client_handler.start()

   
starttime = time.time()

server1 = Server(bind_ip, bind_port)
#server1.mainloop()     # test case to see if just one server works
client_handler1 = threading.Thread(target=server1.specialmainloop)
client_handler1.start()

server2 = Server(bind_ip, 1501)
client_handler2 = threading.Thread(target=server2.mainloop)
client_handler2.start()

# NOTE port numbers must be greater than 1023 if not using sudo privileges
