#!/usr/bin/python3

import os

from .template import SVGTemplate
from ..io.svgreader import SVGReader


here = os.path.realpath(os.path.dirname(__file__))
fn_target = os.path.join(here, "test_target.svg")
fn_template = os.path.join(here, "test_template.svg")


#
# Load a template and test content extraction from a test SVG
#
if __name__ == "__main__":
    # Load template
    print("Loading template...")
    template = SVGTemplate(filename=fn_template, debug=True)
    print(template)

    # Load target
    print("Loading target SVG...")
    target = SVGParser(filename=fn_target, debug=True)
    print(target)

    # Apply template
    print("Extracting content from target using template...")
    results = template.apply(target)
    print(results)

    # TODO: evaluate
