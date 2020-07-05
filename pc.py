from toy import Toy

def _invertcolor(c):
    return (255 - x for x in c)


def _escbg(r, g, b):
    return "\033[48;2;%d;%d;%dm" % (r, g, b)


def _escfg(r, g, b):
    return "\033[38;2;%d;%d;%dm" % (r, g, b)


def _escreset():
    return "\033[0m"


def _renderButton(x):
    b, c = x
    txt = "[X]" if b else "[ ]"
    return _escbg(*c) + _escfg(*_invertcolor(c)) + txt + _escreset()


class EmuTrellis(object):
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.c = [[(0, 0, 0)] * w for _ in range(h)]
        self.b = [[False] * w for _ in range(h)]

    def print(self):
        for y in range(self.h):
            print(*map(_renderButton, zip(self.b[y], self.c[y])))

    def button(self, x, y, state):
        self.b[y][x] = state

    def color(self, x, y, color):
        self.c[y][x] = color

    def width(self):
        return self.w

    def height(self):
        return self.h

emutrellis = EmuTrellis(8, 8)

toy = Toy(emutrellis)


def handle(cmd):
    if cmd == "exit":
        return False
    try:
        n = int(cmd)
        down = n > 0
        x = (abs(n) % 100)//10 - 1
        y = abs(n) % 10 - 1
        emutrellis.button(x, y, down)
        toy.onEvent(x, y, down)
        toy.tick()
    except ValueError:
        # Not int
        toy.tick(cmd)
    except:
        pass
    return True


keepRunning = True
while keepRunning:
    emutrellis.print()
    cmd = input("Enter your command: ").strip()
    keepRunning = handle(cmd)
