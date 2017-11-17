#!/bin/bash

L=40

while [ $L -lt 101 ]; do
    echo "=================== L = $L ========================"
    /usr/lib64/openmpi/bin/mpirun -np 4 ./build/Project4 1500000 2.300524 2.324607 24 $L 1 0 phase_transitions/pt_sub5_L$L_HD verbose
    let L=$L+20
done
