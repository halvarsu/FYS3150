import numpy as np
import matplotlib.pyplot as plt

def plot_eigvecs(omega, rho_max, dim):
    filename = "%.2f_%.2f_%d" %(omega, rho_max, dim)
    eigval = np.loadtxt(file_dir + filename + "val.txt",skiprows=2)
    eigvec = np.loadtxt(file_dir + filename + "vec.txt",skiprows=2)

    sort = np.argsort(eigval)

    fig, [ax1,ax2] = plt.subplots(2)
    eigval = eigval[sort]
    eigvec = eigvec[:,sort]
    print 'eigenvalues:', eigval[:4]
    r = np.loadtxt(file_dir + filename+"rho.txt",skiprows=2)

    [plt.plot(r,eigvec[:,i]**2) for i in range(3)]
    plt.title('omega_r = %.2f, rho_N = %.2f, N = %d' %(omega,rho_max,dim))

    cutoff = 1e-8
    max_point = np.argmax(eigvec[:,2])
    print r[max_point]
    i = np.argsort(eigvec[max_point:,2]**2 < cutoff)[:5]
    print 'cutoff_points:', r[i+max_point]
    plt.show()


def plot_interacting(file_dir ,cmap = plt.cm.jet):
    N_vals = np.array(np.linspace(50,1200,14),dtype=int)
    import glob
    files =  glob.glob(file_dir + "*")
    omega_vals = [0.01,0.5,1,5]
    omega_files = [glob.glob(file_dir + "omega_%.2f*"%omega) for omega in omega_vals]
    fig,axes = plt.subplots(2,2)
    axes_flat = [ax for row in axes for ax in row]
    print(axes_flat)
    ev_i = 1
    cutoff = 1e-12
    for omega,files, ax in zip(omega_vals, omega_files,axes_flat):
        # pick out the part of the file name indicating type
        markers = [f.split('.')[-2][-3:] for f in files]
        rho_file = files[markers.index('rho')]
        vec_file = files[markers.index('vec')]
        val_file = files[markers.index('val')]
        val = np.loadtxt(val_file, skiprows = 2)
        sort = np.argsort(val)
        vec = np.loadtxt(vec_file, skiprows = 2)[:,sort]
        rho = np.loadtxt(rho_file, skiprows = 2)
        ax.plot(rho, vec[:,0:3])
        #ax2.scatter(omega, val[ev_i])

        # find first point after maxima where third wave function < cutoff
        max_point = np.argmax(vec[:,2]**2)
        print rho[max_point], max_point
        mask = vec[max_point:,2]**2 < cutoff
        try:
            cutoff_rho = rho[max_point:][mask][0]
            print "Wave function 3 is < %g at rho=%.2f for omega=%.2f" %(cutoff,cutoff_rho,omega)
        except IndexError:
            print "Warning, wave function does not decrease to suitable values"
            print "rhoMax=%f might be too small for omega =%.2f" %(rho[-1],omega)
    plt.show()

    return

    fig, axes = plt.subplots(2)
    N = 200
    n = len(rho_vals)
    for i, rho_max in enumerate(rho_vals):
        color = cmap(float(i)/(n-1)) 
        plot_noninteracting(rho_max, N, file_dir, axes=axes, 
                color = rho_max)

    for N in N_vals:
        plot_noninteracting(axes)
    ax1,ax2 = axes
    [ax.grid('on') for ax in [ax1,ax2]]

    ax1.legend()
    ax2.axhline(11.)
    ax1.set_xlabel('rho ')
    ax1.set_ylabel('u**2')
    ax2.set_xlabel('rho max')
    ax2.set_ylabel('E_1')
    ax1.set_title('optimal rho_N = %.2f for N = %d' %(rho_opt,dim))
    plt.show()


if __name__ == "__main__":
    version = "Debug"
    method = "jacobi"
    case = "interacting"
    file_base = "build-proj2-Desktop_Qt_5_9_1_GCC_64bit-{}/{}/{}/" .format(version, case, method)
    plot_interacting(file_base)
