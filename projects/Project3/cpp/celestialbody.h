#ifndef CELESTIALBODY_H
#define CELESTIALBODY_H

#include <armadillo>

class CelestialBody
{
public:
    arma::vec position;
    arma::vec velocity;
    arma::vec force;
    double mass;
    double G;

    CelestialBody(arma::vec position, arma::vec velocity, double mass);
    CelestialBody(double x, double y, double z, double vx, double vy, double vz, double mass);
    void resetForce();
};

#endif // CELESTIALBODY_H
