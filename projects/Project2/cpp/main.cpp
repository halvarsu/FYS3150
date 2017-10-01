#include <iostream>
#include <armadillo>
// #include "solve.h"
#include "solve.h"
#include "main.h"
#define CATCH_CONFIG_RUNNER
#include "catch.hpp"


int main(int argc, char * argv[])
{
    std::string mode, solver;
    switch (argc){
        case 1:
            mode   = "interacting";
            solver = "jacobi";
            break;
        case 2:
            mode   = argv[1];
            solver = "jacobi";
            break;
        case 3:
            mode   = argv[1];
            solver = argv[2];
            break;
    }
    std::cout << "running mode " << mode << std::endl;
    if (mode == "test"){
        int dumb = 1;
        char* dumb1[1];
        return Catch::Session().run(dumb, dumb1);
    } else if (mode == "stability") {
            stability_analysis(solver);
            return 0;
    } else if (mode == "interacting") {
        run_interacting(solver);
        return 0;
    } else {
        std::cout << "Invalid mode, exiting " << std::endl;
        return 1;
    }
}

void run_interacting(std::string solver){
    int dim;
    double rhoMin, rhoMax, omega;
    bool interacting;

    // initial values
    rhoMin 	    = 0.0;
    interacting = true;

    // examine stability of rho, 1D case:
    double omegaVals[] 	= {0.01, 0.5, 1, 5};
    double rhoMaxVals[]	= {100., 10.,7., 4.};
    int    dimVals[]	= {400, 200, 200, 200};
    for (unsigned int i = 0; i < 4; i ++){
        omega 	= omegaVals[i];
        rhoMax 	= rhoMaxVals[i];
        dim 	= dimVals[i];
        hamiltonSolve(rhoMin, rhoMax, dim, omega, 0, interacting,solver);
    }
}

void stability_analysis(std::string solver){
    int dim;
    double rhoMin, rhoMax, omega;
    bool interacting;

    // initial values
    omega    = 0.0;
    rhoMin 	  = 0.0;
    interacting = false;

    dim = 200;
    // examine stability of rho, 1D case:
    arma::vec rhoMaxVals = arma::linspace(1,10,11);
    for (unsigned int i = 0; i < rhoMaxVals.size(); i ++){
        rhoMax = rhoMaxVals[i];
        hamiltonSolve(rhoMin, rhoMax, dim, omega, 0, interacting,solver);
    }

    rhoMax = 5.;
    // examine stability of dim, 1D case:
    arma::vec dimVals = arma::linspace(50,400,11);
    for (unsigned int i = 0; i < dimVals.size(); i ++){
        // Updating values for changing dim
        hamiltonSolve(rhoMin, rhoMax, dimVals[i], omega, 0, interacting, solver);
    }
}
