#!/usr/bin/python
#
# Library to handle paths from SVGs
# exported from OpenSCAD
#

from element import SVGElement
from path_d import SVGPathDefinition
import sys


#
# Objects of this class are created
# for every <path/> element encountered in an SVG
#
class SVGPath(SVGElement):
    def __init__(self, svg=None, parent=None, attributes=[], debug=False):
        self.debug = debug
        super().__init__(svg=svg, parent=parent, tag="path", attributes=attributes, debug=debug)
        if not ("d" in self.attributes.keys()):
            self.attributes["d"] = ""
        self.d = SVGPathDefinition(path=self, d=self.attributes["d"], debug=self.debug)

    #
    # If this path has a parent element,
    # then split all closed paths in this path
    # into separate paths and append them
    # to the parent element after this path.
    #
    def split(self, modifyParentSVG=True):
        if modifyParentSVG and (self.parent is None):
            print("Error: Unable to split: SVG to modify is undefined.")
            sys.exit(1)

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
