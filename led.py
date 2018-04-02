import RPi.GPIO as GPIO
import time
import pika
import pybluez
import libbluetooth-dev
import rabbitmq-server

GPIO.setmode(GPIO.BOARD)		#Set to board referenced pins
#set pins 11-13 as output pins
pinRed = 11
pinGreen = 13
pinBlue = 15
GPIO.setup(pinRed, GPIO.OUT)		
GPIO.setup(pinGreen, GPIO.OUT)		
GPIO.setup(pinBlue, GPIO.OUT)		

_host = 'host'
_IP = '192.168.1.14'
_user = 'user'
_queue = 'led'

connection = pika.BlockingConnection(pika.ConnectionParameters(
	host= 'localhost'))
channel = connection.channel()
channel.queue_declare(queue = _queue)


print('[Checkpoint] Connected to vhost %s on RMQ server at %s as user %s', _host, _IP, _user')
      
def callback(ch, method, properties, body):
	print('[Checkpoint] Consuming from RMQ queue: %s', _queue)

channel.basic_consume(callback,
				      queue = _queue
					  no_ack = False)

channel.start_consuming()
					  
	# not too sure when to manipulate these
clientConnected = False
clientDisconnected = False
orderSent = False
orderStarted = False
orderFinished = False


if clientConnected:
	FlashLED("blue")

if clientDisconnected:
    FlashLED("red")

if orderSent:
    FlashLED("purple")
    
if orderStarted:
    FlashLED("yellow")
  
if orderFinished:
    FlashLED("green")
    
    
    
def FlashLED(color):
    if color == "blue":
		print('[Checkpoint] Flashing LED to %s', color)
        GPIO.output(pinRed, GPIO.LOW)
		GPIO.output(pinGreen, GPIO.LOW)
		GPIO.output(pinBlue, GPIO.HIGH)
    if color == "red":
		print('[Checkpoint] Flashing LED to %s', color)
        GPIO.output(pinRed, GPIO.HIGH)
		GPIO.output(pinGreen, GPIO.LOW)
		GPIO.output(pinBlue, GPIO.LOW)
	if color == "purple":
		print('[Checkpoint] Flashing LED to %s', color)
        GPIO.output(pinRed, GPIO.HIGH)
		GPIO.output(pinGreen, GPIO.LOW)
		GPIO.output(pinBlue, GPIO.HIGH)
    if color == "yellow":
		print('[Checkpoint] Flashing LED to %s', color)
        GPIO.output(pinRed, GPIO.HIGH)
		GPIO.output(pinGreen, GPIO.HIGH)
		GPIO.output(pinBlue, GPIO.LOW) 
	if color == "green":
		print('[Checkpoint] Flashing LED to %s', color)
        GPIO.output(pinRed, GPIO.LOW)
		GPIO.output(pinGreen, GPIO.HIGH)
		GPIO.output(pinBlue, GPIO.LOW)

	 
    time.sleep(.25)
    
    GPIO.output(pinRed, GPIO.LOW)
    GPIO.output(pinGreen, GPIO.LOW)
    GPIO.output(pinBlue, GPIO.LOW)
