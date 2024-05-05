import lcd_color #still buggy
import subprocess
import grovepi
import time
import sound
from flask import Flask, render_template, request, jsonify
import sys
import threading
import RPi.GPIO
import jhd1802 # another lcd library
import log

led_state = "ON"
led = 5
app = Flask(__name__)
threshold_value = 1500
sensor_values = [0,0,0,0,0]
def log_on():
    while True:
        time.sleep(1)
        log.write_to_csv('dino.csv',sum(sensor_values))
def sensor_on():
    while True:
        time.sleep(0.2)
        s = sound.get_sensor_value()
        sensor_values.append(s)
        sensor_values.pop(0)

def lcd_update():
        global led_state
        if get_noise_level() > threshold_value and led_state == "OFF":
            led_state = "ON"
            lcd.setCursor(0,0)
            lcd.write("Shhhhhhh")
        if get_noise_level() < threshold_value and led_state == "ON":
            lcd.setCursor(0,0)
            lcd.write("Love you")
            led_state = "OFF"

def lcd_on(): 
    lcd.write("DK DINO ON")
    time.sleep(2)
    lcd.clear()
    while True:
        time.sleep(0.1)
        lcd_update()
        
def led_on():
    while True:
        time.sleep(1)
        l = get_led_state()
        if l == "OFF":
            grovepi.analogWrite(led,0)
        else:
            grovepi.analogWrite(led,250)
def lcd_light_on():
    lcd_color.setRGB(255)
    time.sleep(3)
    while True:
        time.sleep(1)
        l = get_led_state()
        if l == "OFF":
            lcd_color.setRGB(0)
        else:
            lcd_color.setRGB(255)

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

def get_led_state():
    global threshold_value
    noise_level = get_noise_level()
    if noise_level > threshold_value:
        return "ON"
    if noise_level < threshold_value:
        return "OFF"
    return "ON"
@app.route('/update_led_state')
def update_led_state():
    s = get_led_state()
    return jsonify({'led_status': s})

if __name__ == '__main__':
    lcd = jhd1802.JHD1802()
    lcd.clear()
    subprocess.call("ls", shell=True)
    thread1 = threading.Thread(target=sensor_on)
    thread1.daemon = True
    thread1.start()
    thread2 = threading.Thread(target=lcd_on)
    thread2.daemon = True
    thread2.start()
    thread3 = threading.Thread(target=led_on)
    thread3.daemon = True
    thread3.start()
    thread4 = threading.Thread(target=lcd_light_on)
    thread4.daemon = True
    thread4.start()
    thread5 = threading.Thread(target=log_on)
    thread5.daemon = True
    thread5.start()

    app.run(debug=True, host='0.0.0.0')


