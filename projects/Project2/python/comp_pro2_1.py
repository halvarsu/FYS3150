import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import hbar
import sys

N  = 5
k = 4

# defining step size
rho_start = 0
rho_end = 5
h = float(rho_end-rho_start)/N

hbar = 1

# making matrix A
A = np.zeros((N,N))
V = np.zeros(N)
for i in range(N):
	rho = i*h
	V[i] = .5*k*rho**2
	d = 2.0/hbar**2 + V[i]
	e = -1.0/hbar**2
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
k = find_largest(A,N)[1]
l = find_largest(A,N)[2]
def s_c(A,k,l):
	tau = (A[l,l]-A[k,k])/float((2.0*A[k,l]))
	if(tau >= 0 ):
		t = 1.0/(tau+np.sqrt(1+tau**2))
	else:
		t = -1.0/(-tau+np.sqrt(1+tau**2))
	c = 1.0/np.sqrt(1.0+t**2)
	s = t*c
	return s,c

# making matrix B
B = np.copy(A)
s = s_c(A,k,l)[0]
c = s_c(A,k,l)[1]
B[k,k] = A[k,k]*c**2-2*A[k,l]*c*s+A[l,l]*s**2
B[l,l] = A[l,l]*c**2+2*A[k,l]*c*s+A[k,k]*s**2
B[k,l] = 0 #(A[k,k]-A[l,l])*c*s + A[k,l]*(c**2-s**2)
B[l,k] = 0 
for i in range(N):
	if i != k and i!= l:
		B[i,k] = A[i,k]*c - A[i,l]*s
		B[k,i] = B[i,k]
		B[i,l] = A[i,l]*c - A[i,k]*s
		B[l,i] = B[i,l]
#print B


def matB(A,N,n):
	B = np.copy(A)
	for i in range(n):
		_, k, l = find_largest(B,N)

		s = s_c(B,k,l)[0]
		c = s_c(B,k,l)[1]
		B[k,k] = B[k,k]*c**2-2*B[k,l]*c*s+B[l,l]*s**2
		B[l,l] = B[l,l]*c**2+2*B[k,l]*c*s+B[k,k]*s**2
		B[k,l] = 0 #(A[k,k]-A[l,l])*c*s + A[k,l]*(c**2-s**2)
		B[l,k] = 0 
		for i in range(N):
			if i != k and i!= l:
				B[i,k] = B[i,k]*c - B[i,l]*s
				B[k,i] = B[i,k]
				B[i,l] = B[i,l]*c - B[i,k]*s
				B[l,i] = B[i,l]
	return B

print matB(A,N,40)	










