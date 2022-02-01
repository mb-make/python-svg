#!/usr/bin/python3

from svg import SVG
from bbox import SVGBoundingBox


#
# Load a template SVG, extract a list of bounding boxes
# and apply the latter for content extraction from a target SVG
#
class SVGTemplate(SVGParser):
    def __init__(self, filename=None, bboxSelector="bbox[a-zA-Z0-9]", debug=False):
        self.clear()
        super().__init__(filename, debug)

    def clear(self):
        super().clear()
        self.boundingBoxes = []

    #
    # Iterate over all SVG elements and enumerate the ones
    # where the id attribute matches the bbox selector
    #
    def parseBoundingBoxes(self):
        self.boundingBoxes = []
        # TODO: Enumerate bounding boxes

    #
    # Apply this template to a target SVG and
    # enumerate the content enclosed by bounding boxes
    #
    def apply(self, svgTarget=None):
        if svgTarget is None:
            print("Error: SVGTemplate.apply: Missing argument for svgTarget")
            return None

        results = {}
        for e in svgTarget.elementList:
            for bbox in self.boundingBoxes:
                if bbox.contains(e):
                    if not (bbox in results.keys()):
                        results[bbox]
