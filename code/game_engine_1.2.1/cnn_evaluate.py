import time
import numpy as np
from keras.models import load_model, Sequential
import paip_othello as othello

# model = load_model("CNN_cat_model_L_500.h5")
model = None


def load(path):
    model = load_model(path)
    print 'Model loaded'

def check_adjacent(square, board):
    for d in othello.DIRECTIONS4:
        if board[square + d] == othello.EMPTY:
            return True
    return False

def CNN_strategy(player, board):
    # player = othello.PIECES.index(player) # black-1, white-0
    data = np.empty((1, 10, 8, 8), dtype="int8")

    # gameboard = list(board[i] for i in othello.squares())
    # gameboard = list(list(gameboard[i-m*8] for m in xrange(8)) for i in xrange(56, 64))
    validmoves = othello.legal_moves(player, board)
    # validboard = list(int(i in validmoves) for i in othello.squares())
    # validboard = list(list(validboard[i-m*8] for m in xrange(8)) for i in xrange(56, 64))


    arr = np.zeros((10, 8, 8), dtype="int8")
    arr[9] = np.ones((8, 8), dtype="int8")

    for i in xrange(8):
        for j in xrange(8):
            square = i + j*10 + 11
            if square in validmoves:
                arr[4][i][j] = 1
            if board[square] == othello.EMPTY:
                arr[3][i][j] = 1
            else:
                if board[square] == player:
                    arr[1][i][j] = 1
                elif board[square] == othello.opponent(player):
                    arr[2][i][j] = 1
                if check_adjacent(square, board):
                    if board[square] == player:
                        arr[5][i][j] = 1
                    elif board[square] == othello.opponent(player):
                        arr[7][i][j] = 1
                else:
                    if board[square] == player:
                        arr[6][i][j] = 1
                    elif board[square] == othello.opponent(player):
                        arr[8][i][j] = 1

    data[0] = arr
    # print othello.print_board(board)
    # print arr
    # raw_input()

    cat = model.predict(data, batch_size=1)
    value = np.argmax(cat[0])
    if value > 8:
        value = value - 17

    return -value
