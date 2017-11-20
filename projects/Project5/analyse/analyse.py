import argparse
import numpy as np
import matplotlib.pyplot as plt

def main(args):
    """Either runs all parts or just one"""
    parts = {1:part1}
    if args.part == 0:
        part1(args)
    else:
        parts[args.part]()


def part1(args):
    return
    

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-p','--part', type=int,default=0, 
                        choices = [0,1,2,3])
    return parser.parse_args()

if __name__=='__main__':
    args = get_args()
    main(args)

