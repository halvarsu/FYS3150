import numpy as np
import matplotlib.pyplot as plt

def stability_analysis(file_dir, cmap = plt.cm.jet):
    N_vals = np.array(np.linspace(50,400,11),dtype=int)
    rho_vals = np.array(np.linspace(1,10,11))[3:]

    #=============== rho_max analysis =================
    fig, axes = plt.subplots(2)
    N = 200
    n = len(rho_vals)
    for i, rho_max in enumerate(rho_vals):
        color = cmap(float(i)/(n-1)) 
        plot_noninteracting(rho_max, N, file_dir, axes=axes, 
                color = color, rho_analysis=True)

    ax1,ax2 = axes
    [ax.grid('on') for ax in [ax1,ax2]]

    ax1.legend()
    ax2.axhline(11.)
    ax1.set_xlabel('rho ')
    ax1.set_ylabel('u**2')
    ax2.set_xlabel('rho max')
    ax2.set_ylabel('E_3')
    fig.savefig('rho_max_analysis.pdf')

    #================ N analysis ==============
    fig, axes = plt.subplots(2)
    rho_max = 7.0
    N = 200
    n = len(N_vals)
    for i, N in enumerate(N_vals):
        color = cmap(float(i)/(n-1)) 
        plot_noninteracting(rho_max, N, file_dir, axes=axes, 
                color = color, rho_analysis=False)

    ax1,ax2 = axes
    [ax.grid('on') for ax in [ax1,ax2]]

    ax1.legend()
    ax2.axhline(11.)
    ax1.set_xlabel('rho ')
    ax1.set_ylabel('u**2')
    ax2.set_xlabel('rho max')
    ax2.set_ylabel('E_3')
    plt.show()


def plot_noninteracting(rho_max, dim, file_dir, eigenvalue_i = 0, axes=None,
        color=plt.cm.jet(0), rho_analysis=True):
    if axes is None:
        fig, [ax1,ax2] = plt.subplots(2)
    else:
        ax1,ax2 = axes
        fig = plt.gcf()

    filename = file_dir + "rho_%.2f_N_%d" %(rho_max, dim)
    eigval = np.loadtxt(filename + "val.txt",skiprows=2)
    eigvec = np.loadtxt(filename + "vec.txt",skiprows=2)

    sort = np.argsort(eigval)
    eigval = eigval[sort]
    eigvec = eigvec[:,sort]

    print 'rho_max = %.2f, N = %d' %(rho_max,dim)
    print 'eigenvalue no %d = %f' %(eigenvalue_i,eigval[eigenvalue_i])
    r = np.loadtxt(filename + "rho.txt",skiprows=2)
    if rho_analysis:
        label = 'rhomax = %.0f' % rho_max
        ax2.scatter(rho_max, eigval[2], c=color)
    else:
        label = 'N = %d' %dim
        ax2.scatter(dim, eigval[2], c=color)
    ax1.plot(r,eigvec[:,2]**2, c=color, label = label ) 
    return fig, [ax1,ax2]


if __name__ == "__main__":
    version = "Release"
    method = "jacobi"
    case = "non_interacting"
    file_base = "build-proj2-Desktop_Qt_5_9_1_GCC_64bit-{}/{}/{}/" .format(version, case, method)
    stability_analysis(file_base)

