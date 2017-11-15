import subprocess
import numpy as np
import matplotlib.pyplot as plt
import shutil 
import time
import argparse
from tools import sine_print, linear_print

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--load', action="store_true")
    parser.add_argument('-p', '--part', choices=list("Xbcde"),default="X")
    parser.add_argument('-m', '--mpi', action="store_true")
    parser.add_argument('-n', '--nodes', type=int, default=2)
    return parser.parse_args()


def main():
    args = get_args()
    parts = {"b":compare_analytical,"c":graphical}
    if args.part == "X":
        graphical(args) 
        compare_analytical(args)
    else:
        f = parts[args.part]
        f(args)


def compare_analytical(args):
    montecarlosims = np.logspace(1,5,100)
    data = np.zeros((6,len(montecarlosims)))
    # width = shutil.get_terminal_size((80,20)).columns
    width = 40

    print_method = 'sine'
    T = 1
    # prev = time.time()
    for i,NMC in enumerate(montecarlosims):
        NMC = int(NMC)
        
        if print_method == 'sine':
            sine_print(str(NMC),i,width)
        else:
            linear_print(str(NMC), i, width, len(montecarlosims))
        out = subprocess.check_output("build/Project4 {} {}".format(NMC, T), shell = True)
        out = list(map(float, out.split()))
        data[:,i] = out
        # avgE, avgM, avgEsquared, avgMsquared, specific_heat, susceptibility = 

    np.save("analyse/4b",data )

    Z = 12 + 4*np.cosh(8/T)
    evE = 32*np.sinh(8/T)/Z
    evM = 0
    evEsquared = 256*np.cosh(8/T)/Z
    evMsquared = ( 32 + 32*np.exp(8/T) )/Z
    specific_heat  = 1/T**2 * (evEsquared - evE**2)
    susceptibility = 1/T**2 * (evMsquared - evM**2)

    expected_values = [evE, evM, evEsquared, evMsquared, specific_heat,
            susceptibility]
    ylabels = [r'$\langle E \rangle$',
            r'$\langle M \rangle$',
            r'$\langle E^2 \rangle$',
            r'$\langle M^2 \rangle$',
            r'$C_V$',
            r'$\chi$']
    print(data[:,-1])
    print(expected_values)
    fig1, [ax1,ax2,ax3,ax4] = plt.subplots(4)
    fig2, [ax5,ax6] = plt.subplots(2,sharex=True)

    ax1.scatter(montecarlosims,data[0],s=5)
    ax2.scatter(montecarlosims,data[1],s=5)
    ax3.scatter(montecarlosims,data[2],s=5)
    ax4.scatter(montecarlosims,data[3],s=5)
    ax5.scatter(montecarlosims,data[4],s=5)
    ax6.scatter(montecarlosims,data[5],s=5)

    ax4.set_xlabel('Number of Monte Carlo Cycles')
    ax6.set_xlabel('Number of Monte Carlo Cycles')

    for i,ax in enumerate([ax1,ax2,ax3,ax4,ax5,ax6]):
        ax.set_xscale('log')
        ax.set_ylabel(ylabels[i])
        ax.legend()
        ax.axhline(expected_values[i], linestyle='--', color = 'k', label='Analytical')
    fig1.tight_layout()
    fig2.tight_layout()
    fig1.savefig('results/compareAnalyticalExpectations.pdf')
    fig2.savefig('results/compareAnalytical.pdf')
    plt.show()


def process_data(data):
    sim_data = []
    for simulation in data:
        line_data = []
        lines = simulation.split('\n')
        for line in lines:
            out = [float(d) for d in line.split()]
            if out:
                line_data.append(out)
        sim_data.append(line_data)
    return np.array(sim_data).swapaxes(0,1).swapaxes(1,2)

def simulate4c(args):
    montecarlosims = np.logspace(3,6,200)
    # data = np.zeros((6,len(montecarlosims)))
    string_data = []
    width = 40
    
    Tstart = 1
    Tstop = 2.4
    nStep = 2
    Tstep = (Tstop-Tstart)/(nStep - 1) if nStep > 1 else 0
    L = 20

    run_cmd = "mpirun -np {}".format(args.nodes) if args.mpi else ""
    run_cmd += "build/Project4 {} {} {} {} {}".format("{}",
            Tstart, Tstop, Tstep, L)

    for i,NMC in enumerate(montecarlosims):
        NMC = int(NMC)
        print(str(NMC)+"/"+str(max(montecarlosims)))
        prev = time.time()
        out = subprocess.check_output(run_cmd.format(NMC), shell = True)
        print("time used: ", time.time() - prev)
        string_data.append(out)
    data = process_data(string_data)
    return data

def graphical(args):
    if args.load:
        data = np.load("analyse/4c.npy")
    else:
        data = simulate4c(args)
        np.save("analyse/4c")

    fig1, [ax1,ax2,ax3,ax4] = plt.subplots(4)
    fig2, [ax5,ax6] = plt.subplots(2,sharex=True)
    for T, temperated_data in zip(np.linspace(Tstart, Tstop, nStep),data):
        ax1.scatter(montecarlosims,temperated_data[2],s=5, label=r'$T = %.2f$' %T)
        ax2.scatter(montecarlosims,temperated_data[3],s=5, label=r'$T = %.2f$' %T)
        ax3.scatter(montecarlosims,temperated_data[4],s=5, label=r'$T = %.2f$' %T)
        ax4.scatter(montecarlosims,temperated_data[5],s=5, label=r'$T = %.2f$' %T)
        ax5.scatter(montecarlosims,np.abs(temperated_data[0]),s=5, label=r'$T = %.2f$' %T)
        ax6.scatter(montecarlosims,np.abs(temperated_data[1]),s=5, label=r'$T = %.2f$' %T)
    ylabels = [ r'$\langle E^2 \rangle$',
            r'$\langle M^2 \rangle$',
            r'$C_V$',
            r'$\chi$',
            r'$\langle |E| \rangle$',
            r'$\langle |M| \rangle$' ]

    [ax.legend() for ax in [ax1,ax2,ax3,ax4,ax5,ax6]]
    ax4.set_xlabel('Number of Monte Carlo Cycles')
    ax6.set_xlabel('Number of Monte Carlo Cycles')

    for i,ax in enumerate([ax1,ax2,ax3,ax4,ax5,ax6]):
        ax.set_xscale('log')
        ax.set_ylabel(ylabels[i])
        ax.legend()
        #ax.axhline(expected_values[i], linestyle='--', color = 'k', label='Analytical')
    fig1.tight_layout()
    fig2.tight_layout()
    fig1.savefig('results/graphicalOthers.pdf')
    fig2.savefig('results/graphical.pdf')
    plt.show()

if __name__ == "__main__":
    main()
