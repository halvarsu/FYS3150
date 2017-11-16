import numpy as np

def sine_print(text, i, width=60, freq=10):
    print("{1: ^{0}}".format(width,
        "*{1:=^{0}}*".format(int((width-len(text)-1)/2*(1+np.sin(i/10.))+len(text)),text)))

def linear_print(text, i, width, end=100):
    print("{1: ^{0}}".format(width,
        "*{1:=^{0}}*".format(int((width-len(text)-2)*i/end+len(text)),text)))


def process_data(data, return_two = False):
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
    if not letter:
        letter = str(unichr(65+num))
    ax.text(pos[0], pos[1],  letter, transform=ax.transAxes,
        fontsize=16, fontweight='bold', va='top')
