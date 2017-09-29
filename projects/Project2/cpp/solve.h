#ifndef SOLVE_H
#define SOLVE_H

#include <armadillo>

int hamiltonSolve(arma::vec& rho, arma::vec& eigval, arma::mat& eigvec,
                  double omega, int lOrbital, bool interacting);
int hamiltonSolve(arma::vec& rho, arma::vec& eigval, arma::mat& eigvec,
                  double omega, int lOrbital, bool interacting,
                  std::string solver);
void jacobiSolver(arma::vec& eigval, arma::mat& eigvec, arma::mat& A);
void jacobiRotate(arma::mat& A, arma::mat& R ,int k, int l,int n);
double maxOffDiag(arma::mat& A, int& k, int& l, int n);
double potential(double r, double omega, bool interacting);

class solve
{
public:
    solve();
};

#endif // SOLVE_H
