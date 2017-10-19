#ifndef CELESTIALBODY_H
#define CELESTIALBODY_H

#include <armadillo>
#define ASTRO_G 4*arma::datum::pi*arma::datum::pi

class CelestialBody
{
public:
    arma::vec position;
    arma::vec velocity;
    arma::vec force;
    arma::vec prevForce;
    double mass;

    CelestialBody(arma::vec position, arma::vec velocity, double mass);
    CelestialBody(double x, double y, double z, double vx, double vy, double vz, double mass);
    void resetForce();
};

#endif // CELESTIALBODY_H
