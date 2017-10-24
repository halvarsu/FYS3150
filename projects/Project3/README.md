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

This project consists of a object oriented c++ program for simulating
celestial bodies with a python framework for constructing input files and
analysis the output files. 

### Input files
An input file should be a plain text document with the following lines:
```
    years
    steps per year
    Fixed main body? (0 or 1)
    Relativistic correction? (0 or 1)
    n (number of bodies)
    x y z vx vy vz m (body parameters)
```

where the last line is repeated n times, one for each body. The first body
should be the main body (most massive/closest to origin) if Fixed main body
or Relativistic correction is to be used

- Given a vector-table produced by https://ssd.jpl.nasa.gov/horizons.cgi,
analysis/read_horizon.py can produce the infile needed. only works for the
sun, the 8 planets of the solar system and pluto.
