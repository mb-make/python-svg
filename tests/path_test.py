#!/usr/bin/python

import sys
sys.path.append("..")
from path import SVGPath
from path_d import SVGPathDefinition


def testParsing():
    p = SVGPath()
    assert(p.getD() is None)
    p = SVGPath(attributes = {"d": "M 1 1"})
    assert(type(p.getD()) is SVGPathDefinition)


def testSerialization():
    p = SVGPath(attributes = {"d": "M 2 1 L 5.2 3.4"})
    assert(type(p.getD()) is SVGPathDefinition)
    s = str(p)
    assert(s == "<path d=\"M 2.0 1.0 L 5.2 3.4\"/>")


def testSplitting():
    # TODO
    return True


def testInPlaceSplitting():
    # TODO
    return True


if __name__ == "__main__":
    testParsing()
    testSerialization()
    testSplitting()
    testInPlaceSplitting()
