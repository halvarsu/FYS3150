#include "system.h"
#include "statisticssampler.h"
#include "lennardjones.h"
#include <iostream>
#include <iomanip>

using std::ofstream; using std::cout; using std::endl;

StatisticsSampler::StatisticsSampler()
{

}

void StatisticsSampler::saveToFile(System &system)
{
    // Save the statistical properties for each timestep for plotting etc.
    // First, open the file if it's not open already
    if(!m_file.good()) {
        m_file.open("statistics.txt", ofstream::out);
        // If it's still not open, something bad happened...
        if(!m_file.good()) {
            cout << "Error, could not open statistics.txt" << endl;
            exit(1);
        }
    }

    m_file << std::setw(20) << system.steps() <<
            std::setw(20) << system.time() <<
            std::setw(20) << m_temperature <<
            std::setw(20) << m_kineticEnergy <<
            std::setw(20) << m_potentialEnergy <<
            std::setw(20) << m_diffusion << std::endl;

    // Print out values here
}

void StatisticsSampler::sample(System &system)
{
    // Here you should measure different kinds of statistical properties and save it to a file.
    sampleKineticEnergy(system);
    samplePotentialEnergy(system);
    sampleTemperature(system);
    sampleDiffusion(system);
    sampleDensity(system);
    saveToFile(system);
}

void StatisticsSampler::sampleKineticEnergy(System &system)
{
    m_kineticEnergy = 0; // Remember to reset the value from the previous timestep
    // double speedSquared;
    for(Atom *atom : system.atoms()) {
        //speedSquared = (atom->velocity[0]*atom->velocity[0]+atom->velocity[1]*atom->velocity[1]+atom->velocity[2]*atom->velocity[2]);
        //m_kineticEnergy += speedSquared*atom->mass()*0.5;
        m_kineticEnergy += 0.5 * atom->mass() * atom->velocity.lengthSquared();
    }
}

void StatisticsSampler::samplePotentialEnergy(System &system)
{
    m_potentialEnergy = system.potential().potentialEnergy();
}

void StatisticsSampler::sampleTemperature(System &system)
{
    m_temperature = 2./3. * m_kineticEnergy/ system.atoms().size();
    // Units of energy over boltzmans constant
}

void StatisticsSampler::sampleDiffusion(System &system)
{
    m_diffusion = 0;
    for (Atom *atom : system.atoms()){
        m_diffusion += (atom->position - system.systemSize()*atom->nRelocations - atom->initialPosition).lengthSquared();
    }
    m_diffusion /= (6*system.time());
}

void StatisticsSampler::sampleDensity(System &system)
{

}
