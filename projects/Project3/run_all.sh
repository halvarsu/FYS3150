#!/bin/bash

echo "================ Running Earth-Sun system =================="
FILE=EarthSunFixed.txt
./build/Project3 in/$FILE
python analyse/analyse.py -f out/$FILE

echo "================ Running fixed Earth-Jupiter-Sun system =================="
FILE=EarthJupiterSunFixed.txt
./build/Project3 in/$FILE
python analyse/analyse.py -f out/$FILE
echo "M_j = 10 M_{j,real}"
FILE=Earth10xJupiterSunFixed.txt
./build/Project3 in/$FILE
python analyse/analyse.py -f out/$FILE
echo "M_j = 1000 M_{j,real}"
FILE=Earth1000xJupiterSunFixed.txt
./build/Project3 in/$FILE
python analyse/analyse.py -f out/$FILE

echo "================ Running Earth-Jupiter-Sun system =================="
FILE=EarthJupiterSun.txt
./build/Project3 in/$FILE
python analyse/analyse.py -f out/$FILE

echo "================ Running full solar system =================="
FILE=Full.txt
./build/Project3 in/$FILE
python analyse/analyse.py -f out/$FILE


echo "================ Running Mercury-Sun system =================="
FILE=MercurySun.txt
./build/Project3 in/$FILE
python analyse/analyse.py -f out/$FILE -p -n 10
