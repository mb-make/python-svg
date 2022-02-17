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
    def __init__(self, svg=None, parent=None, tag="element", attributes={}, debug=False):
        self.debug = debug
        self.parentSVG = svg
        self.parentElement = parent
        self.tag = tag
        self.attributes = dict(attributes)
        self.children = []
        # Increase speed: only parse if necessary
        #self.parseTransform()
        self.parsedTransform = None
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

    def getChild(self, index):
        return self.children[index]

    #
    # Find the element with the specified ID
    # See also: https://www.w3schools.com/jsref/met_document_getelementbyid.asp
    #
    def getElementById(self, id, depth=0):
        if depth > 100:
            print("Error: Reached maximum recursion depth looking for element by ID.")
            return None
        if ((self.getAttribute("id") or "") == id):
            return self
        for child in self.getChildren():
            e = child.getElementById(id, depth+1)
            if (e != None):
                return e
        return None

    #
    # Return an array of elements with the given class
    # See also: https://www.w3schools.com/jsref/met_document_getelementsbyclassname.asp
    #
    def getElementsByClassName(self, c):
        # TODO
        return []

    #
    # Return an array of elements with the given name
    # See also: https://www.w3schools.com/jsref/met_doc_getelementsbyname.asp
    #
    def getElementsByName(self, name):
        # TODO
        return []

    #
    # Return an array of elements with the given tag name
    # See also: https://www.w3schools.com/jsref/met_document_getelementsbytagname.asp
    #
    def getElementsByTagName(self, tag):
        # TODO
        return []

    #
    # Stringify element
    #
    def __str__(self):
        s = "<{:s}".format(self.tag)
        for key in self.attributes.keys():
            s += " {:s}=".format(key)
            value = self.attributes[key]
            t = type(value)
            if t == int:
                s += "{:d}".format(value)
            else:
                s += "\"{:s}\"".format(str(value))
        selfClosing = (len(self.children) == 0)
        if selfClosing:
            s += "/>"
        else:
            s += ">"
            for child in self.children:
                s += str(child)
            s += "</{:s}>".format(self.tag)
        return s

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
