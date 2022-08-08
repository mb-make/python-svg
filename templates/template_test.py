#!/usr/bin/python3
#
# Load a template and test content extraction from a test SVG
#

import os

from .template import SVGTemplate
from ..io.svgreader import SVGReader


here = os.path.realpath(os.path.dirname(__file__))
fn_target = os.path.join(here, "test_target.svg")
fn_template = os.path.join(here, "test_template.svg")


def test_template_loading():
    svg = SVGTemplate(filename=fn_template, debug=True)
    rects = svg.getElementsByTagName("rect")
    paths = svg.getElementsByTagName("path")
    assert(len(rects) == 4)
    assert(len(paths) == 7)


def test_target_loading():
    svg = SVGReader(filename=fn_target, debug=True)
    rects = svg.getElementsByTagName("rect")
    paths = svg.getElementsByTagName("path")
    assert(len(rects) == 0)
    assert(len(paths) == 8)


def test_template_application():
    # Load template
    print("Loading template...")
    template = SVGTemplate(filename=fn_template, debug=False)
    print(template)

    # Load target
    print("Loading target SVG...")
    target = SVGReader(filename=fn_target, debug=False)
    print(target)

    # Apply template
    print("Extracting content from target using template...")
    results = template.apply(target)
    print(results)
    # TODO: evaluate
