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
    parser.add_argument('-DP', '--dont_plot', help='plot orbit', action = 'store_false')
    parser.add_argument('-e','--energies', help='plot energies of system',action='store_true')
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
        data["n_planets"] = int(infile.readline())
        data["fixed_sun"] = int(infile.readline())
        data["relativistic"] = int(infile.readline())
        _, _, _ = infile.readline().split() # headers for energies, not necessary
        # in this context

    if args.energies:
        data["energies"] = np.loadtxt(info_filename, skiprows=4, dtype=float)

    print("Reading pos from %s" %data_filename)
    pos = np.fromfile(data_filename)
    pos = pos.reshape(-1, data["n_planets"], 3)
    data["pos"] = pos

    #planets = np.zeros((pos.shape[0]//n_planets, n_planets, pos.shape[1]))
    #for i in range(n_planets):
        #planets[:,i] = pos[i::n_planets]
    print("\r    Done reading...     ")
    print(pos)
    return data

def plot(data, args):
    print(data['pos'].shape)
    n_planets = data["n_planets"]
    planets = data["pos"]
    fig = plt.figure()
    n_step = args.plot_step

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
    plt.show()
    if args.precession:
        plot_peri_precession(planets[:,1], args)




def plot_peri_precession(planet,args):
    from scipy.optimize import minimize
    from scipy.interpolate import interp1d
    print(planet.shape)
    # Assuming two-dimensional
    x,y,z = planet.T
    r = np.sqrt(x**2 + y**2 + z**2)
    maxima = np.r_[False, r[1:] < r[:-1]] & np.r_[r[:-1] < r[1:], False]
    dr = np.diff(r)
    dr_min = np.r_[False, dr[1:] < dr[:-1]] & np.r_[dr[:-1] < dr[1:], False]
    dr_max = np.r_[False, dr[1:] > dr[:-1]] & np.r_[dr[:-1] > dr[1:], False]

    r_minima = []
    theta_minima = []
    for a,b in zip(dr_min[:-1][dr_min], dr[:-1][dr_max]):
        r_sub = r[a:b]
        theta_sub = theta[a:b]
        r_func = interp1d(theta_sub,r_sub)
        res = minimize(r_func, (theta_sub[int(theta_sub.size/2)]))
        theta_minima.append(res.x)
        r_minima.append(res.fun)
        
    # exclude endpoints
    theta = np.arctan2(y,x)
    #plt.plot(r[::args.plot_step],theta)
    fix,[ax1,ax2] = plt.subplots(2)
    ax1.plot(theta[maxima])
    ax2.plot(r)
    print(np.sum(maxima))
    ind = np.arange(len(r))
    #ax2.scatter(x[maxima],y[maxima])
    ax2.scatter(ind[maxima],r[maxima])
    #ax2.axis('equal')
    plt.show()

def main():
    args = get_args()
    data = read_data(args)
    plot(data,args)


if __name__ == "__main__":
    main()


