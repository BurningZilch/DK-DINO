# This is still in develop, please wait for update
Our Project involved creating a dino-shaped noise monitor using python 2.7 a Raspberry Pi 4B with buster, a Grove Pi +, a grove oled display 1.12 v2.0, 3 grove chainable leds and a grove sound sensor. The device will notify the user by lights up after user have break their pre-set threshold via the local server through the web browser in same local network
# Headless Install Guide
1. Download and flash Buster system into a sd card from https://downloads.raspberrypi.org/raspios_armhf/images/raspios_armhf-2021-05-28/2021-05-07-raspios-buster-armhf.zip, remember setup the ssh for the pi
2. SSH into the raspberry pi, enable vnc, i2c ...... update and upgrade the software ...... install vim ...... etc
3. sudo apt update ; sudo apt upgrade ; sudo apt install vim
4.  sudo pip install pycparser ; sudo pip install python-periphery ; sudo pip intall tornado ; sudo pip install qrcode 
5. sudo curl -kL dexterindustries.com/update_grovepi | bash
6. git clone https://github.com/DexterInd/GrovePi.git ; cd GrovePi ; cd Firmware ; sudo ./firmware_update.sh
7. git clone https://github.com/Seeed-Studio/grove.py ; cd grove.py ; sudo ./install.sh
8. git clone https://github.com/BurningZilch/DK-DINO
9. plug in oled into any i2c port, sound snesor in A0, chainable leds in D3
10. cd DK-DINO ; python main.py
11. go to the raspberrypidk.local:5000 (change the address name to host name you give to your pi)
12. set qr.py running after the machine boot
![Screenshot 2024-05-18 144720](https://github.com/BurningZilch/DK-DINO/assets/55424397/9e184c40-e9a8-4270-bd81-55101db472bb)
![77A3DDDA-A5D0-4C1F-92CB-06EF9CA1E9CE](https://github.com/BurningZilch/DK-DINO/assets/55424397/2a92a36d-1388-4a4e-a0dd-d0c7f9b6267a)
![IMG_20240518_170019378](https://github.com/BurningZilch/DK-DINO/assets/55424397/d2fad827-cdc7-43c4-ae99-1ab6d0f69d37)

