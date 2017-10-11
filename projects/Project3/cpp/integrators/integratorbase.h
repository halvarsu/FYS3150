#ifndef INTEGRATORBASE_H
#define INTEGRATORBASE_H


class IntegratorBase
{
public:
    IntegratorBase(double dt);
    virtual void integrateOneStep(class SolarSystem &system);
    // see http://www.studytonight.com/cpp/virtual-functions.php
private:
    double m_dt;
};

#endif // INTEGRATORBASE_H
