#ifndef SOLARSYSTEM_H
#define SOLARSYSTEM_H

#include <armadillo>
#include "celestialbody.h"
#include <string>
#include <fstream>
#define ASTRO_GRAV_CONST 4*arma::datum::pi*arma::datum::pi // AU**3/yr**2
#define ASTRO_LIGHT_SPEED 63239.7263 // AU/yr

class SolarSystem
{
public:
    // The object constructors:
    SolarSystem();
    SolarSystem(double G_);

    // Three ways of adding bodies to the SolarSystem object:
    // create a body from arma vectors
    void createCelestialBody(arma::vec pos, arma::vec vel, double mass_);
    // create a body from doubles
    void createCelestialBody(double, double, double, double, double, double, double mass_);
    // add an existing body
    void addCelestialBody(const CelestialBody& body);

    // Function for updating all forces in the celestialBody-members of the system and
    // updating the internal (member) variables m_kineticEnergy and m_potentialEnergy:
    // void calculateForcesAndEnergy();
    virtual void calculateForcesAndEnergy();
    virtual void calculateAngularMomentum();

    //
    void setFixedSun(bool) ;
    bool hasFixedSun() const;

    void setRelativistic(bool) ;
    bool hasRelativisticCorr() const;

    // Function for getting how many objects the system has:
    int numberOfBodies() const;

    // Functions for returning member variables (or a sum of them in the totalEnergy()):
    double totalEnergy() const;
    double potentialEnergy() const;
    double kineticEnergy() const;
    double angularMomentum() const;

    // Function for returning the 'list'(vectors in celestialBodies) of the bodies:
    std::vector<CelestialBody> & bodies();

    // Function for writing to file the positions of all celestialBodies.
    // The file is stored in the solar system as a private member variable,
    // and is opened the first time the function is called.
    void writeToFile(std::string filename);

    // To close the file again. Should be done before termination of program:
    void closeFile();


// The private variables of the system. Should be self-explanatory
protected:
    std::vector<CelestialBody> m_bodies;
    std::ofstream m_file;
    bool m_fixedSun = false;
    bool m_relativistic = false;
    double m_kineticEnergy;
    double m_potentialEnergy;
    double m_angularMomentum;
    double m_G; // gravitational constant
    double m_c_0_squared;
};

class TwoBodySystem : public SolarSystem
{
public:
    virtual void calculateForcesAndEnergy();
};

#endif // SOLARSYSTEM_H
