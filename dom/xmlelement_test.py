#!/usr/bin/python3

from os.path import dirname, realpath, join
import sys
sys.path.append(realpath(join(dirname(__file__), "..")))

from xmlelement import XMLElement


#
# Test-DOM
#
svg = XMLElement(tag="svg", attributes={"class": "visible"})
group = XMLElement(tag="g", attributes={"id": "test"})
path = XMLElement(tag="path", attributes={"name": "stylish_path"})
group.addChild(path)
svg.addChild(group)


def test_find():
    assert(len(svg.find("rect")) == 0)
    assert(len(svg.find("path")) == 1)
    assert(len(svg.find("svg path")) == 1)
    assert(len(svg.find("svg g path")) == 1)
    assert(len(svg.find("svg > g > path")) == 1)
    assert(len(svg.find("svg > path")) == 0)


def test_getElementById():
    assert(svg.getElementById("test") != None)
    assert(svg.getElementById("svg") == None)


def test_getElementsByClassName():
    assert(len(svg.getElementsByClassName("test")) == 0)
    assert(len(svg.getElementsByClassName("visible")) == 1)


def test_getElementsByName():
    assert(len(svg.getElementsByName("test")) == 0)
    assert(len(svg.getElementsByName("stylish_path")) == 1)


def test_getElementsByTagName():
    assert(len(svg.getElementsByTagName("svg")) == 1)
    assert(len(svg.getElementsByTagName("path")) == 1)
