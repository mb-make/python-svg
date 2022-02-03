#!/usr/bin/python3

import sys
sys.path.append("..")
from svg import SVGParser


def testFileImport():
    raise


def testFromString():
    f = SVGParser(filename="tests/import-export/test.svg", debug=True)
    # TODO: asserts...
    raise


def testSerialization():
    raise


def testFileExport():
    raise


if __name__ == "__main__":
    testFileImport()
    testFromString()
    testSerialization()
    testFileExport()
