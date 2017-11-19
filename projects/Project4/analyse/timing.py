import subprocess
import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from tools import add_letter_label

def main(args):
    """Either runs all parts or just one"""
    parts = {1:plot_timing,2:create_results}
    if args.part == 0:
        plot_timing(args)
        create_results(args)
    else:
        parts[args.part](args)


def timing(args):
    """Runs the metropolis solver with the inbuilt timer, catching the
    result and plotting a nice graph."""
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

def create_results(args):
    time1 = np.load('results/time_no_parNMC%d.npy' %1000)
    time_parallel1 = np.load('results/time_parNMC%d.npy' %1000)
    time2 = np.load('results/time_no_parNMC%d.npy' %10000)
    time_parallel2 = np.load('results/time_parNMC%d.npy' %10000)
    avg1 = np.average(time1) 
    avgP1 = np.average(time_parallel1) 
    avg2 = np.average(time2) 
    avgP2 = np.average(time_parallel2) 
    ratio1 = avg1 / avgP1
    ratio2 = avg2 / avgP2
    
    print('avg1: {} avgP1: {}'.format(avg1, avgP1))
    print('avg2: {} avgP2: {}'.format(avg2, avgP2))
    print('Ratio 1: {}'.format(ratio1))
    print('Ratio 2: {}'.format(ratio2))
    fig1, [ax1,ax2] = plt.subplots(2,figsize = [4,4])
    trials = np.arange(time1.size)
    print(time1.shape, time2.shape, time_parallel1.shape,time_parallel2.shape)
    ax1.scatter(trials, time1)#, c = 'b')
    ax2.scatter(trials, time2)#, c = 'b')
    ax1.scatter(trials, time_parallel1)#, c = 'g')
    ax2.scatter(trials, time_parallel2)#, c = 'g')
    for i,[ax,t] in enumerate(zip([ax1,ax2], [time1,time2])):
        ax.set_xlabel('Trial number')
        ax.set_ylabel('Time used $[s]$')
        ax.legend(['1 prosessor', '4 prosessors'])
        #ax.axis([-1,trials.size + 1, 0, 1.5*np.median(t)])
        add_letter_label(ax,i)
    fig1.tight_layout()
    fig1.savefig('results/timingResults.pdf' )
    plt.show()

    

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

