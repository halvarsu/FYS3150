import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0,2*np.pi,1000)


def x(t):
    return -8/5*np.sin(11/10 - 43*t) - 6/5*np.sin(6/5 - 41*t) - 29/7*np.sin(4/3 - 39*t) - 10/3*np.sin(7/5 - 36*t) - 41/10*np.sin(2/5 - 34*t) - 11/5*np.sin(23/22 - 30*t) - 33/5*np.sin(2/3 - 28*t) - 10/3*np.sin(5/6 - 25*t) - 44/5*np.sin(1/3 - 21*t) - 83/7*np.sin(8/7 - 12*t) - 276/5*np.sin(6/5 - 4*t) + 2/3*np.sin(42*t) + 852/5*np.sin(t + 21/5) + 125*np.sin(2*t + 3/5) + 994/5*np.sin(3*t + 4/5) + 592/7*np.sin(5*t + 19/5) + 34*np.sin(6*t + 11/3) + 20*np.sin(7*t + 8/7) + 102/5*np.sin(8*t + 2) + 67/3*np.sin(9*t + 1/3) + 122/5*np.sin(10*t + 9/4) + 95/3*np.sin(11*t + 8/9) + 37/2*np.sin(13*t + 6/7) + 25/2*np.sin(14*t + 4/3) + 47/5*np.sin(15*t + 1/4) + 46/3*np.sin(16*t + 9/4) + 15/4*np.sin(17*t + 22/5) + 127/14*np.sin(18*t + 11/3) + 11/2*np.sin(19*t + 85/21) + 28/3*np.sin(20*t + 1/5) + 23/3*np.sin(22*t + 17/4) + 19/3*np.sin(23*t + 5/4) + 12/5*np.sin(24*t + 15/4) + 17/6*np.sin(26*t + 14/3) + 25/12*np.sin(27*t + 5/4) + 28/5*np.sin(29*t + 10/9) + 5/4*np.sin(31*t + 17/7) + 21/5*np.sin(32*t + 4/3) + 3*np.sin(33*t + 11/3) + 3*np.sin(35*t + 13/4) + np.sin(37*t + 2/5) + 39/19*np.sin(38*t + 10/7) + 9/5*np.sin(40*t + 12/5)
def y(t): 
    return -7/4*np.sin(1/9 - 39*t) - 2/5*np.sin(4/5 - 35*t) - 11/4*np.sin(5/4 - 33*t) - 2*np.sin(2/5 - 26*t) - 13/2*np.sin(3/7 - 24*t) - 153/7*np.sin(1/7 - 6*t) - 231/5*np.sin(3/7 - 5*t) - 1023/5*np.sin(7/5 - t) + 116/9*np.sin(4*t) + 2*np.sin(41*t) + 562/5*np.sin(2*t + 4/3) + 367/4*np.sin(3*t + 11/4) + 38/3*np.sin(7*t + 17/4) + 104/3*np.sin(8*t + 53/13) + 401/10*np.sin(9*t + 9/4) + 119/8*np.sin(10*t + 17/4) + 161/10*np.sin(11*t + 7/3) + 44/5*np.sin(12*t + 17/4) + 111/4*np.sin(13*t + 14/5) + 83/5*np.sin(14*t + 8/3) + 5*np.sin(15*t + 1/3) + 119/6*np.sin(16*t + 29/7) + 32/5*np.sin(17*t + 25/6) + 4*np.sin(18*t + 1/4) + 9*np.sin(19*t + 2/5) + 13/5*np.sin(20*t + 1/3) + 44/9*np.sin(21*t + 2) + 14/5*np.sin(22*t + 46/15) + 17/3*np.sin(23*t + 9/4) + 11/6*np.sin(25*t + 17/4) + 23/3*np.sin(27*t + 7/4) + 17/4*np.sin(28*t + 3/4) + 18/5*np.sin(29*t + 19/5) + 24/5*np.sin(30*t + 18/7) + 16/5*np.sin(31*t + 13/3) + 9/5*np.sin(32*t + 3/2) + 35/17*np.sin(34*t + 2/5) + 5/3*np.sin(36*t + 4/3) + 7/5*np.sin(37*t + 1/19) + 11/4*np.sin(38*t + 11/3) + 1/3*np.sin(40*t + 19/9) + 1/4*np.sin(42*t + 5/4) + 11/6*np.sin(43*t + 13/7)
        
duck_x = x(t)
duck_y = y(t)
duck_x /= np.max(duck_x)

plt.xlabel('DUCK')
plt.ylabel('DUCK')
plt.plot(x(t), y(t))
plt.axis('equal')
plt.savefig('duck.pdf')
plt.show()
