#!/usr/bin/python
#
# Library to handle SVG rectangles
#

def xml_attribute(s, key):
    p = s.find(key+'=\"')
    q = f.find('"',p)
    substring = s[p+len(key)+2:q]
    if p > -1:
        try:
            val = float(substring)
            return val
        except:
            return substring
    return None

class Rect:
    #
    # parse object from string
    #
    def __init__(this, s=None):
        if s != None:
            this.x = xml_attribute(s, 'x') or 0
            this.y = xml_attribute(s, 'y') or 0
            this.width = xml_attribute(s, "width") or 0
            this.height = xml_attribute(s, "height") or 0
            this.style = xml_attribute(s, "style") or ""

    #
    # export path as string
    #
    def __str__(this):
        return '<rect x="' + str(this.x) \
            + '" y="' + str(this.y) \
            + '" width="' + str(this.width) \
            + '" height="'+ str(this.height) \
            + '" style="' + this.style \
            + '" />'
