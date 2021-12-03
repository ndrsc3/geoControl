
# import the libraries
import RPi.GPIO as GPIO
from time import sleep
from flask import Flask, render_template
import datetime

GPIO.setmode(GPIO.BCM) # :? GPIO.BCM vs GPIO.BOARD
GPIO.setwarnings(False)

# Define Pin Variables
ledRPin = 2     # LED Display R
ledGPin = 3     # LED Display G
ledBPin = 4     # LED Display B
btnPin  = 17    # Manual Button

relayPin = 14   # Relay Switch for HOT Tub 24V

# State Variables
global hotStatus, manualStatus
hotStatus = 0
manualStatus = 0

# Set GPIO Pins
GPIO.setup(btnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(ledRPin, GPIO.OUT)
GPIO.setup(ledGPin, GPIO.OUT)
GPIO.setup(ledBPin, GPIO.OUT)

GPIO.setup(relayPin, GPIO.OUT)

# Callback For Manual Switch
def my_callback(channel):

    global hotStatus
    global manualStatus

    # Read Switch State
    if GPIO.input(btnPin):
        print('Manual Switch: Off')
        hotStatus = 0
        manualStatus = 0
        GPIO.output(relayPin, GPIO.HIGH)
        GPIO.output(ledGPin, GPIO.LOW)
        GPIO.output(ledRPin, GPIO.HIGH)
    else:
        print('Manual Switch: On')
        hotStatus = 1
        manualStatus = 1
        GPIO.output(relayPin, GPIO.LOW)
        GPIO.output(ledGPin, GPIO.HIGH)
        GPIO.output(ledRPin, GPIO.LOW)

    print( '\tHotStatus = ', hotStatus)

GPIO.add_event_detect(btnPin, GPIO.BOTH, callback = my_callback)

# Set Pins to Low
GPIO.output(ledRPin, GPIO.HIGH)
GPIO.output(ledGPin, GPIO.LOW)
GPIO.output(ledBPin, GPIO.LOW)
GPIO.output(relayPin, GPIO.HIGH)

app = Flask(__name__)
@app.route("/")
def index():
    # Read Sensors Status
    global hotStatus
    print(hotStatus)

    templateData = {
        'title' : 'La Finka - Hot Tub Control',
        'hot' : hotStatus
    }

    return render_template('index.html', **templateData)

@app.route("/<deviceName>/<action>")
def action(deviceName, action):

    global hotStatus
    global manualStatus

    if (action == "on" and not manualStatus) :
        hotStatus = 1
        GPIO.output(relayPin, GPIO.LOW)
        GPIO.output(ledGPin, GPIO.HIGH)
        GPIO.output(ledRPin, GPIO.LOW)
    if (action == "off" and not manualStatus) :
        hotStatus = 0
        GPIO.output(relayPin, GPIO.HIGH)
        GPIO.output(ledGPin, GPIO.LOW)
        GPIO.output(ledRPin, GPIO.HIGH)

    templateData = {
        'title' : 'La Finka - Hot Tub Control',
        'hot' : hotStatus
    }

    return render_template('index.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
