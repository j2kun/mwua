'use strict';

var state = {
    objects: [1, 2, 3, 4],
    weights: [1, 1, 1, 1],
    learningRate: 0.5,
    roundRewards: [],
    cumulativeRewards: [0, 0, 0, 0]
};

function sum(arr) {
    return arr.reduce(function (sum, x) {
        return sum + x;
    });
}

// Choose an index of the weights array at random, proportionally to the value
// at that index.
function draw(weights) {
    var choice = Math.random() * sum(weights);
    var choiceIndex = 0;

    var _iteratorNormalCompletion = true;
    var _didIteratorError = false;
    var _iteratorError = undefined;

    try {
        for (var _iterator = weights[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
            var weight = _step.value;

            choice = choice - weight;
            if (choice <= 0) {
                return choiceIndex;
            }

            choiceIndex += 1;
        }
    } catch (err) {
        _didIteratorError = true;
        _iteratorError = err;
    } finally {
        try {
            if (!_iteratorNormalCompletion && _iterator.return) {
                _iterator.return();
            }
        } finally {
            if (_didIteratorError) {
                throw _iteratorError;
            }
        }
    }

    throw { 'error': 'How did I get here? Is this real life?' };
}

function selectObject(objects, weights) {
    return objects[draw(weights)];
}

function mwuaStep(objects, weights, chosenObject, chosenRewards, learningRate) {
    var chosenObjectIndex = objects.indexOf(chosenObject);
    for (var i = 0; i < weights.length; i++) {
        weights[i] *= 1 + learningRate * chosenRewards[i];
    }
}

function executeRound(chosenObject, chosenRewards) {
    mwuaStep(state.objects, state.weights, chosenObjects, chosenRewards, state.learningRate);
    state.roundRewards.push(chosenRewards);
    for (var i = 0; i < chosenRewards.length; i++) {
        state.cumulativeRewards[i] += chosenRewards[i];
    }

    updateUI(chosenRewards);
}

function updateUI(chosenRewards) {
    var row = chosenRewards.map(function (n) {
        return '<td>' + n.toString() + '</td>';
    }).join('');
    // TODO: remove chosenRewards class from last row, remove input fields and replace with text of chosenRewards
    $('#rewards tr:last').after('<tr>' + row + '</tr>');
    // TODO: add new input row to rewards table
    /*
        <th id="round0">Round 1: </th>
            <td><input>1</input></td>
            <td><input>1</input></td>
            <td><input>1</input></td>
            <td><input>1</input></td>
        </tr>
    */
    // TODO: update cumulativeRewards row
    // TODO: update chosenObject span and mwuaBest span
}

/*
document.getElementById('calcBtn').addEventListener('click', function () {
   return;
});
*/

// selectObject(state.objects, state.weights)
// mwuaStep(state.objects, state.weights, 2, [2,3,4,5], state.learningRate)
