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

# Menu
CLOCK = "CLOCK"
TEMP = "TEMPERATURE"
HUM = "HUMIDITY"
ALARM = "ALARM"
CONT = "CONTRAST"
 
mode = CLOCK
menu_tab = [CLOCK, TEMP, HUM, ALARM, CONT]
menu_selected = 0
MAX_MENU = 4

# Contrast settings
contrast = 1
contrast_tab = [1, 25, 50, 100, 200]
contrast_selected = 0
MAX_CONTRAST = 4

# Panel settings
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=4, block_orientation=-90)

# Initialisation
humidity = 50
temperature = 22
alarm_state = False

# GPIO settings
NEXT = 23
PREVIOUS = 24
SELECT = 14

GPIO.setmode(GPIO.BCM)  
GPIO.setup(NEXT, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(PREVIOUS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SELECT, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# Handle button
def button_Pressed(channel):  
	global mode
	global menu_selected
	global contrast
	global contrast_selected 
	global alarm_state

	print "button pressed : " + str(channel)

	if channel == NEXT:
		if menu_selected >= MAX_MENU:
			menu_selected = 0
		else:
			menu_selected = menu_selected + 1
	elif channel == PREVIOUS:
		if menu_selected <= 0:
			menu_selected = MAX_MENU
		else:
			menu_selected = menu_selected - 1
	elif channel == SELECT: 
		if mode == CONT:
			if contrast_selected >= MAX_CONTRAST:
				contrast_selected = 0
			else:
				contrast_selected = contrast_selected + 1
		elif mode == ALARM:
			if alarm_state:
				alarm_state = False
			else:
				alarm_state = True
 
	contrast = contrast_tab[contrast_selected]
	mode = menu_tab[menu_selected]	

# Mesure Temperature & Humidity
def get_Temp(signum, frame):
	global humidity
	global temperature

	humidity ,temperature = dht.read_retry(dht.DHT22, 4)

	signal.setitimer(signal.ITIMER_REAL, 45)
	

# Main 
try:
	signal.signal(signal.SIGALRM, get_Temp)
	signal.setitimer(signal.ITIMER_REAL, 4)

	GPIO.add_event_detect(NEXT, GPIO.FALLING, callback=button_Pressed)
	GPIO.add_event_detect(PREVIOUS, GPIO.FALLING, callback=button_Pressed)	
	GPIO.add_event_detect(SELECT, GPIO.FALLING, callback=button_Pressed)

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
			aff = str(temperature)[0:4] + "C"

		elif mode == HUM:
			aff = str(humidity)[0:4] + "%"
			
		elif mode == ALARM:
			if alarm_state == True:
				aff = "A:ON"
			else:
				aff = "A:OFF"

		elif mode == CONT:
			aff = "*" + str(contrast)


		with canvas(device) as draw:
			legacy.text(draw, (1, 1), aff, fill="white", font=proportional(Font.BIGFONT))
		
	GPIO.cleanup()

except KeyboardInterrupt:  
	GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
 
