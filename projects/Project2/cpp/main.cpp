#include <iostream>
#include <fstream>
#include <armadillo>
// #include "solve.h"
#include "solve.h"
#include "main.h"
#define CATCH_CONFIG_RUNNER
#include "catch.hpp"
#include "tests/test.cpp"

int main(int argc, char * argv[])
{
    std::string mode, solver;
    int dim;
    switch (argc){
        case 1:
            mode   = "interacting";
            solver = "jacobi";
            dim    = 1000;
            break;
        case 2:
            mode   = argv[1];
            solver = "jacobi";
            dim    = 1000;
            break;
        case 3:
            mode   = argv[1];
            solver = argv[2];
            dim    = 1000;
            break;
        case 4:
            mode   = argv[1];
            solver = argv[2];
            dim    = std::atoi(argv[3]);
            break;
    }
    std::cout << "running mode " << mode << std::endl;
    if (mode == "test"){
        int foo = 1;
        char* bar[0];
        return Catch::Session().run(foo, bar);
    } else if (mode == "stability") {
            stability_analysis(solver);
            return 0;
    } else if (mode == "interacting") {
        run_interacting(dim, solver);
        return 0;
    } else {
        std::cout << "Invalid mode, exiting " << std::endl;
        return 1;
    }
}

void run_interacting(int dim, std::string solver){
    double rhoMin, rhoMax, omega;
    bool interacting;

    // initial values
    rhoMin 	    = 0.0;
    interacting = true;

    // examine stability of rho, 1D case:
    double omegaVals[] 	= {0.01, 0.25, 0.5, 1, 5};
    double rhoMaxVals[]	= {100., 15., 10.,7., 4.};
    //int    dimVals[]	= {400, 600, 200, 200, 200};
    for (unsigned int i = 0; i < 5; i ++){
        omega 	= omegaVals[i];
        rhoMax 	= rhoMaxVals[i];
        // dim 	= dimVals[i];
        std::cout << "omega   = " << omega << std::endl;
        std::cout << "rho_max = " << rhoMax << std::endl;
        std::cout << "dim     = " << dim << std::endl;
        hamiltonSolve(rhoMin, rhoMax, dim, omega, 0, interacting,solver);
    }
}

void stability_analysis(std::string solver){
    int dim, iterations;
    double rhoMin, rhoMax, omega, step;
    bool interacting;
    std::ofstream outfile;


    // initial values
    omega    = 0.0;
    rhoMin 	  = 0.0;
    interacting = false;

    step = 5.0/200;
    // examine stability of rho, 1D case:
    arma::vec rhoMaxVals = arma::linspace(1,10,31);
    for (unsigned int i = 0; i < rhoMaxVals.size(); i ++){
        rhoMax = rhoMaxVals[i];
        dim = (int) (rhoMax/step);
        iterations = hamiltonSolve(rhoMin, rhoMax, dim, omega, 0, interacting,solver);
    }

    rhoMax = 5.;
    // examine stability of dim, 1D case:
    arma::vec dimVals = arma::linspace(50,400,31);
    outfile.open(solver + "/iterations.txt");//, std::ios_base::app);
    for (unsigned int i = 0; i < dimVals.size(); i ++){
        // Updating values for changing dim
        dim = dimVals[i];
        iterations = hamiltonSolve(rhoMin, rhoMax, dim, omega, 0, interacting, solver);
        std::cout << "saving iterations used= " << iterations << " to iterations.txt" << std::endl;
        outfile << dim << " " << iterations << std::endl;
    }
    outfile.close();
}
