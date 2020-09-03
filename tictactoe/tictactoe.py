"""
Tic Tac Toe Player
"""

import math
import itertools as it

from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    
    numX = numO = 0
    for row in board:
        for col in row:
            numX += col == X
            numO += col == O
    
    return X if numX == numO else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    ret = set()
    
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == EMPTY:
                ret.add((i, j))
    
    return ret


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    if board[action[0]][action[1]] != EMPTY:
        print(action, board)
        raise Exception("A move has already been made on this space")
    
    board[action[0]][action[1]] = player(board)
    return board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    # Check rows
    for row in board:
        if all(box == X for box in row):
            return X
        elif all(box == O for box in row):
            return O
    
    # Check columns
    for col in range(len(board[0])):
        if all(board[i][col] == X for i in range(3)):
            return X
        elif all(board[i][col] == O for i in range(3)):
            return O
    
    # Check diagonals
    if all(board[i][i] == X for i in range(3)):
        return X
    elif all(board[i][i] == O for i in range(3)):
        return O
    elif all(board[i][2 - 1] == X for i in range(3)):
        return X
    elif all(board[i][2 - i] == O for i in range(3)):
        return O
    
    # Check if board is full
    if all(board[i][j] != EMPTY for i, j in it.product(range(3), range(3))):
        return None
    
    # Otherwise, board is not full and has no winners
    raise Exception("Game is not over")


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    try:
        winner(board)
        return True
    except:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    
    try:
        win = winner(board)
        if win == X:
            return 1
        elif win == O:
            return -1

    except:
        pass

    return 0

# Define a function for value calculation
def minimaxValue(board, player):
    if terminal(board):
        return utility(board)

    v = -math.inf if player == X else math.inf

    # print(actions(board))
    for action in actions(board):
        # print(action, board, terminal(board))
        if player == X:
            v = max(v, minimaxValue(result(deepcopy(board), action), O))
        else:
            v = min(v, minimaxValue(result(deepcopy(board), action), X))
        
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # Calculate the current player
    currPlayer = player(board)
    nextPlayer = O if currPlayer == X else X
    
    # Return the move whose value is the best
    suggestedMove = None
    suggestedMoveValue = -math.inf if currPlayer == X else math.inf
    for action in actions(board):
        mmValue = minimaxValue(result(deepcopy(board), action), nextPlayer)
        if currPlayer == X and mmValue > suggestedMoveValue:
            suggestedMove = action
            suggestedMoveValue = mmValue
        elif currPlayer == O and mmValue < suggestedMoveValue:
            suggestedMove = action
            suggestedMoveValue = mmValue
    
    return suggestedMove


if __name__ == "__main__":
    testBoard = [['X', None, None], [None, 'X', None], ['O', None, 'O']]
    print(minimax(testBoard))
    