# SH1106-PiHole-Statistics
A Statistics Display for the SH1106 I2C Display


#Enable I2C Interface
sudo raspi-config --> Interfacing Options --> I2C --> Yes --> OK --> Yes
 

#Installing the dependencies 
sudo apt update
sudo apt upgrade

sudo apt-get install -y python3 python3-dev python-smbus i2c-tools python3-pil python3-pip python3-setuptools python3-rpi.gpio libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjp2-7 libtiff5 git python3-gpiozero python3-imaging
sudo -H pip3 install luma.oled
sudo usermod -a -G spi,gpio,i2c pi

#Downloading the fonts/scripts
sudo mkdir /stats
cd /stats 

sudo wget https://github.com/freddy2312/SH1106-PiHole-Statistics/blob/main/Raspi-Schrift.ttf?raw=true

sudo wget https://github.com/freddy2312/SH1106-PiHole-Statistics/blob/main/VCR_OSD_MONO_1.001.ttf?raw=true

sudo wget https://raw.githubusercontent.com/freddy2312/SH1106-PiHole-Statistics/main/stats.py

sudo wget https://raw.githubusercontent.com/freddy2312/SH1106-PiHole-Statistics/main/launcher.sh
 
sudo chmod 766 /stats/*

#Make it run at startup
sudo crontab –e

Add at the bottom:
@reboot /stats/launcher.sh > /stats/launcher.log 2>&1

