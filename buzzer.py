import time 
import grovepi
import RPi.GPIO as GPIO
import smbus
buzzer = 25 
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer,GPIO.OUT)

def buzz(frequency, length,buzzer_pin):     #create the function "buzz" and feed it the pitch and duration)

    if(frequency==0):
        time.sleep(length)
        return
    period = 1.0 / frequency             #in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
    delayValue = period / 2              #calcuate the time for half of the wave
    numCycles = int(length * frequency)  #the number of waves to produce is the duration times the frequency

    for i in range(numCycles):          #start a loop from 0 to the variable "cycles" calculated above
        GPIO.output(buzzer_pin, True)    #set pin 27 to high
        time.sleep(delayValue)          #wait with pin 27 high
        GPIO.output(buzzer_pin, False)          #set pin 27 to low
        time.sleep(delayValue)          #wait with pin 27 low

buzz(500, 0.3,buzzer)
buzz(300, 0.2,buzzer)
GPIO.cleanup()
