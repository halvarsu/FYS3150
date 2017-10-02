#include "solve.h"
#include <armadillo>

// Finding best
int hamiltonSolve(double rhoMin, double rhoMax, int dim,
                  double omega, int lOrbital, bool interacting, std::string solver){
    arma::vec eigval;
    arma::mat eigvec;
    return hamiltonSolve(eigval, eigvec, rhoMin, rhoMax, dim, omega, lOrbital, interacting, solver);
}

int hamiltonSolve(arma::vec& eigval, arma::mat& eigvec, double rhoMin, double rhoMax, int dim,
                  double omega, int lOrbital, bool interacting, std::string solver){
    arma::vec rho, v;
    arma::mat hamilton;
    double step, diagConst, offDiagConst, orbitalFactor;
    int iterationsUsed;
    std::string filename;
    char* temp;

    step = (rhoMax - rhoMin)/(dim);
    diagConst = 2.0/(step*step);
    offDiagConst = -1.0/(step*step);
    orbitalFactor = lOrbital * ( lOrbital + 1.0 );

    rho = arma::zeros(dim);
    v = arma::zeros(dim);

    for	(int i = 0; i < dim; i++){
        rho[i] = rhoMin + (i+1)*step;
        v[i] = potential(rho[i], omega, interacting); //+ orbitalFactor/(rho[i] * rho[i]);
    }
//    std::cout << step << std::endl;
//    std::cout << rho(1) - rho(0) << std::endl;
//    std::cout << rho(dim-1) << std::endl;

    // setting up a tridiagonal matrix
    hamilton = arma::zeros<arma::mat>(dim, dim);
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
    if ((std::string) solver == "jacobi") {
        iterationsUsed = jacobiSolver(eigval, eigvec, hamilton);
    } else if((std::string) solver == "arma") {
        arma::eig_sym(eigval, eigvec, hamilton);
        iterationsUsed = 0;
    }

    temp = new char[30];
    if (interacting) {
        std::sprintf(temp, "omega_%.2f_rho_%.2f_N_%d",omega, rhoMax, dim);
        filename = solver + "/interacting/" + (std::string) temp;
    } else {
        std::sprintf(temp, "rho_%.2f_N_%d",rhoMax, dim);
        filename = solver + "/non_interacting/" + (std::string) temp;
    }
    std::cout << "saving " << filename << std::endl;
    save(rho, eigval, eigvec, filename);
    return iterationsUsed;
}

void save(arma::vec& rho,arma::vec& eigval,arma::mat& eigvec, std::string filename) {
    eigval.save((std::string)filename+"val.txt", arma::arma_ascii);
    eigvec.save((std::string)filename+"vec.txt", arma::arma_ascii);
    rho.save((std::string)filename+"rho.txt", arma::arma_ascii);
}

double potential(double r, double omega, bool interacting){
    if (interacting) {
        return omega*omega*r*r +1/r;
    } else {
        return r*r;
    }
}


int jacobiSolver(arma::vec& eigval, arma::mat& eigvec, arma::mat& A){
    unsigned int iter, max_iter, n;
    n = A.n_cols;
    max_iter = n*n*n;
    double max_akl = std::numeric_limits<double>::infinity();
    int k,l;
    double tol = 1e-8;

    eigvec = arma::eye<arma::mat>(n,n);

    for (iter = 0; iter < max_iter; iter++) {
        if (max_akl > tol ){
            max_akl = maxOffDiag(A,k,l,n);
            jacobiRotate(A,eigvec,k,l,n);
           } else {
            break;
        }
    }
    eigval = A.diag();
    return iter;
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
    } else {
        return;
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












