#!/usr/bin/python3

import numpy as np

from .transform import SVGTransformList, SVGTransformTranslate, SVGTransformRotate, SVGTransformMatrix


def assertTransformation(transform, numTransformations, expectedMatrix):
    print("Parsing transform string: \"{:s}\"".format(transform))
    t = SVGTransformList(
            parseFromString=transform,
            debug=True
            )
    assert(len(t) == numTransformations)
    m = t.getMatrix().round(decimals=3)
    print("Resulting matrix:\n"+str(m))
    print("Expected matrix:\n"+str(expectedMatrix))
    cmp = (m == expectedMatrix)
    print("Is identical:\n"+str(cmp))
    assert(not (False in cmp))
    #assert(not (False in np.equal(m, matrixIdentity)))


def testParseEmpty():
    transform = ""
    matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    assertTransformation(transform, 0, matrix)


def testParseTranslate():
    transform = "translate(4, 5)"
    matrix = np.array([[1, 0, 4], [0, 1, 5], [0, 0, 1]])
    assertTransformation(transform, 1, matrix)


def testParseRotate():
    transform = "rotate(-45)"
    matrix = np.array([[0.707, 0.707, 0], [-0.707, 0.707, 0], [0, 0, 1]])
    assertTransformation(transform, 1, matrix)


def testParseMatrix():
    transform = "matrix(1, 2, 3, 4, 5, 6)"
    matrix = np.array([[1, 2, 3], [4, 5, 6], [0, 0, 1]])
    assertTransformation(transform, 1, matrix)


def testParseSequence():
    # Multiple transformations
    transform = "translate(10, 20); translate(3, 4); rotate(+30);  translate( 20,-13.5 ) ,;.\t, matrix(1e3 0.2e1 3E-2 +4 5.1E+2 -6.0e-1)"
    t = SVGTransformList(
            parseFromString=transform,
            debug=True
            )
    m = t.getMatrix()
    assert(len(t) == 5)
    assert(type(t.getTransformation(0)) == SVGTransformTranslate)
    assert(type(t.getTransformation(1)) == SVGTransformTranslate)
    assert(type(t.getTransformation(2)) == SVGTransformRotate)
    assert(type(t.getTransformation(3)) == SVGTransformTranslate)
    assert(type(t.getTransformation(4)) == SVGTransformMatrix)


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


def assertApplyToPoint(transform, point, expectedResult):
    t = SVGTransformList(None, transform, debug=True)
    m = t.getSVGMatrix()
    pTransformed = m.applyToPoint(point, debug=True)
    assert(not (False in (pTransformed == expectedResult)))


def testApplyToPointArray():
    transform = "translate(10, 20);"
    p = [2, 1]
    pNew = [12.0, 21.0]
    assertApplyToPoint(transform, p, pNew)


def testApplyToPointTuple():
    transform = "translate(10, 20);"
    p = (2, 1)
    pNew = [12.0, 21.0]
    assertApplyToPoint(transform, p, pNew)


def testApplyToPointNumpyArray():
    transform = "translate(10, 20);"
    p = np.array([2, 1])
    pNew = [12.0, 21.0]
    assertApplyToPoint(transform, p, pNew)

    p = np.array([[2], [1]])
    assertApplyToPoint(transform, p, pNew)


def testApplyToPointNumpyMatrix():
    transform = "translate(10, 20);"
    p = np.matrix([2, 1])
    pNew = [12.0, 21.0]
    assertApplyToPoint(transform, p, pNew)

    p = np.matrix([[2], [1]])
    assertApplyToPoint(transform, p, pNew)


def assertApplyToMatrix(transform, matrix, expectedMatrix):
    t = SVGTransformList(
            parseFromString=transform,
            debug=True
            )
    m = t.getSVGMatrix().applyToMatrix(matrix).getMatrix().round(decimals=3)
    assert(not (False in (m == expectedMatrix)))


def testApplyTranslateToMatrix():
    transform = "translate(3, 2)"
    mOriginal = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    mTransformed = np.array([[1, 0, 3], [0, 1, 2], [0, 0, 1]])
    assertApplyToMatrix(transform, mOriginal, mTransformed)


def testApplyRotateToMatrix():
    transform = "rotate(-45)"
    mOriginal = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    mTransformed = np.array([[0.707, 0.707, 0], [-0.707, 0.707, 0], [0, 0, 1]])
    assertApplyToMatrix(transform, mOriginal, mTransformed)


def testApplySequenceToMatrix():
    # See also: https://www.w3.org/TR/SVG11/coords.html#TransformAttribute
    transform = "translate(50, 90); rotate(-45); translate(130,160);"
    mOriginal = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    mTransformed = np.array([[0.707, 0.707, 255.061], [-0.707, 0.707, 111.213], [0, 0, 1]])
    assertApplyToMatrix(transform, mOriginal, mTransformed)


def testPathApplyTransform():
    raise


def testGroupApplyTransform():
    raise


if __name__ == "__main__":
    testParseEmpty()
    testParseTranslate()
    testParseRotate()
    testParseMatrix()
    testParseSequence()
    testSerialization()
    testApplyToPointArray()
    testApplyToPointTuple()
    testApplyToPointNumpyArray()
    testApplyToPointNumpyMatrix()
    testApplyTranslateToMatrix()
    testApplyRotateToMatrix()
    testApplySequenceToMatrix()
    testPathApplyTransform()
    testGroupApplyTransform()
