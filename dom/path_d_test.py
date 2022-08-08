#!/usr/bin/python3

import numpy as np

from .path_d import SVGPathCommand, SVGPathDefinition
from ..math.transform import SVGTransformList


def testParsing():
    s = "M 1.0 2.0"
    d = SVGPathDefinition(path=None, d=s, debug=True)
    assert(len(d) == 1)
    assert(len(d.getCommands()) == 1)
    assert(d.getCommands()[0].isMoveTo() == True)
    assert(len(d.getPoints()) == 1)
    assert(not (False in (d.getPoint(0) == [1.0, 2.0])))

    s = "M 10 10 m 1.0 2.0 L 2 1 1 3 H 1.0 h -1 V20 v -3 C 20 20, 40 20, 50 10 a 1   -2E2,\t3.0e1;4 5e1 6.0 7 z"
    d = SVGPathDefinition(path=None, d=s, debug=True)
    points = d.getPoints()
    print("Parsed path points: {:s}".format(str(points)))

    assert(len(d.getCommands()) == 11)
    assert(d.getCommand(0).isMoveTo() == True)
    assert(d.getCommand(0).isAbsolute() == True)
    assert(d.getCommand(0).isRelative() == False)
    assert(d.getCommand(0).isAbsolute() == True)
    assert(d.getCommand(1).isMoveTo() == True)
    assert(d.getCommand(2).isLineTo() == True)
    assert(d.getCommand(3).isLineTo() == True)
    assert(d.getCommand(4).isHorizontalLine() == True)
    assert(d.getCommand(5).isHorizontalLine() == True)
    assert(d.getCommand(6).isVerticalLine() == True)
    assert(d.getCommand(7).isVerticalLine() == True)
    assert(d.getCommand(8).isCubicBezier() == True)
    assert(d.getCommand(9).isArc() == True)
    assert(d.getCommand(10).isClosePath() == True)


def testSerialization():
    for s in ["M 1.0 2.0", "C 1.0 2.0 3.0 4.0 5.0 6.0"]:
        d = SVGPathDefinition(path=None, d=s, debug=True)
        assert(str(d) == s)


def testTransformation():
    # The path definition
    d = SVGPathDefinition(
            d = "M 5,6 L 3,4",
            debug=True
            )

    # The transformation
    transform = "translate(1, 2)"
    t = SVGTransformList(
            parseFromString=transform,
            debug=True
            )
    m = t.getSVGMatrix()

    # inplace==False
    assert(not (False in (d.getCommand(0).transform(m, inplace=False).getStartpoint() == [1, 2])))
    assert(not (False in (d.getCommand(0).transform(m, inplace=False).getEndpoint()   == [6, 8])))
    assert(not (False in (d.getCommand(1).transform(m, inplace=False).getStartpoint() == [6, 8])))
    assert(not (False in (d.getCommand(1).transform(m, inplace=False).getEndpoint()   == [4, 6])))

    # inplace==True
    d.transform(m, inplace=True)
    assert(not (False in (d.getCommand(0).getStartpoint() == [1, 2])))
    assert(not (False in (d.getCommand(0).getEndpoint()   == [6, 8])))
    assert(not (False in (d.getCommand(1).getStartpoint() == [6, 8])))
    assert(not (False in (d.getCommand(1).getEndpoint()   == [4, 6])))


def testSplitting():
    raise
