#!/usr/bin/python
#
# Script to insert cuts into stereo-text SVG
# exported from OpenSCAD
#

from sys import argv
from svg import *

# get filenames from console arguments
if len(argv) < 3:
    print "Usage: " + argv[0] + " <SVG in which to insert cuts> <save as filename>"
    exit()

filename_open = argv[1]
filename_save = argv[2]

# import SVG
svg = SVG(filename_open)

svg.break_apart()

index = 0
while (index < len(svg.paths)):
    path = svg.paths[index]
    if len(path) < 10:
        print "removing very short path: " + str(path).replace("\n","")
        svg.paths.remove(path)
    else:
        index += 1

svg.save_as(filename_save)
