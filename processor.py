import pika
import sys
import rmq_params.py

#Receiving messages from order queue
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rmq_params["order_queue"]))
channel = connection.channel()

print("[Checkpoint] Connected to vhost ", host, " on RMQ server at ", argv[3], " as user ", rmq_params["username"])
print("[Checkpoint] Starting order: ", "order #")
  
  
#assuming channel is already created

def callback(ch, method, properties, body):
	print(" [x] Recevied %r" % body)
	
channel.basic_consume(callback, queue='order-Q', no_ack=True)

#for debugging
print(' [*] Waiting for messages. To exit press CTRL+C')

#sending to LED
#bind to channel
channel.queue_bind(exchange = rmq_params["led_queue"],
					queue=result.method.queue)

#sending to client queue				
#assuming name of client queue is "client_queue"	
channel.queue_bind(exchange = rmq_params["client_queue"],
					queue=result.method.queue)



print("[Checkpoint] Completed order: ", "order #")