#DK-DINO
Welcome to DK-DINO, a project aimed at creating a dino-shaped noise monitoring device using a Raspberry Pi 4B, Python 2.7, and various Grove components. This device is designed to light up and notify users when noise levels exceed a predefined threshold.

#Features
Dino-shaped design for engaging interaction.
Noise monitoring using a Grove sound sensor.
Visual notifications through Grove chainable LEDs.
Web-based control for easy configuration within the local network.

#Installation
##Prerequisites
Raspberry Pi 4B with Buster OS
Grove Pi+ with associated sensors and LEDs
##Setup

1.Download and flash Buster system into a sd card from https://downloads.raspberrypi.org/raspios_armhf/images/raspios_armhf-2021-05-28/2021-05-07-raspios-buster-armhf.zip
2. Copy and run this in the pi's terminal:
   sudo apt update -o APT::Get::List-Cleanup="0" -o APT::Get::Changelog="none" ; sudo apt upgrade -o APT::Get::Changelog="none" -y ; sudo apt install vim -y ; sudo pip install pycparser python-periphery tornado qrcode ; sudo curl -kL dexterindustries.com/update_grovepi | bash ;  cd ~ ; git clone https://github.com/Seeed-Studio/grove.py ; cd grove.py ; sudo ./install.sh ; cd ~ ; git clone https://github.com/BurningZilch/DK-DINO
3. cd DK-DINO ; python main.py
4. go to the raspberrypidk.local:5000 on your phone or other device on local network (change the address name to host name you give to your pi)

#Note on Unfinished Features
Due to time constraints, some features were not fully implemented, and many functions are not yet called by main.py. We encourage you to explore the codebase and experiment with these functions with care. Your contributions and improvements are highly welcomed.

#Contributing
Feel free to fork this project, submit pull requests, or suggest new features that could enhance the DK-DINO experience.
#License
This project is dedicated to the public domain under the Unlicense. Feel free to use, modify, and distribute it as you wish.
![Screenshot 2024-05-18 144720](https://github.com/BurningZilch/DK-DINO/assets/55424397/9e184c40-e9a8-4270-bd81-55101db472bb)
![77A3DDDA-A5D0-4C1F-92CB-06EF9CA1E9CE](https://github.com/BurningZilch/DK-DINO/assets/55424397/2a92a36d-1388-4a4e-a0dd-d0c7f9b6267a)
![IMG_20240518_170019378](https://github.com/BurningZilch/DK-DINO/assets/55424397/d2fad827-cdc7-43c4-ae99-1ab6d0f69d37)

