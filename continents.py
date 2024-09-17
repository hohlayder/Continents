from math import hypot
from random import *

from PIL import Image


def getNeighbors(field, pos, radius):
    y, x = pos
    res = []
    for i in range(y - int(radius), y + int(radius) + 1):
        for j in range(x - int(radius), x + int(radius) + 1):
            if hypot(j - x, i - y) <= radius and 0 <= i < len(field[0]) and 0 <= j < len(field):
                res.append(field[i][j])
    return res


def update(field, steps_left):
    nfield = [[0] * (len(field[0]) * 2) for _ in range(len(field) * 2)]
    for i in range(len(field) * 2):
        for j in range(len(field[0]) * 2):
            nfield[i][j] = field[i // 2][j // 2]
    field = [s.copy() for s in nfield]
    if steps_left == 0:
        return smooth(field)
    for i in range(len(field)):
        for j in range(len(field[0])):
            if i != 0 and j != 0 and i != len(field) - 1 and j != len(field[0]) - 1:
                h = [1, 1] if steps_left > 2 else [0, 0]
                for x in range(i - 1, i + 2):
                    for y in range(j - 1, j + 2):
                        if 0 <= x < len(nfield) and 0 <= y < len(nfield[0]):
                            h[field[x][y]] += 5
                nfield[i][j] = 1 if random() * sum(h) > h[0] else 0
            else:
                nfield[i][j] = 0
    return nfield


def smooth(field):
    for st in range(3):
        nfield = [s.copy() for s in field]
        for i in range(len(field)):
            for j in range(len(field[0])):
                if i != 0 and j != 0 and i != len(field) - 1 and j != len(field[0]) - 1:
                    h = [0, 0]
                    for x in range(i - 2, i + 3):
                        for y in range(j - 2, j + 3):
                            if 0 <= x < len(nfield) and 0 <= y < len(nfield[0]):
                                h[field[x][y]] += 5 / (hypot(i - x, j - y) if not (i == x and j == y) else 0.5 ** st)
                    nfield[i][j] = 1 if h[1] > h[0] else 0
                else:
                    nfield[i][j] = 0
        field = nfield
    return nfield


def addHeightMap(field, steps, radius):
    for _ in range(steps * radius):
        nfield = [s.copy() for s in field]
        for i in range(len(field)):
            for j in range(len(field[0])):
                n = getNeighbors(field, (i, j), 3.5)
                if field[i][j] > 0:
                    nfield[i][j] = 1 + min(n)
                else:
                    nfield[i][j] = max(n) - 1
        field = nfield
    for _ in range(5):
        nfield = [s.copy() for s in field]
        for i in range(len(field)):
            for j in range(len(field[0])):
                n = getNeighbors(field, (i, j), 3.5)
                if field[i][j] > 0:
                    nfield[i][j] = max(0.1, sum(n)/len(n))
                else:
                    nfield[i][j] = min(-0.1, sum(n)/len(n))
        field = nfield
    return field


def getColor(value, mode):
    if mode == 1:
        if value:
            return (93, 161, 48)
        return (65, 105, 225)
    elif mode == 2:
        v = [-5, -4, -1, -0.1, 0.1, 1, 2, 3, 3.2, 3.25]
        c = [(20, 30, 105), (45, 65, 155), (65, 105, 225),
             (65, 155, 225), (222, 201, 108), (93, 161, 48), (93, 161, 48),
             (100, 80, 80), (100, 80, 80), (230, 230, 255)]
        value /= rad
        value = min(v[-1], max(v[0], value))
        if value in v:
            return c[v.index(value)]
        for i in range(len(v)):
            if value < v[i]:
                ind = i - 1
                break
        a = value - v[ind]
        l = v[ind + 1] - v[ind]
        b = l - a
        return tuple(map(lambda x: int((x[0] * b + x[1] * a) / l), [(c[ind][i], c[ind + 1][i]) for i in range(3)]))
    return (0, 0, 0)


def save(field, step, mode=1):
    pixels = im.load()
    width, height = im.size
    for y in range(height):
        for x in range(width):
            pixels[x, y] = getColor(field[y * len(field) // height][x * len(field[0]) // width], mode)
    im.save(f'step{step}.png')


seed(1235)
steps = 8
width = 8
height = 8
im = Image.new("RGB", (width * 2 ** steps, height * 2 ** steps))
field = [[int(random() * 2) if x != 0 and y != 0 and x != width - 1 and y != height - 1 else 0 for x in range(width)]
         for y in
         range(height)]
# field = [[1 if x != 0 and y != 0 and x != width - 1 and y != height - 1 else 0 for x in range(width)]
#          for y in
#          range(height)]
save(field, 0)
for i in range(1, steps + 1):
    field = update(field, steps - i)
    save(field, i)
rad = 7
field = addHeightMap(field, 3, rad)
save(field, steps + 1, 2)
