import numpy as np
from random import random
from time import time

from numpy.lib.function_base import flip
from GamePlayfunctions import flipBoard

def dropPiece(board, col, player = 1):
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
        board[5-i, col] = player
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


def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(4):
		for r in range(6):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(7):
		for r in range(3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(4):
		for r in range(3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(4):
		for r in range(3, 6):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True


def evaluate_window(window):
    score = 0

    if window.count(1.) == 3 and window.count(0.) == 1:
        score += 5
    elif window.count(1.) == 2 and window.count(0.) == 2:
        score += 2

    if window.count(-1.) == 3 and window.count(0.) == 1:
        score += -5
    elif window.count(-1.) == 2 and window.count(0.) == 2:
        score += -2

    return score


def scoreBoard(board):
	score = 0

	## Score center column
	center_array = list(board[:, 3])
	center_count = center_array.count(1.)
	score += center_count

	## Score Horizontal
	for r in range(6):
		row_array = list(board[r,:])
		for c in range(4):
			window = row_array[c:c+4]
			score += evaluate_window(window)

	## Score Vertical
	for c in range(7):
		col_array = list(board[:,c])
		for r in range(3):
			window = col_array[r:r+4]
			score += evaluate_window(window)

	## Score posiive sloped diagonal
	for r in range(3):
		for c in range(4):
			window = [board[r+i][c+i] for i in range(4)]
			score += evaluate_window(window)

	for r in range(3):
		for c in range(4):
			window = [board[r+3-i][c+i] for i in range(4)]
			score += evaluate_window(window)

	return score


def minimaxAnalysis(board, depth, alpha, beta, MaxPlayer):
    if depth == 0:
        return (None, scoreBoard(board))

    if winning_move(board, 1.):
        return (None, 1000000)

    if winning_move(board, -1.):
        return (None, -1000000)

    if len(checkValidCols(board)) == 0:
        return(None, 0)

    if MaxPlayer:
        best = -1e99
        for c in checkValidCols(board):
            # Create a board copy with the next move made
            board_copy = np.copy(board)
            dropPiece(board_copy, c)

            # Score new board
            new_score = minimaxAnalysis(board_copy, depth-1, alpha, beta, False)[1]
            if new_score > best:
                best = new_score
                best_col = c

            alpha = max(alpha, best)

            if alpha >= beta:
                break

        return best_col, best

    else:
        worst = 1e99
        for c in checkValidCols(board):
            board_copy = np.copy(board)
            dropPiece(board_copy, c, player=-1)

            # Score new board
            new_score = minimaxAnalysis(board_copy, depth-1, alpha, beta, True)[1]
            if new_score < worst:
                worst = new_score
                worst_col = c

            beta = min(beta, worst)

            if alpha >= beta:
                break

        return worst_col, worst


def MMmove(board):

    depth = 5
    t1 = time()
    col, _ = minimaxAnalysis(board=board, depth=depth, alpha=-1e9, beta=1e9, MaxPlayer=True)
    print('AI found move in {}ms'.format(1000*(time()-t1)))

    dropPiece(board, col)

