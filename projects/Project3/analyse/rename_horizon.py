# coding: utf-8
import read_horizon as r
import glob, sys
import os
files = glob.glob('../planet_data/*')
for f in files:
    with open(f) as infile:
        text = infile.read()
        name = r.parse_planet_name(text)
    with open(name+'_data.txt','w') as outfile:
        outfile.write(text)
        
# get_ipython().magic('save session 1-6')
