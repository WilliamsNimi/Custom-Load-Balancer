import os
import concurrent.futures
import sys
import time

try:          
    load = sys.argv[1]
    load = int(load)
except Exception as e:
    with open("LoadTesterErrorLog.txt", 'a') as f:
        f.write(f"{time.time()}: {e}")
    print("Usage: Python3 get_reqs.py *Load int value*")

def req(count):
    os.system("curl localhost")
    
def threading():
    with concurrent.futures.ThreadPoolExecutor(max_workers = 2) as executor:
        executor.map(req, range(load))
        
if __name__ == "__main__":
    try:
        threading()
    except NameError:
        print("Please provide a valid load value. See Usage above")
