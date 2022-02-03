#!/usr/bin/python3

import sys
sys.path.append("..")
from element import SVGElement


def testParsing():
    e = SVGElement(
            svg=None,
            parent=None,
            tag="path",
            attributes={"transform": "test"},
            debug=False
            )
    assert(e.getTag() == "path")
    assert(len(e.getAttributes()) == 1)
    assert(e.getAttribute("nonexistent") is None)
    assert(e.getAttribute("transform") == "test")
    e.deleteAttribute("transform")
    assert(len(e.getAttributes()) == 0)


def testSerialization():
    e = SVGElement(
            svg=None,
            parent=None,
            tag="path",
            attributes={"transform": "test"},
            debug=False
            )
    s = str(e)
    assert(s == "<path transform=\"test\"/>")


def testTransformation():
    e = SVGElement(
            svg=None,
            parent=None,
            tag=None,
            attributes={"transform": "rotate(90)"},
            debug=True
            )
    m = e.getSVGMatrix()
    p = (0.0, 1.0)
    result = m.applyToPoint(p, debug=True)
    assert(result == (1.0, 0.0))


if __name__ == "__main__":
    testDeserialize()
    testSerialize()
    testTransform()
