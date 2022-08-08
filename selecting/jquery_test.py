#!/usr/bin/python3

from .jquery import *
from ..dom.xmlelement import XMLElement


def test_regular_expressions():
    assert(len(rElement.match("element[attr='fancy']").group()) == 7+2+4+1+2+5)
    assert(len(rElement.match("element[attr=\"fancy\"]").group()) == 7+2+4+1+2+5)

    assert(rTag.match("name") != None)
    assert(rTag.match("name2") != None)
    assert(rTag.match("2name") == None)

    assert(rId.search("#myid") != None)
    assert(rId.search("name#myid") != None)
    assert(rId.search("name#myid.myclass") != None)

    assert(rClass.search(".myclass") != None)
    assert(rClass.search("name.myclass") != None)
    assert(rClass.search("name#myid.myclass") != None)

    assert(rAttrs.search("element") == None)
    assert(len(rAttrs.findall("e[xy=z]")) == 1)
    assert(len(rAttrs.findall("e[xy=z][attr2]")) == 2)

    assert(rKeyValue.search("element#myid") is None)
    assert(len(rKeyValue.findall("e[xy=z]")) == 1)
    assert(len(rKeyValue.findall("e[xy=z][attr][attr='4', attr=\"yes\"]")) == 3)


def test_filter_init():
    f = jQueryFilter("test.myclass#myid[style=None,width=\"4\",height='3']", debug=True)
    print(str(f))
    assert(f.matchTag == "test")
    assert(type(f.matchAttributes) is dict)
    assert(f.matchAttributes == {"class": "myclass", "id": "myid", "style": "None", "width": 4, "height": 3})


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

    # One feature
    elements.append(XMLElement(tag="test"))
    elements.append(XMLElement(attributes={"class": "myclass"}))
    elements.append(XMLElement(attributes={"id": "myid"}))

    assert(filters[0].matches(elements[0]) == True)
    assert(filters[0].matches(elements[1]) == False)

    assert(filters[1].matches(elements[1]) == True)
    assert(filters[2].matches(elements[2]) == True)
    assert(filters[3].matches(elements[3]) == True)

    assert(filters[4].matches(elements[1]) == False)
    assert(filters[5].matches(elements[2]) == False)
    assert(filters[6].matches(elements[3]) == False)


def test_selector_init():
    s = "test.class > tag#id element[variable=\"3\"]"
    q = jQuerySelector(s, debug=True)
    filters = q.getFilters()
    print("Filters: "+str(filters))
    for f in filters:
        print("Filter: "+str(f))

    assert(len(filters) == 4)
    assert(str(filters[0]) == "test.class")
    assert(str(filters[1]) == ">")
    assert(str(filters[2]) == "tag#id")

    print("Additional filter attributes: "+str(filters[3].matchAttributes))
    assert(str(filters[3]) == "element[variable=3]")


def test_selector_matching():
    dom = XMLElement(tag="svg")
    group = XMLElement(tag="g")
    path = XMLElement(tag="path")
    group.addChild(path)
    dom.addChild(group)

    assert(len(jQuerySelector("svg", debug=True).find(dom)) == 1)
    assert(len(jQuerySelector("svg > g", debug=True).find(dom)) == 1)
    assert(len(jQuerySelector("g > path", debug=True).find(dom)) == 1)
    assert(len(jQuerySelector("svg > path", debug=True).find(dom)) == 0)
    assert(len(jQuerySelector("svg path", debug=True).find(dom)) == 1)
