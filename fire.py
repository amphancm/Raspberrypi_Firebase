
import RPi.GPIO as GPIO
from time import sleep
import datetime
from firebase import firebase
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import urllib2, urllib, httplib
import json
import os 
from functools import partial

GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

firebase = firebase.FirebaseApplication('https://YOUR-FIREBASE-URL.firebaseio.com', None)
#firebase.put("/Control", "/device1", "on")

def updatePiInfo():
	result = firebase.get('/Control', '/device1')
	print result
	
	if ( result == "on" ): 	  	
		#disp.clear()
		#disp.display()
		draw.rectangle((0,0,width,height), outline=0, fill=0)				
		draw.text((x, top),    ' FireBase',  font=font, fill=255)
		draw.text((x+20, top+16), ' ON', font=font42, fill=255)
		disp.image(image)
		disp.display()	
		print "Lights on" 
		GPIO.output(18,GPIO.HIGH)
	else :
		if ( result == "off" ):
			print "Lights off"
			GPIO.output(18,GPIO.LOW)
			draw.rectangle((0,0,width,height), outline=0, fill=0)
			#disp.clear()
			#disp.display()		
			draw.text((x, top),    ' FireBase',  font=font, fill=255)
			draw.text((x, top+16), ' OFF', font=font42, fill=255)
			disp.image(image)
			disp.display()


# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Note you can change the I2C address by passing an i2c_address parameter like:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)


# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = 2
shape_width = 20
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = padding


# Load default font.
font = ImageFont.load_default()
font10 = ImageFont.truetype('Minecraftia.ttf', 10)
font20 = ImageFont.truetype('Minecraftia.ttf', 20)
font42 = ImageFont.truetype('Minecraftia.ttf', 42)

# Write two lines of text.
draw.text((x, top),    ' FireBase',  font=font, fill=255)
draw.text((x, top+20), 'CONTROL', font=font20, fill=255)

# Display image.
disp.image(image)
disp.display()

#firebase.post("/Control/device1", "off")
firebase.put("/Control", "/device1", "off")

while True:
	updatePiInfo()
	#firebase.put("/Control", "/device1", "off")
		
        #Retrieve sleep time from firebase and continue the loop
        #sleepTime = firebase.get("/Settings/info_update_time_interval", None)
        #sleepTime = int(sleepTime)
	sleep(1)
	








