#include <iostream>
#include <fstream>
#include <armadillo>
#include <chrono>
#include <iomanip>
#include "solarsystem.h"
#include "celestialbody.h"
#include "integrator.h"
#define PI 3.14159265359

using namespace std;

void initialize(arma::mat& pos, arma::mat& vel,
                double x0, double y0,double z0, double vx0, double vy0, double vz0);

void eulerChromer(arma::mat& pos, arma::mat& vel, double dt);
int readInt(string& line, ifstream& infile, int& lineNumber);
void initialiseSystemFromFile(string filename, SolarSystem &system, int &stepsPerYear, int &years,
                            bool & useEuler);
string getOutFilename(string filename);

int main(int argc, char * argv[]) {
    SolarSystem * system = new SolarSystem();
    int stepsPerYear;
    int years;
    int writeEveryNthStep;
    string filename;
    string outFilename;
    string outInfoFilename;
    bool dontSaveEnergies;
    bool useEuler;


    if (argc > 1){
        filename = (string) argv[1];
        string outFnameBase = getOutFilename(filename);
        outInfoFilename = "out/" + outFnameBase + ".info.txt";
        outFilename = "out/" + outFnameBase + ".bin";

        initialiseSystemFromFile(filename, *system, stepsPerYear, years, useEuler);
        cout << "Initialised system" << endl;
        cout << "Number of bodies: " << system->numberOfBodies() << endl;
        cout << "Fixed sun? " << system->hasFixedSun() << endl;
        cout << "Relativistic Correction? " << system->hasRelativisticCorr() << endl;
        cout << "using forward euler? " << useEuler << endl;
    } else {
        cout << "No arguments! Doing nothing" << endl;
        return 0;
    }
    if (argc > 2) {
        istringstream ss(argv[2]);
        if (!(ss >> writeEveryNthStep)) {
            cerr << "Invalid number " << argv[2] << "\n";
        } else {
            cout << writeEveryNthStep ;
        }

    } else{
        writeEveryNthStep = 1;
    }

    dontSaveEnergies = argc > 3;


    int steps = stepsPerYear*years;
    double dt = 1./stepsPerYear;
    Integrator * integrator = new Integrator(dt, useEuler);

    system->calculateForcesAndEnergy();
    system->calculateAngularMomentum();
    std::ofstream outfile;
    outfile.open(outInfoFilename);
    outfile << years << endl;
    outfile << stepsPerYear << endl;
    outfile << system->hasFixedSun() << endl;
    outfile << system->hasRelativisticCorr() << endl;
    outfile << system->numberOfBodies() << endl;
    // had to change this unnecessary line
    // outfile <<"Kinetic:    Potential:    Total:    AngularMomentum:" << std::endl;
    outfile << useEuler << endl;

    double energy= system->totalEnergy();
    double  kinetic   = system->kineticEnergy();
    double  potential = system->potentialEnergy();
    double  total = system->totalEnergy();
    double  angMom = system->angularMomentum();

    system->writeToFile(outFilename);
    outfile << setprecision(16) << kinetic << " "
            << setprecision(16) << potential << " "
            << setprecision(16) << total <<  " "
            << setprecision(16) << angMom <<  endl;

    string outText;
    int prevLength = 0;
    cout << "STEPS: " << steps << endl;
    auto start = chrono::system_clock::now();

    for(int i = 1; i < steps; i++) {
        integrator->integrateOneStep(*system);
        if (i % writeEveryNthStep == 0) {
            if ((100*i) % (steps) == 0) {
                outText = to_string((100*i)/steps);
                cout << outText << "%" << endl;
                cout << "\033[A" ;//string(prevLength, );
                prevLength = outText.length() + 1;
            }
            system->writeToFile(outFilename);
            if (!dontSaveEnergies){
                system->calculateAngularMomentum();

                kinetic   = system->kineticEnergy();
                potential = system->potentialEnergy();
                total = system->totalEnergy();
                angMom = system->angularMomentum();
                outfile << setprecision(16) << kinetic << " "
                        << setprecision(16) << potential << " "
                        << setprecision(16) << total <<  " "
                        << setprecision(16) << angMom <<  endl;
            }
        }
    }

    auto stop = chrono::system_clock::now();
    chrono::duration<double> elapsed_seconds = stop-start;

    cout << "100% - DONE!" << endl;
    cout << "Used " << elapsed_seconds.count() << " seconds" << endl;
    cout << "Data written to " + outFilename << " and " << outInfoFilename <<  endl;
    outfile.close();
    system->closeFile();
    return 0;
}

void initialiseSystemFromFile(string filename, SolarSystem &system, int & stepsPerYear, int & years,
                              bool & useEuler){
    try {
        ifstream infile;
        string line;
        int lineNumber = 1;
        int numberOfPlanets;
        int fixedSun;
        int relativisticCorrection;
        double x, y, z, vx, vy, vz, mass;

        infile.open(filename);

        years 					= readInt(line, infile, lineNumber);
        stepsPerYear 			= readInt(line, infile, lineNumber);
        fixedSun 				= readInt(line, infile, lineNumber);
        relativisticCorrection 	= readInt(line, infile, lineNumber);
        useEuler			  	= (bool) readInt(line, infile, lineNumber);
        numberOfPlanets	= readInt(line, infile, lineNumber);

        system.setFixedSun((bool)fixedSun);
        system.setRelativistic((bool)relativisticCorrection);

        cout << "Reading " << numberOfPlanets << " bodies.\n"
             << "Data is: x y z vx vy vz mass" << endl;

        // Read each planet:
        lineNumber++;
        for (int j = 1; j < numberOfPlanets+1; j++){
            string line;
            getline(infile, line);
            cout << "planet " << j << ": " << line << endl;
            istringstream iss(line);
            if (!(iss >> x >> y >> z >> vx >> vy >> vz >> mass)) { throw lineNumber; } // error
            system.createCelestialBody(x,y,z,vx,vy,vz,mass);
            lineNumber++;
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

string getOutFilename(string filename){
    // if no delimiter found (gives s.find()=-1), we want pos=0, else we want s.find()+3
    int start = filename.find("in/") + 1;
    int stop = filename.find(".txt");
    if (start != 0) { start += 2; }
    if (stop != -1) { stop -= start; }
    cout << filename << endl;
    cout << start << " " << stop << endl;
    return filename.substr(start, stop);
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
