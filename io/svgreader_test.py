#!/usr/bin/python3

from ..io.svgreader import SVGReader
from ..dom.element import SVGElement
from ..dom.path import SVGPath


def test_file_import():
    filename = "tests/import-export/test.svg"
    dom = SVGReader(filename=filename, debug=True)
    print(str(dom.__dict__))
    assert(not (dom is None))
    assert(dom.getChild(0).getTag() == "svg")
    assert(len(dom.find("svg")) == 1)
    assert(len(dom.find("path")) == 1)
    assert(len(dom.find("rect")) == 0)


def test_string_import():
    sIn = "<svg><rect/></svg>"
    dom = SVGReader(fromString=sIn, debug=True)
    assert(len(dom.getChildren()) == 1)
    assert(dom.getChild(0).getTag() == "svg")
    assert(len(dom.find("svg")) == 1)
    assert(len(dom.find("path")) == 0)
    assert(len(dom.find("rect")) == 1)


def test_string_export():
    sIn = "<svg><rect/></svg>"
    dom = SVGReader(fromString=sIn)
    sOut = str(dom)
    assert(sIn == sOut)


def test_file_export():
    filename = "test.svg.tmp"
    sIn = "<svg><rect/></svg>"

    # Write to file
    p = SVGReader(fromString=sIn)
    p.toFile(filename)
    del p

    # Read back from file
    f = open(filename, "r")
    sOut = f.read()
    f.close()
    os.remove(filename)

    # Compare
    assert(sIn == sOut)
