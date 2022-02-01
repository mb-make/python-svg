#!/usr/bin/python3

from element import SVGElement


#
# Defines a rectangular box and implements methods
# to test whether other elements are touched or contained
#
class SVGBoundingBox(SVGElement):
    def __init__(self, fromElement=None, id=None, minX=None, minY=None, maxX=None, maxY=None):
        if not (fromElement is None):
            self.id = fromElement.attributes["id"]
            self.minX = fromElement.getMinX()
            self.maxX = fromElement.getMaxX()
            self.minY = fromElement.getMinY()
            self.maxY = fromElement.getMaxY()
        if not (id is None):
            self.id = id
        if not (minX is None):
            self.minX = minX
        if not (minY is None):
            self.minY = minY
        if not (maxX is None):
            self.maxX = maxX
        if not (maxY is None):
            self.maxY = maxY

    #
    # Return true, if the point lies inside the bbox,
    # return false otherwise
    #
    def containsPoint(self, x, y):
        if x < self.minX:
            return False
        if x > self.maxX:
            return False
        if y < self.minY:
            return False
        if y > self.maxY:
            return False

    #
    # Return true, if the target element is completely enclosed by the bbox,
    # return false otherwise
    #
    def containsElement(self, element):
        if element.getMinX() < self.minX:
            return False
        if element.getMaxX() > self.maxX:
            return False
        if element.getMinY() < self.minY:
            return False
        if element.getMaxY() > self.maxY:
            return False
        return True

    #
    # Return true, if the target element lies inside the bbox at least partially
    # return false otherwise
    #
    def touchesElement(self, element):
        # TODO: if isPath(element)
        if self.containsPoint(element.getMinX(), element.getMinY()):
            return True
        if self.containsPoint(element.getMinX(), element.getMaxY()):
            return True
        if self.containsPoint(element.getMaxX(), element.getMaxY()):
            return True
        if self.containsPoint(element.getMaxX(), element.getMinY()):
            return True
        return False
