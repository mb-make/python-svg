#!/usr/bin/python

import sys
sys.path.append("..")
from path import SVGPath
from path_d import SVGPathDefinition
from bbox import SVGBoundingBox


def testParsing():
    p = SVGPath()
    assert(len(p) == 0)
    assert(p.getD() is None)

    p = SVGPath(attributes = {"d": "M 1 1"})
    assert(len(p) == 1)
    assert(type(p.getD()) is SVGPathDefinition)
    assert(p.getD().getCommand(0).isMoveTo() == True)


def testSerialization():
    p = SVGPath(attributes = {"d": "M 2 1 L 5.2 3.4"})
    assert(len(p) == 2)
    assert(type(p.getD()) is SVGPathDefinition)
    assert(str(p) == "<path d=\"M 2.0 1.0 L 5.2 3.4\"/>")


def testBoundingBox():
    p = SVGPath(attributes = {"d": "M 1 2 L 3 4"})
    b = SVGBoundingBox(
            minX=1,
            minY=2,
            maxX=3,
            maxY=4
            )
    assert(b.containsElement(p) == True)
    assert(p.containsElement(b) == True)


def testSplitting():
    # TODO
    raise


def testInPlaceSplitting():
    # TODO
    raise


if __name__ == "__main__":
    testParsing()
    testSerialization()
    testSplitting()
    testInPlaceSplitting()
