#!/usr/bin/python3

from ..selecting.bbox import SVGBoundingBox


def testFromElement():
    e = SVGBoundingBox(minX=3, minY=4, maxX=15, maxY=20)
    box = SVGBoundingBox(fromElement=e)
    assert(box.getMinX() == 3)
    assert(box.getMinY() == 4)
    assert(box.getMaxX() == 15)
    assert(box.getMaxY() == 20)


def testContainsPoint():
    box = SVGBoundingBox(minX=3, minY=4, maxX=15, maxY=20)
    assert(box.containsPoint(3, 4) == True)
    assert(box.containsPoint(15, 20) == True)
    assert(box.containsPoint(4, 8) == True)
    assert(box.containsPoint(16, 8) == False)
    assert(box.containsPoint(2.5, 21) == False)


def testContainsElement():
    box = SVGBoundingBox(minX=3, minY=4, maxX=15, maxY=20)
    e = SVGBoundingBox(minX=4, minY=4, maxX=10, maxY=20)
    assert(box.containsElement(e) == True)
    e = SVGBoundingBox(minX=4, minY=4, maxX=10, maxY=21)
    assert(box.containsElement(e) == False)


def testTouchesElement():
    box = SVGBoundingBox(minX=3, minY=4, maxX=15, maxY=20)
    e = SVGBoundingBox(minX=15, minY=20, maxX=30, maxY=40)
    assert(box.touchesElement(e) == True)
    e = SVGBoundingBox(minX=16, minY=20, maxX=30, maxY=40)
    assert(box.touchesElement(e) == False)


if __name__ == "__main__":
    testContainsPoint()
