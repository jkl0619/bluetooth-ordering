import RPi.GPIO as GPIO
import time
import pika
import pybluez
import libbluetooth-dev
import rabbitmq-server

_host = 'localhost'
_user = 'user'


connection = pika.BlockingConnection(pika.ConnectionParameters( host=_host))

print('[Checkpoint] Connected to vhost \'not sure\' on RMQ server at %s as user %s', _host, _user)
print('[Checkpoint] Setting up exchanges and queues...')
channel = connection.channel()
channel.queue_declare(queue='order')
channel.queue_declare(queue='led')
channel.queue_declare(queue='client')

#channel.basic_publish(exchange='',
#	routing_key='order_key',
#	body='order_body')

# routing_key = which queue
# body = the message to be sent

# connection.close() after sending the data to queue

print('[Checkpoint] Bluetooth ready!')

port = 1

server_socket = BluetoothSocket(RFCOMM)
server_socket.bind(("",port))

print('[Checkpoint] Waiting for connection on RFCOMM channel %2d', port)
server_sock.listen(1)

client_info = server_socket.accept
client_socket,address = server_socket.accept()

print('[Checkpoint] accepted connection from (%s, %d)', client_info[0], client_info[0])

menu = '\r item1:\r\t\t time: 6\r\t\t price: 2.25\r\r item2:\r\t\t time: 2\r\t\t price:4.5')

server_socket.send('Sending menu') 

print('[Checkpoint] Sent menu: %s', menu)

#waiting for order back

data = client_socket.recv(1024)



print('[Checkpoint] Received order: %s')










