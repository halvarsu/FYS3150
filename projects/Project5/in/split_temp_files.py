import os
import glob
import argparse
import itertools

parser = argparse.ArgumentParser()
parser.add_argument("-N", "--number_of_outputs",type=int,default=4)
parser.add_argument("-f", "--filename",default="all_temps.txt")
parser.add_argument("-C", "--clean", action="store_true")
args = parser.parse_args()

if args.clean:
    [os.system('rm {}'.format(f)) for f in glob.glob("temps*")]


def grouper(n, iterable, fillvalue=None):
        "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
        args = [iter(iterable)] * n
        return itertools.izip_longest(fillvalue=fillvalue, *args)

with open("all_temps.txt") as infile:
    temps = [int(line) for line in infile.readlines()]

files = [open("temps{}".format(i),"w") for i in range(1,1+args.number_of_outputs)]

for temp_group in grouper(args.number_of_outputs, sorted(temps)):
    for i,T in enumerate(temp_group):
        outfile = files[i]
        outfile.write(str(T) + "\n")

for f in files:
    f.close()


