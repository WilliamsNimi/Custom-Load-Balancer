from http.server import *
import requests
import socket
import json
import concurrent.futures
import time
import random
import threading

start_time = time.time()

servers = {("127.0.0.1", 8080): 0, ("127.0.0.1", 9090): 0, ("127.0.0.1", 5050): 0, ("127.0.0.1", 2000): 0}
active_servers = {}
minimum_load = 0
load_count = 0

def health_check(servers):
    """ Run check on all available servers and adds active servers to active_servers list"""
    for server, load in servers.items():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as checker:
                checker.connect(server)
                checker.settimeout(1)
                if server not in active_servers:
                    active_servers[server] = 0
        except Exception as e:
            with open("Error_Logs/Error_Logs.txt", "a") as f:
                f.write(f"{time.time()} :{ e} for {server}. \n")
    return active_servers

def round_robin(active_servers):
    global minimum_load
    global load_count
    for server, load in active_servers.items():
        if load == minimum_load:
            load_count+=1
            return server
        if load_count == len(active_servers):
            minimum_load += 1
            load_count = 0
            
class BasicServer(BaseHTTPRequestHandler):
    def handle_reqs(self, server):
        if type(server) is tuple:
            url = "http://" + server[0] + ":" + str(server[1])
            res = requests.get(url)
            if res.status_code == 200:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(bytes(json.dumps(res.json()), 'utf-8'))
                self.wfile.write(bytes("\n", 'utf-8'))
                active_servers[server] += 1
            
    def do_GET(self):
        active_servers = health_check(servers)
        #self.handle_reqs(round_robin())
        with concurrent.futures.ThreadPoolExecutor(max_workers = 3) as executor:
            executor.submit(self.handle_reqs(round_robin(active_servers)))

    
if __name__ == "__main__":
    port = HTTPServer(('', 80), BasicServer)
    port.serve_forever()
