#!/usr/bin/python
#
# Script to insert cuts into stereo-text SVG
# exported from OpenSCAD
#

from sys import argv
from svg import *
from path_d import *

# get filenames from console arguments
if len(argv) < 3:
    print "Usage: " + argv[0] + " <SVG in which to insert cuts> <save as filename>"
    exit()

filename_open = argv[1]
filename_save = argv[2]

# import SVG
svg = SVG(filename_open)

# split path into closed paths
svg.break_apart()

# find short path, assume it to be a cut path
for path in svg.paths:
    if len(path) < 10:
        print "rewriting short cut path: \n\t" + str(path.d)

        # extract relevant coordinates
        a = path.d.min_x()
        b = path.d.max_x()
        y = path.d.min_y()

        # rewrite path
        s = "M "+str(a)+","+str(y)+" L "+str(b)+","+str(y)
        print "\t"+s
        path.d = D(s)

# find the maximum and minimum y coordinates from all paths
min_y = None
max_y = None
for path in svg.paths:
    # minimum y
    y = path.d.min_y()
    if (min_y == None) or (y < min_y):
        min_y = y

    # maximum y
    y = path.d.max_y()
    if (max_y == None) or (y > max_y):
        max_y = y

print min_y
print max_y

# export SVG
svg.save_as(filename_save)
