#include "solve.h"
#include <armadillo>

void jacobiSolver(arma::vec& eigval, arma::vec& eigvec, arma::mat& A);
void jacobiRotate(arma::mat& A, arma::vec& R ,int k, int l,int n);
double maxOffDiag(arma::mat& A, int& k, int& l, int n);

// Finding best

solve::solve()
{
    int A = 1;
    std::cout << A << std::endl;
}

void jacobiSolver(arma::vec& eigval, arma::vec& eigvec, arma::mat& A){
    int n = A.size();
    double max_akl;
    int k,l;
    double tol = 1e-8;
    while (max_akl > tol){
        max_akl = maxOffDiag(A,k,l,n);
        jacobiRotate(A,eigvec,k,l,n);
        std::cout << A << std::endl;
    }

}


void jacobiRotate(arma::mat& A, arma::vec& R, int k, int l, int n){
    // Rotates the matrix A in place so that A(k,l)=A(l,k)=0.
    // Also rotates the eigenvector for A, R
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
    A(k,l) = 1.0;
    A(l,k) = 1.0;

    for (int i = 0; i < n; i ++) {
        if (i != k && i != l) {
            double aki = A(k,i);
            double ali = A(l,i);
            A(i,k) = A(k,i) = c*aki - s*ali;
            A(i,l) = A(l,i) = c*ali + s*aki;
        }
        double rik = R(i,k);
        double ril = R(i,l);
        R(i,l) = c*rik - s*ril;
        R(i,k) = c*ril + s*rik;
    }
    return;
}

double maxOffDiag(arma::mat& A, int &k, int &l, int n){
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


















