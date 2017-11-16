#!/bin/bash

L=40

while [ $L -lt 101 ]; do
    echo "=================== L = $L ========================"
    /usr/lib64/openmpi/bin/mpirun -np 4 ./build/Project4 1000000 2.000000 2.072362 24 $L 1 0 phase_transitions/pt_sub1_L$L verbose
    let L=$L+20
done
