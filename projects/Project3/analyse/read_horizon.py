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
    vel = [str(float(v)*365.242199).lower() for v in vel if v]
    pos = [p.lower() for p in pos if p]
    return pos,vel

def process_data(text):
    # infile.readline()
    
    # text = infile.read()

    # pick out target name
    planet_name = parse_planet_name(text)
    mass = masses[planet_name]
    print("Body: %10s  | Mass: %12g solar masses" %(planet_name, mass))
    pos, vel = parse_pos_and_vel(text)

    # Convert GM to sun masses 
    if planet_name == 'Earth':
        import numpy as np
        print("earth dist to sun[AU]: %g " %np.linalg.norm(list(map(float, pos))))
        print("earth velocity[AU/yr]: %g " %np.linalg.norm(list(map(float, vel))))

    data = " ".join(pos) + " " + " ".join(vel) + " "+ str(mass)
    return planet_name, data


def read_mbox(args):
    import mailbox

    mb = mailbox.mbox('NASA.mbox', create=False)
    mails = mb.values()

    for i,mail in enumerate(mails):
        mail_text = str(mail)
        message_start = mail_text.find('Automated mail xmit by MAIL_REQUEST')
        if message_start > 0:
            message = mail_text[message_start:]


def get_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--filename',default='planet_data/horizons_results*.txt')
    parser.add_argument('-F','--folder',default='')
    parser.add_argument('-o','--outfile',default='')
    parser.add_argument('-y','--years',default=2, type=int)
    parser.add_argument('-s','--steps_per_year',default=10000, type=int)
    parser.add_argument('--fixed_sun',action='store_true')
    args = parser.parse_args()
    return args

def main(args):
    return

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
    n_bodies = len(files)
    hasFixedSun = int(args.fixed_sun)
    outfile_lines = [years, steps_per_year, hasFixedSun, n_bodies]
    n_info_lines = len(outfile_lines)
    # bodies = [] 
    for filename in files:
        # main file parser:
        with open(filename) as infile:
            text = infile.read()
            planet_name, data = process_data(text)
        if planet_name == 'Sun':
            # Set as the first body
            outfile_lines.insert(4,data)
            # bodies.insert(0,planet_name)
        else:
            outfile_lines.append(data)
            # bodies.append(planet_name)

    outfile_text = '\n'.join(map(str, outfile_lines))

    if args.outfile:
        # if name of outfile is specified
        outfile_name = args.outfile
    elif args.folder:
        # use name of folder 
        outfile_name = 'in/'
        outfile_name += [a for a in args.folder.split('/') if a][-1]
        outfile_name += '.txt'
    elif n_bodies == 1:
        # use name of planet
        outfile_name = planet_name + '.txt'
    else:
        # default filename
        outfile_name = 'in/data.txt'

    print('opening file...')

    with open(outfile_name, 'w') as outfile:
        outfile.write(outfile_text)
        print('Success! Wrote %d characters on %d lines to file %s'
                %(len(data),len(outfile_lines), outfile_name))
