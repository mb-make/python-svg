#!/usr/bin/python

from .path import SVGPath
from .path_d import SVGPathDefinition
from ..selecting.bbox import SVGBoundingBox


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


def testMetrics():
    p = SVGPath(attributes = {"d": "M 1 2 L 3 5"})
    assert(p.getWidth() == 2)
    assert(p.getHeight() == 3)
    assert(len(p) == 2)


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
    assert(b.touchesElement(p) == True)
    assert(p.touchesElement(b) == True)

    b = SVGBoundingBox(
            minX=2,
            minY=3,
            maxX=4,
            maxY=5
            )
    assert(b.containsElement(p) == False)
    assert(p.containsElement(b) == False)
    assert(b.touchesElement(p) == True)
    assert(p.touchesElement(b) == True)

    # TODO: quadratic, ellipsoid, arc, etc.


def testSplitting():
    # TODO
    raise


def testInPlaceSplitting():
    # TODO
    raise
