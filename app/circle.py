import spidev 
import time 
import os 
import RPi.GPIO as GPIO
import board 
import adafruit_dht 

rele_pin = 21
global is_rele_on
is_rele_on = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(rele_pin, GPIO.OUT)

dhtDevice = adafruit_dht.DHT11(board.D4, use_pulseio=False) 

spi = spidev.SpiDev() 
spi.open(0,0) 
spi.max_speed_hz=1000000 

temperature_c = 0
temperature_f = 0
humidity1 = 0

def translate(value, leftMin, leftMax, rightMin, rightMax):
		leftSpan = leftMax - leftMin
		rightSpan = rightMax - rightMin
		valueScaled = float(value - leftMin) / float(leftSpan)
		return rightMin + (valueScaled * rightSpan)


def lampOnOff(a):
	if a == True:
		GPIO.output(rele_pin, GPIO.HIGH)
	else:
		GPIO.output(rele_pin, GPIO.LOW)
def dataRead():
	try:
		# Print the values to the serial port
		global temperature_c
		temperature_c = dhtDevice.temperature
		# temperature_f = temperature_c * (9 / 5) + 32
		global humidity1
		humidity1 = dhtDevice.humidity
		#print(
		#    "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
		#	temperature_f, temperature_c, humidity1
		#    )
		#)
 
	except RuntimeError as error:
		# Errors happen fairly often, DHT's are hard to read, just keep going
		# print(error.args[0])
		time.sleep(2.0)
		# continue
	except Exception as error:
		# print('Error!')
		dhtDevice.exit()
		raise error
        
	lighting = translate(analogEingang(0), 0, 1023, 100, 0)
	humidity2 = translate(analogEingang(1), 0, 1023, 100, 0)
	# GPIO.output(rele_pin, GPIO.HIGH)
	data = {
		'title' : 'Monitoring...',
		'humidity' : str(humidity1)+' %',
		'temp' : str(temperature_c)+' C*',
		'lighting' : lighting,
		'soilMoistrue' : str("%.2f" % humidity2)+' %'
	}
	return data
	
	
def analogEingang(channel):
	adc = spi.xfer2([1,(8+channel)<<4,0])
	data = ((adc[1]&3) << 8) + adc[2]
	return data

while True:
	time.sleep(0.2)
	data = dataRead()
	if int(data.get('lighting')//1) > 80:
		lampOnOff(False)
	else:
		lampOnOff(True)
