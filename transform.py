#!/usr/bin/python3

# Use regular expressions for parsing
import re

rFloat = re.compile("([0-9]+|[0-9]+\.[0-9]+)")
rOps = re.compile("([a-zA-Z]+)")
rArgs = re.compile("\(([^\(\)]*)\)")
rTransform = re.compile("(matrix|translate||scale|rotate|skewX|skewY)[ \t]*\(([0-9\.\,\; \t]*)\)")


#
# Class to store/handle SVG element transformations
#
class SVGTransformList():
    def __init__(self, element=None, parseFromString=None):
        self.element = element
        self.clear()
        if  not (parseFromString is None):
            self.parseFromString(parseFromString)

    def clear(self):
        self.transformations = []

    def parseFromString(self, s, debug=True):
        self.clear()
        # Use regular expression to separate individual transformations.
        # Transformations are separated by whitespace and/or comma.
        # Keep illegal lists/arguments.
        mTransform = rTransform.findall(s)
        if debug:
            print(mTransform)
        mOps = rOps.findall(s)
        if debug:
            print(mOps)
        mArgs = rArgs.findall(s)
        if debug:
            print(mArgs)

        # Validate syntax
        assert len(mOps) == len(mTransform)
        for i in range(len(mTransform)):
            assert mOps[i] == mTransform[i][0]
            assert mArgs[i] == mTransform[i][1]

        # Parse
        for i in range(len(mTransform)):
            # Fallback
            t = "{:s}({:s})".format(mOps[i], mArgs[i])
            if mOps[i] == "rotate":
                t = SVGTransformRotate(mTransform[i], debug=debug)
            self.transformations += [t]

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
    #
    # m is a regular expression match:
    #  first element = operation, in this case: "rotate"
    #  second element = argument, in this case: rotation angle in degrees
    #
    def __init__(self, m, debug=False):
        arg = m[1]
        if debug:
            print("Debug: Parsing rotation angle: {:s}".format(arg))
        self.angle = float(rFloat.match(arg).group())
        if debug:
            print("Debug: Rotation angle is {:.2f} degrees.".format(self.angle))


#
# Run some tests when executed standalone
#
if __name__ == "__main__":
    print("Importing an empty transformation list...")
    l = SVGTransformList()
    result = str(l)
    print("Result: 'transform=\"{:s}\"'".format(result))
    assert result == ""

    print("Importing a valid transformation list...")
    l = SVGTransformList(None, "rotate(30);  translate(20,13.5)\t, matrix(1 2 3 4 5 6)")
    result = str(l)
    print("Result: 'transform=\"{:s}\"'".format(result))
    assert result == "rotate(30)"

    print("Importing an illegal transformation list...")
    l = SVGTransformList(None, "test")
    result = str(l)
    print("Result: 'transform=\"{:s}\"'".format(result))
    assert result == "test"
