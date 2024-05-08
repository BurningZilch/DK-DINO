import time
import grovepi

pin = 7
numleds = 2

grovepi.pinMode(pin,"OUTPUT")
# test colors used in grovepi.chainableRgbLed_test()
Black = 0   # 0b000 #000000
Blue = 1    # 0b001 #0000FF
Green = 2   # 0b010 #00FF00
Cyan = 3    # 0b011 #00FFFF
Red = 4     # 0b100 #FF0000
Magenta = 5 # 0b101 #FF00FF
Yellow = 6  # 0b110 #FFFF00
White = 7   # 0b111 #FFFFFF
# patterns used in grovepi.chainableRgbLed_pattern()
thisLedOnly = 0
allLedsExceptThis = 1
thisLedAndInwards = 2
thisLedAndOutwards = 3

i = 7
def init(numleds):
    grovepi.chainableRgbLed_init(pin, numleds)
    time.sleep(.5)

def set_color(color,num):
    grovepi.storeColor(color)
    time.sleep(.5)
    grovepi.chainableRgbLed_pattern(pin, thisLedOnly,0)
def set_all(color):
    grovepi.chainableRgbLed_test(pin, numleds, color)
    time.sleep(1)
if __name__ == '__main__':
    while i >= 0:
        set_all(i)
        i = i - 1
        time.sleep(1)
