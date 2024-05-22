import time
import grovepi

pin = 3
numleds = 3

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

s = 8
def init():
    grovepi.chainableRgbLed_init(pin, numleds)
    time.sleep(.5)

def set_color(i,num):
    if i == 1:
        color = [0, 0, 255]  # Blue
    elif i == 2:
        color = [0, 255, 0]  # Green
    elif i == 3:
        color = [0, 255, 255]  # Cyan
    elif i == 4:
        color = [255, 0, 0]  # Red
    elif i == 5:
        color = [255, 0, 255]  # Magenta
    elif i == 6:
        color = [255, 255, 0]  # Yellow
    elif i == 7:
        color = [255, 255, 255]  # White
    elif i == 8: #orange
        color = [255,75,0]
    else:
        color = [0, 0, 0]  # Black (default)  
    grovepi.storeColor(color[0],color[1],color[2])
    time.sleep(.5)
    grovepi.chainableRgbLed_pattern(pin, 0,num)
def set_all(color):
    grovepi.chainableRgbLed_test(pin, numleds, color)
    time.sleep(.5)
if __name__ == '__main__':
    while s >= 0:
        set_all(s)
        s = s - 1
        time.sleep(1)
        if s == 0:
            s = 8
