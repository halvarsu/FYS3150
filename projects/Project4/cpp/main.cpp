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

//    std::random_device rd;
//    std::mt19937 gen(rd());
//    std::uniform_real_distribution<> dist(0.,1.);
//    cout << dist(gen) << endl;

    int spins = 2;
    // int seed = 0;
    MetropolisSolver solver(spins);//, seed);

    // Generate spin matrix with random values of either -1 or 1:
    // arma::mat spin_matrix = 2*arma::randi<arma::mat>(spins,spins,arma::distr_param(0,1)) - 1;

    arma::mat spin_matrix = - arma::ones<arma::mat>(spins,spins);
    spin_matrix.print();

    // handling boundry conditions
    int idx(int i){
        if i == N;
            return 0;
        if i == -1;
            return N-1;
        else;
            return i;
    }
    int S(int a,int b){
        return
    }

    for (i=1; i<spins+1; i++){
        for (i=1; i<spins+1; i++){
            double E += (spins_matrix[i,idx(j+1)]+spins_matrix[i,idx(j-1)]+spin_matrix[idx(i+1),j]+spin_matrix[idx(i-1),j])*spin_matrix[i,j]
        }
    }
    double M = arma::sum(spin_matrix)



    arma::vec deltaE;
    arma::vec w;
    deltaE << -8 << -4 << 0 << 4 << 8;

    double T = 1.0;
    double beta = 1./T;
    w = arma::exp(- beta * deltaE);

    w.print();
    solver.run(spin_matrix, E, M, w);
    spin_matrix.print();
    cout << E << " " << M << endl;
}
