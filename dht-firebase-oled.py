
import RPi.GPIO as GPIO
from time import sleep
import datetime
from firebase import firebase
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import Adafruit_DHT

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

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensor = Adafruit_DHT.DHT11

# Example using a Beaglebone Black with DHT sensor
# connected to pin P8_11.
pin = 4


# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)


firebase = firebase.FirebaseApplication('https://YOUR_FIREBASE_URL.firebaseio.com/', None)


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
font18 = ImageFont.truetype('Minecraftia.ttf', 18)
font20 = ImageFont.truetype('Minecraftia.ttf', 20)
font42 = ImageFont.truetype('Minecraftia.ttf', 42)

# Write two lines of text.
draw.text((x, top),    'Raspberry Pi',  font=font, fill=255)
draw.text((x, top+20), 'Firebase', font=font20, fill=255)

# Display image.
disp.image(image)
disp.display()

#firebase.put("/dht", "/temp", "0.00")
#firebase.put("/dht", "/humidity", "0.00")

def update_firebase():

	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	if humidity is not None and temperature is not None:
		sleep(5)
		str_temp = ' {0:0.2f} *C '.format(temperature)	
		str_hum  = ' {0:0.2f} %'.format(humidity)
		print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))	
		draw.rectangle((0,0,width,height), outline=0, fill=0)
		#disp.clear()
		#disp.display()		
		draw.text((3, top),    'Temperature/Humidity',  font=font, fill=255)
		draw.text((x, top+16), str_temp, font=font18, fill=255)
		draw.text((x, top+36), str_hum, font=font18, fill=255)
		disp.image(image)
		disp.display()	
	else:
		print('Failed to get reading. Try again!')	
		sleep(10)

	data = {"temp": temperature, "humidity": humidity}
	firebase.post('/sensor/dht', data)
	

while True:
		update_firebase()
		
        #sleepTime = int(sleepTime)
		sleep(5)
	








