function uniform(min, max) {
  return Math.random() * (max - min) + min;
}

function initializeWeights(n) {
  var weights = new Array(n);
  for (var i = 0; i < weights.length; i++) {
    weights[i] = 1;
  }

  return weights;
}

function sample(weights) {
  // Sample an index proportionally to the size of the number at that index
  var sum = 0;
  for (var i = 0; i < weights.length; i++) {
    sum += weights[i];
  }

  choice = uniform(0, sum(weights))
  choiceIndex = 0

  for (var i = 0; i < weights.length; i++) {
    weight = weights[i];
    choice -= weight;
    if (choice <= 0) {
        return choiceIndex;
    }

    choiceIndex += 1;
  }
}
