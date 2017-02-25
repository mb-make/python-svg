#!/usr/bin/python
#
# Library to handle SVG path descriptions and segments
#

class Segment:
    #
    # parse segment from string
    #
    def __init__(this, s):
        s = s.strip()

        this.type = s[0]

        if s.find(",") > -1:
            c = s.split(" ")[1].split(",")
            this.x = float(c[0])
            this.y = float(c[1])

    #
    # convert segment back to string
    #
    def __str__(this):
        if "ML".find(this.type) > -1:
            return this.type + " " + str(this.x) + "," + str(this.y)
        # else: return only the type
        return this.type

class D:
    #
    # parse path definition from string
    #
    def __init__(this, s):
        s = s.strip()
        this.segments = []
        p = 0
        while p < len(s):
            # search for beginning of next segment
            while (p < len(s)) and ("MLz".find(s[p]) == -1):
                p += 1

            q = p + 2
            if (q < len(s)) and ("-0123456789".find(s[q]) != -1):
                # has number arguments
                e = s.find(" ", q)
                this.segments.append( Segment(s[p:e]) )
                p = e + 1
            else:
                # has no number args
                this.segments.append( Segment(s[p:p+2]) )
                p = q

    #
    # return number of segments in this path description
    #
    def __len__(this):
        return len(this.segments)

    #
    # export as string
    #
    def __str__(this):
        return " ".join([str(segment) for segment in this.segments])
