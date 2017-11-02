#include <iostream>
#include <fstream>
#include <armadillo>
#include <chrono>
#include <iomanip>
#include <cmath>
#include "metropolis.h"
#include "tools.h"

using namespace std;



int main(int argc, char * argv[]) {
    std::random_device rd;
    std::mt19937 gen(rd());
    gen.seed(2);
    std::uniform_real_distribution<> dist(0.,1.);

    cout << dist(gen) << endl;

    int spins = 2;
    MetropolisSolver solver(spins, 2);
    cout << solver.rand_spin() << endl;

    // Generate spin matrix with random values of either -1 or 1:
    // arma::mat spin_matrix = 2*arma::randi<arma::mat>(spins,spins,arma::distr_param(0,1)) - 1;
    arma::mat spin_matrix = - arma::ones<arma::mat>(spins,spins);
    double E = 0;
    double M = 0;
    arma::vec deltaE;
    arma::vec w;
    deltaE << -8 << -4 << 0 << 4 << 8;
    //double T =
    w = arma::exp(T* deltaE);
    w.print();
    solver.run(spin_matrix, E, M, w);
    cout << E << " " << M << endl;
}
