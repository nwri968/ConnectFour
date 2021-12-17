import numpy as np
from random import random
from random import seed
from MakeMoveNN import NeuralNetwork, ratMove
from GamePlayfunctions import *


def ratFight(rat1, rat2):
    '''
    Makes the two sets of weightings (rats) fight each other and returns the winner.

    Inputs:
        rat1: numpy array of weights
        rat2: numpy array of weights

    Outputs:
        player: 1 or 2 depending on the winner, or 0 if there is a tie
    '''

    board = np.zeros((6,7))
    player = 2

    r1 = NeuralNetwork(rat1)
    r2 = NeuralNetwork(rat2)

    while not checkWin(board) and not boardFull(board):
        player = flipBoard(board, player)
        ratMove(board, r1)

        if checkWin(board) or boardFull(board):
            break
        player = flipBoard(board, player)
        ratMove(board, r2)

    if checkWin(board):
        return player
    else:
        return 0


def topX(scores, X):
    '''
    Get the indices of the highest X numbers in the scores list.

    Inputs:
        scores: A list of score
        X: The number of highest items to pick

    Outputs:
        topIndices: A list of the indices of the highest scores
    '''
    return np.argpartition(scores, -X)[-X:]


def mutate(rat):
    return np.random.normal(rat, 0.1)


def writeRat(rat):
    '''
    Writes the rat into a text file
    '''
    f = open('Top_Rat.txt', 'w')
    for w in rat:
        f.write('{}\n'.format(w))

    f.close()


def trainNN():
    '''
    Plays the board game
    '''
    seed(152858796)
    rats = []
    scores = []
    epochs = 100
    # Create initial rat population
    num_rats = 200

    for n in range(num_rats):
        rats.append(np.array([random() for i in range(735)]))
        scores.append(0)

    # Loop through epochs
    for epoch in range(epochs):
        
        # Loop through rat pairs
        for i in range(num_rats):
            for j in range(num_rats):
                printProgressBar(i*num_rats+j, num_rats**2, prefix='Epoch {} of {}'.format(epoch, epochs))
                if not i==j:
                    rat1 = rats[i]
                    rat2 = rats[j]

                    result = ratFight(rat1, rat2)

                    # Process result
                    if result == 1:
                        scores[i] += 2
                    elif result == 2:
                        scores[j] += 2
                    else:
                        scores[i] += 1
                        scores[j] += 1

        # Now we need to use the performance of the rats to create the new generation

        # Select survivors
        topIndices = topX(scores, int(num_rats/4))
        rats_copy = rats.copy()
        rats_copy = [rats[i] for i in range(num_rats) if i in topIndices]
        rats = rats_copy.copy()

        # Produce offspring
        new_rats = rats.copy()
        for rat in rats:
            for _ in range(3):
                new_rats.append(mutate(rat))

        rats = new_rats.copy()

        # Crossover Events
        # None for now

    # Loop through rat pairs
    for i in range(num_rats):
        for j in range(num_rats):
            printProgressBar(i*num_rats+j, num_rats**2, prefix='Epoch {} of {}'.format(epochs, epochs))
            if not i==j:
                rat1 = rats[i]
                rat2 = rats[j]

                result = ratFight(rat1, rat2)

                # Process result
                if result == 1:
                    scores[i] += 2
                elif result == 2:
                    scores[j] += 2
                else:
                    scores[i] += 1
                    scores[j] += 1

    topRat = np.argmax(scores)

    writeRat(rats[topRat])                   


if __name__ == '__main__':
    trainNN()