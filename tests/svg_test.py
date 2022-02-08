#!/usr/bin/python3

import sys
sys.path.append("..")
from svg import SVGParser


def testFileImport():
    f = SVGParser(filename="tests/import-export/test.svg", debug=True)
    # TODO: asserts...
    raise


def testFromString():
    # TODO
    raise


def testSerialization():
    f = SVGParser(filename="tests/import-export/test.svg", debug=True)
    s = str(f)
    print(s)
    #e = Exception()
    raise RuntimeError()


def testFileExport():
    raise


if __name__ == "__main__":
    testFileImport()
    testFromString()
    testSerialization()
    testFileExport()
