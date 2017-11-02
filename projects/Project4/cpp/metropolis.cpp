#include "metropolis.h"
#include <random>
#include "tools.h"

std::random_device rd;

MetropolisSolver::MetropolisSolver(int n_spins, int seed) :
    m_n_spins(n_spins),
    m_rng(rd()),
    m_intDist(0,n_spins-1),
    m_realDist(0.,1.)
{
    m_rng.seed(seed);
}

MetropolisSolver::MetropolisSolver(int n_spins) :
    m_n_spins(n_spins),
    m_rng(rd()),
    m_intDist(0,n_spins-1),
    m_realDist(0.,1.)
{
}

int MetropolisSolver::rand_spin(){
    // Returns an int from a uniform distribution from 0 to m_n_spins-1
    return m_intDist(m_rng);
}

double MetropolisSolver::rand(){
    // Returns a double from a uniform distribution from 0 to 1
    return m_realDist(m_rng);
}

void MetropolisSolver::run(arma::mat &spin_matrix, double & E, double &M, arma::vec w){
    // loop over all spin
    for(int y =0; y < m_n_spins; y++) {
        for (int x= 0; x < m_n_spins; x++){
            // Find random position
            int ix = MetropolisSolver::rand_spin();
            int iy = MetropolisSolver::rand_spin();
            int deltaE = 2*spin_matrix(iy,ix)*
            (spin_matrix(iy,periodic(ix,m_n_spins,-1))+
            spin_matrix(periodic(iy,m_n_spins,-1),ix) +
            spin_matrix(iy,periodic(ix,m_n_spins,1)) +
            spin_matrix(periodic(iy,m_n_spins,1),ix));
            // Here we perform the Metropolis test
            if ( MetropolisSolver::rand() <= w(deltaE/4+2) ) {
                spin_matrix(iy,ix) *= -1; // flip one spin and accept new spin config
                // update energy and magnetization
                M += (double) 2*spin_matrix(iy,ix);
                E += (double) deltaE;
            }
        }
    }
//    M = M/(m_n_spins*m_n_spins);
//    E = E/(m_n_spins*m_n_spins);
}
