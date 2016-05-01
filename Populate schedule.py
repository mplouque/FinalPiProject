##################################################################################
# Name: Matthew, Abhi, Kayla, Brock, Pablo
# Date: April 27, 2016
# Description: Generates a csv file using random ports from 1026-9999 and then a message of length 4-8 to correspond with it
# USED FOR CYBER STORM 2016
##################################################################################
from random import *
import csv
from random import randint

outputFile = open('schedule.csv', 'w')
outputWriter = csv.writer(outputFile)

outputWriter.writerow(['iterationNumber', 'portNumber1', 'message1', 'portNumber2', 'message2', 'ledcontroller'])
count = 0
letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
#makes each character in the letters string into an index of an array
letters.split
ledControl = 0
#creates a list from 1026 to 9999
portList = range(1026,10000)
#print portList
print len(portList)

#iterate through x times
#x is half the number of available ports from 1026-9999
for i in range(0, 4487):
	#able to use portList
    global portList
    #count goes up
    count += 1
    #assign ledControl either a 0 or a 1, randomly
    ledControl = randint(0,1)
    
    #randomly pick a portNumber by a random element in the portList
    portNum = portList[randint(0, len(portList)-1)]
    #remove that element so that the same port can not be picked twice
    portList.remove(portNum)
    #do the same again for the second port
    portNum2 = portList[randint(0,len(portList)-1)]
    portList.remove(portNum2)

    print len(portList)
    #initialize the blank messages
    message = ''
    message2 = ''
    #make the message from length 4 to 8
    for i in range(0, randint(4,8)):
    	#fill the message with random characters from the letters list
        message += letters[randint(0,len(letters)-1)]
    	message2 +=letters[randint(0,len(letters)-1)]
    #write this line to the csv file, with the iteration, portNum, and message for each pi
    outputWriter.writerow([count, portNum, message, portNum2, message2, ledControl])
    #^rinse and repeat 



    
    




