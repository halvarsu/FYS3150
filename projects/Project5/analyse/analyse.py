import argparse
import numpy as np
import matplotlib


def main(args):
    import matplotlib.pyplot as plt
    """Either runs all parts or just one"""
    part1(args)

def part1(args):
    import numpy as np
    import matplotlib.pyplot as plt
    import glob

    if args.temps == "all":
        all_folders = glob.glob('out/*')
        initial_temps = [string.split('/')[-2].split('_')[-1] for string in all_folders]

    elif args.temps == "low":
        initial_temps = list(range(25,1425,25))
        all_folders = ["out/T_{}".format(T) for T in initial_temps]

    # all_lengths =  [file_len(fname) for fname in all_folders]
    all_data = []
    # all_data = np.zeros(( len(all_folders),6,file_length))

    for i, folder in enumerate(all_folders):
        filename = (folder+'/statistics.txt')
        a = np.loadtxt(filename)
        all_data.append(a.T)

    figsize = (5,3.5)
    fig1, ax1= plt.subplots(1,figsize = figsize)
    fig2, ax2 = plt.subplots(1,figsize = figsize)
    fig3, [ax3a, ax3b] = plt.subplots(1,2, figsize = figsize)
    fig4, ax4 = plt.subplots(1,figsize = figsize)

    sort = np.argsort(initial_temps)
    T_ratios = []
    running_ratio = np.zeros(all_data[0][1].size)
    energy_deviations = []
    # for a,T0 in zip(all_data, initial_temps):
    for num,i in enumerate(sort):
        T0 = initial_temps[i]
        _, time, temperature, kinetic, potential, diffusion = all_data[i]
        N = time.size
        # To SI units
        time        *= 1.00224e-13 
        temperature *= 119.735 
        diffusion   *= 0.998e-7 
        
        final_temp, variance = np.polyfit(time[-int(N/4):],
                temperature[-int(N/4):], 0,cov=True)
        variance = variance[0,0]
        final_temp = final_temp[0]

        final_temp = np.mean(temperature[-int(N/16):])
        #variance = sem(temperature[-int(N/16):])
        variance = np.var(temperature[-int(N/16):])

        T_ratios.append(final_temp/T0)
        print("Final/Initial", T_ratios[-1])
        color = plt.cm.viridis(num/len(sort))

        running_ratio += temperature/T0
        if num % 4 == 0:
            ax1.plot(time[:int(N/8)], temperature[:int(N/8)], c=color) 
            #ax4.plot(time,temperature/T0 ,c=color)
        # ax2.errorbar(final_temp, diffusion[-1], xerr=np.sqrt(variance),fmt='o')
        ax2.plot(final_temp, diffusion[-1] ,'o',c=color)
        Etot = kinetic + potential
        Emean = np.mean(Etot)
        ax3a.plot(time, (Etot-Emean)/Emean,c=color)
        ax3b.plot(final_temp, Etot[-1] ,'o',c=color)

    temperatures = (np.array(all_data)[:,2].T / np.array(initial_temps)).T
    total_energies = np.sum(np.array(all_data)[:,3:5], axis = 1)
    mean_energies = np.mean(total_energies, axis = 1)
    print(total_energies.shape)
    deviation = np.sqrt(np.var((np.abs(total_energies.T - mean_energies)/mean_energies)))
    print(deviation)

    mean = np.mean(temperatures, axis=0)
    err = np.sqrt(np.var(temperatures, axis=0))
    ax4.plot(time, mean,'k-')
    ax4.fill_between(time, mean-err, mean+err, alpha = 0.5, 
            linestyle = 'dashed', antialiased=True)
    # ax4.errorbar(time, np.mean(temperatures, axis=0), np.sqrt(np.var(temperatures,axis=0)))

    print("Ratios")
    print("Mean:", np.mean(T_ratios) ,"+-", np.sqrt(np.var(T_ratios)))
    sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis,
            norm=plt.Normalize(vmin=np.min(initial_temps),
                               vmax=np.max(initial_temps)))
    sm._A = []
    plt.colorbar(sm, ax=ax1, label='Initial temperature [K]')


    for ax in [ax1,ax2,ax3a, ax3b, ax4]:
        ax.grid() 
        #ax.legend() if args.temps == "low" else None
    ax1.set_xlabel('$t$ [s]')
    ax1.set_ylabel('Temperature, [ K ] ')
    ax2.set_xlabel('$T$ [K] ')
    ax2.set_ylabel('$D$ [m$^2$/s]')
    ax3a.set_xlabel('$t$ [s]')
    ax3a.set_ylabel('$(E_T - \\langle E\\rangle)/\\langle E\\rangle $ ')
    ax3b.set_xlabel('$T$ [K]')
    ax3b.set_ylabel('Total energy $E$ [$\\varepsilon$]')
    ax4.set_xlabel('$t$ [s] ')
    ax4.set_ylabel('$\\langle T/T_i \\rangle$ [K]')
    #ax2.set_xlabel('Time [s] ')
    #ax2.set_ylabel('Diffusion Constant')

    outnames = 'kinetic diffusion total meantemp'.split()
    for fig, name in zip([fig1,fig2,fig3,fig4], outnames):
        fig.tight_layout()
        fig.savefig('results/{}_{}.pdf'.format(name, args.temps))
    plt.show()


def get_args():
    parser = argparse.ArgumentParser()

    # parser.add_argument('-p','--part', type=int,default=0, 
    #                     choices = [0,1,2,3])
    parser.add_argument('-T','--temps', default='all',
                        choices = ['all','low'])
    parser.add_argument('--headless', help='Dont plot, only save', action = 'store_true')
    return parser.parse_args()

if __name__=='__main__':
    args = get_args()
    if args.headless:
        matplotlib.use('Agg')
    main(args)
