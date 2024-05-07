import threading
import oled
import jhd1802
import time
import lcd_color
import sound
sensor_values = [0,0,0,0,0]
def lcd_on(): 
    lcd.clear()
    lcd.write("DK DINO ON")
    time.sleep(2)
    lcd.clear()
    i = 0
    while True:
        lcd.write(str(i))
        i = i + 1
        time.sleep(1)
        lcd.clear()
def oled_on():
    face = oled.SH1107G_SSD1327()
    face.backlight(False)
    time.sleep(1)
    face.backlight(True)
    rows, cols = face.size()
    print("after clear")
    i = 1
    while True:
        print("loop")
        face.setCursor(0, 0)
        print("what")
        face.write("DK is here")
        time.sleep(2)
        face.setCursor(rows - 1,0)
        face.write(str(i))
        i = i + 1
def lcd_light_on():
    lcd_color.setRGB(255)
    time.sleep(3)
    l = "OFF"
    while True:
        time.sleep(1)
        if l == "OFF":
            lcd_color.setRGB(0)
            l = "a"
        else:
            lcd_color.setRGB(255)
            l ="OFF"
def sensor_on():
    while True:
        time.sleep(0.2)
        s = sound.get_sensor_value()
        sensor_values.append(s)
        sensor_values.pop(0)
        print(sum(sensor_values))
thread7 = threading.Thread(target=sensor_on)
thread7.daemon = True
thread7.start()

#lcd = jhd1802.JHD1802()
#thread3 = threading.Thread(target=lcd_light_on)
#thread3.daemon = True
#thread3.start()
#thread2 = threading.Thread(target=lcd_on)
#thread2.daemon = True
#thread2.start()
thread6 = threading.Thread(target=oled_on)
thread6.daemon = True
thread6.start()
while True:
    time.sleep(10)
