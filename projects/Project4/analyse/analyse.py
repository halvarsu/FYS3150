import subprocess
import numpy as np
import matplotlib.pyplot as plt
import shutil 


def main():
    compare_analytical()

def sine_print(text, i, width=60, freq=10):
    print("{1: ^{0}}".format(width,
        "*{1:=^{0}}*".format(int((width-len(text)-1)/2*(1+np.sin(i/10.))+len(text)),text)))

def linear_print(text, i, width, end=100):
    print("{1: ^{0}}".format(width,
        "*{1:=^{0}}*".format(int((width-len(text)-2)*i/end+len(text)),text)))


def compare_analytical(visuals = 'sin'):
    montecarlosims = np.logspace(1,6,200)
    data = np.zeros((6,len(montecarlosims)))
    # width = shutil.get_terminal_size((80,20)).columns
    width = 40

    print_method = 'sine'
    T = 1
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
    fig1, [ax1,ax2,ax3,ax4] = plt.subplots(4,sharex=True)
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


if __name__ == "__main__":
    main()
