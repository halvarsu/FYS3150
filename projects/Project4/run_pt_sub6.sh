#!/bin/bash

L=40

while [ $L -lt 101 ]; do
    echo "=================== L = $L ========================"
    mpirun -np 4 ./build/Project4 1000000 2.376884 2.449246 25 $L 1 0 phase_transitions/pt_sub6_L$L verbose
    let L=$L+20
done
