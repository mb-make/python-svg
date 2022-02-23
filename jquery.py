#!/usr/bin/python3
#
# jQuery selector syntax
#

import re

rElement = re.compile("([a-zA-Z0-9\.#\[\'\"=\]]*)[ ]*")
rTag = re.compile("^([a-zA-Z\-_:]+)")
rClass = re.compile("(\.[a-zA-Z\-_]+)")
rId = re.compile("(#[a-zA-Z\-_]+)")


#
# A single filter command
# provided in jQuery syntax
#
class jQueryFilter:
    def __init__(self, selector=None, matchTag=None, matchAttributes=None):
        self.clear()
        if selector != None:
            self.compile(selector)
        if matchTag != None:
            self.matchTag = matchTag
        if matchTag != None:
            self.matchAttributes = matchAttributes

    def clear(self):
        self.matchTag = None
        self.matchAttributes = None

    def compile(self, s):
        matchTag = rTag.match(s)
        if matchTag != None:
            self.matchTag = matchTag.group()
        matchId = rId.match(s)
        if matchId != None:
            self.matchAttributes["id"] = matchId.group()
        matchClass = rClass.match(s)
        if matchClass != None:
            self.matchAttributes["class"] = matchClass.group()

    def matches(self, element):
        if (self.matchTag != None) and (element.getTag() != self.matchTag):
            return False
        for key in self.matchAttributes.keys():
            value = self.matchAttributes[key]
            if value is None:
                continue
            if (element.getAttribute(key) != value):
                return False
        return True


#
# Handle a series of filter commands
# provided in jQuery syntax
#
class jQuerySelector:
    def __init__(self, selector=None):
        self.clear()
        if selector != None:
            self.compile(selector)

    def clear(self):
        self.filters = []

    def getFilter(self, index):
        if type(index) != int:
            return None
        if (index < 0) or (index >= len(self.filters)):
            raise IndexError()
        return self.filters[index]

    #
    # Compile a jQuery selector from a selector string
    #
    def compile(self, selector):
        self.clear()

        # Split the selector string into it's components
        filters = re.findall(rElement, selector)
        for filter in filters:
            q = filter
            if q != ">":
                q = jQueryFilter(filter)
            self.filters.append(q)

    #
    # Apply the selector to a DOM (type SVGReader or SVGElement)
    # and return a list of matching SVGElements
    #
    def find(self, dom):
        if len(self.filters) == 0:
            # Match all elements
            return dom.getElementList()

        recurse = True
        needles = dom
        for filter in self.filters:
            if filter == ">":
                # Do not inspect children recursively on the next filter
                recurse = False
            else:
                # Look for filter matches in the haystack
                haystack = needles
                needles = []
                for element in haystack:
                    needles.append(element.find(filter, recurse=recurse))

                # (Re-)Enable recursive search in the next round
                recurse = True

            # No more elements to inspect
            if len(haystack) == 0:
                break

        return needles
