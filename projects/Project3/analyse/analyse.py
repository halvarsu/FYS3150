import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tools
import glob


def get_args():
    import argparse

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--filename', default='out/example.bin')
    parser.add_argument('-F', '--folder', default='', help = 'Only useful for stability analysis, when several simulations are compared ')
    parser.add_argument('-o', '--outfile', default='')
    parser.add_argument('-s', '--savefig',action='store_true')
    parser.add_argument('-l', '--set_manual_legend',action='store_true')
    parser.add_argument('-p', '--plot_file',default='')
    parser.add_argument('-dim', '--dimensions',type=int,help='plot dimension', default=2, choices=[2,3])
    parser.add_argument('-n', '--plot_step', help='plot every nth data point',
            type=int,default=1)
    parser.add_argument('--precession', help='plot perihelion precession of body 2',
            action = 'store_true')
    parser.add_argument('--energies', help='plot energies of system',
            action = 'store_true')
    parser.add_argument('--stability_analysis', help='plot a folder with simulations with changing dt',
            action = 'store_true')
    parser.add_argument('--no_orbit', help='dont plot orbit',action='store_true')
    parser.add_argument('-v','--verbose', help='1 = print all, 0 = no print',type=int, choices = [0,1], default = 1)
    parser.add_argument('--figsize', nargs=2,type=float, default=(6,4))
    return parser.parse_args()

def read_data(data_filename, args):
    # Finds number of planets from first line, and reads the rest of the
    # data. 
    temp = data_filename.split('.')[:-1]
    temp.append("info.txt")
    info_filename = ".".join(temp)
    data = {}

    print("Reading info from %s" %info_filename)
    with open(info_filename, 'r') as infile:
        data["n_years"] = int(infile.readline())
        data["steps_per_year"] = int(infile.readline())
        data["fixed_sun"] = int(infile.readline())
        data["relativistic"] = int(infile.readline())
        data["n_planets"] = int(infile.readline())
        _,_, _, _ = infile.readline().split() # headers for energies, not necessary
        # in this context

    data["energies"] = np.loadtxt(info_filename, skiprows=6, dtype=float).T

    print("Reading pos from %s" %data_filename)
    pos = np.fromfile(data_filename)
    pos = pos.reshape(-1, data["n_planets"], 3)
    data["pos"] = pos
    data["time"] = np.linspace(0,data["n_years"],pos.shape[0])
    print("\r    Done reading...     ")
    return data

def plot(data, args):
    n_planets = data["n_planets"]
    planets = data["pos"]
    n_step = args.plot_step

    distances = np.sqrt(planets[:,:,0]**2 +planets[:,:,1]**2 + planets[:,:,2]**2)
    avg_dist = np.average(distances, axis = 0)
    sort = np.argsort(avg_dist)
    planets = planets[:,sort]
    distances = distances[:,sort]
    avg_dist = avg_dist[sort]


    if not args.no_orbit:
        fig = plt.figure()
        if args.dimensions == 3:
            ax = fig.add_subplot(111, projection='3d')
            for i in range(n_planets):
                ax.plot(planets[::n_step,i,0], planets[::n_step,i,1],
                        zs=planets[::n_step,i,2])
            m = np.max(np.abs(planets))
            boxlen = [-m,m]
            plt.scatter(planets[0,0,0],planets[0,0,1],planets[0,0,2])
            ax.set_xlabel("X[AU]")
            ax.set_ylabel("Y[AU]")
            ax.set_zlabel("Z[AU]")
            ax.auto_scale_xyz(boxlen,boxlen,boxlen)
        else:
            ax = fig.add_subplot(111)
            for i in range(n_planets):
                ax.plot(planets[::n_step,i,0], planets[::n_step,i,1])
            plt.scatter(planets[0,0,0],planets[0,0,1], c=(0.7, 0.7,0))

            ax.axis('equal')
            ax.set_xlabel('x [AU]')
            ax.set_ylabel('y [AU]')
            ax.set_title('Steps per year = %d' %data["steps_per_year"])
            ax.grid()
    if args.set_manual_legend:
        print("Manual legends enabled. Write legend for planets:")
        legend = []
        for r in avg_dist:
            legend.append(raw_input('avg r = %.2f AU: ' %np.average(r)))
        plt.legend( legend)
    if args.savefig:
        if args.plot_file:
            outfile = "results/" + args.plot_file
        else:
            outfile =  raw_input('Write filename (or leave blank) (default folder=results/):\n') 
            if outfile:
                outfile = "results/" + outfile
            else:
                base_name = "results/figure%dD_{}.pdf" % args.dimensions
                prev_files = glob.glob(base_name.format("*"))
                outfile = base_name.format(len(prev_files))

        print('saving to %s' %outfile )
        fig.savefig(outfile)


def plot_orbit_stability(args):
    filenames = [f for f in glob.glob(args.folder + '/*') if f.endswith('.bin')]
     
    # dirty sorting
    temp = map(lambda x : int(x.split('_N')[-1].split('.')[0]), filenames)
    filenames = list(np.array(filenames)[np.argsort(temp)])

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(211)
    ax2 = fig1.add_subplot(212)
    fig2 = plt.figure()
    ax3 = fig2.add_subplot(111)
    color = plt.cm.jet(np.linspace(0,1,len(filenames)))

    for i, f in enumerate(filenames):
        data = read_data(f, args)
        planet = data["pos"][:,1]

        time = data["time"] 
        x, y, z = planet.T
        r = np.sqrt(x**2 + y**2 + z**2)
        deviation = np.sqrt((x[0]-x[-1])**2 + (y[0] - y[-1])**2 + (z[0] - z[-1])**2)
        ax1.plot(time, r, c=color[i])
        ax2.plot(x,y, c=color[i])
        ax2.axis('equal')
        ax3.scatter(data["steps_per_year"], deviation, c=color[i])
    ax3.set_xscale('log')
    ax3.set_yscale('log')
    ax1.set_xlabel('time [yr]')
    ax1.set_ylabel('distance to origin [AU]')
    ax2.set_xlabel('$y$ [AU]')
    ax2.set_ylabel('$y$ [AU]')
    ax3.set_xlabel('$N$ [steps/yr]')
    ax3.set_ylabel('$\Delta r/\Delta t$ [AU/yr]')

    fig1.savefig("results/stability_orbits.pdf")
    fig2.savefig("results/stability_deviation.pdf")

def plot_energies(data, args):
    plt.figure()
    kinetic, potential, total, angular_momentum = data["energies"][:,1:]
    time = data["time"]
    plt.xlabel("Time")
    plt.ylabel("Kinetic+potential energy [$AJ$]")
    plt.plot(time, total)
    plt.plot(time, kinetic)
    plt.plot(time, potential)



def plot_peri_precession(data,args):
    # Assuming two-dimensional
    planet = data['pos'][:,1]
    time = data["time"]

    x,y,z = planet.T
    r = np.sqrt(x**2 + y**2 + z**2)
    minima = np.r_[False, r[1:] < r[:-1]] & np.r_[r[:-1] < r[1:], False]
    if np.sum(minima)== 0:
        print("Found no perihelion... Cancelling analysis")
        return
    theta = np.arctan2(y,x)
    #plt.plot(r[::args.plot_step],theta)
    fig, axes = plt.subplots(1)
    ax1 = axes
    time_minima = time[minima]
    theta_minima  = theta[minima]
    arcsec_minima = (theta_minima) * 180 / np.pi * 3600
    print(time_minima.shape, theta_minima.shape)
    # orbit_num = np.arange(arcsec_minima.size)
    p, cov= np.polyfit(time_minima, arcsec_minima, 1, cov = True)
    print(cov)
    arcsec_fitted = time_minima*p[0] + p[1]
    angle0 = arcsec_fitted[0]
    ax1.plot(time_minima, arcsec_minima - angle0)
    ax1.plot(time_minima, arcsec_fitted - angle0)
    delta_angle = arcsec_fitted[-1] - angle0
    dt = time[-1] - time[0] 
    insecurity = dt*cov[0,0]
    print(delta_angle)
    print(insecurity)
    ax1.set_xlabel('Time [yr]')
    ax1.set_ylabel('Perihelion angle [arcsec]')
    ax1.legend(['Measured','Fitted'])
    ax1.set_title('$\\Delta \\theta = %.1f \\pm %.2f [arcsec]$ ' %(delta_angle, insecurity))

    fig.savefig("results/peri_precession.pdf")
    return fig, axes

def main(args):
    if args.verbose == 0:
        tools.blockPrint()

    # stability > normal plot, precession, energies
    if args.stability_analysis:
        plot_orbit_stability(args)
    else:
        data = read_data(args.filename, args)
        if not args.no_orbit:
            plot(data,args)
        if args.precession:
            plot_peri_precession(data, args)
        if args.energies:
            plot_energies(data, args)
    plt.show()



if __name__ == "__main__":
    args = get_args()
    main(args)


