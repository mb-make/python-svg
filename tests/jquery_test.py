#!/usr/bin/python3

from os.path import dirname, realpath, join
import sys
sys.path.append(realpath(join(dirname(__file__), "..")))

from jquery import jQuerySelector, jQueryFilter
from xmlelement import XMLElement


def test_filter_init():
    s = "test.myclass#myid"
    f = jQueryFilter(s)
    print(str(f))
    assert(f.matchTag == "test")
    assert(type(f.matchAttributes) is dict)
    assert(f.matchAttributes == {"class": "myclass", "id": "myid"})


def test_filter_matching():
    filters = []
    filters.append(jQueryFilter("test.myclass#myid"))
    filters.append(jQueryFilter("test"))
    filters.append(jQueryFilter(".myclass"))
    filters.append(jQueryFilter("#myid"))
    filters.append(jQueryFilter("testxy"))
    filters.append(jQueryFilter(".myotherclass"))
    filters.append(jQueryFilter("#myotherid"))

    elements = []
    # Three features
    elements.append(XMLElement(tag="test", attributes={"class": "myclass", "id": "myid"}))

    # Two features
    elements.append(XMLElement(tag="test", attributes={"class": "myclass"}))
    elements.append(XMLElement(tag="test", attributes={"id": "myid"}))
    elements.append(XMLElement(attributes={"class": "myclass", "id": "myid"}))

    # One feature
    elements.append(XMLElement(tag="test"))
    elements.append(XMLElement(attributes={"class": "myclass"}))
    elements.append(XMLElement(attributes={"id": "myid"}))

    # result = []
    # for f in filters:
    #     for e in elements:
    #         result[i][j] =
    assert(filters[0].matches(elements[0]))
    assert(not filters[0].matches(elements[1]))


def test_selector_init():
    s = "test.class > tag#id element[variable=\"3\"]"
    q = jQuerySelector(s)
    filters = q.getFilters()
    print(str(filters))
    assert(len(filters) == 4)


def test_selector_matching():
    svg = XMLElement(tag="svg")
    group = XMLElement(tag="g")
    path = XMLElement(tag="path")
    group.addChild(path)
    svg.addChild(group)

    assert(len(jQuerySelector("svg > g").find(svg)) == 1)
    assert(len(jQuerySelector("g > path").find(svg)) == 1)
    assert(len(jQuerySelector("svg > path").find(svg)) == 0)
    assert(len(jQuerySelector("svg path").find(svg)) == 1)
