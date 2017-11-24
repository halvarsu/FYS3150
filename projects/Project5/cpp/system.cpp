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
        atom->position.modEquals(m_systemSize);
    }
        // Read here: http://en.wikipedia.org/wiki/Periodic_boundary_conditions#Practical_implementation:_continuity_and_the_minimum_image_convention
}

void System::removeTotalMomentum() {
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

void System::createFCCLattice(int unitCellsPerDimention, double latticeConstant, double temperature) {
    // You should implement this function properly. Right now, 100 atoms are created uniformly placed in the system of size (10, 10, 10).
    vec3 R0, size;
    for (int i = 0; i < unitCellsPerDimention; i++){
        for (int j = 0; j < unitCellsPerDimention; j++){
            for (int k = 0; k < unitCellsPerDimention; k++){
                R0.set(i, j, k);
                R0 *= latticeConstant;
                this->createUnitCell(R0, latticeConstant, temperature);
            }
        }
    }

    size.set(1,1,1);
    size *= unitCellsPerDimention*latticeConstant;
    setSystemSize(size);

//    for(int i=0; i<100; i++) {
//        Atom *atom = new Atom(UnitConverter::massFromSI(6.63352088e-26));
//        double x = Random::nextDouble(0, 10); // random number in the interval [0,10]
//        double y = Random::nextDouble(0, 10);
//        double z = Random::nextDouble(0, 10);
//        atom->position.set(x,y,z);
//        atom->resetVelocityMaxwellian(temperature);
//        m_atoms.push_back(atom);
//    }
//    setSystemSize(vec3(10, 10, 10)); // Remember to set the correct system size!
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
