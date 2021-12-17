import numpy as np
from random import random

def dropPiece(board, col):
    '''
    Drops a piece for the player in the specified column on the board. If the column is full, no piece will be placed
    and an error message will be returned.

    Inputs:
        board: 2D numpy array representing the board
        col: An integer between 0 and 6 representing the column to drop a piece

    Outputs:
        success: A Boolean representing whether the move was executed successfully
    '''


    spot = False
    for i in range(6):
        if board[5-i,col] == 0:
            spot=True
            break
    
    if spot:
        board[5-i, col] = 1
        return True
    else:
        return False


def checkValidCols(board):
    '''
    Returns a list of all non-empty columns in the game currently

    Inputs:
        board: 2D numpy array representing the board

    Outputs:
        validCols: A list containing the integer indices of all non-empty columns
    '''
    return [i for i in range(7) if int(board[0, i]) == 0]


class NeuralNetwork:
    def __init__(self, w, layers=3, layerSizes = [42, 15, 7]):
        self.layers = layers
        self.layerSizes = layerSizes
        self.weights = []


        for i in range(layers-1):
            self.weights.append(w[0:layerSizes[i]*layerSizes[i+1]].reshape((layerSizes[i], layerSizes[i+1])))

    def process(self, board):
        # Flatten board
        firstNodes = board.flatten()
        secondNodes = np.zeros((self.layerSizes[1],1))

        # Through layers of weights
        for i in range(self.layers-1):
            secondNodes = np.zeros((self.layerSizes[i+1]))

            currentWeights = self.weights[i]
            # Through resultant nodes
            for j in range(self.layerSizes[i+1]):
                secondNodes[j] = np.dot(firstNodes, currentWeights[:,j])

            firstNodes = np.copy(secondNodes)

        self.nodes = firstNodes


def ratMove(board, rat):

    validCols = checkValidCols(board)
    
    rat.process(board)
    nodes = rat.nodes
    # Get the highest score out of the valid cols
    validNodes = []
    for c in validCols:
        validNodes.append(nodes[c])
    
    col = validCols[np.argmax(np.array(validNodes))]
    dropPiece(board,col)






