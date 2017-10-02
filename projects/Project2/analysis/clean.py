import os
import glob
import sys

file_dir = "/uio/hume/student-u10/halvarsu/uio/FYS3150/projects/Project2/build/{}/{}/*"

methods = [m for m in ["arma", "jacobi"] if raw_input("clean "+m+"?(y/N)") == "y"]
case = [c for c in ["interacting", "non_interacting"] if raw_input("clean "+c+"?(y/N)") == "y"]
print case

if raw_input('really remove files?(y/N)') == 'y':
    print "removing files"
    pass
else:
    print "exiting"
    sys.exit()

for c in case:
    for m in methods:
        files = glob.glob(file_dir.format(m, case))
        for f in files:
            print("removing %s" %f)
            os.remove(f)
