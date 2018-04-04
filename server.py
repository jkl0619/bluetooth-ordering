import RPi.GPIO as GPIO
import time
import pika
import rmq_params
import menu
from bluetooth import *


##obtain information from the rmq_params file
_host = '192.168.1.7'
_user = rmq_params.rmq_params['username']
_vhost = rmq_params.rmq_params['vhost']
_pass = rmq_params.rmq_params['password']
_exc = rmq_params.rmq_params['exchange']

##creating RMQ server and defining the queues
credentials = pika.PlainCredentials(_user, _pass)
connection = pika.BlockingConnection(pika.ConnectionParameters( host= _host, credentials = credentials, virtual_host = _vhost))
print('[Checkpoint] Connected to vhost '+_vhost+' on RMQ server at '+_host+' as user '+_user)
print('[Checkpoint] Setting up exchanges and queues...')
channel = connection.channel()
channel.exchange_declare(exchange = _exc)
channel.queue_declare(queue=rmq_params.rmq_params['order_queue'], auto_delete = True)
channel.queue_declare(queue=rmq_params.rmq_params['led_queue'], auto_delete = True)
channel.queue_bind(exchange = _exc, queue = rmq_params.rmq_params['order_queue'])
channel.queue_bind(exchange = _exc, queue = rmq_params.rmq_params['led_queue'])

print('[Checkpoint] Bluetooth ready!')

port = 3         #Arbitrary port declaration

ID = 100         #order ID will begin at 100 and increment as more orders are processed

while True:
    ##begin bluetooth connections
    server_socket = BluetoothSocket(RFCOMM)
    server_socket.bind(("",port))

    print('[Checkpoint] Waiting for connection on RFCOMM channel ' + str(port))
    server_socket.listen(1)

    ##find the client
    client_info = server_socket.accept()
    client_socket,address = client_info

    print('[Checkpoint] Accepted connection from ' + str(client_info[1]))

    ##sending LED that client connected
    channel.basic_publish(exchange=_exc,
            routing_key='led',
            body='CC')

    _menu =""
    for x,y in menu.menu.items():
        temp = ""
        temp+=x
        for xx,yy in y.items():
            temp = temp + ' ' + str(xx) + " " + str(yy)
        _menu = _menu + "    " + temp

    client_socket.send(_menu)

    print('[Checkpoint] Sent menu: ' + _menu)

    #waiting for order back
    data = client_socket.recv(1024)
    data = data.decode('utf-8')

    print('[Checkpoint] Received order:' + str(data))

    data = [str(i) for i in data.split()]

    price = 0
    time = 0
    vals = ''
    for x in range (0,len(data)):
        if data[x] in menu.menu.keys():
            vals =  vals + str(data[x]) + ' '
            p = menu.menu[data[x]]['price']
            t = menu.menu[data[x]]['time']
            price += float(p)                    #get the total price of all items
            time += float(t)                     #get the total time to process all items
            
    channel.queue_declare(queue=str(ID), auto_delete = True)        #declare a queue based on the current client
    channel.queue_bind(exchange = _exc, queue = str(ID))
    
         ##sending data to the client        
    client_socket.send(str(ID))       #Order ID
    client_socket.send(str(data))       #Items list
    client_socket.send(str(price))      #price
    client_socket.send(str(time))       #time

        ##send receipt
    print('[Checkpoint] Sent receipt: ')
    print('Order ID: ' + str(ID))
    print('Items: ' + str(data))
    print('Total Price: ' + str(price))
    print('Total Time: ' + str(time))

        ##sending order to the processor
    channel.basic_publish(exchange=_exc,
            routing_key='order',
            body=str(str(ID) + ';' + vals))
        ##sending LED that order was sent
    channel.basic_publish(exchange=_exc,
            routing_key='led',
            body='OSe')
        ##sending CLIENT that the order is being processed
    channel.basic_publish(exchange = _exc,
            routing_key = str(ID),
            body='The order has been submitted.')

        ##close the bluetooth 
    server_socket.close()
    print('[Checkpoint] Closed Bluetooth Connection')

    ##sending LED that it was disconnected
    channel.basic_publish(exchange=_exc,
            routing_key='led',
            body='CD')

    #connection.close() #after sending the data to queue

    ID += 1      #move on to the next order



