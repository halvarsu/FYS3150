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
    print( 'eigenvalues:', eigval[:4])
    r = np.loadtxt(file_dir + filename+"rho.txt",skiprows=2)

    [plt.plot(r,eigvec[:,i]**2) for i in range(3)]
    plt.title('omega_r = %.2f, rho_N = %.2f, N = %d' %(omega,rho_max,dim))

    cutoff = 1e-8
    max_point = np.argmax(eigvec[:,2])
    print (r[max_point])
    i = np.argsort(eigvec[max_point:,2]**2 < cutoff)[:5]
    print ('cutoff_points:', r[i+max_point])
    plt.show()

def get_omega_files(omega, dim, file_dir):
    import glob
    files = glob.glob(file_dir + "omega_%.2f*"%omega)
    return list(filter(lambda x:bool(x.find('N_%d'%dim)+1), files))

def plot_interacting(args, file_dir ,cmap = plt.cm.jet):
    import glob
    files =  glob.glob(file_dir + "*")
    omega_vals = [0.01,0.25,0.5,1,5]
    dim = args.dim
    omega_files = [get_omega_files(omega,dim,file_dir) for omega in omega_vals]

    #omega_files = 
    fig,ax = plt.subplots(figsize=args.figsize)
    ev_i = 0
    cutoff = 1e-12
    x_max = 0
    y_max = 0
    for omega,files in zip(omega_vals, omega_files):
        print("{:=^80.2f}".format(omega))
        # pick out the part of the file name indicating type
        markers = [f.split('.')[-2][-3:] for f in files]
        rho_file = files[markers.index('rho')]
        vec_file = files[markers.index('vec')]
        val_file = files[markers.index('val')]
        print(rho_file, vec_file, val_file)
        val = np.loadtxt(val_file, skiprows = 2)
        sort = np.argsort(val)
        vec = np.loadtxt(vec_file, skiprows = 2)[:,sort]
        rho = np.loadtxt(rho_file, skiprows = 2)
        rho_normed = rho/np.max(rho)

        step = (rho[-1]-rho[0])/rho.size
        # plot normalized
        ax.plot(rho, vec[:,0]**2/step,label='$\\omega = %.2f$' %omega)

        # find first point after maxima where third wave function < cutoff
        max_point = np.argmax(vec[:,ev_i]**2)
        mask = vec[max_point:,ev_i]**2 < cutoff
        print("eigenvalues: $"+"$ & $".join(map("{:.3f}".format, val[sort][:3]))+"$")
        print("normalized?", np.sum(vec[:,ev_i]**2))
        try:
            cutoff_rho = rho[max_point:][mask][0]
            print( "Wave function 3 is < %g at rho=%.2f for omega=%.2f" %(cutoff,cutoff_rho,omega))
        except IndexError:
            print( "Warning, wave function does not decrease to suitable values")
            print( "rhoMax=%f might be too small for omega =%.2f" %(rho[-1],omega))
    plt.axis([0,6, 0, 2])
    plt.xlabel('$\\rho$')
    plt.ylabel('$|\\psi(\\rho)|^2$')
    plt.legend()
    plt.savefig('results/waveFunc.pdf')
    plt.show()

    return

