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

    int N = 2;
    int NMC = 100000;
    // int seed = 0;
    MetropolisSolver solver(N);//, seed);

    // Generate spin matrix with random values of either -1 or 1:
    // arma::mat spin_matrix = 2*arma::randi<arma::mat>(N,N,arma::distr_param(0,1)) - 1;

    arma::mat spin_matrix = - arma::ones<arma::mat>(N,N);
    spin_matrix.print();

    // handling boundry conditions
    double E = 0;

    for (int i=0; i<N; i++){
        for (int j=0; j<N; j++){
            E += - spin_matrix(i,j)*
                (spin_matrix(i,periodic(j,N,1))+
                 spin_matrix(periodic(i,N,1),j));//+
                 //spin_matrix(i,periodic(j,N,-1))+
                 //spin_matrix(periodic(i,N,-1),j));
        }
    }
    cout << E << endl;

    double M = arma::accu(spin_matrix);



    arma::vec deltaE;
    arma::vec w;
    deltaE << -8 << -4 << 0 << 4 << 8;

    double T = 1.0;
    double beta = 1./T;
    w = arma::exp(- beta * deltaE);

    w.print();
    double avgE = E;
    double avgM = M;
    for (int i = 0; i < NMC; i++) {
        solver.run(spin_matrix, E, M, w);
        avgE += E;
        avgM += M;
    }
    avgE /= (double) NMC;
    avgM /= (double) NMC;
    cout << avgE << " " << avgM << endl;
}
