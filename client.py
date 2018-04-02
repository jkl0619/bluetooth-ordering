#!/usr/bin/env python3


# """A simple echo client"""
import socket
from clientKeys import *
import optparse
import pika
import time

# -s RMQ IP OR HOST NAME -b BLUETOOTH ADDRESS
# Parse through the arguments
parser = optparse.OptionParser()
parser.add_option('-s', dest='host', help='The host ip address or host name to connect the client to')
parser.add_option('-b', dest='bluetooth', help='The bluetooth address')
(options, args) = parser.parse_args()

# initialize values from command line
host = options.host
bluetooth = options.bluetooth
print("[Checkpoint] Connecting to " + host, " on " + bluetooth)

#connect to the RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host))
channel = connection.channel()
#should not declare exchanges or queues channel.queue_declare(queue='menu')
print("[Checkpoint] Connected")

#define callback method
def callback(ch, method, properties, body):
    print(" [Checkpoint] Received Menu: %r" % body)
    print("Enter items separated by space characters:" )
    orderList = input(str(x) for x in input().split())
    channel.basic_publish(exchange='', routing_key='OrderList', body=orderList)
    print(" [Checkpoint] Sent Order: " + orderList)

def callback_receipt(ch, method, properties, body):
    print (" [Checkpoint] Received receipt: %r" % body)

#set our channel to receive messages from the queue
channel.basic_consume(callback, queue='hello', no_ack=True)

