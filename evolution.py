import random

POP_SIZE = 5
NUM_OFFSPRINGS = 5

cMax = 36
cMin = 1
cOpt = cMin + (cMax - cMin) / 2

tMax = 100
tMin = -60

sMax = 3000
sMin = 0

fMax = 50000000.
fMin = 0
fOpt = 0.5

pMax = 33
pMin = 0.356

lMax = 10
lMin = 2
lOpt = lMin + (lMax - lMin) / 2


class Earth:
    def __init__(self):
        self.t = random.uniform(tMin, tMax)
        self.s = random.uniform(sMin, sMax)
        self.p = random.uniform(pMin, pMax)
        self.t0 = tMin + (tMax - tMin) / 2
        self.s0 = sMin + (sMax - sMin) / 2
        self.p0 = pMin + (pMax - pMin) / 2
        self.maxAge = 122
        self.sMaxDif = max(abs(sMax - self.s0), abs(sMin - self.s0))
        self.tMaxDif = max(abs(tMax - self.t0), abs(tMin - self.t0))
        self.pMaxDif = max(abs(pMax - self.p0), abs(pMin - self.p0))


class Human:
    def __init__(self):
        self.fat = random.uniform(fMin, fMax) / fMax
        self.skinColor = random.randint(cMin, cMax)
        self.lung = random.uniform(lMin, lMax)
        self.age = 80
        self.fMaxDif = max(abs(1 - fOpt), abs(0 - fOpt))
        self.skinMaxDif = max(abs(cMax - cOpt), abs(cMin - cOpt))
        self.lMaxDif = max(abs(lMax - lOpt), abs(lMin - lOpt))

    def __len__(self):
        return 3

    def setFat(self, fatVal):
        self.fat = fatVal / fMax
        print fatVal, ' ', self.fat

    def setSkinColor(self, skinColorVal):
        self.skinColor = skinColorVal

    def setAge(self, ageVal):
        self.age = ageVal

    def setLung(self, pressureVal):
        self.pressure = pressureVal


def howMuchLeft(earth, human):
    coef = 1. \
    - 1 / 3. * abs(earth.s - earth.s0) / earth.sMaxDif * abs(human.skinColor - cOpt) / human.skinMaxDif \
    - 1 / 3. * abs(earth.t - earth.t0) / earth.tMaxDif * abs(human.fat * 2 - fOpt) / human.fMaxDif \
    - 1 / 3. * abs(earth.p - earth.p0) / earth.pMaxDif * abs(human.lung - lOpt) / human.lMaxDif
    F = earth.maxAge * (coef**10) * 17 / 20.
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
                new_individual.setFat(random.uniform(fMin, fMax))
                new_individual.setSkinColor(individual.skinColor)
                new_individual.setLung(individual.lung)
            elif mutate_feature == 1:
                new_individual.setFat(individual.fat * fMax)
                new_individual.setSkinColor(random.randint(cMin, cMax))
                new_individual.setLung(individual.lung)
            else:
                new_individual.setFat(individual.fat * fMax)
                new_individual.setSkinColor(individual.skinColor)
                new_individual.setLung(random.uniform(lMin, lMax))
            generation.append(new_individual)
    return generation


def crossover(ind1, ind2):
    h = Human()
    h.setFat((ind1.fat + ind2.fat) / 2)
    h.setAge((ind1.skinColor + ind2.skinColor) / 2)
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
            return (population[i].fat, population[i].skinColor, population[i].lung)
    return False


earth = Earth()
population = randomGeneration(POP_SIZE)
count = 0
while True:
    for guy in population:
        print guy.skinColor, ' ', guy.fat, ' ', guy.lung, ' ', howMuchLeft(earth, guy)
        pass
    temp = satisfied(earth, population)
    if (temp != False):
        print "We have a winner", count
        print temp
        break
    new_population = newMutateGeneration(population)
    population = selection(new_population, earth, POP_SIZE)
    ages = []
    count += 1
