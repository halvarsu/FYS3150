import argparse
import numpy as np
import matplotlib.pyplot as plt
import subprocess
from tools import add_letter_label,savitzky_golay



def main(args):
    """Either runs all parts or just one"""
    parts = {1:plot_phase_transition}
    if args.part == 0:
        plot_phase_transition(args)
    else:
        parts[args.part](args)

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
    """
    loads preproduces phase precession data and calculates the critical
    temperature, along with making a plot.
    """
    L_values = [40,60,80,100]
    fig1, [[ax1,ax2],[ax3,ax4]] = plt.subplots(2,2,
            figsize=args.figsize)
    # fig2, ax2 = plt.subplots(1, figsize=args.figsize)
    TC_values = []
    for L in L_values:
        data = np.zeros((0,9))
        for sub in range(1,9):
            sub_data = np.loadtxt("out_gather/pt_sub{}_L{}.dat".format(sub,L))
            data = np.concatenate((data,sub_data))
        ax1.scatter(data[:,1],data[:,2]/L**2,alpha=0.3,s=3,
                label='L = {}'.format(L),c = plt.cm.jet((L-40)/60.))
        ax2.scatter(data[:,1],np.abs(data[:,3])/L**2,alpha=0.3,s=3,
                label='L = {}'.format(L),c = plt.cm.jet((L-40)/60.))
        ax3.scatter(data[:,1],data[:,6]/L**2,alpha=0.3,s=3,
                label='L = {}'.format(L),c = plt.cm.jet((L-40)/60.))
        ax4.scatter(data[:,1],data[:,7]/L**2,alpha=0.3,s=3,
                label='L = {}'.format(L),c = plt.cm.jet((L-40)/60.))
        C_V_smooth = savitzky_golay(data[:,6], 15, 2)
        ax3.plot(data[:,1],C_V_smooth/L**2, '--')
        T_c = data[[np.argmax(C_V_smooth)],1][0]
        TC_values.append(T_c)
        print("T(L={}) = {}".format(L,T_c))
    from scipy import optimize

    TC_values = np.array(TC_values)
    def T_Cfunc(L, T_Cinfty, a):
        return T_Cinfty + a/L

    popt, pcov = optimize.curve_fit(T_Cfunc, L_values, TC_values)
    print("Calculated value of T_C(L=infty): {} with a = {}".format(*popt))

    #ax1.set_xlabel('$T$ [ $k_B/J$ ]')
    ax1.set_xlabel('$T$ [ $k_B/J$ ]')
    ax2.set_xlabel('$T$ [ $k_B/J$ ]')
    ax3.set_xlabel('$T$ [ $k_B/J$ ]')
    ax4.set_xlabel('$T$ [ $k_B/J$ ]')
    ax1.set_ylabel(r'$\langle E \rangle $ [ $J$ ]')
    ax2.set_ylabel(r'$\langle |M| \rangle $ ')
    ax3.set_ylabel(r'$c_V$ [ $k_B$ ]')
    ax4.set_ylabel(r'$\chi$ [ $J/k_B^2$ ]')
    [add_letter_label(ax,i) for i,ax in enumerate([ax1,ax2,ax3,ax4])]
    # [ax.legend() for ax in [ax1,ax2]]
    # [ax.grid() for ax in [ax1,ax2]]
    ax1.legend()
    # [fig.tight_layout() for fig in [fig1,fig2]]
    fig1.tight_layout() 
    fig1.savefig('results/critical_lowres.pdf')
    # fig2.savefig('results/criticalXI.pdf')
    plt.show()


    

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-p','--part', type=int,default=0, 
                        choices = [0,1,2,3])
    parser.add_argument('--figsize', type=int,nargs=2,default=[8,4])
    return parser.parse_args()

if __name__=='__main__':
    args = get_args()
    main(args)
