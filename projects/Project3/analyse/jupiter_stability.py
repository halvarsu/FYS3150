from analyse import read_data
import numpy as np
import matplotlib.pyplot as plt
import glob

def main():
    plot_jupiter_stability()

def plot_jupiter_stability():
    filenames = [f for f in glob.glob('out/EJS_unfix/*') if f.endswith('.bin')]
     
    fig, [ax1,ax2] = plt.subplots(2, sharex=True, figsize=(6,4))

    AU = 149597870700
    year = 31556926
    sun_mass = 1.99e30
    Astrojoule = (AU/year)**2 * sun_mass

    n_values = []
    for i, f in enumerate(filenames):
        temp = f.split('.')[0]

        num = temp[temp.find('1'):]
        print(num)
        if num[0] != '1':
            num = 'Normal'

        data = read_data(f, None)
        planet = data["pos"][:,1]
        n_values.append(data["steps_per_year"])

        time = data["time"] 
        kinetic, potential, total, angmom = data['energies']
        x, y, z = planet.T
        r = np.sqrt(x**2 + y**2 + z**2)
    
        ax1.plot(time, r, label='Jupiter mass = %s' %num)
        ax2.plot(time, total*Astrojoule, label='Jupiter mass = %s' %num)

    ax1.legend()
    ax2.set_title('Total energy (Jupiter + Earth)')
    ax1.set_ylabel('distance to origin [au]')
    ax2.set_xlabel("Time [yr]")
    ax2.set_ylabel("Energy [Joule]")


    plt.tight_layout()
    num = len(glob.glob('results/energyEarthJupiter*.pdf'))
    plt.savefig('results/energyEarthJupiter%d.pdf' %num)
    plt.show()



if __name__ == "__main__":
    main()
