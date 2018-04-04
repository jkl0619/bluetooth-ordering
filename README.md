"# bluetooth-ordering" 

Report

Task Distribution:
Jae - client.py
Hao - processor.py
Chris - led.py, server.py

Things to be aware of:

Whatever vhost is being used along with the user, the user has to be added into the 
rabbitmq system along with the vhost. Also, the Vhost needs to grant the user permission 
to everything by using:
rabbitmqctl set_permissions -p vhostName UserName 

After the username, it should be .* .* .* with each set of those enclosed by quotations

Rabbitmq server has to be running as well

With bad internet connection (Which sometimes happens) The pika connection might time out (Especially in the client/Mobile phone))
This can happen very rarely. Please retry again.
The bluetooth also had the tendency to be turned off or go idle if we turn on
 the server and do nothing with it. Please make sure bluetooth is on! 
