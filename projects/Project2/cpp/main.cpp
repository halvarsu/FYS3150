#include <iostream>
#include <armadillo>
// #include "solve.h"
#include "solve.h"
#define CATCH_CONFIG_RUNNER
#include "catch.hpp"


void save(arma::vec& rho,arma::vec& eigval,arma::mat& eigvec, std::string filename);

int main(int argc, char * argv[])
{
    if(argc > 1 && (std::string) argv[1] == "test"){
        std::cout << argv[1] << std::endl;
        int dumb = 1;
        char* dumb1[1];
        int result = Catch::Session().run(dumb, dumb1);
        return result;
    }

    int lOrbital, dim;
    double rhoMin, rhoMax, step, omega;
    bool interacting;
    char* filename ;
    arma::mat eigvec;
    arma::vec eigval, rho;

    // initial values
    lOrbital = 0;
    dim      = 200;
    omega    = 0.0;
    rhoMin 	  = 0.0;
    rhoMax 	  = 7.0;
    step = (rhoMax - rhoMin)/(dim+1);
    interacting = false;

    // examine stability of rho, 1D case:
    arma::vec rhoMaxVals = arma::linspace(1,10,11);
    for (int i = 0; i < rhoMaxVals.size(); i ++){
        break;
        // Calculate array of position values
        rho = arma::linspace(rhoMin+step, rhoMaxVals[i], dim);
        // setting up a soon to be tridiagonal matrix and storage for its
        // eigenvectors and -values
        hamiltonSolve(rho, eigval, eigvec, omega, 0, interacting);

        // creating filename and saving values
        filename = new char[20];
        std::sprintf(filename, "rho_stab%.0f_%d",rhoMaxVals[i], dim);
        std::cout << "saving " << filename << std::endl;
        save(rho, eigval, eigvec, filename);
    }

    // results: best rho = 6.79

    rhoMax = 6.79;
    // examine stability of dim, 1D case:
    arma::vec dimVals = arma::linspace(50,310,14);
    for (unsigned int i = 0; i < dimVals.size(); i ++){
        rho = arma::linspace(rhoMin+step, rhoMax, dimVals[i]);
//        hamiltonSolve(rho, eigval, eigvec, omega, 0, interacting);

//        filename = new char[20];
//        std::sprintf(filename, "N_stab%.2f_%d",rhoMax, (int)dimVals[i]);
//        std::cout << "saving " << filename << std::endl;
//        save(rho, eigval, eigvec, filename);

        hamiltonSolve(rho, eigval, eigvec, omega, 0, interacting, "arma");
        filename = new char[20];
        std::sprintf(filename, "N_stab_arma%.2f_%d",rhoMax, (int)dimVals[i]);
        std::cout << "saving " << filename << std::endl;
        save(rho, eigval, eigvec, filename);
    }

    // eigvals.print();
    return 0;
}

void save(arma::vec& rho,arma::vec& eigval,arma::mat& eigvec, std::string filename) {
    eigval.save((std::string)filename+"val.txt", arma::arma_ascii);
    eigvec.save((std::string)filename+"vec.txt", arma::arma_ascii);
    rho.save((std::string)filename+"rho.txt", arma::arma_ascii);
}
