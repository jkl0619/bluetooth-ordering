import RPi.GPIO as GPIO
import time
import pika
import rmq_params
import menu
from bluetooth import *


ID = '69'          #change to be client queue


_host = '172.29.71.135'
_user = rmq_params.rmq_params['username']
_vhost = rmq_params.rmq_params['vhost']
_pass = rmq_params.rmq_params['password']
_exc = rmq_params.rmq_params['exchange']

credentials = pika.PlainCredentials(_user, _pass)
connection = pika.BlockingConnection(pika.ConnectionParameters( host= _host, credentials = credentials))
print('[Checkpoint] Connected to vhost '+_vhost+' on RMQ server at '+_host+' as user '+_user)
print('[Checkpoint] Setting up exchanges and queues...')
channel = connection.channel()
channel.exchange_declare(exchange = _exc)
channel.queue_declare(queue=rmq_params.rmq_params['order_queue'])
channel.queue_declare(queue=rmq_params.rmq_params['led_queue'])
#channel.queue_declare(queue='client')

#channel.basic_publish(exchange=_exc,
#	routing_key='order',
#	body='fuck you')

# routing_key = which queue
# body = the message to be sent

connection.close() #after sending the data to queue

print('[Checkpoint] Bluetooth ready!')

port = 3

server_socket = BluetoothSocket(RFCOMM)
server_socket.bind(("",port))

print('[Checkpoint] Waiting for connection on RFCOMM channel ' + str(port))
server_socket.listen(1)

client_info = server_socket.accept()
client_socket,address = client_info

print('[Checkpoint] Accepted connection from (' + str(client_info[0]) + ',' + str(client_info[0]) + ')')

#menu = '\ritem1:\r\t\t time: 6\r\t\t price: 2.25\r\r item2:\r\t\t time: 2\r\t\t price:4.5'

 

_menu =""

for x,y in menu.menu.items():
    temp = ""
    temp+=x
    for xx,yy in y.items():
        temp = temp + ' ' + str(xx) + " " + str(yy)
    _menu = _menu + " " + temp

client_socket.send(_menu)

print('[Checkpoint] Sent menu: ' + _menu)

#waiting for order back

data = client_socket.recv(1024)
data = data.decode('utf-8')

print('[Checkpoint] Received order:' + str(data))


data = [str(i) for i in data.split()]

price = 0
time = 0

for x in range (0,len(data)):
    if data[x] in menu.menu.keys():
        p = menu.menu[data[x]]['price']
        t = menu.menu[data[x]]['time']
        price += float(p)
        time += float(t)
        
     
        
client_socket.send(ID)       #Order ID
client_socket.send(str(data))       #Items list
client_socket.send(str(price))      #price
client_socket.send(str(time))       #time

print('[Checkpoint] Sent receipt: ')
print('Order ID: ' + ID)
print('Items: ' + str(data))
print('Total Price: ' + str(price))
print('Total Time: ' + str(time))

server_socket.close()
print('[Checkpoint] Closed Bluetooth Connection')







