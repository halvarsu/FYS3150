# coding: utf-8
import numpy as np
a = np.linspace(2,2.3,100)
a
a[1]
dt = a[1] - a[0]
a = np.linspace(2+dt/2,2.3+dt/2,100)
a
np.linspace(2,2.6,200)
a = np.linspace(2,2.6,200)
for i in range(8):
    b = a[i::8]
    
for i in range(8):
    b = a[i::8]
    print(b[0])
    
for i in range(8):
    print(a[len(a)/8)]
    
    
    
for i in range(8):
    print(a[len(a)/8)])
    
    
    
    
for i in range(8):
    print(a[len(a)/8])
    
for i in range(8):
    print(a[i*len(a)/8])
    
for i in range(8):
    print(a[i*len(a)/8])
    
for i in range(8):
    print(a[i*len(a)/8])
    print(a[(i+1)*len(a)/8 - 1])
    
for i in range(8):
    print(a[i*len(a)/8], a[(i+1)*len(a)/8 - 1])
    
for i in range(8):
    print a[i*len(a)/8], a[(i+1)*len(a)/8 - 1]
    
    
for i in range(8):
    start, stop = a[i*len(a)/8], a[(i+1)*len(a)/8 - 1]
    print('mpirun -np 4 ./build/Project4 1000000 %f %f 25 $L 1 0 pt_sub1_L$L verbose' %(start, stop))
    
    
    


    
    
for i in range(8):
    start, stop = a[i*len(a)/8], a[(i+1)*len(a)/8 - 1]
    print('mpirun -np 4 ./build/Project4 1000000 %f %f 25 $L 1 0 pt_sub%d_L$L verbose' %(start, stop, i+1))

    
string = 
string = '''#!/bin/bash

L=40

while [ $L -lt 101 ]; do
    echo "=================== L = $L ========================"
    {}
    let L=$L+20
done
'''
for i in range(8):
    with open('run_pt_sub%d.sh'%(i+1),'w') as outfile:
        start, stop = a[i*len(a)/8], a[(i+1)*len(a)/8 - 1]
        cmd = 'mpirun -np 4 ./build/Project4 1000000 %f %f 25 $L 1 0 pt_sub%d_L$L verbose' %(start, stop, i+1)
        outfile.write(string.format(cmd))

            
    
 
    
for i in range(8):
    with open('run_pt_sub%d.sh'%(i+1),'w') as outfile:
        start, stop = a[i*len(a)/8], a[(i+1)*len(a)/8 - 1]
        cmd = 'mpirun -np 4 ./build/Project4 1000000 %f %f 25 $L 1 0 phase_transitions/pt_sub%d_L$L verbose' %(start, stop, i+1)
        outfile.write(string.format(cmd))
        
