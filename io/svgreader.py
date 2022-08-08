#!/usr/bin/python3
#
# Library to enable scripting of simple operations on SVGs
# especially SVGs exported from OpenSCAD
#

import sys, os
import xml.sax

from ..dom.element import SVGElement
from ..dom.path import SVGPath


#
# The SVG class is a derivative of the XML parser handler class.
# It is capable of handling parser events and
# also stores relevant information.
#
class SVGReader(xml.sax.ContentHandler, SVGElement):
    tagsWithChildren = [
        "svg",
        "metadata",
        "rdf:rdf",
        "cc:work",
        "dc:format",
        "dc:title",
        "g"
        ]

    def __init__(self, filename=None, fromString=None, debug=False):
        SVGElement.__init__(self, svg=self, parent=None, tag="root", attributes={}, debug=debug)
        self.debug = debug
        self.clear()
        if not (filename is None):
            self.fromFile(filename)
            return
        if not (fromString is None):
            self.fromString(fromString)

    #
    # Load SVG from file
    #
    def fromFile(self, filename):
        self.clear()

        # create an XMLReader
        parser = xml.sax.make_parser()
        # turn off namepsaces
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)

        # override the default ContextHandler
        parser.setContentHandler(self)
        parser.parse(filename)

    #
    # Save to file
    #
    def toFile(self, filename):
        f = open(filename, "w")
        f.write(str(self))
        f.close()

    #
    # Load SVG from string
    #
    def fromString(self, s):
        # TODO: Workaround by writing to a file and loading it
        filename = ".svg.tmp"
        f = open(filename, "w")
        f.write(s)
        f.close()
        self.fromFile(filename)
        os.remove(filename)

    #
    # Reset XML parser
    #
    def clear(self):
        #super.__init__()
        # Cursor is currently inside how many tags with closing tags:
        self.descentLevel = 0
        # The list of parents at the momentary position during parsing
        self.currentParents = [self]

    #
    # XML parser callback: an element starts
    #
    def startElement(self, tag, attributes):
        # Determine current parent element
        lastIndex = len(self.currentParents)-1
        if lastIndex < 0:
            raise SyntaxError()
        parent = self.currentParents[lastIndex]

        # Evaluate tag
        tag = tag.lower()
        if tag == "path":
            # <path .../>
            e = SVGPath(svg=self, parent=parent, attributes=attributes, debug=self.debug)
        elif tag in self.tagsWithChildren:
            # Element with children, especially <g>...</g>
            #e = SVGGroup(svg=self, parent=parent, attributes=attributes, debug=self.debug)
            e = SVGElement(svg=self, parent=parent, tag=tag, attributes=attributes, debug=self.debug)
            self.currentParents.append(e)
            self.descentLevel += 1
            if self.debug:
                print("<{:s}>; expecting children; descending to level: {:d}".format(tag, self.descentLevel))
        else:
            # Generic element without children
            e = SVGElement(svg=self, parent=parent, tag=tag, attributes=attributes, debug=self.debug)

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
    # not relevant for SVGs
    #
    def characters(self, content):
        #print(content)
        return
