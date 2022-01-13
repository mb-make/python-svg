#!/usr/bin/python3
#
# Library to enable scripting of simple operations on SVGs
# especially SVGs exported from OpenSCAD
#

import sys
import xml.sax
from element import SVGElement
from path import SVGPath

#
# The SVG class is a derivative of the XML parser handler class.
# It is capable of handling parser events and
# also stores relevant information.
#
class SVGParser(xml.sax.ContentHandler):
    tagsWithChildren = [
        "svg",
        "metadata",
        "rdf:rdf",
        "cc:work",
        "dc:format",
        "dc:title",
        "g"
        ]

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
        elif tag.lower() in self.tagsWithChildren:
            #e = SVGGroup(svg=self, parent=parent, attributes=attributes, debug=self.debug)
            e = SVGElement(svg=self, parent=parent, tag=tag, attributes=attributes, debug=self.debug)
            self.currentParents.append(e)
            self.descentLevel += 1
            if self.debug:
                print("<{:s}>; expecting children; descending to level: {:d}".format(tag, self.descentLevel))
        else:
            e = SVGElement(svg=self, parent=parent, tag=tag, attributes=attributes, debug=self.debug)

        self.elementList.append(e)
        parent.children.append(e)

    #
    # XML parser callback: an elements ends
    #
    def endElement(self, tag):
        if tag.lower() in self.tagsWithChildren:
            if len(self.currentParents) > 0:
                lastParent = self.currentParents.pop(len(self.currentParents)-1)
            self.descentLevel -= 1
            if self.debug:
                print("</{:s}>; ascending to level: {:d}".format(tag, self.descentLevel))

            # Ascending above root element indicates a parser of SVG error
            if self.descentLevel < 0:
                print("Error: Encountered more closing tags than were opened.")
                sys.exit(1)

            # Verify, the current parent element is what we expect it to be
            if lastParent.getTag().lower() != tag.lower():
                print("Error: Expected closing tag for {:s}, but got closing tag for {:s}.".format(lastParent.getTag(), tag))
                sys.exit(1)

    #
    # XML parser callback: tag content is read
    #
    def characters(self, content):
        #print(content)
        return

    def getSVG(self):
        return self.elementTree

    def getElementList(self):
        return self.elementList

    def getPaths(self):
        return self.paths


# Self-test
if __name__ == "__main__":
    f = SVGParser(filename="tests/import-export/test.svg", debug=True)
