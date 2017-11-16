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
string getFilenameBase(string filename);

int main(int argc, char * argv[]) {
    int NMC, nTemps, L;
    double Tstart, Tstop;
    double startTime, stopTime;
    string inFilename = "in/PLACEHOLDER.txt";
    string outFilename;
    bool time_it;
    bool save_to_file;
    bool orderedSpinConfig;
    int nodeCount;
    int localRank;
    ofstream outfile;
    clock_t begin, end;
    bool verbose = false;

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
            cout << "Give me temperature start, stop and number of steps as well!" << endl;
            cout << "Start: ";
            cin >> Tstart;
            cout << "Stop: ";
            cin >> Tstop;
            cout << "Number of steps: ";
            cin >> nTemps;
            cout << "Thank you! Sorry for being rude. Would you mind passing me a lattice size?" << endl;
            cin >> L;
            cout << "Again thank you. Have a beautful phase transitioning day!" << endl;
            orderedSpinConfig = true;
        } else if(argc == 2){
            inFilename = argv[1];
            int result = readData(inFilename, NMC,Tstart, Tstop, nTemps,L,time_it,save_to_file,orderedSpinConfig);
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
            nTemps = 1;
        }
        if (argc == 4){
            cout << "Wrong number of arguments! Can't be 3 (must define only Tstart or all three of Tstart, Tstop and nTemps).";
            return 1;
        }
        if (argc > 4){
            Tstart = atof(argv[2]);
            Tstop = atof(argv[3]);
            nTemps = atoi(argv[4]);
        }
        if (argc > 5){
            L = atoi(argv[5]);
        }
        if (argc > 6){
            time_it = (bool) atoi(argv[6]);
        }
        if (argc > 7){
            orderedSpinConfig = (bool) atoi(argv[7]);
        }
        if (argc > 8){
            inFilename = (string) argv[8];
            save_to_file = true;
        }
        if (argc > 9){
            verbose = true;
        }
        if (argc > 10){
            cout << "Wrong number of arguments! Must be <= 9" << endl;
            return 1;
        }
    } else {
        time_it = false;
        save_to_file = false;
    }

    outFilename = "out/" + getFilenameBase(inFilename) + ".dat";

    MPI_Bcast(&Tstop, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(&Tstart, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(&nTemps, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&NMC, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&L, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&orderedSpinConfig, 1, MPI_INT, 0, MPI_COMM_WORLD);

    // Initialize temperatures
    double dT;
    if (nTemps < 2){
        dT = 0;
    } else {
        dT = (Tstop - Tstart)/(nTemps - 1);
    }

    double temperatures[nTemps];
    for(int i = 0; i < nTemps; i++){
        temperatures[i] = Tstart + dT*i;
    }

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

    // double seed = (- MPI_Wtime()* 1e9 - localRank) ;
    MetropolisSolver solver(L); // can also accept a seed for its random number generators.
    // arma::arma_rng::set_seed(seed);

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
    int localAcceptedPerRun[localExperiments];
    int accepted;
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
        accepted = 0;

        // where the magic happens
        for (int i = 0; i < NMC; i++) {
            solver.run(spin_matrix, E, M, w, accepted);
            avgE[j] += E;
            avgEsquared[j] += E*E;
            avgM[j] += M;
            avgMsquared[j] += M*M;
        }
        avgE[j] 	   =  avgE[j]/ (double) NMC;
        avgEsquared[j] =  avgEsquared[j] / (double) NMC;
        avgM[j] 	   =  avgM[j] 	   / (double) NMC;
        avgMsquared[j] =  avgMsquared[j] / (double) NMC;
        localAcceptedPerRun[j] = accepted;
        if (verbose){
            cout << me << " T = " << T << " done";
        }
    }



    // Global lists, only relevant for node 0
    double energies[nTemps];
    double magnetization[nTemps];
    double energiesSquared[nTemps];
    double magnetizationSquared[nTemps];
    double TValues[nTemps];
    int acceptedValues[nTemps];

    // Gather results to one thread for printing (and timing (need to know when every thread is done))
    MPI_Gatherv(&avgE, localExperiments, MPI_DOUBLE, &energies, experimentsPerNode, displacements,
                MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Gatherv(&avgM, localExperiments, MPI_DOUBLE, &magnetization, experimentsPerNode, displacements,
                MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Gatherv(&avgEsquared, localExperiments, MPI_DOUBLE, &energiesSquared, experimentsPerNode,
                displacements, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Gatherv(&avgMsquared, localExperiments, MPI_DOUBLE, &magnetizationSquared, experimentsPerNode,
                displacements, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Gatherv(&localTemps, localExperiments, MPI_DOUBLE, &TValues, experimentsPerNode,
                displacements, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Gatherv(&localAcceptedPerRun, localExperiments, MPI_INT, &acceptedValues, experimentsPerNode,
                displacements, MPI_INT, 0, MPI_COMM_WORLD);


    if (localRank == 0){
        if (time_it){
            stopTime = MPI_Wtime();
            double time_elapsed = stopTime - startTime;
            cout << "TIMEUSED: " << time_elapsed << endl;
        }
        if(save_to_file){
            outfile.open(outFilename, ios::binary);
        }

        double specific_heat;
        double susceptibility;
        double EforPrinting;
        double MforPrinting;
        double ESquaredforPrinting;
        double MSquaredforPrinting;

        for  (int i = 0; i < nTemps; i++){
            T = TValues[i];
            EforPrinting = energies[i];
            MforPrinting = magnetization[i];
            ESquaredforPrinting= energiesSquared[i];
            MSquaredforPrinting= magnetizationSquared[i];
            specific_heat = 1/(T*T)*(ESquaredforPrinting - EforPrinting*EforPrinting);
            susceptibility = (1/T)*(MSquaredforPrinting - MforPrinting*MforPrinting);
            accepted = acceptedValues[i];

            cout << EforPrinting << " "
                 << MforPrinting << " "
                 << ESquaredforPrinting<< " "
                 << MSquaredforPrinting<< " "
                 << specific_heat << " "
                 << susceptibility <<" "
                 << accepted << endl;

            if (save_to_file){
                outfile << i << " " << T << " " << EforPrinting << " " << MforPrinting <<" "
                << ESquaredforPrinting << " " << MSquaredforPrinting << " " << specific_heat << " "
                << susceptibility << " " << accepted << endl;
            }
        }

        if (save_to_file)	{
            outfile.close();
            cout << "Data written to " << outFilename << endl;
        }
    }
    MPI_Finalize();
}

string getFilenameBase(string filename){
    // Exchanges in/ with out/ and removes .txt. If no in/, just prepends an out/
    // this works because if no delimiter found (aka no in/), we want (and get) pos=0, else we want s.find()+3
    int start = filename.find("in/") + 1;
    int stop = filename.find(".txt");
    if (start != 0) { start += 2; }
    if (stop != -1) { stop -= start; }
    return filename.substr(start, stop);
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















