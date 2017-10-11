#include "forwardeuler.h"
#include "celestialbody.h"
#include "solarsystem.h"

void ForwardEuler::integrateOneStep(SolarSystem &system){
    for (CelestialBody &body : system.bodies()){
        body.position += body.velocity * m_dt;
        body.velocity += body.force / body.mass * m_dt;
    }
}
