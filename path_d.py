#!/usr/bin/python
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
sHV = begin + whitespace + "([hHvH]{1})" + (whitespace + sNumeric) + end

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
        self.m = match
        if debug:
            print(match)

    #
    # Convert segment back to string
    #
    def __str__(self):
        return " ".join(self.m)


#
# The "d" attribute of any path element within an SVG
#
class SVGPathDefinition:
    #
    # initialize path data
    #
    def __init__(self, s=None, debug=False):
        self.debug = debug

        # initialize empty
        self.segments = []
        if s is None:
            return

        #print(rSVGPathSegment.match(s).groups())
        results = rSVGPathSegment.findall(s)
        if self.debug:
            print("Parsing string: {:s}".format(s))
            print("Intermediate results: {:s}".format(str(results)))
        for match in results:
            self.segments.append(SVGPathSegment(match, debug=self.debug))
        if self.debug:
            print("Results: {:s}".format(str([str(seg) for seg in self.segments])))

    #
    # return number of segments in self path description
    #
    def __len__(self):
        return len(self.segments)

    #
    # export as string
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
    SVGPathDefinition(d, debug=True)
