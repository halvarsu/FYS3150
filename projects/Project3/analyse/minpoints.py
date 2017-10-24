import random as ran
import numpy as np
import matplotlib.pyplot as plt

# making random ellipticish orbit
N = 1000
r = np.zeros((3,N))
t = np.linspace(0,2*np.pi,N)
for i in range(N):
	r[0,i] = np.sin(t[i])
	r[1,i] = ran.uniform(.4,.6)*np.cos(t[i])
	
# saving smallest distances and the smallest distancce index
min_dist = 1e24
for i in range(N):
	dist = np.linalg.norm(r[:,i])
	if dist < min_dist:
		min_dist = dist
		min_x,min_y,min_z = r[0,i],r[1,i],r[2,i]
		ind = i # index for 

# from radians to degrees with correct +/-
theta =np.arccos(r[0,ind]/min_dist)*360/(2*np.pi)
if r[0,ind] < 0 and r[1,ind] > 0:
	theta = theta
elif r[0,ind] < 0 and r[1,ind] < 0:
	theta = 360-theta
elif r[0,ind] > 0 and r[1,ind] < 0:
	theta = 360-theta
else:
	theta = theta

print "angle is ",theta,"degrees"
print "coordinates are"
print "x:",min_x
print "y:",min_y
print "z:",min_z
x, y = [0, r[0,ind]], [0, r[1,ind]]
plt.plot(x, y, marker = 'o')
plt.legend([theta,"degrees"])
plt.plot(r[0,:],r[1,:])
plt.axis("equal")
plt.show()
