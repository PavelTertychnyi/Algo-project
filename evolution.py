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
    F = earth.maxAge * (coef**6) * 17 / 20.
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
    h.setFat((ind1.fat + ind2.fat) / 2 * fMax)
    h.setSkinColor((ind1.skinColor + ind2.skinColor) / 2)
    #print "children", h.fat, h.skinColor
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
    count = 0
    averageAge = 0.
    for i in range(len(population)):
        yearsLeft = howMuchLeft(earth, population[i])
        averageAge += population[i].age + yearsLeft
        if yearsLeft >= 0:
            count += 1
    averageAge /= len(population)
    if (count == len(population)):
        return (population[i].fat, population[i].skinColor, population[i].lung, averageAge)
    return (False, averageAge)


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
    temp = satisfied(earth, population)
    averageAge = temp[-1]
    print "iteration ", count, " average age = ", averageAge
    if (temp[0] != False):
        print "We have a winner", count
        print temp[:-1]
        break
    new_population = randomCrossoverGeneration(population)
    population = selection(new_population, earth, POP_SIZE)
    ages = []


    count += 1
