import numpy as np
import matplotlib.pyplot as plt

def stability_analysis(file_dir, figsize=(6,4),cmap = plt.cm.jet):
    N_vals = np.array(np.linspace(50,400,11),dtype=int)
    rho_vals = np.array(np.linspace(1,10,30))

    #=============== rho_max analysis =================
    fig1, ax1 = plt.subplots(figsize=figsize)
    fig2, ax2 = plt.subplots(figsize=figsize)
    axes = ax1,ax2
    step = 5.0/200.
    n = len(rho_vals)
    ev_i = 0
    error_values = []
    color_values = cmap(np.linspace(0,1,n)) 
    sm = plt.cm.ScalarMappable(cmap=cmap,
            norm=plt.normalize(vmin=rho_vals[0], vmax=rho_vals[-1]))
    sm.set_array([])
    for i, rho_max in enumerate(rho_vals):
        color = color_values[i]
        N = int(rho_max/step)
        _, axes, rel_error = plot_noninteracting(rho_max, N, file_dir, axes=axes, 
                color = color, rho_analysis=True, eigenvalue_i=ev_i)
        error_values.append(rel_error)

    
    cb = fig1.colorbar(sm, ax=ax1)
    cb.set_label('$\\rho$ max')

    

    #[ax.grid('on') for ax in [ax1,ax2]]

    ax2.semilogy(rho_vals,error_values)
    ax2.legend(["$\\epsilon_%d$" % i for i in range(len(error_values))])
    # ax1.legend()
    ax1.set_xlim([0,4])
    #ax2.axhline(11.)
    ax1.set_xlabel('$\\rho$ ')
    ax1.set_ylabel('$u_{%d}^2$'%ev_i)
    ax2.set_ylabel('$E_%d$' %ev_i)
    ax2.set_xlabel('$\\rho_{\\text{max}}$')

    #================ N analysis ==============
    fig3, ax3 = plt.subplots(1,figsize=figsize)
    fig4, ax4 = plt.subplots(1,figsize=figsize)
    axes = [ax3,ax4]
    rho_max = 5.0
    N = 200
    n = len(N_vals)
    error_values = []

    sm = plt.cm.ScalarMappable(cmap=cmap,
            norm=plt.normalize(vmin=N_vals[0], vmax=N_vals[-1]))
    sm.set_array([])

    for i, N in enumerate(N_vals):
        color = cmap(float(i)/(n-1)) 
        _, axes, rel_error = plot_noninteracting(rho_max, N, file_dir, axes=axes, 
                color = color, rho_analysis=False, eigenvalue_i=ev_i)
        error_values.append(rel_error)

    error_values = np.array(error_values)
    cb = fig3.colorbar(sm, ax=ax3)
    cb.set_label('$\\rho$ max')

    #[ax.grid('on') for ax in [ax3,ax4]]
    logN = np.log(N_vals) 
    logError = np.log(error_values)
    print(logError.shape, logN.shape, (logError.T/logN).shape)
    gradient = np.average(logError.T/logN, axis = 1)
    print gradient
    ax4.axis('equal')
    print(N_vals.shape, error_values.shape)
    for i in range(len(gradient)):
        ax4.loglog(N_vals,error_values[:,i], label='$\\epsilon_%d$'%(i+1))
    ax4.legend()

    # ax3.legend()
    ax3.set_xlim([0,4])
    #ax4.axhline(11.)
    ax3.set_xlabel('$\\rho$ ')
    ax3.set_ylabel('$u_{%d}^2$'%ev_i)
    ax4.set_ylabel('$E_%d$' %ev_i)
    ax4.set_xlabel('$N$')


    try:
        fig1.savefig('results/rhoMaxAnalysis1.pdf')
        fig2.savefig('results/rhoMaxAnalysis2.pdf')
        fig3.savefig('results/dimAnalysis1.pdf')
        fig4.savefig('results/dimAnalysis2.pdf')
        plt.show()
    except ValueError:
        # \\text obviously doesnt work some times
        ax2.set_xlabel('rho_max')
        fig1.savefig('results/rhoMaxAnalysis1.pdf')
        fig2.savefig('results/rhoMaxAnalysis2.pdf')
        fig3.savefig('results/dimAnalysis1.pdf')
        fig4.savefig('results/dimAnalysis2.pdf')
        plt.show()

def plot_iterations(file_dir, ax):
    filename = file_dir + 'iterations.txt'
    if ax is None:
        fig, ax = plt.subplots(2,figsize=figsize)
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
        fig, [ax1,ax2] = plt.subplots(2,figsize=figsize)
    else:
        ax1,ax2 = axes
        fig = plt.gcf()

    filename = file_dir + "rho_%.2f_N_%d" %(rho_max, dim)
    eigval = np.loadtxt(filename + "val.txt",skiprows=2)
    eigvec = np.loadtxt(filename + "vec.txt",skiprows=2)

    sort = np.argsort(eigval)
    eigval = eigval[sort]
    eigvec = eigvec[:,sort]

    values = np.arange(3,dtype=int)
    expect = (4*values+3)
    result = eigval[values]
    rel_error = np.abs(expect-result)/result
    print 'rho_max = %.2f, N = %d'  %(rho_max,dim)
    for i in values:
        print 'eigenvalue no %d = %f'   %(values[i], result[i])
        print 'relative error : %f'     %(rel_error[i])
    r = np.loadtxt(filename + "rho.txt",skiprows=2)
    step = np.average(np.diff(r))
    if rho_analysis:
        label = 'rhomax = %.0f' % rho_max
        # ax2.scatter(rho_max, rel_error, c=color)
    else:
        label = 'N = %d' %dim
        # ax2.scatter(dim, rel_error, c=color)
    ax1.plot(r,eigvec[:,eigenvalue_i]**2/step, lw = 1,c=color, label = label ) 
    return fig, [ax1,ax2], rel_error


if __name__ == "__main__":
    case = "non_interacting"
    method = "jacobi"
    file_base = "build/{}/{}/" .format( case, method)
    stability_analysis(file_base)

