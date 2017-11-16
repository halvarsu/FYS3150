import numpy as np
import matplotlib.pyplot as plt


def read_data(filename):
    with open(filename) as infile:
        rawdata = infile.readlines()
    expectations = np.zeros((len(rawdata), 6))
    temperatures = np.zeros(len(rawdata), dtype = float)
    total_accepted = np.zeros(len(rawdata), dtype = int)
    for line in rawdata:
        linedata = line.split()
        i = int(linedata[0])
        expectations[i] = [float(d) for d in linedata[2:-1]]
        temperatures[i] = float(linedata[1])
        total_accepted[i] = int(linedata[-1])
    plt.plot(temperatures, total_accepted)
    plt.show()

if __name__ == "__main__":
    read_data('out/example.dat')
