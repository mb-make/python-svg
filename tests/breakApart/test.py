#!/usr/bin/python3

filename = "combined_paths.svg"

#
# TODO:
# * Import SVG
# * Print number of path elements (should be 1)
# * Find/select first path and break apart
# * Print number of path elements (should be 2)
#

f = SVG(filename)
paths = f.find("path")
...len(paths)
...should be 1

path = paths[0]
path.breakApart()

paths2 = f.find("path")
...len(paths)
...should be 2
