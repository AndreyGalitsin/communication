# There are 3 most popular kinds of communication between different modules which are usefull nowadays. 
They are:
1. TCP sockets
2. Websockets
3. POST requests

# 1. TСP sockets
Usage of TCP sockets is the most difficult method of them. Here we have two scripts:
1. client_server_1.py
2. client_server_2.py

They are almost the same. Both of these scripts have a Server and a Client part. They work in two different processes, using multiprocessing module. In this version client_server_2 sends a message to client_server_1, and then client_server_1 returns the same message to client_server_2.

### What is happening here in fact?
1. The Client process in script client_server_2.py connects to the Server process in script client_server_1.py and send a message.
2. In the client_server_1.py script the Server part send this data to the Client part using 'queue'. 
3.The Client part in client_server_1.py script connects to the Server part in client_server_2.py and sends the same message back

### Parameters
1. Server in client_server_1.py is running on localhost on the port 9903
2. Server in client_server_2.py is running on localhost on the port 9904

# 2. Websockets
This process is more easier, then previous with TCP sockets. Websockets is a communication protocol over a TCP connection. Because of this we can conclude, that this method is a little bit slower then TCP sockets.
We can create one server and one client and aloow them communicate with each other without waiting any callbacks.
There are a lot of different methods and frameworks which allow to craete websockets pair of client and server. Here we use a websocket library with async method. The server here sends a message to the client, which returnes the same message back to the server.

https://github.com/aaugustin/websockets

### Parameters
1. Server is running on localhost on the port 9905

# 3. POST requests
This method looks like the first one with TCP sockets but it is a higher-level method. Here we use requests library.
https://github.com/psf/requests

There are 3 scripts here:
1. mult_client_server.py
2. simple_server.py
3. simple_client.py

RUN them in this sequence!

The first script has both, the Server and the Client part which are working in two different processes with multiprocessing module. The same Server and Client parts you can find in simple_server.py and simple_client.py respectively. 

Here a client sends a message to the Server part in mult_client_server.py. The Client part in this script sends the same message to the server.

### Parameters
1. Server in mult_client_server.py is running on localhost on the port 9902
2. Server in simple_server.py is running on localhost on the port 9903


