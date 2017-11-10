import multiprocessing
import numpy as np
import subprocess
import time

def calculate(value):
    out = subprocess.call("echo 123",shell=False)
    return out

if __name__ == '__main__':
    data = []
    results = [subprocess.Popen("./build/Project4 {} \
        {}".format(i,1),shell=True, stdout=subprocess.PIPE) for i in np.arange(10,100,10)]
    for r in results:
        d = r.communicate() # Wait on the results
        data.append(d[0])
        print(d[0])

    print results
    #print(data)
