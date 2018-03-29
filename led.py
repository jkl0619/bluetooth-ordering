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

clientConnected = True
clientDisconnected = False
orderSent = False
orderStarted = False
orderFinished = False

colors = {
	"red" : (1,0,0),
	"green" : (0,1,0),
	"bleu" : (0,0,1),
	"purple" : (1,0,1),
	"yellow" : (1,1,0)
}

# D = {"Key1": (1,2,3), "Key2": (4,5,6)}
# D["Key2"][2]



if clientConnected:
	FlashLED(colors["blue"])

if clientDisconnected:
    FlashLED(colors["red"])

if orderSent:
    FlashLED(colors["purple"])
    
if orderStarted:
    FlashLED(colors["yellow"])
  
if orderFinished:
    FlashLED(colors["green"])
    
    
    
def FlashLED(red,green,blue):				#this doesnt work, cant get tuple to be the input for some reason
    setRed = red
    setGreen = green
    setBlue = blue
    
    if setRed:
        GPIO.output(pinRed, GPIO.HIGH)
    if setGreen:
        GPIO.output(pinGreen, GPIO.HIGH)
    if setBlue:
        GPIO.output(pinBlue, GPIO.HIGH)
        
    time.sleep(.25)
    
    GPIO.output(pinRed, GPIO.LOW)
    GPIO.output(pinGreen, GPIO.LOW)
    GPIO.output(pinBlue, GPIO.LOW)