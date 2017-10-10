#ifndef SOLARSYSTEM_H
#define SOLARSYSTEM_H

#include <armadillo>
#include "celestialbody.h"
#include <string>
#include <fstream>

class SolarSystem
{
public:
    SolarSystem();
    void createCelestialBody(arma::vec pos, arma::vec vel, double mass_);
    void createCelestialBody(double, double, double, double, double, double, double mass_);
    void calculateForcesAndEnergy();
    void addCelestialBody(const CelestialBody& body);
    int numberOfBodies() const;

    double totalEnergy() const;
    double potentialEnergy() const;
    double kineticEnergy() const;
    void writeToFile(std::string filename);
    std::vector<CelestialBody> &bodies();

private:
    std::vector<CelestialBody> m_bodies;
    std::ofstream m_file;
    double m_kineticEnergy;
    double m_potentialEnergy;
};

#endif // SOLARSYSTEM_H
