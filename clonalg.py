import math
from random import uniform
import matplotlib.pyplot as plt

Max_it = 50
n1 = N = 50
n2 = 0
B = 0.1
Nc = B*N  # clone amount
p = 5  # mutation equation parameter

global x
x = [0] * N
global y
y = [0] * N


def alpine02(x1, x2):
    alpineI1 = math.sqrt(x1) * math.sin(x1)
    alpineI2 = math.sqrt(x2) * math.sin(x2)

    return alpineI1 * alpineI2


def initializePopulation():
    for i in range(N):
        x[i] = uniform(0, 10)
        y[i] = uniform(0, 10)


def findAlpineValues(alpineX, alpineY):
    alpineValues = []
    for i in range(len(alpineX)):
        alpineValues.append(
            {"position": i, "fitness": alpine02(alpineX[i], alpineY[i])})

    return alpineValues


def sortN1ByBestFitness(f):
    sortedAlpineByFitness = sorted(f, key=lambda k: k["fitness"], reverse=True)
    return sortedAlpineByFitness[:n1]


def sortByWorstFitness(f):
    sortedAlpineByFitness = sorted(f, key=lambda k: k["fitness"])
    return sortedAlpineByFitness


def sortByPosition(f):
    sortedByPosition = sorted(f, key=lambda k: k["position"])
    return sortedByPosition


def clone(p):
    clonesX = []
    clonesY = []
    clonesP = []
    biggestFitness = p[0]["fitness"]

    for element in p:
        clonesForThisElement = int(Nc * (element["fitness"] / biggestFitness))
        clonesForThisElementValue = 0 if clonesForThisElement < 0 else clonesForThisElement
        for i in range(clonesForThisElementValue):
            clonesX.append(x[element["position"]])
            clonesY.append(y[element["position"]])

    clonesP = findAlpineValues(clonesX, clonesY)
    return clonesX, clonesY, clonesP


def mutate(cx, cy, cp):
    biggestFitness = cp[0]["fitness"]
    mutateX = []
    mutateY = []

    for element in cp:
        fitnessRelation = element["fitness"] / biggestFitness
        position = element["position"]

        mutationRate = math.exp(-p * fitnessRelation)  # 0 to biggest fitness

        valueToMaxX = 10 - cx[position]
        mutateX.append(cx[position] + uniform(
            -cx[position] * mutationRate,
            valueToMaxX * mutationRate
        ))

        valueToMaxY = 10 - cy[position]
        mutateY.append(cy[position] + uniform(
            -cy[position] * mutationRate,
            valueToMaxY * mutationRate
        ))

    x[:] = x + mutateX
    y[:] = y + mutateY
    return x, y


def replace(p1):
    for i in range(n2):
        position = p1[i]["position"]
        x[position] = uniform(0, 10)
        y[position] = uniform(0, 10)


def clonalg_opt():
    initializePopulation()

    for i in range(Max_it):
        f = findAlpineValues(x, y)
        p1 = sortN1ByBestFitness(f)
        # clone amount is based on affinity
        cx, cy, cp = clone(p1)
        # mutation is inversely proportional to affinity and adds in x and y
        c1x, c1y = mutate(cx, cy, cp)
        f1 = findAlpineValues(c1x, c1y)
        p1 = sortByWorstFitness(f1)
        # replace n2 elements of lower fitness with randomly generated new ones
        replace(p1)

    # graph plot
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.set(xlabel='x1', ylabel='x2', zlabel='Fitness',
           title='Curva todas as geração')
    p1 = sortByPosition(p1)

    for i in range(len(x)):
        ax.scatter(x[i], y[i], p1[i]["fitness"])

    plt.show()


clonalg_opt()
