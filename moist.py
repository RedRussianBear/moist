import time
import mysql.connector
import RPi.GPIO as GPIO

#GPIO Pin number constants
pins = {
	'pump': 1,
	'valve': 2,
	'mode': 3,
	'scale': 4
}


def timestamp():
	return time.strftime('%Y-%m-%d %H:%M:%S')

# Read binary data from USB scale, extract weight
def getWeight(dev="/dev/usb/hidraw0"):
	weight = -1
	try:
		f = open(dev, 'rb')
		
		# Read data from USB device and treat as 4 bytes and 1 short
		format = "BBBBH"
		numbytes = struct.calcsize(format)
		binaryData = struct.unpack(format, f.read(numbytes))
		
		# Retrieve final section of data (unsigned short), which is the weight in grams
		weight = binaryData[4]
	except OSError as e:
		print("{0} - Failed to read from USB device".format(timestamp()))
	return weight

# Emulates a measurement mode change button press
def toggleMode():
	GPIO.out(pins['mode'], GPIO.LOW)
	time.sleep(0.0625)
	GPIO.out(pins['mode'], GPIO.HIGH)

# Emulates a poweron button press
def powerScale():
	GPIO.out(pins['scale'], GPIO.LOW)
	time.sleep(0.0625)
	GPIO.out(pins['scale'], GPIO.HIGH)

def drainDevice():
	
	
	# Drain water from the scale
	GPIO.out(pins['valve'], GPIO.LOW)
	GPIO.out(pins['pump'], GPIO.LOW)
	time.sleep(10)
	GPIO.out(pins['valve'], GPIO.HIGH)
	GPIO.out(pins['pump'], GPIO.HIGH)
	
	# Keep the scale awake
	toggleMode()
	toggleMode()

def scaleSetup():
	# Set up GPIO relay controls
	GPIO.setmode(GPIO.BCM)
	for key in pins:
		GPIO.setup(pins[key], GPIO.OUT)
	
	# Turn on the scale
	powerScale()
	
	# Toggle mode to grams
	toggleMode()

	
def sqlSetup():
	#mySQL config

# Main method
if __name__ == "__main__":
	scaleSetup()
	
	GPIO.cleanup()
	