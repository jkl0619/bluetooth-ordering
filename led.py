import RPi.GPIO as GPIO
import time
import pika
import rmq_params
import sys

##function used to display a color to the LED
def FlashLED(color, pinRed, pinGreen, pinBlue):
    if color == "blue":
        print('[Checkpoint] Flashing LED to ' + color)
        GPIO.output(pinRed, GPIO.LOW)
        GPIO.output(pinGreen, GPIO.LOW)
        GPIO.output(pinBlue, GPIO.HIGH)
    if color == "red":
        print('[Checkpoint] Flashing LED to ' + color)
        GPIO.output(pinRed, GPIO.HIGH)
        GPIO.output(pinGreen, GPIO.LOW)
        GPIO.output(pinBlue, GPIO.LOW)
    if color == "purple":
        print('[Checkpoint] Flashing LED to ' + color)
        GPIO.output(pinRed, GPIO.HIGH)
        GPIO.output(pinGreen, GPIO.LOW)
        GPIO.output(pinBlue, GPIO.HIGH)
    if color == "yellow":
        print('[Checkpoint] Flashing LED to ' + color)
        GPIO.output(pinRed, GPIO.HIGH)
        GPIO.output(pinGreen, GPIO.HIGH)
        GPIO.output(pinBlue, GPIO.LOW) 
    if color == "green":
        print('[Checkpoint] Flashing LED to ' + color)
        GPIO.output(pinRed, GPIO.LOW)
        GPIO.output(pinGreen, GPIO.HIGH)
        GPIO.output(pinBlue, GPIO.LOW)

    time.sleep(.25)

    GPIO.output(pinRed, GPIO.LOW)
    GPIO.output(pinGreen, GPIO.LOW)
    GPIO.output(pinBlue, GPIO.LOW)


GPIO.setwarnings(False)        #used to get rid of warnings from GPIO


##argument parsing and error handling
if sys.argv[1] == '-s':
    _host = sys.argv[2]
else:
    print('Incorrect IP flag, format: ' + "'" + 'python led.py -s IP.ADDRESS -m PINMODE -r RED.PIN -g GREEN.PIN -b BLUE.PIN' + "'")

if sys.argv[3] == '-m':
    if sys.argv[4] == '10':
        GPIO.setmode(GPIO.BOARD)
    elif sys.argv[4] == '11':
        GPIO.setmode(GPIO.BCM)
    else:
        print('Incorrect pin-mode flag, format: ' + "'" + 'python led.py -s IP.ADDRESS -m PINMODE -r RED.PIN -g GREEN.PIN -b BLUE.PIN' + "'")
                
if sys.argv[5] == '-r':
    pinRed= int(sys.argv[6])
else:
    print('Incorrect red pin flag, format: ' + "'" + 'python led.py -s IP.ADDRESS -m PINMODE -r RED.PIN -g GREEN.PIN -b BLUE.PIN' + "'")

if sys.argv[7] == '-g':
    pinGreen = int(sys.argv[8])
else:
    print('Incorrect green pin flag, format: ' + "'" + 'python led.py -s IP.ADDRESS -m PINMODE -r RED.PIN -g GREEN.PIN -b BLUE.PIN' + "'")
    
if sys.argv[9] == '-b':
    pinBlue = int(sys.argv[10])
else:
    print('Incorrect blue pin flag, format: ' + "'" + 'python led.py -s IP.ADDRESS -m PINMODE -r RED.PIN -g GREEN.PIN -b BLUE.PIN' + "'")
        

##set pins 11-13 as output pins
GPIO.setup(pinRed, GPIO.OUT)		
GPIO.setup(pinGreen, GPIO.OUT)		
GPIO.setup(pinBlue, GPIO.OUT)		

##obtain information from the rmq_params file
_user = rmq_params.rmq_params['username']
_vhost = rmq_params.rmq_params['vhost']
_pass = rmq_params.rmq_params['password']
_exc = rmq_params.rmq_params['exchange']
_queue = 'led'

##connect to the RMQ server
credentials = pika.PlainCredentials(_user, _pass)
connection = pika.BlockingConnection(pika.ConnectionParameters(host= _host, credentials = credentials, virtual_host = _vhost))
channel = connection.channel()
#channel.queue_bind(exchange = _exc, queue = rmq_params.rmq_params['led_queue'])


print('[Checkpoint] Connected to vhost ' + _vhost + ' on RMQ server at ' + _host + ' as user ' + _user)
      

print('[Checkpoint] Consuming from RMQ queue: ' + _queue)

    ##constantly wait for LED updates
while True:
    def callback(ch, method, properties, body):        
        if body.decode('utf-8') == 'CC':
            FlashLED('blue', pinRed, pinGreen, pinBlue)

        if body.decode('utf-8') == 'CD':
            FlashLED("red", pinRed, pinGreen, pinBlue)

        if body.decode('utf-8') == 'OSe':
            FlashLED("purple", pinRed, pinGreen, pinBlue)

        if body.decode('utf-8') == 'OSt':
            FlashLED("yellow", pinRed, pinGreen, pinBlue)

        if body.decode('utf-8') == 'OF':
            FlashLED("green", pinRed, pinGreen, pinBlue)
            
        ##get message
    channel.basic_consume(callback,
    		      queue = _queue,
    		      no_ack = True)
    
    channel.start_consuming()

    
    


