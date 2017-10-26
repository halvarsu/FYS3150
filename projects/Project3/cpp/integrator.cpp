#include "integrator.h"
#include "celestialbody.h"
#include "solarsystem.h"
#include <functional>

using namespace std::placeholders;

Integrator::Integrator(double dt, bool useEuler) :
    m_dt(dt),
    m_dt_squared(dt*dt),
    m_useEuler(useEuler)
{
}

Integrator::Integrator(double dt) :
    m_dt(dt),
    m_dt_squared(dt*dt),
    m_useEuler(false)
{
//    if (kind == "euler") {
//        Integrator::integrate = std::bind(&Integrator::integrateOneStepEuler, _1);
//    } else if (kind == "velocityVerlet"){
//        Integrator::integrate = std::bind(&Integrator::integrateOneStepVelocityVerlet, _1);
//    } else {
//        std::cout << "Invalid integrator kind " << kind << std::endl;
//        std::terminate();
//    }
}


void Integrator::integrateOneStep(SolarSystem &system){
    if (m_useEuler) {
        Integrator::integrateOneStepEuler(system);
    } else {
        Integrator::integrateOneStepVelocityVerlet(system);
    }
}

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
        body.position += m_dt * body.velocity  + 0.5*m_dt_squared*(body.force / body.mass) ;
    }

    system.calculateForcesAndEnergy();

    for (CelestialBody &body : system.bodies()){
        body.velocity += m_dt * 0.5 * (body.force + body.prevForce) / body.mass;
    }

    if (system.hasFixedSun()) {
        system.bodies()[0].position << 0 << 0 << 0;
    }
}
