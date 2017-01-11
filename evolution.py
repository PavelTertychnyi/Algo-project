import math
import random

POP_SIZE = 5
NUM_OFFSPRINGS = 5

cMax = 36
cMin = 1
cOpt = 18

tMax = 100
tMin = -60

sMax = 3000
sMin = 0

fMax = 50000000.
fMin = 0
fOpt = 0.5


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
        self.fat = random.randint(fMin, fMax) / fMax
        self.skinColor = random.randint(cMin, cMax)
        self.age = 80
        self.fMaxDif = max(abs(1 - fOpt), abs(0 - fOpt))
        self.skinMaxDif = max(abs(cMax - cOpt), abs(cMin - cOpt))

    def __len__(self):
        return 2

    def setFat(self, fatVal):
        self.fat = fatVal / fMax
        #print fatVal, ' ', self.fat

    def setSkinColor(self, skinColorVal):
        self.skinColor = skinColorVal

    def setAge(self, ageVal):
        self.age = ageVal


def howMuchLeft(earth, human):
    coef = 1. - 0.5 * abs(earth.s - earth.s0) / earth.sMaxDif * abs(human.skinColor - cOpt) / human.skinMaxDif - 0.5 * abs(earth.t - earth.t0) / earth.tMaxDif * abs(human.fat * 2 - fOpt) / human.fMaxDif
    F = earth.maxAge * (coef**10) * 4.5 / 5.
    print "F", F, ' ', F - human.age, ' ', human.age
    return  F - human.age


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
                new_individual.setFat(individual.fat * fMax)
                new_individual.setSkinColor(random.randint(cMin, cMax))
            generation.append(new_individual)
    return generation


def crossover(ind1, ind2):
    h = Human()
    h.setFat((ind1.fat + ind2.fat) / 2 * fMax)
    h.setSkinColor((ind1.skinColor + ind2.skinColor) / 2)
    #print "children", h.fat, h.skinColor
    return h


def selection(population, planet, size):
    fitness = []
    for i, individual in enumerate(population):
        fitness.append((howMuchLeft(planet, individual), i))
    fitness.sort(key=lambda x: x[0], reverse=True)
    #print fitness
    strongest = fitness[:size]
    #print strongest
    new_generation = [population[j] for i, j in strongest]
    #print new_generation
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
            return (population[i].fat, population[i].skinColor, howMuchLeft(earth, population[i]))
    return False


def randomCrossoverGeneration(population):
    generation = []
    pairs = []
    p = choseParent(population)
    #print p[0].fat, p[0].skinColor, "\t", p[1].fat, p[1].skinColor
    pairs.append(p)
    pairs.append((p[1], p[0]))
    h = crossover(p[0], p[1])
    generation.append(h)
    while len(generation) != NUM_OFFSPRINGS:
        p = choseParent(population)
        #print p
        if p not in pairs:
            pairs.append(p)
            pairs.append((p[1], p[0]))
            #print p[0].fat, p[0].skinColor, "\t", p[1].fat, p[1].skinColor
            h = crossover(p[0], p[1])
            generation.append(h)
    return shiftMutation(generation)

def shiftMutation(population):
    mutants = []
    for individ in population:

        for j in range(10):
            mutate_feature = random.randint(0, len(individ) - 1)
            new_individual = Human()
            change = random.uniform(-0.1, 0.1)
            if mutate_feature == 0:
                new_individual.setFat(individ.fat * fMax * (1 + change))
                new_individual.setSkinColor(individ.skinColor)
            else:
                new_individual.setFat(individ.fat * fMax)
                new_individual.setSkinColor(individ.skinColor * (1 + change))
            mutants.append(new_individual)
    return mutants


def choseParent(population):
    ind1 = random.choice(population)
    ind2 = random.choice(population)
    while ind2 == ind1:
        ind2 = random.choice(population)
    return (ind1, ind2)

def probabilityCrossoverGeneration(population, earth):
    generation = []
    ages = []
    total_age = 0
    for i in range(len(population)):
        a = population[i].age + howMuchLeft(earth, population[i])
        if a < 0:
            ages.append(0)
        else:
            ages.append(a)
            total_age += a
    prob = []
    prev = 0
    for i in range(len(population)):
        prob.append(ages[i] / float(total_age) + prev)
        prev = prob[i]
    for i in range(NUM_OFFSPRINGS):
        ind1 = chooseProbableParent(prob, population)
        ind2 = chooseProbableParent(prob, population)
        while ind2 == ind1:
            ind2 = chooseProbableParent(prob, population)
        h = crossover(ind1, ind2)
        generation.append(h)
    return generation

def chooseProbableParent(prob, population):
    toss = random.random()
    count = 0
    while toss > prob[count]:
        count += 1
    return population[count]


earth = Earth()
population = randomGeneration(POP_SIZE)
count = 0
while True:
    #for guy in population:
    #    print guy.skinColor, ' ', guy.fat, ' ', howMuchLeft(earth, guy)
    #    pass
    temp = satisfied(earth, population)
    if (temp != False):
        print "We have a winner", count
        print temp
        break
    new_population = randomCrossoverGeneration(population)
    population = selection(new_population, earth, POP_SIZE)
    ages = []


    count += 1
