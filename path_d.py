#!/usr/bin/python3
#
# Classes to handle SVG path definitions and their commands
# https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths
#

import re
from transform import sNumeric
import numpy as np
from copy import deepcopy


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

sSVGPathCommand = "|".join([sA,sC,sQS,sMLT,sHV,sZ])
#print(sSVGPathCommand)
rSVGPathCommand = re.compile(sSVGPathCommand)
#print(rSVGPathCommand)


svgPathDCommandCharsLower = "mlvhcqstaz"
svgPathDCommandCharsUpper = "MLVHCQSTAZ"
svgPathDCommandChars = svgPathDCommandCharsLower + svgPathDCommandCharsUpper

# Command chars can be omitted indicating repetition of the previous command with new values
sBeginsWithCommandChar = "^" + whitespace + "([" + svgPathDCommandChars + "]{1})" + whitespace
rSVGPathCommandChar = re.compile(sBeginsWithCommandChar)


#
# Any single atomic command within an SVG path definition ("d" attribute)
#
class SVGPathCommand:
    #
    # Parse path command from regular expression match
    #
    def __init__(self, command=[], startpoint=[0,0], previousCommand=None, debug=False):
        self.debug = debug
        self.startpoint = np.array(startpoint)
        self.endpoint = None
        self.m = []

        if len(command) == 0:
            return
        if self.debug:
            print("Parsing path command: {:s}".format(str(command)))
        command = list(command)

        # Strip empty array elements at beginning and end of the list
        while (len(command) > 0) and ((command[0] is None) or (command[0] == "")):
            command.pop(0)
        while (len(command) > 0) and ((command[len(command)-1] is None) or (command[len(command)-1] == "")):
            command.pop(len(command)-1)
        assert len(command) >= 1

        i = 0
        if command[0] in svgPathDCommandChars:
            # First list element is command character
            self.m = [command[0]]
            i = 1
        else:
            # TODO: is character vs. is numeric
            # Command character omission implies repetition
            self.m = [previousCommand.m[0]]

        # Following list elements: float values
        if len(command) > 1:
            for m in command[i:]:
                self.m.append(float(m))

    def getCommandChar(self):
        return self.m[0]

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
            print("Moving from ({:.2f}, {:.2f})".format(x, y))

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

        self.endpoint = np.array([x, y])

        if self.debug:
            print("to ({:.2f}, {:.2f})".format(x, y))

        return self.endpoint

    #
    # Apply a transformation matrix to this path segment
    #
    def transform(self, matrix, inplace=True):
        if inplace:
            cmd = self
        else:
            # TODO: Is it possible to do this? What about object references (previous command etc.)?
            cmd = deepcopy(self)
            # SVGPathCommand()
            # cmd.debug = self.debug
            # cmd.m = self.m
            # cmd.startpoint = self.startpoint.deepcopy()
            # cmd.endpoint = self.endpoint.deepcopy()
        if self.debug:
            print("Transforming startpoint from\n" + str(self.getStartpoint()))
        cmd.startpoint = matrix.applyToPoint(self.getStartpoint())
        if self.debug:
            print("to\n" + str(cmd.startpoint))
            print("Transforming endpoint from\n" + str(self.getEndpoint()))
        cmd.endpoint = matrix.applyToPoint(self.getEndpoint())
        if self.debug:
            print("to\n" + str(cmd.endpoint))
        return cmd

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

        # Initialize empty
        self.d = d
        self.commands = []
        if d is None:
            return

        # Parse input string
        if self.debug:
            print("Parsing path definition: \"{:s}\"".format(d))

        for idx, (s, cmd) in enumerate(self):
            if self.debug:
                a = str(cmd.getStartpoint())
                b = str(cmd.getEndpoint())
                r = str(cmd)
                print("{:3d}: \"{:s}\" -> \"{:s}\", from {:s} to {:s}".format(idx, s, r, a, b))

        self.updatePoints()

        #
        # TODO: Verification
        #  1. The number of characters must be equal in source and parsed content.
        #  2. The number of numeric values must be equal in source and parsed content.
        #  3. Characters other than the above command commands are forbidden.
        #

        if self.debug:
            print("Results: {:s}".format(str([str(command) for command in self.commands])))

    #
    # Path definition string tokenizer
    #
    def __iter__(self):
        self.commands = []
        self.previousCommand = None
        self.cursor = np.array([0.0, 0.0])
        return self

    #
    # Tokenize one command after the other
    #
    def __next__(self):
        self.d = self.d.strip()
        if len(self.d) == 0:
            raise StopIteration

        # Explicitly insert repeated command char
        m = rSVGPathCommandChar.match(self.d)
        if self.debug:
            print("Remains to be tokenized: " + self.d)
            print(str(m))
        repeat = True if (m is None) else False
        if self.debug:
            print("Repetition: {:s}".format("Yes" if repeat else "No"))
        if repeat:
            self.d = self.previousCommand.getCommandChar() + " " + self.d

        # Parse remaining string
        match = rSVGPathCommand.search(self.d)
        if match is None:
            print("Error: Syntax error in path definition.")
            raise StopIteration
        cmd = SVGPathCommand(command=match.groups(), startpoint=self.cursor, previousCommand=self.previousCommand, debug=self.debug)

        # Store yielded command and move on to the next
        self.commands.append(cmd)
        self.previousCommand = cmd
        self.cursor = cmd.getEndpoint()
        span = match.span()
        s = self.d[span[0]:span[1]]
        self.d = self.d[span[1]:]
        return (s, cmd)

    #
    # Whenever the path definition is altered,
    # the array of points should be updated
    #
    def updatePoints(self):
        # Walk along the path and store the points
        cursor = np.array([0.0, 0.0])
        if self.debug:
            print("Startpoint: "+str(cursor))
        self.points = np.array([cursor])
        for cmd in self.getCommands():
            cursor = cmd.getEndpoint()
            if self.debug:
                print("Next point: "+str(cursor))
            self.points = np.append(self.points, [cursor], axis=0)

        if self.debug:
            print("Resulting array of points: "+str(self.points))

        # If the first command is not drawn, then the startpoint is not treated as a curve point.
        if self.commands[0].isMoveTo():
            self.points = np.delete(self.points, 0, axis=0)

        if self.debug:
            print("Points: {:s}".format(str(self.points)))

    #
    # Return the number of commands in self path description
    #
    def __len__(self):
        return len(self.commands)

    #
    # Stringify the path definition
    #
    def __str__(self):
        return " ".join([str(command) for command in self.commands])

    #
    # Return the parsed array of of path commands
    #
    def getCommands(self):
        return self.commands

    #
    # Return a specific command
    #
    def getCommand(self, index):
        return self.getCommands()[index]

    #
    # Return the path's points
    # relative to the path's origin
    #
    def getPoints(self):
        return self.points

    def getPoint(self, index):
        return self.getPoints()[index]

    def getMinX(self):
        return self.getPoints().T[0, :].min()

    def getMinY(self):
        return self.getPoints().T[1, :].min()

    def getMaxX(self):
        return self.getPoints().T[0, :].max()

    def getMaxY(self):
        return self.getPoints().T[1, :].max()

    #
    # Apply a transformation matrix to all path points
    #
    def transform(self, matrix, inplace=True):
        if inplace:
            d = self
        else:
            # TODO: Will object references be correct?
            d = deepcopy(self)
        for cmd in d.getCommands():
            cmd.transform(matrix, inplace=inplace)
        self.updatePoints()
