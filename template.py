#!/usr/bin/python3

from svg import SVGReader
from rect import SVGRect
from bbox import SVGBoundingBox


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

    #
    # Find all selector elements in the loaded SVG
    #
    def getSelectorElements(self):
        results = {}
        key = "inkscape:label"
        for e in self.getElementList():
            if key in e.getAttributes().keys():
                label = e.getAttributes(key)
                tp = type(e)
                if tp == SVGRect:
                    results[label] = e
                else:
                    print("Warning: Skipping {:s}. Only rectangles are supported as selectors.".format(tp))
        return results

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
