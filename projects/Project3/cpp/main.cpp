#include <iostream>
#include <fstream>
#include <armadillo>
#define PI 3.14159265359

void initialize(arma::mat& pos, arma::mat& vel,
                double x0, double y0,double z0, double vx0, double vy0, double vz0);

void eulerChromer(arma::mat& pos, arma::mat& vel, double dt);

int main(int argc, char * argv[]) {
    int n = 10000;
    double T = 10;
    double dt = 0.01;
    int n_dim = 3;

    arma::mat pos, vel;
    pos = arma::zeros<arma::mat>(n,2);
    vel = arma::zeros<arma::mat>(n,2);
    initialize(pos, vel, 1, 0, 0, 0, 2*PI,0);
    eulerChromer(pos, vel, dt);
    pos.save("out/pos", arma::arma_ascii);
    vel.save("out/vel", arma::arma_ascii);
    return 0;
}


void initialize(arma::mat& pos, arma::mat& vel,
                double x0, double y0, double z0, double vx0, double vy0, double vz0){
    pos[0,0] = x0;
    pos[0,1] = y0;
    pos[0,2] = z0;
    vel[0,0] = vx0;
    vel[0,1] = vy0;
    vel[0,2] = vy0;
}

void eulerChromer(arma::mat& pos, arma::mat& vel, double dt){
    int n = pos.n_rows;
    double r;
    double G = 4*PI*PI;

    for (int i = 0; i < n-1; i++) {
        r = sqrt(pos[i,0]*pos[i,0]+ pos[i,1]*pos[i,1] + pos[i,2]*pos[i,2]);
        vel[i+1] = vel[i] - (G*pos[i])/(r*r*r)*dt;
        pos[i+1] = pos[i] + vel[i+1]*dt;
    }
}
