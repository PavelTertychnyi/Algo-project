import math
import random

POP_SIZE = 23
NUM_OFFSPRINGS = 10

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

    def __len__(self):
        return 2

    def setFat(self, fatVal):
        self.fat = fatVal / 50.

    def setSkinColor(self, skinColorVal):
        self.skinColor = skinColorVal

    def setAge(self, ageVal):
        self.age = ageVal


def howMuchLeft(earth, human):
    F = earth.maxAge - human.age * (
    1 - 0.5 * abs(earth.s - earth.s0) * (earth.s - earth.s0) * cMax / earth.sMaxDif / earth.sMaxDif / human.skinColor -
    0.5 * abs(earth.t - earth.t0) * (earth.t - earth.t0) / earth.tMaxDif / earth.tMaxDif * human.fat)
    return F


def mutation(population):
    individual = random.choice(population)
    mutate_feature = random.randint(0, len(individual) - 1)
    if mutate_feature == 0:
        individual.setFat(random.randint(fMin, fMax))
    else:
        individual.setSkinColor(random.randint(cMin, cMax))
    population[population.index(individual)] = individual
    return population

def newMutateGeneration(population):
    generation = []
    for individual in population:
        for i in range(NUM_OFFSPRINGS):
            mutate_feature = random.randint(0, len(individual) - 1)
            new_individual = Human()
            if mutate_feature == 0:
                new_individual.setFat(random.randint(fMin, fMax))
                new_individual.setSkinColor(individual.skinColor)
            else:
                new_individual.setFat(individual.fat)
                new_individual.setSkinColor(random.randint(cMin, cMax))
            generation.append(new_individual)
    return generation


def crossover(ind1, ind2):
    h = Human()
    h.setFat((ind1.fat + ind2.far) / 2)
    h.setAge((ind1.skinColor + ind2.skinColor) / 2)
    return h


def selection(population, planet, size):
    fitness = []
    for i, individual in enumerate(population):
        fitness.append((howMuchLeft(planet, individual), i))
    fitness.sort(key=lambda x: x[0], reverse=True)
    strongest = fitness[:size]
    new_generation = [population[j] for i, j in strongest]
    return new_generation


def randomGeneration(size):
    generation = []
    for i in range(size):
        h = Human()
        generation.append(h)
    return generation

def satisfied(earth, population):
    for i in range(len(population)):
        if howMuchLeft(earth, population[i]) >= 0:
            return (population[i].fat, population[i].skinColor)
    return False


earth = Earth()
population = randomGeneration(POP_SIZE)
count = 0
while True:
    new_population = newMutateGeneration(population)
    population = selection(new_population, earth, POP_SIZE)
    ages = []
    if satisfied(earth, population) != False:
        print "We have a winner", count

        break
    count += 1




