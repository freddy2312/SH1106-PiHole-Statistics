#!/usr/bin/python3
from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, ws0010
from time import sleep
from gpiozero import CPUTemperature

# Standard libraries
import time
import math
import json
import requests
import subprocess

# Graphics libraries
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# GPIOZero functions for buttons and LEDs
from gpiozero import Button
from gpiozero import PWMLED

font = ImageFont.truetype('/home/admin/VCR_OSD_MONO_1.001.ttf',15)
font2 = ImageFont.truetype('/home/admin/VCR_OSD_MONO_1.001.ttf',40)
font3 = ImageFont.truetype('/home/admin/VCR_OSD_MONO_1.001.ttf',13)
font4 = ImageFont.truetype('/home/admin/VCR_OSD_MONO_1.001.ttf',11)
font5 = ImageFont.truetype('/home/admin/Raspi-Schrift.ttf',60)
# rev.1 users set port=0
# substitute spi(device=0, port=0) below if using that interface
# substitute bitbang_6800(RS=7, E=8, PINS=[25,24,23,27]) below if using that interface
serial = i2c(port=1, address=0x3C)

# substitute ssd1331(...) or sh1106(...) below if using that device
device = sh1106(serial)
width = 128
height = 64
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)

padding = 0
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="black", fill="black")
  #  draw.text((x, top), "test", fill="white")

mode=0
counter=1
zaehler=0
zaehler2=0
zaehler3=0
zaehler4=0

while True:
#Screen 1: Ads Percentage Today & Ads Today
    while zaehler < 10: #True:
# Get Pi-Hole data
         r = requests.get("http://localhost/admin/api.php?summary")

    # Scroll from right-hand side (x 128 to 0 in steps of 16)
         with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="black", fill="black")
    # Display large Pi-Hole ads blocked percentage
            draw.text((x, top-2),   "%s%%" % r.json()["ads_percentage_today"],  font=font2, fill="white")
            draw.text((x, top+34),   "ADs BLOCKED:", font=font, fill="white")
            draw.text((x, top+48),   "%s" % r.json()["ads_blocked_today"], font=font, fill="white")
         zaehler += 1
         sleep(1)

#Screen 2: IP, Ads Percentage, Ads Blocked, Queries     
    while zaehler2 < 10:    
        cmd = "hostname -I | cut -d\' \' -f1"
        IP = subprocess.check_output(cmd, shell = True )

        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="black", fill="black")
            draw.text((x, top), str(IP.decode('UTF-8')), font=font, fill="white")  
            draw.text((x, top+20),   "BLK: %s%%" % r.json()["ads_percentage_today"],  font=font3, fill="white")
            draw.text((x, top+34),   "ADS: %s" % r.json()["ads_blocked_today"], font=font3, fill="white")    
            draw.text((x, top+48),   "QRY: %s" % r.json()["dns_queries_today"], font=font3, fill="white")

        #draw.text((x, top), "test", fill="white")
        zaehler2 += 1
        sleep(1)

#Screen 3: Hardware info
    while zaehler3 < 10:
        cmd = "top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell = True )
        cmd = "free -m | awk 'NR==2{printf \"%s/%sMB\", $3,$2 }'"
        MemUsage = subprocess.check_output(cmd, shell = True )
        cmd = "df -h | awk '$NF==\"/\"{printf \"%d/%dGB\", $3,$2}'"
        Disk = subprocess.check_output(cmd, shell = True )
        cpu = CPUTemperature()

        with canvas(device) as draw:
            #draw.text((x, top),      str(IP.decode('UTF-8')),  font=font3, fill=255)
            draw.text((x, top),   "CPU: %s" % round(float(str(CPU.decode('UTF-8')))*10,2)+str("%"), font=font3, fill=255)
            draw.text((x, top+16),   "RAM: %s" % str(MemUsage.decode('UTF-8')), font=font3, fill=255)
            draw.text((x, top+32),   "USG: %s" % str(Disk.decode('UTF-8')),font=font3, fill=255)
            draw.text((x, top+48),   "TEMP: %s" % round(float(str(cpu.temperature)),1)+str("°C"), font=font3, fill=255)
     
        zaehler3 += 1
        sleep(1)

    while zaehler4 < 5:
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="black", fill="black")
            draw.text((x+40, top+2),   "B",  font=font5, fill=255)

        zaehler4 += 1
        sleep(1)

    zaehler=0
    zaehler2=0
    zaehler3=0
    zaehler4=0
