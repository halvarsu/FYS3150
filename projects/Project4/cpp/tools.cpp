#include <random>
#include "tools.h"


int periodic(int i, int limit, int add)
{
    return (i + limit + add) % (limit);
}

