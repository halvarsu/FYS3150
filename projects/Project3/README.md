# Project 3

## Setup

This project uses [Qt creator](https://www1.qt.io/download/ "Qt creator download") for project management and building.

To setup, you need to configure your project manually.  After git clone, open Project3 in qt creator. Then do the following: 
- under Projects/Run/Deployment/ add a custom buildstep with the following parameters:

```
    Command: mkdir
    Arguments: -p out
    Working directory: %{buildDir}
```

- under Projects/Run/Run/: set Working Directory to the project folder,

## Running

After compiling, run main program from this folder, with an input file as first argument. Second and third arguments are also possible: the second should be an int, specifing how often the program should print to file, and the third argument will, if present (can be anything), disable saving of energy to file. 

Two output files are then produces in `out`, a binary file containing positions, and a text file containing information about the simulation and energies. 

The analysis script `analyse/analyse.py` analyses these files with `-f` argument. See `-h` argument for more options.


### Input files
An input file should be a plain text document with the following lines:
```
    years
    steps per year
    Fixed main body? (0 or 1)
    Relativistic correction? (0 or 1)
    Use Forward Euler? (0 or 1) 
    n (number of bodies)
    x y z vx vy vz m (body parameters)
```

where the last line is repeated n times, one for each body. NOTE: The first body
should be the main body (most massive/closest to origin) if Fixed main body
or Relativistic correction is to be used

#### Creating input
- `analysis/read_horizon.py` produces an infile, given a vector-table produced by https://ssd.jpl.nasa.gov/horizons.cgi. O
Currently only works for the sun, the 8 planets of the solar system and pluto. See `-h` argument for more options.

