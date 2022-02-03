#!/usr/bin/python3

import sys
sys.path.append("..")
from transform import SVGTransformList
import numpy as np


def testParsing():
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


def assertTransformation(transform, numTransformations, expectedMatrix):
    print("Parsing transform string: \"{:s}\"".format(transform))
    t = SVGTransformList(
            parseFromString=transform,
            debug=True
            )
    assert(len(t) == numTransformations)
    m = t.getMatrix()
    print("Resulting matrix:\n"+str(m))
    print("Expected matrix:\n"+str(expectedMatrix))
    cmp = (m == expectedMatrix)
    print("Is identical:\n"+str(cmp))
    assert(not (False in cmp))
    #assert(not (False in np.equal(m, matrixIdentity)))


def testIdentity():
    transform = ""
    matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    assertTransformation(transform, 0, matrix)


def testTranslate():
    transform = "translate(4, 5)"
    matrix = np.array([[1, 0, 4], [0, 1, 5], [0, 0, 1]])
    assertTransformation(transform, 1, matrix)


def testRotate():
    transform = "rotate(-45)"
    matrix = np.array([[0.707, 0.707, 0], [-0.707, 0.707, 0], [0, 0, 1]])
    assertTransformation(transform, 1, matrix)


def testMatrix():
    transform = "matrix(1, 2, 3, 4, 5, 6)"
    matrix = np.array([[1, 2, 3], [4, 5, 6], [0, 0, 1]])
    assertTransformation(transform, 1, matrix)


def testApplyToPoint():
    transform = "translate(10, 20);"
    t = SVGTransformList(None, transform, debug=True)
    m = t.getSVGMatrix()
    p = np.array([2, 1])
    pNew = m.applyToPoint(p, debug=True)
    assert(p == pNew)


def testApplyToMatrix():
    transform = "translate(3, 2)"
    t = SVGTransformList(
            parseFromString=transform,
            debug=True
            )
    #TODO
    raise


def testPathApplyTransform():
    raise


def testGroupApplyTransform():
    raise


if __name__ == "__main__":
    testParsing()
    testSerialization()
    testIdentity()
    testTranslate()
    testApplyToPoint()
    testApplyToMatrix()
    testPathApplyTransform()
    testGroupApplyTransform()
