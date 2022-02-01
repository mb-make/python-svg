#!/usr/bin/python3
#
# Classes to handle SVG path definitions and their commands
# https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths
#

import re
from transform import sNumeric


#
# Compile regular expression for parsing
#
whitespace = "[ \t\,\:\;\(\)]*"
# uncaptured group
begin = "" #"(?:"
end = "" #")"

# Arc:
# A rx ry x-axis-rotation large-arc-flag sweep-flag x y
# a rx ry x-axis-rotation large-arc-flag sweep-flag dx dy
sA = begin + whitespace + "([aA]{1})" + (whitespace + sNumeric)*7 + end

# Bezier curve:
#  C x1 y1, x2 y2, x y
#  c dx1 dy1, dx2 dy2, dx dy
sC = begin + whitespace + "([cC]{1})" + (whitespace + sNumeric)*6 + end

# Quadratic curve:
#  Q x1 y1, x y
#  q dx1 dy1, dx dy
# Append Bezier (smooth):
#  S x2 y2, x y
#  s dx2 dy2, dx dy
sQS = begin + whitespace + "([qQsS]{1})" + (whitespace + sNumeric)*4 + end

# MoveTo:
#  M x y
#  m dx dy
# LineTo:
#  L x y
#  l dx dy
# Append quadratic Bezier:
#  T x y
#  t dx dy
sMLT = begin + whitespace + "([mMlLtT]{1})" + (whitespace + sNumeric)*2 + end

sImplicitRepetition = begin + whitespace + (whitespace + sNumeric)*2 + end

# Horizontal line:
#  H x
#  h dx
# Vertical line:
#  V y
#  v dy
sHV = begin + whitespace + "([hHvV]{1})" + (whitespace + sNumeric) + end

# Close path:
#  Z
#  z
sZ = begin + whitespace + "([zZ]{1})" + end

sSVGPathCommand = "|".join([sA,sC,sQS,sMLT,sHV,sZ,sImplicitRepetition])
#print(sSVGPathCommand)
rSVGPathCommand = re.compile(sSVGPathCommand)
#print(rSVGPathCommand)


#
# Any single atomic command within an SVG path definition ("d" attribute)
#
class SVGPathCommand:
    #
    # Parse path command from regular expression match
    #
    def __init__(self, command, startpoint=(0,0), previousCommand=None, debug=False):
        self.debug = debug

        command = list(command)

        # Strip empty array elements at beginning and end of the list
        while (len(command) > 0) and (command[0] == ""):
            command.pop(0)
        while (len(command) > 0) and (command[len(command)-1] == ""):
            command.pop(len(command)-1)
        assert len(command) >= 1
        if self.debug:
            print("Parsing path command: {:s}".format(str(command)))

        i = 0
        anyCommand = "mMlLvVhHcCqQsStTaAzZ"
        if command[0] in anyCommand:
            # First list element is command character
            self.m = [command[0]]
            i = 1
        else:
            # Command character omission implies repetition
            self.m = [previousCommand.m[0]]

        # Following list elements: float values
        if len(command) > 1:
            for m in command[i:]:
                self.m.append(float(m))

        self.startpoint = startpoint
        self.endpoint = None

    def isMoveTo(self):
        return self.m[0].upper() == "M"

    def isLineTo(self):
        return self.m[0].upper() == "L"

    def isHorizontalLine(self):
        return self.m[0].upper() == "H"

    def isVerticalLine(self):
        return self.m[0].upper() == "V"

    def isClosePath(self):
        return self.m[0].upper() == "Z"

    def isCubicBezier(self):
        return self.m[0].upper() == "C"

    def isMultipleCubicBeziers(self):
        return self.m[0].upper() == "S"

    def isQuadraticBezier(self):
        return self.m[0].upper() == "Q"

    def isMultipleQuadraticBeziers(self):
        return self.m[0].upper() == "T"

    def isArc(self):
        return self.m[0].upper() == "A"

    def isRelative(self):
        return not self.isAbsolute()

    def isAbsolute(self):
        return self.m[0] == self.m[0].upper()

    def getStartpoint(self):
        return self.startpoint

    def getEndpoint(self):
        if not (self.endpoint is None):
            return self.endpoint

        x = self.startpoint[0]
        y = self.startpoint[1]
        if self.debug:
            print("Moving from ({:.2f},{:.2f})".format(x, y))

        if self.isMoveTo() or self.isLineTo() or self.isMultipleQuadraticBeziers():
            x = self.m[1]
            y = self.m[2]
        elif self.isHorizontalLine():
            x = self.m[1]
            y = self.startpoint[1]
        elif self.isVerticalLine():
            x = self.startpoint[0]
            y = self.m[1]
        elif self.isClosePath():
            x = 0.0
            y = 0.0
        elif self.isCubicBezier():
            x = self.m[5]
            y = self.m[6]
        elif self.isMultipleCubicBeziers() or self.isQuadraticBezier():
            x = self.m[3]
            y = self.m[4]
        elif self.isArc():
            x = self.m[6]
            y = self.m[7]
        else:
            print("Error: Path command not recognized.")

        if self.isRelative() and (not self.isClosePath()):
            if self.debug:
                print("Path command uses relative coordinates.")
            if not self.isVerticalLine():
                x += self.startpoint[0]
            if not self.isHorizontalLine():
                y += self.startpoint[1]

        self.endpoint = (x, y)

        if self.debug:
            print("to ({:.2f},{:.2f})".format(x, y))

        return self.endpoint

    #
    # Convert command back to string
    #
    def __str__(self):
        return " ".join([str(e) for e in self.m])


#
# Loads, parsees and enables handling of paths
# as defined in a path's "d" attribute
#
class SVGPathDefinition:
    #
    # initialize path data
    #
    def __init__(self, path=None, d=None, debug=False):
        self.path = path
        self.debug = debug

        # initialize empty
        self.commands = []
        if d is None:
            return

        #print(rSVGPathCommand.match(s).groups())
        results = rSVGPathCommand.findall(d)
        if self.debug:
            print("Parsing path definition: \"{:s}\"".format(d))
            #print("Intermediate results: {:s}".format(str(results)))

        # Walk along the path and store the points
        cursor = (0.0, 0.0)
        self.points = [cursor]
        cmd = None
        for match in results:
            cmd = SVGPathCommand(command=match, startpoint=cursor, previousCommand=cmd, debug=self.debug)
            self.commands.append(cmd)
            cursor = cmd.getEndpoint()
            self.points.append(cursor)

        # If the first command is not drawn, then the startpoint is not treated as a curve point.
        if self.commands[0].isMoveTo():
            self.points.pop(0)

        #
        # TODO: Verification
        #  1. The number of characters must be equal in source and parsed content.
        #  2. The number of numeric values must be equal in source and parsed content.
        #  3. Characters other than the above command commands are forbidden.
        #

        if self.debug:
            print("Results: {:s}".format(str([str(command) for command in self.commands])))
            print("Points: {:s}".format(str(self.points)))

    #
    # Return the number of commands in self path description
    #
    def __len__(self):
        return len(self.commands)

    #
    # Return the parsed array of of path commands
    #
    def getCommands(self):
        return self.commands

    #
    # Return a specific command
    #
    def getCommand(self, index):
        return self.commands[index]

    #
    # Return the path's points
    # relative to the path's origin
    #
    def getPoints(self):
        return self.points

    #
    # Export as string
    #
    def __str__(self):
        return " ".join([str(command) for command in self.commands])

    #
    # min/max functions
    #
    def getMinX(self):
        result = None
        for command in self.commands:
            if "ML".find(command.type) > -1:
                if (result == None) or (command.x < result):
                    result = command.x
        return result

    def getMaxX(self):
        result = None
        for command in self.commands:
            if "ML".find(command.type) > -1:
                if (result == None) or (command.x > result):
                    result = command.x
        return result

    def getMinY(self):
        result = None
        for command in self.commands:
            if "ML".find(command.type) > -1:
                if (result == None) or (command.y < result):
                    result = command.y
        return result

    def getMaxY(self):
        result = None
        for command in self.commands:
            if "ML".find(command.type) > -1:
                if (result == None) or (command.y > result):
                    result = command.y
        return result
