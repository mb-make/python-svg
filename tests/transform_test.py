#!/usr/bin/python3

import sys
sys.path.append("..")
from transform import SVGTransformList
import numpy as np


def testSVGTransformList():
    #
    # Test transformation list parsing
    #
    print("Importing an empty transformation list...")
    l = SVGTransformList(debug=True)
    result = str(l)
    print("Result: 'transform=\"{:s}\"'".format(result))
    assert result == ""

    #print("Transformation matrix:")
    l.getTransformationMatrix()

    transform = "translate(10, 20); translate(3, 4); rotate(+30);  translate( 20,-13.5 ) ,;.\t, matrix(1e3 0.2e1 3E-2 +4 5.1E+2 -6.0e-1)"
    print("Importing a valid transformation list: \"{:s}\"".format(transform))
    l = SVGTransformList(None, transform, debug=True)
    result = str(l)
    print("Result: 'transform=\"{:s}\"'".format(result))
    #assert result == "rotate(30)"

    #print("Transformation matrix:")
    l.getTransformationMatrix()

    #print("Importing an illegal transformation list...")
    #transform = "test ()"
    #l = SVGTransformList(None, transform)
    #result = str(l)
    #print("Result: 'transform=\"{:s}\"'".format(result))
    #assert result == "test"

    #
    # Test point transformation
    #
    print("Testing point transformation:")
    transform = "translate(10, 20); translate(3, 4);"
    l = SVGTransformList(None, transform, debug=True)
    result = str(l)
    print("Result: 'transform=\"{:s}\"'".format(result))
    m = l.getTransformationMatrix()
    print("Transforming point:")
    p = np.array([1, 1])
    print(p)
    pNew = m.applyToPoint(p, debug=True)
    print("Result:")
    print(pNew)


if __name__ == "__main__":
    testSVGTransformList()
