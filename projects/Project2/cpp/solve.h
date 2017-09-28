#ifndef SOLVE_H
#define SOLVE_H

#include <armadillo>

void jacobiSolver(arma::vec& eigval, arma::mat& eigvec, arma::mat& A);
void jacobiRotate(arma::mat& A, arma::mat& R ,int k, int l,int n);
double maxOffDiag(arma::mat& A, int& k, int& l, int n);

class solve
{
public:
    solve();
};

#endif // SOLVE_H
