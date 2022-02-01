#!/usr/bin/python3

import sys
sys.path.append("..")
from element import SVGElement


def testSVGElement():
    #
    # Verify transformation attribute parsing
    #
    transform = 'matrix(1,2,3,4,5,6);rotate(45), translate(2.0 1e3)'
    print("Parsing transform attribute:\n\ttransform=\"{:s}\"".format(transform))

    e = SVGElement(
            svg=None,
            parent=None,
            tag=None,
            attributes={"transform": transform},
            debug=True
            )
    #print(e)
    t = e.getTransform()
    #print(str(t))
    m = t.getTransformationMatrix()
    #print(str(m))

    # TODO: asserts...


if __name__ == "__main__":
    testSVGElement()
