import numpy as np
import matplotlib.pyplot as plt

def stability_analysis(file_dir, cmap = plt.cm.jet):
    N_vals = np.array(np.linspace(50,400,11),dtype=int)
    rho_vals = np.array(np.linspace(1,10,30))

    #=============== rho_max analysis =================
    fig1, axes = plt.subplots(2)
    step = 5.0/200.
    n = len(rho_vals)
    ev_i = 0
    error_values = []
    for i, rho_max in enumerate(rho_vals):
        color = cmap(float(i)/(n-1)) 
        N = int(rho_max/step)
        fig1, axes, rel_error = plot_noninteracting(rho_max, N, file_dir, axes=axes, 
                color = color, rho_analysis=True, eigenvalue_i=ev_i)
        error_values.append(rel_error)


    ax1,ax2 = axes
    [ax.grid('on') for ax in [ax1,ax2]]

    ax2.semilogy(rho_vals,error_values)
    ax1.legend()
    #ax2.axhline(11.)
    ax1.set_xlabel('$\\rho$ ')
    ax1.set_ylabel('$u_{%d}^2$'%ev_i)
    ax2.set_ylabel('$E_%d$' %ev_i)
    ax2.set_xlabel('$\\rho_{\\text{max}}$')

    #================ N analysis ==============
    fig2, ax3 = plt.subplots(1)
    fig3, ax4 = plt.subplots(1)
    axes = [ax3,ax4]
    rho_max = 5.0
    N = 200
    n = len(N_vals)
    error_values = []
    for i, N in enumerate(N_vals):
        color = cmap(float(i)/(n-1)) 
        fig2, axes, rel_error = plot_noninteracting(rho_max, N, file_dir, axes=axes, 
                color = color, rho_analysis=False, eigenvalue_i=ev_i)
        error_values.append(rel_error)

    [ax.grid('on') for ax in [ax3,ax4]]
    ax4.loglog(N_vals,error_values)

    ax3.legend()
    #ax4.axhline(11.)
    ax3.set_xlabel('$\\rho$ ')
    ax3.set_ylabel('$u_{%d}^2$'%ev_i)
    ax4.set_ylabel('$E_%d$' %ev_i)
    ax4.set_xlabel('$N$')


    try:
        fig1.savefig('results/rhoMaxAnalysis.pdf')
        fig2.savefig('results/dimAnalysis.pdf')
        plt.show()
    except ValueError:
        # \\text obviously doesnt work some times
        ax2.set_xlabel('rho_max')
        fig1.savefig('results/rhoMaxAnalysis.pdf')
        fig2.savefig('results/dimAnalysis.pdf')
        plt.show()

def plot_iterations(file_dir, ax):
    filename = file_dir + 'iterations.txt'
    if ax is None:
        fig, ax = plt.subplots(2)
    else:
        fig = plt.gcf()

    N, iterations = np.loadtxt(filename).T
    logN = np.log(N) 
    logIter = np.log(iterations)
    gradient = np.average(logIter/logN)
    lines = ax.loglog(N, iterations, '-o')
    ax.legend(['Gradient = %.2f' %gradient])
    ax.set_ylabel('Iterations used')
    ax.set_xlabel('$N$')
    ax.grid('on')
    ax.axis('equal')
    plt.savefig('results/iterations.pdf')
    return fig, ax


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

    expect = (4*eigenvalue_i+3)
    result = eigval[eigenvalue_i]
    rel_error = np.abs(expect-result)/result
    print 'rho_max = %.2f, N = %d'  %(rho_max,dim)
    print 'eigenvalue no %d = %f'   %(eigenvalue_i, result)
    print 'relative error : %f'     %(rel_error)
    r = np.loadtxt(filename + "rho.txt",skiprows=2)
    if rho_analysis:
        label = 'rhomax = %.0f' % rho_max
        # ax2.scatter(rho_max, rel_error, c=color)
    else:
        label = 'N = %d' %dim
        # ax2.scatter(dim, rel_error, c=color)
    ax1.plot(r,eigvec[:,2]**2, c=color, label = label ) 
    return fig, [ax1,ax2], rel_error


if __name__ == "__main__":
    case = "non_interacting"
    method = "jacobi"
    file_base = "build/{}/{}/" .format( case, method)
    stability_analysis(file_base)

