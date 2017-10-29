import numpy as np
import matplotlib.pyplot as plt

class Planet:	
	def __init__(self,x0,y0,v_init,run_years=4,NperY=10000):
		self.x0 = x0
		self.y0 = y0
		self.v_init = v_init
		self.dt = float(run_years)/NperY
		self.N = int(NperY*run_years)
		self.pos = np.zeros((2,self.N))
		self.vel = np.zeros((2,self.N))

	def coordinates(self):
		N  = self.N
		dt = self.dt
		self.pos[0,0] = self.x0
		self.vel[1,0] = self.v_init
		for i in range(N-1):
			a = -4*np.pi*np.pi/(np.sqrt(self.pos[0,i]**2+self.pos[1,i]**2)**3)*self.pos[:,i]
			self.vel[:,i+1] = self.vel[:,i] + a*dt
			self.pos[:,i+1] = self.pos[:,i] + self.vel[:,i+1]*dt
		return self.pos, self.vel

# plotting real orbit for reference
text = "%.3f $\cdot V_{Earth}$"  % (1.)
orbit = Planet(1,0,2*np.pi)
x_k , v_k = orbit.coordinates()[0] , orbit.coordinates()[1]
plt.plot(x_k[0],x_k[1],label = text)

# plotting 12 different velocities
n = 12
v_init = np.linspace(2.5*np.pi,3*np.pi,n)
for v in v_init:
    print v
    text = "%.3f $\cdot V_{Earth}$"  % (v/(2*np.pi))
    orbit = Planet(1,0,v)
    x_k , v_k = orbit.coordinates()[0] , orbit.coordinates()[1]
    plt.plot(x_k[0],x_k[1],label = text)

plt.axis('equal')
plt.scatter(0,0,s=100,c='y',marker='*')
plt.legend()
plt.xlabel("x [AU]")
plt.ylabel("y [AU]")
plt.show()



