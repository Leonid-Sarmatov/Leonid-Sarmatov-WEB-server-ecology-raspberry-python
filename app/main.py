import spidev 
import time 
import os 
import RPi.GPIO as GPIO
import board 
import adafruit_dht 

# Initial the dht device, with data pin connected to:
# dhtDevice = adafruit_dht.DHT22(board.D4)
 
# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
rele_pin = 21
global is_rele_on
is_rele_on = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(rele_pin, GPIO.OUT)

dhtDevice = adafruit_dht.DHT11(board.D4, use_pulseio=False) 


# SPI Verbindung herstellen
spi = spidev.SpiDev() 
spi.open(0,0) 
spi.max_speed_hz=1000000 

# from flask import Flask, render_template, jsonify
from flask import *

app = Flask(__name__)

temperature_c = 0
temperature_f = 0
humidity1 = 0


def dataReadTest():
	data = {
		'title' : 'Monitoring...',
		'humidity' : '1234',
		'temp' : '1234',
		'soilMoistrue' : '1234',
		'lighting' : '1234'
	}
	return data

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
		print(
		    "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
			temperature_f, temperature_c, humidity1
		    )
		)
 
	except RuntimeError as error:
		# Errors happen fairly often, DHT's are hard to read, just keep going
		print(error.args[0])
		# time.sleep(2.0)
		# continue
	except Exception as error:
		print('Error!')
		dhtDevice.exit()
		raise error
        
	lighting = translate(analogEingang(0), 0, 1023, 100, 0)
	humidity2 = translate(analogEingang(1), 0, 1023, 100, 0)
	# GPIO.output(rele_pin, GPIO.HIGH)
	data = {
		'title' : 'Monitoring...',
		'humidity' : str(humidity1)+' %',
		'temp' : str(temperature_c)+' C*',
		'lighting' : str("%.2f" % lighting)+' %',
		'soilMoistrue' : str("%.2f" % humidity2)+' %'
	}
	return data
	
	
def analogEingang(channel):
	adc = spi.xfer2([1,(8+channel)<<4,0])
	data = ((adc[1]&3) << 8) + adc[2]
	return data


@app.route("/api", methods=['GET'])
def api():
	return jsonify(dataRead())
	
	
@app.route("/apiOn", methods=['GET'])
def apiOn():
	lampOnOff(True)
	return None
	
@app.route("/apiOff", methods=['GET'])
def apiOff():
	lampOnOff(False)
	return None
	
	
@app.route("/monitoring", methods=['GET'])
def monitoring():
	
	data = {
		'title' : 'Monitoring...',
		'humidity' : '---',
		'temp' : '---',
		'lighting' : '---',
		'soilMoistrue' : '---'
	}
	return render_template('main.html', **data)
	# return jsonify(data)
	

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)

