from flask import Flask, request, send_file, jsonify 
from flask_cors import CORS
import RPi.GPIO as GPIO
from time import sleep

app = Flask(__name__)
CORS(app)

Motor1A = 16
Motor1B = 18
Motor1E = 22
Motor2A = 23
Motor2B = 21
Motor2E = 19

def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(Motor1A,GPIO.OUT)
	GPIO.setup(Motor1B,GPIO.OUT)
	GPIO.setup(Motor1E,GPIO.OUT)
	GPIO.setup(Motor2A,GPIO.OUT)
	GPIO.setup(Motor2B,GPIO.OUT)
	GPIO.setup(Motor2E,GPIO.OUT)

@app.route("/get_image", methods = ['GET'])
def get_image():
	if request.method == 'GET':
       		return send_file('/tmp/image.jpg', mimetype='image/jpg')

@app.route("/forward", methods = ['POST'])
def forward():
	if request.method == 'POST':
		setup()
		go_forward()
		sleep(1)
		stop()
		return jsonify(success=True)

@app.route("/back", methods = ['POST'])
def back():
	if request.method == 'POST':
		setup()
		go_back()
		sleep(1)
		stop()
		return jsonify(success=True)

@app.route("/left", methods = ['POST'])
def left():
	if request.method == 'POST':
		setup()
		go_left()
		sleep(1)
		stop()
		return jsonify(success=True)

@app.route("/right", methods = ['POST'])
def right():
	if request.method == 'POST':
		setup()
		go_right()
		sleep(1)
		stop()
		return jsonify(success=True)

@app.route("/forwardleft", methods = ['POST'])
def forwardleft():
	if request.method == 'POST':
		setup()
		go_forward()
		go_left()
		sleep(1)
		stop()
		return jsonify(success=True)

@app.route("/forwardright", methods = ['POST'])
def forwardright():
	if request.method == 'POST':
		setup()
		go_forward()
		go_right()
		sleep(1)
		stop()
		return jsonify(success=True)

@app.route("/backleft", methods = ['POST'])
def backleft():
	if request.method == 'POST':
		setup()
		go_back()
		go_left()
		sleep(1)
		stop()
		return jsonify(success=True)

@app.route("/backright", methods = ['POST'])
def backright():
	if request.method == 'POST':
		setup()
		go_back()
		go_right()
		sleep(1)
		stop()
		return jsonify(success=True)

def go_forward():
	print "Forward"
	GPIO.output(Motor1A,GPIO.HIGH)
	GPIO.output(Motor1B,GPIO.LOW)
	GPIO.output(Motor1E,GPIO.HIGH)

def go_back():
	print "Back"
	GPIO.output(Motor1A,GPIO.LOW)
	GPIO.output(Motor1B,GPIO.HIGH)
	GPIO.output(Motor1E,GPIO.HIGH)

def go_left():
	print "Left"
	GPIO.output(Motor2A,GPIO.HIGH)
	GPIO.output(Motor2B,GPIO.LOW)
	GPIO.output(Motor2E,GPIO.HIGH)

def go_right():
	print "Right"
	GPIO.output(Motor2A,GPIO.LOW)
	GPIO.output(Motor2B,GPIO.HIGH)
	GPIO.output(Motor2E,GPIO.HIGH)

def stop():
	print "Stop"
	GPIO.output(Motor1E,GPIO.LOW)
	GPIO.output(Motor2E,GPIO.LOW)
	GPIO.cleanup()

if __name__ == '__main__':
     app.run(host='0.0.0.0',port='5000',debug=True)
