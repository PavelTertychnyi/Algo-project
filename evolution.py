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
        t = random.randint(tMin, tMax)
        s = random.randint(sMin, sMax)
        t0 = 20
        s0 = 1367
        maxAge = 122
        c1 = 0.5
        c2 = 0.5
        sMaxDif = max(abs(sMax - s0), abs(sMin - s0))
        tMaxDif = max(abs(tMax - t0), abs(tMin - t0))


class Human:
    def __init__(self):
        fat = random.randint(fMin, fMax) / 50.
        skinColor = random.randint(cMin, cMax)
        age = 80

    def setFat(self, fatVal):
        self.fat = fatVal

    def setSkinColor(self, skinColorVal):
        self.skinColor = skinColorVal

    def setAge(self, ageVal):
        age = ageVal



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


def selection(population, planet, size):
    fitness = []
    for i, individual in enumerate(population):
        fitness.append(0 - howMuchLeft(planet, individual), i)
    fitness.sort(key=lambda x: x[0])
    strongest = fitness[:size + 1]
    new_generation = [population[j] for i, j in strongest]
    return new_generation





