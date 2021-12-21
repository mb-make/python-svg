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

sSVGPathSegment = "|".join([sA,sC,sQS,sMLT,sHV,sZ])
#print(sSVGPathSegment)
rSVGPathSegment = re.compile(sSVGPathSegment)
#print(rSVGPathSegment)


#
# Any single atomic command within an SVG path definition ("d" attribute)
#
class SVGPathSegment:
    #
    # Parse path segment from regular expression match
    #
    def __init__(self, match, debug=False):
        # Strip empty array elements (TODO: enhance regular expression)
        match = list(match)
        while (len(match) > 0) and (match[0] == ""):
            match.pop(0)
        while (len(match) > 0) and (match[len(match)-1] == ""):
            match.pop(len(match)-1)
        assert len(match) >= 1
        self.m = [match[0]]
        if len(match) > 1:
            for m in match[1:]:
                self.m.append(float(m))
        #if self.debug:
        #    print(self.m)

    def isMoveTo(self):
        return self.m[0].upper() == "M"

    def isLineTo(self):
        return self.m[0].upper() == "L"

    def isClosePath(self):
        return self.m[0].upper() == "Z"

    def isRelative(self):
        return not self.isAbsolute()

    def isAbsolute(self):
        return self.m[0] == self.m[0].upper()

    def getX(self):
        return self.m[1]

    def getY(self):
        return self.m[2]

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

        #print(rSVGPathSegment.match(s).groups())
        results = rSVGPathSegment.findall(d)
        if self.debug:
            print("Parsing path definition attribute: \"{:s}\"".format(d))
            #print("Intermediate results: {:s}".format(str(results)))
        for match in results:
            self.segments.append(SVGPathSegment(match, debug=self.debug))
        if self.debug:
            print("Results: {:s}".format(str([str(seg) for seg in self.segments])))
        #
        # TODO: Verification
        #  1. The number of characters must be equal in source and parsed content.
        #  2. The number of numeric values must be equal in source and parsed content.
        #  3. Characters other than the above segment commands are forbidden.
        #

    #
    # Return the number of segments in self path description
    #
    def __len__(self):
        return len(self.segments)

    #
    # Return the relative cursor coordinates,
    # optionally at the indexed segment
    #
    def getSegmentCoordinates(self, index=None):
        coordinates = []
        cursorX, cursorY = 0.00, 0.00
        for i in range(len(self.segments)):
            if self.debug:
                print("Cursor at relative ({:.2f},{:.2f})".format(cursorX, cursorY))
            coordinates.append([cursorX, cursorY])
            segment = self.segments[i]
            if self.debug:
                print(str(segment))
            if segment.isClosePath():
                cursorX, cursorY = 0.00, 0.00
            elif segment.isAbsolute():
                if segment.isMoveTo() or segment.isLineTo():
                    cursorX, cursorY = segment.getX(), segment.getY()
            elif segment.isRelative():
                if segment.isMoveTo() or segment.isLineTo():
                    cursorX += segment.getX()
                    cursorY += segment.getY()
            if self.debug:
                print("Cursor at relative ({:.2f},{:.2f})".format(cursorX, cursorY))
        if index is None:
            return coordinates
        return coordinates[index]

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
    d = "M 10 10 C 20 20, 40 20, 50 10 a 1   -2E2,\t3.0e1;4 5e1 6.0 7 M 2 1 z"
    D = SVGPathDefinition(path=None, d=d, debug=True)
    P = D.getSegmentCoordinates()
    print("Parsed path points: {:s}".format(str(P)))
