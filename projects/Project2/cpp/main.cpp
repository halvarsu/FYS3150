#include <iostream>
#include <armadillo>
// #include "solve.h"
#include "solve.h"
#define CATCH_CONFIG_RUNNER
#include "catch.hpp"


double potential(double r, double omega, bool interacting);
void f(double  * a);
void initialize(double *omega, double *rMin, double *rMax, int* lOrbital, int* dim);

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
    arma::mat eigvec;
    arma::vec eigval, rho;

    lOrbital = 0;
    dim      = 200;
    omega    = 0.0;
    rhoMin 	  = 0.0;
    rhoMax 	  = 7.0;
    step = (rhoMax - rhoMin)/dim;
    interacting = false;

    // Calculate array of position values
    rho = arma::linspace(rhoMin+step, rhoMax, dim);

    // setting up a soon to be tridiagonal matrix and storage for its
    // eigenvectors and -values
    hamiltonSolve(rho, eigval, eigvec, omega, 0, interacting);


    // creating filename and saving values
    char* filename = new char[20];
    int len = std::sprintf(filename, "%.2f_%.2f_%d",omega,rhoMax, dim);
    std::cout << filename << std::endl;

    // eigvals.print();
    eigval.save((std::string)filename+"val.txt", arma::arma_ascii);
    eigvec.save((std::string)filename+"vec.txt", arma::arma_ascii);
    rho.save((std::string)filename+"rho.txt", arma::arma_ascii);
    return 0;
}

