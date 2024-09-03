import os
import concurrent.futures

load =1000
def req(count):
    os.system("curl localhost")
    print(count)
def threading():
    with concurrent.futures.ThreadPoolExecutor(max_workers = 2) as executor:
        executor.map(req, range(load))

threading()
