from random import *

from PIL import Image


def update(field, steps_left):
    nfield = [[0] * (len(field[0]) * 2) for _ in range(len(field) * 2)]
    for i in range(len(field) * 2):
        for j in range(len(field[0]) * 2):
            nfield[i][j] = field[i // 2][j // 2]
    field = [s.copy() for s in nfield]
    for i in range(len(field)):
        for j in range(len(field[0])):
            if i != 0 and j != 0 and i != len(field) - 1 and j != len(field[0]) - 1:
                h = [1, 1] if steps_left > 1 else [0, 0]
                for x in range(i - 1, i + 2):
                    for y in range(j - 1, j + 2):
                        if 0 <= x < len(nfield) and 0 <= y < len(nfield[0]):
                            h[field[x][y]] += 5
                            if field[x][y] == 1:
                                h[field[x][y]] += 0
                if steps_left != 0:
                    nfield[i][j] = 1 if random() * sum(h) > h[0] else 0
                else:
                    nfield[i][j] = 1 if h[0] < h[1] else 0
            else:
                nfield[i][j] = 0
    return nfield


def getColor(value):
    if value:
        return (93, 161, 48)
    return (65, 105, 225)


def save(field, step):
    pixels = im.load()
    width, height = im.size
    for y in range(height):
        for x in range(width):
            pixels[x, y] = getColor(field[y * len(field) // height][x * len(field[0]) // width])
    im.save(f'step{step}.png')


seed(19851985)
steps = 4
width = 8
height = 8
im = Image.new("RGB", (width * 2 ** steps, height * 2 ** steps))
field = [[int(random() * 2) if x != 0 and y != 0 and x != width - 1 and y != height - 1 else 0 for x in range(width)]
         for y in
         range(height)]
save(field, 0)
for i in range(1, steps + 1):
    field = update(field, steps - i)
    save(field, i)