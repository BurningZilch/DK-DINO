import random
import led
import canva_oled
from oled import SH1107G_SSD1327
import time
import sound
import time
from flask import Flask, render_template, request, jsonify, send_from_directory
import sys
import RPi.GPIO
import log
import subprocess
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop, PeriodicCallback
from gpiozero import CPUTemperature
import numpy as np

canva = np.zeros((128,128))
last_canva = np.zeros((128,128))

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
threshold_value = 1000 
sensor_values = [0,0,0,0,0]
led_state = "ON"
led_state2 = "ON"
led_state3 = "ON"
last_led_state = "OFF"
last_led_state2 = "OFF"
last_led_state3 = "OFF"
numleds = 3
oled_screen = SH1107G_SSD1327()
def log_on():
    log.write_to_csv('uploads/dino.csv',sum(sensor_values), threshold_value)

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

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

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
    led_state2 = get_led_state(threshold_value + 0.2 * threshold_value)
    led_state3 = get_led_state(threshold_value + 0.4 * threshold_value)

def led_control():
    global last_led_state
    global last_led_state2
    global last_led_state3
    if led_state == "ON":
        if last_led_state == "OFF":
            led.set_color(6,0)
        last_led_state = "ON"
    else:
        if last_led_state == "ON":
            led.set_color(0,0)
        last_led_state = "OFF"
    if led_state2 == "ON":
        if last_led_state2 == "OFF":
            led.set_color(8,1)
        last_led_state2 = "ON"
    else:
        if last_led_state2 == "ON":
            led.set_color(0,1)
        last_led_state2 = "OFF"
    
    
    if led_state3 == "ON":
        if last_led_state3 == "OFF":
            led.set_color(4,2)
        last_led_state3 = "ON"
    else:
        if last_led_state3 == "ON":
            led.set_color(0,2)
        last_led_state3 = "OFF"
    

def oled_update():
    global canva
    c = get_noise_level()
    bar_height = remap(c,1000,2500, 1, 100)
    canva = np.roll(canva, -1, axis=0)
    canva_oled.line(127,127-bar_height,127,127,1,canva)
    canva_oled.write('noise: '+str(sum(sensor_values))+' ',0,0,1,canva)
    canva_oled.write('threshold: '+ str(threshold_value)+ ' ',0,1,1,canva)
    canva_oled.write(str(CPUTemperature())[-17:-1],0,2,1,canva)
    canva = np.rot90(canva)
    canva = np.rot90(canva)
    canva_oled.frame(oled_screen,canva,last_canva)
    canva = np.rot90(canva,k=-1)
    canva = np.rot90(canva,k=-1)

def remap(value, in_min, in_max, out_min, out_max):
    #TODO
    #by the way, should make a line chart instead of bar chart
   return random.randint(1,99) 
   

if __name__ == '__main__':
    led.init()
    oled_screen.clear()
    oled_screen.backlight(True)
    rows, cols = oled_screen.size()
    canva_oled.fullscreen_image('logo.bmp',canva)
    canva_oled.frame(oled_screen,canva, last_canva)
    time.sleep(3)
    canva = np.zeros_like(canva)
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000, address='0.0.0.0')  # Listen on all available network interfaces
    callback_sensor = PeriodicCallback(sensor_on, 200)  # 1000 milliseconds = 1 second
    callback_sensor.start() # 0 delay
    callback_log = PeriodicCallback(log_on, 2000)  # 1000 milliseconds = 1 second
    callback_log.start() # 0 delay
    callback_led_state = PeriodicCallback(led_state_update, 1000)  # 1000 milliseconds = 1 second
    callback_led_state.start() # 0 delay
    callback_led_control = PeriodicCallback(led_control, 500)  # 1000 milliseconds = 1 second
    callback_led_control.start()
    callback_oled = PeriodicCallback(oled_update,2000)
    callback_oled.start()

    IOLoop.instance().start()

