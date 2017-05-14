import time

import Font

from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional #, LCD_FONT, CP437_FONT, SINCLAIR_FONT, TINY_FONT
from luma.core import legacy


serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=4, block_orientation=-90)

contrast = 25

while True:

	device.contrast(contrast)

	hour = time.strftime("%H")
	minutes = time.strftime("%M")
	aff = hour + ":" + minutes

	with canvas(device) as draw:
		legacy.text(draw, (1, 1), aff, fill="white", font=proportional(Font.BIGFONT))

