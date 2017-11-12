#include <iostream>
#include <fstream>
#include <armadillo>
#include <chrono>
#include <iomanip>
#include <cmath>
#include "metropolis.h"
#include "tools.h"
#include <string>
// #include <studio.h>
#include <ctime>
#include <mpi.h>
#include <random>

using namespace std;

int main(int argc, char * argv[]) {
    int NMC;
    double T;
    int L;
    string filename;
    bool time_it;
    bool save_to_file;
    bool orderedSpinConfig;
    int numProcs;
    int localRank;

    MPI_Init (&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &numProcs);
    MPI_Comm_rank(MPI_COMM_WORLD, &localRank);

    // Root process (localRank == 0) Gathers input data
    if (localRank == 0){
        if (argc == 1){
            cout << "Give me your number of montecarlo simulations!" << endl;
            cin >> NMC;
            cout << "Please give me a temperature as well" << endl;
            cin >> T;
            cout << "Would you mind passing me a lattice size?" << endl;
            cin >> L;
            orderedSpinConfig = true;
            time_it = false;
            save_to_file = false;
        } else if(argc == 2){
            filename = argv[1];
            int result = readData(filename, NMC,T,L,time_it,save_to_file,orderedSpinConfig);
            if (result != 0){
                cout << "Error in file at line " << result << endl;
                return 1;
            }
        } else if (argc == 3){
            NMC = atoi(argv[1]);
            T = atof(argv[2]);
            L = 2;
            time_it = false;
            save_to_file = false;
            orderedSpinConfig = false;
        } else if (argc == 4){
            NMC = atoi(argv[1]);
            T = atof(argv[2]);
            L = atoi(argv[3]);
            time_it = false;
            save_to_file = false;
            orderedSpinConfig = false;
        } else {
            cout << "Wrong number of arguments! Must be < 4" << endl;
            return 1;
        }
    } else {
        time_it = false;
        save_to_file = false;
    }

    MPI_Bcast(&NMC, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&T, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(&L, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&orderedSpinConfig, 1, MPI_INT, 0, MPI_COMM_WORLD);


    //    std::random_device rd;
    //    std::mt19937 gen(rd());
    //    std::uniform_real_distribution<> dist(0.,1.);
    //    cout << dist(gen) << endl;

    int seed = time(NULL) + localRank;
    MetropolisSolver solver(L, seed); // can also accept a seed for its random number generators.

    arma::arma_rng::set_seed(seed);

    // Generate spin matrix with random values of either -1 or 1:
    arma::mat spin_matrix;
    if (orderedSpinConfig){
        spin_matrix = - arma::ones<arma::mat>(L,L);
    } else {
        spin_matrix= 2*arma::randi<arma::mat>(L,L,arma::distr_param(0,1)) - 1;
    }

    double E = 0;

    // handling boundry conditions
    for (int i=0; i<L; i++){
        for (int j=0; j<L; j++){
            E += - spin_matrix(i,j)*
                (spin_matrix(i,periodic(j,L,1))+
                 spin_matrix(periodic(i,L,1),j));
        }
    }

    double M = arma::accu(spin_matrix);

    arma::vec deltaE;
    arma::vec w;
    deltaE << -8 << -4 << 0 << 4 << 8;

    double beta = 1./T;
    w = arma::exp(- beta * deltaE);

    double avgE = E;
    double avgEsquared = E*E;
    double avgM = M;
    double avgMsquared = M*M;

    if (save_to_file){
        // open file
    }

    if (time_it){
        // start clock
        clock_t begin = clock();
    }

    // where the magic happens
    for (int i = 0; i < NMC; i++) {
        solver.run(spin_matrix, E, M, w);
        avgE += E;
        avgEsquared += E*E;
        avgM += M;
        avgMsquared += M*M;
        if (save_to_file){
            // need a file to save to
        }
    }
    if (time_it){
        clock_t end = clock();
        double time_elapsed = double(end-begin)/CLOCKS_PER_SEC;
        // print clock
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

    if (save_to_file){
        outfile.open(out/filename);
        outfile << avgE << endl;
        outfile << avgM << endl;
        outfile << avgEsquared << endl;
        outfile << avgMsquared << endl;
        outfile << specific_heat << endl;
        outfile << susceptibility << endl;
        outfile.close()
    }
    MPI_Finalize();
}
















