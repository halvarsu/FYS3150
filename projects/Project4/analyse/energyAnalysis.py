
import numpy as np
import matplotlib.pyplot as plt
from tools import add_letter_label
energiesT1 = np.loadtxt('out/energiesT1.dat')
# energiesT1Ord = np.loadtxt('out/energiesT1Ordered.dat')
energiesT2_4 = np.loadtxt('out/energiesT2_4.dat')
# energiesT2_4Ord = np.loadtxt('out/energiesT2_4Ordered.dat')


binsT1 = np.linspace(-800,-740,16)
binsT2 = np.linspace(-700,-300,101)
fig1,[ax1,ax2] = plt.subplots(2)
ax1.hist(energiesT1, binsT1,alpha=0.5)
# ax1.hist(energiesT1Ordered, binsT1,alpha=0.5)
ax2.hist(energiesT2_4, binsT2,alpha=0.5)
# ax2.hist(energiesT2_4Ordered, binsT2,alpha=0.5)

# totalT1 = float(energiesT1.size)
# totalT2_4 = float(energiesT2_4.size)
# print(totalT1)
# ax1.hist(energiesT1/totalT1, binsT1,alpha=0.5)
# ax2.hist(energiesT2_4/totalT2_4, binsT2,alpha=0.5)

for i,ax in enumerate([ax1,ax2]):
    ax.set_xlabel('Energy bins [J]')
    ax.set_ylabel('Number of energies')
    add_letter_label(ax, i)

plt.tight_layout()
plt.savefig('results/energiesBinsBoth.pdf')
plt.show()
