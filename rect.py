#!/usr/bin/python
#
# SVG rectangles
#

from element import SVGElement


class SVGRect(SVGElement):
    def __init__(self, attributes=[]):
        self.x = attributes["x"] or 0.0
        self.y = attributes["y"] or 0.0
        self.width = attributes["width"] or 0.0
        self.height = attributes["height"] or 0.0
