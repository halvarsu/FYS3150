#ifndef CELESTIALBODY_H
#define CELESTIALBODY_H

#include <armadillo>
#define ASTRO_G 4*arma::datum::pi*arma::datum::pi

class CelestialBody
{
public:
    // Three dimentional vectors for storing spatial information about the body:
    arma::vec position;
    arma::vec velocity;
    arma::vec force;
    arma::vec prevForce;
    double mass;

    // Two constructors, gives a choice of how to create the celestialBody objects:
    CelestialBody(arma::vec position, arma::vec velocity, double mass);
    CelestialBody(double x, double y, double z, double vx, double vy, double vz, double mass);
    // For setting prevForce to force and force to zero
    void resetForce();
};

#endif // CELESTIALBODY_H
