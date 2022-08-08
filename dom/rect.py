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
    def __init__(self, attributes=[]):
        self.x = attributes["x"] or 0.0
        self.y = attributes["y"] or 0.0
        self.width = attributes["width"] or 0.0
        self.height = attributes["height"] or 0.0

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
        self.bottomLeftAbsolute = self.bottomLeftRelative * self.getCTM()
        self.topRightAbsolute   = self.topRightRelative * self.getCTM()
        (self.minX, self.minY) = self.bottomLeftAbsolute
        (self.maxX, self.maxY) = self.topRightAbsolute
