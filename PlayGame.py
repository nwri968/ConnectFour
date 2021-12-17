import numpy as np
from MakeMoveNN import ratMove, dropPiece, NeuralNetwork
from GamePlayfunctions import *

def playermove(board):

    print(board)
    col = int(input('\nEnter column to play: '))

    dropPiece(board, col)


def main():
    '''
    Plays the board game
    '''
    # Create AI
    weights = np.loadtxt('Top_Rat.txt')
    AI = NeuralNetwork(weights)

    # Begin game

    board = np.zeros((6,7))
    player = 2

    while not checkWin(board) and not boardFull(board):
        player = flipBoard(board, player)
        playermove(board)

        if checkWin(board) or boardFull(board):
            break
        player = flipBoard(board, player)
        ratMove(board, AI)

    if checkWin(board):
        if player == 1:
            print('You Win!')
        else:
            print('Rat Wins!')
    else:
        print('Draw')
        
    return 0


if __name__ == '__main__':
    main()