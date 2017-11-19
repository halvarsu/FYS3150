import subprocess
import argparse
import numpy as np
import matplotlib.pyplot as plt

def main(args):
    """Either runs all parts or just one"""
    parts = {1:timing}
    if args.part == 0:
        timing(args)
    else:
        parts[args.part]()


def timing(args):
    NMC = 10
    Tstart = 2
    Tstop = 2
    nTemp = 1000
    L = 40

    nTrials = 100
    trials = np.arange(nTrials)
    time = []
    time_parallel = []
    run = "mpirun -np 1 ./build/Project4 {} {} {} {} {} 1"
    run_parallel = "mpirun -np 4 ./build/Project4 {} {} {} {} {} 1"
    for i in trials:
        out_parallel = subprocess.check_output(run_parallel.format( 
            NMC, Tstart, Tstop, nTemp, L), shell = True)
        out = subprocess.check_output(run.format(
            NMC, Tstart, Tstop, nTemp, L), shell = True)
        t = float(out.split('\n')[0].split()[1])
        tp = float(out_parallel.split('\n')[0].split()[1])
        print(t, tp)
        time.append(t)
        time_parallel.append(tp)
    avg_time = np.average(time)
    avg_time_parallel = np.average(time_parallel)
    print('Average time used 1 prosessor: {}s'.format(avg_time))
    print('Average time used 4 prosessors: {}s'.format(avg_time_parallel))
    plt.scatter(trials, time)
    plt.scatter(trials, time_parallel)
    plt.xlabel('Trial number')
    plt.ylabel('Time used $[s]$')
    plt.legend(['1 prosessor', '4 prosessors'])
    plt.savefig('results/timing.pdf')
    #plt.show()
    return
    

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-p','--part', type=int,default=0, 
                        choices = [0,1,2,3])
    return parser.parse_args()

if __name__=='__main__':
    args = get_args()
    main(args)

