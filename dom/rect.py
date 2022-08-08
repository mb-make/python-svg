#!/usr/bin/python
#
# SVG rectangles
#

from .element import SVGElement
from ..selecting.bbox import SVGBoundingBox


class SVGRect(SVGElement, SVGBoundingBox):
    #
    # TODO: Add support for transformed element or parents
    #
    def __init__(self, svg=None, parent=None, attributes={}, debug=False):
        SVGElement.__init__(self, svg=svg, parent=parent, tag="rect", attributes=attributes, debug=debug)

        x = 0.0
        if "x" in attributes.keys():
            x = attributes["x"]
        self.x = float(x)

        y = 0.0
        if "y" in attributes.keys():
            y = attributes["y"]
        self.y = float(y)

        width = 0.0
        if "width" in attributes.keys():
            width = attributes["width"]
        self.width = float(width)

        height = 0.0
        if "height" in attributes.keys():
            height = attributes["height"]
        self.height = float(height)

        # Width and height shall not be negative
        if self.width < 0.0:
            self.x += self.width
            self.width *= -1.0
        if self.height < 0.0:
            self.y += self.height
            self.height *= -1.0

        # Calculate bounding box in absolute coordinates
        self.bottomLeftRelative = (self.x, self.y)
        self.topRightRelative   = (self.x+self.width, self.y+self.height)
        # self.bottomLeftAbsolute = self.bottomLeftRelative * self.getCTM()
        # self.topRightAbsolute   = self.topRightRelative * self.getCTM()
        # (self.minX, self.minY) = self.bottomLeftAbsolute
        # (self.maxX, self.maxY) = self.topRightAbsolute
