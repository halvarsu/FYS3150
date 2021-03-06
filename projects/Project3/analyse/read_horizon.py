import sys
import re
import glob
import numpy as np
import analyse
import tools

def get_mass(body_name):
    sun_mass = 1.988544e6 # in 10e24 kg
    pm = {'Mercury':0.3301 ,'Venus':4.867 ,'Earth':5.972 ,'Moon':0.073
            ,'Mars':0.642 ,"Jupiter":1898
            ,'Saturn':568 ,'Uranus':86.8 ,'Neptune':102 ,'Pluto':0.0146} # in 10e24 kg

    masses = {k:m/sun_mass for k,m in pm.items()}        
    masses['Sun'] = 1
    return masses[body_name]


def parse_body_name(text):
    name_index = text.find("Target body name: ")
    body_name = text[name_index:].split("\n")[0].split()[3]
    return body_name

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
    body_name = parse_body_name(text)
    mass = get_mass(body_name)
    print("Parsing body: %10s  | Mass: %12g solar masses" %(body_name, mass))
    pos, vel = parse_pos_and_vel(text)

    # Convert GM to sun masses 
    if body_name == 'Earth':
        print("earth dist to sun[AU]: %g " %np.linalg.norm(list(map(float, pos))))
        print("earth velocity[AU/yr]: %g " %np.linalg.norm(list(map(float, vel))))

    data = " ".join(pos) + " " + " ".join(vel) + " "+ str(mass)
    return body_name, data

def fix_barycentric(outfile_lines):
    """Reads the data and corrects velocities such that the center of mass
    is at rest"""
    # [years, steps_per_year, has_fixed_sun, relativistic, n_bodies]
    info = outfile_lines[:5]
    bodies = outfile_lines[5:]
    bodies = np.array(map(lambda x:map(float,x.split()),bodies))
    pos = bodies[:,:3]
    vel =  bodies[:,3:-1]
    mass = bodies[:,-1]
    M = np.sum(mass)
    mom = (vel.T*mass).T
    tot_mom = np.sum(mom, axis=0)
    vel =  vel -tot_mom / M

    bodies_array = np.concatenate((pos,vel,mass[:,np.newaxis]),axis=1)
    print(bodies_array.shape)
    bodies = []
    for body in bodies_array:
        bodies.append(" ".join(map(str,body)))

    outfile_lines_new = info + bodies
    return outfile_lines_new
    



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
    parser.add_argument('-m','--main_body',default='Sun')
    parser.add_argument('-y','--years',default=2, type=int)
    parser.add_argument('-s','--steps_per_year',default=10000, type=int)
    parser.add_argument('-v','--verbose', help='1 = print all, 0 = no print',type=int, choices = [0,1], default = 1)
    parser.add_argument('--fix_barycentric',action='store_true')
    parser.add_argument('--fixed_sun',action='store_true')
    parser.add_argument('--relativistic',action='store_true')
    parser.add_argument('--use_euler',action='store_true')
    args = parser.parse_args()
    return args

def main(args):
    if args.verbose == 0:
        tools.blockPrint()
    if args.folder:
        files = glob.glob(args.folder+'/*')
    else:
        files = glob.glob(args.filename)
    print(files)
    years = args.years
    steps_per_year = args.steps_per_year
    n_bodies =      len(files)
    has_fixed_sun = int(args.fixed_sun)
    relativistic =  int(args.relativistic)
    use_euler =     int(args.use_euler)
    outfile_lines = [years, steps_per_year, has_fixed_sun, relativistic,  use_euler, n_bodies]
    print ("Years:  %d   Steps per year: %d   fixed:  %d  relativistic: "\
            "%d  Euler %d"%(years, steps_per_year, has_fixed_sun,
                relativistic, use_euler))
    print ()
    n_info_lines = len(outfile_lines)
    # bodies = [] 
    for filename in files:
        # main file parser:
        with open(filename) as infile:
            text = infile.read()
            body_name, data = process_data(text)
        if body_name == args.main_body:
            # Set as the first body
            print(" -----> Setting Sun as first body")
            outfile_lines.insert(n_info_lines,data)
        else:
            outfile_lines.append(data)
    if args.fix_barycentric:
        outfile_lines = fix_barycentric(outfile_lines)

    outfile_text = '\n'.join(map(str, outfile_lines))

    if args.outfile:
        # if name of outfile is specified
        outfile_name = args.outfile
    elif args.folder:
        # use name of folder 
        outfile_name = 'in/'
        outfile_name += [a for a in args.folder.split('/') if a][-1]
        outfile_name += "Fixed" if args.fixed_sun else ""
        outfile_name += '.txt'
    elif n_bodies == 1:
        # use name of planet
        outfile_name = body_name + '.txt'
    else:
        # default filename
        outfile_name = 'in/data.txt'

    print('opening file for writing...')

    with open(outfile_name, 'w') as outfile:
        outfile.write(outfile_text)
        print('Success! Wrote %d characters on %d lines to file %s'
                %(len(data),len(outfile_lines), outfile_name))
    return

if __name__ == "__main__":
    args =  get_args()
    main(args)

