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
    def __init__(this, s=None, d=None, epilogue=None):
        # initialize empty
        this.d = D()
        this.epilogue = ""

        # has a D object been provided ?
        if d == None:
            if s != None:
                # parse from string
                a = s.find("d=\"") + 3
                b = s.find("\"", a)
                this.d = D(s[a:b])
                this.epilogue = s[b+1:].strip("\n")
        else:
            # define attributes directly
            this.d = d
            this.epilogue = epilogue

        if (this.epilogue.find(">") == -1):
            this.epilogue += "/>"

    #
    # export path as string
    #
    def __str__(this):
        return "<path d=\"" + str(this.d) + "\"" + this.epilogue

    #
    # return the number of path segments (M,L,z)
    #
    def __len__(this):
        return len(this.d)

    #
    # split all closed paths into separate paths
    #
    def split(this):
        paths = []
        new_path = Path()

        # d="m/M ... z/Z" is one closed path
        for segment in this.d.segments:
            # append segment to current path
            new_path.d.segments.append(segment)

            # is the path complete?
            if segment.type == 'z' \
            or segment.type == 'Z':
                # path is complete, cut!
                new_path.epilogue = this.epilogue
                paths.append(new_path)
                # proceed with new path
                new_path = Path()

        return paths

