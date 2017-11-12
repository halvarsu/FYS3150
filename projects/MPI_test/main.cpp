//    First C++ example of MPI Hello world
using namespace std;
#include <mpi.h>
#include <iostream>

int main (int argc, char* argv[])
{
    int processCount, localRank;
    //   MPI initializations

    MPI_Init (&argc, &argv);
    MPI_Comm_size (MPI_COMM_WORLD, &processCount);
    MPI_Comm_rank (MPI_COMM_WORLD, &localRank);

    string me = "(Process " + to_string(localRank) + ") ";
    double a;
    if (localRank == 0){
        cout << "=================== Illustrating MPI_Bcast and MPI_Reduce: ==================" << endl;
        cout << me << "Give me a number to send to the other " << processCount-1<< " processes." << endl;
        cout << "a = ";
        cin >> a;
    }
    MPI_Bcast(&a, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    cout << me <<"a = "<< a << endl;


    double aTotal;
    cout << me << "Ready for sending a for summation..." << endl;
    MPI_Reduce(&a, &aTotal, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

    if (localRank == 0) {
        cout << me << "Received all a's. aTotal = " << aTotal << endl;
    }

    double sendData[processCount];
    if (localRank == 0){
        cout << "========= Illustrating MPI_Scatter and multiplication with MPI_Reduce: =====" << endl;
        cout << me <<"Give me " << processCount << " numbers to distribute to all processes:" << endl;
        for (int i = 0; i < processCount; i++){
            cout << "value" << i << " = ";
            cin >> sendData[i];
        }
    }
    double value;
    MPI_Scatter(&sendData, 1, MPI_DOUBLE, &value, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    cout << me << "Received value = " << value << endl;
    cout << me << "Adding 1 ";
    value += 1;
    cout << " (value = "<< value << ")" << endl;
    cout << me << "Ready for reduction" << endl;
    double prod;
    MPI_Reduce(&value,&prod,1,MPI_DOUBLE, MPI_PROD, 0, MPI_COMM_WORLD);
    if (localRank == 0){
        cout << me << "Product = " << prod << endl;
    }

    MPI_Finalize ();
    return 0;
}
