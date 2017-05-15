import time
import RPi.GPIO as GPIO
import Font
import signal
import Adafruit_DHT as dht

from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional #, LCD_FONT, CP437_FONT, SINCLAIR_FONT, TINY_FONT
from luma.core import legacy

#Constants
CLOCK = "CLOCK"
TEMP = "TEMP"

#
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=4, block_orientation=-90)

#
contrast = 25
mode = CLOCK
humidity = 50
temperature = 22


#
GPIO.setmode(GPIO.BCM)  

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def button_Pressed(channel):  
	global mode

	print "button pressed : "
	print channel  
	
	if mode == CLOCK:
		mode = TEMP
	elif mode == TEMP:
		mode = CLOCK



def get_Temp(signum, frame):
	global humidity
	global temperature

	humidity ,temperature = dht.read_retry(dht.DHT22, 4)

try:
	signal.signal(signal.SIGALRM, get_Temp)
	signal.setitimer(signal.ITIMER_REAL,45)

	GPIO.add_event_detect(24, GPIO.FALLING, callback=button_Pressed)
	GPIO.add_event_detect(23, GPIO.FALLING, callback=button_Pressed)	

	while True:

		device.contrast(contrast)


		year = time.strftime("%Y") 
		month = time.strftime("%m")
		day = time.strftime("%d")
		hours = time.strftime("%H")
		minutes = time.strftime("%M")
		seconds = int(time.strftime("%S"))
	
		if mode == CLOCK:

			if (seconds % 2) == 1:
				aff = hours + ":" + minutes
			else:
				aff = hours + ":" + minutes
		
		elif mode == TEMP:
			
			aff = str(temperature) + " C"


		with canvas(device) as draw:
			legacy.text(draw, (1, 1), aff, fill="white", font=proportional(Font.BIGFONT))
		


except KeyboardInterrupt:  
	GPIO.cleanup()       # clean up GPIO on CTRL+C exit  

GPIO.cleanup()           # clean up GPIO on normal exit  
