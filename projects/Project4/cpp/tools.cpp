
#include "tools.h"

using namespace std;

void readData(string filename, int& NMC, double & T, int &L, bool & parallel, bool & timeit, bool & save_to_file, bool & orderedSpinConfig){
    std::ifstream infile(filename);
    infile >> NMC;
    infile >> T;
    infile >> L;
    infile >> parallel;
    infile >> timeit;
    infile >> save_to_file;
    infile >> orderedSpinConfig;
    return;
}

int periodic(int i, int limit, int add)
{
    return (i + limit + add) % (limit);
}

