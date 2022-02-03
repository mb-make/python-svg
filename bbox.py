#!/usr/bin/python3

from element import SVGElement


#
# Defines a rectangular box and implements methods
# to test whether other elements are touched or contained
#
class SVGBoundingBox(SVGElement):
    def __init__(self, fromElement=None, minX=None, minY=None, maxX=None, maxY=None):
        if not (fromElement is None):
            self.minX = fromElement.getMinX()
            self.maxX = fromElement.getMaxX()
            self.minY = fromElement.getMinY()
            self.maxY = fromElement.getMaxY()
        if not (minX is None):
            self.minX = minX
        if not (minY is None):
            self.minY = minY
        if not (maxX is None):
            self.maxX = maxX
        if not (maxY is None):
            self.maxY = maxY

    def getMinX(self):
        return self.minX

    def getMinY(self):
        return self.minY

    def getMaxX(self):
        return self.maxX

    def getMaxY(self):
        return self.maxY

    #
    # Return true, if the point lies inside the bbox,
    # return false otherwise
    #
    def containsPoint(self, x, y):
        if x < self.getMinX():
            return False
        if x > self.getMaxX():
            return False
        if y < self.getMinY():
            return False
        if y > self.getMaxY():
            return False
        return True

    #
    # Return true, if the target element is completely enclosed by the bbox,
    # return false otherwise
    #
    def containsElement(self, element):
        if element.getMinX() < self.getMinX():
            return False
        if element.getMaxX() > self.getMaxX():
            return False
        if element.getMinY() < self.getMinY():
            return False
        if element.getMaxY() > self.getMaxY():
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
