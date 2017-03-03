#!/usr/bin/python
#
# Library to work with SVGs exported from OpenSCAD
#

from path import *
from rect import *

class SVG:
    def __init__(this, filename):
        # parse from file
        this.svg = open(filename).read()

        first_occurence_of_a_path = this.svg.find("<path ")
        this.preamble = this.svg[:first_occurence_of_a_path]

        this.epilogue = "</svg>\n"

        this.populate_elements()

    def populate_elements(this):
        # begin with empty list
        this.elements = []

        # find first element in SVG DOM
        p = this.svg.find("<")
        while (p > -1):
            q = this.svg.find(' ', p)
            e = this.svg.find(">", p)

            t = this.svg[p+1:min(q,e)].strip()

            s = this.svg[p:e+1]

            if t == "path":
                print "Found path: '"+s+"'"
                this.elements.append( Path(s) )
            elif t == "rect":
                print "Found rect: '"+s+"'"
                this.elements.append( Rect(s) )

            # find next element in SVG DOM
            p = this.svg.find("<", e)

    #
    # export as string
    #
    def __str__(this):
        return this.preamble \
            + "\n".join([str(e) for e in this.elements]) \
            + this.epilogue

    #
    # save string to file
    #
    def save_as(this, filename):
        open(filename, "w").write(str(this))

    #
    # Split the one mega-path, which OpenSCAD exports,
    # into connected paths
    #
    def break_apart(this):
        oldlist = this.elements
        for e in oldlist:
            if e.__class__.__name__ == Path.__name__:
                this.elements.extend( e.split() )
                this.elements.remove(e)
