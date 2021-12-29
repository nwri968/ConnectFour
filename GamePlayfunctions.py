import numpy as np

def printProgressBar (iteration, total, prefix = 'Progress:', suffix = 'Complete', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    '''
    Prints a nice little progress bar
    '''

    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


def checkWin(board):  
    '''
    Checks if the board contains a connect four.

    Inputs:
        board: 2D numpy array representing the board

    Outputs:
        win: A Boolean which is False unless there exists a connect four in the board
    '''

    # Check horizontal
    for row in range(6):
        count = 0
        for col in range(7):
            if board[row,col] == 1:
                count += 1
            else:
                count = 0
            if count == 4:
                return True

    # Check Vertical
    for col in range(7):
        count = 0
        for row in range(6):
            if board[row,col] == 1:
                count += 1
            else:
                count = 0
            if count == 4:
                return True

    # Check Diagonal
    startLocations1 = [[5,3], [5,4], [5,5], [5,6], [4,6], [3,6]]
    startLocations2 = [[5,3], [5,2], [5,1], [5,0], [4,0], [3,0]]

    # Up and left direction
    for start in startLocations1:
        row = start[0]
        col = start[0]
        count = 0
        while row >= 0 and col >= 0:
            if board[row,col] == 1:
                count += 1
            else:
                count = 0
            if count == 4:
                return True

            row += -1
            col += -1

    # Up and right direction
    for start in startLocations2:
        row = start[0]
        col = start[0]
        count = 0
        while row >= 0 and col <= 6:
            if board[row,col] == 1:
                count += 1
            else:
                count = 0
            if count == 4:
                return True

            row += -1
            col += 1

    
    return False


def boardFull(board):
    return np.count_nonzero(board == 0) == 0


def flipBoard(board, player):
    '''
    Switches the board to the other player's turn by multiplying the board by -1, and switching the player number.

    Inputs:
        board: 2D numpy array representing the board
        player: A integer that is either 1 or 2 depending on which player's turn it is

    Outputs:
        player: The other player number
    '''

    board = board*-1

    return board, (3 - player)