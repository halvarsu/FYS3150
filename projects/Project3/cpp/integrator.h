#ifndef INTEGRATOR_H
#define INTEGRATOR_H

class Integrator
{
public:
    double m_dt;
    Integrator(double dt);
    void integrateOneStep(class SolarSystem &system);
};

#endif // INTEGRATOR_H
