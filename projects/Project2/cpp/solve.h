#ifndef SOLVE_H
#define SOLVE_H

#include <armadillo>

void save(arma::vec&, arma::vec&, arma::mat&, std::string);
int hamiltonSolve(double, double, int, double, int, bool, std::string = "jacobi");
int hamiltonSolve(arma::vec&, arma::mat&, double, double, int, double, int, bool, std::string = "jacobi");
void jacobiSolver(arma::vec&, arma::mat&, arma::mat&);
void jacobiRotate(arma::mat&, arma::mat& ,int, int, int);
double maxOffDiag(arma::mat&, int&, int&, int);
double potential(double, double, bool);

class solve
{
public:
    solve();
};

#endif // SOLVE_H
