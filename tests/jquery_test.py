#!/usr/bin/python3

from os.path import dirname, realpath, join
import sys
sys.path.append(realpath(join(dirname(__file__), "..")))

from jquery import jQuerySelector

def test_splitting():
    s = "test.class > tag#id element[variable="3"]"
    q = jQuerySelector(s)
    assert(len(q) == 4)
