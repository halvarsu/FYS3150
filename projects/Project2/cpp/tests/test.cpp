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
    A << 1 << 2 << 3 << arma::endr
      << 1 << 2 << 3 << arma::endr
      << 1 << 2 << 3;
    std::cout << A << std::endl;
}
