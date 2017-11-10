#ifndef METROPOLIS_H
#define METROPOLIS_H

#include <random>
#include <armadillo>
#include <omp.h>

class MetropolisSolver
{
public:
    MetropolisSolver(int n_spins, int seed);
    MetropolisSolver(int n_spins);

    //void run(arma::mat & spin_matrix, double & E, double &M, arma::vec w, bool parallel);
    void run(arma::mat &spin_matrix, double & E, double &M, arma::vec w);
    int rand_coord();
    double rand();
private:
    int m_latticeLength;
    int m_n_spins;      // = latticeLength^2
    std::mt19937 m_rng;
    std::uniform_int_distribution<> m_latticeDistribution;
    std::uniform_real_distribution<> m_realDistribution;
};

#endif // METROPOLIS_H
