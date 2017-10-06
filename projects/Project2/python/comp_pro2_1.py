import numpy as np
import matplotlib.pyplot as plt
import sys

N  = 100

# defining step size
rho_start = 0
rho_end = 5
h = float(rho_end-rho_start)/N

omega = 1

# making matrix A
A = np.zeros((N,N))
V = np.zeros(N)
for i in range(N):
	rho = (i+1)*h
	V[i] = rho**2*omega**2
#	V[i] = rho**2+1/rho
	d = 2.0/h**2 + V[i]
	e = -1.0/h**2
# inserting the three diagonal element series
	A[i,i] = d
	if i > 0: 
		A[i,i-1] = e
	if i < N-1:
		A[i,i+1] = e

# finding the largest number above the diagonal
def find_largest(A,N):
	largest = 0
	k,l=0,0
	for i in range(N):
		for j, value in enumerate(A[i,i+1:]):
			if abs(value) > largest:
				largest = abs(value)
				k,l=i,j+i+1	
	return largest,k,l

# finding sin and cos
def s_c(A,k,l):
	tau = (A[l,l]-A[k,k])/float((2.0*A[k,l]))
	if(tau >= 0 ):
		t = 1.0/(tau+np.sqrt(1+tau**2))
	else:
		t = -1.0/(-tau+np.sqrt(1+tau**2))
	c = 1.0/np.sqrt(1.0+t**2)
	s = t*c
	return s,c


# making diagonal matrix B from A
def matB(A,N,n):
	B = np.copy(A)
	for j in range(n):
		largest, k, l = find_largest(B,N)
		if abs(largest) < 1e-8:
			print "exit",j
			return np.sort(np.diagonal(B))
			
		s,c = s_c(B,k,l)
		b_kk, b_ll = B[k,k], B[l,l]
		B[k,k] = b_kk*c**2-2*B[k,l]*c*s+b_ll*s**2
		B[l,l] = b_ll*c**2+2*B[k,l]*c*s+b_kk*s**2
		B[k,l] = 0 
		B[l,k] = 0 
		for i in range(N):
			if i != k and i!= l:
				b_il, b_ik = B[i,l], B[i,k]
				B[i,k] = b_ik*c - b_il*s
				B[k,i] = B[i,k]
				B[i,l] = b_il*c + b_ik*s
				B[l,i] = B[i,l]
				
	return np.sort(np.diagonal(B))

sorted_eig_B = matB(A,N,100000)

# my calculated eigenvalues
print sorted_eig_B

# letting numpy calculate values
eig,eigv = np.linalg.eig(A)		
print np.sort(eig)

# testing calculated eigenvalues to exact ones
B_eig = np.copy(sorted_eig_B)
def testone(B,A):
	eig,eigv = np.linalg.eig(A)
	calcu = B
	exact = np.sort(eig)
	tol = 1e-5
	for i in range(N):
		if np.abs(float(calcu[i]-exact[i])) > tol:
			print "Eigenvalue number ",i+1," has a larger error than",tol,". The error is ",np.abs(float(calcu[i]-exact[i]))
		
B_eig[0] = 4
testone(B_eig,A)

plt.plot(eigv)
plt.show()

