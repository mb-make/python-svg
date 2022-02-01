#!/usr/bin/python3

import sys
sys.path.append("..")
from bbox import SVGBoundingBox


def testSVGBoundingBox():
    template = SVGBoundingBox(minX=3, minY=4, maxX=15, maxY=20)
    assert(template.containsPoint(4, 8) == True)
    assert(template.containsPoint(16, 8) == False)
    assert(template.containsPoint(2.5, 21) == False)


if __name__ == "__main__":
    testSVGBoundingBox()
