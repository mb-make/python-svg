#!/usr/bin/python3

from transform import SVGTransformList, SVGMatrix

#
# Generic XML element and element parent class
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
class SVGElement():
    #
    # An element is initialized by setting the XML tag name and attributes.
    # Additionally the containing SVG is referenced.
    #
    def __init__(self, svg=None, parent=None, tag=None, attributes=None, debug=False):
        self.debug = debug
        self.parentSVG = svg
        self.parentElement = parent
        self.tag = tag
        self.attributes = attributes
        self.children = []
        # Increase speed: only parse if necessary
        #self.parseTransform()
        self.transform = None
        # Current transformation matrix for this element and it's children
        # (this matrix already includes the transformations of parent elements)
        self.ctm = None

    def getTag(self):
        return self.tag

    def getAttributes(self):
        return self.attributes

    def getAttribute(self, key):
        if key in self.attributes.keys():
            return self.attributes[key]
        return None

    def setAttribute(self, key, value):
        if self.attributes is None:
            self.attributes = {}
        self.attributes[key] = value

    def deleteAttribute(self, key):
        self.attributes.pop(key)

    def getParentSVG(self):
        return self.parentSVG

    def getParentElement(self):
        return self.parentElement

    def getChildren(self):
        return self.children

    #
    # Parse the coordinates transformation attribute
    #
    def parseTransform(self):
        if ((not (self.attributes is None)) and ("transform" in self.attributes.keys())):
            self.transform = SVGTransformList(parseFromString=self.attributes["transform"], debug=self.debug)
            return
        # Error; use empty transformation list
        self.transform = SVGTransformList()

    #
    # Return the transformation list of the current element
    #
    def getTransform(self):
        if self.transform is None:
            self.parseTransform()
        return self.transform

    #
    # Return the current transformation matrix (CTM)
    # of the current element including transformations of parent elements
    # as SVGMatrix
    #
    def calculateCTM(self):
        transform = self.getTransform()
        myMatrix = transform.getTransformationMatrix()
        if self.parentElement is None:
            self.ctm = myMatrix
            return
        parentCTM = self.parentElement.getCTM()
        self.ctm = myMatrix.applyToMatrix(parentCTM)

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


if __name__ == "__main__":
    transform = 'matrix(1,2,3,4,5,6);rotate(45), translate(2.0 1e3)'
    print("Parsing element with attributes: transform=\"{:s}\"".format(transform))
    e = SVGElement(
            svg=None,
            parent=None,
            tag=None,
            attributes={"transform": transform},
            debug=True
            )
    #print(e)
    t = e.getTransform()
    #print(str(t))
    m = t.getTransformationMatrix()
    #print(str(m))
