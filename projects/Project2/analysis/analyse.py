import numpy as np
import matplotlib.pyplot as plt

file_dir = "../build-proj2-Desktop_Qt_5_9_1_GCC_64bit-Debug/"

eigval = np.loadtxt(file_dir + "eigval.txt",skiprows=2)
eigvec = np.loadtxt(file_dir + "eigvec.txt",skiprows=2)
r = np.loadtxt(file_dir + "radial_val.txt",skiprows=2)

plt.plot(r,eigvec[2]**2)
plt.show()
