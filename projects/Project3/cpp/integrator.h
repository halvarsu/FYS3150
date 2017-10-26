#ifndef INTEGRATOR_H
#define INTEGRATOR_H

#include <string>

// This simple class uses different integrators to evolve a solar system one step at a time.
// Updates energies, forces, velocities and positions of celestial bodies and solar system
class Integrator
{
public:
    double m_dt;
    double m_dt_squared;
    bool m_useEuler;

    Integrator(double dt);
    Integrator(double dt, bool useEuler);
    // many small steps with Euler == a giant step with velocityVerlet (for same accuracy)
    void integrateOneStepEuler(class SolarSystem &system);
    void integrateOneStepVelocityVerlet(class SolarSystem &system);
    void integrateOneStep(class SolarSystem &system);
};

#endif // INTEGRATOR_H
