#!/usr/bin/python3

import sys
sys.path.append("..")
from svg import SVGParser


def testSVGParser():
    f = SVGParser(filename="tests/import-export/test.svg", debug=True)
    # TODO: asserts...


if __name__ == "__main__":
    testSVGParser()
