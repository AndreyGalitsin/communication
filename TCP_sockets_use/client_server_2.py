import socket 
import time
import json
from multiprocessing import Process

class Client():
    def __init__(self, client_host='localhost', client_port=1523):
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

    def Main(self):
        self.connect()
        counter = 0
        dist = 0
        
        while True:
            
            request = {"three": 3, "four": 4}

            self.make_request(request)
            self.run_client()
            time.sleep(10)
        self.close()

class Server(object):
    def __init__(self, server_host='localhost', server_port=1502):
        self.server_host = server_host
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.server_host, self.server_port))

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                request_bytes = client.recv(size)
                if request_bytes:
                    request_string = request_bytes.decode('utf-8')
                    request_dict = json.loads(request_string)
                    print('mes from serv_1 to serv_2', request_dict)

                    encode_response = json.dumps(response, indent=2).encode('utf-8')                    
                    client.send(encode_response)
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False

class Communication():
    def __init__(self):
        self.client = Client('localhost', 9903)
        self.server = Server('localhost', 9904)
    
    def run(self):
        client_process = Process(group = None, target = self.client.Main)
        client_process.daemon = True
        client_process.start()

        self.server.sock.listen(50)        
        client, address = self.server.sock.accept()
        server_process = Process(group = None,target = self.server.listenToClient, args = (client,address))
        server_process.daemon = True
        server_process.start()
        
        while True:
            time.sleep(3)



if __name__ == '__main__':
    Communication().run()
