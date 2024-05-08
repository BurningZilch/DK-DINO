import time
import grovepi

pin = 7


grovepi.pinMode(pin,"OUTPUT")
# test colors used in grovepi.chainableRgbLed_test()
testColorBlack = 0   # 0b000 #000000
testColorBlue = 1    # 0b001 #0000FF
testColorGreen = 2   # 0b010 #00FF00
testColorCyan = 3    # 0b011 #00FFFF
testColorRed = 4     # 0b100 #FF0000
testColorMagenta = 5 # 0b101 #FF00FF
testColorYellow = 6  # 0b110 #FFFF00
testColorWhite = 7   # 0b111 #FFFFFF
# patterns used in grovepi.chainableRgbLed_pattern()
thisLedOnly = 0
allLedsExceptThis = 1
thisLedAndInwards = 2
thisLedAndOutwards = 3

def init(numleds):
    grovepi.chainableRgbLed_init(pin, numleds)
    time.sleep(.5)

def set_color(color,num):
    grovepi.storeColor(color)
    time.sleep(.5)
    grovepi.chainableRgbLed_pattern(pin, thisLedOnly,0)
