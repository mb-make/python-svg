#!/usr/bin/python3
#
# jQuery selector syntax
#

import re

rElement = re.compile("([a-zA-Z0-9\.\#\[\]\'\"=>]+)[ ]*")
rTag = re.compile("^([a-zA-Z\-_:]+)")
rClass = re.compile("\.([a-zA-Z]+)")
rId = re.compile("\#([a-zA-Z]+)")
rAttrs = re.compile("\[([ a-zA-Z0-9\=\'\"\,]+)\]")
rKeyValue = re.compile("([a-zA-Z]+)[ ]*\=[ \"\']*([a-zA-Z0-9]+)")


#
# A single filter command
# provided in jQuery syntax
#
class jQueryFilter:
    def __init__(self, selector=None, matchTag=None, matchAttributes=None, debug=False):
        self.debug = debug
        self.clear()
        if selector != None:
            self.compile(selector)
        if matchTag != None:
            self.matchTag = matchTag
        if matchAttributes != None:
            self.matchAttributes = matchAttributes

    def clear(self):
        self.matchTag = None
        self.matchAttributes = {}

    def compile(self, s):
        if self.debug:
            print("Compiling jQueryFilter from string: \"{:s}\"".format(s))
        matchTag = rTag.match(s)
        if self.debug:
            print("Tag regex match: {:s}".format(str(matchTag)))
        if matchTag != None:
            self.matchTag = matchTag.group(0)
        matchId = rId.search(s)
        if self.debug:
            print("Id regex match: {:s}".format(str(matchId)))
        if matchId != None:
            self.matchAttributes["id"] = matchId.group(1)
        matchClass = rClass.search(s)
        if self.debug:
            print("Class regex match: {:s}".format(str(matchClass)))
        if matchClass != None:
            self.matchAttributes["class"] = matchClass.group(1)
        matchAttrs = rAttrs.search(s)
        if self.debug:
            print("Additional attributes regex match: {:s}".format(str(matchAttrs)))
        if matchAttrs != None:
            haystack = matchAttrs.group(1)
            if self.debug:
                print("Parsing additional attributes: {:s}".format(str(haystack)))
            attrs = rKeyValue.findall(haystack)
            if self.debug:
                print("Found key-value pairs: {:s}".format(str(attrs)))
            for attr in attrs:
                value = attr[1]
                try:
                    value = int(value)
                except:
                    pass
                self.matchAttributes[attr[0]] = value

    def __str__(self):
        s = (self.matchTag or "")
        keys = list(self.matchAttributes.keys())
        if "class" in keys:
            s += "."+self.matchAttributes["class"]
            keys.remove("class")
        if "id" in keys:
            s += "#"+self.matchAttributes["id"]
            keys.remove("id")
        if len(keys) > 0:
            s += "["
            s += ",".join(key+"="+(str(self.matchAttributes[key]) if type(self.matchAttributes[key]) is int else "\"{:s}\"".format(self.matchAttributes[key])) for key in keys)
            s += "]"
        return s

    def matches(self, element):
        if self.matchTag != None:
            if element.getTag() == self.matchTag:
                if self.debug:
                    print("Element tag name matches ('{:s}')".format(self.matchTag))
            else:
                if self.debug:
                    print("Element tag name mismatch: expected '{:s}', got '{:s}'".format(self.matchTag, element.getTag()))
                return False
        for key in self.matchAttributes.keys():
            value = self.matchAttributes[key]
            if value is None:
                continue
            if element.getAttribute(key) == value:
                if self.debug:
                    print("Attribute matches: '{:s}={:s}'".format(key, value))
            else:
                if self.debug:
                    print("Attribute mismatch: expected '{:s}={:s}', got '{:s}={:s}'".format(key, value, key, element.getAttribute(key)))
                return False
        return True


#
# Handle a series of filter commands
# provided in jQuery syntax
#
class jQuerySelector:
    def __init__(self, selector=None, debug=False):
        self.debug = debug
        self.clear()
        if selector != None:
            self.compile(selector)

    def clear(self):
        self.filters = []

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
                q = jQueryFilter(filter, debug=self.debug)
            self.filters.append(q)

    def __str__(self):
        return " ".join([str(f) for f in self.filters])

    def getFilters(self):
        return self.filters

    def getFilter(self, index):
        if type(index) != int:
            return None
        if (index < 0) or (index >= len(self.filters)):
            raise IndexError()
        return self.filters[index]

    #
    # Apply the selector to a DOM (type SVGReader or SVGElement)
    # and return a list of matching SVGElements
    #
    def find(self, dom):
        if len(self.filters) == 0:
            # Match all elements
            return [dom, dom.getElementList()]

        recurse = True
        needles = [dom]
        if self.debug:
            selectorString = str(self)
        for filter in self.filters:
            if filter == ">":
                # Do not inspect children recursively on the next filter
                recurse = False
            else:
                # Look for filter matches in the haystack
                haystack = needles
                needles = []
                for element in haystack:
                    if self.debug:
                        print("Looking for '{:s}' below '<{:s}.../>'...".format(selectorString, element.getTag()))
                    needles += element.find(filter, recurse=recurse)

                # (Re-)Enable recursive search in the next round
                recurse = True

            # No more elements to inspect
            if len(haystack) == 0:
                break

        return needles
