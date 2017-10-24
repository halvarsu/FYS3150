import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def get_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', default='out/example.txt')
    parser.add_argument('--fixed_sun', action='store_true')
    parser.add_argument('-dim', '--dimensions',type=int,help='plot dimension', default=2, choices=[2,3])
    parser.add_argument('-s', '--plot_step', help='plot every nth data point',default=1)
    parser.add_argument('-p', '--phase', help='plot phase precession of body 2',
            action = 'store_true')
    return parser.parse_args()

def read_data(args):
    # Finds number of planets from first line, and reads the rest of the
    # data. 
    filename = args.filename
    print("Reading %s" %filename)
    with open(filename, 'r') as infile:
        n_planets = int(infile.readline())

    pos = np.loadtxt(filename, skiprows=1, dtype=float)

    planets = np.zeros((pos.shape[0]//n_planets, n_planets, pos.shape[1]))
    for i in range(n_planets):
        planets[:,i] = pos[i::n_planets]
    return n_planets, planets

def plot(planets, args):
    print(planets.shape)
    n_planets = planets.shape[1]
    fig = plt.figure()
    n = args.plot_step

    if args.dimensions == 3:
        ax = fig.add_subplot(111, projection='3d')
        for i in range(n_planets):
            ax.plot(planets[::n,i,0], planets[::n,i,1], zs=planets[::n,i,2])
        m = np.max(np.abs(planets))
        boxlen = [-m,m]
        plt.scatter(planets[0,0,0],planets[0,0,1],zs=planets[0,0,2], c='y')
        ax.auto_scale_xyz(boxlen,boxlen,boxlen)
    else:
        ax = fig.add_subplot(111)
        for i in range(n_planets):
            ax.plot(planets[::n,i,0], planets[::n,i,1])
        plt.scatter(planets[0,0,0],planets[0,0,1], c='y')
        ax.axis('equal')
        ax.grid()
    plt.show()
    if args.phase:
        plot_phase_precession(planets[:,1], args)




def plot_phase_precession(planet,args):
    pass

def main():
    args = get_args()
    n_planets, data = read_data(args)
    plot(data,args)


if __name__ == "__main__":
    main()


