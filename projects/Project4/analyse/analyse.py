import subprocess
import numpy as np
import matplotlib.pyplot as plt
import shutil 
import time
import argparse
from tools import sine_print, linear_print, process_data, add_letter_label

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--load', action="store_true")
    parser.add_argument('-p', '--part', choices=list("Xbcde"),default="X")
    parser.add_argument('-m', '--mpi', action="store_true")
    parser.add_argument('-n', '--nodes', type=int, default=2)
    parser.add_argument('--figsize', type=int,nargs=2,default=[4,4])
    return parser.parse_args()


def main():
    """Chooses a part based on args.part. if 0, runs all parts defined."""
    args = get_args()
    parts = {"b":compare_analytical,"c":graphical}
    if args.part == "X":
        graphical(args) 
        compare_analytical(args)
    else:
        f = parts[args.part]
        f(args)


def compare_analytical(args):
    """
    Runs a 2x2 lattice simulation in parallel by starting several
    subprocesses all running the CPP code at the same time. Compares to
    analytical values.
    """
    montecarlosims = np.logspace(1,6,500)
    data = np.zeros((7,len(montecarlosims)))
    width = shutil.get_terminal_size((80,20)).columns
    # width = 40

    print_method = 'sine'
    T = 1
    # prev = time.time()
    results = []
    print("setting up")
    for i,NMC in enumerate(montecarlosims):
        print(i, NMC)
        NMC = int(NMC)
        
        r = subprocess.Popen("./build/Project4 {} {}".format(NMC,T),
                shell=True, stdout=subprocess.PIPE) 
        results.append(r)
        # out = subprocess.check_output("build/Project4 {} {}".format(NMC, T), shell = True)
        # out = list(map(float, out.split()))
        # data[:,i] =r out
    print("gathering data")
    for i, (NMC, r) in enumerate(zip(montecarlosims,results)):
        if print_method == 'sine':
            sine_print(str(NMC),i,width)
        else:
            linear_print(str(NMC), i, width, len(montecarlosims))
        out, err = r.communicate() # Wait on the results
        data[:,i] = list(map(float, out.split())) #.append(out)

    np.save("analyse/4b",data )

    Z = 12 + 4*np.cosh(8/T)
    evE = - 32*np.sinh(8/T)/Z
    evM = 0
    evEsquared = 256*np.cosh(8/T)/Z
    evMsquared = ( 32 + 32*np.exp(8/T) )/Z
    specific_heat  = 1/T**2 * (evEsquared - evE**2)
    susceptibility = 1/T**2 * (evMsquared - evM**2)

    expected_values = [evE, evM, evEsquared, evMsquared, specific_heat,
            susceptibility]
    ylabels = [r'$\langle E \rangle$ [ $J$ ]',
            r'$\langle M \rangle$',
            r'$\langle E^2 \rangle$ [ $J^2$ ]',
            r'$\langle M^2 \rangle$',
            r'$C_V$ [ $k_B$ ]',
            r'$\chi$ [ $J/k_B^2$ ]']
    print(data[:,-1])
    print(expected_values)
    fig1, [[ax1,ax2],[ax3,ax4]] = plt.subplots(2,2,figsize = [8,4])
    fig2, [ax5,ax6] = plt.subplots(2,figsize=args.figsize,sharex=True)

    ax1.scatter(montecarlosims,data[0],s=5)
    ax2.scatter(montecarlosims,data[1],s=5)
    ax3.scatter(montecarlosims,data[2],s=5)
    ax4.scatter(montecarlosims,data[3],s=5)
    ax5.scatter(montecarlosims,data[4],s=5)
    ax6.scatter(montecarlosims,data[5],s=5)

    ax1.set_xlabel('Number of Monte Carlo Cycles')
    ax2.set_xlabel('Number of Monte Carlo Cycles')
    ax3.set_xlabel('Number of Monte Carlo Cycles')
    ax4.set_xlabel('Number of Monte Carlo Cycles')
    ax6.set_xlabel('Number of Monte Carlo Cycles')

    [add_letter_label(ax,i) for i,ax in enumerate([ax5,ax6])]
    [add_letter_label(ax,i) for i,ax in enumerate([ax1,ax2,ax3,ax4])]

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

def simulate4c(args):
    """
    Returns simulated values for the 20x20 lattice, for two temperatures
    T=1 and T=2.4. Run CPP in parallel, if args.mpi is True.
    """
    montecarlosims = np.logspace(2,5,250)
    string_data = []
    width = 40
    
    Tstart = 1
    Tstop = 2.4
    nStep = 2
    Tstep = (Tstop-Tstart)/(nStep - 1) if nStep > 1 else 0
    temperatures = np.linspace(Tstart, Tstop, nStep)
    time_it = 0
    ordered_spin = 1

    L = 20

    run_cmd = "mpirun -np {} ".format(args.nodes) if args.mpi else ""
    run_cmd += "build/Project4 {} {} {} {} {} {} {}".format("{}",
            Tstart, Tstop, nStep, L, time_it, {})

    for i,NMC in enumerate(montecarlosims):
        NMC = int(NMC)
        print(str(NMC)+"/"+str(max(montecarlosims)))
        prev = time.time()
        out = subprocess.check_output(run_cmd.format(NMC, 0), shell = True)
        prev2 = time.time()
        outOrdered = subprocess.check_output(run_cmd.format(NMC, 1), shell = True)
        print("time used 1: ", prev2 - prev)
        print("time used 2: ", time.time() - prev2)
        string_data.append(out)
        string_data.append(outOrdered)
    data, dataOrdered = process_data(string_data, return_two = True)
    return data,dataOrdered, temperatures, montecarlosims

def graphical(args):
    """Creates the graphical solution of 4c"""
    if args.load:
        data = np.load("analyse/4cData.npy")
        dataOrdered = np.load("analyse/4cDataOrdered.npy")
        temperatures = np.load("analyse/4cTemps.npy")
        montecarlosims = np.load("analyse/4cNMC.npy")
    else:
        data, dataOrdered, temperatures, montecarlosims  = simulate4c(args)
        np.save("analyse/4cData",data)
        np.save("analyse/4cDataOrdered",dataOrdered)
        np.save("analyse/4cTemps",temperatures)
        np.save("analyse/4cNMC",montecarlosims)

    fig1, [[ax1,ax2],[ax1b,ax2b]] = plt.subplots(2,2,figsize=(6,6))
    fig2, ax3 = plt.subplots(1)

    print( data.shape, dataOrdered.shape, montecarlosims.shape)

    for T, tempData, tempDataOrdered in zip(temperatures,data, dataOrdered):
        for [axE, axM], data, label in zip([[ax1,ax2],[ax1b,ax2b]],[tempData, tempDataOrdered], ["Random", "Ordered"]):
            energy = np.abs(data[0]) 
            magnet = np.abs(data[1])
            accept = data[-1] 
            axE.set_title(label)
            axM.set_title(label)
            axE.scatter(montecarlosims, energy, s=3,
                    label=r'$T = %.2f$'%(T),alpha = 0.5)
            axM.scatter(montecarlosims, magnet, s=3,
                    label=r'$T = %.2f$ '%(T),alpha = 0.5)
            ax3.loglog(montecarlosims, accept, 'o', markersize=3, label=r'$T = %.2f$, %s'
                    %(T,label),alpha = 0.5)

    ax1.set_xlabel('NMC')
    ax2.set_xlabel('NMC')
    ax1b.set_xlabel('NMC')
    ax2b.set_xlabel('NMC')
    ax3.set_xlabel('Number of Monte Carlo Cycles')

    ylabels = [ r'$\langle |E| \rangle$',
                r'$\langle |M| \rangle$',
                r'Accepted Configurations']
    #ax3.set_yscale('log')
    for i,ax in enumerate([ax1,ax2,ax3]):
        ax.set_ylabel(ylabels[i])
        ax.legend()
    for i,ax in enumerate([ax1b,ax2b]):
        ax.set_ylabel(ylabels[i])
    #ax1.set_xscale('log') 
    ax3.axis('equal')
    ax3.grid()
    #ax2.set_xscale('log') 

    fig1.tight_layout()
    fig2.tight_layout()
    fig1.savefig('results/equilibrium.pdf')
    fig2.savefig('results/accepted.pdf')
    plt.show()

if __name__ == "__main__":
    main()
