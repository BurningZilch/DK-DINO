from picamera import PiCamera
from time import sleep

c = PiCamera()

c.start_preview()
sleep(5)
c.capture('/home/pi/Desktop/hi.jpg')
c.stop_preview()
