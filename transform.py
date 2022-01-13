#!/usr/bin/python3

# Use regular expressions for parsing
import re

# Use NumPy for matrix operations (element transformations)
import numpy as np
from numpy import sin, cos, tan


# Comma before and after "E"
rFv1 = "[\+\-]*[0-9]+\.[0-9]+[eE]{1}[\+\-]*[0-9]+\.[0-9]+"
# Comma before "E"
rFv2 = "[\+\-]*[0-9]+\.[0-9]+[eE]{1}[\+\-]*[0-9]+"
# Comma after "E"; not supported
#rFv3 = "[\+\-]*[0-9]+[eE]{1}[\+\-]*[0-9]+\.[0-9]+"
# No comma neither before nor after "E"
rFv4 = "[\+\-]*[0-9]+[eE]{1}[\+\-]*[0-9]+"
# Comma, but no "E"
rFnoE = "[\+\-]*[0-9]+\.[0-9]+"
# No comma, no "E"
rFint = "[\+\-]*[0-9]+"
sNumeric = "("+rFv1+"|"+rFv2+"|"+rFv4+"|"+rFnoE+"|"+rFint+")"
rFloat = re.compile(sNumeric)
rOps = re.compile("([a-zA-Z]+)[^\(\)]*\([^\(\)]*\)")
rArgs = re.compile("\(([^\(\)]*)\)")
rTransform = re.compile("(matrix|translate||scale|rotate|skewX|skewY)[ \t]*\(([\+\-0-9eE\.\,\; \t]*)\)")


#
# The math implementing
#  https://www.w3.org/TR/SVG11/coords.html#InterfaceSVGMatrix
# See also:
#  https://www.scriptverse.academy/tutorials/python-matrix-multiplication.html
#
class SVGMatrix:
    def __init__(self, a=1, b=0, c=0, d=1, e=0, f=0, npMatrix=None, debug=False):
        self.debug = debug
        if npMatrix is None:
            self.matrix = np.array([[a, c, e], [b, d, f], [0, 0, 1]])
        else:
            self.matrix = npMatrix

    def getMatrix(self):
        return self.matrix

    def __str__(self):
        return str(self.matrix)

    def applyToPoint(self, point, debug=False):
        if debug or self.debug:
            print("Applying matrix \n{:s}\nto point{:s}\n".format(str(self.matrix), str(point)))
        pAbs = np.matmul(point, self.matrix)
        if debug or self.debug:
            print("Result: \n{:s}\n".format(str(pAbs)))
        return pAbs

    def applyToMatrix(self, matrix, debug=False):
        if debug or self.debug:
            print("Applying matrix \n{:s}\nto matrix\n{:s}\n".format(str(self.matrix), str(matrix)))
        if type(matrix) is SVGMatrix:
            matrix = matrix.getMatrix()
        mAbs = np.matmul(matrix, self.matrix)
        if debug or self.debug:
            print("Result: \n{:s}\n".format(str(mAbs)))
        return mAbs


#
# Class to store/handle SVG element transformations
#
class SVGTransformList():
    def __init__(self, element=None, parseFromString=None, debug=False):
        self.debug = debug
        self.element = element
        self.clear()
        if  not (parseFromString is None):
            self.parseFromString(parseFromString)

    def clear(self):
        self.transformations = []
        self.matrix = None

    def parseFromString(self, s):
        self.clear()
        # Use regular expression to separate individual transformations.
        # Transformations are separated by whitespace and/or comma.
        # Keep illegal lists/arguments.
        mTransform = rTransform.findall(s)
        if self.debug:
            print("Parsed transformations: {:s}".format(str(mTransform)))
        mOps = rOps.findall(s)
        if self.debug:
            print("Validating operations: {:s}".format(str(mOps)))
        assert len(mOps) == len(mTransform)
        mArgs = rArgs.findall(s)
        if self.debug:
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
                t = SVGTransformRotate(mTransform[i], debug=self.debug)
            elif mOps[i] == "translate":
                t = SVGTransformTranslate(mTransform[i], debug=self.debug)
            elif mOps[i] == "matrix":
                t = SVGTransformMatrix(mTransform[i], debug=self.debug)
            self.transformations += [t]

    #
    # Return the effective cumulative transformation
    # of all transformations in this list
    #
    def getTransformationMatrix(self):
        if self.matrix is None:
            self.calculateTransformationMatrix()
        return self.matrix

    #
    # Calculate the effective cumulative transformation
    # of all transformations in this list
    #
    def calculateTransformationMatrix(self):
        if len(self.transformations) == 0:
            # Identity matrix
            self.matrix = SVGMatrix()
            return
        self.matrix = self.transformations[0].getMatrix()
        if len(self.transformations) > 1:
            if self.debug:
                print("Calculating transformation matrix beginning with:")
                print(str(self.transformations[0])+"=")
                print(str(self.matrix))
            for t in self.transformations[1:]:
                individualTransformMatrix = t.getMatrix()
                if self.debug:
                    print("Apply:")
                    print(str(t)+"=")
                    print(str(individualTransformMatrix))
                self.matrix = individualTransformMatrix.applyToMatrix(self.matrix)
                if self.debug:
                    print("Result:")
                    print(str(self.matrix))

    # Export to string
    def __str__(self):
        ts = []
        for t in self.transformations:
            ts.append(str(t))
        return ", ".join(ts)


#
# Implement matrix, translate and rotate first
#
# Read more: https://www.w3.org/TR/SVG11/coords.html#TransformAttribute
#
class SVGTransformCommand:
    def getMatrix(self):
        return self.matrix


class SVGTransformRotate(SVGTransformCommand):
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
            print("Parsing rotation: \"{:s}\"".format(arg))
        f = rFloat.findall(arg)
        # rotate(angle [x y])
        assert len(f) in [1, 3]

        # Rotate by angle in degrees
        self.angle = float(f[0])

        # Rotate around (alternate) origin
        self.altOrigin = (len(f) == 3)
        self.x = float(f[1]) if self.altOrigin else 0.0
        self.y = float(f[2]) if self.altOrigin else 0.0

        self.matrix = SVGMatrix(
            a=cos(self.angle), c=-sin(self.angle), e=self.x,
            b=sin(self.angle), d= cos(self.angle), f=self.y
            )

        if debug:
            print("Parsed rotation around ({:.2f}, {:.2f}) by {:.2f} degrees.".format(self.x, self.y, self.angle))
            print("Yielded transformation matrix:\n{:s}".format(str(self.matrix)))

    def __str__(self):
        return "rotate({:.3f} {:.3f} {:.3f})".format(self.angle, self.x, self.y) if self.altOrigin else "rotate({:.3f})".format(self.angle)


class SVGTransformTranslate(SVGTransformCommand):
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

        self.matrix = SVGMatrix(
            a=1, c=0, e=self.tx,
            b=0, d=1, f=self.ty
            )

        if debug:
            print("Parsed translation vector is ({:.2f}, {:.2f}).".format(self.tx, self.ty))
            print("Yielded transformation matrix:\n{:s}".format(str(self.matrix)))

    def __str__(self):
        return "translate({:.3f}, {:.3f})".format(self.tx, self.ty)


class SVGTransformMatrix(SVGTransformCommand):
    #
    # m is a regular expression match:
    #  first element = operation, in this case: "matrix"
    #  second element = arguments, in this case: six matrix components a-f
    #
    def __init__(self, m, debug=False):
        arg = m[1]
        if debug:
            print("Parsing matrix components: \"{:s}\"".format(arg))
        f = rFloat.findall(arg)
        assert len(f) == 6
        self.f = []
        for i in range(6):
            self.f += [float(f[i])]

        self.matrix = SVGMatrix(
            a=self.f[0], c=self.f[1], e=self.f[2],
            b=self.f[3], d=self.f[4], f=self.f[5]
            )

        if debug:
            print("Parsed matrix is [[{:.2f}, {:.2f}, {:.2f}], [{:.2f}, {:.2f}, {:.2f}], [0, 0, 1]]."
                .format(self.f[0], self.f[1], self.f[2], self.f[3], self.f[4], self.f[5]))
            print("Yielded transformation matrix:\n{:s}".format(str(self.matrix)))

    def __str__(self):
        return "matrix({:s})".format(", ".join(["{:.3f}".format(x) for x in self.f]))


#
# Run some tests when executed standalone
#
if __name__ == "__main__":
    print("Importing an empty transformation list...")
    l = SVGTransformList(debug=True)
    result = str(l)
    print("Result: 'transform=\"{:s}\"'".format(result))
    assert result == ""

    #print("Transformation matrix:")
    l.getTransformationMatrix()

    transform = "rotate(+30);  translate( 20,-13.5 ) ,;.\t, matrix(1e3 0.2e1 3E-2 +4 5.1E+2 -6.0e-1)"
    print("Importing a valid transformation list: \"{:s}\"".format(transform))
    l = SVGTransformList(None, transform, debug=True)
    result = str(l)
    print("Result: 'transform=\"{:s}\"'".format(result))
    #assert result == "rotate(30)"

    #print("Transformation matrix:")
    l.getTransformationMatrix()

    #print("Importing an illegal transformation list...")
    #transform = "test ()"
    #l = SVGTransformList(None, transform)
    #result = str(l)
    #print("Result: 'transform=\"{:s}\"'".format(result))
    #assert result == "test"
