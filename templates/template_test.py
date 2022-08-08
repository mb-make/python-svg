#!/usr/bin/python3

# import sys
# sys.path.append("..")

from .template import SVGTemplate
from ..io.svgreader import SVGReader


#
# Load a template and test content extraction from a test SVG
#
if __name__ == "__main__":
    # Load template
    print("Loading template...")
    template = SVGTemplate(filename="template-application/template.svg", debug=True)
    print(template)

    # Load target
    print("Loading target SVG...")
    target = SVGParser(filename="template-application/target.svg", debug=True)
    print(target)

    # Apply template
    print("Extracting content from target using template...")
    results = template.apply(target)
    print(results)

    # TODO: evaluate
