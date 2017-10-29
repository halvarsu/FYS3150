import analyse 
import glob

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

def get_sorted_filenames(folder_name):
    files = [f for f in glob.glob(folder_name + '/*') if f.endswith('.bin')]
    # dirty sorting
    sort = [int(f.split('_N')[-1].split('.')[0]) for f in files]
    return list(np.array(files)[np.argsort(sort)])

def main():
    euler   = get_sorted_filenames('out/stability_analysis_euler')[2:-4]
    verlet  = get_sorted_filenames('out/stability_analysis_verlet')[2:-4]

    fig = plt.figure(figsize = (6,8))
    # loglogplot :
    ax1 = fig.add_subplot(311)
    # euler r-plot
    ax2 = fig.add_subplot(323)
    # euler orbit-plot
    ax3 = fig.add_subplot(325)
    # verlet r-plot
    ax4 = fig.add_subplot(324)
    # verlet orbit-plot
    ax5 = fig.add_subplot(326)

    color = plt.cm.jet(np.linspace(0,1,len(euler)))


    n_values = []
    deviation_values = []

    for i, f in enumerate(euler):
        data = analyse.read_data(f)
        planet = data["pos"][:,1]
        n_values.append(data["steps_per_year"])

        time = data["time"] 
        x, y, z = planet.T
        r = np.sqrt(x**2 + y**2 + z**2)
        deviation = np.sqrt((x[0]-x[-1])**2 + (y[0] - y[-1])**2 + (z[0] - z[-1])**2)
        deviation_values.append(deviation)
    
        ax2.plot(time, r, c=color[i])
        ax3.plot(x,y, c=color[i])
        ax3.axis('equal')
        ax1.scatter(data["steps_per_year"], deviation, c=color[i],marker='v')

    

    ax1.plot(n_values, deviation_values, label='euler')
    n_values = []
    deviation_values = []

    # copy paste :(  
    for i, f in enumerate(verlet):
        data = analyse.read_data(f)
        planet = data["pos"][:,1]
        n_values.append(data["steps_per_year"])

        time = data["time"] 
        x, y, z = planet.T
        r = np.sqrt(x**2 + y**2 + z**2)
        deviation = np.sqrt((x[0]-x[-1])**2 + (y[0] - y[-1])**2 + (z[0] - z[-1])**2)
        deviation_values.append(deviation)
    
        ax4.plot(time, r, c=color[i])
        ax5.plot(x,y, c=color[i])
        ax5.axis('equal')
        ax1.scatter(data["steps_per_year"], deviation, c=color[i],marker='x')


    ax1.plot(n_values, deviation_values, label='verlet')#, '-x')

    ax1.legend()
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel('$N$ [steps/yr]')
    ax1.set_ylabel('$|\Delta \\vec r|/\Delta t$ [AU/yr]')
    for ax in [ax2,ax4]:
        ax.set_xlabel('time [yr]')
        ax.set_ylabel('distance to origin [AU]')
    for ax in [ax3,ax5]:
        ax.set_xlabel('$x$ [AU]')
        ax.set_ylabel('$y$ [AU]')
    ax2.set_title('Euler')
    ax4.set_title('Verlet')

    sm = plt.cm.ScalarMappable(cmap=plt.cm.jet,
            norm=colors.LogNorm(vmin=n_values[0], vmax=n_values[-1]))
    sm.set_array([])
    cb = fig.colorbar(sm, ax=ax1)#, pad=0.2)
    cb.set_label('$N$-values in all plots')

    plt.tight_layout()

    fig.savefig('results/stability.pdf')
    plt.show()
#     fig1.savefig("results/stability_orbits.pdf")
 #    fig2.savefig("results/stability_deviation.pdf")

if __name__ == "__main__":
    main()
