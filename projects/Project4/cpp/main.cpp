#include <iostream>
#include <fstream>
#include <armadillo>
#include <chrono>
#include <iomanip>
#include <cmath>
#include "metropolis.h"
#include "tools.h"

using namespace std;



int main(int soetpotet, char * argv[]) {
    int N = 2;
    int NMC = 1000000;

    if(soetpotet == 1){
        cout << "Give me your number of montecarlo simulations!" << endl;
        cin >> NMC;
    } else {
        NMC = atoi(argv[1]);
    }

//    std::random_device rd;
//    std::mt19937 gen(rd());
//    std::uniform_real_distribution<> dist(0.,1.);
//    cout << dist(gen) << endl;

    // int seed = 0;
    MetropolisSolver solver(N);//, seed);

    // Generate spin matrix with random values of either -1 or 1:
    arma::mat spin_matrix = 2*arma::randi<arma::mat>(N,N,arma::distr_param(0,1)) - 1;
    // arma::mat spin_matrix = - arma::ones<arma::mat>(N,N);

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

    double M = arma::accu(spin_matrix);



    arma::vec deltaE;
    arma::vec w;
    deltaE << -8 << -4 << 0 << 4 << 8;

    double T = 1.0;
    double beta = 1./T;
    w = arma::exp(- beta * deltaE);

    double avgE = E;
    double avgEsquared = E*E;
    double avgM = M;
    double avgMsquared = M*M;
    for (int i = 0; i < NMC; i++) {
        solver.run(spin_matrix, E, M, w);
        avgE += E;
        avgEsquared += E*E;
        avgM += M;
        avgMsquared += M*M;
    }
    avgE /= (double) NMC;
    avgEsquared /= (double) NMC;
    avgM /= (double) NMC;
    avgMsquared /= (double) NMC;
    double specific_heat = 1/(T*T)*(avgEsquared - avgE*avgE);
    double susceptibility = (1/T)*(avgMsquared - avgM*avgM);
    cout << avgE << " "
         << avgM << " "
         << avgEsquared << " "
         << avgMsquared << " "
         << specific_heat << " "
         << susceptibility << endl;
}















