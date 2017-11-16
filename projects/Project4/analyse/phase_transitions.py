import argparse
import numpy as np
import matplotlib.pyplot as plt
import subprocess


def main(args):
    """Either runs all parts or just one"""
    parts = {1:phase_transitions}
    if args.part == 0:
        phase_transitions(args)
    else:
        parts[args.part]()

def calculate_phase_transitions(args):
    # NMC = 100000
    # Tstart = 2
    # Tstop = 2.3
    # nTemps = 100
    # Tstep = (Tstop - Tstart)/(nTemps-1) if nTemps > 1 else 0
    
    # results = []
    # run_cmd = ("mpirun -np 4 ./build/Project4"+ 8 * " {}")
    # run_cmd = run_cmd.format(NMC, Tstart, Tstop, nTemps, '{0}', 1, 0,
    #         "phasetransL{0}")

    # lattice_sizes = [20]
    # data = np.zeros((7,len(lattice_sizes)))

    # for L in lattice_sizes:
    #     r = subprocess.check_output(run_cmd.format(L),
    #             shell=True)#, stdout=subprocess.PIPE) 
    #     results.append(r)
    return

def plot_phase_transition(args):
    L_values = [40,60,80]
    for L in L_values:
        data = np.zeros((0,9))
        for sub in range(1,9):
            sub_data = np.loadtxt("out_gather/pt_sub{}_L{}.dat".format(sub,L))
            print(data.shape,sub_data.shape)
            data = np.concatenate((data,sub_data))
        plt.scatter(data[:,1],data[:,6]/L**2,alpha=0.5,
                label='L = {}'.format(L),c = plt.cm.jet((L-40)/60.))
    plt.xlabel('Temperature')
    plt.ylabel('$C_V$')
    plt.legend()
    plt.savefig('temp/fig2.png')
    plt.show()


plot_phase_transition(None)
    

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-p','--part', type=int,default=0, 
                        choices = [0,1,2,3])
    return parser.parse_args()

if __name__=='__main__':
    args = get_args()
    # main(args)
