import sys
import re

def parse_planet_name(text):
    name_index = text.find("Target body name: ")
    planet_name = text[name_index:].split("\n")[0].split()[3]
    return planet_name

def parse_pos_and_vel(text):
    index = text.find("$$SOE")
    pos, vel = text[index:].split("\n")[2:4]
    non_decimal = re.compile(r'[^\d=.E\-+]+')
    pos = non_decimal.sub('',pos).split('=')
    vel = non_decimal.sub('',vel).split('=')
    vel = [str(float(v)*365.25).lower() for v in vel if v]
    pos = [p.lower() for p in pos if p]
    return pos,vel

def process_data(filename, outfile = None):
    with open(filename) as infile:
        infile.readline()
        
        text = infile.read()

        # pick out target name
        planet_name = parse_planet_name(text)
        mass = masses[planet_name]
        print(planet_name, mass)
        pos, vel = parse_pos_and_vel(text)

        # Convert GM to sun masses 
        if planet_name == 'Earth':
            import numpy as np
            print("earth dist to sun[AU]:")
            print(np.linalg.norm(list(map(float, pos))))
            print("earth velocity[AU/yr]:")
            print(np.linalg.norm(list(map(float, vel))))

        data = " ".join(pos) + " " + " ".join(vel) + " "+ str(mass)

    if outfile is None:
        with open(planet_name + "_data.txt","w") as outfile:
            outfile.write(data)
    else:
        outfile.write(data)

def get_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--filename',default='planet_data/horizons_results*.txt')
    parser.add_argument('-F','--folder',default='')
    parser.add_argument('-o','--outfile',default='in/data.txt')
    parser.add_argument('-y','--years',default=2, type=int)
    parser.add_argument('-s','--steps_per_year',default=10000, type=int)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args =  get_args()

    sun_mass = 1.988544e6 # in 10e24 kg
    pm = {'Mercury':0.3301 ,'Venus':4.867 ,'Earth':5.972 ,'Moon':0.073
            ,'Mars':0.642 ,"Jupiter":1898
            ,'Saturn':568 ,'Uranus':86.8 ,'Neptune':102 ,'Pluto':0.0146} # in 10e24 kg

    masses = {k:m/sun_mass for k,m in pm.items()}        
    masses['Sun'] = 1



    import glob
    if args.folder:
        files = glob.glob(args.folder+'/*')
    else:
        files = glob.glob(args.filename)
    print(files)
    years = args.years
    steps_per_year = args.steps_per_year
    if args.outfile:
        outfile = open(args.outfile, 'w')
        outfile.write("%d\n%d\n%d\n"%(years,steps_per_year, len(files)))
    else:
        outfile = None
    for filename in files:
        process_data(filename, outfile)
        if args.outfile:
            outfile.write('\n') 

    if args.outfile:
        outfile.close()

