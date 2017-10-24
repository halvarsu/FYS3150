import random as ran
import numpy as np
import matplotlib.pyplot as plt


# making random elliptic orbit
N = 1000
r = np.zeros((2,N))
t = np.linspace(0,2*np.pi,N)
for i in range(N):
	r[0,i] = np.sin(t[i])
	r[1,i] = ran.uniform(.4,.6)*np.cos(t[i])
	

# saving smallest distances and the smallest distancce index
list_of_min_points = []
min_dist = 1e24
for i in range(N):
	dist = np.linalg.norm(r[:,i])
	if dist < min_dist:
		min_dist = dist
		list_of_min_points.append(r[:,i])
		index_smallest = i
		print min_dist, i
print list_of_min_points[:]
i_s = index_smallest

# from radians to degrees with correct +/-
theta =np.arccos(r[0,i_s]/min_dist)*360/(2*np.pi)
print theta
if r[0,i_s] < 0 and r[1,i_s] > 0:
	print "-x  +y"
	theta = theta
elif r[0,i_s] < 0 and r[1,i_s] < 0:
	print "-x  -y"
	theta = 360-theta
elif r[0,i_s] > 0 and r[1,i_s] < 0:
	print "+x  -y"
	theta = 360-theta
else:
	theta = theta

print theta,"degrees"

x, y = [0, r[0,i_s]], [0, r[1,i_s]]
plt.plot(x, y, marker = 'o')
plt.legend([theta,"degrees"])
plt.plot(r[0,:],r[1,:])
plt.axis("equal")
plt.show()
