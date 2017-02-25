#!/usr/bin/python
#
# Library to handle paths from SVGs
# exported from OpenSCAD
#

from path_d import *

class Path:
    #
    # create new path object
    #
    def __init__(this, s, d=None, epilogue=None):
        if d == None:
            # parse from string
            a = s.find("d=\"") + 3
            b = s.find("\"", a)
            this.d = D(s[a:b])
            this.epilogue = s[b+1:]
        else:
            # define attributes directly
            this.d = d
            this.epilogue = epilogue

    #
    # export path as string
    #
    def __str__(this):
        return "<path d=\"" + str(this.d) + "\"" + this.epilogue + "\n"

    #
    # return the number of path segments (M,L,z)
    #
    def __len__(this):
        d = str(this.d)
        return d.count('M') + d.count('L') + d.count('z')

    #
    # split all closed paths into separate paths
    #
    def split(this):
        paths = []
        d = str(this.d)

        # d="M ... z" is one closed path
        p = d.find("M ")
        while (p > -1):
            q = d.find(" z", p) + 2
            paths.append( Path(None, D(d[p:q]), this.epilogue) )
            p = d.find("M ", q)

        return paths

