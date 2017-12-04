#include "lennardjones.h"
#include "system.h"
#include <cmath>

double LennardJones::potentialEnergy() const
{
    return m_potentialEnergy;
}

double LennardJones::kineticEnergy() const
{
    return m_kineticEnergy;
}

double LennardJones::sigma() const
{
    return m_sigma;
}

void LennardJones::setSigma(double sigma)
{
    m_sigma = sigma;
}

double LennardJones::epsilon() const
{
    return m_epsilon;
}

void LennardJones::setEpsilon(double epsilon)
{
    m_epsilon = epsilon;
}


void LennardJones::calculateForces(System &system)
{
    m_potentialEnergy = 0;
    std::vector<Atom*> atoms = system.atoms();
    int numberOfAtoms = atoms.size();

    for(Atom *atom : atoms) {
        // Reset forces on all bodies, also updating prevForce
        atom->resetForce();
    }

    for(int i=0; i<numberOfAtoms; i++) {
        Atom *atom1 = atoms[i];

        for(int j=i+1; j<numberOfAtoms; j++) {
            Atom * atom2 = atoms[j];
            vec3 drVec = atom1->position - atom2->position;
            for (int i = 0; i < 3; i++){
                if (drVec[i] <= - system.systemSizeHalf()[i]){
                    drVec[i] += system.systemSize()[i];
                } else if (drVec[i] >= system.systemSizeHalf()[i]){
                    drVec[i] -= system.systemSize()[i];
                }
            }
            double drSquared = drVec.lengthSquared();
            double idr_ul2 = m_sigma*m_sigma/drSquared; // inverse delta r, unitless, squared
            double attractive = std::pow(idr_ul2, 3);
            double repulsive = std::pow(idr_ul2, 6);

            m_potentialEnergy += 4*m_epsilon *(repulsive - attractive);

            vec3 forceVector = 24*m_epsilon * drVec/drSquared * (2*repulsive - attractive);

            atom1->force += forceVector;
            atom2->force -= forceVector;
        }
    }
    return;
}
