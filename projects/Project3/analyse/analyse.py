import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def get_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', default='out/example.bin')
    parser.add_argument('--fixed_sun', action='store_true')
    parser.add_argument('-dim', '--dimensions',type=int,help='plot dimension', default=2, choices=[2,3])
    parser.add_argument('-ps', '--plot_step', help='plot every nth data point',
            type=int,default=1)
    parser.add_argument('-p', '--precession', help='plot perihelion precession of body 2',
            action = 'store_true')
    parser.add_argument('-e', '--energies', help='plot energies of system',
            action = 'store_true')
    #parser.add_argument('-e','--energies', help='plot energies of system',action='store_true')
    parser.add_argument('-DP','--disable_plot', help='dont plot main orbit',action='store_true')
    return parser.parse_args()

def read_data(args):
    # Finds number of planets from first line, and reads the rest of the
    # data. 
    data_filename = args.filename
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
        _, _, _ = infile.readline().split() # headers for energies, not necessary
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

    if not args.disable_plot:
        fig = plt.figure()
        if args.dimensions == 3:
            ax = fig.add_subplot(111, projection='3d')
            for i in range(n_planets):
                ax.plot(planets[::n_step,i,0], planets[::n_step,i,1],
                        zs=planets[::n_step,i,2])
            m = np.max(np.abs(planets))
            boxlen = [-m,m]
            plt.scatter(planets[0,0,0],planets[0,0,1],zs=planets[0,0,2], c='y')
            ax.auto_scale_xyz(boxlen,boxlen,boxlen)
        else:
            ax = fig.add_subplot(111)
            for i in range(n_planets):
                ax.plot(planets[::n_step,i,0], planets[::n_step,i,1])
            plt.scatter(planets[0,0,0],planets[0,0,1], c='y')
            ax.axis('equal')
            ax.grid()
    if args.precession:
        fig2, axes2 = plot_peri_precession(data, args)
    # if args.energies:
    #     plot_energies(data, args)
    plt.show()


def plot_energies(data, args):
    energies = data["energies"]
    return


def plot_peri_precession(data,args):
    # Assuming two-dimensional
    planet = data['pos'][:,1]
    time = data["time"]

    x,y,z = planet.T
    r = np.sqrt(x**2 + y**2 + z**2)
    minima = np.r_[False, r[1:] < r[:-1]] & np.r_[r[:-1] < r[1:], False]
    theta = np.arctan2(y,x)
    #plt.plot(r[::args.plot_step],theta)
    fig, axes = plt.subplots(1)
    ax1 = axes
    time_minima = time[minima]
    theta_minima  = theta[minima]
    arcsec_minima = (theta_minima) * 180 / np.pi * 3600
    # orbit_num = np.arange(arcsec_minima.size)
    p, cov= np.polyfit(time_minima, arcsec_minima, 1, cov = True)
    print(cov)
    arcsec_fitted = time_minima*p[0] + p[1]
    angle0 = arcsec_fitted[0]
    ax1.plot(time_minima, arcsec_minima - angle0)
    ax1.plot(time_minima, arcsec_fitted - angle0)
    print("dtheta: %f" %(arcsec_fitted[-1] - angle0))
    ax1.set_xlabel('Time [yr]')
    ax1.set_ylabel('Perihelion angle [arcsec]')
    ax1.legend(['Measured','Fitted'])
    return fig, axes

def main():
    args = get_args()
    data = read_data(args)
    plot(data,args)


if __name__ == "__main__":
    main()


