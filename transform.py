#!/usr/bin/python3

# Use regular expressions for parsing
import re

rFloat = re.compile("([\+\-]*[0-9]+\.[0-9]+|[\+\-]*[0-9]+)")
rOps = re.compile("([a-zA-Z]+)[^\(\)]*\([^\(\)]*\)")
rArgs = re.compile("\(([^\(\)]*)\)")
rTransform = re.compile("(matrix|translate||scale|rotate|skewX|skewY)[ \t]*\(([\+\-0-9eE\.\,\; \t]*)\)")


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
            print("Parsed transformations: {:s}".format(str(mTransform)))
        mOps = rOps.findall(s)
        if debug:
            print("Validating operations: {:s}".format(str(mOps)))
        assert len(mOps) == len(mTransform)
        mArgs = rArgs.findall(s)
        if debug:
            print("Validating arguments: {:s}".format(str(mArgs)))
        assert len(mArgs) == len(mTransform)

        # Validate syntax
        for i in range(len(mTransform)):
            assert mOps[i] == mTransform[i][0]
            assert mArgs[i] == mTransform[i][1]

        # Parse
        for i in range(len(mTransform)):
            # Fallback
            t = "{:s}({:s})".format(mOps[i], mArgs[i])
            if mOps[i] == "rotate":
                t = SVGTransformRotate(mTransform[i], debug=debug)
            elif mOps[i] == "translate":
                t = SVGTransformTranslate(mTransform[i], debug=debug)
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
        assert len(m) == 2
        arg = m[1]
        assert arg != ""
        if debug:
            print("Parsing rotation angle: \"{:s}\"".format(arg))
        f = rFloat.findall(arg)
        assert len(f) == 1
        self.angle = float(f[0])
        if debug:
            print("Parsed rotation angle is {:.2f} degrees.".format(self.angle))

class SVGTransformTranslate():
    #
    # m is a regular expression match:
    #  first element = operation, in this case: "translate"
    #  second element = arguments, in this case: one or two translation parameters
    #   tx and, optionally, ty
    #
    def __init__(self, m, debug=False):
        arg = m[1]
        if debug:
            print("Parsing translation parameters: \"{:s}\"".format(arg))
        f = rFloat.findall(arg)
        assert len(f) > 1
        assert len(f) < 3
        self.tx = float(f[0])
        self.ty = 0.0
        if len(f) == 2:
            self.ty = float(f[1])
        if debug:
            print("Parsed translation vector is ({:.2f}, {:.2f}).".format(self.tx, self.ty))


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
    l = SVGTransformList(None, "rotate(+30);  translate( 20,-13.5 )\t, matrix(1e3 2 3 4 5 6)")
    result = str(l)
    print("Result: 'transform=\"{:s}\"'".format(result))
    assert result == "rotate(30)"

    print("Importing an illegal transformation list...")
    l = SVGTransformList(None, "test")
    result = str(l)
    print("Result: 'transform=\"{:s}\"'".format(result))
    assert result == "test"
