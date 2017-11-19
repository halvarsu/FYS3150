import subprocess
import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main(args):
    """Either runs all parts or just one"""
    parts = {1:plot_timing}
    if args.part == 0:
        plot_timing(args)
    else:
        parts[args.part]()


def timing(args):
    NMC = args.NMC
    Tstart = 2
    Tstop = 2
    nTemp = 24
    L = 40

    nTrials = 20
    trials = np.arange(nTrials)
    time = []
    time_parallel = []
    run = "/usr/lib64/openmpi/bin/mpirun -np 1 ./build/Project4 {} {} {} {} {} 1"
    run_parallel = "/usr/lib64/openmpi/bin/mpirun -np 4 ./build/Project4 {} {} {} {} {} 1"
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
    time = np.array(time)
    time_parallel = np.array(time_parallel)
    np.save('results/time_no_parNMC%d'%NMC,time)
    np.save('results/time_parNMC%d'%NMC,time_parallel)
    return  time, time_parallel

def plot_timing(args):
    if args.load:
        time = np.load('results/time_no_parNMC%d.npy' %args.NMC)
        time_parallel = np.load('results/time_parNMC%d.npy' %args.NMC)
    else:
        time,time_parallel = timing(args)
    trials = np.arange(time.size)
    avg_time = np.average(time)
    avg_time_parallel = np.average(time_parallel)

    print('Average time used 1 prosessor: {}s'.format(avg_time))
    print('Average time used 4 prosessors: {}s'.format(avg_time_parallel))
    plt.scatter(trials, time, c = 'b')
    plt.scatter(trials, time_parallel, c = 'g')
    plt.xlabel('Trial number')
    plt.ylabel('Time used $[s]$')
    plt.legend(['1 prosessor', '4 prosessors'])
    plt.savefig('results/timingNMC%d.pdf' %args.NMC)
    #plt.show()
    return
    

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-p','--part', type=int,default=0, 
                        choices = [0,1,2,3])
    parser.add_argument('-N','--NMC', type=int,default=1000 )
    parser.add_argument('-l','--load' ,action='store_true')
    return parser.parse_args()

if __name__=='__main__':
    args = get_args()
    main(args)

