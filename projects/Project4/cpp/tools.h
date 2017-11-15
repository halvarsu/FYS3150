#ifndef TOOLS_H
#define TOOLS_H

#include <string>
#include <fstream>

using namespace std;

int periodic(int i, int limit, int add);
int readData(string filename, int& NMC, double & Tstart, double &Tstop, int &Tstep, int &L, bool & timeit, bool & save_to_file, bool & orderedSpinConfig);

#endif // TOOLS_H
