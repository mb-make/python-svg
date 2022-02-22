#!/usr/bin/python3

import sys, os
sys.path.append("..")
from svg import SVGReader
from element import SVGElement
from path import SVGPath


def testFileImport():
    filename = "tests/import-export/test.svg"
    f = SVGReader(filename=filename, debug=True)
    e = f.getSVG()
    assert(not (e is None))
    assert(type(e) is SVGElement)
    assert(e.getTag().lower() == "svg")


def testFromString():
    sIn = "<svg><rect/></svg>"
    p = SVGReader(fromString=sIn)
    dom = p.getSVG()
    assert(dom.getTag() == "svg")
    assert(len(dom.getChildren()) == 1)
    assert(dom.getChild(0).getTag() == "rect")


def testSerialization():
    sIn = "<svg><rect/></svg>"
    f = SVGReader(fromString=sIn)
    sOut = str(f)
    assert(sIn == sOut)


def testFileExport():
    filename = "test.svg.tmp"
    sIn = "<svg><rect/></svg>"

    # Write to file
    p = SVGReader(fromString=sIn)
    p.toFile(filename)
    del p

    # Read back from file
    f = open(filename, "r")
    sOut = f.read()
    f.close()
    os.remove(filename)

    # Compare
    assert(sIn == sOut)


def testGetElementById():
    filename = "tests/import-export/test.svg"
    f = SVGReader(filename=filename, debug=True)
    assert(f.getElementById("test") is None)
    assert(f.getElementById("svg2") != None)
    assert(f.getElementById("namedview7") != None)
    assert(f.getElementById("path15-3") != None)
    assert(type(f.getElementById("path15-3")) == SVGPath)


def testGetElementsByClassName():
    filename = "tests/import-export/test.svg"
    f = SVGReader(filename=filename, debug=True)
    assert(len(f.getElementsByName("test")) == 0)
    assert(len(f.getElementsByName("svg")) == 1)
    assert(len(f.getElementsByName("path")) == 1)


def testGetElementsByName():
    filename = "tests/import-export/test.svg"
    f = SVGReader(filename=filename, debug=True)
    assert(len(f.getElementsByName("test")) == 0)
    assert(len(f.getElementsByName("svg")) == 1)
    assert(len(f.getElementsByName("path")) == 1)


def testGetElementsByTagName():
    filename = "tests/import-export/test.svg"
    f = SVGReader(filename=filename, debug=True)
    assert(len(f.getElementsByTagName("test")) == 0)
    assert(len(f.getElementsByTagName("svg")) == 1)
    assert(len(f.getElementsByTagName("path")) == 1)


if __name__ == "__main__":
    testFileImport()
    testFromString()
    testSerialization()
    testFileExport()
