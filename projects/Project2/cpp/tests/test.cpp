#include "solve.h"
#include "catch.hpp"
#include <armadillo>

TEST_CASE( "Test maxOffDiag") {
    int n , k, l;
    n = 5;
    arma::mat A = arma::randu<arma::mat>(n,n); // in range 0,1. TODO: Exchange with randint(need internet to find this func)
    A(3,4) =  A(4,3) = 10.;
    A(1,3) =  A(1,3) = 9.;
    REQUIRE(maxOffDiag(A, k, l, n) == 10.*10.);
    REQUIRE(k == 3);
    REQUIRE(l == 4);
}

TEST_CASE("Test jacobiRotate") {
    int n;
    n = 5;
    arma::mat A = arma::randu<arma::mat>(n,n); // in range 0,1. TODO: Exchange with randint(need internet to find this func)
    arma::mat vectors = arma::zeros<arma::mat>(n,n);
    A(3,4) =  A(4,3) = 10.;
    A(1,3) =  A(1,3) = 9.;
    jacobiRotate(A, vectors, 3, 4, n);
    REQUIRE(A(3,4) == 0);
    REQUIRE(A(4,3) == 0);
}

TEST_CASE("Test jacobiSolver") {
    int n = 3;
    arma::mat A;
    A << 2 << -4 << 2 << arma::endr
      << -4 << 4 << 4 << arma::endr
      << 2 << 4 << 2;
    arma::mat eigvec;
    arma::vec eigval, expect;
    expect << -4 << arma::endr << 4 << arma::endr << 8;

    jacobiSolver(eigval, eigvec, A);
    REQUIRE(arma::all(arma::vectorise(expect - arma::sort(eigval)) < 1e-10 ));
}


TEST_CASE("Test hamiltonSolve") {
    // testing orthogonality
    int dim = 100;
    double rhoMin = 0, rhoMax = 10., omega = 0;
    double step = (rhoMax - rhoMin)/dim;
    arma::mat eigvec, eigvecT, I, r;
    arma::vec eigval, rho;
    bool interacting = false;

    rho = arma::linspace(rhoMin + step, rhoMax, dim);
    hamiltonSolve(eigval, eigvec,  rhoMin, rhoMax, dim, omega, 0, interacting, "jacobi");

    eigvecT = arma::trans(eigvec);
    I = arma::eye(dim,dim);
    REQUIRE(arma::all(arma::vectorise(eigvec*eigvecT- I) < 1e-10));
}











