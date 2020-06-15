import time
import json
from multiprocessing import Process, Queue
import multiprocessing
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

class Client():
    def __init__(self):
        self.time_sleep = 1

    def Main(self, q_data):
        while True:
            time.sleep(self.time_sleep)
            try:
                data = q_data.get(timeout=0.01)
            except: 
                continue
            
            request = data
            res = requests.post("http://localhost:9901", data=json.dumps(request))

            print('res', res)

class Server(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        post_string = post_data.decode('utf-8')
        response_dict = json.loads(post_string)

        self.q_data.put(response_dict)

        print('response_dict', response_dict)

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

class Communication():
    def __init__(self):
        self.client = Client()

    @staticmethod
    def server_run(q_data, server_class=HTTPServer, handler_class=None, port=9902):
        if handler_class is None:
            handler_class=Server

        setattr(handler_class, 'q_data', q_data)

        server_address = ('localhost', port)
        httpd = server_class(server_address, handler_class)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()

    def run(self):
        q_data = Queue()
        
        client_process = Process(group = None, target = self.client.Main, args = (q_data, ))
        client_process.daemon = True
        client_process.start()
        
        server_process = Process(group = None, target = self.server_run, args = (q_data, ))
        server_process.daemon = True
        server_process.start()
        
        while True:
            time.sleep(3)      

if __name__ == "__main__":
    s = Communication()
    s.run()