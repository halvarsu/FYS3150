#include "system.h"
#include "velocityverlet.h"
#include "lennardjones.h"
#include "statisticssampler.h"
#include "unitconverter.h"
#include "math/random.h"

System::System()
{

}

System::~System()
{
    for(Atom *atom : m_atoms) {
        delete atom;
    }
    m_atoms.clear();
}

void System::applyPeriodicBoundaryConditions() {
    // Goes through every particle and moves them to the other side of
    // the box if they have left the boundaries
    for (Atom *atom : m_atoms) {
        for (int i = 0; i < 3; i++){
            if (atom->position[i] <= 0){
                atom->position[i] += m_systemSize[i];
                atom->nRelocations[i] += 1;
            } else if (atom->position[i] >= m_systemSize[i]){
                atom->position[i] -= m_systemSize[i];
                atom->nRelocations[i] -= 1;
            }
        }
    }
}

void System::removeTotalMomentum() {
    // Find the total momentum and remove momentum equally on each atom so the total momentum becomes zero.
    vec3 totalMomentum;
    double totalMass;
    for(Atom *atom : m_atoms){
        totalMomentum += atom->velocity * atom->mass();
    }
    for(Atom *atom : m_atoms){
        totalMass += atom->mass();
    }
    for(Atom *atom : m_atoms){
        atom->velocity -= totalMomentum/totalMass;
    }
}

void System::createUnitCell(vec3 R0, double latticeConstant, double temperature){
    // Create 4 new atoms with positions in a Face Centered Cubic unit cell grid
    vector<vec3 *> cellPositions = {new vec3(0,0,0),
                                    new vec3(latticeConstant/2, latticeConstant/2, 0),
                                    new vec3(0, latticeConstant/2, latticeConstant/2),
                                    new vec3(latticeConstant/2, 0, latticeConstant/2)};
    for (vec3* pos : cellPositions){
        Atom *atom	= new Atom(UnitConverter::massFromSI(6.63352088e-26));
        atom->position.set(R0 + *pos);
        atom->initialPosition.set(R0 + *pos);
        m_atoms.push_back(atom);
        atom->resetVelocityMaxwellian(temperature);
    }
}

void System::createFCCLattice(int unitCellsPerDimension, double latticeConstant, double temperature) {
    // Creates N cubed unit cells of a Face Centered Cubic with spacings between cells b,
    // where N is unicCellsPerDimension and b is latticeConstant
    vec3 R0, ones;
    for (int i = 0; i < unitCellsPerDimension; i++){
        for (int j = 0; j < unitCellsPerDimension; j++){
            for (int k = 0; k < unitCellsPerDimension; k++){
                R0.set(i, j, k);
                R0 *= latticeConstant;
                this->createUnitCell(R0, latticeConstant, temperature);
            }
        }
    }

    ones.set(1,1,1);
    setSystemSize(unitCellsPerDimension*latticeConstant*ones);
}

void System::create100Uniform(double temperature) {
    for (int i = 0 ; i < 100; i ++){
        Atom *atom	= new Atom(UnitConverter::massFromSI(6.63352088e-26));
        double x = Random::nextDouble(0, 10); // random number in the interval [0,10]
        double y = Random::nextDouble(0, 10);
        double z = Random::nextDouble(0, 10);
        atom->position.set(x,y,z);
        atom->resetVelocityMaxwellian(temperature);
        m_atoms.push_back(atom);
    }
    setSystemSize(vec3(10, 10, 10));
}

void System::calculateForces() {
    for(Atom *atom : m_atoms) {
        atom->resetForce();
    }
    m_potential.calculateForces(*this); // 'this' is a pointer, '*this' is a reference to that object
}

void System::step(double dt) {
    m_integrator.integrate(*this, dt);
    m_steps++;
    m_time += dt;
}
