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
void initialize(double T, arma::mat &spin_matrix,int L, double &E, double &M, arma::vec &w, bool orderedSpinConfig);

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

    string me = "(Process " + to_string(localRank) + ") ";

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
            Tstart = atof(argv[2]);;
        }
        if (argc == 3){
            Tstop = Tstart;
            Tstep = 1;
        }
        if (argc == 4){
            cout << "Wrong number of arguments! Can't be 5 (must define only Tstart or all three of Tstart, Tstop and Tstep).";
            return 1;
        }
        if (argc > 4){
            Tstart = atof(argv[2]);
            Tstop = atof(argv[3]);
            Tstep = atof(argv[4]);
        }
        if (argc > 5){
            L = atoi(argv[5]);
        }
        if (argc > 6){
            time_it = (bool) atoi(argv[6]);
        }
        if (argc > 7){
            save_to_file = (bool) atoi(argv[7]);
        }
        if (argc > 8){
            orderedSpinConfig = (bool) atoi(argv[8]);
        }
        if (argc > 9){
            cout << "Wrong number of arguments! Must be <= 8" << endl;
            return 1;
        }
    } else {
        time_it = false;
        save_to_file = false;
    }

    MPI_Bcast(&Tstop, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(&Tstart, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(&Tstep, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(&NMC, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&L, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&orderedSpinConfig, 1, MPI_INT, 0, MPI_COMM_WORLD);

    // Initialize temperatures
    int nTemps = (int) ceil((Tstop-Tstart)/Tstep) + 1;
    double temperatures[nTemps];
    for(int i = 0; i < nTemps; i++){
        temperatures[i] = Tstart + Tstep*i;
    }

    // cout << me << " NMC: " << NMC << " nt: " << nTemps << endl;
    int sum = 0;
    int experimentsPerNode[nodeCount];
    int displacements[nodeCount];
    int expPerNodeBase = nTemps / nodeCount;
    int expRest = nTemps % nodeCount;

    // int localExperimentCount = expPerNodeBase + (int) (localRank < expRest);

    for (int i = 0; i < nodeCount; i ++){
        experimentsPerNode[i] = expPerNodeBase + (int) (i < expRest);
        displacements[i] = sum;
        sum += experimentsPerNode[i];
    }

    int localExperiments = experimentsPerNode[localRank];
    double localTemps[localExperiments];

    MPI_Scatterv(&temperatures, experimentsPerNode, displacements, MPI_DOUBLE,&localTemps ,localExperiments, MPI_DOUBLE, 0, MPI_COMM_WORLD);

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
    double T;
    arma::vec w;
    // Loop over local temperatures
    double avgE[localExperiments];
    double avgEsquared[localExperiments];
    double avgM[localExperiments];
    double avgMsquared[localExperiments];
    if (localRank == 0  && time_it) {
        startTime = MPI_Wtime();
    }
    for (int j; j < localExperiments; j ++){
        T = localTemps[j];
        //	Initialize spins, energies, magnetization and transfer probabilities for a given T
        initialize(T, spin_matrix, L, E, M, w, orderedSpinConfig);
        avgE[j] 	   =0;
        avgEsquared[j] = 0;
        avgM[j] 	   =0;
        avgMsquared[j] = 0;

        // where the magic happens
        for (int i = 0; i < NMC; i++) {
            solver.run(spin_matrix, E, M, w);
            avgE[j] += E;
            avgEsquared[j] += E*E;
            avgM[j] += M;
            avgMsquared[j] += M*M;
        }
        avgE[j] 	   =  avgE[j]/ (double) NMC;
        avgEsquared[j] =  avgEsquared[j] / (double) NMC;
        avgM[j] 	   =  avgM[j] 	   / (double) NMC;
        avgMsquared[j] =  avgMsquared[j] / (double) NMC;
    }


    if (localRank == 0 && time_it){
        end = clock();
        double time_elapsed = double(end-begin)/CLOCKS_PER_SEC;
        cout << "TIMEUSED: " << time_elapsed << endl;
    }

    double energies[nTemps];
    double magnetization[nTemps];
    double energiesSquared[nTemps];
    double magnetizationSquared[nTemps];

    // Gather results to one thread for printing (and timing (need to know when every thread is done))
    //////////////////////////////////////////////////////////////
//    for (int i = 0; i < localExperiments; i ++ ){
//        cout << me << "avgE["<<i<<"] = " << avgE[i] << endl;
//        cout << me << "avgM["<<i<<"] = " << avgM[i] << endl;
//        cout << me << "avgE^2["<<i<<"] = " << avgEsquared[i] << endl;
//        cout << me << "avgM^2["<<i<<"] = " << avgMsquared[i] << endl;
//    }
    MPI_Gatherv(&avgE, localExperiments, MPI_DOUBLE, &energies, experimentsPerNode, displacements,
                MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Gatherv(&avgM, localExperiments, MPI_DOUBLE, &magnetization, experimentsPerNode, displacements,
                MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Gatherv(&avgEsquared, localExperiments, MPI_DOUBLE, &energiesSquared, experimentsPerNode,
                displacements, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Gatherv(&avgMsquared, localExperiments, MPI_DOUBLE, &magnetizationSquared, experimentsPerNode,
                displacements, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    if (localRank == 0){
        double specific_heat;
        double susceptibility;
        if(save_to_file){
            outfile.open("out/"+filename);
        }

        double EforPrinting;
        double MforPrinting;
        double ESquaredforPrinting;
        double MSquaredforPrinting;

        for  (int i = 0; i < nTemps; i++){
            EforPrinting = energies[i];
            MforPrinting = magnetization[i];
            ESquaredforPrinting= energiesSquared[i];
            MSquaredforPrinting= magnetizationSquared[i];
            specific_heat = 1/(T*T)*(ESquaredforPrinting - EforPrinting*EforPrinting);
            susceptibility = (1/T)*(MSquaredforPrinting - MforPrinting*MforPrinting);

            cout << EforPrinting << " "
                 << MforPrinting << " "
                 << ESquaredforPrinting<< " "
                 << MSquaredforPrinting<< " "
                 << specific_heat << " "
                 << susceptibility << endl;

            if (save_to_file){
                outfile << i << " " << T << " " << avgE << " " << avgM <<" "
                << avgEsquared << " " << avgMsquared << endl;
            }
        }

        if (save_to_file)	{
            outfile.close();
        }
    }
    MPI_Finalize();
}


void initialize(double T, arma::mat &spin_matrix, int L, double &E, double &M, arma::vec &w, bool orderedSpinConfig){
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
    arma::vec deltaE;
    deltaE << -8 << -4 << 0 << 4 << 8;
    w = arma::exp(- deltaE/T);
}














