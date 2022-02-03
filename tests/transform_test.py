#!/usr/bin/python3

import sys
sys.path.append("..")
from transform import SVGTransformList
import numpy as np


def testParsing():
    # Empty transformation list
    t = SVGTransformList(debug=True)
    assert(len(t) == 0)

    m = t.getMatrix()
    matrixIdentity = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    assert(m == matrixIdentity)
    #assert(not (False in np.equal(m, matrixIdentity)))

    # Multiple transformations
    transform = "translate(10, 20); translate(3, 4); rotate(+30);  translate( 20,-13.5 ) ,;.\t, matrix(1e3 0.2e1 3E-2 +4 5.1E+2 -6.0e-1)"
    t = SVGTransformList(
            parseFromString=transform,
            debug=True
            )
    m = t.getMatrix()

    # Illegal transform string
    transform = "test ()"
    t = SVGTransformList(None, transform)
    s = str(t)
    assert(s == "test")


def testSerialization():
    # Empty list
    t = SVGTransformList(debug=True)
    assert(str(t) == "")

    # Translate
    transform = "translate(10.000, 20.000)"
    t = SVGTransformList(
            parseFromString=transform,
            debug=True
            )
    s = str(t)
    assert(s == transform)


def testTransformPoint():
    transform = "translate(10, 20);"
    t = SVGTransformList(None, transform, debug=True)
    m = t.getSVGMatrix()
    p = np.array([2, 1])
    pNew = m.applyToPoint(p, debug=True)
    assert(p == pNew)


def testTransformMatrix():
    transform = "translate(3, 2)"
    t = SVGTransformList(
            parseFromString=transform,
            debug=True
            )


def testPathApplyTransform():
    raise


def testGroupApplyTransform():
    raise


if __name__ == "__main__":
    testParsing()
    testSerialization()
    testTransformPoint()
    testTransformMatrix()
    testPathApplyTransform()
    testGroupApplyTransform()
