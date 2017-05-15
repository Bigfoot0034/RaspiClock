# RaspiClock

Hey ! I'm new...

Work In Progress

## Hardware

### What do you need
  - Raspberry Pi Zero W
  - ...

### Wirering
  - ...

## Installation

### Raspbian

Update & Upgrade your system if necessary :
```
sudo apt-get update && sudo apt-get upgrade -y
```

### Libraries

#### Luma.LED_Matrix
https://github.com/rm-hull/luma.led_matrix

```
sudo usermod -a -G spi,gpio pi
sudo apt-get install python-dev python-pip libfreetype6-dev libjpeg-dev
sudo -i pip install --upgrade pip setuptools
sudo -H pip install --upgrade luma.led_matrix
```
Source & more instructions : http://luma-led-matrix.readthedocs.io/en/latest/install.html#installing-from-pypi


#### Adafruit Python DHT Sensor Library
https://github.com/adafruit/Adafruit_Python_DHT

```
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
sudo apt-get install build-essential python-dev
sudo python setup.py install
```
Source & more instruction : http://www.rototron.info/dht22-tutorial-for-raspberry-pi/


## RaspiClock
https://github.com/Bigfoot0034/RaspiClock

```
git clone https://github.com/Bigfoot0034/RaspiClock
```

## Sources
http://raspi.tv/2013/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-2
http://effbot.org/zone/stupid-exceptions-keyboardinterrupt.htm
http://www.rototron.info/dht22-tutorial-for-raspberry-pi/
http://luma-led-matrix.readthedocs.io/en/latest/install.html#installing-from-pypi
