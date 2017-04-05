import random


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

    for t in range(numRounds):
        chosenObjectIndex = draw(weights)
        chosenObject = objects[chosenObjectIndex]

        outcome = observeOutcome(t, weights, chosenObject)
        thisRoundReward = reward(chosenObject, outcome)
        cumulativeReward += thisRoundReward

        for i in range(len(weights)):
            weights[i] *= (1 + learningRate * reward(objects[i], outcome))

    return weights
