#include "integrator.h"
#include "celestialbody.h"
#include "solarsystem.h"


Integrator::Integrator(double dt) : m_dt(dt) {}

void Integrator::integrateOneStep(SolarSystem &system){
    for (CelestialBody &body : system.bodies()){
        body.position += body.velocity * m_dt;
        body.velocity += body.force / body.mass * m_dt;
    }
}
