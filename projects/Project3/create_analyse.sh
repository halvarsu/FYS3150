#!/bin/bash

N=20

mkdir -p in/stability_analysis/
mkdir -p out/stability_analysis/
rm in/stability_analysis/*
rm out/stability_analysis/*

while [ $N -lt 100000 ]; do
    echo "================ n/yr = $N =================="
    INFOLDER=EarthSun
    INFILE=in/stability_analysis/EarthSun_N${N}.txt
    OUTFILE=out/stability_analysis/EarthSun_N${N}.txt
    echo $OUTFILE
    let N=$N*2
    python analyse/read_horizon.py -F planet_data/$INFOLDER -o $INFILE -y 1 -s $N --use_euler
    ./build/Project3 $INFILE 1 NO_ENERGIES
done

# python analyse/analyse.py -F out/stability_analysis
