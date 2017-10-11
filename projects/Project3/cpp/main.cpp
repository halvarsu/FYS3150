#include <iostream>
#include <fstream>
#include <armadillo>
#include "solarsystem.h"
#include "integrators/forwardeuler.h"
#define PI 3.14159265359

using namespace std;

void initialize(arma::mat& pos, arma::mat& vel,
                double x0, double y0,double z0, double vx0, double vy0, double vz0);

void eulerChromer(arma::mat& pos, arma::mat& vel, double dt);
int readInt(string& line, ifstream& infile, int& lineNumber);
void initialiseSystemFromFile(string filename, SolarSystem &system, int& steps, int& years);

int main(int argc, char * argv[]) {
    SolarSystem system = SolarSystem();

    if (argc > 1){
        string filename = (string) argv[1];
        initialiseSystemFromFile(filename, system, 1.);
        return 0;
    }

    return 0;
}

void initialiseSystemFromFile(string filename, SolarSystem &system, int& steps, int& years){
    try {
        ifstream infile;
        int lineNumber = 1;
        int numberOfPlanets;
        double x, y, z, vx, vy, vz, mass;

        infile.open(filename);

        years 			= readInt(line, infile, lineNumber);
        stepsPerYear 	= readInt(line, infile, lineNumber);
        numberOfPlanets	= readInt(line, infile, lineNumber);

        cout << "Reading " << numberOfPlanets << " planets" << endl;

        // Read each planet:
        i++;
        for (int j = 1; j < numberOfPlanets+1; j++){
            string line;
            getline(infile, line);
            cout << "planet " << j + 1 << ": " << line << endl;
            istringstream iss(line);
            if (!(iss >> x >> y >> z >> vx >> vy >> vz >> mass)) { throw i; } // error
            system.createCelestialBody(x,y,z,vx,vy,vz,mass);
            i++;
        }

    } catch (int lineNumber) {
        cout << "Couldn't read line " << lineNumber  << " in file " << filename << endl;
        throw;
    }
}

int readInt(string& line, ifstream& infile, int& lineNumber){
    double out;
    getline(infile, line);
    istringstream iss(line);
    if (!(iss >> out)) { throw lineNumber; } // error
    return out;
}

void initialize(arma::mat& pos, arma::mat& vel,
                double x0, double y0, double z0, double vx0, double vy0, double vz0){
    pos(0,0) = x0;
    pos(0,1) = y0;
    pos(0,2) = z0;
    vel(0,0) = vx0;
    vel(0,1) = vy0;
    vel(0,2) = vz0;
}

void eulerChromer(arma::mat& pos, arma::mat& vel, double dt){
    int n = pos.n_rows;
    cout << n << endl;
    double r;
    double G = 4*PI*PI;

    for (int i = 0; i < n-1; i++) {
        r = sqrt(pos(i,0)*pos(i,0)+ pos(i,1)*pos(i,1) + pos(i,2)*pos(i,2));
        vel(i+1,0) = vel(i,0) - (G*pos(i,0))/(r*r*r)*dt;
        pos(i+1,0) = pos(i,0) + vel(i+1,0)*dt;
        vel(i+1,1) = vel(i,1) - (G*pos(i,1))/(r*r*r)*dt;
        pos(i+1,1) = pos(i,1) + vel(i+1,1)*dt;
        vel(i+1,2) = vel(i,2) - (G*pos(i,2))/(r*r*r)*dt;
        pos(i+1,2) = pos(i,2) + vel(i+1,2)*dt;
    }
}
