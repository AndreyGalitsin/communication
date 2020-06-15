from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
	
from urllib.parse import parse_qs
  

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
        
        print('response_dict', response_dict)


        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=Server, port=9901):
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == '__main__':
    run()