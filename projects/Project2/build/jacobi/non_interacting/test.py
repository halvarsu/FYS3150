import glob

a = map(lambda x: x.split("_")[3],glob.glob("*N*"))
print [b[:-7] for b in a]

