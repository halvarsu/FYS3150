#ifndef SYSTEM_H
#define SYSTEM_H
#include "atom.h"
#include "math/vec3.h"
#include <vector>
#include "velocityverlet.h"
#include "lennardjones.h"

class System
{
private:
    vec3 m_systemSize;
    vec3 m_systemSizeHalf;
    VelocityVerlet m_integrator;
    std::vector<Atom*> m_atoms;
    LennardJones m_potential;
    double m_time = 0;
    int m_steps = 0;

public:
    System();
    ~System();
    void createUnitCell(vec3 R0, double latticeConstant, double temperature);
    void createFCCLattice(int numberOfUnitCellsEachDimension, double latticeConstant, double temperature);
    void create100Uniform(double temperature);
    void applyPeriodicBoundaryConditions();
    void removeTotalMomentum();
    void calculateForces();
    void step(double dt);

    // Setters and getters
    std::vector<Atom *> &atoms() { return m_atoms; } // Returns a reference to the std::vector of atom pointers
    double volume() { return m_systemSize[0]*m_systemSize[1]*m_systemSize[2]; }
    vec3 systemSize() { return m_systemSize; }
    vec3 systemSizeHalf() { return m_systemSizeHalf; }
    void setSystemSize(vec3 systemSize) { m_systemSize = systemSize; m_systemSizeHalf = systemSize/2;}
    LennardJones &potential() { return m_potential; }
    double time() { return m_time; }
    void setTime(double time) { m_time = time; }
    VelocityVerlet &integrator() { return m_integrator; }
    int steps() { return m_steps; }
    void setSteps(int steps) { m_steps = steps; }
};
#endif
