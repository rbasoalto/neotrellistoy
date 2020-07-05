__all__ = ["Toy"]

baseColors = {
    "red": (255, 0, 0),
    "yellow": (255, 150, 0),
    "green": (0, 255, 0),
    "cyan": (0, 255, 255),
    "blue": (0, 0, 255),
    "purple": (180, 0, 255),
}


def parseColor(c):
    """parses a color in hex-like to a 3-tuple"""
    if c in baseColors:
        return baseColors[c]
    if len(c) == 6:
        return tuple(map(lambda x: int(x, 16), (c[:2], c[2:4], c[4:])))
    if len(c) == 3:
        return tuple(map(lambda x: 16*int(x, 16), c))
    raise ValueError("Can't find color '{}'".format(c))


# some color definitions
OFF = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

sequence = [OFF, RED, YELLOW, GREEN, CYAN, BLUE, PURPLE]


class Toy(object):
    def __init__(self, matrix):
        self.matrix = matrix
        self.state = [[0] * matrix.width() for _ in range(matrix.height())]
        self.commands = {
            "clear": self.cmdClear,
            "color": self.cmdColor,
        }

    def onEvent(self, x, y, down):
        """Callback for events, button at (x,y) was (pressed if down else released)"""
        if down:
            self.state[y][x] = (self.state[y][x] + 1) % len(sequence)
            self.matrix.color(x, y, sequence[self.state[y][x]])

    def tick(self, cmd=None):
        """Time passed, maybe do stuff"""
        if cmd and isinstance(cmd, str):
            parts = cmd.split()
            if parts[0] in self.commands:
                try:
                    self.commands[parts[0]](parts[1:])
                except Exception as e:
                    print("Exception processing command", e)

    def genMatrix(self):
        for y in range(self.matrix.height()):
            for x in range(self.matrix.width()):
                yield (x, y)

    def genCol(self, x):
        for y in range(self.matrix.height()):
            yield (x, y)

    def genRow(self, y):
        for x in range(self.matrix.width()):
            yield (x, y)

    def genCell(self, x, y):
        yield (x, y)

    def genRowColCell(self, args):
        """takes args as string, and generates the (x,y) coords for a row, col, or cell"""
        if len(args) == 2:
            x = int(args[0])
            y = int(args[1])
            if x == 0 and y == 0:
                return self.genMatrix()
            elif x == 0:
                return self.genRow(y - 1)
            elif y == 0:
                return self.genCol(x - 1)
            else:
                return self.genCell(x - 1, y - 1)
        else:
            return self.genMatrix()

    def cmdClear(self, args):
        """clear the board, or a row, or a column, or a cell"""
        for (x, y) in self.genRowColCell(args):
            self.state[y][x] = 0
            self.matrix.color(x, y, sequence[0])

    def cmdColor(self, args):
        """color <color> [x y]"""
        color = parseColor(args.pop(0))
        for (x, y) in self.genRowColCell(args):
            self.state[y][x] = -1
            self.matrix.color(x, y, color)
