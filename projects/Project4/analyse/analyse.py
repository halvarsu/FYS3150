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
    montecarlosims = np.logspace(1,6,1000)
    data = np.zeros((6,len(montecarlosims)))
    width = shutil.get_terminal_size((80,20)).columns

    print_method = 'sine'
    for i,NMC in enumerate(montecarlosims):
        NMC = int(NMC)
        if print_method == 'sine':
            sine_print(str(NMC),i,width)
        else:
            linear_print(str(NMC), i, width, len(montecarlosims))
        #print("="*10 + str(NMC) + "="*10)
        # proc = subprocess.Popen(['build/Project4', str(NMC)], 
        #         stdout=subprocess.PIPE,shell=True)
        # (out,err) = proc.communicate()
        out = subprocess.check_output("build/Project4 %d" %NMC, shell = True)
        out = list(map(float, out.split()))
        data[:,i] = out
        # avgE, avgM, avgEsquared, avgMsquared, specific_heat, susceptibility = 
        #print(out)

    fig, [ax1,ax2] = plt.subplots(2,sharex=True)

    ax1.scatter(montecarlosims,data[4],s=5)
    ax2.scatter(montecarlosims,data[5],s=5)
    ax1.axhline(0.128329327, linestyle='--', color = 'k', label='Analytical')
    ax2.axhline(15.97321, linestyle='--',color = 'k',label='Analytical')
    ax1.legend()
    ax2.legend()

    ax1.set_xscale('log')
    ax1.set_ylabel(r'$C_V$')

    ax2.set_xlabel('Number of Monte Carlo Cycles')
    ax2.set_ylabel(r'$\chi$')
    ax2.set_xscale('log')
    plt.savefig('results/compareAnalytical.pdf')
    plt.show()


if __name__ == "__main__":
    main()
