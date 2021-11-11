
class SVGElement():
    def __init__(self, svg, parent, tag, attributes):
        self.parentSVG = svg
        self.parentElement = parent
        self.tag = tag
        self.attributes = attributes
