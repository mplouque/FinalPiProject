import socket, threading, time, csv
import RPi.GPIO as GPIO

# initialize the output pins
pi0 = 17
pi1 = 27

GPIO.setmode(GPIO.BCM)

# setup the pins as output pins
GPIO.setup(pi0, GPIO.OUT)
GPIO.setup(pi1, GPIO.OUT)


# need to come up with a way to definitively determine who won the competition(see line 70 (may try writing to a file for permanent solution))

# change to match number of potential connections from cyberstorm students
ABSOLUTE_MAX_NUMBER_OF_CONNECTIONS = 5

# start with 1 because the header row of the CSV file is index 0
ITERATION = 1
 
# change to actual assigned IP on day of cyberstorm
bind_ip = "192.168.0.112"
# initial starting port
bind_port = 9991
# number of seconds before control to PI toggles
TIME_INTERVAL = 60.0

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
        self.message = 'Default message'
        # the SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    # server will listen to incoming connections
    def listen(self, maxNumberofConnections):
        self.socket.listen(maxNumberofConnections)
    
    def changeMessage(self, newMessage):
        # change server's message
        self.message = newMessage
        
    # server can accept connections
    def acceptConnection(self):
        self.socket.accept()

    # client-handling thread
    def handle_client(self, client_socket, address):
        # print out what the client sends
        request = client_socket.recv(1024)
        print "[*] Received: %s" % request
        
        # if correct message is not received
	print (str(request).lower() , self.message.lower())
 
        if str(request).lower().strip("\n") != self.message.lower():
            # send back a packet with the correct iteration number
            client_socket.send("iteration: " + str(ITERATION) + '\n')
	    GPIO.output(pi0, 0)
	    GPIO.output(pi1, 0)

        # Note: LED Logic (which server has control of the LED is handled by the Arduino Multiplexer)
        # pi 0 must be on
        elif (str(ARRAY[ITERATION][5]) == str(0)):
            # turn on pi 0
            GPIO.output(pi0, 1)
            GPIO.output(pi1, 0)
            # send back congratulations message!
            client_socket.send("Congrulations!")
            print "[*****] Winning connection from %s:%d" % (address[0], address[1])
	    GPIO.cleanup()
        # pi 1 must be on
        elif (str(ARRAY[ITERATION][5]) == str(1)):
            # turn on pi 0
            GPIO.output(pi1, 0)
            GPIO.output(pi0, 1)
            # send back congratulations message!
            client_socket.send("Congrulations!")
            print "[*****] Winning connection from %s:%d" % (address[0], address[1])
        # verify integrity of the if statements
        else:
            print "This should not happen"
            
	print (str(request).lower().strip("\n") == self.message.lower().strip())

        # always close the connection 
        client_socket.close()
    
    # function that the server instance loops through
    def mainloop(self):
        
        # user friendly information (will have issues with two server threads printing at same time... look into boundedSemaphores)
        print "[*] Listening on %s:%d" % (self.ip, int(self.port))
        
        addressInUse = True 
        # ensures that if the timing doesn't line up exactly, the thread will wait until the addressInUse is released and then start its mainloop
        while addressInUse:
                
            try:
                # server will bind itself to its ip and port numbers
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.socket.bind((self.ip, self.port))
                
                # allow server to listen to connections
                self.listen(ABSOLUTE_MAX_NUMBER_OF_CONNECTIONS)
                addressInUse = False 
            except:
                # skip back to the loop
                pass
            

        # loop to handle client requests
        while True: 
            
            try:
                # ensures that 1 second before the port change, the socket times out, which allows the thread to end
                self.socket.settimeout(TIME_INTERVAL-1) 
                
                # return value is a tuple(client is a socket object, address is the address of the client socket)
                client, addr  = self.socket.accept()
                
                # show us where the connection came from 
                print "[*] Accepted connection from %s:%d" % (addr[0], addr[1])
                
                # spin up our client thread to handle incoming data
                client_handler = threading.Thread(target=self.handle_client, args=(client,addr))
                
                # start the thread
                client_handler.start()
            except:
                # exit the thread
                print "terminating thread\n"
                break

# initialize the time   
starttime = time.time()

# create the servers
server0 = Server(bind_ip, int(ARRAY[ITERATION][1]))
server1 = Server(bind_ip, int(ARRAY[ITERATION][3]))

# change the message of the server to the correct row in the csv file(array)
server0.changeMessage(str(ARRAY[ITERATION][2]))
server1.changeMessage(str(ARRAY[ITERATION][4]))
 

# create the threads
client_handler0 = threading.Thread(target=server0.mainloop)
client_handler0.start()
client_handler1 = threading.Thread(target=server1.mainloop)
client_handler1.start()

# NOTE port numbers must be greater than 1023 if not using sudo privileges

while True:
    
    if ( (time.time() - starttime) - TIME_INTERVAL) >= 0:
        # increment the global variable 
        ITERATION += 1
        
        # change port to a new value in list
        newPort0 = int(ARRAY[ITERATION][1])
        newPort1 = int(ARRAY[ITERATION][3])
        
        # resetup the starttime counter
        starttime = time.time()
        
        # recreate the server
        server0 = Server(bind_ip, newPort0)
        server1 = Server(bind_ip, newPort1)
        
        # change the message on the server
        server0.changeMessage(str(ARRAY[ITERATION][2]))
        server1.changeMessage(str(ARRAY[ITERATION][4]))
        
        # respawn the threads
        client_handler0 = threading.Thread(target=server0.mainloop)
        client_handler0.start()
        client_handler1 = threading.Thread(target=server1.mainloop)
        client_handler1.start()
        
         
        
# make sure to run GPIO.cleanup()
