from http.server import *
import requests
import socket
import json
import concurrent.futures
import time
import random

start_time = time.time()

servers = [("127.0.0.1", 8080), ("127.0.0.1", 9090)]
active_servers = []

def health_check(servers):
    """ Run check on all available servers and adds active servers to active_servers list"""
    for server in servers:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as checker:
                checker.connect(server)
                checker.settimeout(1)
                if server not in active_servers:
                    active_servers.append(server)
        except Exception as e:
            return False #TODO: Add a logger here to a file
    return active_servers
            
class BasicServer(BaseHTTPRequestHandler):
    
    def handle_reqs(self, server):
        url = "http://" + server[0] + ":" + str(server[1])
        res = requests.get(url)
        if res.status_code == 200:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(res.json()), 'utf-8'))
            self.wfile.write(bytes("\n", 'utf-8'))
            
    def do_GET(self):
        self.handle_reqs(random.choice(health_check(servers))) #randomly selecting servers from a list of active servers
        """with concurrent.futures.ThreadPoolExecutor(max_workers = 2) as executor:
            executor.map(self.handle_reqs, active_servers)
        print(time.time() - start_time)"""

port = HTTPServer(('', 80), BasicServer)
port.serve_forever()
