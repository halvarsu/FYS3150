#include <iostream>
#include <fstream>

using namespace std;

int main(int argc, char * argv[])
{
    std::ofstream test;
    cout << "Hello World!" << endl;
    test.open("out/" + (string) argv[1]);
    test << "HEI";
    test.close();
    return 0;
}
