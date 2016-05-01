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

count = 0
letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
letters.split
ledControl = 0
portList = range(1026,10000)
#print portList
print len(portList)
outputWriter.writerow(['iterationNumber', 'portNumber1', 'message1', 'portNumber2', 'message2', 'ledControl'])

for i in range(0, 4487):
    global portList
    count += 1
    ledControl = randint(0,1)
    #portNum =(randint(1025, 10000))

    portNum = portList[randint(0, len(portList)-1)]
    portList.remove(portNum)
    portNum2 = portList[randint(0,len(portList)-1)]
    portList.remove(portNum2)

    print len(portList)
    message = ''
    message2 = ''

    for i in range(0, randint(4,8)):
        message += letters[randint(0,len(letters)-1)]
    	message2 +=letters[randint(0,len(letters)-1)]
    outputWriter.writerow([count, portNum, message, portNum2, message2, ledControl])



    
    




