#!/usr/bin/python3

import sys
sys.path.append("..")
from path_d import SVGPathCommand, SVGPathDefinition


def testSVGPathDefinition():
    #
    # Test path definition parsing
    #
    s = "M 10 10 m 1.0 2.0 L 2 1 l 1 3 H 1.0 h -1 V20 v -3 C 20 20, 40 20, 50 10 a 1   -2E2,\t3.0e1;4 5e1 6.0 7 z"
    print("Testing path definition parsing:\n\t\"{:s}\"".format(s))
    path = SVGPathDefinition(path=None, d=s, debug=True)
    points = path.getPoints()
    print("Parsed path points: {:s}".format(str(points)))


if __name__ == "__main__":
    testSVGPathDefinition()
