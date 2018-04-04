#!/usr/bin/env/python
import pika
from bluetooth import *
import sys
import rmq_params
import menu
import time

#Establish connection with vhost
credentials = pika.PlainCredentials(rmq_params.rmq_params["username"], rmq_params.rmq_params["password"])
connection = pika.BlockingConnection(pika.ConnectionParameters(host=sys.argv[2], credentials = credentials, virtual_host=rmq_params.rmq_params["vhost"]))
channel = connection.channel()

#Checkpoint
print("[Checkpoint] Connected to vhost " + rmq_params.rmq_params["vhost"] + " on RMQ server at "+ sys.argv[2]+ " as user "+ rmq_params.rmq_params["username"])  
print("[Checkpoint] Consuming from RMQ queue: " + rmq_params.rmq_params["order_queue"])

#defines callback function to carry out tasks when item is received
def callback(ch, method, properties, body):
	#print("[x] Recevied %r" % body)
    info = body.decode('utf-8')
    orderID, list = info.split(";") #splits the recevied info into orderID and items
    items = list.split()

    sleepTime = 0

    for x in range(0,len(items)): #calculates sleep time
        if items[x] in menu.menu.keys():
            t = menu.menu[items[x]]["time"]
            sleepTime += float(t)
            
    print("[Checkpoint] Starting order: " + orderID)

    #sends LED yellow command to the LED queue
    channel.basic_publish(exchange=rmq_params.rmq_params["exchange"], routing_key =rmq_params.rmq_params["led_queue"], body ='OSt')
    
    #sends message to the client queue
    channel.basic_publish(exchange= rmq_params.rmq_params["exchange"], routing_key = orderID, body ='We are processing your order.') 
    
    #processing
    time.sleep(sleepTime)

    #sends LED green command to the LED queue
    channel.basic_publish(exchange= rmq_params.rmq_params["exchange"], routing_key = rmq_params.rmq_params["led_queue"], body ='OF')
    
    #sends message to the client queue
    channel.basic_publish(exchange= rmq_params.rmq_params["exchange"], routing_key = orderID, body ='We finished processing your order.')

    print("[Checkpoint] Completed order: " + orderID)
            

#binds the channel
channel.queue_bind(exchange = rmq_params.rmq_params["exchange"], queue= rmq_params.rmq_params["order_queue"])

#read in messages from the order queue
channel.basic_consume(callback, queue=rmq_params.rmq_params["order_queue"], no_ack=True)
channel.start_consuming()


