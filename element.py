#!/usr/bin/python3

from transform import SVGTransformList

#
# Generic XML element class
#
class SVGElement():
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
    # Return the current transformation matrix
    # of the current element including transformations of parent elements
    #
    def calculateCTM(self):
        # TODO
        return None

    #
    # Return the current transformation matrix
    # of the current element including transformations of parent elements
    #
    def getCTM(self):
        if self.ctm is None:
            self.calculateCTM()
        return self.ctm


if __name__ == "__main__":
    transform = 'matrix(1,2,3,4,5,6);rotate(45), translate(2.0 1e3)'
    print("Parsing element with attributes: transform=\"{:s}\"".format(transform))
    e = SVGElement(svg=None, parent=None, tag=None, attributes={"transform": transform})
    print(e)
    print(e.transform)
