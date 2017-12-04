#!/bin/bash

# Reads temperatures from file, and finishes those not done.

while read -r line || [[ -n "$line"  ]]; do
    echo $line
    read -r -a array <<< $line
    T=${array[0]}
    DONE=${array[1]}
    if [[ -n $DONE ]]; then
        echo Skipping T=$T
    else
        echo Doing T=$T
        mkdir T_$T
        cd T_$T
        /uio/hume/student-u10/halvarsu/uio/FYS3150/projects/Project5/build/molecular-dynamics-fys3150 5 $T 5.26 10000
        cd ..
        sed -i "/${T}/s/$/ DONE/" $1
    fi
done < "$1"
