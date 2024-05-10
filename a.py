import random
import servo
import led
from oled import SH1107G_SSD1327
import jhd1802
import time
import lcd_color
import sound
import time
from flask import Flask, render_template, request, jsonify
import sys
import RPi.GPIO
import log
import subprocess
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop, PeriodicCallback

app = Flask(__name__)
threshold_value = 1500
sensor_values = [0,0,0,0,0]
led_state = "ON"
led_state2 = "ON"
led_state3 = "ON"
last_led_state = "ON"
numleds = 3
oled_screen = SH1107G_SSD1327()
oled_refresh = 0
current_hand = 0

def log_on():
    log.write_to_csv('dino.csv',sum(sensor_values), led_state)
@app.route('/')
def index():
    return render_template('index.html', threshold=threshold_value)

@app.route('/', methods=['POST'])
def set_threshold():
    global threshold_value
    threshold_value = int(request.form['threshold'])
    return jsonify({'success': True})

def get_noise_level():
    return sum(sensor_values)

@app.route('/get_noise_level')
def get_noise_level_route():
    noise_level = get_noise_level()
    return jsonify({'noise_level': noise_level})
@app.route('/t')
def t():
    return render_template('test.html')

def get_led_state(t):
    noise_level = get_noise_level()
    if (noise_level > t):
        return "ON"
    if noise_level < t:
        return "OFF"
    return "ON"
@app.route('/update_led_state')
def update_led_state():
    s = get_led_state(threshold_value)
    return jsonify({'led_status': s})


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
    s = sound.get_sensor_value()
    sensor_values.append(s)
    sensor_values.pop(0)
    print(sum(sensor_values))

def led_state_update():
    global led_state
    global led_state2
    global led_state3
    led_state = get_led_state(threshold_value)
    led_state2 = get_led_state(threshold_value + 200)
    led_state3 = get_led_state(threshold_value + 400)

def led_control():
    i = 0
    if led_state == "ON":
        led.set_color(6,0)
    else:
        led.set_color(0,0)
    if led_state2 == "ON":
        led.set_color(8,1)
    else:
        led.set_color(0,1)
    if led_state3 == "ON":
        led.set_color(4,2)
    else:
        led.set_color(0,2)

    #    while i < numleds:
    #        led.set_color(random.randint(1,7),i)
    #        i = i + 1

def lcd_update():
    pass
  #  lcd.setCursor(0,0)
  #  lcd.write("disco dino!!")
  #  lcd.setCursor(1,0)
  #  lcd.write(str(get_noise_level()))

def oled_update():
    global oled_refresh
    oled_screen.setCursor(0,0)
    oled_screen.write("Disco Dino!!")
    oled_screen.setCursor(rows - 1, 0)
    oled_screen.write('noise value :'+str(sum(sensor_values)))
    oled_refresh = oled_refresh + 1 
    oled_screen.setCursor(rows - 5, 0)
    oled_screen.write('threshold :'  +str(threshold_value))

def lcd_light():
    pass
  #  if led_state == "ON":
  #      lcd_color.setRGB(255)
  #  else:
  #      lcd_color.setRGB(0)

def bonk():
    global current_hand
    if led_state =="ON" and current_hand == 0:
        hand.setAngle(90)
        current_hand = 90 
    else:
        current_hand = current_hand - 10 
        hand.setAngle(current_hand)

if __name__ == '__main__':
    hand = servo.GroveServo(25)
    led.init()
    oled_screen.clear()
    oled_screen.backlight(True)
    rows, cols = oled_screen.size()
#    lcd = jhd1802.JHD1802()
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000, address='0.0.0.0')  # Listen on all available network interfaces
    callback_sensor = PeriodicCallback(sensor_on, 200)  # 1000 milliseconds = 1 second
    callback_sensor.start() # 0 delay
    callback_log = PeriodicCallback(log_on, 2000)  # 1000 milliseconds = 1 second
    callback_log.start() # 0 delay
    callback_led_state = PeriodicCallback(led_state_update, 1000)  # 1000 milliseconds = 1 second
    callback_led_state.start() # 0 delay
    callback_led_control = PeriodicCallback(led_control, 2000)  # 1000 milliseconds = 1 second
    callback_led_control.start()
    callback_oled = PeriodicCallback(oled_update,2000)
    callback_oled.start()
    callback_lcd = PeriodicCallback(lcd_update,2000)
#    callback_lcd.start()
    callback_lcdr = PeriodicCallback(lcd_light,2000)
    callback_lcdr.start()
    callback_bonk = PeriodicCallback(bonk,1000)
#    callback_bonk.start()



    IOLoop.instance().start()

