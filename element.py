#!/usr/bin/python3

from transform import SVGTransformList

#
# Generic XML element class
#
class SVGElement():
    def __init__(self, svg=None, parent=None, tag=None, attributes=[], debug=False):
        self.parentSVG = svg
        self.parentElement = parent
        self.tag = tag
        self.attributes = attributes
        self.children = []
        self.parse()

    def parse(self):
        # Special property to handle element transformations
        self.transform = SVGTransformList()
        if not (self.attributes is None):
            if "transform" in self.attributes.keys():
                self.transform = SVGTransformList(parseFromString=self.attributes["transform"])


if __name__ == "__main__":
    transform = 'matrix(1,2,3,4,5,6);rotate(45), translate(2.0 1e3)'
    print("Parsing element with attributes: transform=\"{:s}\"".format(transform))
    e = SVGElement(svg=None, parent=None, tag=None, attributes={"transform": transform})
    print(e)
    print(e.transform)
