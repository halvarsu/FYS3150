#ifndef METROPOLIS_H
#define METROPOLIS_H

#include <random>
#include <armadillo>

class MetropolisSolver
{
public:
    MetropolisSolver(int n_spins, int seed);
    MetropolisSolver(int n_spins);

    void run(arma::mat & spin_matrix, double & E, double &M, arma::vec w);
    int rand_spin();
    double rand();
private:
    int m_n_spins;
    std::mt19937 m_rng;
    std::uniform_int_distribution<> m_intDist;
    std::uniform_real_distribution<> m_realDist;
};

#endif // METROPOLIS_H
