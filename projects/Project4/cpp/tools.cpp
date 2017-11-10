
#include "tools.h"

using namespace std;

int readData(string filename, int& NMC, double & T, int &L, bool & parallel, bool & timeit, bool & save_to_file, bool & orderedSpinConfig){
    std::ifstream infile(filename);
    int temp;
    if(!(infile >> NMC)) { return 1;};
    if(!(infile >> L)) { return 2;};
    if(!(infile >> T)) { return 3;};
    if(!(infile >> temp)) { return 4;};
    parallel = (bool) temp;
    if(!(infile >> temp)) { return 5;};
    parallel = (bool) timeit;
    if(!(infile >> temp)) { return 6;};
    parallel = (bool) save_to_file;
    if(!(infile >> temp)) { return 7;};
    parallel = (bool) orderedSpinConfig;
    return 0;
}

int periodic(int i, int limit, int add)
{
    return (i + limit + add) % (limit);
}

