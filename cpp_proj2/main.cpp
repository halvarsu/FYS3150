#include <iostream>
#include <armadillo>
#include "solve.h"

double potential(double r);
void f(double  * a);
void initialize(double *rMin, double *rMax, int* lOrbital, int* dim);

int main()
{
    double rMin, rMax;
    int lOrbital, dim;
    initialize(&rMin, &rMax, &lOrbital, &dim);

    // initialize constants
    double step = rMax/(dim+1);
    double diagConst = 2.0/(step*step);
    double offDiagConst = -1.0/(step*step);
    double orbitalFactor = lOrbital* ( lOrbital + 1.0);

    // Calculate array of potential values
    arma::vec v = arma::zeros(dim);
    arma::vec r = arma::linspace(rMin, rMax, dim);

    for	(int i = 0; i < dim; i++){
        r[i] = rMin + (i+1) * step;
        v[i] = potential(r[i]) + orbitalFactor/(r[i] * r[i]);
    }

    // setting up a tridiagonal matrix and finding eigenvectors and -values
    arma::mat hamilton = arma::zeros<arma::mat>(dim, dim);
    hamilton(0,0) = diagConst  + v[0];
    hamilton(0,1) = offDiagConst;

    for (int i = 1; i < dim - 1; i++ ) {
        hamilton(i,i-1) = offDiagConst;
        hamilton(i,i) = diagConst + v[i];
        hamilton(i,i+1) = offDiagConst;
    }

    hamilton(dim-1,dim-2) = offDiagConst;
    hamilton(dim-1,dim-1) = diagConst + v[dim-1];

    // diagonalize and obtain eigenvalues, unsorted
    arma::vec eigValues;
    arma::mat eigVectors;

    // The algorithm
    arma::eig_sym(eigValues, eigVectors, hamilton);

    eigValues.save("eigval.txt", arma::arma_ascii);
    eigVectors.save("eigvec.txt", arma::arma_ascii);
    r.save("radial_val.txt", arma::arma_ascii);

    std::cout << "Hello World!" << step << std::endl;
    return 0;
}

void f(double  * a){
    *a = 10.;
}

void initialize(double *rMin, double *rMax, int* lOrbital, int* dim){
    *rMin = 0.0;
    *rMax = 5.0;
    *lOrbital = 0;
    *dim = 200;
}


double potential(double r){
    return r*r;
}
