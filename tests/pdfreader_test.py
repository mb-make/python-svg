#!/usr/bin/python3

from os.path import dirname, realpath, join
import sys
sys.path.append(realpath(join(dirname(__file__), "..")))

from pdfreader import PDFReader
from svgreader import SVGReader


def test_init():
    f = PDFReader(filename="59_1.pdf")


def test_getnumpages():
    f = PDFReader(filename="59_1.pdf")
    assert(len(f) == 3)
    assert(f.getNumPages() == 3)


def test_getpage():
    f = PDFReader(filename="59_1.pdf")
    p = f.getPage(3)
    assert(type(f) == SVGReader)
