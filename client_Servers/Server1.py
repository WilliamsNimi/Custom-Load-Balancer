from http.server import *
import socket
import json

class BasicServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        data = {"message": "Alpha Server Responding"}
        self.wfile.write(bytes(json.dumps(data), 'utf-8'))

port = HTTPServer(('', 8080), BasicServer)
port.serve_forever()
