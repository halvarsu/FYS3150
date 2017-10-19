import numpy as np
import matplotlib.pyplot as plt


x0=1.563246546807631E+00 
y0=5.725226790391031E-01 
z0=5.016658374850980E-02
vx0=-4.244787458165965E-03 
vy0=-1.195685962735690E-02
vz0=-1.465083647294641E-04



filename = 'out/test.txt'

with open(filename, 'r') as infile:
    n_planets = int(infile.readline())

pos = np.loadtxt(filename, skiprows=1, dtype=float)
planets = np.zeros((pos.shape[0]/n_planets, n_planets, pos.shape[1]))
for i in range(n_planets):
    planets[:,i] = pos[i::n_planets]

plt.plot(planets[:,:,1],planets[:,:,0], '-o', markersize =3)
plt.show()
