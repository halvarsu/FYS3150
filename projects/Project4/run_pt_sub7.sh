#!/bin/bash

L=40

while [ $L -lt 101 ]; do
    echo "=================== L = $L ========================"
    mpirun -np 4 ./build/Project4 1000000 2.452261 2.524623 24 $L 1 0 phase_transitions/pt_sub7_L$L verbose
    let L=$L+20
done
