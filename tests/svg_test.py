#!/usr/bin/python3

import sys, os
sys.path.append("..")
from svg import SVGParser
from element import SVGElement


def testFileImport():
    filename = "tests/import-export/test.svg"
    f = SVGParser(filename=filename, debug=True)
    e = f.getSVG()
    assert(not (e is None))
    assert(type(e) is SVGElement)
    assert(e.getTag().lower() == "svg")


def testFromString():
    sIn = "<svg><rect/></svg>"
    p = SVGParser(fromString=sIn)
    dom = p.getSVG()
    assert(dom.getTag() == "svg")
    assert(len(dom.getChildren()) == 1)
    assert(dom.getChild(0).getTag() == "rect")


def testSerialization():
    filename = "tests/import-export/test.svg"
    sIn = "<svg><rect/></svg>"
    f = SVGParser(fromString=sIn)
    sOut = str(f)
    assert(sIn == sOut)


def testFileExport():
    filename = "test.svg.tmp"
    sIn = "<svg><rect/></svg>"

    # Write to file
    p = SVGParser(fromString=sIn)
    p.toFile(filename)
    del p

    # Read back from file
    f = open(filename, "r")
    sOut = f.read()
    f.close()
    os.remove(filename)

    # Compare
    assert(sIn == sOut)


if __name__ == "__main__":
    testFileImport()
    testFromString()
    testSerialization()
    testFileExport()
