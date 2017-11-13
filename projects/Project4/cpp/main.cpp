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
void initialize(double T, arma::mat &spin_matrix, double &E, double &M, arma::vec &w, bool orderedSpinConfig);

int main(int argc, char * argv[]) {
    int NMC;
    double Tstart, Tstop, Tstep;
    double startTime, stopTime;
    int L;
    string filename;
    bool time_it;
    bool save_to_file;
    bool orderedSpinConfig;
    int nodeCount;
    int localRank;
    ofstream outfile;
    clock_t begin, end;

    MPI_Init (&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &nodeCount);
    MPI_Comm_rank(MPI_COMM_WORLD, &localRank);

    // Root process (localRank == 0) Gathers input data
    L = 2;
    time_it = false;
    save_to_file = false;
    orderedSpinConfig = false;
    if (localRank == 0){
        if (argc == 1){
            cout << "Give me your number of montecarlo simulations!" << endl;
            cin >> NMC;
            cout << "Please give me temperature start, stop and step as well" << endl;
            cout << "Start: ";
            cin >> Tstart;
            cout << "Stop: ";
            cin >> Tstop;
            cout << "Step: ";
            cin >> Tstep;
            cout << "Would you mind passing me a lattice size?" << endl;
            cin >> L;
            orderedSpinConfig = true;
        } else if(argc == 2){
            filename = argv[1];
            int result = readData(filename, NMC,Tstart, Tstop, Tstep,L,time_it,save_to_file,orderedSpinConfig);
            if (result != 0){
                cout << "Error in file at line " << result << endl;
                return 1;
            }
        }
        if (argc > 2){
            NMC = atoi(argv[1]);
        }
        if (argc == 3){
            Tstart = atof(argv[3]);;
            Tstop = Tstart + 1;
            Tstep = 1
        }
        if (argc == 4){
            cout << "Wrong number of arguments! Can't be 5 (must define only Tstart or all three of Tstart, Tstop and Tstep)."
            return 1;
        }
        if (argc > 4){
            Tstart = atof(argv[3]);
            Tstop = atof(argv[4]);
            Tstep = atof(argv[5]);
        }
        if (argc > 5){
            L = atoi(argv[3]);
        }
        if (argc > 6){
            time_it = (bool) atoi(argv[4]);
        }
        if (argc > 7){
            save_to_file = (bool) atoi(argv[5]);
        }
        if (argc > 8){
            orderedSpinConfig = (bool) atoi(argv[6]);
        }
        if (argc > 9){
            cout << "Wrong number of arguments! Must be <= 8" << endl;
            return 1;
        }
    } else {
        time_it = false;
        save_to_file = false;
    }

    // Initialize temperatures
    int nTemps = (int)((Tstop-Tstart)/Tstep);
    double temperatures[nTemps];
    for(int i = 0; i < nTemps; i++){
        temperatures[i] = Tstart + Tstep*i;
    }

    int sum = 0;
    int experimentsPerNode[nodeCount];
    int displacements[nodeCount];
    int expPerNodeBase = nTemps / nodeCount;
    int expRest = nTemps / nodeCount;
    for (int i = 0; i < nodeCount; i ++){
        experimentsPerNode[i] = expPerNodeBase + (int) (i < expRest);
        displacements[i] = sum;
        sum += experimentsPerNode[i];
    }

    double localTemps[experimentsPerNode[localRank]];

    MPI_Scatterv(&temperatures, &experimentsPerNode, &displacements, MPI_DOUBLE,&localTemps ,1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(&NMC, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&L, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&orderedSpinConfig, 1, MPI_INT, 0, MPI_COMM_WORLD);


    //    std::random_device rd;
    //    std::mt19937 gen(rd());
    //    std::uniform_real_distribution<> dist(0.,1.);
    //    cout << dist(gen) << endl;

    double seed = (- MPI_Wtime() - localRank) * 1e9;
    MetropolisSolver solver(L, seed); // can also accept a seed for its random number generators.
    arma::arma_rng::set_seed(seed);

    // Generate spin matrix with random values of either -1 or 1:
    arma::mat spin_matrix;
    double E;
    double M;
    arma::vec w;
    // Loop over local temperatures
    for(int j; j < experimentsPerNode[localRank]; j ++){
        T = localTemps[j];
    }
    //	Initialize spins, energies, magnetization and transfer probabilities for a given T
    initialize(T, &spin_matrix, &E, &M, &w, orderedSpinConfig);
    double avgE = E;
    double avgEsquared = E*E;
    double avgM = M;
    double avgMsquared = M*M;

    if (localRank == 0 ){
        if (save_to_file)	{ outfile.open("out/"+filename); 	}
        if (time_it) 		{ startTime = MPI_Wtime(); 			}
    }

    // where the magic happens
    for (int i = 0; i < NMC; i++) {
        solver.run(spin_matrix, E, M, w);
        avgE += E;
        avgEsquared += E*E;
        avgM += M;
        avgMsquared += M*M;
        if (localRank == 0 && save_to_file){
            outfile << i << " " << T << " " << avgE << " " << avgM <<" "
            << avgEsquared << " " << avgMsquared << endl;
        }
    }
    if (localRank == 0 && time_it){
        end = clock();
        double time_elapsed = double(end-begin)/CLOCKS_PER_SEC;
        cout << "TIMEUSED: " << time_elapsed << endl;
    }

    avgE /= (double) NMC;
    avgEsquared /= (double) NMC;
    avgM /= (double) NMC;
    avgMsquared /= (double) NMC;

    double energies[nodeCount];
    double magnetization[nodeCount];
    double energiesSquared[nodeCount];
    double magnetizationSquared[nodeCount];

    // Gather results to one thread for printing (and timing (need to know when every thread is done))
    MPI_Gather(&avgE, 1, MPI_DOUBLE, &energies,1,MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Gather(&avgM, 1, MPI_DOUBLE, &magnetization,1,MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Gather(&avgEsquared, 1, MPI_DOUBLE, &energiesSquared,1,MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Gather(&avgMsquared, 1, MPI_DOUBLE, &magnetizationSquared,1,MPI_DOUBLE, 0, MPI_COMM_WORLD);

    if (localRank == 0){
        double specific_heat;
        double susceptibility;

        for  (int i = 0; i < nodeCount; i++){
            avgE = energies[i];
            avgM = magnetization[i];
            avgEsquared = energiesSquared[i];
            avgMsquared = magnetizationSquared[i];

            specific_heat = 1/(T*T)*(avgEsquared - avgE*avgE);
            susceptibility = (1/T)*(avgMsquared - avgM*avgM);
            cout << avgE << " "
                 << avgM << " "
                 << avgEsquared << " "
                 << avgMsquared << " "
                 << specific_heat << " "
                 << susceptibility << endl;
        }

        if (save_to_file){
            outfile.close();
        }
    }
    MPI_Finalize();
}


void initialize(double T, arma::mat &spin_matrix, double &E, double &M, arma::vec &w, bool orderedSpinConfig){
    if (orderedSpinConfig){
        spin_matrix = - arma::ones<arma::mat>(L,L);
    } else {
        spin_matrix= 2*arma::randi<arma::mat>(L,L,arma::distr_param(0,1)) - 1;
    }
    E = 0;

    // handling boundry conditions
    for (int i=0; i<L; i++){
        for (int j=0; j<L; j++){
            E += - spin_matrix(i,j)*
                (spin_matrix(i,periodic(j,L,1))+
                 spin_matrix(periodic(i,L,1),j));
        }
    }

    M = arma::accu(spin_matrix);
    arma::vec deltaE << -8 << -4 << 0 << 4 << 8;
    w = arma::exp(- deltaE/T);
}














