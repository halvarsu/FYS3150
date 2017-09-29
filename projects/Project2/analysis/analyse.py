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

#plot_eigvecs(0.0, 7., 200)
# plot_eigvecs(0.25, 7., 200)
# plot_eigvecs(1., 7., 200)

def plot_rho_stability(rho_vals, dim,file_dir):
    fig, [ax1,ax2] = plt.subplots(2)
    eigenvalues = np.zeros(len(rho_vals))
    for i,rho_max in enumerate(rho_vals):
        filename = "rho_stab%.0f_%d" %(rho_max, dim)
        eigval = np.loadtxt(file_dir + filename + "val.txt",skiprows=2)
        eigvec = np.loadtxt(file_dir + filename + "vec.txt",skiprows=2)

        sort = np.argsort(eigval)

        eigval = eigval[sort]
        eigvec = eigvec[:,sort]
        print 'rho = %.2f' %rho_max
        print 'third eigenvalue:', eigval[2]
        eigenvalues[i]= eigval[2]
        r = np.loadtxt(file_dir + filename+"rho.txt",skiprows=2)
        best = 7
        lw = 4 if rho_max == 7. else 1
        substr = '--' if rho_max == 7. else '-'
        cm = plt.cm.jet
        c = cm(rho_max/float(np.max(rho_vals)))
        ax1.plot(r,eigvec[:,2]**2,substr, lw = lw, c=c, label = 'rhomax = %.0f' %rho_max) 
        ax2.scatter(rho_max, eigval[2], c=c)
    # Find spot where third eigenvalue crosses 11-line
    crossed = eigenvalues < 11
    cross_point = len(eigenvalues[crossed])-2
    rho_A = rho_vals[cross_point]
    rho_B = rho_vals[cross_point+1]
    E_A = eigenvalues[cross_point] - 11
    E_B = eigenvalues[cross_point+1] - 11
    rho_opt =  rho_A - (rho_B - rho_A)/(E_B-E_A)*E_A
    print(rho_opt)
    ax2.scatter(rho_opt,11,c=0)
    print(eigenvalues[cross_point])
    

    [ax.grid('on') for ax in [ax1,ax2]]
    ax1.legend()
    ax2.axhline(11.)
    ax1.set_xlabel('rho ')
    ax1.set_ylabel('u**2')
    ax2.set_xlabel('rho max')
    ax2.set_ylabel('E_3')
    ax1.set_title('optimal rho_N = %.2f for N = %d' %(rho_opt,dim))
    plt.show()

def plot_N_stability(rho_max, dim_vals,file_dir, ev_i=0):
    fig, [ax1,ax2] = plt.subplots(2)
    eigenvalues = np.zeros(len(dim_vals))

    for i,dim in enumerate(dim_vals):
        filename = "N_stab_arma%.2f_%d" %(rho_max, dim)
        print(filename)
        eigval = np.loadtxt(file_dir + filename + "val.txt",skiprows=2)
        eigvec = np.loadtxt(file_dir + filename + "vec.txt",skiprows=2)

        sort = np.argsort(eigval)

        eigval = eigval[sort]
        eigvec = eigvec[:,sort]
        print 'dim = %d' %dim
        print 'eigenvalue no %d:' %(ev_i+1), eigval[ev_i]
        eigenvalues[i]= eigval[ev_i]
        r = np.loadtxt(file_dir + filename+"rho.txt",skiprows=2)
        best = 7
        lw = 4 if dim == 190 else 1
        substr = '--' if rho_max == 190 else '-'
        cm = plt.cm.jet
        c = cm(dim/float(np.max(dim_vals)))
        ax1.plot(r,eigvec[:,ev_i]**2,substr, lw = lw, c=c, label = 'dim = %d' %dim) 
        ax2.scatter(dim, eigval[ev_i], c=c)
    # Find spot where third eigenvalue crosses 11-line
    crossed = eigenvalues < expected_evs( ev_i )
    cross_point = len(eigenvalues[crossed])-2
    dim_A = dim_vals[cross_point]
    dim_B = dim_vals[cross_point+1]
    E_A = eigenvalues[cross_point] - expected_evs( ev_i )
    E_B = eigenvalues[cross_point+1] - expected_evs( ev_i )
    dim_opt =  dim_A - (dim_B - dim_A)/(E_B-E_A)*E_A
    print(dim_opt)
    ax2.scatter(dim_opt,expected_evs( ev_i ),c=0)
    print(eigenvalues[cross_point])
    

    [ax.grid('on') for ax in [ax1,ax2]]
    ax1.legend()
    ax2.axhline(expected_evs( ev_i ))
    ax1.set_xlabel('rho ')
    ax1.set_ylabel('u**2')
    ax2.set_xlabel('dim')
    ax2.set_ylabel('E_3')
    ax1.set_title('optimal dim = %d for rho_max = %.2f' %(dim_opt,rho_max))
    plt.show()

def expected_evs(i):
    return 4*(i+3./4)
file_dir = "/uio/hume/student-u10/halvarsu/uio/FYS3150/projects/Project2/build-proj2-Desktop_Qt_5_9_1_GCC_64bit-Release/"

#plot_rho_stability(np.arange(4,11) , 200,file_dir)
N_vals = np.array(np.linspace(50,1010,39),dtype=int)
plot_N_stability(6.79, N_vals ,file_dir, ev_i=0)


