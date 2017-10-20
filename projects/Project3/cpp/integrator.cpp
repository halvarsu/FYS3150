#include "integrator.h"
#include "celestialbody.h"
#include "solarsystem.h"


Integrator::Integrator(double dt) : m_dt(dt) {}

void Integrator::integrateOneStepEuler(SolarSystem &system){
    system.calculateForcesAndEnergy();
    for (CelestialBody &body : system.bodies()){
        body.position += body.velocity * m_dt;
        body.velocity += body.force / body.mass * m_dt;
    }
    if (system.hasFixedSun()) {
        system.bodies()[0].position << 0 << 0 << 0;
    }
}

void Integrator::integrateOneStepVelocityVerlet(SolarSystem &system){
    for (CelestialBody &body : system.bodies()){
        body.position += m_dt * body.velocity  + 0.5*m_dt*m_dt*(body.force / body.mass) ;
    }

    system.calculateForcesAndEnergy();

    for (CelestialBody &body : system.bodies()){
        body.velocity += m_dt * 0.5 * (body.force + body.prevForce) / body.mass;
    }

    if (system.hasFixedSun()) {
        system.bodies()[0].position << 0 << 0 << 0;
    }
}
