#include "solve.h"
#include <armadillo>

// Finding best

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
    n = A.n_cols;
    double max_akl = std::numeric_limits<double>::infinity();
    int k,l;
    double tol = 1e-8;

    eigvec = arma::eye<arma::mat>(n,n);

    for (unsigned int i = 0; i < max_iter; i++) {
        if (max_akl > tol ){
            max_akl = maxOffDiag(A,k,l,n);
            jacobiRotate(A,eigvec,k,l,n);
           } else {
            break;
        }
    }
    eigval = A.diag();
}







