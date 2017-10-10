#include <iostream>
#include <fstream>
#include <armadillo>
#define PI 3.14159265359

using namespace std;

void initialize(arma::mat& pos, arma::mat& vel,
                double x0, double y0,double z0, double vx0, double vy0, double vz0);

void eulerChromer(arma::mat& pos, arma::mat& vel, double dt);

int main(int argc, char * argv[]) {
    int n = 10000;
    double T = 10.;
    double dt = T/n;

    arma::mat pos, vel;
    pos = arma::zeros<arma::mat>(n,3);
    vel = arma::zeros<arma::mat>(n,3);
    initialize(pos, vel, 1, 0, 0, 0, 2*PI,0);
    eulerChromer(pos, vel, dt);
    pos.save("out/pos.txt", arma::arma_ascii);
    vel.save("out/vel.txt", arma::arma_ascii);
    pos.print();
    arma::vec test;
    test = arma::ones(3);
    test.print();
    double test2;
    cout << test2 << std::endl;
    return 0;
}


void initialize(arma::mat& pos, arma::mat& vel,
                double x0, double y0, double z0, double vx0, double vy0, double vz0){
    pos(0,0) = x0;
    pos(0,1) = y0;
    pos(0,2) = z0;
    vel(0,0) = vx0;
    vel(0,1) = vy0;
    vel(0,2) = vz0;
}

void eulerChromer(arma::mat& pos, arma::mat& vel, double dt){
    int n = pos.n_rows;
    cout << n << endl;
    double r;
    double G = 4*PI*PI;

    for (int i = 0; i < n-1; i++) {
        r = sqrt(pos(i,0)*pos(i,0)+ pos(i,1)*pos(i,1) + pos(i,2)*pos(i,2));
        vel(i+1,0) = vel(i,0) - (G*pos(i,0))/(r*r*r)*dt;
        pos(i+1,0) = pos(i,0) + vel(i+1,0)*dt;
        vel(i+1,1) = vel(i,1) - (G*pos(i,1))/(r*r*r)*dt;
        pos(i+1,1) = pos(i,1) + vel(i+1,1)*dt;
        vel(i+1,2) = vel(i,2) - (G*pos(i,2))/(r*r*r)*dt;
        pos(i+1,2) = pos(i,2) + vel(i+1,2)*dt;
    }
}
