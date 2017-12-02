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
    for (Atom *atom : m_atoms) {
        // atom->position.modEquals(m_systemSize);
        for (int i = 0; i < 3; i++){
            if (atom->position[i] <= 0){
                atom->position[i] += m_systemSize[i];
            } else if (atom->position[i] >= m_systemSize[i]){
                atom->position[i] -= m_systemSize[i];
            }
        }
    }
        // Read here: http://en.wikipedia.org/wiki/Periodic_boundary_conditions#Practical_implementation:_continuity_and_the_minimum_image_convention
}

void System::removeTotalMomentum() {
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
    // Find the total momentum and remove momentum equally on each atom so the total momentum becomes zero.
}

void System::createUnitCell(vec3 R0, double latticeConstant, double temperature){
    Atom *atom1	= new Atom(UnitConverter::massFromSI(6.63352088e-26));
    Atom *atom2 = new Atom(UnitConverter::massFromSI(6.63352088e-26));
    Atom *atom3 = new Atom(UnitConverter::massFromSI(6.63352088e-26));
    Atom *atom4 = new Atom(UnitConverter::massFromSI(6.63352088e-26));
    vec3 pos1(0, 0, 0);
    vec3 pos2(latticeConstant/2, latticeConstant/2, 0);
    vec3 pos3(0, latticeConstant/2, latticeConstant/2);
    vec3 pos4(latticeConstant/2, 0, latticeConstant/2);
    atom1->position.set(R0 + pos1);
    atom2->position.set(R0 + pos2);
    atom3->position.set(R0 + pos3);
    atom4->position.set(R0 + pos4);
    atom1->resetVelocityMaxwellian(temperature);
    m_atoms.push_back(atom1);
    atom2->resetVelocityMaxwellian(temperature);
    m_atoms.push_back(atom2);
    atom3->resetVelocityMaxwellian(temperature);
    m_atoms.push_back(atom3);
    atom4->resetVelocityMaxwellian(temperature);
    m_atoms.push_back(atom4);
}

void System::createFCCLattice(int unitCellsPerDimension, double latticeConstant, double temperature) {
    // You should implement this function properly. Right now, 100 atoms are created uniformly placed in the system of size (10, 10, 10).
    vec3 R0, size;
    for (int i = 0; i < unitCellsPerDimension; i++){
        for (int j = 0; j < unitCellsPerDimension; j++){
            for (int k = 0; k < unitCellsPerDimension; k++){
                R0.set(i, j, k);
                R0 *= latticeConstant;
                this->createUnitCell(R0, latticeConstant, temperature);
            }
        }
    }

    size.set(1,1,1);
    size *= unitCellsPerDimension*latticeConstant;
    setSystemSize(size);
}

void System::calculateForces() {
    for(Atom *atom : m_atoms) {
        atom->resetForce();
    }
    m_potential.calculateForces(*this); // this is a pointer, *this is a reference to this object
}

void System::step(double dt) {
    m_integrator.integrate(*this, dt);
    m_steps++;
    m_time += dt;
}
