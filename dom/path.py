#!/usr/bin/python
#
# Library to handle paths from SVGs
# exported from OpenSCAD
#

import sys
import numpy as np

from .element import SVGElement
from .path_d import SVGPathDefinition
from ..selecting.bbox import SVGBoundingBox


#
# Objects of this class are created
# for every <path/> element encountered in an SVG
#
class SVGPath(SVGElement, SVGBoundingBox):
    def __init__(self, svg=None, parent=None, attributes={}, debug=False):
        SVGElement.__init__(self, svg=svg, parent=parent, tag="path", attributes=attributes, debug=debug)
        if "d" in self.attributes.keys():
            d = self.attributes["d"]
            self.attributes["d"] = SVGPathDefinition(path=self, d=d, debug=self.debug)

    # Return this object's path definition object
    def getD(self):
        if "d" in self.attributes.keys():
            return self.attributes["d"]
        return None

    # Update path definition string
    def setD(self, s):
        self.attributes["d"] = SVGPathDefinition(path=self, d=s, debug=self.debug)

    # Return the number of points this path is comprised of
    def __len__(self):
        return len(self.getPoints())

    # Return the path definition's array of (x,y) values (numpy type)
    def getPoints(self):
        d = self.getD()
        if d is None:
            return np.array([])
        return d.getPoints()

    # Return the n-th point of this path
    def getPoint(self, index):
        points = self.getPoints()
        if index >= len(points):
            return None
        return points[index]

    # Return an array of the path definition's X coordinates (numpy type)
    def getPointsX(self):
        points = self.getPoints()
        if points is None:
            return None
        # a = []
        # for p in points:
        #     a.append(p[0])
        # return np.array(a)
        return points.T[0, :]

    # Return an array of the path definition's Y coordinates (numpy type)
    def getPointsY(self):
        points = self.getPoints()
        if points is None:
            return None
        # a = []
        # for p in points:
        #     a.append(p[1])
        # return np.array(a)
        return points.T[1, :]

    #
    # Overload some getters of SVGBoundingBox
    #
    def getMinX(self):
        return self.getPointsX().min()

    def getMinY(self):
        return self.getPointsY().min()

    def getMaxX(self):
        return self.getPointsX().max()

    def getMaxY(self):
        return self.getPointsY().max()

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
