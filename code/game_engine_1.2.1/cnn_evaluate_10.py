import time
import numpy as np
from keras.models import load_model, Sequential
import paip_othello as othello

# model = load_model("CNN_cat_model_L_500.h5")
model = None
cnn_time = 0
cnn_cnt = 0

BORDER = np.ones((10, 10), dtype="int8")
for i in range(1,9):
    for j in range(1,9):
        BORDER[i][j] = 0

def load(path):
    global model, cnn_time, cnn_cnt
    model = load_model(path)
    cnn_time = 0
    cnn_cnt = 0
    print 'Model loaded'

def check_adjacent(square, board):
    for d in othello.DIRECTIONS4:
        if board[square + d] == othello.EMPTY:
            return True
    return False

def CNN_strategy(player, board):
    global cnn_time, cnn_cnt
    start = time.time()
    # player = othello.PIECES.index(player) # black-1, white-0
    data = np.empty((1, 11, 10, 10), dtype="int8")

    # gameboard = list(board[i] for i in othello.squares())
    # gameboard = list(list(gameboard[i-m*8] for m in xrange(8)) for i in xrange(56, 64))
    validmoves = othello.legal_moves(player, board)
    # validboard = list(int(i in validmoves) for i in othello.squares())
    # validboard = list(list(validboard[i-m*8] for m in xrange(8)) for i in xrange(56, 64))


    arr = np.zeros((11, 10, 10), dtype="int8")
    arr[10] = np.ones((10, 10), dtype="int8")
    arr[9] = BORDER

    for i in xrange(1,9):
        for j in xrange(1,9):
            square = i + j*10
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
    cnn_time += time.time()-start
    cnn_cnt += 1

    return -value
