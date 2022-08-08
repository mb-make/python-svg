#!/usr/bin/python3

from ..math.transform import SVGTransformList, SVGMatrix
from .xmlelement import XMLElement


#
# Extends the generic XML element by SVG-specific methods
#
# Transformations and current transfomration matrix (CTM)
# are imlemented here, since they are the same for all elements.
#
# Every SVG element must implement the following
# methods, defining the element's bounding box
# in absolute coordinates:
#  - getMinX()
#  - getMaxX()
#  - getMinY()
#  - getMaxY()
#
# The class SVGBoundingBox can be used as parent class
# to fulfill that.
#
class SVGElement(XMLElement):
    #
    # An element is initialized by setting the XML tag name and attributes.
    # Additionally the containing SVG is referenced.
    #
    def __init__(self, svg=None, parent=None, tag="element", attributes={}, debug=False):
        XMLElement.__init__(self, svg, parent, tag, attributes, debug)
        # Increase speed: only parse if necessary
        #self.parseTransform()
        self.parsedTransform = None
        # Current transformation matrix for this element and it's children
        # (this matrix already includes the transformations of parent elements)
        self.ctm = None

    #
    # Parse the coordinates transformation attribute
    #
    def parseTransform(self):
        if ((not (self.attributes is None)) and ("transform" in self.attributes.keys())):
            self.parsedTransform = SVGTransformList(parseFromString=self.attributes["transform"], debug=self.debug)
            return
        # Error; use empty transformation list
        self.parsedTransform = SVGTransformList()

    #
    # Return the transformation list of the current element
    #
    def getTransform(self):
        if self.parsedTransform is None:
            self.parseTransform()
        return self.parsedTransform

    #
    # Return the transformation matrix
    # relative to the parent element
    # as NumPy matrix
    #
    def getMatrix(self):
        return self.getSVGMatrix().getMatrix()

    #
    # Return the transformation matrix
    # relative to the parent element
    # as SVGMatrix object
    #
    def getSVGMatrix(self):
        return self.getTransform().getSVGMatrix()

    #
    # Return the current transformation matrix (CTM)
    # of the current element including transformations of parent elements
    # as SVGMatrix
    #
    def calculateCTM(self):
        m = self.getSVGMatrix()
        if self.parentElement is None:
            self.ctm = m
            return
        parentCTM = self.parentElement.getCTM()
        self.ctm = m.applyToMatrix(parentCTM)

    #
    # Return the current transformation matrix
    # of the current element including transformations of parent elements
    #
    def getCTM(self):
        if self.ctm is None:
            self.calculateCTM()
        if self.debug:
            print("<{:s}>: ctm =".format(self.getTag()))
            print(str(self.ctm))
        return self.ctm
