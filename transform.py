#!/usr/bin/python3

# Use regular expressions for parsing
import re


#
# Class to store/handle SVG element transformations
#
class SVGTransformList():
    def __init__(self, element, parseFromString=None):
        self.element = element
        self.clear()
        if  not (parseFromString is None):
            self.parseFromString(parseFromString)

    def clear(self):
        self.transformations = []

    def parseFromString(self, s):
        self.clear()
        # Use regular expression to separate individual transformations.
        # Transformations are separated by whitespace and/or comma.
        r = re.compile("[a-zA-Z]+")
        m = r.match("test")

    # Export to string
    def __str__(self):
        ts = []
        for t in self.transformations:
            ts.append(str(t))
        return ",".join(ts)


#
# Implement matrix, translate and rotate first
#
# Read more: https://www.w3.org/TR/SVG11/coords.html#TransformAttribute
#

class SVGTransformRotate():
    def __init__(self, s):
        a = s.find("(")
        b = s.find(")", a)


#
# Run some tests when executed standalone
#
if __name__ == "__main__":
    empty = SVGTransformList()
    print("Empty transformation list: 'transform=\"{:s}\"'".format(str(empty)))
