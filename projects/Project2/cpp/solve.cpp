#include "solve.h"
#include <armadillo>

// Finding best

int hamiltonSolve(arma::vec& rho, arma::vec& eigval, arma::mat& eigvec, double omega, int lOrbital, bool interacting){
    int dim = rho.n_rows;
    double step = rho[1] - rho[0];
    double diagConst = 2.0/(step*step);
    double offDiagConst = -1.0/(step*step);
    double orbitalFactor = lOrbital * ( lOrbital + 1.0 );
    arma::vec v = arma::zeros(dim);

    for	(int i = 0; i < dim; i++){
        v[i] = potential(rho[i], omega, interacting) + orbitalFactor/(rho[i] * rho[i]);
    }

    // setting up a tridiagonal matrix
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

    // The algorithm to solve ham and fill in eigenvectors and -values
    // arma::eig_sym(eigValues, eigVectors, hamilton);
    jacobiSolver(eigval, eigvec, hamilton);

    return 0;
}

double potential(double r, double omega, bool interacting){
    if (interacting) {
        return omega*omega*r*r +1/r;
    } else {
        return r*r;
    }
}


double maxOffDiag(arma::mat& A, int &k, int &l, int n){
    /* Accepts a matrix, two indices and the size of the matrix,
     * sets the indices to argmax(A) and returns max(A) */
    double maxOff = 0;
    for (int i = 0; i < n; i++){
        for (int j = i+1; j < n; j++){
            if (A(i,j)*A(i,j) > maxOff){
                maxOff = A(i,j)*A(i,j);
                k = i;
                l = j;
            }
        }
    }
    return maxOff;
}


void jacobiRotate(arma::mat& A, arma::mat& R, int k, int l, int n){
    /* Rotates the matrix A in place so that A(k,l)=A(l,k)=0.
     * Also rotates the eigenvector for A, R */
    double c,s,t;
    if ( A(k,l) != 0.0) {
        double tau = (A(l,l)- A(k,k))/(2*A(k,l));
        if (tau > 0) {
            t = 1.0/(tau + sqrt (1.0 + tau*tau));
        } else {
            t = -1.0/(-tau + sqrt(1.0 + tau*tau));
        }
        c = 1/sqrt(1+t*t);
        s = t*c;
    }
    double akk = A(k,k);
    double all = A(l,l);

    A(k,k) = c*c*akk  - 2.0 * c*s*A(k,l) + s*s*all;
    A(l,l) = s*s*akk  + 2.0 * c*s*A(k,l) + c*c*all;
    A(k,l) = 0.0;
    A(l,k) = 0.0;

    for (int i = 0; i < n; i ++) {
        if (i != k && i != l) {
            double aki = A(k,i);
            double ali = A(l,i);
            A(i,k) = A(k,i) = c*aki - s*ali;
            A(i,l) = A(l,i) = c*ali + s*aki;
        }
        double rik = R(i,k);
        double ril = R(i,l);
        R(i,k) = c*rik - s*ril;
        R(i,l) = c*ril + s*rik;
    }
    return;
}




void jacobiSolver(arma::vec& eigval, arma::mat& eigvec, arma::mat& A){
    unsigned int max_iter, n;
    unsigned int iter;
    n = A.n_cols;
    max_iter = n*n*n;
    double max_akl = std::numeric_limits<double>::infinity();
    int k,l;
    double tol = 1e-8;

    eigvec = arma::eye<arma::mat>(n,n);

    for (unsigned int i = 0; i < max_iter; i++) {
        if (max_akl > tol ){
            max_akl = maxOffDiag(A,k,l,n);
            jacobiRotate(A,eigvec,k,l,n);
           } else {
            std::cout << "iterations used: " << i << std::endl;
            break;
        }
    }
    eigval = A.diag();
}








