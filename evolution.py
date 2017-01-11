import random

POP_SIZE = 23
NUM_OFFSPRINGS = POP_SIZE * 10

cMax = 36
cMin = 1

tMax = 80
tMin = -40

sMax = 1500
sMin = 1200

fMax = 50
fMin = 0

class Earth:
    def __init__(self):
        t = random.randint(tMin, tMax)
        s = random.randint(sMin, sMax)
        t0 = 20
        s0 = 1367
        maxAge = 122
        c1 = 0.5
        c2 = 0.5
        sMaxDif = max(abs(sMax - s0), abs(sMin - s0))


class Human:
    def __init__(self):
        fat = random.randint(fMin, fMax) / 100
        skinColor = random.randint(cMin, cMax)
        age = 80

def randomGeneration(size):
    generation = []
    for i in range(size):
        h = Human()
        generation.append(h)
    return generation
