import subprocess
import re
import qrcode
from PIL import Image

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
        result = subprocess.check_output(["iwgetid", "-r"])
        ssid = result.strip()
        print(ssid)
        return ssid
    except subprocess.CalledProcessError as e:
        print("Failed to get SSID: ", e)
        return None

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

