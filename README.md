# Will update after this exam season
Our Project involved creating a dino-shaped noise monitor using python 2.7 a Raspberry Pi 4B with buster, a Grove Pi +, a grove oled display 1.12 v2.0, 3 grove chainable leds and a grove sound sensor. The device will notify the user by lights up after user have break their pre-set threshold via the local server through the web browser in same local network
# Headless Install Guide

1. Download and flash Buster system into a sd card from https://downloads.raspberrypi.org/raspios_armhf/images/raspios_armhf-2021-05-28/2021-05-07-raspios-buster-armhf.zip, remember setup the ssh for the pi
2. Copy and run this in the pi's terminal:
   sudo apt update -o APT::Get::List-Cleanup="0" -o APT::Get::Changelog="none" ; sudo apt upgrade -o APT::Get::Changelog="none" -y ; sudo apt install vim -y ; sudo pip install pycparser python-periphery tornado qrcode ; sudo curl -kL dexterindustries.com/update_grovepi | bash ;  cd ~ ; git clone https://github.com/Seeed-Studio/grove.py ; cd grove.py ; sudo ./install.sh ; cd ~ ; git clone https://github.com/BurningZilch/DK-DINO

4. cd DK-DINO ; python main.py
5. go to the raspberrypidk.local:5000 (change the address name to host name you give to your pi)
6. set qr.py running after the machine boot
![Screenshot 2024-05-18 144720](https://github.com/BurningZilch/DK-DINO/assets/55424397/9e184c40-e9a8-4270-bd81-55101db472bb)
![77A3DDDA-A5D0-4C1F-92CB-06EF9CA1E9CE](https://github.com/BurningZilch/DK-DINO/assets/55424397/2a92a36d-1388-4a4e-a0dd-d0c7f9b6267a)
![IMG_20240518_170019378](https://github.com/BurningZilch/DK-DINO/assets/55424397/d2fad827-cdc7-43c4-ae99-1ab6d0f69d37)

