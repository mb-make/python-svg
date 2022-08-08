#!/usr/bin/python3

from ..selecting.jquery import jQuerySelector, jQueryFilter


#
# A super-class for the more XML/DOM-related methods
#
class XMLElement:
    def __init__(self, root=None, parent=None, tag="xml", attributes={}, debug=False):
        self.debug = debug
        self.documentRoot = root
        self.parentElement = parent
        self.tag = tag
        self.attributes = dict(attributes)
        self.children = []

    def isRootNode(self):
        # if self.parentElement is None:
        #     return True
        if self.documentRoot == self:
            return True
        return False

    def __str__(self):
        if self.isRootNode():
            # Omit the root node on export, only list the children
            s = ""
            for child in self.children:
                s += str(child)
            return s

        s = "<{:s}".format(self.tag)
        for key in self.attributes.keys():
            s += " {:s}=".format(key)
            value = self.attributes[key]
            t = type(value)
            if t == int:
                s += "{:d}".format(value)
            else:
                s += "\"{:s}\"".format(str(value))
        selfClosing = (len(self.children) == 0)
        if selfClosing:
            s += "/>"
        else:
            s += ">"
            for child in self.children:
                s += str(child)
            s += "</{:s}>".format(self.tag)
        return s

    def getTag(self):
        return self.tag

    def getId(self):
        if "id" in self.attributes.keys():
            return self.attributes["id"]
        return None

    def getClass(self):
        if "class" in self.attributes.keys():
            return self.attributes["class"]
        return None

    def getAttributes(self):
        return self.attributes

    def getAttribute(self, key):
        if key in self.attributes.keys():
            return self.attributes[key]
        return None

    def setAttribute(self, key, value):
        if self.attributes is None:
            self.attributes = {}
        self.attributes[key] = value

    def deleteAttribute(self, key):
        self.attributes.pop(key)

    def getDocumentRoot(self):
        return self.documentRoot

    def getParentElement(self):
        return self.parentElement

    def getChildren(self):
        return self.children

    def getChild(self, index):
        return self.children[index]

    def addChild(self, element):
        self.children.append(element)

    def getElementList(self, recursionDepth=0):
        if recursionDepth > 100:
            raise RecursionError
        result = []
        for child in self.children:
            result.append(child)
            result += child.getElementList(recursionDepth+1)
        return result

    #
    # Iterate recursively over all of the element's children
    #
    def __len__(self):
        return len(self.getElementList())

    def __iter__(self):
        self.iterIndex = 0
        self.iterElementList = self.getElementList()
        return self

    def __next__(self):
        if self.iterIndex >= len(self.iterElementList):
            raise StopIteration
        else:
            element = self.iterElementList[self.iterIndex]
            self.iterIndex += 1
            return element

    #
    # Use a selector to find matching elements
    #
    def find(self, selector, recurse=True):
        if type(selector) == str:
            selector = jQuerySelector(selector)

        if type(selector) == jQuerySelector:
            return selector.find(self)

        if type(selector) != jQueryFilter:
            raise TypeError

        results = []
        if selector.matches(self):
            results.append(self)
        if recurse:
            # Look for filter matches recursively
            for idx, element in enumerate(self):
                if selector.matches(element):
                    results.append(element)
        else:
            # Look for filter matches among the immediate child elements
            for element in self.getChildren():
                if selector.matches(element):
                    results.append(element)
        return results

    #
    # Return the element with the specified ID (or None)
    # See also: https://www.w3schools.com/jsref/met_document_getelementbyid.asp
    #
    def getElementById(self, id, recurse=True):
        filter = jQueryFilter(matchAttributes={"id": id})
        results = self.find(filter, recurse=recurse)
        if len(results) > 1:
            raise SyntaxError
        if len(results) == 0:
            return None
        return results[0]

    #
    # Return an array of elements with the given tag name
    # See also: https://www.w3schools.com/jsref/met_document_getelementsbytagname.asp
    #
    def getElementsByTagName(self, tag, recurse=True):
        filter = jQueryFilter(matchTag=tag)
        results = self.find(filter, recurse=recurse)
        return results

    #
    # Return an array of elements with the given class
    # See also: https://www.w3schools.com/jsref/met_document_getelementsbyclassname.asp
    #
    def getElementsByClassName(self, _class, recurse=True):
        filter = jQueryFilter(matchAttributes={"class": _class})
        results = self.find(filter, recurse=recurse)
        return results

    #
    # Return an array of elements with the given name
    # See also: https://www.w3schools.com/jsref/met_doc_getelementsbyname.asp
    #
    def getElementsByName(self, name, recurse=True):
        filter = jQueryFilter(matchAttributes={"name": name})
        results = self.find(filter, recurse=recurse)
        return results
