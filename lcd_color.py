import time,sys

if sys.platform == 'uwp':
    import winrt_smbus as smbus
    bus = smbus.SMBus(1)
else:
    import smbus
    import RPi.GPIO as GPIO
    rev = GPIO.RPI_REVISION
    if rev == 2 or rev == 3:
        bus = smbus.SMBus(1)
    else:
        bus = smbus.SMBus(0)

# this device has two I2C addresses
DISPLAY_RGB_ADDR = 0x62
DISPLAY_TEXT_ADDR = 0x3e

# set backlight to (R,G,B) (values from 0..255 for each)
def setRGB(r):
   # bus.write_byte_data(DISPLAY_RGB_ADDR,0,0)
   # bus.write_byte_data(DISPLAY_RGB_ADDR,1,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,0x08,0xaa)
    


    bus.write_byte_data(DISPLAY_RGB_ADDR,4,r)
def main():
    import time
    setRGB(0)
    time.sleep(1)
    setRGB(200)
    time.sleep(1)
if __name__ == '__main__':
    while True:
        main()
