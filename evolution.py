import math
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
        self.t = random.randint(tMin, tMax)
        self.s = random.randint(sMin, sMax)
        self.t0 = 20
        self.s0 = 1367
        self.maxAge = 122
        self.c1 = 0.5
        self.c2 = 0.5
        self.sMaxDif = max(abs(sMax - self.s0), abs(sMin - self.s0))
        self.tMaxDif = max(abs(tMax - self.t0), abs(tMin - self.t0))


class Human:
    def __init__(self):
        self.fat = random.randint(fMin, fMax) / 50.
        self.skinColor = random.randint(cMin, cMax)
        self.age = 80

    def setFat(self, fatVal):
        self.fat = fatVal

    def setSkinColor(self, skinColorVal):
        self.skinColor = skinColorVal

    def setAge(self, ageVal):
        self.age = ageVal



def howMuchLeft(earth, human):
    F = earth.maxAge - human.age * (1 - 0.5 * abs(earth.s - earth.s0) * (earth.s - earth.s0) * cMax / earth.sMaxDif / earth.sMaxDif / human.skinColor -
                                        0.5 * abs(earth.t - earth.t0) * (earth.t - earth.t0) / earth.tMaxDif / earth.tMaxDif * human.fat)
    return F


def mutation(population):
    individual = random.choice(population)
    mutate_feature = random.randint(0, len(individual) - 1)
    if mutate_feature == 0:
        individual[mutate_feature] = random.randint(fMin, fMax)
    else:
        individual[mutate_feature] = random.randint(cMin, cMax)
    population[population.index(individual)] = individual
    return population


def crossover(ind1, ind2):
    child = tuple()
    for feature in xrange(len(ind1) - 1):
        child += ((ind1[feature] + ind2[feature]) / 2.0, )
    return child


def selection(population, size):
    fitness = []
    for individual in population:
        fitness.append()

def randomGeneration(size):
    generation = []
    for i in range(size):
        h = Human()
        generation.append(h)
    return generation

if __name__ == "main":
    earth = Earth()
    population = randomGeneration(10)

