import subprocess
import time
import re
import qrcode
from PIL import Image
import oled
import canva_oled
import numpy as np

matrixs = np.zeros((128,128))
last_matrixs = np.zeros((128,128))

def convert_to_bw_and_resize(input_image_path, output_image_path, target_size):
    # Open the input image
    image = Image.open(input_image_path)

    # Convert to black and white (grayscale)
    bw_image = image.convert("L")
    bw_image = bw_image.point(lambda x: 255 -x, mode='1')

    # Resize to the target size (128x128)
    resized_image = bw_image.resize(target_size, Image.ANTIALIAS)

    # Save as BMP
    resized_image.save(output_image_path, format="BMP")

def get_current_wifi_ssid():
    try:
        time.sleep(15) # wait for the machine to connect to wifi
        print('ok')
        result = subprocess.check_output(["iwgetid", "-r"])
        ssid = result.strip()
        print(ssid)
        return ssid
    except subprocess.CalledProcessError as e:
        print("Failed to get SSID: ", e)
        
        return get_current_wifi_ssid()

def run_shell_command(command):
    try:
        # Run the shell command and capture the output
        output = subprocess.check_output(command, shell=True)
        # Decode the output to a string (assuming UTF-8 encoding)
        output_str = output[5:]
        return output_str
    except subprocess.CalledProcessError as e:
        print("Error executing command: {e}" + str(e))
        return None

def get_wifi_password(ssid):
    try:
        # Execute the command and capture its output
        command_to_run = "sudo cat /etc/wpa_supplicant/wpa_supplicant.conf | grep psk"
        output = run_shell_command(command_to_run)
        # Decode the byte output to a string
        output_str = output.decode("utf-8")
        print(output_str)
        return output_str
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None

def generate_wifi_qr(ssid, security, password):
    security = security.upper()
    wifi_config = "WIFI:S:{};T:{};P:{};;".format(ssid, security, password)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(wifi_config)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("wifi_qr.png")

if __name__ == "__main__":
    a = oled.SH1107G_SSD1327()
    canva_oled.fullscreen_image('dk_dino_logo.bmp',matrixs)
    matrixs = np.zeros_like(matrixs)
    canva_oled.frame(a,matrixs,last_matrixs)
    print('what')
    ssid = get_current_wifi_ssid()
    if ssid is None:
        print("Could not determine the current Wi-Fi SSID.")
    else:
        security = 'WPA'  # Set the security type manually for testing purposes
        password = get_wifi_password(ssid) if security != 'nopass' else ''
        if security != 'nopass' and password is None:
            print("Could not determine the Wi-Fi password.")
        else:
            generate_wifi_qr(ssid, security, password)
            print("Wi-Fi QR code generated and saved as wifi_qr.png")
            convert_to_bw_and_resize('wifi_qr.png','wifi_qr.bmp',(128,128))
            a.backlight(False)
            time.sleep(1)
            a.backlight(True)
            canva_oled.fullscreen_image('/home/pi/DK-DINO/wifi_qr.bmp', matrixs)
            canva_oled.frame(a,matrixs,last_matrixs)
