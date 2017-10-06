import numpy as np
import matplotlib.pyplot as plt


pos = np.loadtxt('out/pos.txt', skiprows=2, dtype=float)
vel = np.loadtxt('out/vel.txt', skiprows=2, dtype=float)
plt.scatter(0,0, c='y')
plt.axis('equal')

print(pos.shape)

#plt.plot(pos[:,0],pos[:,1])
plt.plot(vel[:,0],vel[:,1])
plt.show()
