import time
import grovepi

sensor = 0

grovepi.pinMode(sensor,"INPUT")

def get_sensor_value():
    try:
        value = 65535
        while value > 60000:
            value = grovepi.analogRead(sensor)
        return value
    except IOError:
        print("ioerror")
        return "Error"
