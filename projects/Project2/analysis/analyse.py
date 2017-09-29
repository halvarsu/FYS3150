import numpy as np
import matplotlib.pyplot as plt

file_dir = "/uio/hume/student-u10/halvarsu/uio/FYS3150/projects/Project2/build-proj2-Desktop_Qt_5_9_1_GCC_64bit-Debug/"

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

plot_eigvecs(0.0, 7., 200)
#plot_eigvecs(0.25, 7., 200)
#plot_eigvecs(1., 7., 200)
