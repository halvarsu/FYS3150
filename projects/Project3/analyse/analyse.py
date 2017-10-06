import numpy as np
import matplotlib.pyplot as plt


x = np.loadtxt('out/posx', skiprows=2, dtype=float)
y = np.loadtxt('out/posy', skiprows=2, dtype=float)
vx = np.loadtxt('out/velx', skiprows=2, dtype=float)
vy = np.loadtxt('out/vely', skiprows=2, dtype=float)
plt.scatter(0,0, c='y')
plt.axis('equal')

plt.plot(x,y)
plt.show()
