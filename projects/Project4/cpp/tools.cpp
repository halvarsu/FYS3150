
#include "tools.h"

using namespace std;

int readData(string filename, int& NMC, double & Tstart, double& Tstop, double& Tstep, int &L, bool & timeit, bool & saveToFile, bool & orderedSpinConfig){
    std::ifstream infile(filename);
    int temp;
    if(!(infile >> NMC)) { return 1;};

    if(!(infile >> Tstart >> Tstop >> Tstep)) { return 3;};

    if(!(infile >> L)) { return 2;};

    if(!(infile >> temp)) { return 4;};
    timeit = (bool) temp;

    if(!(infile >> temp)) { return 5;};
    saveToFile = (bool) temp;

    if(!(infile >> temp)) { return 6;};
    orderedSpinConfig = (bool) temp;

    return 0;
}

int periodic(int i, int limit, int add)
{
    return (i + limit + add) % (limit);
}

