# coding: utf-8
import numpy as np

a = np.linspace(2.2,2.4,192)
    
for i in range(8):
    print a[i*len(a)/8], a[(i+1)*len(a)/8 - 1]

    
string = '''#!/bin/bash

L=40

while [ $L -lt 101 ]; do
    echo "=================== L = $L ========================"
    {}
    let L=$L+20
done
'''
for i in range(8):
    with open('shell/run_pt_sub%d_HD.sh'%(i+1),'w') as outfile:
        start, stop = a[i*len(a)/8], a[(i+1)*len(a)/8 - 1]
        cmd = '/usr/lib64/openmpi/bin/mpirun -np 4 ./build/Project4 1500000 %f %f 24 $L 1 0 phase_transitions/pt_sub%d_L$L_HD verbose' %(start, stop, i+1)
        outfile.write(string.format(cmd))
