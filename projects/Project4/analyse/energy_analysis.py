import numpy as np
import matplotlib.pyplot as plt
from tools import add_letter_label

"""Simple script for generating histograms of the code generated by the Git
branch save_energies."""

energiesT1 = np.loadtxt('out/energiesT1.dat')
energiesT1Ordered = np.loadtxt('out/energiesT1Ordered.dat')
energiesT2_4 = np.loadtxt('out/energiesT2_4.dat')
energiesT2_4Ordered = np.loadtxt('out/energiesT2_4Ordered.dat')


binsT1 = np.linspace(-800,-740,16)
binsT2 = np.linspace(-700,-300,101)
fig1,[[ax1a,ax1b],[ax2a,ax2b]] = plt.subplots(2,2,figsize=[4,4])
fig2,[ax3,ax4 ]= plt.subplots(2,figsize=[4,4])

ax1a.hist(energiesT1, binsT1,alpha=0.5)
ax1b.hist(energiesT2_4, binsT2,alpha=0.5)
ax2a.hist(energiesT1Ordered, binsT1,alpha=0.5)
ax2b.hist(energiesT2_4Ordered, binsT2,alpha=0.5)

NMC = np.arange(energiesT1.size)
stop = 1000

runLength = NMC + 1
energiesCumsum1 = np.cumsum(energiesT1)/runLength
energiesCumsum2_4 = np.cumsum(energiesT2_4)/runLength

eC1Ord = np.cumsum(energiesT1Ordered)/runLength
eC2Ord = np.cumsum(energiesT2_4Ordered)/runLength

ax3.plot(NMC[:stop], energiesT1Ordered[:stop],'g--',alpha =0.5,
        label='Random')
ax3.plot(NMC[:stop], (energiesCumsum1)[:stop],'g-',lw=5,
        label='Cumulative Random')
ax3.plot(NMC[:stop], energiesT1[:stop],'r--',alpha =0.5,
        label='Ordered')
ax3.plot(NMC[:stop], (eC1Ord)[:stop],'r-',lw=5,
        label='Cumulative Ordered')
ax4.plot(NMC[:stop], energiesT2_4[:stop],'g--',alpha =0.5,
        label='Random')
ax4.plot(NMC[:stop], (energiesCumsum2_4)[:stop],'g-',lw=5,
        label='Cumulative Random')
ax4.plot(NMC[:stop], energiesT2_4Ordered[:stop],'r--',alpha =0.5,
        label='Ordered')
ax4.plot(NMC[:stop], (eC2Ord)[:stop],'r-', lw=5,
        label='Cumulative Ordered')

# totalT1 = float(energiesT1.size)
# totalT2_4 = float(energiesT2_4.size)
# print(totalT1)
# ax1.hist(energiesT1/totalT1, binsT1,alpha=0.5)
# ax2.hist(energiesT2_4/totalT2_4, binsT2,alpha=0.5)

for i,ax in enumerate([ax1a,ax1b,ax2a,ax2b]):
    ax.set_xlabel('Energy bins [J]')
    ax.set_ylabel('Number of energies')
    add_letter_label(ax, i)
    ax.legend()
ax3.set_title('$T = 1$')
ax4.set_title('$T = 2.4$')

fig1.tight_layout()
fig2.tight_layout()
fig1.savefig('results/energiesBinsBoth.pdf')
fig2.savefig('results/energiesGraphs.pdf')
plt.show()
