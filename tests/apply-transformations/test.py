#!/usr/bin/python3

import sys, os
sys.path.append(os.path.join("..", ".."))
from svg import SVGParser

sp = SVGParser(filename="test.svg", debug=True)

sr = sp.getSVG().getChildren()[0]
ch = sr.getChildren()
print([e.getTag() for e in ch])

g = ch[3]
print(g.getTag())

print("transform =")
t = g.getTransform()
print(str(t))
matrixG = t.getTransformationMatrix()
print(str(matrixG))

path = g.getChildren()[0]
print(path.getTag())

print("transform =")
t = path.getTransform()
print(str(t))
matrixPath = t.getTransformationMatrix()
print(str(matrixPath))

ctm = path.getCTM()
print("<path>: ctm = ")
print(str(ctm))

print("Path points:")
points = path.getPoints()
print(points)

print("Transformed with path matrix:")
points2 = []
for p in points:
    pt = matrixPath.applyToPoint(p, debug=False)
    points2.append(pt)
print(points2)

print("Further transformed with group matrix:")
points3 = []
for p in points2:
    pt = matrixG.applyToPoint(p, debug=False)
    points3.append(pt)
print(points3)

print("In comparison to being transformed with the path's CTM matrix:")
points4 = []
for p in points:
    pt = ctm.applyToPoint(p, debug=False)
    points4.append(pt)
print(points4)
