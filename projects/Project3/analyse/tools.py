import os, sys

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__

def printDisable(*args):
    enablePrint()
    print(args)
    blockPrint()


