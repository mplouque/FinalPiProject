import RPi.GPIO as GPIO
from time import sleep

# initialize the output pins
pi0 = 17
pi1 = 27

GPIO.setmode(GPIO.BCM)

# setup the pins as output pins
GPIO.setup(pi0, GPIO.OUT)
GPIO.setup(pi1, GPIO.OUT)

state0 = 0
state1 = 1
# turn on pi 1
GPIO.output(pi0, state0)
GPIO.output(pi1, state1)
sleep(2.0)
state0 = 1 - state0
state1 = 1 - state1


# give control to pi0
GPIO.output(pi0, state0)
GPIO.output(pi1, state1)
sleep(2.0)
state0 = 1 - state0
state1 = 1 - state1

# give control to pi1
GPIO.output(pi0, state0)
GPIO.output(pi1, state1)
sleep(2.0)
state0 = 1 - state0
state1 = 1 - state1

# give control to pi0
GPIO.output(pi0, state0)
GPIO.output(pi1, state1)
sleep(2.0)
state0 = 1 - state0
state1 = 1 - state1


GPIO.cleanup()
