#!/bin/bash

N=40

FOLDER_EULER=stability_analysis_euler
FOLDER_VERLET=stability_analysis_verlet
mkdir -p in/$FOLDER_EULER
mkdir -p out/$FOLDER_EULER
mkdir -p in/$FOLDER_VERLET
mkdir -p out/$FOLDER_VERLET
rm in/$FOLDER_EULER/*
rm out/$FOLDER_EULER/*
rm in/$FOLDER_VERLET/*
rm out/$FOLDER_VERLET/*

while [ $N -lt 4000000 ]; do
    PLANETSFOLDER=planet_data/EarthSunIdealized
    INFILE1=in/$FOLDER_EULER/EarthSun_N${N}.txt
    INFILE2=in/$FOLDER_VERLET/EarthSun_N${N}.txt
    echo "================ EULER n/yr = $N =================="
    python analyse/read_horizon.py -F $PLANETSFOLDER -o $INFILE1 -y 1 -s $N --use_euler --fixed_sun
    ./build/Project3 $INFILE1 1 NO_ENERGIES
    echo "================ VERLET n/yr = $N =================="
    python analyse/read_horizon.py -F $PLANETSFOLDER -o $INFILE2 -y 1 -s $N --fixed_sun
    ./build/Project3 $INFILE2 1 NO_ENERGIES
    let N=$N*2
done

# python analyse/analyse.py -F out/stability_analysis
