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
    m_relativistic = true;
}

SolarSystem::SolarSystem()
{
    m_kineticEnergy = 0;
    m_potentialEnergy = 0;
    m_G = ASTRO_GRAV_CONST;
    m_c_0_squared = ASTRO_LIGHT_SPEED*ASTRO_LIGHT_SPEED;
    m_relativistic = true;
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
    // Main body should be first celestial body
    for(; i<numberOfBodies(); i++) {
        CelestialBody &body1 = m_bodies[i];

        for(int j=i+1; j<numberOfBodies(); j++) {
            CelestialBody &body2 = m_bodies[j];
            arma::vec deltaRVector = body1.position - body2.position;
            // calculate norm of vector as \sqrt{\sum_i{x_i^2}}
            double dr = arma::norm(deltaRVector);

            double force = m_G*body1.mass*body2.mass/(dr*dr);
            arma::vec forceVector = force*deltaRVector/dr;
            if (m_relativistic) {
                // Dont calculate for main body:
                if (i != 0) {
                    double l1 = arma::norm(arma::cross(body1.position,body1.velocity));
                    double r1 = arma::norm(body1.position);
                    body1.force -= forceVector*(1+3*l1*l1/(r1*r1*m_c_0_squared));
                } else {
                    body1.force -= forceVector;
                }
                double l2 = arma::norm(arma::cross(body2.position,body2.velocity));
                double r2 = arma::norm(body2.position);
                // Correction is assumed to be around barycenter
                body2.force += forceVector*(1+3*l2*l2/(r2*r2*m_c_0_squared));
            } else {
                body1.force -= forceVector;
                body2.force += forceVector;
            }
            m_potentialEnergy -= force * dr;
        }

        double vel_squared = arma::dot(body1.velocity, body1.velocity);
        m_kineticEnergy += 0.5*body1.mass*vel_squared;
    }
    if (m_fixedSun) {
        m_bodies[0].force << 0 << 0 << 0;
    }
}

void TwoBodySystem::calculateForcesAndEnergy()
{
    // Assumes two bodies, where one is a fixed massive object with mass defined by
    // the gravitational constant such that M_{massive} = 1.
    m_kineticEnergy = 0;
    m_potentialEnergy = 0;

    for(CelestialBody &body : m_bodies) {
        // Reset forces on all bodies, also updating prevForce
        body.resetForce();
    }

    // Sun should be first celestial body, and should be fixed at (0,0,0)
    CelestialBody &body1 = m_bodies[0];
    CelestialBody &body2 = m_bodies[1];

    // calculate norm of vector as \sqrt{\sum_i{x_i^2}}
    double r = arma::norm(body1.position);
    double force = m_G*body1.mass*body2.mass/(r*r);

    if (m_relativistic) {
        double l = arma::norm(body2.angularMomPerMass);
        force *= (1+3*l*l/(r*r*m_c_0_squared));
    }

    body2.force += force*body1.position/r;
    m_potentialEnergy -= force * r;
    double vel_squared = arma::dot(body1.velocity, body1.velocity);
    m_kineticEnergy += 0.5*body1.mass*vel_squared;
}

void SolarSystem::setFixedSun(bool isFixed) {
    m_fixedSun = isFixed;
}
bool SolarSystem::hasFixedSun() const{
    return m_fixedSun;
}

void SolarSystem::setRelativistic(bool isRelativistic) {
    m_relativistic = isRelativistic;
}
bool SolarSystem::hasRelativisticCorr() const{
    return m_relativistic;
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

