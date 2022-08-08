#!/usr/bin/python3

from ..io.svgreader import SVGReader
from ..dom.rect import SVGRect
from ..selecting.bbox import SVGBoundingBox


#
# Handle the results yielded from a selector match
#
class SVGTemplateMatch:
    def __init__(self, svg, template, selectorElement, elements=[]):
        self.svg = svg
        self.template = template
        self.selectorElement = selectorElement
        self.elements = elements

    def append(self, element):
        self.elements.append(element)

    def __len__(self):
        return len(self.elements)

    def getText(self):
        # TODO: Extract text from elements
        for e in results[label]:
            if e.getTag().lower() == "text":
                # TODO
                pass
        return ""


#
# Use a template SVG to select elements from a target SVG
#
# Loads a template SVG, extract a list of selector elements
# and allows to apply them to a target SVG.
#
class SVGTemplate(SVGReader):
    def __init__(self, filename=None, debug=False):
        SVGReader.__init__(self, filename, debug)
        self.selectorElements = None

    #
    # Find all selector elements in the loaded SVG
    #
    def getSelectorElements(self):
        if self.selectorElements is None:
            self.selectorElements = {}
            key = "id"
            for e in self.getElementList():
                if key in e.getAttributes().keys():
                    label = e.getAttribute(key)
                    tp = type(e)

                    # For the time being, only rectangles are supported as selector elements.
                    if tp == SVGRect:
                        self.selectorElements[label] = e
                        if self.debug:
                            print("Found selector <rect {:s}=\"{:s}\".../>".format(key, label))
        return self.selectorElements

    #
    # Apply this template to a target SVG and
    # return a dictionary of matched elements
    #
    # @param targetSVG: The document to analyze as SVGReader or SVGElement object
    #
    def apply(self, targetSVG):
        tp = type(targetSVG)
        if (tp != SVGReader):
        # if (tp != SVGElement) and (tp != SVGReader):
            print("Error: Illegal argument type: {:s}".format(type(tp)))
            return None

        results = {}
        selectors = self.getSelectorElements()
        for q in selectors.keys():
            bbox = selectors[q]
            results[q] = SVGTemplateMatch(
                            svg=targetSVG,
                            template=self,
                            selectorElement=bbox
                            )
            for e in targetSVG.getElementList():
                if bbox.contains(e):
                    results[q].append(result)
        return results
