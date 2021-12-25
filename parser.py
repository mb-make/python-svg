#!/usr/bin/python3
#
# Library to enable scripting of simple operations on SVGs
# especially SVGs exported from OpenSCAD
#

import xml.sax
from element import SVGElement
from path import SVGPath

#
# The SVG class is a derivative of the XML parser handler class.
# It is capable of handling parser events and
# also stores relevant information.
#
class SVGParser(xml.sax.ContentHandler):
    def __init__(self, filename=None, debug=False):
        self.debug = debug
        if filename is None:
            self.clear()
        else:
            self.load(filename)

    #
    # Reset object, delete all stored information
    #
    def clear(self):
        #super.__init__()
        # Cursor is currently inside how many tags with closing tags:
        self.descentLevel = 0
        # The list of parents at the momentary position during parsing
        self.currentParents = []
        # The tree of parsed elements
        self.elementTree = SVGElement()
        # A flattened list of all parsed elements
        self.elementList = []
        # A list of all the paths inside the SVG for convenient access
        self.paths = []

    #
    # Load SVG from file
    #
    def load(self, filename):
        self.clear()

        # create an XMLReader
        parser = xml.sax.make_parser()
        # turn off namepsaces
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)

        # override the default ContextHandler
        parser.setContentHandler(self)
        parser.parse(filename)

        if self.debug:
            print("Parser found {:d} paths.".format(len(self.paths)))

    #
    # XML parser callback: an element starts
    #
    def startElement(self, tag, attributes):
        # Determine current parent element
        parent = self.elementTree
        l = len(self.currentParents)
        if l > 0:
            parent = self.currentParents[l-1]

        # Evaluate tag
        tag = tag.lower()
        if tag == "path":
            e = SVGPath(svg=self, parent=parent, attributes=attributes, debug=self.debug)
            self.paths.append(e)
        elif tag == "g":
            #e = SVGGroup(svg=self, parent=parent, attributes=attributes, debug=self.debug)
            e = SVGElement(svg=self, parent=parent, tag="g", attributes=attributes, debug=self.debug)
            self.currentParents.append(e)
            self.descentLevel += 1
            if self.debug:
                print("Begin group; descending to level: ", self.descentLevel)
        else:
            e = SVGElement(svg=self, parent=parent, tag=tag, attributes=attributes, debug=self.debug)

        self.elementList.append(e)
        parent.children.append(e)

    #
    # XML parser callback: an elements ends
    #
    def endElement(self, tag):
        if tag == "g":
            if len(self.currentParents) > 0:
                self.currentParents.pop(len(self.currentParents)-1)
            self.descentLevel -= 1
            if self.debug:
                print("End group; ascending to level: ", self.descentLevel)

    #
    # XML parser callback: tag content is read
    #
    def characters(self, content):
        #print(content)
        return

    def getElementList(self):
        return self.elementList

    def getPaths(self):
        return self.paths


# Self-test
if __name__ == "__main__":
    f = SVGParser(filename="tests/import-export/test.svg", debug=True)
