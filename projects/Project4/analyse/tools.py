import numpy as np

def sine_print(text, i, width=60, freq=10):
    print("{1: ^{0}}".format(width,
        "*{1:=^{0}}*".format(int((width-len(text)-1)/2*(1+np.sin(i/10.))+len(text)),text)))

def linear_print(text, i, width, end=100):
    print("{1: ^{0}}".format(width,
        "*{1:=^{0}}*".format(int((width-len(text)-2)*i/end+len(text)),text)))


def process_data(data):
    sim_data = []
    for simulation in data:
        line_data = []
        lines = simulation.split('\n')
        for line in lines:
            out = [float(d) for d in line.split()]
            if out:
                line_data.append(out)
        sim_data.append(line_data)
    return np.array(sim_data).swapaxes(0,1).swapaxes(1,2)

