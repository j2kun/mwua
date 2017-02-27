import random
import numpy


# draw: [float] -> int
# pick an index from the given list of floats proportionally
# to the size of the entry (i.e. normalize to a probability
# distribution and draw according to the probabilities).
def draw(weights):
    choice = random.uniform(0, sum(weights))
    choiceIndex = 0

    for weight in weights:
        choice -= weight
        if choice <= 0:
            return choiceIndex

        choiceIndex += 1


# MWUA: the multiplicative weights update algorithm
def MWUA(objects, observeOutcome, reward, learningRate, numRounds):
    weights = [1] * len(objects)
    cumulativeReward = 0
    outcomes = []

    for t in range(numRounds):
        assert all(w >= 0 for w in weights)
        chosenObjectIndex = draw(weights)
        chosenObject = objects[chosenObjectIndex]

        outcome = observeOutcome(t, weights, chosenObject)
        outcomes.append(outcome)
        thisRoundReward = reward(chosenObject, outcome)
        cumulativeReward += thisRoundReward

        for i in range(len(weights)):
            weights[i] *= (1 + learningRate * reward(objects[i], outcome))

    return weights, cumulativeReward, outcomes


class InfeasibleException(Exception):
    pass


# create an oracle to solve the one-constraint optimization problem:
# (vector, scalar) -> find nonngeative x in { x : c.dot(x) = optimalValue }
#                     such that vector.dot(x) >= scalar
def makeOracle(c, optimalValue):
    n = len(c)

    def oracle(weightedVector, weightedThreshold):
        def quantity(i):
            return weightedVector[i] * optimalValue / c[i] if c[i] > 0 else -1

        biggest = max(range(n), key=quantity)
        if quantity(biggest) < weightedThreshold:
            raise InfeasibleException

        output = numpy.array([optimalValue / c[i] if i == biggest else 0 for i in range(n)])
        return output

    return oracle


# Solve a linear program of the form
#       min  c.dot(x)
#       s.t. Ax >= b, x >= 0
# given an optimal value for c.dot(x)
def solveGivenOptimalValue(A, b, linearObjective, optimalValue, learningRate=0.1):
    m, n = A.shape  # m equations, n variables
    oracle = makeOracle(linearObjective, optimalValue)

    # the reward function for the LP solver
    def reward(i, specialVector):
        constraint = A[i]
        threshold = b[i]
        return threshold - numpy.dot(constraint, specialVector)

    def observeOutcome(_, weights, __):
        weights = numpy.array(weights)
        weightedVector = A.transpose().dot(weights)
        weightedThreshold = weights.dot(b)
        return oracle(weightedVector, weightedThreshold)

    numRounds = 1000
    weights, cumulativeReward, outcomes = MWUA(
        range(m), observeOutcome, reward, learningRate, numRounds
    )
    averageVector = sum(outcomes) / numRounds

    return averageVector


def example():
    A = numpy.array([[1, 2, 3], [0, 4, 2]])
    b = numpy.array([5, 6])
    c = numpy.array([1, 2, 1])
    z = 3

    x = solveGivenOptimalValue(A, b, c, z)
    print(x)
    print(c.dot(x))
    print(A.dot(x) - b)


# Solve a linear program of the form
#       min  c.dot(x)
#       s.t. Ax >= b, x >= 0
def solve(A, b, linearObjective, maxRange=1000):
    optRange = [0, maxRange]

    while optRange[1] - optRange[0] > 1e-8:
        proposedOpt = sum(optRange) / 2
        print("Attempting to solve with proposedOpt=%G" % proposedOpt)

        # Because the binary search starts so high, it results in extreme
        # reward values that must be tempered by a slow learning rate. Exercise
        # to the reader: determine absolute bounds for the rewards, and set
        # this learning rate in a more principled fashion.
        learningRate = 1 / max(2 * proposedOpt * c for c in linearObjective)
        learningRate = min(learningRate, 0.1)

        try:
            result = solveGivenOptimalValue(A, b, linearObjective, proposedOpt, learningRate)
            optRange[1] = proposedOpt
        except InfeasibleException:
            optRange[0] = proposedOpt

    return result


if __name__ == "__main__":
    A = numpy.array([[1, 2, 3], [0, 4, 2]])
    b = numpy.array([5, 6])
    c = numpy.array([1, 2, 1])

    x = solve(A, b, c)
    print(x)
    print(c.dot(x))
    print(A.dot(x) - b)
