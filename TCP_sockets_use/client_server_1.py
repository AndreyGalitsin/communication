import time
import json
import socket

import socket
from multiprocessing import Process, Queue
import multiprocessing

class Client():
    def __init__(self, client_host='localhost', client_port=1502):
        self.client_host = client_host
        self.client_port = client_port
        self.time_sleep = 1

    def connect(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # connect to server on local computer 
        self.s.connect((self.client_host,self.client_port))

    def make_request(self, request):
        self.encode_request = json.dumps(request, indent=2).encode('utf-8')

    def run_client(self):
        try:
            self.s.send(self.encode_request)
            try:
                response_bytes = self.s.recv(1024) 
                response_string = response_bytes.decode('utf-8')
                self.response_dict = json.loads(response_string)
                print('Received from the server :',self.response_dict) 
                time.sleep(self.time_sleep)
            except:
                pass
        except:
            pass

    def close(self):
        self.s.close()

    def Main(self, q):
        self.connect()
        while True:
            try:
                request_dict = q.get(timeout=0.1)
                request = request_dict
            except: 
                request = {'zero': 0}
            self.make_request(request)
            self.run_client()
        self.close()


class Server(object):
    def __init__(self, server_host='localhost', server_port=1523):
        self.server_host = server_host
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.server_host, self.server_port))

    def listenToClient(self, client, address, q):
        size = 1024
        while True:
            try:
                request_bytes = client.recv(size)
                if request_bytes:
                    request_string = request_bytes.decode('utf-8')
                    request_dict = json.loads(request_string)
                    q.put(request_dict)
                    print('mes from serv_2 to serv_1', request_dict)
                     
                    encode_response = json.dumps(response, indent=2).encode('utf-8')                                      
                    client.send(encode_response)   
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False

class Communication():
    def __init__(self):
        self.server = Server("localhost", 9903)
        self.client = Client("localhost", 9904)

    def run(self):
        q = Queue()

        self.server.sock.listen(50)
        client, address = self.server.sock.accept()
        server_process = Process(group = None, target = self.server.listenToClient, args = (client,address,q))
        server_process.daemon = True
        server_process.start()

        client_process = Process(group = None, target = self.client.Main, args = (q, ))
        client_process.daemon = True
        client_process.start()

        while True:
            time.sleep(3)      

if __name__ == "__main__":
    Communication().run()