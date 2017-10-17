#ifndef FORWARDEULER_H
#define FORWARDEULER_H

// see http://www.cplusplus.com/doc/tutorial/inheritance/
class ForwardEuler
{
public:
    double m_dt;
    ForwardEuler(double dt);
    void integrateOneStep(class SolarSystem &system);
};

#endif // FORWARDEULER_H
