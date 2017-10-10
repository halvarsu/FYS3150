#include "celestialbody.h"

CelestialBody::CelestialBody(arma::vec pos, arma::vec vel, double mass_) {
    position = pos;
    velocity = vel;
    mass = mass_;
}

CelestialBody::CelestialBody(double x, double y, double z, double vx, double vy, double vz, double mass_){
    // position and velocity are already arma vectors (from header file) and can be initialised with
    // this fancy arma syntax:
    position << x  << y  << z;
    velocity << vx << vy << vz;
    mass = mass_;
}
void CelestialBody::resetForce(){
    force << 0 << 0 << 0;
}
