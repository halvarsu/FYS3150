import argparse
import numpy as np
import matplotlib.pyplot as plt

def main(args):
    """Either runs all parts or just one"""
    parts = {1:part1, 2:part2}
    if args.part == 0:
        part1(args)
        part2(args)
    else:
        parts[args.part](args)

def part1(args):
    return

def part2(args):
    print("Part 2")
    import numpy as np
    import matplotlib.pyplot as plt
    import glob
    file_length = 9999
    if args.temps == "all":
        all_folders = glob.glob('out/*')
        temps = [string.split('/')[-2].split('_')[-1] for string in all_folders]
    elif args.temps == "low":
        temps = [15,40,45,60,90,150,200]
        all_folders = ["out/T_{}".format(T) for T in temps]

    all_data = np.zeros(( len(all_folders),6,file_length))

    for i, folder in enumerate(all_folders):
        file = (folder+'/statistics.txt')
        a = np.loadtxt(file)
        all_data[i] = a.T

    fig, [ax1,ax2] = plt.subplots(2)

    for a,T0 in zip(all_data, temps):
        _, time, temperature, kinetic, potential, diffusion = a
        time        = 1.00224e-13 * time
        temperature = 119.735 * temperature
        diffusion = 1 * diffusion
        print(diffusion[-1], time[-1])
        ax1.plot(time, temperature, label = "$T_0 = {}$".format(T0))
        N = time.size
        #ax2.plot(time, diffusion*time)
        ax2.scatter(temperature[-1], diffusion[-1])


    for ax in [ax1,ax2]:
        ax.grid() 
        ax.legend() if args.temps == "low" else None
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Temperature [K]')
    #ax2.set_xlabel('Time [s] ')
    #ax2.set_ylabel('Diffusion Constant')
    ax2.set_xlabel('Temperature [K] ')
    ax2.set_ylabel('MSD')
    plt.tight_layout()
    plt.savefig('results/diffusion_{}.png'.format(args.temps))
    plt.show()


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-p','--part', type=int,default=0, 
                        choices = [0,1,2,3])
    parser.add_argument('-T','--temps', default='all',
                        choices = ['all','low'])
    return parser.parse_args()

if __name__=='__main__':
    args = get_args()
    main(args)
