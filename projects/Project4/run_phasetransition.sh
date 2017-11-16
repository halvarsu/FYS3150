#!/bin/bash

L=40
while [ $L -lt 101 ]; do
    echo "=================== L = $L ========================"
    mpirun -np 4 ./build/Project4 100000 2 2.3 100 $L 1 0 phasetransL$L verbose
    let L=$L+20
done

