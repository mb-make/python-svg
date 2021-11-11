#!/usr/bin/python3
#
# Library to enable scripting of simple operations on SVGs
# especially SVGs exported from OpenSCAD
#

import xml.sax
from path import Path

#
# The SVG class is a derivative of the XML parser handler class.
# It is capable of handling parser events and
# also stores relevant information.
#
class SVG(xml.sax.ContentHandler):
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

        print("Parser found ${:d} paths.".format(len(svg.paths)))

    #
    # During parsing: returns the last encountered tag requiring a closing tag
    #
    def getCurrentParent(self):
        l = len(self.currentParents)
        if l == 0:
            return None
        else:
            return self.currentParents[l-1]

    #
    # XML parser callback: an element starts
    #
    def startElement(self, tag, attributes):
        #e = SVGElement(tag, attributes)
        if tag == "path":
            self.addPath(attributes)
        elif tag == "g":
            self.parserDescend(attributes)

    #
    # XML parser callback: an elements ends
    #
    def endElement(self, tag):
        if tag == "g":
            self.parserAscend()

    #
    # XML parser callback: tag content is read
    #
    def characters(self, content):
        #print(content)
        return

    def parserDescend(self, attributes):
        self.descentLevel += 1
        if self.debug:
            id = attributes["id"] if "id" in attributes else ""
            print("Begin group ", id, "; descending to level ", self.descentLevel)
        g = Group(attributes, debug=self.debug)
        self.currentParents.append(g)

    def parserAscend(self):
        if len(self.currentParents) > 0:
            self.currentParents.pop(len(self.currentParents)-1)
        self.descentLevel -= 1
        if self.debug:
            print("End group; ascending to level: ", self.descentLevel)

    def addPath(self, attributes):
        if self.debug:
            id = attributes["id"]
            print("Path id=", id)
        p = Path(attributes, self.currentParents, debug=self.debug)
        self.paths.append(p)
        if self.debug:
            print("Parents: ", len(p.parents), "; command count: ", p.cmdCount)
