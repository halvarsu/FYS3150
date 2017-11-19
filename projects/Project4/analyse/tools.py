import numpy as np

def sine_print(text, i, width=60, freq=10):
    """Prints with a fill in the form of a sinus wave"""
    print("{1: ^{0}}".format(width,
        "*{1:=^{0}}*".format(int((width-len(text)-1)/2*(1+np.sin(i/10.))+len(text)),text)))

def linear_print(text, i, width, end=100):
    """Prints with a linearly increasing fill"""
    print("{1: ^{0}}".format(width,
        "*{1:=^{0}}*".format(int((width-len(text)-2)*i/end+len(text)),text)))


def process_data(data, return_two = False):
    """Reads lists of strings with lines and columns, and writes to a numpy
    array. Use return_two if every second element is of one category."""
    sim_data = []
    for simulation in data:
        line_data = []
        lines = simulation.split('\n')
        for line in lines:
            out = [float(d) for d in line.split()]
            if out:
                line_data.append(out)
        sim_data.append(line_data)
    data = np.array(sim_data).swapaxes(0,1).swapaxes(1,2)
    if return_two:
        return data[:,:,0::2], data[:,:,1::2]
    else:
        return data

def add_letter_label(ax,num, letter='', pos = [0.02,0.95]):
    """Adds a nice letter to the top of a matplotlib ax"""
    if not letter:
        letter = str(chr(65+num))
    ax.text(pos[0], pos[1],  letter, transform=ax.transAxes,
        fontsize=16, fontweight='bold', va='top')

def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    r"""From the internet, see http://scipy-cookbook.readthedocs.io/items/SavitzkyGolay.html. Smooth (and optionally differentiate) data with
    a Savitzky-Golay filter.  The Savitzky-Golay filter removes high
    frequency noise from data.  It has the advantage of preserving the
    original shape and features of the signal better than other types of
    filtering approaches, such as moving averages techniques.

    Parameters
    ----------
    y : array_like, shape (N,)
        the values of the time history of the signal.
    window_size : int
        the length of the window. Must be an odd integer number.
    order : int
        the order of the polynomial used in the filtering.
        Must be less then `window_size` - 1.
    deriv: int
        the order of the derivative to compute (default = 0 means only smoothing)
    Returns
    -------
    ys : ndarray, shape (N)
        the smoothed signal (or it's n-th derivative).
    Notes
    -----
    The Savitzky-Golay is a type of low-pass filter, particularly
    suited for smoothing noisy data. The main idea behind this
    approach is to make for each point a least-square fit with a
    polynomial of high order over a odd-sized window centered at
    the point.
    Examples
    --------
    t = np.linspace(-4, 4, 500)
    y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
    ysg = savitzky_golay(y, window_size=31, order=4)
    import matplotlib.pyplot as plt
    plt.plot(t, y, label='Noisy signal')
    plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
    plt.plot(t, ysg, 'r', label='Filtered signal')
    plt.legend()
    plt.show()
    References
    ----------
    .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
       Data by Simplified Least Squares Procedures. Analytical
       Chemistry, 1964, 36 (8), pp 1627-1639.
    .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
       W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
       Cambridge University Press ISBN-13: 9780521880688
    """
    import numpy as np
    from math import factorial
    
    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError, msg:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')
