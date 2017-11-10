import multiprocessing
import numpy as np
import subprocess
import time

def calculate(value):
    out = subprocess.call("echo 123",shell=False)
    return out

if __name__ == '__main__':
    results = [subprocess.Popen("./build/Project4 {} {}".format(i,1),shell=True) for i in np.arange(10,100,10)]
    for r in results:
        r.wait() # Wait on the results
    print results
