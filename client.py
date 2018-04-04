#!/usr/bin/env python3

import socket
import optparse
import pika
import time
import rmq_params as param
from bluetooth import *

# -s RMQ IP OR HOST NAME -b BLUETOOTH ADDRESS
# Parse through the arguments
parser = optparse.OptionParser()
parser.add_option('-s', dest='host', help='The host ip address or host name to connect the client to')
parser.add_option('-b', dest='bluetooth', help='The bluetooth address')
(options, args) = parser.parse_args()

# initialize values from command line
host = options.host
bluetooth = options.bluetooth

#connect to bluetooth
client_socket=BluetoothSocket(RFCOMM)
client_socket.connect((bluetooth,3))
print(" [Checkpoint] Connecting to " + host, " on " + bluetooth)
data = client_socket.recv(1024)
data = data.decode('utf-8')
print(" [Checkpoint] Received Menu: %r" % data)

print("Enter items separated by space characters:")
orderList = input()
client_socket.send(orderList)
print(" [Checkpoint] Sent order: ")
print(orderList)

orderID = client_socket.recv(1024)
items = client_socket.recv(1024)
totalPrice = client_socket.recv(1024)
totalTime = client_socket.recv(1024)

#Fix receiving items into appropriate cast type
items = items.decode('utf-8')
orderID = orderID.decode('utf-8')
totalPrice = totalPrice.decode('utf-8')
totalTime = totalTime.decode('utf-8')
totalPrice = float(totalPrice)
totalTime = float(totalTime)
print(" [Checkpoint] Received receipt: ")
print("Order ID: " + orderID)
print("Items: " + items)
print("Total Price: " +str( totalPrice))
print("Total Time: " + str(totalTime))

client_socket.close()
print(" [Checkpoint] Closed Bluetooth Connection")


credentials = pika.PlainCredentials(param.rmq_params["username"], param.rmq_params["password"])

#connect to the RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host, credentials=credentials))
channel = connection.channel()

print(" [Checkpoint] Connected to vhost " + param.rmq_params["vhost"], "on RMQ server at " + host, " as user " + param.rmq_params["username"])

#define callback method
def callback(ch, method, properties, body):
	print("Order Update: " + body)

channel.queue_bind(exchange=param.rmq_params["exchange"],queue=orderID)
channel.basic_consume(callback, queue=orderID, no_ack=True)
print(" [Checkpoint] Consuming from RMQ Queue: " + orderID)

channel.start_consuming()

