#!/usr/bin/python3
#
# Library to handle SVG path descriptions and segments
# https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths
#

import re
from transform import sNumeric


#
# Compile regular expression for parsing
#
whitespace = "[ \t\,\:\;\(\)]*"
# uncaptured group
begin = "" #"(?:"
end = "" #")"

# Arc:
# A rx ry x-axis-rotation large-arc-flag sweep-flag x y
# a rx ry x-axis-rotation large-arc-flag sweep-flag dx dy
sA = begin + whitespace + "([aA]{1})" + (whitespace + sNumeric)*7 + end

# Bezier curve:
#  C x1 y1, x2 y2, x y
#  c dx1 dy1, dx2 dy2, dx dy
sC = begin + whitespace + "([cC]{1})" + (whitespace + sNumeric)*6 + end

# Quadratic curve:
#  Q x1 y1, x y
#  q dx1 dy1, dx dy
# Append Bezier (smooth):
#  S x2 y2, x y
#  s dx2 dy2, dx dy
sQS = begin + whitespace + "([qQsS]{1})" + (whitespace + sNumeric)*4 + end

# MoveTo:
#  M x y
#  m dx dy
# LineTo:
#  L x y
#  l dx dy
# Append quadratic Bezier:
#  T x y
#  t dx dy
sMLT = begin + whitespace + "([mMlLtT]{1})" + (whitespace + sNumeric)*2 + end

# Horizontal line:
#  H x
#  h dx
# Vertical line:
#  V y
#  v dy
sHV = begin + whitespace + "([hHvV]{1})" + (whitespace + sNumeric) + end

# Close path:
#  Z
#  z
sZ = begin + whitespace + "([zZ]{1})" + end

sSVGPathCommand = "|".join([sA,sC,sQS,sMLT,sHV,sZ])
#print(sSVGPathCommand)
rSVGPathCommand = re.compile(sSVGPathCommand)
#print(rSVGPathCommand)


#
# Any single atomic command within an SVG path definition ("d" attribute)
#
class SVGPathCommand:
    #
    # Parse path segment from regular expression match
    #
    def __init__(self, command, startpoint=(0,0), debug=False):
        self.debug = debug

        command = list(command)

        # Strip empty array elements at beginning and end of the list
        while (len(command) > 0) and (command[0] == ""):
            command.pop(0)
        while (len(command) > 0) and (command[len(command)-1] == ""):
            command.pop(len(command)-1)
        assert len(command) >= 1

        # First list element: Command
        self.m = [command[0]]
        # Following list elements: float values
        if len(command) > 1:
            for m in command[1:]:
                self.m.append(float(m))
        if self.debug:
            print("Parsing path command: {:s}".format(str(self.m)))

        self.startpoint = startpoint
        self.endpoint = None

    def isMoveTo(self):
        return self.m[0].upper() == "M"

    def isLineTo(self):
        return self.m[0].upper() == "L"

    def isHorizontalLine(self):
        return self.m[0].upper() == "H"

    def isVerticalLine(self):
        return self.m[0].upper() == "V"

    def isClosePath(self):
        return self.m[0].upper() == "Z"

    def isCubicBezier(self):
        return self.m[0].upper() == "C"

    def isMultipleCubicBeziers(self):
        return self.m[0].upper() == "S"

    def isQuadraticBezier(self):
        return self.m[0].upper() == "Q"

    def isMultipleQuadraticBeziers(self):
        return self.m[0].upper() == "T"

    def isArc(self):
        return self.m[0].upper() == "A"

    def isRelative(self):
        return not self.isAbsolute()

    def isAbsolute(self):
        return self.m[0] == self.m[0].upper()

    def getStartpoint(self):
        return self.startpoint

    def getEndpoint(self):
        if not (self.endpoint is None):
            return self.endpoint

        x = self.startpoint[0]
        y = self.startpoint[1]
        if self.debug:
            print("Cursor is at ({:.2f},{:.2f}).".format(x, y))

        if self.isMoveTo() or self.isLineTo() or self.isMultipleQuadraticBeziers():
            x = self.m[1]
            y = self.m[2]
        elif self.isHorizontalLine():
            x = self.m[1]
            y = self.startpoint[1]
        elif self.isVerticalLine():
            x = self.startpoint[0]
            y = self.m[1]
        elif self.isClosePath():
            x = 0.0
            y = 0.0
        elif self.isCubicBezier():
            x = self.m[5]
            y = self.m[6]
        elif self.isMultipleCubicBeziers() or self.isQuadraticBezier():
            x = self.m[3]
            y = self.m[4]
        elif self.isArc():
            x = self.m[6]
            y = self.m[7]
        else:
            print("Error: Path command not recognized.")

        if self.isRelative() and (not self.isClosePath()):
            if self.debug:
                print("Path command uses relative coordinates.")
            if not self.isVerticalLine():
                x += self.startpoint[0]
            if not self.isHorizontalLine():
                y += self.startpoint[1]

        self.endpoint = (x, y)

        if self.debug:
            print("Cursor is at ({:.2f},{:.2f}).".format(x, y))

        return self.endpoint

    #
    # Convert segment back to string
    #
    def __str__(self):
        return " ".join([str(e) for e in self.m])


#
# Loads, parsees and enables handling of paths
# as defined in a path's "d" attribute
#
class SVGPathDefinition:
    #
    # initialize path data
    #
    def __init__(self, path=None, d=None, debug=False):
        self.path = path
        self.debug = debug

        # initialize empty
        self.segments = []
        if d is None:
            return

        #print(rSVGPathCommand.match(s).groups())
        results = rSVGPathCommand.findall(d)
        if self.debug:
            print("Parsing path definition: \"{:s}\"".format(d))
            #print("Intermediate results: {:s}".format(str(results)))

        # Walk along the path and store the points
        cursor = (0.0, 0.0)
        self.points = [cursor]
        for match in results:
            cmd = SVGPathCommand(command=match, startpoint=cursor, debug=self.debug)
            self.segments.append(cmd)
            cursor = cmd.getEndpoint()
            self.points.append(cursor)

        #
        # TODO: Verification
        #  1. The number of characters must be equal in source and parsed content.
        #  2. The number of numeric values must be equal in source and parsed content.
        #  3. Characters other than the above segment commands are forbidden.
        #

        if self.debug:
            print("Results: {:s}".format(str([str(seg) for seg in self.segments])))
            print("Points: {:s}".format(str(self.points)))

    #
    # Return the number of segments in self path description
    #
    def __len__(self):
        return len(self.segments)

    #
    # Return the path's points
    # relative to the path's origin
    #
    def getPoints(self):
        return self.points

    #
    # Export as string
    #
    def __str__(self):
        return " ".join([str(segment) for segment in self.segments])

    #
    # min/max functions
    #
    def minX(self):
        result = None
        for segment in self.segments:
            if "ML".find(segment.type) > -1:
                if (result == None) or (segment.x < result):
                    result = segment.x
        return result

    def maxX(self):
        result = None
        for segment in self.segments:
            if "ML".find(segment.type) > -1:
                if (result == None) or (segment.x > result):
                    result = segment.x
        return result

    def minY(self):
        result = None
        for segment in self.segments:
            if "ML".find(segment.type) > -1:
                if (result == None) or (segment.y < result):
                    result = segment.y
        return result

    def maxY(self):
        result = None
        for segment in self.segments:
            if "ML".find(segment.type) > -1:
                if (result == None) or (segment.y > result):
                    result = segment.y
        return result


if __name__ == "__main__":
    s = "M 10 10 m 1.0 2.0 C 20 20, 40 20, 50 10 a 1   -2E2,\t3.0e1;4 5e1 6.0 7 M 2 1 z"
    path = SVGPathDefinition(path=None, d=s, debug=True)
    points = D.getPoints()
    #print("Parsed path points: {:s}".format(str(points)))
