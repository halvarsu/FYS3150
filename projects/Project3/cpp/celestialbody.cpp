#include "celestialbody.h"
#include <armadillo>

CelestialBody::CelestialBody(arma::vec pos, arma::vec vel, double mass_) {
    // Uses astronomical units (with G = 4pi) as default!
    position = pos;
    velocity = vel;
    angularMomPerMass = arma::cross(position, velocity);
    mass = mass_;
}

CelestialBody::CelestialBody(double x, double y, double z, double vx, double vy, double vz, double mass_){
    // position and velocity are already arma vectors (from header file) and can be initialised with
    // this fancy arma syntax:
    position << x << arma::endr << y << arma::endr << z;
    velocity << vx << arma::endr<< vy<< arma::endr << vz;
    angularMomPerMass = arma::cross(position, velocity);
    mass = mass_;
}
void CelestialBody::resetForce(){
    prevForce = force;
    force << 0 << arma::endr<< 0 << arma::endr<< 0;
}
