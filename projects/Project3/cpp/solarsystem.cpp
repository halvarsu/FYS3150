#include "solarsystem.h"
#include <iostream>
#include <iomanip>
using namespace std;

// some kind of magical c++ syntax for declaring attributes (member variables) in the constructor:
SolarSystem::SolarSystem(double G_)
{
    m_kineticEnergy = 0;
    m_potentialEnergy = 0;
    m_G = G_;
}

SolarSystem::SolarSystem()
{
    m_kineticEnergy = 0;
    m_potentialEnergy = 0;
    m_G = ASTRO_GRAV_CONST;
}

void SolarSystem::createCelestialBody(arma::vec position, arma::vec velocity, double mass) {
    m_bodies.push_back( CelestialBody(position, velocity, mass) );
}

void SolarSystem::createCelestialBody(double x, double y, double z, double vx, double vy, double vz, double mass_) {
    m_bodies.push_back( CelestialBody(x,y,z,vx,vy,vz, mass_) );
}


void SolarSystem::addCelestialBody(const CelestialBody& body){
    m_bodies.push_back( body );
}


void SolarSystem::calculateForcesAndEnergy()
{
    m_kineticEnergy = 0;
    m_potentialEnergy = 0;

    for(CelestialBody &body : m_bodies) {
        // Reset forces on all bodies, also updating prevForce
        body.resetForce();
    }


    int i;
    // Sun should be first celestial body
    for(; i<numberOfBodies(); i++) {
        CelestialBody &body1 = m_bodies[i];

        for(int j=i+1; j<numberOfBodies(); j++) {
            CelestialBody &body2 = m_bodies[j];
            arma::vec deltaRVector = body1.position - body2.position;
            // calculate norm of vector as \sqrt{\sum_i{x_i^2}}
            double dr = arma::norm(deltaRVector);

            double force = m_G*body1.mass*body2.mass/(dr*dr);
            arma::vec forceVector = force*deltaRVector/dr;
            body1.force -= forceVector;
            body2.force += forceVector;
            m_potentialEnergy -= force * dr;
        }

        double vel_squared = arma::dot(body1.velocity, body1.velocity);
        m_kineticEnergy += 0.5*body1.mass*vel_squared;
    }
}

void SolarSystem::setFixedSun(bool isFixed) {
    m_fixedSun = isFixed;
}
bool SolarSystem::hasFixedSun() const{
    return m_fixedSun;
}

int SolarSystem::numberOfBodies() const
{
    return m_bodies.size();
}

double SolarSystem::totalEnergy() const
{
    return m_kineticEnergy + m_potentialEnergy;
}

double SolarSystem::potentialEnergy() const
{
    return m_potentialEnergy;
}

double SolarSystem::kineticEnergy() const
{
    return m_kineticEnergy;
}

void SolarSystem::writeToFile(string filename)
{
    if(!m_file.good() || !m_file.is_open()) {
        m_file.open(filename.c_str(), ofstream::out);
        m_file << numberOfBodies() << endl;
        if(!m_file.good()) {
            cout << "Error opening file " << filename << ". Aborting!" << endl;
            terminate();
        }
    }

    int i = 0;
    for (CelestialBody &body : m_bodies) {
        m_file << setprecision(10) << body.position(0) << " "
               << setprecision(10) << body.position(1) << " "
               << setprecision(10) << body.position(2) << endl;
        i++;
    }
}

void SolarSystem::closeFile(){
    m_file.close();
}

std::vector<CelestialBody> &SolarSystem::bodies()
{
    return m_bodies;
}
