#include "metropolis.h"
#include <random>
#include "tools.h"


MetropolisSolver::MetropolisSolver(int latticeLength, double seed) :
    m_latticeLength(latticeLength),
    m_n_spins(latticeLength*latticeLength),
    m_latticeDistribution(0,latticeLength-1),
    m_realDistribution(0.,1.)
{
    m_rng.seed(seed);
}

MetropolisSolver::MetropolisSolver(int latticeLength) :
    m_latticeLength(latticeLength),
    m_n_spins(latticeLength*latticeLength),
    m_latticeDistribution(0,latticeLength-1),
    m_realDistribution(0.,1.)
{
    m_rng.seed(m_rd());
}

int MetropolisSolver::rand_coord(){
    // Returns an int from a uniform distribution from 0 to m_latticeLength-1
    return m_latticeDistribution(m_rng);
}

double MetropolisSolver::rand(){
    // Returns a double from a uniform distribution from 0 to 1
    return m_realDistribution(m_rng);
}

void MetropolisSolver::run(arma::mat &spin_matrix, double & E, double &M, arma::vec w, int&accepted){
    // loop over all spin, to make one cycle proportional to the lattice size
    for (int i= 0; i < m_n_spins; i++){
        // Find random position
        int ix = MetropolisSolver::rand_coord();
        int iy = MetropolisSolver::rand_coord();
        // get energy change due to spin flip
        int deltaE = 2*spin_matrix(iy,ix)*
                        (spin_matrix(iy,periodic(ix,m_latticeLength,-1))+
                         spin_matrix(periodic(iy,m_latticeLength,-1),ix) +
                         spin_matrix(iy,periodic(ix,m_latticeLength,1)) +
                         spin_matrix(periodic(iy,m_latticeLength,1),ix));
        // the Metropolis test
        if ( MetropolisSolver::rand() <= w(deltaE/4+2) ) { // The morten way reduces number of FLOPS by two, should have done that instead.
            spin_matrix(iy,ix) *= -1; // flip spin and accept new spin config
            // update energy and magnetization
            M += (double) 2*spin_matrix(iy,ix);
            E += (double) deltaE;
            accepted+=1;
        }
    }
}












