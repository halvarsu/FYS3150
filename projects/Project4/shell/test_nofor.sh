#!/bin/bash

L=40

while [ $L -lt 101 ]; do
    let NMC=10*$L*$L
    echo "=================== L = $L, NMC = $NMC ========================"
    /usr/lib64/openmpi/bin/mpirun -np 4 ./build/Project4 $NMC 2.000000 2.072362 24 $L 1 0 phase_transitions/test_nofor$L verbose
    let L=$L+20
done
